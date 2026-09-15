# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Investigate and fix a "Shell interpolation token" validation error blocking
legitimate hook submissions.

Context: After deleting a plugin and resubmitting it fresh, submission now
fails with an error: "Shell interpolation token in 'hoks/hooks.json'."
(note: the path in the error says "hoks" not "hooks" — could be a typo in
the error string, or a clue that something is truncating/mangling the
path before it's reported).

The hooks.json for this plugin contains a hook command using
${CLAUDE_PROJECT_DIR:-.} — this is a standard, documented variable
substitution pattern used in Claude Code hook commands, not inherently
malicious shell injection.

Please:
1. Search the codebase for the string "Shell interpolation token" to find
   the validator that's rejecting this submission.
2. Understand what it's checking for and why — is it a security check
   meant to block genuinely dangerous patterns (command substitution like
   $(...), backticks, unescaped pipes into eval, etc.) that's written too
   broadly and also catches safe ${VAR:-default} style substitution? Or
   is ${CLAUDE_PROJECT_DIR:-.} specifically supposed to be an allowed
   exception that isn't being recognized?
3. Fix the typo in the error message path ("hoks" → "hooks") and, more
   importantly, find why the reported path is wrong at all — trace
   whether the validator is reading/reporting the correct file path or
   whether something upstream is corrupting it.
4. Determine why this validation didn't block the plugin before deletion
   — was this hooks.json content unchanged from what was previously
   approved, meaning the validator is newly triggering on already-valid
   content (regression from a recent change)? Or is this genuinely new
   content that was never actually validated before?
5. Fix the validator so it distinguishes between safe, standard
   substitution patterns (e.g. ${CLAUDE_PROJECT_DIR:-.} and other
   documented Claude Code hook variables) and actually dangerous shell
   interpolation (command substitution, backticks, unescaped injection
   vectors) — allow the former, keep blocking the latter.
6. Add tests: one hooks.json using ${CLAUDE_PROJECT_DIR:-.} that should
   pass validation, and one using something like $(whoami) or backticks
   that should still be correctly rejected.

Show me the diff, and confirm by resubmitting this exact plugin that it
now passes.
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
