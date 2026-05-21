import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL   = "openai/gpt-4o-mini"

SYSTEM_PROMPT = """You are Mindmosaic, a compassionate and empathetic AI mental health support assistant. 

Your role:
- Provide emotional support and a safe space to talk
- Listen actively and respond with empathy
- Suggest simple coping strategies (breathing, journaling, mindfulness)
- Speak naturally — user may write in English or Roman Urdu, respond in the same language
- Never diagnose or replace a real therapist
- Keep responses warm, concise (3-5 sentences), and supportive
- If someone seems to be in crisis, always encourage professional help

You are NOT a doctor. Always remind users to seek professional help for serious issues.
"""

def get_ai_response(history: list, user_message: str) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in history[-10:]:  # last 10 messages for context
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Mindmosaic Mental Health Chatbot"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "I'm taking a moment to gather my thoughts... Please try again. 💙"
    except Exception as e:
        return f"Something went wrong on my end. Please try again shortly. ({str(e)})"
