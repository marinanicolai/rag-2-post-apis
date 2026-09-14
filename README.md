# 📦 Supply Chain RAG Explorer (React Frontend)

-----
Add the missing tabs to the plugin detail page to match what an individual
skill's detail page already has.

Context: A skill's detail page (Overview → View full details) has six
tabs: Overview, Full Skill, How to Use, Install, Versions, Reviews. The
plugin detail page currently only has three: Overview, Install, Versions.
Add the missing ones so plugins have parity with skills.

Please:
1. Find the skill detail page's tab component and how "Full Skill" and
   "Reviews" are implemented there (what data each pulls, and any
   "How to Use" tab if one exists for skills — confirm whether it does).
2. For "Full Skill" equivalent on a plugin: since a plugin bundles
   multiple skills/hooks/references rather than one file, decide (and
   show me the options rather than guessing) what "full content" means
   for a plugin — e.g. a combined view of all bundled SKILL.md files and
   hooks.json, or a file-tree browser of everything in the bundle. Use
   whichever fits the existing data model with least new plumbing.
3. Add a "Reviews" tab to the plugin page reusing the same
   rating/write-a-review component skills use, scoped to the plugin
   instead of the skill.
4. Add "How to Use" to the plugin page if it exists for skills and is
   missing from plugins.
5. Match tab styling/order to the skill page exactly.
6. Add a test that loads a plugin's detail page and asserts all expected
   tabs render with non-empty content.

Show me the diff and a screenshot of the updated plugin page's tab bar.

----

Add plugin-authoring guidance to the Guide page.

Context: The Guide page currently has no content helping a user
understand what a plugin is or how to define/submit one. Add it.

Please:
1. Check what the Guide page currently covers for skills/hooks
   submission, so the new plugin section matches its structure, tone,
   and depth rather than introducing an inconsistent format.
2. Write a "Defining a Plugin" section covering:
   - What a plugin is (a bundle of skills + hooks + reference files)
     and when someone should package things as a plugin vs. submitting
     a standalone skill or hook.
   - The required plugin.json fields (name, version, etc.) and what
     each one means.
   - The expected folder/file structure (skills/, hooks/, references/)
     — pull this from the actual structure the app generates/expects,
     not from assumption.
   - The submission → review → approval flow, and what "version" means
     for a plugin.
3. Link out to (or embed) the existing skill/hook submission guidance
   where it overlaps, rather than duplicating it.
4. Add this as a new tab/section on the Guide page consistent with
   existing navigation.

Show me the diff and the rendered Guide page section.


------



Fix plugin version handling so it matches how skill versioning works —
currently a rejected plugin submission creates a new stacked version
entry, and "Submit for Review" ends up on the wrong (oldest) version.

Context: A plugin with one skill and one hook, resubmitted after
rejection, ends up with three version entries (v1.0.0 Draft, v1.0.1
Rejected, v1.0.2 Rejected) and the "Submit for Review" button appears on
v1.0.0 instead of the current one. Skills don't behave this way — a
skill resubmission after rejection does not create a stack of version
entries.

Please:
1. Find how skill submission/resubmission handles versioning — confirm
   whether it updates the same version record in place on resubmission,
   or otherwise avoids creating a new version per rejected attempt.
2. Find where plugin submission diverges from this — likely the same
   shared logic issue as the earlier hook-folder bug, where plugin
   submission isn't reusing the skill's versioning behavior correctly.
3. Fix plugin resubmission to behave the same way skills do: no
   accumulating Draft/Rejected version entries from repeated submission
   attempts on what is still conceptually "the first version."
4. Fix "Submit for Review" so it only ever appears on the current
   actionable version (never on a stale/older entry).
5. Decide what should happen to the existing already-created v1.0.1/
   v1.0.2 Rejected records for plugins already in this broken state —
   flag this rather than silently deleting data, and propose a
   migration if needed.
6. Add a regression test: submit a plugin, get it rejected, resubmit,
   and assert only one version entry exists (or whatever matches the
   confirmed skill behavior) with "Submit for Review" in the right
   place.

Show me the diff and the before/after Versions tab for this plugin.

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
