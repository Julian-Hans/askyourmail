import logging
import json
from typing import List

from askyourmail.src.main import main
from askyourmail.src.data.EvaluationPair import EvaluationPair
from askyourmail.src.util.Evaluator import Evaluator
from askyourmail.src.util.Constants import *
import pickle

def evaluate():
    # load list of evaluation pairs
    evaluation_dataset:List[EvaluationPair] = []
    with open(EVAL_GEN_DATASET_PATH_INPUT, 'r') as f:
        evaluation_dataset_string = json.load(f)
        for el in evaluation_dataset_string:
            _tmp_ev_pair = EvaluationPair.from_dict(el)
            evaluation_dataset.append(_tmp_ev_pair)

    log.info(f"Loaded {len(evaluation_dataset)} evaluation pairs from {EVAL_GEN_DATASET_PATH_INPUT}")
    evaluations_base = []
    evaluations_context_from = []
    evaluations_context_date = []
    evaluations_context_combined = []

    for eval_pair in evaluation_dataset:
        # base query
        log.info(f"Evaluating base query")
        evaluator_base = Evaluator(query=eval_pair.eval_gen_agent_output.query, evaluation_pair=eval_pair)
        evaluator_base.evaluate()
        evaluations_base.append(evaluator_base)

        # context from
        log.info(f"Evaluating from context")
        evaluator_context_from = Evaluator(query=eval_pair.eval_gen_agent_output.context_query_from, evaluation_pair=eval_pair)
        evaluator_context_from.evaluate()
        evaluations_context_from.append(evaluator_context_from)

        # context date
        log.info(f"Evaluating date context")
        evaluator_context_date = Evaluator(query=eval_pair.eval_gen_agent_output.context_query_date, evaluation_pair=eval_pair)
        evaluator_context_date.evaluate()
        evaluations_context_date.append(evaluator_context_date)

        # context combined
        log.info(f"Evaluating combined context")
        evaluator_context_combined = Evaluator(query=eval_pair.eval_gen_agent_output.context_query_combined, evaluation_pair=eval_pair)
        evaluator_context_combined.evaluate()
        evaluations_context_combined.append(evaluator_context_combined)

    # calculate final accuracies
    base_accuracy = sum([1 for el in evaluations_base if el.ground_truth_in_answer])/len(evaluations_base)
    context_from_accuracy = sum([1 for el in evaluations_context_from if el.ground_truth_in_answer])/len(evaluations_context_from)
    context_date_accuracy = sum([1 for el in evaluations_context_date if el.ground_truth_in_answer])/len(evaluations_context_date)
    context_combined_accuracy = sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])/len(evaluations_context_combined)


    for index, eval_pair in enumerate(evaluation_dataset):
        result = f"""
        --------------------------
        Evaluation pair {index + 1}/{len(evaluation_dataset)}

        ==Base query==:
        {evaluations_base[index].to_string()}

        ==Context from==:
        {evaluations_context_from[index].to_string()}

        ==Context date==:
        {evaluations_context_date[index].to_string()}

        ==Context combined==:
        {evaluations_context_combined[index].to_string()}
        --------------------------
        """
        print(result)

    results = f"""
    ==Parameters==:

    total k = {TOTAL_RETRIEVAL_K}
    retrieval k naive = {RETRIEVAL_K_NAIVE}
    retrieval k per filter = {RETRIEVAL_K_PER_FILTER}
    retrieval k combined filters = {RETRIEVAL_K_COMBINED_FILTERS}
    evaluation batch size = {len(evaluation_dataset)}

    ==Evaluation results==:

    Base accuracy: {base_accuracy} ({sum([1 for el in evaluations_base if el.ground_truth_in_answer])}/{len(evaluations_base)})
    Context from accuracy: {context_from_accuracy} ({sum([1 for el in evaluations_context_from if el.ground_truth_in_answer])}/{len(evaluations_context_from)})
    Context date accuracy: {context_date_accuracy} ({sum([1 for el in evaluations_context_date if el.ground_truth_in_answer])}/{len(evaluations_context_date)})
    Context combined accuracy: {context_combined_accuracy} ({sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])}/{len(evaluations_context_combined)})

    """

    print(results)


    # save results using pickle
    with open(EVAL_RESULT_PATH_BASE_BASE, 'wb') as f:
        pickle.dump(evaluations_base, f)
    log.info(f"Saved base results at {EVAL_RESULT_PATH_BASE_BASE}")

    with open(EVAL_RESULT_PATH_CONTEXT_FROM, 'wb') as f:
        pickle.dump(evaluations_context_from, f)
    log.info(f"Saved context from results at {EVAL_RESULT_PATH_CONTEXT_FROM}")

    with open(EVAL_RESULT_PATH_CONTEXT_DATE, 'wb') as f:
        pickle.dump(evaluations_context_date, f)
    log.info(f"Saved context date results at {EVAL_RESULT_PATH_CONTEXT_DATE}")

    with open(EVAL_RESULT_PATH_CONTEXT_COMBINED, 'wb') as f:
        pickle.dump(evaluations_context_combined, f)
    log.info(f"Saved context combined results at {EVAL_RESULT_PATH_CONTEXT_COMBINED}")



def load_evaluations():
    evaluations_base = []
    evaluations_context_from = []
    evaluations_context_date = []
    evaluations_context_combined = []

    with open(EVAL_RESULT_PATH_BASE_BASE_INPUT, 'rb') as f:
        evaluations_base = pickle.load(f)
    
    with open(EVAL_RESULT_PATH_CONTEXT_FROM_INPUT, 'rb') as f:
        evaluations_context_from = pickle.load(f)
    
    with open(EVAL_RESULT_PATH_CONTEXT_DATE_INPUT, 'rb') as f:
        evaluations_context_date = pickle.load(f)
    
    with open(EVAL_RESULT_PATH_CONTEXT_COMBINED_INPUT, 'rb') as f:
        evaluations_context_combined = pickle.load(f)
    
evaluate()