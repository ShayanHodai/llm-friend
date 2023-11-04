import openai
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message

def page_initial():
    st.title("Birdy app 🦜 your LLM friend")
    message('Hey! My name is Birdy 😊 \n\nHow can I help you?', avatar_style='bottts')
    return None

def set_api_key():
    load_dotenv()
    with st.sidebar:
        user_key = st.text_input("Your OpenAI API key: ", key = "user_key")
        if user_key:
            if user_key == os.getenv('OPENAI_API_KEY'):
                st.write("Success! ")
                return user_key
            else:
                st.warning("Failed! \nAdd your OPENAI_API_KEY in the .env file first and retry!", icon= "⚠")
                exit(1)

def model(user_key):
    return ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0.5, openai_api_key=user_key)

def user_msg():
    user_text = st.chat_input("Enter text:", key = "user_text")
    return user_text

def chain(user_input, llm):
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="""your name is Birdy, act as a friend, Birdy. Engage user to talk more, while you listen more. Ask directed questions that users identify the root of problem.
        Root cause analysis. Always reply them in a warm way.""")
        ]
    if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("🧠 thinking ..."):
                response = llm(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))

def display():
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user', avatar_style='no-avatar')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai', avatar_style='bottts')

def main():
    page_initial() # initialize page
    user_key = set_api_key() # check the openai api key
    if user_key:   
        llm = model(user_key) # the llm
        user_input = user_msg() # user input
        chain(user_input, llm) # chat history + user input
        display() # display chat history

if __name__ == '__main__':
    main()




