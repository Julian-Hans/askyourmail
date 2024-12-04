# external imports
import os
import logging as log
from dotenv import load_dotenv

LOGGING_LEVEL = log.INFO

log.basicConfig(
    format="[%(levelname)s] \033[92m%(funcName)s\033[0m: %(message)s",
    level=LOGGING_LEVEL
)

load_dotenv("project.env")

MODEL_NAME = "gpt-3.5-turbo"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"askyourmail"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

KAGGLEHUB_DATASET_NAME = "marawanxmamdouh/email-thread-summary-dataset"
CHROMA_DB_PATH = "chroma_db"
