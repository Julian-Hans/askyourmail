# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.graphs.MainGraph import MainGraph
from askyourmail.src.data.Email import Email


# external imports
from langsmith import Client
import gradio as gr
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)





# init langsmith client
client = Client()



def main(state: AgentState) -> None:
    log.info("Starting main")
    main_graph = MainGraph()
    final_state = main_graph.run(state)
    
    for email in final_state["retrievedEmails"]:
        log.info(f"Retrieved Mail ID: {email.thread_id}")

    log.info("-------")
    for email in final_state["relevantEmails"]:
        log.info(f"Relevant Mail ID: {email.thread_id}")

    log.info("-------")
    log.info(f"Query: {final_state['query']}")
    log.info(f"Answer: {final_state['answer']}")
if __name__ == "__main__":

    state: AgentState = {
        "query": """I got an email on 2002-05-08 12:09:29, sent by Joe, regarding renting from aztec. How much does it cost again?""",
    }
    main(state = state)
    