from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
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
<p>Developed with ❤️ by <a style='display: block; text-align: center;' href="https://www.youtube.com/@thinkmetrics/videos" target="_blank"> Thinkmetrics </a>
<a> Email: thinkmetrics@gmail.com </a></p>
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
    if prompt := st.chat_input("Ask a question about Qlik front end functions:"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

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