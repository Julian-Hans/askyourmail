# libraries
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
import copy
from typing import List

# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.agents.ReflectionAgent.ReflectionAgentInput import ReflectionAgentInput
from askyourmail.src.agents.ReflectionAgent.ReflectionAgentOutput import ReflectionAgentOutput
from askyourmail.src.agents.prompts.PromptBlueprint import PromptBlueprint

class ReflectionAgent():
    
    def __init__(self, llm: BaseChatModel = None) -> None:
        log.info("Initializing ReflectionAgent")
        if llm is None:
            self.llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        else:
            self.llm = llm
        
        self.agent = self._get_agent()
    
    def invoke(self, input: ReflectionAgentInput) -> ReflectionAgentOutput:
        return self.agent.invoke(copy.deepcopy(input).to_dict())
    
    def batch(self, input: List[ReflectionAgentInput]) -> List[ReflectionAgentOutput]:
        """Wrapper around the RunnableSequence's (agent's) batch method. Similar to invoke but uses threading to process multiple inputs in parallel."""

        input_dict = [inp.to_dict() for inp in copy.deepcopy(input)]
        res = self.agent.batch(input_dict)
        return res 


    def _get_agent(self) -> RunnableSequence:
        blueprint = PromptBlueprint.get_blueprint(class_name=self.__class__.__name__, version="v1")
        prompt = ChatPromptTemplate.from_messages(blueprint, template_format="jinja2")
        structured_llm = self.llm.with_structured_output(ReflectionAgentOutput)
        return prompt | structured_llm
        