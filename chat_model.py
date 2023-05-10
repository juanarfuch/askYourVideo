from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)



template = """You are a professional assistant, expert in answering questions using the 
video transcriptions obtained from: {docs}.
You must answer the questions provided by the user, only with factual information from the transcription.
If you don't have enough information to answer the question, say to the user that you don't know and couldn't find the answer in the video.
You should be friendly and detailed."""


system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{question}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
chain = LLMChain(llm=chat, prompt=chat_prompt)

def get_response_from_query(query, docs, k=4):
    response = chain.run(question=query, docs="".join(doc.page_content for doc in docs))
    response = response.replace("\n", "")
    return response
