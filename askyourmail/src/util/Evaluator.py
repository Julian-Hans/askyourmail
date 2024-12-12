from askyourmail.src.data.EvaluationPair import EvaluationPair
from askyourmail.src.graphs.states.States import AgentState
from askyourmail.src.main import main

class Evaluator:
    def __init__(self, query, evaluation_pair: EvaluationPair):
        self.query = query
        self.evaluation_pair = evaluation_pair
        self.ground_truth_in_retrieved_emails = False
        self.ground_truth_in_relevant_emails = False
        self.ground_truth_in_answer = False
        self.evaluated = False
        self.final_state = None
    
    def construct_agent_state_from_evaluation_pair(self, query) -> AgentState:
        state = {
            "query" : query
        }
        return state

    def evaluate(self):
        agent_state = self.construct_agent_state_from_evaluation_pair(self.query)
        self.final_state=main(agent_state)

        
        # check if the ground truth threat is in the retrieved emails
        for retrieved_email in self.final_state["retrievedEmails"]:
            if retrieved_email.thread_id == self.evaluation_pair.email.thread_id:
                self.ground_truth_in_retrieved_emails = True

        # check if the ground truth threat is in the relevant emails
        for relevant_email in self.final_state["relevantEmails"]:
            if relevant_email.thread_id == self.evaluation_pair.email.thread_id:
                self.ground_truth_in_relevant_emails = True

        # check if the ground truth threat has been used by the answer agent
        for id in self.final_state["usedSources"]:
            if str(id) == self.evaluation_pair.email.thread_id:
                self.ground_truth_in_answer = True

        self.evaluated = True
        return self

    def to_string(self):
        result = (
            f"Thread_ID: {self.evaluation_pair.email.thread_id}\n"
            f"Query: {self.query}\n"
            f"Expected Answer: {self.evaluation_pair.eval_gen_agent_output.answer}\n"
            f"Generated Answer: {self.final_state['answer']}\n"
            f"Ground Truth in Retrieved Emails: {self.ground_truth_in_retrieved_emails}\n"
            f"Ground Truth in Relevant Emails: {self.ground_truth_in_relevant_emails}\n"
            f"Ground Truth in Answer: {self.ground_truth_in_answer}\n"
            f"Used Sources: {', '.join(map(str, self.final_state['usedSources']))}\n"
        )
        return result
    