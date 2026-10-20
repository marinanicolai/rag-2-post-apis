```
Read docs/script-support/PROGRESS.md first. Task: plan Step 3, the publisher. Read-only, no code changes.

Goal (from the ADR amendment): when a submission becomes approved, publish it to the skillhub-plugins repo as a commit plus a tag, and record published_commit_sha, published_tag and publish_status on the record.

Report:

What exists today: where approval happens (the function where status becomes approved/published), what migration 058 added (columns for published_commit_sha / published_tag / publish_status?), and any existing code that writes to skillhub-plugins or builds the plugin/skill bundle (e.g. with_name_description_fallback, hash_tree).
The repo layout in skillhub-plugins: folder structure for skills, plugins and hooks, how marketplace.json (or equivalent) lists them, and naming and tag conventions already in use.
Proposed design:
Trigger: synchronous on approve, or a background job/queue? Which fits the CGI/Apache setup?
How it authenticates to GitLab (deploy token, project access token, CI job?). Name the secret, never its value.
The tag format (e.g. <type>/<name>/v<revision>) and the commit message.
publish_status states (pending → published / failed) and retries.
Idempotency: approving twice or retrying must not create duplicate commits or tags.
What’s committed is exactly the installed bytes (same hash as the approval hash).
What happens on edits after publish (a new version, a new tag).
Risks and open questions for me, 
A small, ordered implementation plan (branches/MRs) with tests for each step.

No pushes, no writes to skillhub-plugins, no prod access.
```
