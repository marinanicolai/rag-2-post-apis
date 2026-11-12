```
Goal: make the ```mermaid blocks in our docs render as diagrams, by copying how the FedQuery docs do it (https://fweb.rsma.frb.gov/ai/cgi-bin/fed-query/docs/, where Mermaid diagrams already render).

Step 1, investigate (read-only, then stop and report):
1. Find the FedQuery repo. Check if it's cloned locally (search under C:\Users\M3MXN08\repo\). If not, it's on gitlab.frb.gov under ai-program, probably near our ai-marketplace project. Do a read-only shallow clone into a temp folder outside our repo.
2. In FedQuery's docs, find and show me:
   - the Mermaid-related packages and exact versions in its docs package.json (e.g. mermaid, vitepress-plugin-mermaid)
   - its VitePress version, compared with ours (vitepress 2.0.0-alpha.17)
   - how config.ts/config.mts wires Mermaid (withMermaid wrapper, markdown config, or a custom theme component)
   - any theme/CSS overrides for diagrams (dark mode, sizing)
3. Tell me whether that setup will work with our VitePress version, or what has to change.

Step 2, after I approve: on a new branch chore/docs-add-mermaid from origin/main:
- Add the same packages and versions to apps/docs/package.json, and wire Mermaid into apps/docs/src/.vitepress/config.ts the way FedQuery does. Keep the base path logic (process.env.DOCS_BASE_PATH), ignoreDeadLinks array and favicon unchanged.
- I have no Node locally, so you can't update package-lock.json, and the jobs that run `npm ci` would fail with an out-of-sync lockfile. To solve that, add a TEMPORARY manual CI job (when: manual, stage build, same docker_build runner and node:22 image and Nexus .npmrc setup as .build-docs) named lockfile:regen that runs `npm install` at the repo root and saves package-lock.json as an artifact. I'll run it, download the artifact, and you'll commit the new lockfile and remove the temporary job in the same branch.
- Don't print or commit any tokens or .npmrc auth.
- Commit locally, don't push. Then give me git diff --stat and exact steps for running the job and handing you the artifact.
```
