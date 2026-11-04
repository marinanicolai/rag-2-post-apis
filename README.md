```
Rules: you're in a dedicated git worktree on feature/hook-versions-060. Never touch
other folders or switch branches. Read CLAUDE.md and docs/script-support/PROGRESS.md
first. What an admin reviewed must be exactly what users get. Migrations are idempotent
(IF NOT EXISTS). The DLP hook may block Python: give me the commands and I'll run them.
Use writing-plans for the plan, run it past council and include its objections, then wait
for my OK. Build with test-driven-development and executing-plans. Run
requesting-code-review on your diff before telling me it's ready. Don't commit.

Task: ADR step 4, migration 060: hook_versions (hook_id, version, hook_config,
reference_files, full SHA-256 content_hash). plugin_version_hooks points at
hook_version_id instead of the live hook. Backfill existing hooks as version 1 and repoint
existing pins. Editing a hook creates a new version; approved plugin versions keep their
pinned version. Real case: on dev, testnicolai 1.0.0 drifted because its pinned live hook
changed format after approval (HOOK.md to hooks.json). Make that impossible. Keep the
renderer and the audit script working. The prod deploy job runs alembic AFTER unpacking
code, so say whether 060 must be pre-applied.
```
