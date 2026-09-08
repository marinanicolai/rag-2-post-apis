# 📦 Supply Chain RAG Explorer (React Frontend)


Same root cause showing up on the hooks path too — makes sense this is one shared bug across skills/hooks/plugins rather than three separate ones. Here's a prompt that has Claude fix it everywhere at once:

---

*Confirmed the same bug affects hooks, not just plugins: after deleting a rejected hook from the Admin Review Queue, resubmitting a hook with the same slug fails with "Hook with slug 'onboardin-hooks' already exists" — even though it was deleted. This is the identical pattern already found with plugin versions ("Version '1.0.0' already exists..." after deleting a rejected plugin submission).*

*This points to one shared root cause rather than three separate bugs: investigate the delete/reject logic across all three submission types (skills, hooks, plugins) and find where uniqueness checks (slug for hooks/skills, version for plugins) are validated against records that a "Delete" in the admin panel doesn't actually remove — likely a shared soft-delete pattern, or the delete action only updates status without clearing/freeing the unique key, or the uniqueness query doesn't filter out deleted/rejected rows.*

*Fix the shared logic once: either make admin delete a true hard-delete of the record, or (if history should be preserved) exclude soft-deleted/rejected records from all uniqueness checks (slug, version, etc.) across skills, hooks, and plugins. Add regression tests for all three: submit → reject → delete → resubmit with the same slug/version should succeed in each case.*
----


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
