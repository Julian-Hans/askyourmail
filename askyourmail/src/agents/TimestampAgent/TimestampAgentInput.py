from askyourmail.src.data.Email import Email
from typing import List

class TimestampAgentInput():
    """The input object for the TimestampAgent.
    """
    def __init__(self, query: str, emails: List[Email]):
        self.query = query
        self.emails = emails

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        # Create a shallow copy of self.__dict__
        _res = self.__dict__.copy()
        
        # Replace the emails attribute with a list of dictionaries
        if isinstance(self.emails, list) and all(hasattr(email, "to_dict") and callable(email.to_dict) for email in self.emails):
            _res["emails"] = [email.to_dict() for email in self.emails]
        
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: TimestampAgentInput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"TimestampAgentInput: term = {self.term})" #TODO: remove or fix
   