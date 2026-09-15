# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Versioning is still showing on the plugin card for regular users — fix
this for real this time.

Context: A previous task asked to hide version info (the version number
next to the plugin name, the "X Versions" stat, and the Versions tab)
from the plugin card for regular users, keeping it admin-only. It's still
showing. Since then, the versioning bug itself (SubmitPluginPage.tsx /
VersionSelector.tsx forcing version bumps) was also worked on, which may
have touched the same files and undone the hide, or the original hide
may never have covered every place version info renders.

Please:
1. Find every place version info currently renders on the plugin card
   and detail page for a regular user — check specifically: the version
   number next to the plugin name (e.g. "v1.0.4"), the version count
   stat in the stat row, and the "Versions" tab — and anywhere else you
   find it.
2. For each one, check git history/blame to see whether it was ever
   actually hidden and got reintroduced by later changes, or whether the
   original hide missed it entirely.
3. Confirm how the app currently distinguishes an admin view from a
   regular user view elsewhere (reuse that exact pattern — don't
   introduce a new way of checking role).
4. Hide all version info from the regular user view using that pattern.
   Keep it fully visible for admins, since they still need it for review.
5. Do NOT touch the versioning logic itself (that's tracked separately) —
   this should be a pure display/visibility fix.
6. Add a test that specifically checks a regular user's rendered plugin
   card/detail page contains no version number, version stat, or
   Versions tab, while an admin's does. This test should have caught the
   regression last time — make sure it actually would have.

Show me the diff and a screenshot of the plugin card as both a regular
user and an admin.
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
