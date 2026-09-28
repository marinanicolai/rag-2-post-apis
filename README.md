# 📦 Supply Chain RAG Explorer (React Frontend)

---
Start
----
```
---
id: classification-label-required
severity: high
action: deny
enabled: true
applies_to: [file]
detector:
  type: classification
  require_marking: true
  media_type_prefixes: ["application/vnd.openxmlformats", "application/vnd.ms-", "application/msword", "application/pdf"]
---

# Documents with no classification marking

Word, Excel, PowerPoint and PDF files that carry readable text but show no
recognized classification marking may not be sent to Claude. The
`classification-ceiling` rule only catches markings above the approved
ceiling, so a document with no marking at all would otherwise pass
silently. This rule closes that gap: every readable document must carry at
least the organization's lowest recognized marking before it can be sent.

How it works: the rule uses the same `classification` detector as
`classification-ceiling`, in `require_marking` mode. The list of recognized
markings comes from the ladder in `PACK.md`, so this rule never spells out
marking names and cannot drift from the manifest. In this mode the detector
reports only "unmarked"; markings above the ceiling are still handled by
`classification-ceiling`.

Scope: only files whose media type starts with one of `media_type_prefixes`
(Office Open XML, legacy Office, and PDF). Code, plain text and other files
are not checked by this rule. Files with no extractable text are handled by
`uninspectable-files`, not here.

Open decisions (pending with the policy owner):

- How public documents that carry no marking should be labeled so they are
  not blocked as unmarked.
- Whether "unmarked files" should cover only documents (current scope) or
  also code and plain text.

## Message to user

{file} does not appear to carry a classification marking. Every document
sent to Claude must show a recognized classification marking (at minimum,
the organization's lowest level) before it can be checked. Add the
appropriate marking to the file, or use an approved, already-labeled copy,
and try again. Reference: {reference_id}
```
```
Get-ChildItem -Recurse -File -Exclude *.pyc | Select-String -Pattern "classification-label-required" -List | Select-Object Path
```

```
Select-String -Path <pack-file> -Pattern "classification-label-required" -Context 2,20


```

```
git diff --stat
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
