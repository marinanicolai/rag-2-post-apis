# 📦 Supply Chain RAG Explorer (React Frontend)

-----


---

*Add optional support for reference files in the Skill submission flow (both the manual form and the SKILL.md upload/folder-upload paths). Skills can optionally include a `references/` subfolder alongside `SKILL.md` (as seen in `skills/onboarding-tour/references/architecture.md`, `glossary.md`, `ownership.md`) — right now there's no way to attach these when submitting.*

*1. In the manual submission form, add an optional "Reference Files" section where users can upload 0–3 (or however many is reasonable) supporting `.md` files, each with its own filename.*

*2. In the drag-and-drop / folder-upload flow, detect any `references/*.md` files inside a skill's folder and list them in the detected-files summary as attached reference docs for that skill (not as separate skills).*

*3. Store these files as supporting attachments tied to the skill record — keep them clearly separate from the skill's own name/description, since we just fixed a bug where a `references/architecture.md` file was mistakenly parsed as if it were the skill itself. Reuse that fix's boundary: reference files should never feed the skill's name/description parsing.*

*4. Show the reference files in the Admin review panel (read-only list/preview) alongside the skill content, and make them downloadable/viewable on the skill's public page after approval.*

*Keep this optional — a skill with no `references/` folder should submit exactly as it does today.*

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
