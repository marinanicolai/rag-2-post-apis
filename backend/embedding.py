import os
import faiss
import numpy as np
import pickle
import logging
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

# -------------------------
# 1️⃣ Load Embedding Model (GLOBAL, once at startup)
# -------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DIMENSIONS = 384  # embedding dimension of all-MiniLM-L6-v2

logger.info("⏳ Loading embedding model: %s", MODEL_NAME)
embedding_model = SentenceTransformer(MODEL_NAME)
logger.info("✅ Embedding model loaded successfully.")

# -------------------------
# 2️⃣ FAISS + Chunk Storage
# -------------------------
INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks_store.pkl"

# Load or create FAISS index
if os.path.exists(INDEX_FILE):
    faiss_index = faiss.read_index(INDEX_FILE)
    logger.info("✅ Loaded FAISS index from %s", INDEX_FILE)
else:
    faiss_index = faiss.IndexFlatL2(DIMENSIONS)
    logger.info("✅ Created new FAISS index with dimension %d", DIMENSIONS)

# Load or initialize chunk store
if os.path.exists(CHUNKS_FILE):
    with open(CHUNKS_FILE, "rb") as f:
        chunks_list: List[Dict] = pickle.load(f)
    logger.info("✅ Loaded chunk store from %s", CHUNKS_FILE)
else:
    chunks_list: List[Dict] = []
    logger.info("✅ Initialized empty chunk store")

logger.info("FAISS index size at startup: %d", faiss_index.ntotal)
logger.info("Number of chunks stored at startup: %d", len(chunks_list))
logger.info("FAISS index type: %s", type(faiss_index))

# -------------------------
# 3️⃣ Embedding Helpers
# -------------------------
def get_embedding(text: str) -> np.ndarray:
    """Return embedding vector for a single text."""
    emb = embedding_model.encode(
        [text],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )[0]
    return emb.astype("float32")


def get_embeddings_batch(texts: List[str]) -> np.ndarray:
    """Return embedding matrix for a list of texts."""
    if not texts:
        return np.empty((0, DIMENSIONS), dtype="float32")

    embs = embedding_model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embs.astype("float32")

# -------------------------
# 4️⃣ Extract & Chunk Any File
# -------------------------
def extract_and_chunk_text(file_path: str) -> int:
    """
    Extract text chunks from PDF/DOCX/XLSX and store as chunks with embeddings.
    Returns number of chunks added.
    """
    logger.info("➡️ extract_and_chunk_text called for %s", file_path)
    ext = file_path.lower()

    # Import loaders lazily (avoids circular imports)
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

    logger.info("✅ Extracted %d chunks from %s", len(chunks), file_path)

    if not chunks:
        logger.warning("⚠️ No chunks extracted from %s", file_path)
        return 0

    # 🔥 Batch embeddings for speed instead of per-chunk calls
    logger.info("⏳ Creating embeddings for %d chunks...", len(chunks))
    embeddings = get_embeddings_batch(chunks)
    logger.info("✅ Created embeddings with shape %s", embeddings.shape)

    # Add to FAISS
    faiss_index.add(embeddings)

    # Store chunk text + source file
    for chunk_text in chunks:
        chunks_list.append({
            "text": chunk_text,
            "source": file_path,
        })

    # Persist FAISS and chunk store
    faiss.write_index(faiss_index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks_list, f)

    logger.info("✅ Saved FAISS index to %s", INDEX_FILE)
    logger.info("✅ Saved chunk store to %s", CHUNKS_FILE)
    logger.info("📊 FAISS index size now: %d", faiss_index.ntotal)
    logger.info("📊 Number of chunks stored now: %d", len(chunks_list))

    return len(chunks)

# -------------------------
# 5️⃣ Semantic Search
# -------------------------
def search(query: str, top_k: int = 5) -> List[Dict]:
    """
    Returns top-K chunks semantically closest to the query.
    Each chunk contains 'text' and 'source'.
    """
    logger.info("➡️ search called, query=%s, top_k=%d", query, top_k)

    if faiss_index.ntotal == 0 or len(chunks_list) == 0:
        logger.warning("⚠️ search called with empty FAISS index / chunks_list")
        return []

    query_emb = get_embedding(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_emb, top_k)

    results = []
    for idx in indices[0]:
        if idx == -1 or idx >= len(chunks_list):
            continue
        chunk = chunks_list[idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
        })

    logger.info("✅ search returning %d results", len(results))
    return results
