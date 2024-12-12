
from pydantic import BaseModel, Field

class AssistantAgentOutput(BaseModel):
    """The output object for the AssistantAgent.
    """
    result: str = Field(description="The result of the AssistantAgent.")

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        _res = self.__dict__
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: AssistantAgentOutput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"AssistantAgentOutput: result = {self.result})"
   