# external imports
import os
import logging as log

LOGGING_LEVEL = log.INFO

log.basicConfig(
    format="[%(levelname)s] \033[92m%(funcName)s\033[0m: %(message)s",
    level=LOGGING_LEVEL
)

MODEL_NAME = "gpt-4-turbo"
OPENAI_API_BASE = "http://localhost:4000"
OPENAI_API_KEY = "" # this should not be in here
LANGCHAIN_API_KEY = "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" # this should not be in here

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"askyourmail"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY