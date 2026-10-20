```
’m mid-merge on feature/approval-rules (git merge origin/main). There’s one conflict, in apps/api/skillhub/services/submissions.py. Everything else auto-merged. Don’t resolve yet. For each conflict block, show me:

what main’s side does (the Hameed fix: frontmatter parsing/validation, the 1024 limit)
what the approval-rules side does (no self-approval, two approvers or one approver plus a clean scan for scripts, per-content-hash approvals, withdrawals)
your proposed resolution. Both behaviors must be kept, and neither side should simply win.

Also check the auto-merged files (review_queue.py, blueprints/submissions.py, blueprints/skills.py, plugin_service.py, AdminQueueView.tsx) for anything that merged cleanly but is logically wrong, e.g. a function called with a changed signature, or the “As installed” panel and the approval UI both editing the same part of AdminQueueView. Then run the approval, withdrawal and submission tests. Don’t commit until I say so.
```
