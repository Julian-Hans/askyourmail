# libraries
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
import copy

# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.agents.AssistantAgent.AssistantAgentInput import AssistantAgentInput
from askyourmail.src.agents.AssistantAgent.AssistantAgentOutput import AssistantAgentOutput

class AssistantAgent():
    
    def __init__(self, llm: BaseChatModel = None) -> None:
        if llm is None:
            self.llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        else:
            self.llm = llm
        
        self.agent = self._get_agent()
    
    def invoke(self, input: AssistantAgentInput) -> AssistantAgentOutput:
        return self.agent.invoke(copy.deepcopy(input).to_dict())