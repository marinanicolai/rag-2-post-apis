```
Add a link to the developer docs in SkillHub's admin area. New branch feat/admin-docs-link from origin/main in this worktree. Commit locally, don't push.

1. Investigate first (read-only, short report): where the admin navigation lives in apps/web, how docsUrl.ts builds the docs URL per environment (dev .../ai-marketplace-dev/docs/, prod .../ai-marketplace/docs/), and where the existing nav docs link (Nav.tsx) is shown and to whom.
2. Then implement:
   - A "Developer docs" item in the admin navigation, visible to admin/auditor roles only (same role check the admin section already uses), opening in a new tab with an external-link icon and an accessible label ("Developer docs, opens in a new tab").
   - Use docsUrl.ts to build the URL. No hardcoded paths.
   - Optional contextual links: from the submission review page to the review docs page, and from the Model notes panel to the LLM review docs page, only if those docs pages exist.
   - If the current Nav.tsx docs link points regular users at these developer docs, tell me before changing it. Regular users should go to the user guide instead.
3. Tests: link renders for admin/auditor and not for regular users, the URL is correct for dev and prod base paths, and it's keyboard accessible.
4. Give me git diff --stat and a short summary.
```
