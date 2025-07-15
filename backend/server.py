from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

class Prompt(BaseModel):
    prompt: str

llm = ChatGroq(groq_api_key =api_key,model="llama-3.3-70b-versatile")
def chat_with_groq(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response

app = FastAPI()


@app.post("/groq")
def get_responce_from_groq(prompt:Prompt):
    if not prompt.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    response = chat_with_groq(prompt.prompt)
    return {"response": response.content.strip()}


