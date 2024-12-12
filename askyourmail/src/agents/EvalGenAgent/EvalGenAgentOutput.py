
from pydantic import BaseModel, Field

class EvalGenAgentOutput(BaseModel):
    """The output object for the EvalGenAgent.
    """
    query: str = Field(description="The query or question that is only answerable with the information from the email body.")
    context_query_from: str = Field(description="The query or question that is only answerable with the information from the email body, including information about the sender of the email (derived of the from field), but without information about the date the email was received.")
    context_query_date: str = Field(description="The query or question that is only answerable with the information from the email body, including information about the timeframe in which the email was received (derived of the from date field), but without information about who sent the email.")
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
    def from_dict(cls, data: dict):
        """Creates an instance of EvalGenAgentOutput from a dictionary.

        Args:
            data (dict): The dictionary containing the data.

        Returns:
            EvalGenAgentOutput: The instance created from the dictionary.
        """
        return cls(**data)

    def __str__(self):
        return f"EvalGenAgentOutput: result = {self.verdict})"
   