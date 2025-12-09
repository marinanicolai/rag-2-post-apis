import time
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from embedding import extract_and_chunk_text, search
from llm_groq import generate_answer_with_groq

app = FastAPI()

# --- CORS so React (Vercel) can talk to this API ---
# For now, keep it wide open while debugging.
# We can lock this down later to your exact Vercel + localhost origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow any origin for now
    allow_credentials=False,    # must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
async def health():
    return {"status": "ok"}

logger = logging.getLogger("uvicorn")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    start = time.time()
    logger.info("➡️ /upload called with filename=%s", file.filename)

    content = await file.read()
    logger.info("✅ File read: %d bytes", len(content))

    logger.info("⏳ Starting processing...")
    # TODO: your current PDF/text splitting/embedding code here
    # e.g. extract_text(content), split, embed, save, etc.
    logger.info("✅ Finished processing in %.2f sec", time.time() - start)

    return {"status": "ok"}
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract chunks + auto-store in FAISS
        total_chunks = extract_and_chunk_text(file_path)

        return JSONResponse({
            "message": f"File '{file.filename}' uploaded and {total_chunks} chunks embedded successfully!",
            "filename": file.filename,
            "chunks": total_chunks,
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


class AskRequest(BaseModel):
    q: str


@app.post("/ask/")
async def ask_question(req: AskRequest):
    try:
        # for debugging purposes you can use:
        # import pdb; pdb.set_trace()
        chunks = search(req.q, top_k=2)
        answer = generate_answer_with_groq(req.q, chunks)

        return {
            "query": req.q,
            "answer": answer,
            # later you can also return "sources": chunks
        }
    except Exception as e:
        return {"error": str(e)}
