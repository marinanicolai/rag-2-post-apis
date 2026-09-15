# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Add a Feature/Unfeature action to the Plugins admin dashboard, matching
the Skills admin dashboard, and remove/replace the current delete-style
action on plugins.

Context: In the Skills admin table, each row's Actions column has two
buttons: a toggle that reads "Feature" or "Unfeature" depending on
current state, plus "Deprecate". The Plugins admin table currently only
shows a single action per row (labeled "Deprecate" for published
plugins, "No actions available" for others) — there's no Feature/
Unfeature toggle for plugins at all, and the existing action needs to be
removed.

Please:
1. Find the Skills admin table's Feature/Unfeature implementation: the
   button component, what data field it toggles (e.g. a `featured`
   boolean), how it affects display elsewhere (skills marked "Featured"
   show a badge on their detail page, per earlier screenshots — e.g. the
   "mini" skill shows a "Featured" tag).
2. Find the current Plugins admin table's action button — confirm
   exactly what it does when clicked (does it actually delete the
   plugin, or deprecate/unpublish it while keeping the record). Tell me
   which before changing anything.
3. Add the same Feature/Unfeature toggle to the Plugins admin table,
   reusing the skill's component/logic rather than reimplementing it,
   with an equivalent `featured` field on the plugin model if one
   doesn't already exist.
4. Make Feature/Unfeature available for plugins regardless of status
   (published, draft, rejected, etc.) the same way it's available across
   skill statuses — or flag if skills actually restrict it to certain
   statuses only, and match that instead.
5. Remove the current single delete-style action, unless step 2 reveals
   it's actually the same "Deprecate" action skills also have — in that
   case, keep Deprecate and add Feature/Unfeature alongside it (two
   buttons per row, exactly like skills), rather than removing it.
6. Make sure a plugin's "Featured" state surfaces the same way a
   skill's does — e.g. a "Featured" badge on the plugin card/detail page.
7. Add a test: toggling Feature/Unfeature on a plugin updates its state
   and the admin table reflects it immediately, mirroring an existing
   test for skills if one exists.


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
