import streamlit as st
from langchain_community.llms.ollama import Ollama

from PromptGenerator import chat_bot_api

llm = Ollama(model="llama3:70b")
llm.base_url = 'http://172.28.105.30/backend'


def get_response(user_input):
    try:
        response = llm.invoke(user_input)
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


# Title of the application
st.title('NOMAD query generator')

# Text input for user question
user_input = st.text_input("What are you looking for in NOMAD database?", "")

if user_input:
    # Generate a response using the function defined above
    response = get_response(user_input)
    # Display the response
    st.text_area("Response", response, height=150)
