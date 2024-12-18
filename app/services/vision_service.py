import os
import io
import json
from google.cloud import vision
from google.oauth2.service_account import Credentials
from app.utils.logger import logger
from app.services.emotion_analysis import analyze_emotions
from app.utils.config import SERVICE_ACCOUNT_JSON

def create_vision_client():
    """
    Create a Vision API client using credentials from SERVICE_ACCOUNT_JSON.
    """

    if not SERVICE_ACCOUNT_JSON:
        raise EnvironmentError("SERVICE_ACCOUNT_JSON environment variable is not set.")

    try:
        service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in SERVICE_ACCOUNT_JSON: {e}")

    credentials = Credentials.from_service_account_info(service_account_info)

    return vision.ImageAnnotatorClient(credentials=credentials)

def analyze_image(image_path: str):
    """
    Analyze an image to extract labels, objects, and emotions.
    """
    logger.info("Analyzing image with Google Vision...")
    try:
        client = create_vision_client()
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.annotate_image({
            "image": image,
            "features": [
                {"type_": vision.Feature.Type.LABEL_DETECTION, "max_results": 10},
                {"type_": vision.Feature.Type.FACE_DETECTION, "max_results": 5},
                {"type_": vision.Feature.Type.OBJECT_LOCALIZATION},
                {"type_": vision.Feature.Type.TEXT_DETECTION},
            ],
        })

        description_parts = []
        emotion_counts = analyze_emotions(response.face_annotations)

        # Labels
        if response.label_annotations:
            labels = [label.description for label in response.label_annotations]
            description_parts.append(", ".join(labels))

        # Objects
        if response.localized_object_annotations:
            objects = [obj.name for obj in response.localized_object_annotations]
            description_parts.append("Objects detected include: " + ", ".join(objects))

        # Text
        if response.text_annotations:
            text_description = response.text_annotations[0].description.strip()
            description_parts.append(f"Text found: '{text_description}'.")

        description = " ".join(description_parts)
        return description, emotion_counts
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise
