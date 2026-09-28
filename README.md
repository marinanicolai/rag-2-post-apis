# 📦 Supply Chain RAG Explorer (React Frontend)

---
Start
----
```
 quick update on the DLP hooks work. Everything is on my branch `marina-dev` in data-loss-protection-toolkit (pushed, tests green, pack validates 28/28). No merge request yet; I wanted your input on a few decisions first.

Where it stands against your requirements:
1. Unmarked files: Office and PDF attachments with no recognized marking are now blocked (classification-label-required is enabled, using the PACK.md ladder instead of the old regex placeholder).
2. Files above INTERNAL FR: blocked by classification-ceiling (unchanged).
3. Classified text: detected in prompts and file text where the marking is present.
4. Prompts and pre-tool calls: both covered, including @ mentions with spaces in the file name and Bash commands that read files.
5. Blocks outright with an explanation message.
6. Audit log: working, and DLP_AUDIT_LOG can't override an admin policy.

I also fixed some hardening issues along the way: garbled input and timeouts now block instead of allowing, env variables can no longer weaken the policy, and file types no longer depend on the Windows registry (Excel was making .csv look like an Office file).

Decisions I need from you:
- PUBLIC has no marking in the ladder, so a public PDF or Word doc is currently blocked as unmarked. How should public documents be marked, or should PUBLIC get a marking?
- Should "unmarked files" cover documents only (Office and PDF, current scope), or also CSV, code and plain text?
- Files the hook can't read (images, scanned PDFs, encrypted files) are currently logged, not blocked. Do you want them blocked?

 Happy to walk you through it on a quick call if that's easier, let me know


```




```

```
git diff --stat
```
```

python scripts\zscaler_spec.py
python -m pytest tests -q
```

```
git status --short
```

test

```
        fc.text.strip()
    )

    # Any of these means the text in hand is not the file's text. The strings
    # fallback matters most: it pulls readable runs out of any binary, so a
    # password-protected .docx used to arrive looking successfully inspected.
    # A document extractor that returned nothing counts too, which covers a PDF
    # with no text layer. PDF extractors are named "pdf:pypdf", "pdf:strings"
    # and "pdf:heuristic", hence the prefix and suffix checks.
    if (
        fc.extractor in ("strings", "none")
        or fc.extractor.endswith(":strings")
        or fc.error is not None
        or fc.truncated
        or (fc.extractor.startswith(("office", "pdf")) and not fc.has_text)
    ):
        fc.inspected = False

    return fc
```
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
