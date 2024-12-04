
from langchain_core.pydantic_v1 import BaseModel, Field

class ReflectionAgentOutput(BaseModel):
    """The output object for the ReflectionAgent.
    """
    verdict: bool = Field(description="The verdict of the Email Reflection. True when the email contains the information requested by the provided query. False if not.")

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        _res = self.__dict__
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: ReflectionAgentOutput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"ReflectionAgentOutput: result = {self.verdict})"
   