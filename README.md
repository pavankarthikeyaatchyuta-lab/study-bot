# Study Bot – Generative AI Learning Assistant

An AI-powered Study Assistant API that answers academic questions in clear, simple language. Built with **FastAPI**, powered by **Groq's LLaMA 3.1 8B** (via LangChain), with persistent conversational memory backed by **MongoDB Atlas**.

🔗 **Live API:** [https://limitbreak-ai.onrender.com](https://limitbreak-ai.onrender.com)
📘 **Swagger UI:** [https://limitbreak-ai.onrender.com/docs](https://limitbreak-ai.onrender.com/docs)

---

## Overview

This project is a RESTful backend service that lets clients send a study-related question and receive an AI-generated, student-friendly explanation. It's deployed on **Render** as a production-style web service, with interactive API docs exposed via Swagger UI.

## Features

- 🤖 **Generative AI responses** — powered by Groq's `llama-3.1-8b-instant` model
- 🧠 **Conversational memory** — retains context across multiple turns per user
- 💾 **Persistent storage** — chat history saved in MongoDB Atlas
- 📚 **Study-focused** — system prompt constrains the bot to academic/learning questions, answered in simple language
- ☁️ **Cloud-deployed** — live on Render with public API access
- 📖 **Interactive docs** — Swagger UI for testing without Postman/cURL

## How Memory Works

Each interaction is stored in MongoDB with:

| Field | Description |
|---|---|
| `user_id` | Unique identifier for the user/session |
| `user_message` | The user's query |
| `bot_response` | The AI-generated reply |
| `timestamp` | Order of the interaction |

On each new request, prior messages for that `user_id` are retrieved and appended to the prompt sent to the LLM — simulating memory in an otherwise stateless API.

## Tech Stack

- **Framework:** FastAPI
- **LLM:** Groq LLaMA 3.1 8B (via `langchain-groq`)
- **Database:** MongoDB Atlas (`pymongo`)
- **Server:** Uvicorn
- **Deployment:** Render
- **Runtime:** Python 3.12.3

## API

### `POST /chat`

**Request body:**
```json
{
  "user_id": "student1",
  "message": "Explain Artificial Intelligence in simple words"
}
```

**Response:**
```json
{
  "response": "Artificial Intelligence (AI) is like having a smart assistant..."
}
```

Try it live at [`/docs`](https://limitbreak-ai.onrender.com/docs).

## Local Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/pavankarthikeyaatchyuta-lab/study-bot.git
   cd study-bot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with:
   ```
   GROQ_API_KEY=your_groq_api_key
   MONGODB_URI=your_mongodb_connection_string
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open `http://127.0.0.1:8000/docs` to test the `/chat` endpoint.

## Deployment

Deployed on Render as a managed web service:
- **Start command:** `uvicorn main:app --host 0.0.0.0 --port 10000` (see `start.sh`)
- **Runtime:** specified in `runtime.txt`
- **Environment variables:** `GROQ_API_KEY`, `MONGODB_URI` configured in Render dashboard

## Future Improvements

- User-facing frontend interface
- Authentication and user management
- Rate limiting / input validation
- Analytics on chat usage
- Trimming/summarizing long chat histories before they hit the prompt
