from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from db import chats_collection
from datetime import datetime

load_dotenv()

app = FastAPI()

# Load API key from environment (works locally + Render)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM (Render-safe)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY
)

class ChatRequest(BaseModel):
    user_id: str
    message: str

def get_chat_history(user_id: str):
    if not chats_collection:
        return ""
    history = chats_collection.find({"user_id": user_id}).sort("timestamp", 1)
    chat_text = ""
    for chat in history:
        chat_text += f"User: {chat['user_message']}\nBot: {chat['bot_response']}\n"
    return chat_text

@app.post("/chat")
def chat(request: ChatRequest):
    # Get history safely
    try:
        history = get_chat_history(request.user_id)
    except Exception:
        history = ""

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

    # Call Groq safely
    try:
        response = llm.invoke(full_prompt).content
    except Exception as e:
        return {"error": f"Groq error: {str(e)}"}

    # Store in DB safely
    try:
        if chats_collection:
            chats_collection.insert_one({
                "user_id": request.user_id,
                "user_message": request.message,
                "bot_response": response,
                "timestamp": datetime.utcnow()
            })
    except Exception:
        pass

    return {"response": response}