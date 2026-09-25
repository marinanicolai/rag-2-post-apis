# 📦 Supply Chain RAG Explorer (React Frontend)

---
Start
----
ix(hook): environment variables can no longer weaken the policy
DLP_ENFORCEMENT, DLP_FAIL_MODE and DLP_RESTRICTIONS_DIR were read from the
process environment, which is the shell of the person the policy applies to.
Verified end to end on a document marked above the ceiling: exit 2 and a block
with no variable set, exit 0 and an advisory message with DLP_ENFORCEMENT=shadow.
No administrator rights and no file edit were needed.

An environment value is now honoured only when it is at least as strict as the
pack's own setting. Tightening still works, so an operator can harden a machine
without republishing the pack, while shadow and open are ignored when the pack
asks for enforce and closed. A rejected value is not silent: it is written to
the decision record as env_ignored, so an attempt to loosen the policy shows up
in the audit trail rather than disappearing.

DLP_RESTRICTIONS_DIR now ranks below the managed directory instead of above it.
Where an administrator has published a pack, that pack is the policy and the
variable cannot redirect the hook at a permissive copy. Where no managed pack
exists the variable still works, so development and testing a candidate pack
are unaffected.

How to verify:

    DLP_ENFORCEMENT=shadow python client/hook.py PreToolUse < payload.json

still exits 2 against a pack published with enforcement: enforce, and the
decision log records env_ignored=["DLP_ENFORCEMENT=shadow (weaker than enforce)"].

---
End
----

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
