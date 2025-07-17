from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")

class Prompt(BaseModel):
    prompt: str
    enable_web:bool = False

llm = ChatGroq(groq_api_key =api_key,model="llama-3.3-70b-versatile")
def chat_with_groq(prompt: str,context: str = None) -> str:
    if context:
        full_prompt = f"Use the following context to answer the question:\n{context}\n\nQuestion: {prompt}"
    else:
        full_prompt = prompt
    response = llm.invoke(full_prompt)
    return response
def get_web_search_snippet(query: str) -> str:
    params = {
        "q": query,
        "api_key": serp_api_key,
        "engine": "google",
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    snippets = []

    # Extract top 2 organic results if available
    for result in data.get("organic_results", [])[:2]:
        snippet = result.get("snippet")
        if snippet:
            snippets.append(snippet)

    return "\n".join(snippets)


app = FastAPI()

@app.post("/groq")
def get_responce_from_groq(prompt:Prompt):
    if not prompt.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    if prompt.enable_web:
        context = get_web_search_snippet(prompt.prompt)
        response = chat_with_groq(prompt.prompt, context)
    else:
        response = chat_with_groq(prompt.prompt)
    return {"response": response.content.strip()}


