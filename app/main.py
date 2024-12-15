from fastapi import FastAPI
from app.routes import router
from app.utils.logger import setup_logging

setup_logging()

app = FastAPI(title="Flirty Comment Generator API")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the SnapFlirt API!"}
