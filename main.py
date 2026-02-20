from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from db import chats_collection
from datetime import datetime

load_dotenv()

app = FastAPI()

# Use supported Groq model (old llama3-8b-8192 is decommissioned)
llm = ChatGroq(model="llama-3.1-8b-instant")

class ChatRequest(BaseModel):
    user_id: str
    message: str

def get_chat_history(user_id: str):
    history = chats_collection.find({"user_id": user_id}).sort("timestamp", 1)
    chat_text = ""
    for chat in history:
        chat_text += f"User: {chat['user_message']}\nBot: {chat['bot_response']}\n"
    return chat_text

@app.post("/chat")
def chat(request: ChatRequest):
    history = get_chat_history(request.user_id)

    system_prompt = (
        "You are a helpful AI Study Assistant. "
        "Answer only study-related or learning questions in simple words."
    )

    full_prompt = f"""
{system_prompt}

Previous conversation:
{history}

User: {request.message}
Bot:
"""

    response = llm.invoke(full_prompt).content

    chats_collection.insert_one({
        "user_id": request.user_id,
        "user_message": request.message,
        "bot_response": response,
        "timestamp": datetime.utcnow()
    })

    return {"response": response}