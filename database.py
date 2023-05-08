from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()

def create_db(docs, embeddings=embeddings):
    try:
        database = FAISS.from_documents(docs, embeddings)
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")
        return None
    return database

def search_similar_documents(db, query, k=4):
    try:
        docs = db.similarity_search(query, k=k)
    except Exception as e:
        print(f"An error occurred while searching for similar documents: {e}")
        return None
    return docs
