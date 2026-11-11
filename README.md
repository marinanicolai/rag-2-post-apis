```
!40 is merged. MR !39 (docs/vitepress-theme-and-content, "Restyle the docs site") shows 60 changed files, including backend code: feedback schemas/services/blueprints, kerberos_auth.py, app.py, tests. Those don't belong in a docs MR.

Please (read-only first, don't push):
1. Update the branch with main and list what's still different, grouped as docs vs non-docs.
2. Tell me where the non-docs changes came from (which branch/commits), e.g. feat/feedback-show-name.
3. Propose how to split it: a docs-only MR, and the backend changes in their own MR.
4. Confirm config.ts on this branch keeps base: process.env.DOCS_BASE_PATH || '...-dev/docs/'.
```
