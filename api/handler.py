from mangum import Mangum
from app.main import app  

# Mangum wrapper to make FastAPI compatible with Vercel's serverless handler
handler = Mangum(app)
