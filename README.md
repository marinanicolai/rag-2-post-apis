```
Create branch docs/progress-tracker from an up-to-date main (git checkout main, git pull, git checkout -b docs/progress-tracker). Create docs/script-support/PROGRESS.md as the working log for Skillhub script support, with these sections: Where we stopped, Build order, Team tasks, Branches in flight, Decisions, Side issues, Open questions. Fill it from the repo, the ADR amendment build order and what you know from this session (approval rules merged Oct 14, deploy and admin test pending; Hameed display bug under investigation, DB rows complete; Phase 2 edit/withdraw on hold).

Build order: 1 Migration 058 (done) · 2 Approval rules (merged, rollout pending) · 3 Publisher (commit and tag in skillhub-plugins, record published_commit_sha/tag/publish_status) · 4 Migration 059 hook versions · 5 CI scanning of every submission · 6 LLM review via LiteLLM, scanner and judge, advisory only · 7 LiteLLM registration.

Team tasks (meeting notes plus Missy’s additions), each mapped to a step:

Email notifications: email admins when a skill, plugin or hook is submitted for review. New item, after step 2.
Admin approval guide: an admin page on how to approve, what to check and how to read scan results. New item, after steps 5–6.
Automated scanning before approval in GitLab CI → step 5.
LLM judge: LiteLLM summarizes each submission and flags risks for the admin → step 6.
(Missy) Badges when automated scans pass → step 5 plus UI.
(Missy) UI that explains the badges and reminds users to check alignment with local and jurisdictional policy → steps 5–6, UI.
(Missy) Scan flag for “deep SME expertise needed”, so niche submissions get a human expert’s review → step 6, as a judge output field.

Decisions: deploy only from main pipelines; never run deploy:prod:fresh-install; prod psql is read-only, and writes go through BEGIN/ROLLBACK first; the LLM review never counts as a clean scan or approves anything; description limit 1024; no js-yaml on the client; CI baseline 1,243 passed / 690 failed / 185 errors / 35 skipped.

In CLAUDE.md, add an “Ongoing work” section: “Before starting any task, read docs/script-support/PROGRESS.md. At the end of any task that changes integration status, a branch, or a decision, update it in the same branch.” Show me the diff before committing, then commit both files and push with git push -u origin HEAD. Don’t touch any other files.
```
```
Root cause narrowed to the frontend. Prod GET /api/v1/admin/queue?page=1&per_page=100 returns Hameed’s items complete, e.g. SKL-39MQ14: name="context-catch", description="Resume work from the exact /context-throw checkpoint file…", content="# context-catch\n\nTurn a checkpoint…" (no frontmatter), author_name, status="pending", skill_fields={category:“engineering”, reference_files:[], …}. Clicking an item fires no new request, so the detail panel renders from this list item. The queue LIST shows name and description fine, so the DETAIL panel reads them from somewhere else. Read-only: find the admin queue detail component and list every field it reads for the title and description. Check whether it uses skill_fields.*, or parses frontmatter from content, instead of item.name and item.description. Report the exact file and line. Then propose the smallest fix: the detail panel uses item.name and item.description first and falls back to the other source only if those are empty. Put it on the current fix branch with a test using an item shaped like this one.
```
