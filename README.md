```
Goal: replace the current SkillHub docs (apps/docs/) with developer/technical documentation, modeled on our FedQuery docs (https://fweb.rsma.frb.gov/ai/cgi-bin/fed-query/docs/). The current pages are an end-user guide, and we already have a separate user guide, so those pages should come out of the docs site.

Work on a new branch from origin/main named docs/developer-reference. Don't push. I'll review and push myself.

## Target structure (adapt to SkillHub, based on what's actually in the code)
Sidebar groups, like FedQuery:
- Overview: Introduction (what SkillHub is, architecture at a glance), Getting Started (local setup, env vars by name only), Dev Tooling (tests, lint, Claude Code setup, scripts)
- Frontend: apps/web (React): structure, routing, state, API client, docs link (docsUrl.ts)
- Backend: skillhub_flask: app factory, blueprints, services, schemas, libs/db and libs/python-common
- Features: one page per real feature you find in the code, e.g. Skills catalog & discovery, Submissions & review, Plugins & script distribution, Publish plugins (signed seed-dir), Feedback (incl. show_name), Notifications, Auth (Kerberos / RBAC require_role), Divisions & staff batch sync, Audit log
- Data: schema overview, Alembic migrations and how they're applied (link to the runbook, don't copy it)
- Ops & Deploy: CI pipeline stages, dev vs prod deploys, docs build per environment (DOCS_BASE_PATH, the base-path guard), logs
- API Reference: endpoints grouped by blueprint (method, path, required role, request/response schema). If there is an OpenAPI spec in the repo, use it
- Reference: glossary, links to the user guide and runbooks

## Page pattern for every feature page (like FedQuery's Retrieval page)
1. One-paragraph summary: what it does and who uses it
2. "Where it sits": a Mermaid diagram showing the flow (e.g. React page → API route → service → DB/table → response), with labeled edges
3. "The code": walk through the real path, citing file paths and function names (e.g. apps/api/skillhub_flask/blueprints/feedback.py → feature_skill()), with short code excerpts
4. Data touched: tables/columns, migrations that created them
5. Permissions: roles required
6. Gotchas / known limits, only if visible in code or comments

## Rules
- Ground everything in the repo. Don't invent features, endpoints, or behavior. If something is unclear, write a "TODO: confirm" note instead of guessing.
- Never include secrets, .env values, tokens, or credentials. Env vars by name only.
- Keep the restyled theme, config.ts base-path handling (process.env.DOCS_BASE_PATH with the guard) and the CI files unchanged.
- Mermaid: add Mermaid support to VitePress (e.g. vitepress-plugin-mermaid). It must install through our Nexus npm registry and render without internet access. If FedQuery's docs config is available locally, copy its approach. Tell me which package and version you chose.
- Remove the user-guide pages (Getting Started for users, Skill Discovery, Social Features, FAQ, Admin Guide, etc.) from the sidebar and delete them. List what you deleted so I can confirm.
- Internal links must work under the base path (use relative links, no hardcoded /docs/...). Also fix the head icon link that hardcodes /docs/logo.svg.

## Step 1 (do this first, then stop)
Show me:
1. The proposed sidebar (groups and page titles) based on what you found in the code
2. The list of current pages you'll delete
3. Which Mermaid package you'll add and how
4. One fully written sample feature page (pick Feedback), so I can approve the style

## Step 2 (after I approve)
Write all pages, update the sidebar in config.ts, then:
- run the docs build with DOCS_BASE_PATH=/ai/cgi-bin/ai-marketplace-dev/docs/ and confirm the base-path guard would pass (stylesheet links under that path)
- check that every Mermaid diagram renders in the built output
- give me git diff --stat and a short summary
```
