import logging
import json
import time
from typing import List

from askyourmail.src.main import main
from askyourmail.src.data.EvaluationPair import EvaluationPair
from askyourmail.src.util.Evaluator import Evaluator
from askyourmail.src.util.Constants import *
import pickle
log.info(OPENAI_API_KEY)

def evaluate_combined(checkpoint:bool = False):
    # load list of evaluation pairs
    evaluation_dataset:List[EvaluationPair] = []
    with open(EVAL_GEN_DATASET_PATH_INPUT, 'r') as f:
        evaluation_dataset_string = json.load(f)
        for el in evaluation_dataset_string:
            _tmp_ev_pair = EvaluationPair.from_dict(el)
            evaluation_dataset.append(_tmp_ev_pair)
    
    log.info(f"Loaded {len(evaluation_dataset)} evaluation pairs from {EVAL_GEN_DATASET_PATH_INPUT}")
    evaluations_context_combined = []
    
    if checkpoint:
        # empty eval dataset
        _tmp_evaluation_dataset = []
        _evaluated_dataset = []
        # load checkpoint
        with open(LATEST_EVAL_RESULT_CHECKPOINT_PATH_CONTEXT_COMBINED, 'rb') as f:
            evaluations_context_combined = pickle.load(f)
        log.info(f"Loaded checkpoint context combined results at {LATEST_EVAL_RESULT_CHECKPOINT_PATH_CONTEXT_COMBINED}: {len(evaluations_context_combined)} elements")

        for evaluator in evaluations_context_combined:
            _evaluated_dataset.append(evaluator.evaluation_pair)
        
        _tmp_evaluation_dataset = evaluation_dataset[len(_evaluated_dataset):]
        evaluation_dataset = _tmp_evaluation_dataset
        log.info(f"Continuing evaluation with {len(evaluation_dataset)} elements")


    for index, eval_pair in enumerate(evaluation_dataset):
        # context combined
        log.info(f"Evaluating combined context {index + 1}/{len(evaluation_dataset)}")
        evaluator_context_combined = Evaluator(query=eval_pair.eval_gen_agent_output.context_query_combined, evaluation_pair=eval_pair)
        evaluator_context_combined.evaluate()
        if(TOTAL_RETRIEVAL_K > 50):
            time.sleep(30) # avoid timeout because of openai rate limits
        evaluations_context_combined.append(evaluator_context_combined)
        if index % 10 == 0:
            path = EVAL_RESULT_CHECKPOINT_PATH_CONTEXT_COMBINED + f"{index}_of_{len(evaluation_dataset)}.pickle"
            with open(path, 'wb') as f:
                pickle.dump(evaluations_context_combined, f)
            log.info(f"Saved checkpoint combined results at {path}")
            
    
    context_combined_accuracy = sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])/len(evaluations_context_combined)
    proportion_of_groundtruth_in_retrieved_but_not_in_relevant = sum([1 for el in evaluations_context_combined if (el.ground_truth_in_retrieved_emails and el.ground_truth_in_relevant_emails == False) ])/len(evaluations_context_combined)
    proportion_of_groundtruth_in_relevant_but_not_in_answer = sum([1 for el in evaluations_context_combined if (el.ground_truth_in_relevant_emails and el.ground_truth_in_answer == False) ])/len(evaluations_context_combined)


    for index, eval_pair in enumerate(evaluation_dataset):
        result = f"""
        --------------------------
        Evaluation pair {index + 1}/{len(evaluation_dataset)}

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

    Context combined accuracy: {context_combined_accuracy} ({sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])}/{len(evaluations_context_combined)})
    Proportion of ground truth in retrieved but not in relevant: {proportion_of_groundtruth_in_retrieved_but_not_in_relevant} ({sum([1 for el in evaluations_context_combined if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails) ])} / {len(evaluations_context_combined)})
    Proportion of ground truth in relevant but not in answer: {proportion_of_groundtruth_in_relevant_but_not_in_answer} ({sum([1 for el in evaluations_context_combined if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer) ])} / {len(evaluations_context_combined)})
    """

    print(results)


    # save results using pickle

    with open(EVAL_RESULT_PATH_CONTEXT_COMBINED, 'wb') as f:
        pickle.dump(evaluations_context_combined, f)
    log.info(f"Saved context combined results at {EVAL_RESULT_PATH_CONTEXT_COMBINED}")

