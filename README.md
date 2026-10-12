```
On branch bug/resubmit-changes-requested in ai-marketplace, fix the admin review bug. Edit files only. Do NOT run Python or pytest (the DLP hook blocks it); I'll run tests myself and paste results.

Context (already verified):
- SubmissionStatus (libs/db/skillhub_db/models/submission.py) is: SUBMITTED, ADMIN_REVIEW, APPROVED, REJECTED, PUBLISHED, CHANGES_REQUESTED. There are no gate2_* states.
- apps/api/skillhub/services/submissions.py, review_submission() (~line 554): around line 577 it has
  reviewable_states = {"gate2_passed", "gate2_flagged"}
  so it rejects every real submission (they sit in ADMIN_REVIEW).
- review_submission is the ONLY live path to APPROVED / REJECTED / CHANGES_REQUESTED. It's called by POST /api/v1/admin/submissions/<submission_id>/review in apps/api/skillhub_flask/blueprints/submissions.py (~line 274). approve_submission and request_changes are test-only; don't touch them.

Changes:
1. services/submissions.py: replace the reviewable_states line with
   reviewable_states = {SubmissionStatus.ADMIN_REVIEW.value}
   Keep the existing current_status comparison logic. SubmissionStatus is already imported (used at ~line 722); confirm.
2. blueprints/submissions.py, review_submission_endpoint: it maps every ValueError to 404. Split it like the resubmit endpoint does: "not found" in the message -> 404, otherwise 400.
3. apps/api/tests/services/test_resubmit_changes_requested.py: the existing test test_review_submission_changes_requested_decision should now pass unchanged. Add two tests in the same style (same _submission / _db_returning helpers, patch NotificationService): decision="approved" and decision="rejected" from ADMIN_REVIEW. Assert the resulting status. Add one test that a submission in SUBMITTED raises ValueError mentioning "reviewable state". Read review_submission fully first so assertions match what it actually returns and mocks (e.g. Skill creation on approve, db.query chains). If approve needs more mocking than is reasonable, tell me instead of guessing.
4. grep apps/api/tests for "gate2_passed" or "gate2_flagged" used as a submission status (not llm_judge or analytics results) and list any tests that will now break. Don't edit them yet.

Do not change llm_judge.py, analytics, migrations, or docs. Don't commit. When done, show me the diff summary and the exact pytest command to run from apps\api:
.\.venv\Scripts\python.exe -m pytest tests\services\test_resubmit_changes_requested.py tests\test_division_enforcement.py -q -p no:cacheprovider
```
