# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.graphs.MainGraph import MainGraph

# external imports
import os
from langsmith import Client


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"askyourmail"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# init langsmith client
client = Client()



def main(state: AgentState) -> None:
    log.info("Starting main")
    main_graph = MainGraph()
    main_graph.run(state)


if __name__ == "__main__":
    state = AgentState()
    main(state = state)