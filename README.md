# 📦 Supply Chain RAG Explorer (React Frontend)

---
Start
----
1. Make a demo folder with test documents outside the repo
```
New-Item -ItemType Directory -Force C:\temp\dlp-demo | Out-Null
python -c "from docx import Document; d=Document(); d.add_paragraph('Agenda for Tuesday: budget review, staffing.'); d.save(r'C:\temp\dlp-demo\unmarked.docx'); d=Document(); d.add_paragraph('INTERNAL FR'); d.add_paragraph('Agenda for Tuesday: budget review, staffing.'); d.save(r'C:\temp\dlp-demo\internal.docx'); d=Document(); d.add_paragraph('RESTRICTED FR'); d.add_paragraph('Draft notes for the demo.'); d.save(r'C:\temp\dlp-demo\restricted.docx')"
Copy-Item samples\files\restricted_fr_memo.txt C:\temp\dlp-demo\
Get-ChildItem C:\temp\dlp-demo

```
During the meeting

Part 1: it's all green (2 minutes)
```
git log --oneline -12
python scripts\validate_pack.py
python -m pytest tests -q



```
Part 2: map tests to his requirements (5 minutes). -v prints each test by name, which reads well on a shared screen:
```
python -m pytest tests\test_client_hook.py -v
python -m pytest tests\test_client_proxy.py -v  
```
Then show the risk register. It's the one-page summary of what's covered:

```

python scripts\risk_register.py --skip-pytest

```
Part 3: live in Claude Code (10 minutes). Open a terminal in the demo folder and start Claude Code:
```
cd C:\temp\dlp-demo
claude
```
Prompt in Claude Code	Expected	Requirement
```
summarize @unmarked.docx	Blocked

```
"does not appear to carry a classification marking"	#1
summarize @internal.docx	
```
Allowed	#1 and #2 (control)
```
summarize @restricted.docx	
```
Blocked by the ceiling rule	#2
```
Paste a line starting RESTRICTED FR and ask to rephrase it	Blocked on the prompt
```
#3, #4
run: type restricted_fr_memo.txt	Blocked before Bash runs	#4 (pre-tool call)

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
