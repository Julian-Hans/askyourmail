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
    return final_state


if __name__ == "__main__":

    state: EvaluationDatasetGeneratorGraph = {
        "k": EVAL_GEN_BATCH_SIZE
    }
    final_state = main(state)
    with open(EVAL_GEN_DATASET_PATH, 'w') as f:
        json.dump(
            [pair.to_dict() for pair in final_state["evaluationPairs"]],  # Convert each EvaluationPair to dict and dump
            f,
            indent=4
        )
    log.info(f"Generated evaluation dataset at {EVAL_GEN_DATASET_PATH}")