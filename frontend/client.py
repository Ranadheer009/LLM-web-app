import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
backend_url = os.getenv("URL")

st.title("Text genetation app")

user_input = st.text_input("Enter your prompt here")
if st.button("Generate"):
    if user_input:
        responce = requests.post("f{backend_url}/groq", json={"prompt": user_input})
        if responce.status_code == 200:
            st.success(responce.json().get("response", "No response from server"))
        else:
            st.error(f"Error: {responce.status_code} - {responce.json().get('detail', 'Unknown error')}")   
