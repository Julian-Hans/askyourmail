import logging
import gradio as gr

from askyourmail.src.graphs.EvaluationDatasetGeneratorGraph import EvaluationDatasetGeneratorGraph
from askyourmail.src.graphs.states.States import EvalGenAgentState
from askyourmail.src.util.Constants import *
import json

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Retain the main function
def main(state: EvalGenAgentState) -> EvalGenAgentState:
    log.info("Starting main")
    main_graph = EvaluationDatasetGeneratorGraph()
    final_state = main_graph.run(state)
    
    for email in final_state["retrievedEmails"]:
        log.info(f"Retrieved Mail ID: {email.thread_id}")

    log.info("-------")
    for email in final_state["relevantEmails"]:
        log.info(f"Relevant Mail ID: {email.thread_id}")

    log.info("-------")
    log.info(f"Query: {final_state['query']}")
    log.info(f"Answer: {final_state['answer']}")
    return final_state


if __name__ == "__main__":

    state: EvaluationDatasetGeneratorGraph = {
        "k": EVAL_GEN_BATCH_SIZE
    }
    final_state = main(state)
    with open(EVAL_GEN_DATASET_PATH, 'w') as f:
        json.dump(final_state["evaluationPairs"], f, indent=4)
    