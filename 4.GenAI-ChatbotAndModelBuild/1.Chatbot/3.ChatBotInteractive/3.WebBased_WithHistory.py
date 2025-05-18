import streamlit as st
import pandas as pd
import numpy as np
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


llm = ChatOllama(
    model="llama3",
    max_tokens=100,
)

# Maintain the history of the conversation
messages = []
st.title("Chatbot with History")
st.write("Welcome to my chatbot")

prompt = st.chat_input("Enter your message:")

if prompt:
    messages.append(HumanMessage(prompt)) # The user message is added to the history so that the model can use it to generate a more relevant response to the next user input
    response = llm.invoke(messages)
    messages.append(AIMessage(response.content)) # The AI message is added to the history so that the model can use it to generate a more relevant response to the next user input.
    st.write("Bot : "+response.content)
