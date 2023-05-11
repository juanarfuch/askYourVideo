import argparse
from utils.video_processing import load_transcript, split_transcript
from utils.database import create_db
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from utils.chat_model import ChatOpenAI
from utils.prompts import CONDENSE_PROMPT, QA_PROMPT

def user_interaction(chain):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    while True:
        chat_history = []
        user_question = input("Enter your question or type 'exit' to quit: ")
        if user_question.lower() == "exit":
            break
        response = chain.run({"question": user_question, "chat_history": chat_history})
        print(f'Bot:{response}')

def main(video_url, temperature, model_name):
    transcript = load_transcript(video_url)
    docs = split_transcript(transcript)
    db = create_db(docs)
    chat = ChatOpenAI(temperature=temperature, model_name=model_name)
    question_generator = LLMChain(llm=chat,  prompt= CONDENSE_PROMPT)
    doc_chain=load_qa_chain(chat, prompt=QA_PROMPT)
    chain = ConversationalRetrievalChain(
        retriever=db,
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        )
    user_interaction(chain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chatbot for handling user queries based on YouTube video transcripts.')
    parser.add_argument('--temperature', type=float, default=0.2, help='The temperature to use for the chat model.')
    parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo', help='The name of the chat model to use.')
    args = parser.parse_args()
    video_url = input("Please enter the YouTube video URL: ")
    main(video_url, args.temperature, args.model_name)

