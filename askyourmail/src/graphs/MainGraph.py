
# external imports
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import Literal
from typing import List
from langchain_chroma.vectorstores import Chroma
import chromadb
from langchain_openai import OpenAIEmbeddings


# local imports
from askyourmail.src.agents.AnswerAgent.AnswerAgentInput import AnswerAgentInput
from askyourmail.src.util.Constants import *
from askyourmail.src.util.TimedateParser import parse_date_range
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AnswerAgent.AnswerAgent import AnswerAgent
from askyourmail.src.agents.ReflectionAgent.ReflectionAgent import ReflectionAgent
from askyourmail.src.agents.ReflectionAgent.ReflectionAgentInput import ReflectionAgentInput
from askyourmail.src.agents.FilterAgent.FilterAgent import FilterAgent
from askyourmail.src.agents.FilterAgent.FilterAgentInput import FilterAgentInput
from askyourmail.src.data.Email import Email
from askyourmail.src.data.Filter import Filter, FromFilter, TimeFilter

class MainGraph():
    def __init__(self) -> None:
        llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        self.filter_agent = FilterAgent(llm)
        self.reflection_agent = ReflectionAgent(llm)
        self.answer_agent = AnswerAgent(llm)
        self.graph = self._compile_graph()

    def _compile_graph(self) -> CompiledGraph:
        log.info("Compiling MainGraph")
        workflow = StateGraph(AgentState)

        workflow.add_node("filter", self._filter_node)
        workflow.add_node("chroma_retrieval", self._chroma_retrieval_node)
        workflow.add_node("reflection", self._reflection_node)
        workflow.add_node("answer_", self._answer_node)

        workflow.add_edge("filter", "chroma_retrieval")
        workflow.add_edge("chroma_retrieval", "reflection")
        workflow.add_edge("reflection", "answer_")
        workflow.add_edge("answer_", END)

        workflow.set_entry_point("filter")
        return workflow.compile()
    
    def _assistant_reflector_router(self, state: AgentState) -> Literal["__continue__", "__end__"]:
        return "__end__"
    
    def _filter_node(self, state: AgentState) -> AgentState:
        log.info("Running Filter node")
        # get query from state
        query = state["query"]
        filterAgentInput = FilterAgentInput(query)
        # extract filters from query
        result = self.filter_agent.invoke(filterAgentInput)
        log.info(f"Filter Agent output: {result.time}")
        generated_filters = []
        if result.from_:
            from_filter = FromFilter(from_=result.from_)
            generated_filters.append(from_filter)
        if result.time:
            try: 
                date_start, date_end = parse_date_range(result.time)
                start_timestamp = int(date_start.timestamp())
                end_timestamp = int(date_end.timestamp())
                time_filter = TimeFilter(time=result.time, start_date=date_start, end_date=date_end, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
                generated_filters.append(time_filter)
            except:
                log.error(f"Could not parse date range: {result.time}. Skipping time filter.")
                # leave ranges as None

        # package collected data back into state
        state["extractedFilters"] = generated_filters
        for filter in generated_filters:
            log.info(f"Filter Agent extracted filter: {filter.to_string()}")
        return state

    def _chroma_retrieval_node(self, state: AgentState) -> AgentState:
        log.info("Running ChromaDB retrieval node")
        # get emails from chroma (similarity search with scores and top k)
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

        chroma_db = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
        )

        retrieved_emails = []
        retrieved_emails_filter = []
        retrieved_emails_combined_filter = []

        # standard (unfiltered) similarity search
        log.info("Running (naive) ChromaDB similarity search.")
        docs_results = chroma_db.similarity_search_with_relevance_scores(state["query"], k=RETRIEVAL_K_NAIVE)

        # create emails from retrieved docs
        for doc in docs_results:
            _tmp_mail = Email(thread_id=doc[0].metadata["thread_id"], subject=doc[0].metadata["subject"], from_=doc[0].metadata["from"], to=doc[0].metadata["to"], body=doc[0].metadata["body"], timestamp=doc[0].metadata["timestamp"])
            retrieved_emails.append(_tmp_mail)
        
        # use individual filters to search
        for filter in state["extractedFilters"]:
            log.info(f"Running filtered ChromaDB similarity search with filter: {filter.to_string()}")
            docs_results_with_filter = chroma_db.similarity_search_with_relevance_scores(state["query"], k=RETRIEVAL_K_PER_FILTER, filter=filter.to_chroma_filter())
            for doc in docs_results_with_filter:
                _tmp_mail = Email(thread_id=doc[0].metadata["thread_id"], subject=doc[0].metadata["subject"], from_=doc[0].metadata["from"], to=doc[0].metadata["to"], body=doc[0].metadata["body"], timestamp=doc[0].metadata["timestamp"])
                retrieved_emails_filter.append(_tmp_mail)
        
        # combine all filters to a single precise one
        log.info(f"Number of filters: {len(state['extractedFilters'])}")
        if len(state["extractedFilters"]) > 1:
            combined_filter = Filter() # init empty filter
            for index, filter in enumerate(state["extractedFilters"]):
                if index == 0:
                    combined_filter.chroma_filter = filter.to_chroma_filter()
                else:
                    combined_filter.chroma_filter = combined_filter.combine_and(combined_filter.chroma_filter, filter.to_chroma_filter())

            # run combined filter search 
            log.info(f"Running (combined filter) ChromaDB similarity search with filter: {combined_filter.to_string()}")
            combined_filter_docs_results = chroma_db.similarity_search_with_relevance_scores(state["query"], k=RETRIEVAL_K_NAIVE, filter=combined_filter.to_chroma_filter())
            # create emails from retrieved docs
            for doc in combined_filter_docs_results:
                _tmp_mail = Email(thread_id=doc[0].metadata["thread_id"], subject=doc[0].metadata["subject"], from_=doc[0].metadata["from"], to=doc[0].metadata["to"], body=doc[0].metadata["body"], timestamp=doc[0].metadata["timestamp"])
                retrieved_emails_combined_filter.append(_tmp_mail)

        all_retrieved_emails = retrieved_emails + retrieved_emails_filter + retrieved_emails_combined_filter
        # Compute overlaps between the three retrieved email lists
        naive_set = set((email.thread_id, email.subject, email.from_, email.to, email.body, email.timestamp) for email in retrieved_emails)
        filter_set = set((email.thread_id, email.subject, email.from_, email.to, email.body, email.timestamp) for email in retrieved_emails_filter)
        combined_filter_set = set((email.thread_id, email.subject, email.from_, email.to, email.body, email.timestamp) for email in retrieved_emails_combined_filter)

        overlap_naive_filter = naive_set & filter_set
        overlap_naive_combined = naive_set & combined_filter_set
        overlap_filter_combined = filter_set & combined_filter_set

        log.info(f"Overlap between naive and filter search: {len(overlap_naive_filter)} emails.")
        log.info(f"Overlap between naive and combined filter search: {len(overlap_naive_combined)} emails.")
        log.info(f"Overlap between filter and combined filter search: {len(overlap_filter_combined)} emails.")
        
        # Deduplicate emails (temporary solution)
        unique_emails = []
        seen = set()
        for email in all_retrieved_emails:
            email_tuple = (email.thread_id, email.subject, email.from_, email.to, email.body, email.timestamp)
            if email_tuple not in seen:
                seen.add(email_tuple)
                unique_emails.append(email)
        final_retrieved_emails = unique_emails

        # package emails back into state
        state["retrievedEmails"] = final_retrieved_emails
        log.info(f"ChromaDB retrieved (naive) {len(retrieved_emails)} emails.")
        log.info(f"ChromaDB retrieved (individual filter) {len(retrieved_emails_filter)} emails.")
        log.info(f"ChromaDB retrieved (combined filter) {len(retrieved_emails_combined_filter)} emails.")
        log.info(f"ChromaDB retrieved a total of: {len(all_retrieved_emails)} emails.")
        log.info(f"ChromaDB retrieved a total of: {len(final_retrieved_emails)} unique emails.")
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

    def _answer_node(self, state: AgentState) -> AgentState:
        # get relevant emails from state to answer the query
        input: AnswerAgentInput = AnswerAgentInput(state["query"], state["relevantEmails"])
        
        result = self.answer_agent.invoke(input)

        # package result back into the state
        state["answer"] = result.result # TODO: bad naming
        state["usedSources"] = result.used_sources
        
        log.info(f"AnswerAgent generated answer: {result.result}")
        log.info(f"AnswerAgent used sources: {result.used_sources}")
        return state

    
    def run(self, state: AgentState) -> AgentState:
        log.info("Running MainGraph")
        events = self.graph.stream(state, {"recursion_limit": 25}, stream_mode="values")
        final_state = None  # Initialize a variable to hold the final state

        for event in events:
            final_state = event  # Update the final state with the latest state

        return final_state  # Return the final state after processing all events
