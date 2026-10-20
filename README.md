```
> Yes, apply the resolution in a scratch copy first. Check that submissions.py compiles (`python -m py_compile`) and that pytest can **collect** the four test files without import errors. Then show me the final resolved conflict block(s) as a diff. If that looks right, apply the exact same resolution to the real merge, confirm `git diff --check` shows no leftover conflict markers, and `git status` shows the conflict resolved. Don't commit yet. Also update PROGRESS.md on this branch: step 2 = "merged main into feature/approval-rules; conflict in services/submissions.py resolved keeping both the Hameed fix and approval rules; awaiting CI".
```

**Then you run the mock-based tests yourself.** In the CLI, the `!` prefix runs the command as you:
```
! apps/api/.venv/Scripts/python.exe -m pytest apps/api/tests/blueprints/test_self_approval_http.py apps/api/tests/test_submissions_blueprint.py -q
```
The other two files (`test_approval_rules.py`, `test_withdrawals.py`) will probably fail to connect without Postgres. That's expected, and CI covers them.

**I haven't seen the resolution itself yet.** It's above this part of the CLI's output. Scroll up and send me a photo of the conflict block and the CLI's proposal before you let it commit. I'm checking that the self-approval check and the new frontmatter validation both stay in the submit/approve flow.

After that: commit → `git push` → MR `feature/approval-rules` → main → pipeline → merge → deploy.
