# 📦 Supply Chain RAG Explorer (React Frontend)

---
Start
----
```
Select-String -Path docs\risks.yaml -Pattern "docx_unlabeled" -Context 12,8```
```
  Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\\(\.git|__pycache__)\\' } | Select-String -Pattern "no marking and no sensitivity" -List | Select-Object Path
```

```
Select-String -Path docs\risks.yaml -Pattern "classification-ceiling" -Context 4,4

```

```
git diff --stat
```


test

```
        fc.text.strip()
    )

    # Any of these means the text in hand is not the file's text. The strings
    # fallback matters most: it pulls readable runs out of any binary, so a
    # password-protected .docx used to arrive looking successfully inspected.
    # A document extractor that returned nothing counts too, which covers a PDF
    # with no text layer. PDF extractors are named "pdf:pypdf", "pdf:strings"
    # and "pdf:heuristic", hence the prefix and suffix checks.
    if (
        fc.extractor in ("strings", "none")
        or fc.extractor.endswith(":strings")
        or fc.error is not None
        or fc.truncated
        or (fc.extractor.startswith(("office", "pdf")) and not fc.has_text)
    ):
        fc.inspected = False

    return fc
```
---
End
----

## 🧠 RAG System Architecture

Below is the high-level architecture of the full system (Frontend + Backend + AI Pipeline):

![RAG Architecture](./rag-frontend/src/assets/rag-1.png)

---

## 🧱 Tech Stack

* ⚛️ React 19
* 🟦 TypeScript
* ⚡ Vite
* 🎨 Custom dark/green UI
* 🌐 REST API integration (`upload` + `ask`)
* 🧠 RAG Pipeline (via FastAPI backend)
* 🔍 FAISS Vector Database
* 🤖 Groq LLaMA 3.3

---

## 📂 What This Repo Includes

* Upload UI for documents
* Question input & answer panel
* Status messages & error handling
* API connection layer (`src/api.ts`)
* Ready for deployment on **Vercel**

❗ This repo does **not** include the backend.
You must run the FastAPI RAG backend separately.

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If using a deployed backend (Railway, etc.):

```env
VITE_API_BASE_URL=https://your-backend-url.up.railway.app
```

---

## ▶️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/your-repo-name.git

# 2. Move into the project
cd your-repo-name

# 3. Install dependencies
npm install

# 4. Start the app
npm run dev
```

Then open:

```
http://localhost:5173
```

Make sure your **FastAPI backend is running at the API URL**.

---

## 🔄 How the RAG Flow Works

1. User uploads a file
2. Frontend sends it to the FastAPI backend
3. Backend:

   * Chunks the file
   * Creates embeddings
   * Stores them in FAISS
4. User asks a question
5. Backend:

   * Finds the most relevant chunks
   * Sends them to Groq LLaMA
6. AI-generated answer is returned to the UI

---

## 🚀 Deployment

This frontend is optimized for:

* ✅ **Vercel**
* ✅ **Netlify**
* ✅ Any static Vite-compatible host

Build command:

```bash
npm run build
```

Output folder:

```bash
dist
```

---

## 🎯 Who This Is For

* Developers learning **RAG architecture**
* Students exploring **LLMs + vector databases**
* Frontend engineers integrating **real AI systems**
* Anyone building **AI-powered document Q&A**

---
