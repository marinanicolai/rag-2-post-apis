# 📦 Supply Chain RAG Explorer (React Frontend)

-----



*When a plugin folder is submitted and lands in the Admin review view, the file paths shown don't match what was uploaded — they've been renamed with an added hash suffix, and in the hook's case the file itself changed type:*

- *Uploaded: `skills/onboarding-tour/SKILL.md` → Review shows: `skills/onboarding-tour-cf1d104f/SKILL.md` (slug + hash appended to the folder name)*
- *Uploaded: `hooks/hooks.json` → Review shows: `hooks/offers-a-one-time-onboarding-tour-on-first-session-in-a-repo-then-stays-silent-19a43813/HOOK.md` (folder renamed to a slugified version of the hook's description + hash, and the file itself changed from `hooks.json` to `HOOK.md` — worth checking whether the actual JSON content survived this at all, since the preview just shows the description text repeated, not the hook config)*
- *`references/architecture.md` kept its own filename, only the parent skill folder was renamed.*

*Find where the plugin submission is persisted/stored for review (the step between the folder upload and the Admin Review Queue) and identify why it's regenerating folder/file names — likely a slugify-for-uniqueness step (turning the skill/hook's name or description into a slug and appending a content hash) that's being applied to storage paths instead of just being used as an internal ID.*

*Fix it so the review view displays the original folder/file paths and names exactly as uploaded (`skills/onboarding-tour/SKILL.md`, `hooks/hooks.json`, etc.) — any internal slug+hash the system needs for storage/dedup should stay an internal identifier, never overwrite the user-facing path or the file's own name/extension. Also confirm the hook's actual JSON content (not just its description) is what's actually being stored and shown, not a synthesized placeholder.*

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
