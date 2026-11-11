```
!39 is [merged / merging now].

Mermaid: I don't have Node on my laptop. [I'll do A on SALT / a teammate will do A], via a separate chore/docs-add-mermaid MR. Until that's merged, write the diagrams as ```mermaid code blocks (option C) so nothing is blocked. Wiring the renderer is a small follow-up once the lockfile MR lands.

Step 1 answers:
- Sidebar: approved. [or: merge X into Y / drop Z]
- Delete list: approved (13 deletions, 2 rewrites, 4 folded in, plus the 11 tracked VitePress cache files).
- Sample Feedback page: approved. [or: changes, e.g. fewer code excerpts, max 2 diagrams per page, keep TODO notes]
- Favicon: yes, replace the hardcoded /docs/logo.svg with public/favicon.svg referenced via the base path.

When I confirm !39 is merged, fetch, rebase docs/developer-reference onto origin/main, and start Step 2. Commit locally, and don't push.
```
