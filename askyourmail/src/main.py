import logging
import gradio as gr

from askyourmail.src.graphs.MainGraph import MainGraph
from askyourmail.src.graphs.states.States import AgentState

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Retain the main function
def main(state: AgentState) -> AgentState:
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
    return final_state

# Chatbot main logic
def process_query(query: str) -> str:
    log.info("Processing query...")
    state: AgentState = {
        "query": query,
    }

    final_state = main(state)
    
    relevant_emails = final_state["relevantEmails"]
    answer = final_state["answer"]
    used_sources = final_state["usedSources"]
    query = final_state["query"]

    relevant_emails_filtered_by_used_sources = [email for email in relevant_emails if int(email.thread_id) in used_sources]
    relevant_emails_str = "\n-----------------\n".join(email.to_string() for email in relevant_emails_filtered_by_used_sources)
    
    response = (
        f"Query: {query}\n\n"
        f"Answer: {answer}\n\n"
        f"Relevant Email IDs:\n" + "\n".join(map(str, used_sources)) + "\n\n"
        f"Relevant Emails:\n==================\n{relevant_emails_str}\n=================="
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
    