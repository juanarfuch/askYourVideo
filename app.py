# Import necessary libraries
import streamlit as st
from utils.video_processing import load_transcript, split_transcript
from utils.database import create_db
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain
from utils.prompts import CONDENSE_PROMPT, QA_PROMPT

# Set Streamlit page configuration
st.set_page_config(page_title='🧠ChatBot🤖', layout='wide')

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Sidebar options
with st.sidebar.expander("🛠️ ", expanded=False):
    # Option to start a new chat
    if st.button("New Chat"):
        st.session_state["chat_history"] = []

# Set up the Streamlit app layout
st.title("🤖 Chat Bot with 🧠")
st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")
if st.session_state["chat_history"]==[]:
    video_url = st.text_input("Please enter the YouTube video URL: ")
    if video_url:
        # Load and split transcript, create embeddings, and vectorstore
        transcript = load_transcript(video_url)
        docs = split_transcript(transcript)
        db = create_db(docs)

        llm = OpenAI(temperature=0.2)
        question_generator = LLMChain(llm=llm, prompt=CONDENSE_PROMPT)
        doc_chain = load_qa_chain(llm, prompt=QA_PROMPT)
        chain = ConversationalRetrievalChain(
            retriever=db,
            question_generator=question_generator,
            combine_docs_chain=doc_chain,
        )
        
        user_question = st.text_input("Enter your question")
        if user_question:
            result = chain({"question": user_question, "chat_history": st.session_state["chat_history"]})
            st.session_state["chat_history"].append((user_question, result['answer']))

        # Display the conversation history
        with st.expander("Conversation", expanded=True):
            for user, bot in st.session_state["chat_history"]:
                st.info(f'User: {user}')
                st.success(f'Bot: {bot}')
