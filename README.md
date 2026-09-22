# 📦 Supply Chain RAG Explorer (React Frontend)

---
Please EDIT the existing **Contributors** and **Help & Support** frames in the current Figma file. Do not create new pages.

Use the existing application design and components as the source of truth. Do not redesign these pages.

## 1. Remove the unwanted chat UI

There is an incorrect/strange chat or conversational UI that was added to these pages.

Remove any:

* chat box
* message input
* conversation panel
* prompt field
* chat-specific component

that was added specifically to the Contributors or Help & Support page.

IMPORTANT: Do NOT remove the application's normal shared header/navigation if that header already exists on the other application pages.

The pages should use the same application shell/header/navigation as the rest of the existing Figma application.

---

# 2. Fix the Contributors page

Keep the existing **Project Contributors** structure and the existing contributor information.

Do not replace the existing layout with a new design.

The current initials such as:

YT
SO
MN
FH
CH

are placeholders and need to be replaced with the people's REAL Microsoft 365 / Teams profile photos.

## Retrieve the actual profile photos

Use Microsoft Graph and each person's company email/userPrincipalName.

Use:

GET https://graph.microsoft.com/v1.0/users/{userPrincipalName}/photo/$value

For every contributor:

1. Identify the contributor's existing company email address from the contributor information.
2. Query Microsoft Graph using that email/userPrincipalName.
3. Download the actual profile photo returned by Microsoft Graph.
4. Import that image into Figma.
5. Replace the initials avatar with the actual photo.
6. Crop the image correctly inside the same circular avatar shape.
7. Keep the same avatar size, spacing, alignment, and styling currently used on the page.

Do NOT generate AI photos.

Do NOT use photos found through a web search.

Do NOT replace the person's real Microsoft profile image with initials if Microsoft Graph access is available.

If the Graph request fails because authentication or permissions are missing, STOP and tell me exactly what permission/authentication is missing rather than silently replacing all photos with initials.

If Graph successfully connects but a specific person genuinely has no profile image, only then keep the initials fallback for that specific person.

Do this for ALL contributors currently listed on the Contributors page.

---

# 3. Fix the Help & Support page

Flora should be the ONLY support contact.

Remove all other people currently shown as contacts on this page.

Do NOT show:

* Marina as Primary Project Contact
* Yaseen for technical issues
* Steven for access/login
* Christopher for data/content
* Marina for feature requests
* any other team member as a support contact

Instead, use **Flora Haberkorn as the single contact for ALL project support and questions**.

Create one clear contact section using the same existing application design.

Suggested content:

### Need help?

For questions, technical issues, access problems, data/content questions, feature requests, feedback, or any other project-related issue, please contact:

**Flora Haberkorn**
[Flora's existing project role]
[Flora's company email]

Use Flora's REAL Microsoft 365 / Teams profile photo.

Retrieve it through Microsoft Graph using Flora's company email/userPrincipalName and:

GET https://graph.microsoft.com/v1.0/users/{userPrincipalName}/photo/$value

Import the actual image into Figma and display it in the existing avatar style.

Do not show Flora multiple times in separate cards.

There should be ONE clear primary support/contact card for Flora.

You may list underneath the card that Flora can be contacted for:

* General questions
* Technical/application issues
* Access or login issues
* Data/content questions
* Feature requests
* Feedback
* Other project-related issues

But Flora should remain the only named contact.

---

# 4. Preserve the existing design

Do not redesign either screen.

Reuse the same:

* application shell
* top navigation
* typography
* colors
* spacing
* card styling
* borders
* avatar styling
* content width
* section headings
* components
* design tokens

that are already being used on the other application pages.

These two screens should look like native parts of the existing application.

## Final check before finishing

Before you finish, verify:

* Contributors page still contains all current contributors.
* Every available Microsoft profile photo has actually been imported into Figma.
* Initials are only used when a specific Microsoft account genuinely has no profile photo.
* No added chat/message UI remains.
* Help & Support contains only Flora as the contact person.
* Flora appears only once as the main support contact.
* Existing application navigation/header is preserved.
* No unnecessary new components or visual styles were introduced.


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
