from dotenv import load_dotenv
#import streamlit as st
#from langchain_community.document_loaders import TextLoader
#from langchain.document_loaders import TextLoader
#from langchain_openai import OpenAI
import pdfplumber
from  langchain_openai import OpenAIEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, models
from langchain_community.vectorstores import Qdrant
import os


load_dotenv()

# Define collection config

url=os.getenv("QDRANT_HOST")
api_key=os.getenv("QDRANT_API_KEY")
collection_name=os.getenv("QDRANT_COLLECTION_NAME")
vector_size = 1536  # use 768 for Instructor-XL

# Initialize Qdrant client

client = QdrantClient(
    url=url,
    api_key=api_key
)


# # Delete and recreate collection
# if client.collection_exists(collection_name=collection_name):
#     client.delete_collection(collection_name=collection_name)

# client.create_collection(
#     collection_name=collection_name,
#     vectors_config=models.VectorParams(size=1536, distance=Distance.COSINE),
# )


# Load and extract text from PDF
raw_texts = ""
with pdfplumber.open("Qlik-functions.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            raw_texts += text + "\n"

# Split text into chunks
def get_text_chunks(raw_texts):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return splitter.split_text(raw_texts)

text_chunks = get_text_chunks(raw_texts)

print(text_chunks)

# Define embeddings
embeddings = OpenAIEmbeddings()
# embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

# Create vector store and upload to Qdrant
vector_store = Qdrant.from_texts(
    texts=text_chunks,
    embedding=embeddings,
    url=url,
    api_key=api_key,
    collection_name=collection_name
)

# #create a qdrant client

# client = QdrantClient(
#     os.getenv("QDRANT_HOST"),
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# # create a collection

# vectors_config = QdrantClient.http.models.VectorParams(
#     size = 1536, 
#     #768 for instructor-xl, 1536 for openAi
#     distance=QdrantClient.http.models.Distance.COSINE
#     )

# #********** Only to create a new collection ********

# collection_name = os.getenv("QDRANT_COLLECTION_NAME")

# if client.collection_exists(collection_name):
#     client.delete_collection(collection_name)

# client.create_collection(
#     collection_name=collection_name,
#     vectors_config= vectors_config   # your config here
# )

# #vector store

# embeddings = OpenAIEmbeddings()
# #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

# #Recreating a vector store

# # vector_store = Qdrant(

# #     client=client,
# #     collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
# #     embeddings=embeddings,
# #     )

# raw_texts = ""
# with pdfplumber.open("Qlik-functions.pdf") as pdf:
#     # loop over all the pages
#     for page in pdf.pages:
#         raw_texts += page.extract_text()

# print(raw_texts)

# def get_text_chunks(raw_texts):
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(raw_texts)
    
#     return chunks
#     print(chunks)

# text_chunks = get_text_chunks(raw_texts)

# # Creating a store first time

# vector_store = Qdrant.from_texts(
#     text_chunks,
#     embeddings, 
#     url=os.getenv("QDRANT_HOST"),
#     api_key=os.getenv("QDRANT_API_KEY"),
#     collection_name=os.getenv("QDRANT_COLLECTION_NAME")
# )

# next time use the following qdrant instance instead of rewriting the entire vectore database

# vector_store = Qdrant(

#     client=client,
#     collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
#     embeddings=embeddings,
#     )


#plug vector store retrieval chain not used in this part. Retrieval is used in the app

# qa = RetrievalQA.from_chain_type(
#     llm=OpenAI(),
#     chain_type="stuff",
#     retriever = vector_store.as_retriever() #querying the information from the vector store

# )

# query = "How to create symbols in qliksense"
# response = qa.run(query)
# print(response)

