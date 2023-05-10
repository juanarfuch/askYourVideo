import os
import asyncio
from dotenv import find_dotenv, load_dotenv
from youtubePers import YoutubeLoading
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv(find_dotenv())
openaiapikey = os.environ.get("OPENAI_API_KEY")

def load_transcript(url, add_video_info=True):

    loader = YoutubeLoading.from_youtube_url(url, add_video_info=add_video_info)
    # Use asyncio.to_thread to run the load method asynchronously   
    transcript = loader.load()
    return transcript

def split_transcript(transcript, chunk_size=1000, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(transcript)
    return docs
