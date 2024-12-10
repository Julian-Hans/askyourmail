import pandas as pd
import uuid
import kagglehub
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction


# local imports
from askyourmail.src.data.Email import Email
from askyourmail.src.data.Conversation import Conversation
from askyourmail.src.util.Constants import *


class Processor:
    def __init__(self, chroma_db_path=CHROMA_DB_PATH):
        """
        Initialize the EmailThreadProcessor with ChromaDB path and Kaggle configurations.
        """
        self.chroma_db_path = chroma_db_path
        self.client = chromadb.PersistentClient(path=chroma_db_path)
        self.collection = None
    
    def initialize_collection(self, collection_name, model_name, api_base, api_key):
        """
        Initialize a ChromaDB collection with specified parameters.

        Args:
            collection_name (str): Name of the collection.
            model_name (str): Model name for OpenAI embeddings.
            api_base (str): OpenAI API base URL.
            api_key (str): OpenAI API key.
        """
        embedding_function = OpenAIEmbeddingFunction(
                model_name=model_name,
                api_base=api_base,
                api_key=api_key
            )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={"hnsw:space": "cosine"}
            )
        
    def download_and_load_data(self, kaggle_dataset_name):
        """
            Download the dataset from Kaggle and load it into a Pandas DataFrame.
            
            Args:
                kaggle_dataset_name (str): Name of the Kaggle dataset to download.

            Returns:
                pd.DataFrame: Loaded dataset as a Pandas DataFrame.
        """
        path = kagglehub.dataset_download(kaggle_dataset_name)
        log.info(f"Path to dataset files: {path}")
        csv_path = f"{path}/CSV/email_thread_details.csv"
        df = pd.read_csv(csv_path)
        df = df.iloc[:len(df)//2].reset_index(drop=True)
        return df

    def process_emails(self, email_df):
        """
            Takes emails df and creates email and conversations objects from columns.
            Populated Emails and Conversations are returned as lists.

            Args:
                emails_df (pd.DataFrame): DataFrame containing email data.

            Returns:
                tuple: 
                (emails (list): List of Email objects, 
                conversations (list): List of Conversation objects.).
        """
        # Convert DataFrame rows into Email objects
        emails = []
        for _, row in email_df.iterrows():
            row['timestamp'] = int(pd.to_datetime(row['timestamp']).timestamp())
            email = Email(
                thread_id=row['thread_id'], 
                subject=row['subject'],
                timestamp=row['timestamp'],
                from_=row['from'],
                to=row['to'],
                body=row['body']
            )
            emails.append(email)

        # Group emails into conversations by thread_id
        conversations = {}
        for email in emails:
            if email.thread_id not in conversations:
                conversations[email.thread_id] = Conversation(thread_id=email.thread_id)
            conversations[email.thread_id].add_email(email)

        # Conversations are now accessible as a dictionary with thread_id as the key
        conversation_list = list(conversations.values())

        return emails, conversation_list

    def add_emails_to_vector_store(self, conversation_list):
        # Split body into chunks for embedding
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

        # Add emails to the collection
        for conversation in conversation_list:
            for email in conversation.emails:
                chunks = text_splitter.split_text(email.body)
                for i, chunk in enumerate(chunks):
                    self.collection.upsert(
                        documents=[chunk],
                        metadatas=[email.to_dict()],
                        ids=[str(uuid.uuid1())]
                    )

        log.info("Emails successfully inserted into vector store!")

    def run_pipline(self, collection_name, model_name, api_base, api_key):
        kagglehub_dataset_name = KAGGLEHUB_DATASET_NAME

        log.info("Starting pipeline...")
        log.info("\nInitializing collection...")
        self.initialize_collection(collection_name, model_name, api_base, api_key)
        log.info("Collection initialized successfully!")
        log.info("\nLoading email data from Kaggle...")
        emails_df = self.download_and_load_data(kagglehub_dataset_name)
        log.info("Email data loaded successfully!")

        log.info("\nProcessing emails...")
        emails, conversation_list = self.process_emails(emails_df)
        log.info("Emails processed successfully!")

        log.info("\nAdding emails to collection...")
        self.add_emails_to_vector_store(conversation_list)
        log.info("Pipeline completed successfully!")

        


if __name__ == "__main__":
    #processor = Processor()
    #processor.run_pipline(COLLECTION_NAME, EMBEDDING_MODEL_NAME, OPENAI_API_BASE, OPENAI_API_KEY)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    collection_old = client.get_collection("emails")

    log.info(collection_old.count())
    log.info(collection.count())
    
    
