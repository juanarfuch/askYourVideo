from video_processing import load_transcript, split_transcript
from database import create_db
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompts import CONDENSE_PROMPT, QA_PROMPT


def main():
    video_url = input("Please enter the YouTube video URL: ")
    ###Obtenemos el transcript de la url de video
    transcript =load_transcript(video_url)
    ###Separamos el transcript en documentos
    docs = split_transcript(transcript)
    ###Creamos la base de datos
    db = create_db(docs)

    chat = ChatOpenAI(temperature=0.2, model_name='gpt-3.5-turbo')
    question_generator = LLMChain(llm=chat,  prompt= CONDENSE_PROMPT)
    doc_chain=load_qa_chain(chat, prompt=QA_PROMPT)
        
    chain = ConversationalRetrievalChain(
        retriever=db.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    while True:
        chat_history = []
        user_question = input("Enter your question or type 'exit' to quit: ")
        if user_question.lower() == "exit":
            break
        response = chain.run({"question": user_question, "chat_history": chat_history})
        print(f'Bot:{response}')
if __name__ == "__main__":
    main()
       
