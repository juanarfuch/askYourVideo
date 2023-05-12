import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Instantiate OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Set up logging
logger = logging.getLogger(__name__)

def create_db(docs, embeddings=embeddings):
    """
    Function to create a new FAISS database from the given documents.

    Parameters:
    docs: A list of documents to be included in the database.
    embeddings: The embeddings to be used. Default is OpenAI embeddings.

    Returns:
    The FAISS database, or None if an error occurs or no documents are provided.
    """
    if not docs:
        logger.error("No documents to create the database.")
        return None
    try:
        database  = FAISS.from_documents(docs, embeddings).as_retriever()
    except Exception as e:
        logger.error(f"An error occurred while creating the database: {e}")
        return None
    return database
