from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.utils.logger import setup_logging
from app.utils.config import FRONTEND_URL

setup_logging()

app = FastAPI(title="Flirty Comment Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URL,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"], 
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the SnapFlirt API!"}
