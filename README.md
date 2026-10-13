```
On feature/approval-rules (don't touch other branches or stashes):
1. Admin skill-revision routes: POST /api/v1/admin/skills/<skill_id>/approve (skills.py:699) and /reject (:783). Check git log/blame and search all callers (frontend + backend). If unused, propose removing them. If used, route them through authorize_approval / assert_not_submitter and record_review_event, matching the other approve paths. Show me the plan before editing.
2. Add tests: (a) script plugin + one approver + scan_results with a serious/secret finding → stays awaiting / refused; (b) HTTP-level test: the submitter calls the approve endpoint → 403, for plugins, hooks, and submissions.
3. Check whether tests/blueprints/test_plugins_admin.py and test_hooks_admin.py still pass logically now that self-approval is blocked; update fixtures so approver != submitter where needed.
I can't run python locally (DLP hook blocks the venv), so don't try. Push the branch and tell me which CI job to watch.
```

