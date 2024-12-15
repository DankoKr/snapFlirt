from fastapi import APIRouter, UploadFile
from app.services.vision_service import analyze_image
from app.services.llm_service import generate_flirty_comment

router = APIRouter()

@router.post("/generate-flirt/")
async def generate_flirt(file: UploadFile):
    """
    Analyze an image and generate a flirty comment.
    """
    try:
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        description, emotions = analyze_image(temp_file_path)
        flirty_comment = generate_flirty_comment(description, emotions)

        return {"description": description, "emotions": emotions, "flirty_comment": flirty_comment}
    except Exception as e:
        return {"error": str(e)}
