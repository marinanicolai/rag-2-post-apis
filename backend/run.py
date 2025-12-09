from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from embedding import extract_and_chunk_text, search
from llm_groq import generate_answer_with_groq

app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
            "message": f"File '{file.filename}' uploaded and {total_chunks} chunks embedded successfully!"
        })
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

from pydantic import BaseModel

class AskRequest(BaseModel):
    q: str

@app.post("/ask/")
async def ask_question(req: AskRequest):
    try: 
        # for debugging porposes you can use import pdb;pdb.set_trace() -pausing the executin and getting the var data, c al the code, n line by line
        chunks = search(req.q, top_k=2)
        answer = generate_answer_with_groq(req.q, chunks)


        return {
            "query": req.q,
            "answer": answer,
        }
    except Exception as e:
        return {"error": str(e)}