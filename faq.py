import os
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts.chat import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import EdenAiEmbeddings
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["EDENAI_API_KEY"] = os.getenv('EDENAI_API_KEY')

llm = ChatGroq(groq_api_key=groq_api_key, model_name='Llama3-8b-8192')

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only. 
    Please provide the most accurate response based on the question.
    If you don't find answer, give a generic answer. Don't mention that you don't know the answer.
    <context>
    {context}
    <context>
    Question: {input}
    """
)

embeddings = EdenAiEmbeddings(provider="openai")

if 'vectors' not in st.session_state:
    st.session_state.vectors = Chroma(embedding_function=embeddings, persist_directory="FAQ_db")

user_prompt = st.chat_input("Ask a question related to Mental Health")

if user_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({'input': user_prompt})
    st.write(response['answer'])
