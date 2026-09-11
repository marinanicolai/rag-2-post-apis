# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Fix a bug in hook submission: it's creating an unnecessary per-hook folder
and a redundant HOOK.md file that shouldn't exist.

Context: When a skill is submitted, the app creates
`skills/<skill-name>/SKILL.md` — one folder per skill, with a markdown
file describing it. That's correct for skills. Hook submission is now
doing the same thing (likely because it reuses shared submission logic),
producing:

  hooks/<long-slugified-description>/HOOK.md
  hooks/<long-slugified-description>/hooks.json

This is wrong. There should be no per-hook subfolder and no HOOK.md —
hook definitions belong directly in a single hooks.json (matcher +
command entries), matching the standard Claude Code plugin hooks
structure (a flat `hooks/hooks.json` at the plugin root, not nested
per-hook folders with their own doc file).

Please:
1. Find the code path that packages a submitted hook into the plugin's
   file structure, and confirm it's sharing logic with the skill
   packaging path (the one that creates `skills/<name>/SKILL.md`).
2. Identify exactly where it's (a) generating a folder name from the
   hook's description text, and (b) writing a HOOK.md file — these
   should not happen for hooks.
3. Fix it so a submitted hook is written into a single hooks.json
   (creating `hooks/hooks.json` if it doesn't exist yet, or appending/
   merging the new hook entry into it if it does), with no wrapper
   folder and no HOOK.md.
4. Make sure this doesn't break the reference-files feature we just
   added for hooks — reference files should still attach to the hook
   submission correctly without needing the now-removed folder as their
   anchor point. If reference files were relying on that folder to have
   somewhere to live, tell me and propose where they should live instead
   (e.g. alongside hooks.json, or wherever skills' references/ directory
   pattern would map for a flat-file structure).
5. Update or add tests that submit a hook and assert the resulting file
   list matches the expected flat structure (no extra folder, no
   HOOK.md).

Show me the diff, and the before/after file listing for a hook
submission.
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
