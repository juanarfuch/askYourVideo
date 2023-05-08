import os
import asyncio
from dotenv import find_dotenv, load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv(find_dotenv())
openaiapikey = os.environ.get("OPENAI_API_KEY")

async def load_transcript(url, add_video_info=False):
    try:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=add_video_info)
        # Use asyncio.to_thread to run the load method asynchronously
        transcript = await asyncio.to_thread(loader.load)
    except Exception as e:
        print(f"An error occurred while loading the transcript: {e}")
        return None
    return transcript

def split_transcript(transcript, chunk_size=1000, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(transcript)
    return docs
