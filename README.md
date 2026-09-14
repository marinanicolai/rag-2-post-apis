# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Remove the version information from the plugin card as shown to regular
users, without deleting the underlying version data or admin
functionality.

Context: The plugin's versioning logic still has an unresolved bug
(stacked Draft/Rejected version entries, "Submit for Review" appearing on
the wrong version). Rather than continue chasing that fix right now, hide
version-related UI from the plugin card for regular users so they aren't
seeing a confusing/incorrect Versions display.

Please:
1. Find every place on the plugin card and detail page where version
   info surfaces for a regular user: the "X Versions" stat in the stat
   row, the "Versions" tab, the version number next to the plugin name
   (e.g. "v1.0.4"), and anywhere else it appears.
2. Hide all of that from the regular user view.
3. Confirm whether admins still need version info to do plugin review
   (they likely do, to see submission history and act on Draft/Rejected
   versions) — if so, keep the Versions tab and stat visible in the
   admin view only, and tell me where that admin/user distinction is
   made elsewhere in the app so this follows the same pattern.
4. Do not change or touch the underlying version data model, submission
   flow, or the versioning bug itself — this is a display-only change.
   Leave a comment or note in the code marking this as a temporary hide
   pending the real versioning fix.
5. Add/update a test confirming a regular user's view of a plugin card
   has no version stat or tab, while an admin's view still does (if
   admins keep it).

Show me the diff and a screenshot of the plugin card as a regular user
would now see it.
------


This repository contains the **React + TypeScript + Vite frontend** for a **Retrieval-Augmented Generation (RAG) system**.  
It allows you to:

- Upload documents (PDF, Word, Excel)
- Ask natural-language questions
- Get AI-generated answers based only on your uploaded data

This repo is meant for **learning, exploring, and experimenting with RAG**, not just as a template UI.

---

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
