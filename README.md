# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Fix incorrect stats on the plugin detail card (Versions / Published /
Skills / Hooks counts).

Context: An approved plugin ("onboarding-context-pack") actually contains
1 hook (hooks.json), 1 skill (SKILL.md), and 3 reference files. The
plugin detail card is showing "5 Skills" and "5 Hooks" — both wrong, and
suspiciously identical, which suggests they aren't being counted
independently. There's also no "References" stat shown at all.

Please:
1. Find the component that renders this card's stat row (Versions,
   Published, Skills, Hooks) and trace where each number comes from —
   a stored count on the plugin/version record, or something computed
   on the fly from the bundled files.
2. If computed from files: check whether it's counting distinct skill
   directories / hook entries correctly, or whether it's counting
   something broader (e.g. total files, total lines, or a leftover count
   from the extra-folder-per-hook bug we just fixed) and mislabeling that
   same number under both "Skills" and "Hooks".
3. If stored on the record: check whether it's set at submission time,
   approval time, or version-publish time, and whether it's being
   recalculated correctly after edits/approval — or whether it's stale
   from before other fixes landed.
4. Fix the counting so Skills = number of skills in the approved bundle,
   Hooks = number of hook entries, independently and accurately.
5. Decide (and tell me) whether reference files should get their own
   stat ("3 References") next to Skills/Hooks, or are intentionally
   omitted — if intentional, confirm that's still true post-fix; if not,
   add it.
6. Add a regression test: submit/approve a plugin with a known number of
   skills, hooks, and reference files, and assert the card's displayed
   counts match exactly.

Show me the diff, and a screenshot or rendered output of the fixed card
for this same plugin.
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
