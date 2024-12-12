from askyourmail.src.data.Email import Email

class EvalGenAgentInput():
    """The input object for the EvalGenAgent.
    """
    def __init__(self, email: Email):
        self.email = email

    def to_dict(self):
        """Converts the object to a dictionary.

        Returns:
            dict: The input object as a dictionary.
        """        
        # Create a shallow copy of self.__dict__
        _res = self.__dict__.copy()
        
        # Update _res with the dictionary returned by email.to_dict()
        if hasattr(self.email, "to_dict") and callable(self.email.to_dict):
            _res.update(self.email.to_dict())
        
        return _res
            
    @classmethod
    def from_json(cls, data: dict):
        _obj: EvalGenAgentInput = cls(**data)
        return _obj
        
    def __str__(self):
        return f"EvalGenAgentInput: term = {self.term})" #TODO: remove or fix
   