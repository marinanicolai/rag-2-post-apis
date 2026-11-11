```
Answers:
1. I'm merging !39 (docs/vitepress-theme-and-content) now. When I confirm it's merged, git fetch and base docs/developer-reference on the new origin/main (no stacked MR).
2. OK, no local build. CI is the check: build:docs and build:docs:prod run the build and the base-path guard, and I'll check diagrams on dev after deploy:dev. Before adding the Mermaid package, tell me whether apps/docs shares the root package-lock.json and whether any job uses `npm ci`. If adding a dependency without regenerating the lockfile would break those jobs, stop and propose options (e.g. I regenerate the lockfile on a machine with Node, or we use an approach that needs no new dependency).
3. No OpenAPI spec: write the API Reference as endpoint tables from the Flask blueprints (method, path, role, request/response schema). Note that the spec generator is broken as a TODO.
4. CI stages: build → validate → package → deploy. Jobs: build:web, build:web:dev, build:docs, build:docs:prod (per-env DOCS_BASE_PATH passed via docker run -e, guard fails the build if stylesheet links aren't under the base path), validate:manifest, package:backend, package:frontend, package:frontend:dev, deploy:dev (manual), deploy:prod (manual, runs alembic upgrade heads), publish:plugins (tag-gated, prod). Don't describe anything beyond this. Use TODO notes where needed.

Then continue with Step 1: the sidebar, the delete list, and the sample Feedback page. Don't write the rest yet.
```
