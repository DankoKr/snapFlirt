# SnapFlirt - Flirty Comment Generator API

SnapFlirt is a FastAPI-based application that processes images to generate clever, flirty comments. It uses Google Cloud Vision to analyze images for objects, labels, and emotions, and integrates with a language model (LLM) to craft personalized pickup lines.

## Features

- Analyze uploaded images for objects, labels, and text using Google Cloud Vision.
- Detect common emotions like joy, sadness, anger, and confidence from faces in the image.
- Generate personalized and witty flirty comments using a language model (LLM).

## Requirements

- Google Cloud Vision API credentials

## Instalation

1. Create a python virtual env:

```bash
python -m venv venv
```

Or:

```bash
python3 -m venv venv
```

2. Activate the virtual env:

Windows (Command Prompt):

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

3. Install the requirements.txt

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root:

- GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
- GROQ_API_URL=https://api.groq.com/v1/chat/completions
- GROQ_API_KEY=your-llm-api-key

5. Run the server

```bash
uvicorn app.main:app --reload
```

6. Swagger UI Endpoints

http://127.0.0.1:8000/docs
