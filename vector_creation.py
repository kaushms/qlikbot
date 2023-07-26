from dotenv import load_dotenv
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import qdrant_client
import os


os.environ['QDRANT_HOST'] = "https://f7fe3590-9b3d-400f-b8ff-8c6aa50d3b6a.eu-central-1-0.aws.cloud.qdrant.io"
os.environ['QDRANT_API_KEY'] = "RdnriNBkmD9HpgKXPVpppZCgG7vxNJrXcIAbSPmRXsZkooZdlKaopw"

#create a qdrant client

client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)


# create a collection

os.environ['QDRANT_COLLECTION_NAME'] = "cheatsheet-collection"

vectors_config = qdrant_client.http.models.VectorParams(
    size = 1536, 
    #768 for instructor-xl, 1536 for openAi
    distance=qdrant_client.http.models.Distance.COSINE
    )

client.recreate_collection(
    collection_name = os.getenv("QDRANT_COLLECTION_NAME"),
    vectors_config=vectors_config
)

#vector store

os.environ["OPENAI_API_KEY"]="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"

embeddings = OpenAIEmbeddings()

vector_store = Qdrant(

    client=client,
    collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
    embeddings=embeddings,
)

#add documents to the vector store

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

with open('Qlik-functions.txt') as f:
    raw_text = f.read()

texts = get_text_chunks(raw_text)

vector_store.add_texts(texts)


#plug vector store retrieval chain

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever = vector_store.as_retriever() #querying the information from the vector store

)

query = "How to create symbols in qliksense"
response = qa.run(query)
print(response)