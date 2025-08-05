
from dotenv import load_dotenv
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from htmlTemplates import css, bot_template, user_template
from langchain.callbacks.base import BaseCallbackHandler
from jinja2 import Template
import qdrant_client
import os

# Custom callback handler to stream tokens to Streamlit
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.placeholder.markdown(self.text)

def get_vector_store():
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

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(
        temperature=0, 
        model="gpt-4.1", 
        streaming=True
    )
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vectorstore.as_retriever(), 
        memory=memory
    )
    return conversation_chain

def render_message(template, msg):
    st.markdown(Template(template).render(MSG=msg), unsafe_allow_html=True)

def display_chat():
    if "chat_history" in st.session_state and st.session_state.chat_history:
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                render_message(user_template, message.content)
            else:
                render_message(bot_template, message.content)

def main():
    load_dotenv()
 
st.set_page_config(page_title="Your personal QlikBot", layout="wide")
st.markdown(css, unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="QlikBot", layout="wide")
    st.markdown(css, unsafe_allow_html=True)

    # Setup chat session
    if "conversation" not in st.session_state:
        st.session_state.conversation = get_conversation_chain(get_vector_store())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Page header
    st.markdown("<h1 style='text-align: center;color: #bd5d3a;'>Qlik AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Your personal Qlik helper</p>", unsafe_allow_html=True)
    #st.markdown("<h1 style='text-align: center; color: #da7756; font-family: ui-serif, Georgia, serif; font-size: 2.8rem; font-weight: 700;'>Qlik AI Assistant</h1>", unsafe_allow_html=True)
    #st.markdown("<p style='text-align: center; color: #3d3929; font-family: ui-serif, Georgia, serif; opacity: 0.75;'>Your personal Qlik helper</p>", unsafe_allow_html=True)
    # Layout: Sidebar (narrow) + Main panel
    col1, col2, col3 = st.columns([2, 5, 2])  # Sidebar | Main | Spacer

    # -- Left column (Chat history) --
    with col1:
        st.markdown("### 💬 History")
        if st.session_state.chat_history:
            for i, msg in enumerate(st.session_state.chat_history):
                sender = "You" if i % 2 == 0 else "Bot"
                st.markdown(f"- **{sender}**: {msg.content[:40]}...")

    # -- Center column (Chat UI) --
    with col2:
        display_chat()  # Render using your bot_template/user_template

        user_input = st.chat_input("Ask a question about Qlik...")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                handler = StreamlitCallbackHandler(placeholder)
                response = st.session_state.conversation(
                    {"question": user_input},
                    callbacks=[handler]
                )

            st.session_state.chat_history = response["chat_history"]
            st.rerun()

if __name__ == '__main__':
    main()
