# external imports
import os
import logging as log
from dotenv import load_dotenv
from datetime import datetime

LOGGING_LEVEL = log.INFO

log.basicConfig(
    format="[%(levelname)s] \033[92m%(funcName)s\033[0m: %(message)s",
    level=LOGGING_LEVEL
)

load_dotenv(".env")

MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "langchain-api-key")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"askyourmail_eval_big_k"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

KAGGLEHUB_DATASET_NAME = "marawanxmamdouh/email-thread-summary-dataset"
CHROMA_DB_PATH = "chroma_db"

COLLECTION_NAME = "emails2"
TOTAL_RETRIEVAL_K = 160 # TODO: should be a max 
RETRIEVAL_K_NAIVE = int(TOTAL_RETRIEVAL_K*(1/4))
RETRIEVAL_K_PER_FILTER = int(TOTAL_RETRIEVAL_K*(1/4)) 
RETRIEVAL_K_COMBINED_FILTERS = int(TOTAL_RETRIEVAL_K*(1/4)) 

# evaluation graph only
EVAL_GEN_BATCH_SIZE = 25
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
EVAL_GEN_DATASET_PATH_BASE = f"evaluation/eval_gen_dataset"
EVAL_GEN_DATASET_PATH = f"{EVAL_GEN_DATASET_PATH_BASE}_{current_date}_k_{EVAL_GEN_BATCH_SIZE}.json"
EVAL_GEN_DATASET_PATH_INPUT = f"{EVAL_GEN_DATASET_PATH_BASE}_k_{EVAL_GEN_BATCH_SIZE}.json"

# evaluation results only
# man this is painful
EVAL_RESULT_PATH_BASE = f"evaluation/eval_result"
EVAL_RESULT_PATH_BASE_BASE = f"{EVAL_RESULT_PATH_BASE}_base_{current_date}_k_{EVAL_GEN_BATCH_SIZE}.pickle"
EVAL_RESULT_PATH_CONTEXT_FROM = f"{EVAL_RESULT_PATH_BASE}_context_from_{current_date}_k_{EVAL_GEN_BATCH_SIZE}.pickle"
EVAL_RESULT_PATH_CONTEXT_DATE = f"{EVAL_RESULT_PATH_BASE}_context_date_{current_date}_k_{EVAL_GEN_BATCH_SIZE}.pickle"
EVAL_RESULT_PATH_CONTEXT_COMBINED = f"{EVAL_RESULT_PATH_BASE}_context_combined_{current_date}_k_{EVAL_GEN_BATCH_SIZE}.pickle"

# next time ill use an actual framework for evaluation
EVAL_RESULT_PATH_BASE_BASE_INPUT = f"{EVAL_RESULT_PATH_BASE}_base_k_{EVAL_GEN_BATCH_SIZE}.pickle"
EVAL_RESULT_PATH_CONTEXT_FROM_INPUT = f"{EVAL_RESULT_PATH_BASE}_context_from_k_{EVAL_GEN_BATCH_SIZE}.pickle"
EVAL_RESULT_PATH_CONTEXT_DATE_INPUT = f"{EVAL_RESULT_PATH_BASE}_context_date_k_{EVAL_GEN_BATCH_SIZE}.pickle"
EVAL_RESULT_PATH_CONTEXT_COMBINED_INPUT = f"{EVAL_RESULT_PATH_BASE}_context_combined_k_{EVAL_GEN_BATCH_SIZE}.pickle"

# checkpoints for big eval
EVAL_RESULT_CHECKPOINT_PATH_CONTEXT_COMBINED = f"evaluation/checkpoints/"
LATEST_EVAL_RESULT_CHECKPOINT_PATH_CONTEXT_COMBINED= f"{EVAL_RESULT_CHECKPOINT_PATH_CONTEXT_COMBINED}300_of_992.pickle"
# as we average around 16000 tokens per request, and 1m token cost 0.15 USD ->
# with k = 32  -> 0.00220095 USD per query
# with k = 160 -> 0.01 USD per query