```
Read-only investigation, no edits, no branch switching. Prepare a plan for ADR step 3, the publisher: when a plugin version is approved, a job commits the exact approved files to the skillhub-plugins repo, tags it <plugin-name>/v<version>, and records published_commit_sha / published_tag / publish_status on plugin_versions (migration 058).
Tell me:
1. Where approval completes in the code (file:line), i.e. where a publish job should be created.
2. How the jobs table (058) is meant to be used: is there any worker/runner code yet, or none?
3. How the approved files can be rebuilt exactly from the DB (the content behind content_hash), and whether that tree matches what the gate validated.
4. Is there any existing GitLab API client or git code in the repo? Which library would be simplest (python-gitlab vs plain HTTP to the GitLab commits API)?
5. Where secrets/config live (env vars, .env, settings.py), so I know where the skillhub-publisher token would go.
6. A short step-by-step implementation plan with file names, and what tests it needs (including idempotency: tag already exists on the same tree = success).
Output a plan, not code.
```
