# Built-in imports
from typing_extensions import TypedDict
import logging
from typing import List

# Internal imports
from askyourmail.src.data.Email import Email

class AgentState(TypedDict):
    query: str
    extractedFrom: str
    extractedTime: str
    retrievedEmails: List[Email]
    relevantEmails: List[Email]
    answer: str


