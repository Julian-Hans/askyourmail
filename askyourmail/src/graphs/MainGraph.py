
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
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.agents.AssistantAgent.AssistantAgentOutput import AssistantAgentOutput
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AssistantAgent.AssistantAgent import AssistantAgent
from askyourmail.src.agents.ReflectionAgent.ReflectionAgent import ReflectionAgent
from askyourmail.src.agents.ReflectionAgent.ReflectionAgentInput import ReflectionAgentInput
from askyourmail.src.agents.ReflectionAgent.ReflectionAgentOutput import ReflectionAgentOutput
from askyourmail.src.data.Email import Email

class MainGraph():
    def __init__(self) -> None:
        llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        self.reflection_agent = ReflectionAgent(llm)
        self.graph = self._compile_graph()

    def _compile_graph(self) -> CompiledGraph:
        workflow = StateGraph(AgentState)

        workflow.add_node("chroma_retrieval", self._chroma_retrieval_node)
        workflow.add_node("reflection", self._reflection_node)

        workflow.add_edge("chroma_retrieval", "reflection")
        workflow.add_edge("reflection", END)
        #workflow.add_node("filter_extraction", self._filter_extraction_node)

        #workflow.add_edge("chroma_retrieval", "reflection")

        """workflow.add_conditional_edges(
            "reflection",
            self._reflection_router,
            {
                "__continue__" : "filter_extraction",
                "__end__" : END
            }
        )"""
        #workflow.add_edge("filter_extraction", "chroma_retrieval")
        #workflow.add_edge("chroma_retrieval", "reflection")

        #workflow.add_node("assistant", self._assistant_node)

       #workflow.add_edge("assistant", "assistant_reflector")

        #workflow.add_conditional_edges(
        #    "assistant_reflector",
        #    self._assistant_reflector_router,
        #    {
        #        "__continue__" : "assistant",
        #        "__end__" : END
        #    }
        #)

        workflow.set_entry_point("chroma_retrieval")
        return workflow.compile()
    
    def _assistant_reflector_router(self, state: AgentState) -> Literal["__continue__", "__end__"]:
        return "__end__"
    
    def _chroma_retrieval_node(self, state: AgentState) -> AgentState:
        # get emails from chroma (similarity search with scores and top k)
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

        chroma_db = Chroma(
            client=client,
            collection_name="emails",
            embedding_function=embeddings,
        )

        docs_results = chroma_db.similarity_search_with_relevance_scores(state["query"], k=RETRIEVAL_K)
        retrieved_emails = []
        # create emails from retrieved docs
        for doc in docs_results:
            _tmp_mail = Email(thread_id=doc[0].metadata["thread_id"], subject=doc[0].metadata["subject"], from_=doc[0].metadata["from"], to=doc[0].metadata["to"], body=doc[0].metadata["body"], timestamp=doc[0].metadata["timestamp"])
            retrieved_emails.append(_tmp_mail)

        # Deduplicate emails (temporary solution)
        unique_emails = []
        seen = set()
        for email in retrieved_emails:
            email_tuple = (email.thread_id, email.subject, email.from_, email.to, email.body, email.timestamp)
            if email_tuple not in seen:
                seen.add(email_tuple)
                unique_emails.append(email)
        retrieved_emails = unique_emails

        # package emails back into state
        state["retrievedEmails"] = retrieved_emails
        return state

    def _reflection_node(self, state: AgentState) -> AgentState:
        # get emails to be graded from state
        input: List[ReflectionAgentInput] = []
        for email in state["retrievedEmails"]:
            input.append(ReflectionAgentInput(state["query"], email))
        
        results = self.reflection_agent.batch(input)

        # package result back into the state
        relevant_emails = []

        for i, res in enumerate(results):
            if res.verdict:
                relevant_emails.append(input[i].email)

        log.info(f"ReflectionAgent found {len(relevant_emails)} emails relevant out of {len(input)} retrieved candidates.")
        state["relevantEmails"] = relevant_emails
        return state

    def _assistant_node(self, state: AgentState) -> AgentState:
        input: AssistantAgentInput = state["assistantAgentInput"]

        # invoke agent
        result = self.assistant_agent.invoke(input) 
        # package results back into state
        state["assistantAgentOutput"] = result

        return state
    
    def run(self, state: AgentState) -> AgentState:
        events = self.graph.stream(state, {"recursion_limit": 25}, stream_mode="values")
        final_state = None  # Initialize a variable to hold the final state

        for event in events:
            final_state = event  # Update the final state with the latest state

        return final_state  # Return the final state after processing all events
