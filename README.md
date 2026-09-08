# 📦 Supply Chain RAG Explorer (React Frontend)

Here's a short prompt for Claude:

---

*The real `hooks.json` uses the standard nested Claude Code hook schema:*

```json
{
  "description": "...",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear",
        "hooks": [
          { "type": "command", "command": "test -f ... || echo 'Onboarding notice...'" }
        ]
      }
    ]
  }
}
```

*But after upload/extraction, the Review Queue shows a completely different, wrong "Hook Configuration": a flat `{"hooks": [{"command": "echo \"hello from hook\"", "type": "command"}]}` — the real command (the `test -f ... || echo 'Onboarding notice...'` logic) isn't there at all, replaced by what looks like a hardcoded placeholder example.*

*Find the hook-parsing code that runs when a `hooks.json` file is uploaded/detected in a plugin or hook submission. It's likely written to expect a flat `hooks: [{type, command}]` array and either fails silently on the actual nested schema (`hooks.<EventName>[].hooks[].command`, with `matcher`) and falls back to a default/placeholder value, or it's grabbing the wrong node in the structure. Fix the parser to correctly walk the nested schema — for each event name (SessionStart, etc.), each matcher group, and each command inside `hooks[]` — and extract the real `type`/`command`/`matcher` values, so what's stored and shown in review matches exactly what's in the source file. Remove any hardcoded fallback/example value so a parse failure surfaces as a visible error instead of silently submitting fake data.*

*Add a test using this exact nested hooks.json (SessionStart + matcher + the onboarding-complete.md command) to confirm the extracted config matches the source file verbatim.*







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
