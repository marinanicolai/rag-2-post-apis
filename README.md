```
git switch --detach 0a17a51
.\.venv\Scripts\python.exe -m pytest tests\test_phase1_service.py tests\test_phase1_approval.py tests\test_submissions_blueprint.py tests\test_reference_files_review_carrythrough.py -q -p no:cacheprovider --tb=no
git switch feature/plugins-spine
```
```
On feature/plugins-spine: tests/test_reference_files_review_carrythrough.py has 2 tests failing with "Submission is not in a reviewable state: gate2_passed" because review_submission now only accepts SubmissionStatus.ADMIN_REVIEW (merged from main today). Update those tests' fixtures to put the submission in SubmissionStatus.ADMIN_REVIEW instead of "gate2_passed". Change only the test setup, not assertions or service code. Also grep apps/api/tests for any other test that sets a submission status to "gate2_passed" or "gate2_flagged" before calling review_submission and list them. Don't run Python, don't commit.
```
