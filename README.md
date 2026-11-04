```
Only one agent works in this repo now, so use option 2: work in the main checkout
(C:\Users\M3MXN08\repo\ai-marketplace). First, housekeeping:
1. Run git status --short and tell me if anything is uncommitted. If it is, stop and show me.
2. Delete the empty leftover folder ..\ai-marketplace-hook-card and run git worktree prune.
3. Don't touch the stash list.

Then two tasks, in this order:

Task A: unblock the leak branch (small, do it first).
fix/profile-sync-enrich-user is already merged to main (c0497ef), before
fix/download-skill-500-traceback. So:
- git switch fix/download-skill-500-traceback, git pull, git merge origin/main
  (merge, not rebase; resolve PROGRESS.md by keeping both sides).
- Update TestProfileSync500 in test_500_responses_do_not_leak.py to patch
  StaffLookupService.lookup_user (to raise) instead of enrich_user with create=True.
- Give me the pytest command for that file, which I'll run myself since the DLP hook may
  block you. After I confirm it passes, commit and I'll push.

Task B: the hook card (the task I gave you earlier).
- git switch fix/hook-card-match-skill-plugin (it's at main, c0497ef).
- Do steps 1–3 from my earlier message: investigate why the Hook detail card differs
  from Skill and Plugin, then give me the plan. No code until I OK the plan.
```
