from agent.llm import LLM
import streamlit as st
import os
from dotenv import load_dotenv

st.title("Chatbot")

if "bot" not in st.session_state:
    load_dotenv()
    MODEL = os.environ.get("MODEL", "")
    st.session_state.bot = LLM(MODEL)

with st.sidebar:
    messages, delete_buttons = st.columns(2)
    st.write("# Chat History")
    if st.button("New Chat"):
        st.session_state.bot.memory.clear()
    for file in os.listdir("history"):
        file_name = file.split(".")[0]
        padded = file_name + (15 - len(file_name)) * " "
        with messages:
            if st.button(padded, key=file_name):
                st.session_state.bot.new_memory(file_name)
        with delete_buttons:
            if st.button(":red[X]", key=file_name + "delete"):
                os.remove("history/" + file)
                st.session_state.bot.memory.clear()
                st.rerun()

for message in st.session_state.bot.memory.get():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Please ask your Question"):
    with st.chat_message("user"):
        st.markdown(prompt)
    streamer = st.session_state.bot.query(prompt, stream=True)
    with st.chat_message("assistant"):
        content = st.write_stream(streamer)
        if type(content) == str:
            st.session_state.bot.process_agent_message(content)
        else:
            raise ValueError("Stream not a string")
        st.rerun()
