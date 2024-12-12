# Built-in imports
from typing_extensions import TypedDict
from typing import List

# Internal imports
from askyourmail.src.data.Email import Email
from askyourmail.src.data.Filter import Filter
from askyourmail.src.data.EvaluationPair import EvaluationPair

class AgentState(TypedDict):
    query: str
    extractedFilters: List[Filter]
    retrievedEmails: List[Email]
    relevantEmails: List[Email]
    answer: str
    usedSources: List[int]


class EvalGenAgentState(TypedDict):
    k: int 
    retrievedEmails: List[Email]
    evaluationPairs: List[EvaluationPair]
    