# external imports
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from askyourmail.src.util.Constants import *

class Filter:
    def __init__(self):
        self.chroma_filter = None
    
    def combine_and(self, filter1, filter2):
        return {
            "$and": [filter1, filter2]
        }

    def to_chroma_filter(self):
        return self.chroma_filter


class TimeFilter(Filter):
    def __init__(self, time=None, start_date=None, end_date=None, start_timestamp=None, end_timestamp=None):
        super().__init__()
        self.time = time
        self.start_date = start_date
        self.end_date = end_date
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def to_chroma_filter(self):
        filter_condition = {
            "$and": [
                {"timestamp": {"$gte": self.start_timestamp}},  # Greater than or equal to start timestamp
                {"timestamp": {"$lte": self.end_timestamp}}    # Less than or equal to end timestamp
            ]
        }
        return filter_condition
    
    def to_string(self):
        return f"TimeFilter: {self.time}, {self.start_date}, {self.end_date}, {self.start_timestamp}, {self.end_timestamp}"

class FromFilter(Filter):
    def __init__(self, from_=None):
        super().__init__()
        self.from_ = from_

    def to_chroma_filter(self):
        # get available senders from the email dataset and create a filter condition where the senders name (literal string) appears in the db sender field
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        db2 = Chroma(
            client=client,
            collection_name="emails2",
            embedding_function=embeddings,
        )
        db_all2 = db2.get(include=["metadatas"])
        self.db_sender_set = set()
        for item in db_all2["metadatas"]:
            self.db_sender_set.add(item["from"])

        self.final_sender_list = []
        for sender in self.db_sender_set:
            if self.from_ in sender:
                self.final_sender_list.append(sender)
        
        if len(self.final_sender_list) == 0:
            log.error(f"No sender found in the database for the given sender: {self.from_}")
            self.final_sender_list.append(self.from_)
        log.info(f"Final sender list: {self.final_sender_list}")
        filter_condition = {
            "from": {"$in": self.final_sender_list}  # Match any of the specified senders
        }
        return filter_condition
    
    def to_string(self):
        return f"FromFilter: {self.from_}"  
    