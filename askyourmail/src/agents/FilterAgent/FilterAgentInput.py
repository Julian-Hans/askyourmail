from askyourmail.src.data.Email import Email
from typing import List

class FilterAgentInput():
    """The input object for the FilterAgent.
    """
    def __init__(self, query: str):
        self.query = query

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        # Create a shallow copy of self.__dict__
        _res = self.__dict__.copy()
        
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: FilterAgentInput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"FilterAgentInput: term = {self.term})" #TODO: remove or fix
   