
# external imports
import logging
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import Literal
from typing import List
from langchain_chroma.vectorstores import Chroma
import chromadb
from langchain_openai import OpenAIEmbeddings


# local imports
from askyourmail.src.agents.EvalGenAgent.EvalGenAgent import EvalGenAgent
from askyourmail.src.agents.EvalGenAgent.EvalGenAgentInput import EvalGenAgentInput
from askyourmail.src.agents.EvalGenAgent.EvalGenAgentOutput import EvalGenAgentOutput
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import EvalGenAgentState
from askyourmail.src.data.Email import Email
from askyourmail.src.data.EvaluationPair import EvaluationPair
import random

class EvaluationDatasetGeneratorGraph():
    def __init__(self) -> None:
        llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        self.eval_gen_agent = EvalGenAgent(llm)
        self.graph = self._compile_graph()

    def _compile_graph(self) -> CompiledGraph:
        workflow = StateGraph(EvalGenAgentState)

        workflow.add_node("db_extract", self._db_extract_node)
        workflow.add_node("eval_generation", self._eval_generation_node)

        workflow.add_edge("db_extract", "eval_generation")
        workflow.add_edge("eval_generation", END)

        workflow.set_entry_point("db_extract")
        return workflow.compile()

    def _db_extract_node(self, state: EvalGenAgentState) -> EvalGenAgentState:
        # read all metadata from the emails2 collection and parse them to mail objects
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        db2 = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
        )
        db_all2 = db2.get(include=["metadatas"])
        
        emails_in_db = []

        for item in db_all2["metadatas"]:
            _tmp_email = Email(
                thread_id=item["thread_id"],
                subject=item["subject"],
                from_=item["from"],
                to=item["to"],
                body=item["body"],
                timestamp=item["timestamp"],
            )
            emails_in_db.append(_tmp_email)
        
        unique_emails_in_db = []
        seen = set()
        for email in emails_in_db:
            email_tuple = (email.thread_id, email.subject, email.from_, email.to, email.body, email.timestamp)
            if email_tuple not in seen:
                seen.add(email_tuple)
                unique_emails_in_db.append(email)

        k = EVAL_GEN_BATCH_SIZE  # Number of random emails to select
        if len(unique_emails_in_db) < k:
            k = len(unique_emails_in_db)  # Adjust k if there are fewer emails than k

        selected_emails = random.sample(unique_emails_in_db, k)
        state["retrievedEmails"] = selected_emails
        return state


    def _eval_generation_node(self, state: EvalGenAgentState) -> EvalGenAgentState:
        # get emails to be processed for query/answer pairs from state
        input: List[EvalGenAgentInput] = []
        for email in state["retrievedEmails"]:
            input.append(EvalGenAgentInput(email))
        
        results: List[EvalGenAgentOutput] = self.eval_gen_agent.batch(input)

        # package result back into the state
        evaluation_pairs: List[EvaluationPair] = []

        for i, res in enumerate(results):
            if res.valid_flag:
                _tmp_eval_pair = EvaluationPair(
                    email=input[i].email,
                    eval_gen_agent_output=res,
                )

        state["evaluationPairs"] = evaluation_pairs
        log.info(f"Evaluation Agent generated {len(evaluation_pairs)} valid evaluation pairs from {len(input)} retrieved mails.")
        return state

    
    
    def run(self, state: EvalGenAgentState) -> EvalGenAgentState:
        events = self.graph.stream(state, {"recursion_limit": 25}, stream_mode="values")
        final_state = None  # Initialize a variable to hold the final state

        for event in events:
            final_state = event  # Update the final state with the latest state

        return final_state  # Return the final state after processing all events
