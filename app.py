# from dotenv import load_dotenv
# import streamlit as st
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain.document_loaders import TextLoader
# from langchain.chains import RetrievalQA,StuffDocumentsChain,create_qa_with_sources_chain
# from langchain.prompts import PromptTemplate
# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.vectorstores import Qdrant
# from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
# from htmlTemplates import css, bot_template, user_template
# from langchain.llms import HuggingFaceHub
# import qdrant_client
# import os
# from htmlTemplates import css, bot_template, user_template
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from jinja2 import Template
# from langchain.callbacks.base import BaseCallbackHandler


# #adding class to handle streamlit callback
# class StreamlitCallbackHandler(BaseCallbackHandler):
#     def __init__(self, placeholder):
#         self.placeholder = placeholder
#         self.text = ""

#     def on_llm_new_token(self, token: str, **kwargs) -> None:
#         self.text += token
#         self.placeholder.markdown(self.text)


# # from firebase_admin import credentials
# # from firebase_admin import auth
# # from st_paywall import add_auth

# load_dotenv()
# # cred = credentials.Certificate('qlikbot-f2d02-7192216b6f67.json')
# # firebase_admin.initialize_app(cred)



# def get_vector_store():

#     #create a qdrant client

#     client = qdrant_client.QdrantClient(
#         os.getenv("QDRANT_HOST"),
#         api_key=os.getenv("QDRANT_API_KEY")
# )
#     embeddings = OpenAIEmbeddings()
#     #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

#     vector_store = Qdrant(

#         client=client,
#         collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
#         embeddings=embeddings,
# )
#     return vector_store

# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = get_vector_store()

# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI(temperature=0, 
#                      model="gpt-4.1", 
#                      streaming =  True, 
#                      callbacks=[StreamingStdOutCallbackHandler()])
#     memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

#     conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)
#     return conversation_chain

# def render_message(template, msg):
#     st.markdown(Template(template).render(MSG=msg), unsafe_allow_html=True)

# def display_chat():
#     if "chat_history" in st.session_state and st.session_state.chat_history:
#         for i, message in enumerate(st.session_state.chat_history):
#             if i % 2 == 0:
#                 render_message(user_template, message.content)
#             else:
#                 render_message(bot_template, message.content)

# def main():
#     load_dotenv()
#     st.set_page_config(page_title="Your personal QlikBot", layout="centered")
#     st.markdown(css, unsafe_allow_html=True)

#     st.header("Ask your QlikCheatsheet 💬")

#     # Init session state
#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     # Init vector store and chain
#     if st.session_state.conversation is None:
#         vector_store = get_vector_store()
#         st.session_state.conversation = get_conversation_chain(vector_store)

#     # Display chat history first
#     display_chat()

#    # Chat input at the bottom
# user_input = st.chat_input("Ask a question about Qlik...")

# if user_input:
#     # Show user message
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Show assistant reply with streaming
#     with st.chat_message("assistant"):
#         response_placeholder = st.empty()
#         stream_handler = StreamlitCallbackHandler(response_placeholder)

#         # Run conversation with streaming callback
#         response = st.session_state.conversation(
#             {"question": user_input},
#             callbacks=[stream_handler]
#         )

#     # Update chat history
#     st.session_state.chat_history = response['chat_history']
#     st.rerun()
# if __name__ == '__main__':
#     main()

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
    st.set_page_config(page_title="Your personal QlikBot", layout="centered")
    st.markdown(css, unsafe_allow_html=True)

    st.header("Ask your QlikCheatsheet 💬")

    # Initialize session state
    if "conversation" not in st.session_state:
        vector_store = get_vector_store()
        st.session_state.conversation = get_conversation_chain(vector_store)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display existing chat history
    display_chat()

    # Chat input at the bottom
    user_input = st.chat_input("Ask a question about Qlik...")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Placeholder for assistant's streaming response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            stream_handler = StreamlitCallbackHandler(response_placeholder)

            # Run conversation with streaming callback
            response = st.session_state.conversation(
                {"question": user_input},
                callbacks=[stream_handler]
            )

        # Update chat history and rerun to show updated chat
        st.session_state.chat_history = response['chat_history']
        st.rerun()

if __name__ == '__main__':
    main()
