from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()

def create_db(docs, embeddings=embeddings):
    if not docs:
        return None
    try:
        database  = FAISS.from_documents(docs, embeddings).as_retriever()
    except Exception as e:
        return None
    return database
