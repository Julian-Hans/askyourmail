# external imports
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from chromadb.utils import embedding_functions
import chromadb
from chromadb.config import Settings
import uuid

# TODO: this is a work in progress

# IDEA: let agent create set of filters given the query
# email metadata to be included in text: subject, content, attachment name, date, sender, recipient
# email metadata to be metadata:         sender, recipient, date, attachment types, # of attachments, 


# local imports
from askyourmail.src.util.Constants import *

def test():
    # Set up embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=OPENAI_API_KEY,
                    model_name=EMBEDDING_MODEL_NAME
                )

    documents = []

    doc1 = Document(
        metadata={"title": "Document 1", "author": "John Doe"},
        page_content="This is the first document",
    )

    doc2 = Document(
        metadata={"title": "Document 2", "author": "Jane Doe"},
        page_content="This is the second document. Bananas are my favourite fruit!",
    )

    doc3 = Document(
        metadata={"title": "Document 3", "author": "John Doe"},
        page_content="This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas! This is the third document. My favourite color is yellow and i like bananas!This is the third document. My favourite color is yellow and i like bananas!",
    )

    documents.append(doc1)
    documents.append(doc2)
    documents.append(doc3)

    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    client = chromadb.HttpClient(settings=Settings(allow_reset=True))
    collection = client.get_or_create_collection(name="my_collection", embedding_function=openai_ef)

    client.reset()  # resets the database
    collection = client.get_or_create_collection(name="my_collection", embedding_function=openai_ef)
    for doc in docs:
        collection.add(
            ids=[str(uuid.uuid1())], metadatas=doc.metadata, documents=doc.page_content
        )

    # tell LangChain to use our client and collection name
    db4 = Chroma(
        client=client,
        collection_name="my_collection",
        embedding_function=embeddings,
    )
    query = "What is my favourite color?"
    docs_res = db4.similarity_search(query)
    print(docs_res[0].page_content)
    print(docs_res[0].metadata)


def main():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    db = Chroma(
        client=client,
        collection_name="emails",
        embedding_function=embeddings,
    )

    db_all = db.get(include=["embeddings", "metadatas", "documents"])
    print(f"Total number of embeddings in db_all: {len(db_all['embeddings'])}")
    print(f"Total number of metadatas in db_all: {len(db_all['metadatas'])}")
    print(f"Total number of documents in db_all: {len(db_all['documents'])}")

    unique_embeddings = set(tuple(embedding) for embedding in db_all["embeddings"])
    unique_metadatas = set(tuple(metadata.items()) for metadata in db_all["metadatas"])
    unique_documents = set(tuple(document) for document in db_all["documents"])
    print(f"Number of unique embeddings: {len(unique_embeddings)}")
    print(f"Number of unique metadatas: {len(unique_metadatas)}")
    print(f"Number of unique documents: {len(unique_documents)}")


    db2 = Chroma(
        client=client,
        collection_name="emails2",
        embedding_function=embeddings,
    )

    db_all2 = db2.get(include=["embeddings", "metadatas", "documents"])
    print(f"Total number of embeddings in db_all: {len(db_all2['embeddings'])}")
    print(f"Total number of metadatas in db_all: {len(db_all2['metadatas'])}")
    print(f"Total number of documents in db_all: {len(db_all2['documents'])}")
    
    unique_embeddings = set(tuple(embedding) for embedding in db_all2["embeddings"])
    unique_metadatas = set(tuple(metadata.items()) for metadata in db_all2["metadatas"])
    unique_documents = set(tuple(document) for document in db_all2["documents"])
    print(f"Number of unique embeddings: {len(unique_embeddings)}")
    print(f"Number of unique metadatas: {len(unique_metadatas)}")
    print(f"Number of unique documents: {len(unique_documents)}")
    #db_metadata = db.get()["metadatas"]
    #sender_set = set()
    #recipient_set = set()
    #for metadata in db_metadata:
     #   sender_set.add(metadata["from"])
      #  recipient_set.add(metadata["to"])

main()