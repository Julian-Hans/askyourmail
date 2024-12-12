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
RETRIEVAL_K_NAIVE = 50
RETRIEVAL_K_PER_FILTER = 10
RETRIEVAL_K_COMBINED_FILTERS = 10

# evaluation graph only
EVAL_GEN_BATCH_SIZE = 10
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
EVAL_GEN_DATASET_PATH = f"/evaluation/eval_gen_dataset_{current_date}_k_{EVAL_GEN_BATCH_SIZE}.json"