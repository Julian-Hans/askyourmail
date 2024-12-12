from askyourmail.src.data.Email import Email
from askyourmail.src.agents.EvalGenAgent.EvalGenAgentOutput import EvalGenAgentOutput
import json

class EvaluationPair:
    def __init__(self, email: Email, eval_gen_agent_output: EvalGenAgentOutput) -> None:
        self.email = email
        self.eval_gen_agent_output = eval_gen_agent_output

    def to_json(self) -> str:
        return json.dumps({
            'email': self.email.to_dict(),  # Assuming Email class has a to_dict method
            'eval_gen_agent_output': self.eval_gen_agent_output.to_dict()  # Assuming EvalGenAgentOutput class has a to_dict method
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'EvaluationPair':
        data = json.loads(json_str)
        email = Email.from_dict(data['email'])  # Assuming Email class has a from_dict method
        eval_gen_agent_output = EvalGenAgentOutput.from_dict(data['eval_gen_agent_output'])  # Assuming EvalGenAgentOutput class has a from_dict method
        return cls(email, eval_gen_agent_output)