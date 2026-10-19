```
Two Skillhub issues. Work in two phases on separate branches from an up-to-date origin/main. Show me your plan before editing each phase. I can't run Python locally (DLP hook), so CI runs the tests.

PHASE 1 — bug (branch: fix/skill-submission-missing-name-description)
Symptom: user Hameed Karzai submitted skills "context-throw" and "context-catch" through the Skillhub submit form. In the admin review queue the submission shows no name and no description, so the admin can't review it. He resubmitted (duplicates now exist). He believes a colon in the description caused server-side parsing to fail; the form's client-side validation didn't catch it. His description text contains a colon and an arrow, e.g. "...then get the exact /clear → /context-catch "checkpoint-file" command..." and a SKILL.md frontmatter description with ':' inside.
Also: the form says description is 10-200 characters but the counter shows 0/10000.

1. Trace the submission path end to end: frontend submit form (both the upload path and the "OR" manual-fields path) -> API endpoint -> how name/description are extracted (SKILL.md YAML frontmatter parse? form fields? which wins?) -> what's stored on the submission row -> what the admin review queue/detail page reads. file:line for each step.
2. Reproduce with a unit test: a SKILL.md whose description contains an unquoted colon (and quotes, arrows, backticks). Confirm whether the frontmatter parse fails or silently returns empty fields, and whether the API then stores empty name/description without erroring.
3. Fix so this can't happen again:
   - Parse frontmatter robustly (yaml.safe_load; if parsing fails, return a clear 400 with the line/field, never store empty name/description).
   - If the user typed name/description in the form, use those; don't let a failed frontmatter parse blank them.
   - When the server generates SKILL.md frontmatter, quote/escape values properly.
   - Make the server and client agree on the description length limit (check what the DB column and the server validator allow; pick one and use it in both the form hint and the counter).
   - Client: show the server's validation error message to the user instead of failing silently.
4. Tests for: colon in description, quotes/arrows/backticks, missing frontmatter, overlong description, form fields overriding frontmatter.
5. Existing bad data: give me READ-ONLY SQL (schema ai_marketplace) to list submissions with empty/NULL name or description, so I can see Hameed's and any others. Don't write any data fix; if a re-parse is possible from stored files, propose a guarded per-row UPDATE I run myself.
Commit, push, open an MR, tell me which CI job to check.

PHASE 2 — feature (branch: feature/edit-submission)
Let a submitter edit their own submission after submitting, so they don't have to create duplicates.
Rules (must fit the approval rules already on main: no self-approval, approvals counted per content hash, review_events append-only):
- Editable only while status is pending/awaiting review or changes_requested. After approval, an edit creates a new version instead (existing versioning), not an in-place change.
- Only the submitter (and admins) can edit; enforce in the API, not just the UI.
- An edit recomputes the content hash, so prior approvals no longer count and any scans must rerun; write a review_event ("edit") with actor and old/new hash.
- Admin review page shows that it was edited and when.
- Also give the submitter a way to withdraw/delete their own pending submission, so duplicates like Hameed's can be cleaned up.
First report how submissions and versions are modeled today and the smallest design that meets the rules, with file names. Wait for my OK before implementing. Then tests (submitter can edit pending, can't edit approved, non-owner gets 403, approvals reset after edit), MR.
```
