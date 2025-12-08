
# 📦 Supply Chain AI Assistant (RAG Application)

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to upload business documents (Excel, PDF, Word) and ask intelligent questions about **inventory, suppliers, orders, and forecasts**.  

This system combines:
- ✅ **FastAPI backend** for document ingestion, embeddings, and AI reasoning  
- ✅ **Streamlit UI** for rapid internal testing and demos  
- ✅ **Vector search + LLMs** for accurate, document-grounded answers  
- ✅ Future-ready architecture for **React production frontend**

---

## 🚀 Features

- 📄 Upload business documents (Excel, PDF, DOCX)
- 🧠 Automatic text extraction & chunking
- 🔍 Vector embeddings for semantic search
- 💬 AI-powered Q&A over your private data
- 📊 Document-grounded answers (not hallucinations)
- ⚡ Real-time interaction through a clean UI
- 🔐 Designed for enterprise data security

---

## 🧠 How RAG Works in This Project

1. **User uploads a file**
2. **Text is extracted and chunked**
3. **Chunks are converted into embeddings**
4. **Embeddings are stored in a vector database**
5. **User asks a question**
6. **Relevant chunks are retrieved**
7. **LLM generates an answer using only retrieved context**

✅ This ensures **accurate, secure, and explainable AI responses**

---

## 🏗️ Architecture Overview

```

Frontend (Streamlit → React)
│
▼
FastAPI Backend (RAG Engine)
│
▼
Embeddings → Vector Search → LLM Response

````

| Layer | Technology |
|--------|-------------|
| Frontend (Current) | Streamlit |
| Frontend (Planned) | React + TypeScript |
| Backend API | FastAPI |
| Embeddings | OpenAI / HF |
| Vector DB | FAISS |
| LLM | GPT / Open Source |
| File Parsing | pandas, PyMuPDF, python-docx |

---

## 🎯 Use Case Examples

- ✅ Analyze supplier risks from Excel sheets  
- ✅ Query large procurement reports instantly  
- ✅ Ask natural language questions about inventory  
- ✅ Compare sales forecasts vs actuals  
- ✅ Internal enterprise knowledge assistant  

---

## 🧪 Development UI (Streamlit)

The Streamlit UI is used as a:
- Rapid prototyping interface  
- Debug console for embeddings and retrieval  
- Internal demo tool  

It will later be replaced by a **React enterprise frontend** for:
- Authentication
- User roles
- Multi-tenant usage
- Usage analytics
- Production deployment

---

## 🖥️ Running the Project Locally

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
````

---

### 2️⃣ Start the FastAPI Backend

```bash
uvicorn run:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Start the Streamlit UI

```bash
streamlit run supply_chain_app.py
```

UI runs at:

```
http://localhost:8501
```

---

## 🧩 API Endpoints

| Method | Endpoint   | Purpose                  |
| ------ | ---------- | ------------------------ |
| POST   | `/upload/` | Upload + embed documents |
| POST   | `/ask/`    | Ask questions            |
| GET    | `/health`  | System health check      |

---

## 📌 Roadmap

✅ Phase 1 – Streamlit RAG UI
✅ Phase 2 – FastAPI AI Backend
🚧 Phase 3 – React Frontend
🚧 Phase 4 – Auth & User Sessions
🚧 Phase 5 – Production Cloud Deployment
🚧 Phase 6 – Monitoring & Analytics

---

## 🔐 Data Security

* ✅ No public document exposure
* ✅ Private embeddings only
* ✅ Role-based access (planned)
* ✅ API-level request validation
* ✅ Secure model inference boundary

---

## 👩‍💻 Author

**Marina Nicolai**
Senior Frontend / Full-Stack Developer transitioning into **AI & ML Engineering**
Specializes in:

* RAG pipelines
* AI internal tools
* Enterprise BI & automation
* React, FastAPI, Python, AWS

---

## ⭐ Why This Project Matters

This project demonstrates:

* ✅ End-to-end AI system design
* ✅ Real business value
* ✅ Production-ready architecture
* ✅ Scalable frontend/backend separation
* ✅ Responsible use of enterprise AI

---

## 🤝 Contributions

Contributions, feedback, and collaboration ideas are welcome!

---

## 📜 License

MIT License

