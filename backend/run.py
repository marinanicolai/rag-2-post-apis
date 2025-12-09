import time
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from embedding import extract_and_chunk_text, search
from llm_groq import generate_answer_with_groq

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

app = FastAPI()

# --- CORS (for React / Vercel / localhost) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    start = time.time()
    logger.info("➡️ /upload called with filename=%s", file.filename)

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info("✅ Saved file to %s", file_path)

        # Extract chunks + auto-store in FAISS
        logger.info("⏳ Calling extract_and_chunk_text...")
        total_chunks = extract_and_chunk_text(file_path)
        logger.info("✅ extract_and_chunk_text finished, chunks=%d", total_chunks)

        logger.info("✅ /upload finished in %.2f sec", time.time() - start)
        return JSONResponse({
            "message": f"File '{file.filename}' uploaded and {total_chunks} chunks embedded successfully!",
            "filename": file.filename,
            "chunks": total_chunks,
        })

    except Exception as e:
        logger.exception("❌ Error in /upload: %s", e)
        return JSONResponse({"error": str(e)}, status_code=500)


class AskRequest(BaseModel):
    q: str


@app.post("/ask/")
async def ask_question(req: AskRequest):
    try:
        logger.info("➡️ /ask called with query=%s", req.q)
        chunks = search(req.q, top_k=2)
        answer = generate_answer_with_groq(req.q, chunks)
        logger.info("✅ /ask finished")

        return {
            "query": req.q,
            "answer": answer,
            # "sources": chunks  # you can add this later if you want
        }
    except Exception as e:
        logger.exception("❌ Error in /ask: %s", e)
        return {"error": str(e)}
