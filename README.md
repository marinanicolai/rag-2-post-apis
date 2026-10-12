```
I'm on feature/plugins-spine, mid-merge of origin/main. There is one conflict: apps/api/skillhub/services/submissions.py. Resolve it. Edit files only: do NOT run Python/pytest, do NOT commit, do NOT run git merge --abort.

What each side brings:
- main (theirs) brings today's fix: in review_submission, reviewable_states = {SubmissionStatus.ADMIN_REVIEW.value} (replacing the stale {"gate2_passed", "gate2_flagged"}), and resubmit_submission uses SubmissionStatus.CHANGES_REQUESTED instead of the removed GATE3_CHANGES_REQUESTED.
- spine (ours) brings the plugin implementation (plugin-related changes in submissions.py).

Rules:
1. Keep ALL of spine's plugin logic AND main's two fixes. Neither side's changes should be lost.
2. If spine still contains "gate2_passed"/"gate2_flagged" as reviewable states or references GATE3_CHANGES_REQUESTED anywhere, it's stale. Use main's version.
3. Check the SubmissionStatus enum on this branch (libs/db/skillhub_db/models/submission.py) and confirm it still has ADMIN_REVIEW and CHANGES_REQUESTED.
4. Make sure no conflict markers (<<<<<<<, =======, >>>>>>>) remain anywhere in the repo.
5. Also check that apps/api/skillhub_flask/blueprints/submissions.py (auto-merged) still has the 404/400 split in review_submission_endpoint and didn't lose any plugin routes.

When done, show me each conflict hunk: what was on each side and what you kept, and why. Then give me the pytest command to run from apps\api for test_resubmit_changes_requested.py plus any plugin test files that touch submissions.
```
