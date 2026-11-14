import streamlit as st
import ollama
from typing import Dict, Generator
from openai import OpenAI

client = OpenAI()

def ollama_generator(model:str, messages:Dict) -> Generator:
    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True
    )
    for chunk in stream:
        yield chunk['message']['content']

def openai_generate(messages:Dict):
    stream = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


st.title("大學生求職指南")
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
st.session_state.selected_model = st.selectbox(
    "Please select the model:", [model["name"] for model in ollama.list()["models"]]+["OpenAI"])
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("How could I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response=""    
    with st.chat_message("assistant"):
        if st.session_state.selected_model in ["llama3.1:latest","llama3.1:8b","test:latest"]:
            response = st.write_stream(ollama_generator(
                st.session_state.selected_model, st.session_state.messages))
        elif st.session_state.selected_model == "OpenAI":
            response = st.write_stream(openai_generate(
                st.session_state.messages))
    st.session_state.messages.append(
        {"role": "assistant", "content": response})