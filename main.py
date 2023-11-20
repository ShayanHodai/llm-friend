import openai
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message

def page_initial():
    """streamlit initial page
    """
    st.title("Hey! My name is Birdy 😊")
    st.title("How can I help you?")
    # message('Hey! My name is Birdy 😊 \n\nHow can I help you?', avatar_style='bottts')
    # st.image('Logo/Political Banter-logos_transparent.png')
    return None

def set_api_key():
    """check user OpenAI API key
    """
    with st.sidebar:
        st.title("About Birdy App 🦜")
        st.header("Your 24/7 available LLM firend!")
        st.markdown("Birdy is an application with the intention of being a considerate friend for everyone. The model has been built using OpenAI's gpt-3.5-turbo")
        user_key = st.text_input("Your OpenAI API key: ", key = "user_key")
        openai.api_key = user_key
        if user_key: 
            try: # check wether the entered key is valid by doing a test
                response = openai.Completion.create(
                engine="davinci",
                prompt="This is a test.",
                max_tokens=1)
            except:
                st.warning("Failed! \n OpenAI API key is not valid! Refresh the page and retry", icon= "⚠")
                exit(1)
            else:
                st.write("Success! ")
                return user_key
    
def model(user_key):
    """llm selection
    """
    return ChatOpenAI(model_name='gpt-3.5-turbo',temperature=0.5, openai_api_key=user_key)

def user_msg():
    """user message
    """
    user_text = st.chat_input("Enter text:", key = "user_text")
    return user_text

def chain(user_input, llm):
    """prompt engineering + memory 
    """
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
    """display chat history
    """
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user', avatar_style='no-avatar')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai', avatar_style='bottts')

def main():
    page_initial() # streamlit initial page
    user_key = set_api_key() # check user OpenAI API key
    if user_key:   
        llm = model(user_key) # llm selection
        user_input = user_msg() # user message
        chain(user_input, llm) # prompt engineering + memory 
        display() # display chat history

if __name__ == '__main__':
    main()




