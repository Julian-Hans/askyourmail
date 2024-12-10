# Built-in imports
from typing_extensions import TypedDict
import logging
from typing import List

# Internal imports
from askyourmail.src.data.Email import Email
from askyourmail.src.data.Filter import Filter

class AgentState(TypedDict):
    query: str
    extractedFilters: List[Filter]
    retrievedEmails: List[Email]
    relevantEmails: List[Email]
    answer: str


