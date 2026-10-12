I'd run them **one at a time**, each on its own branch and merge request. Smaller changes are easier to review, and if one causes a problem, it's easy to undo without touching the others. Each prompt asks Claude Code to **plan first and wait for your approval** before writing code.

Since Zach and Abyane haven't answered the open questions yet, the prompts use safe defaults: existing hashes aren't recalculated, and existing hooks get a first version automatically. If they decide differently, you adjust before approving the plan.

**Prompt 1: hash fix and `PluginVersion` additions**

```
Create a branch named feature/script-support-hash-and-plugin-version.

Context: we're adding script support to Skillhub. Every version must be identified by one full SHA-256 (64 hex characters) covering ALL files in the bundle (main content plus every reference file), so what an admin reviewed is exactly what users receive.

Tasks:
1. Create one shared function for the bundle hash (main content + all reference files, in a stable, deterministic order) and use it everywhere a content hash is computed today: submissions.py (currently truncated to 16 chars), SkillVersion, PluginVersion (plugin_service.py), and duplicates.py.
2. Change Submission.content_hash to store the full 64 characters. Do not recalculate existing rows; only new or updated rows use the new hash.
3. Add to PluginVersion: approved_commit_sha (nullable, 40 chars), release_tag (nullable), litellm_registered_at (nullable timestamp).
4. Write Alembic migration 058, following the existing style in libs/db/migrations/versions/ and CLAUDE.md (idempotent, guarded upgrade and downgrade, docstring explaining the change).
5. Add unit tests: the same files give the same hash; any change to any file changes the hash; the order of reference files doesn't change the hash.
6. Also check, without changing it: is the AuditLog trigger that blocks UPDATE/DELETE created by any migration? Report what you find.

First show me your plan and the files you'll change, and wait for my approval before writing code.
```

**Prompt 2: hook versions** (after prompt 1 is merged)

```
Create a branch named feature/script-support-hook-versions.

Context: PluginVersionHook currently points to the live Hook row, so editing a hook changes already-approved plugins. Hooks need frozen versions, like SkillVersion.

Tasks:
1. Add a HookVersion model: id (UUID), hook_id, version, hook_config (JSONB), reference_files (JSONB), content_hash (full SHA-256 using the shared bundle hash function), created_at.
2. Change PluginVersionHook to reference HookVersion instead of Hook.
3. Write migration 059 that creates the table, creates a first HookVersion for every existing hook from its current state, and repoints existing PluginVersionHook rows to those versions. Follow the existing migration style; make upgrade and downgrade safe.
4. Update the services that create or approve hooks and plugins so new approvals create a HookVersion and plugins pin it.
5. Add tests proving that editing a hook after approval does not change an approved plugin version.

First show me your plan and wait for my approval before writing code.
```

**Prompt 3: scan results** (after prompt 2)

```
Create a branch named feature/script-support-scan-results.

Context: submissions will be scanned in GitLab CI (secret detection, SAST, and custom Skillhub script-policy rules). Results must be stored per version and per tool, including the tool version, because old scans aren't equivalent to new ones.

Tasks:
1. Add a ScanResult model: id, the version it belongs to (plugin, skill, or hook version), tool_name, tool_version, level (block, justify, warn), findings (JSONB), scanned_at, pipeline_url, and an optional justification text plus justified_by for "justify" findings an admin accepts.
2. Write migration 060 following the existing style.
3. Add a service function to save results and to get the latest results for a version.
4. Add tests.

No API endpoints yet. First show me your plan and wait for my approval before writing code.
```

**Prompt 4: admin explainer page** (can run anytime, in parallel)

```
Create a branch named feature/admin-how-script-review-works.

Add a page in the admin section titled "How script review works" that explains the process in plain, non-technical language. Follow the existing admin page patterns, components, and styling, and make it accessible (headings in order, readable contrast, keyboard navigable).

Sections:
1. Why we review scripts (they run on other people's computers with their permissions)
2. What happens after a submission (files held safely, not installable; automatic checks; admin review)
3. What the automatic checks look for (secrets; launching programs, internet access, hidden code; known security problems)
4. What the results mean (secret = always blocks; serious = blocks unless the admin records a reason; everything else = warning)
5. How to review and decide (checklist: read every script, check findings and AI summary, confirm the code matches its description, never approve your own submission)
6. What approval does (exact files saved to a locked repository; users install only that exact version)
7. Updates, rollback, and revoking
8. Who to contact

Link to it from the admin review page. First show me your plan and wait for my approval before writing code.
```

Start with **prompt 1** or **prompt 4**. Prompt 4 doesn't depend on any database changes, so it's a good quick win while waiting for Zach's and Abyane's feedback on the note.
