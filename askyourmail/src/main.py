# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.graphs.MainGraph import MainGraph

# external imports
import os
from langsmith import Client


# init langsmith client
client = Client()



def main(state: AgentState) -> None:
    log.info("Starting main")
    main_graph = MainGraph()
    main_graph.run(state)


if __name__ == "__main__":
    state: AgentState ={
        "assistantAgentInput": AssistantAgentInput("Hello world (input)!"),
        "assistantAgentOutput": None
    }
    main(state = state)