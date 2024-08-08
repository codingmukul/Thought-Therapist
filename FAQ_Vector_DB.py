import os
import pandas as pd
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import EdenAiEmbeddings
from langchain.vectorstores import FAISS

# Load environment variables early in the script
load_dotenv()

# Set the EdenAI API key
os.environ["EDENAI_API_KEY"] = os.getenv('EDENAI_API_KEY')

# Load the CSV and drop unnecessary columns
df = pd.read_csv('FAQ.csv')
df = df.drop(columns=['Question_ID', 'Questions'])

# Convert rows to Documents
documents = [Document(page_content=row[0]) for row in df.itertuples(index=False, name=None)]

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split the documents into chunks
split_documents = []
for doc in documents:  # Limiting to the first 10 documents
    chunks = text_splitter.split_text(doc.page_content)
    for chunk in chunks:
        split_documents.append(Document(page_content=chunk, metadata=doc.metadata))

# Initialize EdenAI embeddings provider
embeddings = EdenAiEmbeddings(provider="openai")

# Initialize FAISS vector store and embed the documents
vector_store = FAISS.from_documents(split_documents, embeddings)

# Persist the FAISS index locally
vector_store.save_local('FAQ_db')

print("Documents have been embedded and stored successfully.")