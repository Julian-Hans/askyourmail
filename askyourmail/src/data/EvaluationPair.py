from askyourmail.src.data.Email import Email
from askyourmail.src.agents.EvalGenAgent.EvalGenAgentOutput import EvalGenAgentOutput
import json

class EvaluationPair:
    def __init__(self, email: Email, eval_gen_agent_output: EvalGenAgentOutput) -> None:
        self.email = email
        self.eval_gen_agent_output = eval_gen_agent_output

    def to_dict(self) -> dict:
        return {
            'email': self.email.to_dict(),
            'eval_gen_agent_output': self.eval_gen_agent_output.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        email = Email.from_dict(data['email'])
        eval_gen_agent_output = EvalGenAgentOutput.from_dict(data['eval_gen_agent_output'])
        return cls(email, eval_gen_agent_output)