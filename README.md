# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Fix the plugin versioning bug at its actual root cause: SubmitPluginPage.tsx
and VersionSelector.tsx force a version bump on every save.

Context: Previous fixes only touched the display and the backend's
acceptance of in-place resubmission — they did NOT touch the form. As a
result, using "Edit & Resubmit" (changes-requested flow) or restarting
after rejection through the form still creates a new stacked version row
every time, because the form itself always bumps the version number on
save. The underlying "Resubmit same content, same version" capability was
never actually wired into the UI that triggers it.

Please:
1. Read SubmitPluginPage.tsx and VersionSelector.tsx and confirm exactly
   where/how a new version number gets generated on every save — is it
   auto-incremented unconditionally in the submit handler, computed in
   VersionSelector regardless of context, or something else.
2. Compare this against how skills handle the equivalent flow (edit +
   resubmit after rejection) — skills apparently don't have this bug, so
   use their submit flow as the reference implementation for what
   "correct" looks like.
3. Implement one of these two fixes — pick based on what you find, and
   tell me which you chose and why:
   (a) Minimal fix: make the form support a genuine "resubmit same
       content, same version" mode, so "Edit & Resubmit" after a
       changes-requested or rejected review updates the existing version
       row in place instead of always incrementing, while a deliberate
       new version (the user actually changing functionality/bumping
       semver themselves) still creates a new row.
   (b) Structural fix: split plugins into a review-attempt table
       (tracks each submission attempt, rejections, feedback) separate
       from a published-version table (tracks only actually-published
       versions) — mirroring exactly how skills are structured. This is
       the more durable fix if skills already use this pattern.
4. Whichever you pick, make sure "Submit for Review" appears only on the
   single current actionable entry, with no stacked Draft/Rejected rows
   accumulating from repeated resubmission of unchanged or lightly-edited
   content.
5. Add a regression test that specifically exercises the "Edit &
   Resubmit" button after a changes-requested review, and after a
   rejection, and asserts no new version row is created unless the
   submitter is intentionally publishing a new version.
6. Run the existing test suite (vitest) and confirm nothing that depends
   on the old versioning behavior breaks silently.

This is the third attempt at this bug — the first two fixed only display
and backend acceptance without touching the form that actually causes the
bump. Do not repeat that pattern: verify your fix by actually clicking
through "Edit & Resubmit" in the affected flow, not just checking that
data displays correctly after the fact.
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
