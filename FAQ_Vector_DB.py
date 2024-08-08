import pandas as pd
df = pd.read_csv('FAQ.csv')
df = df.drop(columns=['Question_ID','Questions'])

from langchain.schema import Document

documents = [Document(page_content=row[0]) for row in df.itertuples(index=False, name=None)]

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_documents = []

from langchain_community.embeddings import EdenAiEmbeddings
import os
# Set the EdenAI API key
os.environ["EDENAI_API_KEY"] = os.getenv('EDENAI_API_KEY')

# Initialize EdenAI embeddings provider
embeddings = EdenAiEmbeddings(provider="openai")
from langchain.vectorstores import Chroma
vector_store = Chroma(embedding_function=embeddings,persist_directory='FAQ_db')

from dotenv import load_dotenv
load_dotenv()

for doc in documents[0:10]:
    chunks = text_splitter.split_text(doc.page_content)
    for chunk in chunks:
        split_documents.append(Document(page_content=chunk, metadata=doc.metadata))

vector_store = Chroma.from_documents(split_documents,embeddings,persist_directory='FAQ_db')

print("Documents have been embedded and stored successfully.")

