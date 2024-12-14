import os
import requests
import time
from dotenv import load_dotenv
from google.cloud import vision
import io

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

def analyze_image(image_path):
    print("Analyzing image with Google Cloud Vision...")
    try:
        client = vision.ImageAnnotatorClient()

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        # What to be detected
        response = client.annotate_image({
            'image': image,
            'features': [
                {'type_': vision.Feature.Type.LABEL_DETECTION, 'max_results': 10},
                {'type_': vision.Feature.Type.FACE_DETECTION, 'max_results': 5},
                {'type_': vision.Feature.Type.LANDMARK_DETECTION, 'max_results': 5},
                {'type_': vision.Feature.Type.OBJECT_LOCALIZATION},
                {'type_': vision.Feature.Type.TEXT_DETECTION}
            ]
        })

        description_parts = []

        # Handle Labels
        if response.label_annotations:
            labels = [label.description for label in response.label_annotations]
            description_parts.append(", ".join(labels))

        # Handle Faces
        faces = response.face_annotations
        if faces:
            face_count = len(faces)
            face_desc = f"There {'is' if face_count == 1 else 'are'} {face_count} face{'s' if face_count > 1 else ''}"
            # Describe emotions if present (add more)
            emotions_list = []
            for i, face in enumerate(faces, start=1):
                emotions = []
                if face.joy_likelihood > vision.Likelihood.POSSIBLE:
                    emotions.append("joyful")
                if face.surprise_likelihood > vision.Likelihood.POSSIBLE:
                    emotions.append("surprised")
                if emotions:
                    emotions_list.append(f"Face {i} appears {', '.join(emotions)}")
            if emotions_list:
                face_desc += " (" + "; ".join(emotions_list) + ")"
            description_parts.append(face_desc)

        # Handle Object Localization
        if response.localized_object_annotations:
            objects = [obj.name for obj in response.localized_object_annotations]
            description_parts.append("Objects detected include: " + ", ".join(objects))
        
        # Handle Text Detection
        if response.text_annotations:
            text_description = response.text_annotations[0].description.strip()
            if text_description:
                description_parts.append(f"Text found in the image: '{text_description}'.")

        full_description = " ".join(description_parts)
        return full_description if full_description else "Unable to generate a detailed description."

    except Exception as e:
        print(f"Error in Google Cloud Vision analysis: {e}")
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
    description = analyze_image(image_path)
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