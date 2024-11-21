# external imports
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