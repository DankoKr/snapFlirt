import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
MODEL_NAME = "llama-3.1-8b-instant"
FRONTEND_URL = os.getenv("FRONTEND_URL")