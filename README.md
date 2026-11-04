```
git worktree remove ..\amp-publisher
git worktree remove ..\amp-hook-versions
git worktree remove ..\amp-llm-review
git branch -D feature/publisher-core feature/hook-versions-060 feature/llm-review
git worktree list
```
```
git status --short
```
```
git switch feature/adr-script-support
git merge --ff-only origin/main
git log --oneline -1
```
```
We're implementing the rest of the ADR "Skillhub Plugin Script Support" on ONE branch,
feature/adr-script-support, as ONE merge request. Read CLAUDE.md,
docs/script-support/PROGRESS.md and the Oct 20 Publisher plan under docs/ first.
Rules: what an admin reviewed must be exactly what users get. Migrations are idempotent.
skillhub-plugins holds only APPROVED versions (as in the ADR). The DLP hook may block
Python: give me test commands to run. Use writing-plans, test-driven-development and
executing-plans; run requesting-code-review before each commit; use council on the 060
and LLM review plans. Don't switch branches.

Work in this order. Plan each part, wait for my OK, build it, then I commit before the next:
1. Migration 060, hook_versions: plugin_version_hooks points at a frozen hook version;
   backfill existing hooks as v1 and repoint pins; editing a hook creates a new version.
   (Real case: testnicolai 1.0.0 on dev drifted because its pinned live hook changed after
   approval.) Say whether 060 must be pre-applied, since the prod deploy runs alembic after
   unpacking the code.
2. Publisher (GitLab part): on approval, enqueue a publish job; the worker commits the
   approved tree to skillhub-plugins as skillhub-publisher, creates an immutable tag, and
   records the publish columns from 058. Idempotent; retries; review_events row. Settings,
   off by default; one CLI command for the worker. Fix publish_plugins.py's empty revoked[].
3. LLM review via LiteLLM (scanner + judge): scan_results rows with scanner='llm-review';
   judge summary on the admin review page (use the 508 skill). Advisory only; untrusted
   submission text kept separate from instructions; setting off by default; mocked tests.
4. LiteLLM registration of approved versions, behind its own setting, off by default.
Start with the plan for part 1. Also tell me which parts are realistic today.
```
