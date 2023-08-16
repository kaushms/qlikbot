from dotenv import load_dotenv
import streamlit as st

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
import streamlit as st

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ by <a style='display: block; text-align: center;' href="https://www.youtube.com/@thinkmetrics/videos" target="_blank"> Thinkmetrics </a></p>
</div>
"""

def get_vector_store():

    #create a qdrant client

    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
)
    embeddings = OpenAIEmbeddings()

    vector_store = Qdrant(

        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embeddings=embeddings,
)

    return vector_store


def main():
    load_dotenv()
    st.set_page_config(page_title="Your personal QlikBot")
    st.header("Ask Qlik bot 🤖")
    st.caption("Your AI Powered Qlik helper")
    st.markdown(footer,unsafe_allow_html=True)
    # create vector store
    vector_store = get_vector_store()
    
    # create chain s
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )

    # show user input
    user_question = st.text_input("Ask a question about Qlik front end functions:")
    if user_question:
        st.write(f"Question: {user_question}")
        answer = qa.run(user_question)
        st.write(f"Answer: {answer}")



    
    
 
        
if __name__ == '__main__':
    main()