```
I'm mid-rebase of feature/script-support-hash-and-plugin-version onto origin/main in ai-marketplace. Commit f52d5c5 ("Use shared full SHA-256 bundle hash for skills and submissions") conflicts in apps/api/skillhub_flask/blueprints/skills.py. submissions.py auto-merged.

Resolve the conflict in skills.py. Edit files only: don't run Python, don't run git rebase --continue/--abort/--skip, don't commit.

What each side brings:
- origin/main (HEAD during rebase): plugins-spine (plugin routes/logic) plus other main changes.
- f52d5c5 (being applied): replaces the old content hash with compute_bundle_hash from libs/python-common/skillhub_common/bundle_hash.py (full 64-char SHA-256); forks copy the parent's content_hash.

Rules:
1. Keep ALL of main's changes (plugin-related code, any new routes) AND f52d5c5's switch to compute_bundle_hash.
2. Do NOT change the plugin tree hash (hash_tree for plugin versions). Revocation depends on it staying as-is.
3. Check that the auto-merged submissions.py still uses compute_bundle_hash where f52d5c5 intended and still has main's reviewable_states = {SubmissionStatus.ADMIN_REVIEW.value}.
4. No conflict markers left anywhere.
Show me each conflict hunk: both sides and what you kept. Then give me the pytest command (from apps\api) for test_bundle_hash.py, test_submission_content_hash.py, and test_resubmit_changes_requested.py.
```
