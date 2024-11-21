# Built-in imports
from typing_extensions import TypedDict
import logging

# Internal imports
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.agents.AssistantAgent.AssistantAgentOutput import AssistantAgentOutput

class AgentState(TypedDict):
    assistantAgentInput: AssistantAgentInput
    asistantAgentOutput: AssistantAgentOutput


