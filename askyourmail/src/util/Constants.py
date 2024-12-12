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

load_dotenv("project.env")

MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"askyourmail"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

KAGGLEHUB_DATASET_NAME = "marawanxmamdouh/email-thread-summary-dataset"
CHROMA_DB_PATH = "chroma_db"

COLLECTION_NAME = "emails2"
TOTAL_RETRIEVAL_K = 24
RETRIEVAL_K_NAIVE = int(TOTAL_RETRIEVAL_K*(4/10))
RETRIEVAL_K_PER_FILTER = int(TOTAL_RETRIEVAL_K*(8/10)/2) # divided by number of filters
RETRIEVAL_K_COMBINED_FILTERS = int(TOTAL_RETRIEVAL_K*(4/10))

# evaluation graph only
EVAL_GEN_BATCH_SIZE = 50
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

# as we average around 785 tokens per request, and 1m token cost 0.15 USD ->
# 1 eval request costs around 0.000118110236 USD
# -> when total retrieval k = 1000, one query costs around 0.12 USD
# -> when total retrieval k = 100, one query costs around 0.012 USD
# -> when total retrieval k = 10, one query costs around 0.0012 USD