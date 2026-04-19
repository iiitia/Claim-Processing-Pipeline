from fastapi import FastAPI, UploadFile, File
import os
from app.pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Claim Processing API is running 🚀"}

@app.post("/api/process")
async def process_claim(claim_id: str, file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    try:
        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        result = run_pipeline(file_path, claim_id)
        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)