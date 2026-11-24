```
Approved, with these changes:

1. 5-lead cap: keep it, but say it in the UI, e.g. "The model returns at most 5 notes.
   Fewer notes doesn't mean fewer problems." The model's silence must never read as a
   clean result.
2. Local "looked at" / checklist state: fine for cycle 1, but label it as saved only on
   this device and keep it out of anything that looks like the approval record or audit
   trail.
3. Diff: compare raw file source between versions, not rendered output, so renderer-only
   differences in SKILL.md don't show up as changes. If raw content isn't available for
   a file, say so on that file instead of showing a rendered diff.
4. The brief-adapter spike comes first and is read-only. If it can't cleanly expose the base
   and head files, stop and report back before building the endpoint.

Copy the Figma frames into the worktree, but don't commit them yet. Keep the review_page
flag off by default. Add the remaining Figma gaps (per-file read dots, run metadata
"ran X ago · prompt v3 · alias", server-side looked-at/checklist) to the cycle 2 list in
the plan.

Go ahead and start with the spike.
```
