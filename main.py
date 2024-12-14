import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

HF_API_URL = os.getenv("HF_API_URL")
HF_API_KEY = os.getenv("HF_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
GROQ_HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

def analyze_image_with_blip(image_path):
    print("Analyzing image with BLIP...")
    with open(image_path, "rb") as image_file:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, data=image_file)

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No description generated.")
        elif isinstance(result, dict):
            return result.get("generated_text", "No description generated.")
        else:
            return "Unexpected response format."
    else:
        print(f"Error analyzing image: {response.status_code} - {response.text}")
        return None

def generate_flirty_comment(description, retries=3, delay=5):
    print("Generating flirty comment...")
    prompt = (
        f"Someone is described as: {description}. Write a flirty, playful message perfect for a dating app or social chat that’s short, catchy, and highlights their unique charm."
    )

    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "llama-3.1-8b-instant"
    }

    for attempt in range(retries):
        response = requests.post(GROQ_API_URL, json=payload, headers=GROQ_HEADERS)

        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "No flirty comment generated.")
        elif response.status_code in {500, 503}:
            print(f"Groq API is temporarily unavailable. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            print(f"Error generating flirty comment: {response.status_code} - {response.text}")
            return None

    return "Service unavailable after multiple retries."

def process_image_and_generate_flirt(image_path):
    description = analyze_image_with_blip(image_path)
    if description:
        print(f"Image Description: {description}")
        flirty_comment = generate_flirty_comment(description)
        return flirty_comment
    else:
        return "Unable to process the image."


if __name__ == "__main__":
    image_path = "gym-girl.png"
    flirty_comment = process_image_and_generate_flirt(image_path)
    print("Flirty Comment:", flirty_comment)
