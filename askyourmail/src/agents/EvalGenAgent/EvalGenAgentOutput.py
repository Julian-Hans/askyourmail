
from langchain_core.pydantic_v1 import BaseModel, Field

class EvalGenAgentOutput(BaseModel):
    """The output object for the EvalGenAgent.
    """
    query: str = Field(description="The query or question that is only answerable with the information from the email body.")
    context_query_from: str = Field(description="The query or question that is only answerable with the information from the email body, including information about the sender of the email (derived of the from field).")
    context_query_date: str = Field(description="The query or question that is only answerable with the information from the email body, including information about the timeframe in which the email was received (derived of the from date field).")
    context_query_combined: str = Field(description="The query or question that is only answerable with the information from the email body, including information about the sender of the email (derived of the from field) and information about the timeframe in which the email was received (derived of the from date field).")
    answer: str = Field(description="The answer to the query or question that is only answerable with the information from the email body.")
    specificness: int = Field(description="The specificness of the query, ranging from 0 to 2")
    valid_flag: bool = Field(description="The flag indicating if you are able to formulate a valid, human like query.")

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        _res = self.__dict__
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: EvalGenAgentOutput = cls(**data)
        return _obj
    
    @classmethod
    def to_json(self):
        """Converts the object to a JSON string.

        Returns:
            str: The input object as a JSON string.
        """
        return self.json()

    def __str__(self):
        return f"EvalGenAgentOutput: result = {self.verdict})"
   