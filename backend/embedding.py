import os
import faiss
import numpy as np
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# -------------------------
# 1️⃣ Load Embedding Model
# -------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)
DIMENSIONS = 384  # embedding dimension of all-MiniLM-L6-v2

# -------------------------
# 2️⃣ FAISS + Chunk Storage
# -------------------------
INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks_store.pkl"

# Load or create FAISS index
if os.path.exists(INDEX_FILE):
    faiss_index = faiss.read_index(INDEX_FILE)
    print("✅ Loaded FAISS index")
else:
    faiss_index = faiss.IndexFlatL2(DIMENSIONS)
    print("✅ Created new FAISS index")

# Load or initialize chunk store
if os.path.exists(CHUNKS_FILE):
    with open(CHUNKS_FILE, "rb") as f:
        chunks_list: List[Dict] = pickle.load(f)
    print("✅ Loaded chunk store")
else:
    chunks_list: List[Dict] = []
    print("✅ Initialized empty chunk store")

# -------------------------
# 3️⃣ Embedding Function
# -------------------------
def get_embedding(text: str) -> np.ndarray:
    """Return embedding vector for a given text."""
    return embedding_model.encode([text])[0].astype("float32")

# -------------------------
# 4️⃣ Extract & Chunk Any File
# -------------------------
def extract_and_chunk_text(file_path: str) -> int:
    """
    Extract text from PDF/DOCX/XLSX and store as chunks with embeddings.
    Returns number of chunks added.
    """
    ext = file_path.lower()

    # Import loaders
    from loaders.pdf import chunk_pdf_content
    from loaders.doc_loader import chunk_docx_content
    from loaders.excel import chunk_excel_content

    # Extract chunks
    if ext.endswith(".pdf"):
        chunks = chunk_pdf_content(file_path)
    elif ext.endswith(".docx"):
        chunks = chunk_docx_content(file_path)
    elif ext.endswith(".xlsx") or ext.endswith(".xls"):
        chunks = chunk_excel_content(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Add chunks to FAISS and store
    for chunk_text in chunks:
        emb = get_embedding(chunk_text)
        faiss_index.add(np.array([emb]))  # add to FAISS

        # Store chunk text + source file
        chunks_list.append({
            "text": chunk_text,
            "source": file_path
        })

    # Save FAISS and chunk store
    faiss.write_index(faiss_index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks_list, f)

    return len(chunks)

# -------------------------
# 5️⃣ Semantic Search
# -------------------------
def search(query: str, top_k: int = 5) -> List[Dict]:
    """
    Returns top-K chunks semantically closest to the query.
    Each chunk contains 'text' and 'source'.
    """
    query_emb = get_embedding(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_emb, top_k)

    results = []
    for idx in indices[0]:
        if idx == -1 or idx >= len(chunks_list):
            continue
        chunk = chunks_list[idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["source"]
        })

    return results

# -------------------------
# 6️⃣ Debug / Info
# -------------------------
print("FAISS index size:", faiss_index.ntotal)
print("Number of chunks stored:", len(chunks_list))
print("FAISS index type:", type(faiss_index))