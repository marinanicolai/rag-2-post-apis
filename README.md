```
Goal: replace our static API Reference with the FedQuery approach: the backend generates its OpenAPI 3 spec live from the Flask app and serves a self-hosted Swagger UI, and the docs API Reference becomes one page that links to it.

Reference implementation (FedQuery):
- Spec built at request time from Flask url_map plus the request/response models (apps/bdm-backend/app/openapi.py in the FedQuery repo)
- Swagger UI served by the backend via the flask-swagger-ui wheel, assets self-hosted under .../openapi/swagger/dist/, never from a CDN (per .claude/rules/federal-compliance.md)
- Docs page: links to Swagger UI and raw JSON, plus "Why this is a link, not a copy" and "What is actually verified" sections. No vendored openapi.json in the docs.
FedQuery live: https://fweb.rsma.frb.gov/ai/cgi-bin/fed-query-api/current/fed-query.cgi/openapi/swagger
Find the FedQuery repo locally under C:\Users\M3MXN08\repo\ or do a read-only shallow clone into a temp folder.

Step 1 (read-only, then stop and report):
1. Show how FedQuery builds the spec (openapi.py), registers the Swagger UI blueprint, and pins the dependency.
2. Map that onto SkillHub: our Flask app factory and blueprints (skillhub_flask), our schemas (Pydantic or something else?), and how roles/require_role and Kerberos auth should appear in the spec.
3. Our backend URLs: dev is https://fweb.rsma.frb.gov/ai/cgi-bin/ai-marketplace-dev/ai-marketplace.cgi and prod is .../ai-marketplace/ai-marketplace.cgi. Propose the routes (e.g. /openapi.json and /openapi/swagger).
4. Access: the spec must sit behind the same Kerberos auth as the rest of the API, not public. Confirm how.
5. Dependencies: flask-swagger-ui (or whatever FedQuery uses) must install from our Nexus pip mirror and be pinned in requirements.txt. Check whether the deploy's venv step installs from requirements.txt.
6. Cleanup list: the broken gen:openapi script and specs/openapi.json (131 bytes, contains a traceback), scripts/gen_api_reference.py, and the per-blueprint API pages under apps/docs/src/api/.
7. The docs page needs the right Swagger link per environment. Propose how (e.g. derive it from DOCS_BASE_PATH in config.ts, the same way the "Back to SkillHub" link works).

Step 2 (after I approve), on a new branch feat/openapi-swagger from origin/main:
- Implement the spec generator and the Swagger UI route, with tests: the spec builds, includes every registered route, validates as OpenAPI 3, and the UI assets are served locally.
- Replace the API Reference sidebar group with one page modeled on FedQuery's (links, "Why this is a link, not a copy", "What is actually verified").
- Remove the items from the cleanup list, updating links that pointed to them.
- No CDN URLs anywhere. No secrets or tokens printed or committed. Don't touch .claude/settings.json.
- Commit locally, don't push. Give me git diff --stat and a summary..
```
