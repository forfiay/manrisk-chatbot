from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate

CHROMA_PATH = "chroma"
embeddings = FastEmbedEmbeddings()

model = ChatOllama(model="llama3.2:3b")
prompt = PromptTemplate.from_template(
        """ 
        You are the expert of risk management in Indonesia's banking industry. Your job is to answer questions related to your expertise, use the following context to answer the questions. Be as detailed as possible, but don't make up any information that's not from the context. If you don't know an answer, just say you don't know. Please never said that you know the answer from XXX file, or from XXX context.  
        {context}
        
        {question}
        """
    )

def chain_():
    vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "score_threshold": 0.5,
        },
    )
    chain = ({"context": retriever, "question": RunnablePassthrough()}
        |prompt
        |model
        |StrOutputParser()
    )
    return chain

def ask(chain, query:str):
    response = chain.invoke(
        query
    )
    return response

import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="🤖💬 Risk Management Chatbot")

st.header("Risk Management BOT 🤖")
st.caption("Chatbot yang akan membantu kamu menjawab pertanyaan terkait Manajemen Risiko di industri perbankan Indonesia 🏛")

def page():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hai👋 ada yang bisa dibantu?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask(chain_(), prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
if __name__ == "__main__":
    page()