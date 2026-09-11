# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Here's a short prompt for Claude:

---

*The Plugin detail page (`/plugins/onboarding-context-pack`) and the Skill detail page (`/skills/mini`) should feel like the same design system, but they diverge significantly in the Install and Versions areas:*

*- The Skill page's Install tab has a rich "Installation Pipeline" diagram (SkillHub Server → Download → `~/.claude/skills/`), a "Quick Install" section with a direct download button + numbered CLI steps, and a separate "Copy & Paste Install" section with a "Copy Skill Content" button and manual steps.*
*- The Plugin page's "How to Use" tab only has a plain numbered text list (extract zip, open terminal, run `/plugin`, choose install from local path) — no pipeline visual, no direct download button, no copy-paste option, and it's under a differently-named tab ("How to Use" vs "Install").*

*Audit both detail-page components/routes and bring the Plugin page's Install experience up to parity with the Skill page's: same tab naming and order where it makes sense, the same installation-pipeline visual (adapted for a plugin's actual install path, e.g. into a plugins directory or via `/plugin install`), a one-click download of the plugin package, and a copy-paste fallback if applicable to plugins. Also check the stat row and remaining subtabs (Overview, Versions, and Skill's "Full Skill"/"Reviews" vs Plugin's "Members") for other inconsistencies worth resolving so both detail pages share one consistent layout and interaction pattern, adjusting only what's genuinely equivalent between a skill and a plugin (a plugin bundling multiple skills/hooks may legitimately need extra sections like "Members").*
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
