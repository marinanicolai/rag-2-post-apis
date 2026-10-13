```
Decisions:
1. Guard the routes, don't remove them. Do your plan: assert_not_submitter + record_review_event in approve_revision and reject_revision, PermissionError -> 403, a self-approval 403 test for each, and check test_rejection_workflow still holds. Don't fix create_draft_revision / short_desc in this branch; just add it to your summary as a known pre-existing bug.
2. Yes, add tests/blueprints/conftest.py with the three fixtures. Leave tests/admin/test_hook_admin.py alone.
3. Go ahead with 2a and 2b as you described.

CI: before changing .gitlab-ci.yml, find out why the test/lint/typecheck/security stages were commented out (git log -S / blame on those lines: who, when, commit message). Report that, plus what the test:api job needs to run (Postgres service, env vars, runner tag). Don't re-enable it yet; I'll decide after I see why it was disabled.

Then commit on feature/approval-rules and push. Report which CI jobs actually ran.

```

