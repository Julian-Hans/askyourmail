
# external imports
import logging
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from typing import Literal


# local imports
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.util.Constants import *
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.agents.AssistantAgent.AssistantAgent import AssistantAgent

class MainGraph():
    def __init__(self) -> None:
        llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        self.assistant_agent = AssistantAgent(llm)
        #self.assistant_agent_reflection = AssistantAgent(llm) # TODO: add reflection
        self.graph = self._compile_graph()

    def _compile_graph() -> CompiledGraph:
        workflow = StateGraph(AgentState)

        workflow.add_node("assistant", self._assistant_node)

       #workflow.add_edge("assistant", "assistant_reflector")

        #workflow.add_conditional_edges(
        #    "assistant_reflector",
        #    self._assistant_reflector_router,
        #    {
        #        "__continue__" : "assistant",
        #        "__end__" : END
        #    }
        #)

        return workflow.compile()
    
    def _assistant_reflector_router(self, state: AgentState) -> Literal["__continue__", "__end__"]:
        return "__end__"
    
    def _assistant_node(self, state: AgentState) -> AgentState:
        input: AssistantAgentInput = state["assistantInput"]

        # invoke agent
        result = self.assistant_agent.invoke(input)

        # package results back into state
        state["assistantOutput"] = result

        return state
    
    def run(self, state: AgentState) -> None:
        events = self.graph.stream(state, {"recursion_limit": 25})
        for s in events:
            print(s)
            print("----")