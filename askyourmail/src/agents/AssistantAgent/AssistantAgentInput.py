

class AssistantAgentInput():
    """The input object for the AssistantAgent.
    """
    def __init__(self, term: str):
        self.term = term

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        _res = self.__dict__
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: AssistantAgentInput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"AssistantAgentInput: term = {self.term})"
   