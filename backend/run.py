from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from embedding import extract_and_chunk_text, search
from llm_groq import generate_answer_with_groq

app = FastAPI()

# --- CORS so React can talk to this API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev
        "http://localhost:3000",   # CRA / other
        "https://rag-2-post-apis-git-main-marinanicolais-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
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
