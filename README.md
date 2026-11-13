```
New request: an endpoint, visible in our Swagger UI, that returns a list of all skills available for discovery, with the IDs of each skill, so he can test it from a Svelte app (likely MartinAI's Chat-UI).

Work on this branch (feat/openapi-swagger). Commit locally, don't push.

Step 1 (read-only, report first):
1. Is there already an endpoint that returns discoverable skills (e.g. the one the discovery/catalog page uses, like GET /api/v1/skills)? Show its path, role/auth requirements, query params, response shape, and pagination.
2. What exactly does "available for discovery" mean in our code: published and approved status, not withdrawn or archived, visibility and division rules, anything else? Point to the code that decides it.
3. Will it appear correctly in the generated OpenAPI spec (path, params, response schema with field types)? If not, what's missing?
4. Cross-app access: Robert will call it from another app. Tell me what would block that today: Kerberos auth (does Swagger "Try it out" work with the browser's session?), CORS for a different origin, and network reach from AWS EKS to fweb. Don't change auth or CORS. Just report.

Step 2 (after I approve):
- If a suitable endpoint exists: make sure it's fully documented in the spec (summary, params, response model, example) and reuses the same discovery rules as the catalog page.
- If not: add GET /api/v1/skills/discoverable (or the name you propose) that reuses the existing discovery query. No new visibility logic, and no unpublished, draft or withdrawn skills. Response:
  { "items": [ { "id", "slug", "name", "short_description", "category", "latest_version", "updated_at" } ], "total", "page", "page_size" }
  Supported params: page, page_size (with a max), q (search), category.
- Only the fields above. No submitter emails, internal notes, scan results, model notes or file contents.
- Tests: returns only discoverable skills, excludes draft/withdrawn/rejected, respects division rules if any, pagination works, appears in the OpenAPI spec with the right schema.
- Give me git diff --stat, and an example curl and response I can send Robert.
```
