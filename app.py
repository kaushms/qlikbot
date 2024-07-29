from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
# used to create the memory
from langchain.memory import ConversationBufferMemory
# used to create the prompt template
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentExecutor

import qdrant_client
import os
import streamlit as st
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents.agent_toolkits import create_retriever_tool



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

    if 'example_question' not in st.session_state:
        st.session_state.example_question = ""


    st.set_page_config(page_title="Your personal QlikBot", page_icon="🤖")
    st.title("🚀 Qlik Bot: Your Qlik Assistant 🤖")
    st.caption("Your AI Powered Qlik helper")
    
# Define example questions
    example_questions = [
    "Set expression for last 12 months sales",
    "calculate max  sales per customer & country",
    "How to use conditional symbols",
    "Tell me a funny data joke"
    ]

     # Add footer information to the sidebar
    with st.sidebar:
        st.markdown("""
    <style>
    .sidebar-footer {
        background-color: #f8f9fa;
        color: #333;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .sidebar-footer a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }
    .sidebar-footer a:hover {
        text-decoration: underline;
    }
    .sidebar-footer p {
        margin: 5px 0;
    }
    </style>
    <div class="sidebar-footer">
        <p>Developed with ❤️ by</p>
        <p><a href="https://www.youtube.com/@thinkmetrics/videos" target="_blank">Thinkmetrics</a></p>
        <p><a href="mailto:thinkmetrics@gmail.com">thinkmetrics@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    # Add a horizontal line separator
    st.sidebar.markdown("---")

    # # Add a section for additional sidebar content
    # st.sidebar.subheader("Additional Options")
    # option1 = st.sidebar.checkbox("Option 1")
    # option2 = st.sidebar.checkbox("Option 2")

    # # Add a button
    # if st.sidebar.button("Click me!"):
    #     st.sidebar.write("Button clicked!")


    # create vector store
    vector_store = get_vector_store()
    
    # create chain s
    # qa = RetrievalQA.from_chain_type(
    #     llm=ChatOpenAI(model="gpt-3.5-turbo"),
    #     chain_type="stuff",
    #     retriever=vector_store.as_retriever()
    # )

    retriever=vector_store.as_retriever()
    tool = create_retriever_tool(
    retriever, 
    "search_qlik-cheatsheet",
    "Searches and returns answers regarding Qlik.")

        # This is needed for both the memory and the prompt
    memory_key = "history"
    if "memory" not in st.session_state.keys():
        st.session_state.memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

# Initialize the chat message history
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
        {"role": "assistant", "content": "Ask a question about Qlik front end functions:"}
    ]


    memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

    tools = [tool]

    # define the prompt
    system_message = SystemMessage(
        content=(
            "Do your best to answer the questions. "
            "Feel free to use any tools available to look up "
            "relevant information, only if neccessary"
        )
)
    prompt_template = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

    llm = ChatOpenAI(temperature = 0, model="gpt-3.5-turbo")

    # Prompt for user input and display message history
    if prompt := st.text_input("How can I help you today?", value=st.session_state.example_question):

        #prompt := st.chat_input("Ask a question about Qlik front end functions:"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display example questions as buttons in a horizontal layout
    st.markdown("<h6>Example Questions</h6>", unsafe_allow_html=True)  # Using h4 for a smaller header
    cols = st.columns(len(example_questions))
    for col, question in zip(cols, example_questions):
        if col.button(question):
            st.session_state.example_question = question
            st.rerun()
            #st.experimental_rerun()

# Check if an example question was selected
    if st.session_state.example_question:
        prompt = st.session_state.example_question
        st.session_state.example_question = ""


    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
         st.write(message["content"])

    # instantiate agent
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=st.session_state.memory, verbose=True)  


    # Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
         with st.spinner("Thinking..."):
            response = agent_executor({"input": prompt})
            st.write(response["output"])
            message = {"role": "assistant", "content": response["output"]}
            st.session_state.messages.append(message) # Add response to message history



if __name__ == '__main__':
    main()