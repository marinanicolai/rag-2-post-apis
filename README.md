# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Investigate and fix a bug in the skillhub app's SKILL.md generation.

Context: When a user uploads a skill/plugin file, the app auto-generates a
SKILL.md with YAML frontmatter containing `name` and `description` fields,
e.g.:
---
name: <kebab-case-slug>
description: <what it does and when to trigger it>
---

Bug: generated SKILL.md files have incorrect frontmatter — sometimes it's
an empty object (`{}`) instead of populated YAML, sometimes `name` doesn't
match the actual skill being uploaded.

Please:
1. Find the upload handler and the code path that builds/writes SKILL.md
   (search for "SKILL.md", "frontmatter", or wherever the file is
   templated).
2. Trace where `name` and `description` are supposed to come from — the
   uploaded file's own frontmatter, a form field, the filename, or an LLM
   call — and find exactly where that data gets lost, overwritten, or
   serialized wrong (e.g. dumping an empty dict instead of parsed fields,
   a key-mapping mismatch, or the YAML serializer stripping values).
3. Reproduce the bug with a sample upload and show me the broken output
   vs. the expected output.
4. Fix the root cause so every generated SKILL.md has valid, non-empty
   frontmatter matching the schema above.
5. Add or update a test that uploads a sample skill and asserts the
   resulting SKILL.md has the correct `name` and `description`.
6. Flag edge cases you find along the way — e.g. should an uploaded file's
   own existing frontmatter be preserved or always regenerated; how are
   duplicate or invalid names handled; what happens when description is
   missing from the source file.

Show me the diff and a before/after example of the generated SKILL.md.
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
