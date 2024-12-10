
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from pydantic import BaseModel, Field
from typing import List

class FilterAgentOutput(BaseModel):
    """The output object for the FilterAgent."""
    from_: str = Field(description="The from email filter field. Generated with only the available email information.")
    time: str = Field(description="The time email filter field. Generated with only the available email information.")
    
    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        _res = self.__dict__
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: FilterAgentOutput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"FilterAgentOutput: result = {self.verdict})"
   