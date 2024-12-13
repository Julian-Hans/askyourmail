# ASKYOURMAIL
A conversational interface for retrieving emails and answering natural language queries based on them.
It uses Langchain, Chroma and OpenAIs gpt4-o-mini as well as text-embedding-3-small.

## Prerequisites
This project uses Poetry (version 1.8.4) for virtual environment and dependency management, as well as Python (version 3.11.7). Make sure you have python and pip installed and (if not present) install poetry using 

```pip install poetry```

Copy the `.env.example`file and rename it to `.env`, populating the required keys. You can use langsmith to track your experiments, but that is optional.

Make sure that the chroma_db directory contains a chroma database with a valid collection. If there is none (or you want to generate your own, see section Populating chroma_db.)

## Quickstart:
After making sure you meet all requirements, run the interactive interface using 
```poetry run python main.py```

## Populating chroma_db:
With `askyourmail/src/data/Processor.py` you can generate a new collection for the chroma database. You can change the dataset from `askyourmail/src/util/constants.py`, but will have to parse email dataset that differ from our format beforehand. 
The process will take a long time, as the embeddings are created sequentially. The final database for our dataset should be around 1 GB in size.

## How to use:
In askyourmail/src you will find 3 python files serving different purposes.
- `main.py`: runs a gradio instance accessible under localhost:7860 that allows interaction with the system. This assumes that the `chroma_db` directory contains a chroma database with a valid email collection.
- `generateEvalDataset.py`: utilizes gpt4-o-mini to generate query-email pairs used for evaluation. They are saved to evaluation using the format specified in `askyourmail/src/util/constants.py`.
- `evaluate.py`: runs evaluations given the parameters specified in `askyourmail/src/util/constants.py`. Pipe this into eval_log.txt using the pipe operator `python evaluate.py > eval_log.txt`

## Costs and Evaluation Results
As with `TOTAL_RETRIEVAL_K` = 32 one query averages around 16000 tokens per request, and 1m token cost 0.15 USD. This means that for
- `TOTAL_RETRIEVAL_K` = 32  -> 0.0022 USD per query (yielding 84% accuracy, assuming the user provides good context)
- `TOTAL_RETRIEVAL_K` = 160 -> 0.01   USD per query (yielding 94% accuracy, assuming the user provides good context)
Our evaluation with a generated dataset of 600 elements and k = 32 cost a total of 1.75$.
For more details, see `eval_log_*.txt`!