import asyncio
from video_processing import load_transcript, split_transcript
from chat_model import get_response_from_query
from database import create_db, search_similar_documents

async def main():
    video_url = input("Please enter the YouTube video URL: ")
    # Add the 'await' keyword before calling load_transcript
    transcript = await load_transcript(video_url)
    docs = split_transcript(transcript)
    db = create_db(docs)
    user_question = input("Enter your question or type 'exit' to quit: ")
    similar_docs = search_similar_documents(db, user_question)
    response = get_response_from_query(user_question, similar_docs)
    print(f"Answer: {response}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
