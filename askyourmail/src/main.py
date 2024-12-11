import logging
import gradio as gr

from askyourmail.src.graphs.MainGraph import MainGraph
from askyourmail.src.graphs.states.States import AgentState

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

# Chatbot main logic
def process_query(query: str) -> str:
    state: AgentState = {"query": query}
    main_graph = MainGraph()
    final_state = main_graph.run(state)

    # Prepare a readable response
    retrieved_emails = [
        f"Mail ID: {email.thread_id}, Content: {email.content}"
        for email in final_state.get("retrievedEmails", [])
    ]
    relevant_emails = [
        f"Mail ID: {email.thread_id}, Content: {email.content}"
        for email in final_state.get("relevantEmails", [])
    ]
    query_answer = final_state.get("answer", "No answer found.")

    response = (
        f"Query: {query}\n\n"
        f"Answer: {query_answer}\n\n"
        f"Retrieved Emails:\n" + "\n".join(retrieved_emails) + "\n\n"
        f"Relevant Emails:\n" + "\n".join(relevant_emails)
    )

    return response

# Define the Gradio interface
app = gr.Interface(
    fn=process_query,
    inputs=gr.Textbox(lines=2, placeholder="Enter your email-related query here..."),
    outputs=gr.Textbox(label="Response"),
    title="Ask Your Mail Bot",
    description="Enter an email-related query to retrieve relevant email information."
)

if __name__ == "__main__":
    log.info("Launching Gradio Interface...")
    app.launch()
