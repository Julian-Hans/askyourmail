
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from pydantic import BaseModel, Field
from typing import List

class TimestampAgentOutput(BaseModel):
    """The output object for the TimestampAgent."""
    result: str = Field(description="The Timestamp or result to the provided query, generated with only the available email information.")
    used_sources: List[int] = Field(description="The thread_ids of the sources used to generate the Timestamp.")
    
    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        _res = self.__dict__
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: TimestampAgentOutput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"TimestampAgentOutput: result = {self.verdict})"
   