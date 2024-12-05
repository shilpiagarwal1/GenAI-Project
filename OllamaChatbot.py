import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama.llms import OllamaLLM

import os
from dotenv import load_dotenv
load_dotenv()


#Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Q & A with Ollama"
#Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant.Please respond to the question asked"),
        ("user","Question:{question}")
    ]
    
)


def generate_response(question,engine,temperature,max_tokens):
    
    llm = OllamaLLM(model=engine)

    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

#Title of the app
st.title("Enhanced Q&A Chatbot with Ollama")

##Sidebar for settings
st.sidebar.title("Settings")

#Dropddown to select various Open AI models
engine=st.sidebar.selectbox("Select an Open AI Model",["gemma:2b"])

#Adjust Response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## Main Interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)
else:
    st.write("please provide the query")
    
