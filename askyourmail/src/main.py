# Local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.graphs.MainGraph import MainGraph
from askyourmail.src.data.Email import Email
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


# External imports
import gradio as gr
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Retain the main function
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
    # Test example
    state: AgentState = {
        "query": """I got an email on 2002-05-08 12:09:29, sent by Joe, regarding renting from Aztec. How much does it cost again?""",
    }
    main(state=state)

# chatbot main logic
def process_query(query: str) -> str:
    """
    Process the query using the chatbot's main logic and return the response.
    """
    state: AgentState = {
        "query": query
    }
    main_graph = MainGraph()
    final_state = main_graph.run(state)

    # Log retrieved emails and the final answer
    retrieved_emails = [
        f"Mail ID: {email.thread_id}, Content: {email.content}"
        for email in final_state.get("retrievedEmails", [])
    ]
    relevant_emails = [
        f"Mail ID: {email.thread_id}, Content: {email.content}"
        for email in final_state.get("relevantEmails", [])
    ]
    query_answer = final_state.get("answer", "No answer found.")

    # Prepare a readable response
    response = (
        f"Query: {query}\n\n"
        f"Answer: {query_answer}\n\n"
        f"Retrieved Emails:\n" + "\n".join(retrieved_emails) + "\n\n"
        f"Relevant Emails:\n" + "\n".join(relevant_emails)
    )

    return response

# Define the Gradio interface
def gradio_query_interface(query):
    """
    Wrap the process_query function for the Gradio interface.
    """
    return process_query(query)

app = gr.Interface(
    fn=gradio_query_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your email-related query here..."),
    outputs=gr.Textbox(label="Response"),
    title="Ask Your Mail Bot",
    description="Enter an email-related query to retrieve relevant email information."
)

if __name__ == "__main__":
    log.info("Launching Gradio Interface...")
    app.launch()
