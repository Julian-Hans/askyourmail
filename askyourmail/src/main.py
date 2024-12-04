# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.graphs.MainGraph import MainGraph
from askyourmail.src.data.Email import Email

# external imports
from langsmith import Client


# init langsmith client
client = Client()



def main(state: AgentState) -> None:
    log.info("Starting main")
    main_graph = MainGraph()
    main_graph.run(state)


if __name__ == "__main__":

    sample_email_0 = Email(thread_id="0", subject="Python learning resources", from_="learn@python.com", to="me@me.com", body="Here are some resources to learn Python: https://www.python.org/", timestamp="2022-01-01")
    sample_email_1 = Email(thread_id="1", subject="Strawberry Cakes", from_="recipes@cooking.com", to="me@me.com", body="Discover our new strawberrycake recipes", timestamp="2020-01-01")
    sample_emails = [sample_email_0, sample_email_1]

    state: AgentState = {
        "query": "I received an email about learning python. Can you help me find it?",
        "retrievedEmails" : sample_emails,
        "relevantEmails": []
    }
    main(state = state)