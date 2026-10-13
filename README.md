```
Read-only investigation. Do not edit files, commit, switch branches, pop/drop stashes, or run migrations. Only report.

Context: I'm implementing the Skillhub plugin script-support plan. Steps in order:
1. Migration 058 + models: plugin_versions publish columns (publish_status, published_commit_sha, published_tag, published_repo_at, publish_error, publish_attempts), plugins.active_version_id, new scan_results, append-only review_events (DB trigger blocks UPDATE/DELETE), new jobs table.
2. Approval rules in the API: no self-approval; a version containing a script needs two different approvers, OR one approver plus a clean scan.
3. Publisher (commit approved tree to skillhub-plugins, tag, record sha).
4. Migration 059 hook_versions.
5. CI scanning of submissions.
6. LiteLLM registration behind a setting.

I believe step 2 is done. Verify that claim and tell me the latest state.

1. Repo state
   - git status, current branch, git log --oneline -15, git stash list.
   - Local and remote branches touched in the last 7 days, and which are merged into origin/main (git fetch first).
   - Latest Alembic migration on main and on the current branch. Does migration 058 exist anywhere (any branch)?

2. Step 1 (migration 058)
   - For each table/column above: present or missing, and where (file:line).
   - Is review_events append-only enforced by a DB trigger? Are migrations idempotent (IF NOT EXISTS)?

3. Step 2 (approval rules): find the code and answer each with file:line evidence
   - Is self-approval blocked in the API layer (not only the UI)? Which endpoints approve submissions, skills, hooks, and plugin versions? Is the check applied to all of them?
   - How does the code decide a version "contains a script"?
   - Two-approver rule: are approvals counted per distinct user? Can the same admin approving twice count as two?
   - "Clean scan" path: what does it read? If scan_results doesn't exist yet, what happens (fails closed = requires two approvers, fails open = allows, or errors)?
   - Is each approval recorded (review_events or the existing audit log)?

4. Tests
   - List tests covering: self-approval via API rejected; script + 1 approver + no/dirty scan stays pending; script + 1 approver + clean scan approved; script + 2 distinct approvers approved; same approver twice not counted twice; no-script + 1 approver approved.
   - Run only those tests (and the approval-related test module) and report pass/fail. Note any of the above cases that have no test.

5. Anything started on steps 3-6.

Output format:
- A short verdict: is step 2 done (yes / partly / no), and is step 1 done?
- A table: requirement | status (done / partial / missing) | evidence (file:line or test name)
- Gaps or bugs found, most important first
- Branch/merge status: what's merged to main vs only on a branch
- Recommended next step
```

