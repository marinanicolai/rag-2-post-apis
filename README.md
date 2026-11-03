```
Results from salt1 (read-only, BEGIN READ ONLY ... ROLLBACK):

- Query 3a: the 45d25cbf1e0a row exists ONLY in ai_marketplace_dev.
  division it, slug testnicolai, name "test" (not "mini"), version 1.0.0,
  quarantined, id 036c2008-7cba-475a-a866-fbcd2f388b02.
  Nothing in ai_marketplace (prod).
- Query 3b (ai_marketplace_dev): pinned_hooks = 1.

Conclusions: the Oct 22 audit was a dev audit, not prod. testnicolai's drift
comes from its pinned hook's output changing after approval (HOOK.md ->
hooks.json), not from a skill edit. Open question 3 is answered for dev.

Correction: 3e32471 is already pushed to origin/fix/skill-download-frontmatter.
Don't amend or force-push; put the fixes in a new commit on top.

Go ahead with items 4 and 5:
- the --schema fix in scripts/audit_plugin_renderer_hashes.py, plus the same
  schema qualification in scripts/sql/audit_plugin_skill_md_inputs.sql
- PROGRESS.md: relabel the Oct 22 audit as dev, record the 3a/3b results and the
  name correction, mark the prod audit as outstanding, and flag that the merge
  request note "expect exit code 1 until the two quarantined DRIFT rows are
  retired" came from dev and is unconfirmed for prod. Set "Last updated" to
  2026-11-03.
Leave everything uncommitted for my review.
```
