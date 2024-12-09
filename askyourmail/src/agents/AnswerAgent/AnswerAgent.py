# libraries
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
import copy
from typing import List

# local imports
from askyourmail.src.util.Constants import *
from askyourmail.src.agents.AnswerAgent.AnswerAgentInput import AnswerAgentInput
from askyourmail.src.agents.AnswerAgent.AnswerAgentOutput import AnswerAgentOutput
from askyourmail.src.agents.prompts.PromptBlueprint import PromptBlueprint

class AnswerAgent():
    
    def __init__(self, llm: BaseChatModel = None) -> None:
        log.info("Initializing AnswerAgent")
        if llm is None:
            self.llm = ChatOpenAI(model=MODEL_NAME, openai_api_base=OPENAI_API_BASE)
        else:
            self.llm = llm
        
        self.agent = self._get_agent()
    
    def invoke(self, input: AnswerAgentInput) -> AnswerAgentOutput:
        return self.agent.invoke(copy.deepcopy(input).to_dict())

    def _get_agent(self) -> RunnableSequence:
        blueprint = PromptBlueprint.get_blueprint(class_name=self.__class__.__name__, version="v1")
        prompt = ChatPromptTemplate.from_messages(blueprint, template_format="jinja2")
        structured_llm = self.llm.with_structured_output(AnswerAgentOutput)
        return prompt | structured_llm
        