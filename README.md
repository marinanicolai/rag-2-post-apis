# 📦 Supply Chain RAG Explorer (React Frontend)
Use the existing Figma design as the source of truth.

Create two new pages/frames:

1. Contributors
2. Help & Support

IMPORTANT: Before creating anything, inspect the existing Figma pages and reuse the existing application's:

* page layout
* header and navigation
* typography
* colors
* spacing
* cards
* buttons
* icons
* borders
* components
* design tokens

Do NOT introduce a new visual style. These pages should look like they were originally designed as part of the existing application.

## Microsoft Teams / Microsoft 365 profile photos

For every person displayed on the Contributors or Help & Support pages, retrieve their existing Microsoft 365 / Teams profile photo using Microsoft Graph.

Use the person's company email address / userPrincipalName to identify the correct Microsoft 365 account.

Use the Microsoft Graph profile photo endpoint:

GET https://graph.microsoft.com/v1.0/users/{userPrincipalName}/photo/$value

Use the appropriate authenticated Microsoft Graph credentials already available in the development environment.

Do not scrape profile photos from the Teams UI.

Do not use random or generated profile images.

If Microsoft Graph returns a profile photo, use that photo in the person's contributor/contact card.

If the person does not have a profile photo or Microsoft Graph returns 404, use the existing application's default avatar treatment or an initials-based avatar.

Do not fail the entire page because one contributor does not have a photo.

Keep profile images visually consistent:

* same dimensions
* same crop
* same border radius
* same spacing
* same styling as existing user/avatar components in the application

If the existing Figma design already has an Avatar or User component, reuse it.

## Contributors page

Create a Contributors page containing:

* Project name
* Project start date
* Short project description

Then add a section called:

### Project Contributors

For each contributor display:

* Microsoft Teams / Microsoft 365 profile photo
* Full name
* Role
* Contact information
* Short description of their contribution, when available

Example:

[Profile Photo]

Marina Nicolai
Software Developer
[company email]

Contribution:
Application development and project implementation.

Use reusable contributor cards/components so additional team members can easily be added later.

## Help & Support page

Create a Help & Support page using the same existing application design.

At the top display:

"Need help? Find the appropriate contact below."

Create contact sections for:

* General questions
* Technical/application issues
* Access or login issues
* Data/content questions
* Feature requests or feedback

For each contact display:

* Microsoft Teams / Microsoft 365 profile photo
* Name
* Role
* Contact information
* Short explanation of when that person should be contacted

Also create a clearly visible:

### Primary Project Contact

Display:

[Microsoft Teams Profile Photo]

Marina Nicolai
Software Developer
[company email]

Reuse the same contributor/contact component whenever possible.

## Important implementation rules

1. Inspect the existing Figma file before designing anything.
2. Reuse existing Figma components whenever possible.
3. Extend the existing design system — do not redesign the application.
4. Use Microsoft Graph for Microsoft 365/Teams profile photos.
5. Match people using their company email/userPrincipalName, not just their display name.
6. Use the application's existing fallback avatar if no Microsoft profile photo exists.
7. Do not expose Microsoft Graph access tokens, secrets, or credentials in Figma or in the UI.
8. Keep the new Contributors and Help pages completely consistent with the other existing pages.

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