def evaluate_all():
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
    context_combined_accuracy = sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])/len(evaluations_context_combined)
    proportion_of_groundtruth_in_retrieved_but_not_in_relevant_combined = sum([1 for el in evaluations_context_combined if (el.ground_truth_in_retrieved_emails and el.ground_truth_in_relevant_emails == False) ])/len(evaluations_context_combined)
    proportion_of_groundtruth_in_relevant_but_not_in_answer_combined = sum([1 for el in evaluations_context_combined if (el.ground_truth_in_relevant_emails and el.ground_truth_in_answer == False) ])/len(evaluations_context_combined)

    # Calculate accuracies and proportions for `evaluations_base`
    base_accuracy = sum([1 for el in evaluations_base if el.ground_truth_in_answer]) / len(evaluations_base)
    proportion_of_groundtruth_in_retrieved_but_not_in_relevant_base = sum([1 for el in evaluations_base if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails)]) / len(evaluations_base)
    proportion_of_groundtruth_in_relevant_but_not_in_answer_base = sum([1 for el in evaluations_base if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer)]) / len(evaluations_base)

    # Calculate accuracies and proportions for `evaluations_context_from`
    context_from_accuracy = sum([1 for el in evaluations_context_from if el.ground_truth_in_answer]) / len(evaluations_context_from)
    proportion_of_groundtruth_in_retrieved_but_not_in_relevant_from = sum([1 for el in evaluations_context_from if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails)]) / len(evaluations_context_from)
    proportion_of_groundtruth_in_relevant_but_not_in_answer_from = sum([1 for el in evaluations_context_from if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer)]) / len(evaluations_context_from)

    # Calculate accuracies and proportions for `evaluations_context_date`
    context_date_accuracy = sum([1 for el in evaluations_context_date if el.ground_truth_in_answer]) / len(evaluations_context_date)
    proportion_of_groundtruth_in_retrieved_but_not_in_relevant_date = sum([1 for el in evaluations_context_date if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails)]) / len(evaluations_context_date)
    proportion_of_groundtruth_in_relevant_but_not_in_answer_date = sum([1 for el in evaluations_context_date if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer)]) / len(evaluations_context_date)



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
    Proportion of ground truth in retrieved but not in relevant (base): {proportion_of_groundtruth_in_retrieved_but_not_in_relevant_base} ({sum([1 for el in evaluations_base if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails) ])} / {len(evaluations_base)})
    Proportion of ground truth in relevant but not in answer (base): {proportion_of_groundtruth_in_relevant_but_not_in_answer_base} ({sum([1 for el in evaluations_base if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer) ])} / {len(evaluations_base)})

    Context from accuracy: {context_from_accuracy} ({sum([1 for el in evaluations_context_from if el.ground_truth_in_answer])}/{len(evaluations_context_from)})
    Proportion of ground truth in retrieved but not in relevant (context from): {proportion_of_groundtruth_in_retrieved_but_not_in_relevant_from} ({sum([1 for el in evaluations_context_from if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails) ])} / {len(evaluations_context_from)})
    Proportion of ground truth in relevant but not in answer (context from): {proportion_of_groundtruth_in_relevant_but_not_in_answer_from} ({sum([1 for el in evaluations_context_from if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer) ])} / {len(evaluations_context_from)})

    Context date accuracy: {context_date_accuracy} ({sum([1 for el in evaluations_context_date if el.ground_truth_in_answer])}/{len(evaluations_context_date)})
    Proportion of ground truth in retrieved but not in relevant (context date): {proportion_of_groundtruth_in_retrieved_but_not_in_relevant_date} ({sum([1 for el in evaluations_context_date if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails) ])} / {len(evaluations_context_date)})
    Proportion of ground truth in relevant but not in answer (context date): {proportion_of_groundtruth_in_relevant_but_not_in_answer_date} ({sum([1 for el in evaluations_context_date if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer) ])} / {len(evaluations_context_date)})

    Context combined accuracy: {context_combined_accuracy} ({sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])}/{len(evaluations_context_combined)})
    Proportion of ground truth in retrieved but not in relevant (context combined): {proportion_of_groundtruth_in_retrieved_but_not_in_relevant_combined} ({sum([1 for el in evaluations_context_combined if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails) ])} / {len(evaluations_context_combined)})
    Proportion of ground truth in relevant but not in answer (context combined): {proportion_of_groundtruth_in_relevant_but_not_in_answer_combined} ({sum([1 for el in evaluations_context_combined if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer) ])} / {len(evaluations_context_combined)})
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
    

def load_combined():
    evaluations_context_combined:List[Evaluator] = []

    with open(EVAL_RESULT_PATH_CONTEXT_COMBINED_INPUT, 'rb') as f:
        evaluations_context_combined = pickle.load(f)
    
    context_combined_accuracy = sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])/len(evaluations_context_combined)
    proportion_of_groundtruth_in_retrieved_but_not_in_relevant = sum([1 for el in evaluations_context_combined if (el.ground_truth_in_retrieved_emails and el.ground_truth_in_relevant_emails == False) ])/len(evaluations_context_combined)
    proportion_of_groundtruth_in_relevant_but_not_in_answer = sum([1 for el in evaluations_context_combined if (el.ground_truth_in_relevant_emails and el.ground_truth_in_answer == False) ])/len(evaluations_context_combined)

    for index, evaluator in enumerate(evaluations_context_combined):
        
        result = f"""
        --------------------------
        Evaluation pair {index + 1}/{len(evaluations_context_combined)}

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
    evaluation batch size = {len(evaluations_context_combined)}

    ==Evaluation results==:

    Context combined accuracy: {context_combined_accuracy} ({sum([1 for el in evaluations_context_combined if el.ground_truth_in_answer])}/{len(evaluations_context_combined)})
    Proportion of ground truth in retrieved but not in relevant: {proportion_of_groundtruth_in_retrieved_but_not_in_relevant} ({sum([1 for el in evaluations_context_combined if (el.ground_truth_in_retrieved_emails and not el.ground_truth_in_relevant_emails) ])} / {len(evaluations_context_combined)})
    Proportion of ground truth in relevant but not in answer: {proportion_of_groundtruth_in_relevant_but_not_in_answer} ({sum([1 for el in evaluations_context_combined if (el.ground_truth_in_relevant_emails and not el.ground_truth_in_answer) ])} / {len(evaluations_context_combined)})
    """

    print(results)

evaluate_combined(True)