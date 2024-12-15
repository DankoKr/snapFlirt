import requests
from app.utils.logger import logger
from app.utils.config import GROQ_API_URL, GROQ_HEADERS, MODEL_NAME

def generate_flirty_comment(description, emotions):
    """
    Use an LLM to generate a flirty comment based on description and emotions.
    """
    emotions_summary = ", ".join([f"{emotion}: {count}" for emotion, count in emotions.items() if count > 0])
    prompt = (
        f"Based on this description: {description}, and the detected emotions: {emotions_summary}, "
        f"write a short, clever, flirty pickup line no longer than 30 words. "
        f"Focus only on the pickup line."
    )

    payload = {"messages": [{"role": "user", "content": prompt}], "model": MODEL_NAME}

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=GROQ_HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No comment generated.")
    except requests.RequestException as e:
        logger.error(f"Error calling LLM API: {e}")
        raise
