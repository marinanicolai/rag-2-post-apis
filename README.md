```
Read-only investigation in ai-marketplace (main now has plugins-spine and the full SHA-256 bundle hash). Don't edit files, run Python, or commit. Never read .env files or .gitlab/ci/deploy-*.yml.

Goal: prepare the "publish approved plugin to the skillhub-plugins GitLab repo" feature. Flow (approved ADR): admin approves a plugin version → a service account commits the approved files to a protected GitLab repo and tags them → the commit sha is recorded on the version (LiteLLM registration comes later, behind a disabled setting).

Answer, with file paths and line numbers:
1. Approval hook point: where a plugin version (and a hook version, if separate) moves to published/approved. What runs in that transaction today (audit log, notifications, status changes)? Is there one place to hook publishing, or several?
2. What exactly is "the approved bundle" in the data model: which tables/columns hold the files, reference files, and hashes (content_hash, hash_tree, bundle hash) for a plugin version and its pinned skills/hooks? What would need to be written to the repo for a version to be reproducible?
3. Existing outbound integrations: any existing HTTP client code, GitLab API usage, or service-account settings pattern (how secrets get into config). Any retry or idempotency helpers?
4. Background work: confirm whether any job/queue system exists (threads, celery, scheduled tasks). The create-submission endpoint starts a thread for gate 2. Is that the only pattern?
5. Current PluginVersion, plugin, and hook columns related to publishing or scanning (status values, quarantine, scan fields). Compare against the design note: extend PluginVersion, add HookVersion and ScanResult, one 64-char bundle hash.
6. Revocation today: what code relies on hash_tree, and what "revoked" means in the schema.

Then propose (don't implement): the minimal migration 058 columns and tables needed for publishing (e.g. published_commit_sha, published_tag, publish_status, publish_error, published_at, and a ScanResult table), and whether publishing should run synchronously in the approve request or via a small job table, with tradeoffs. Keep the report under about 2 pages.
```
