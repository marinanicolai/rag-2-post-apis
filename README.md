```
On branch feature/approval-rules (from current main: plugins-spine, bundle hash, and migration 058 with scan_results, review_events, jobs, and publish fields on plugin_versions). Implement the approval rules from the approved ADR amendment. Scope: rules and audit events only. Do NOT build the publisher, job runner, scanning, or LiteLLM code, and don't add a migration (tell me if you think one is needed).

RULES: Edit and create files only. Don't run Python or git commit. Never read .env or .gitlab/ci/deploy-*.yml. Don't read docs/ or ai_docs/. Only open the files you need.

Approval paths (from the investigation):
- Plugins: approve_plugin_version in apps/api/skillhub_flask/services/plugin_service.py (~1548), called by POST /api/v1/plugins/<slug>/versions/<version>/approve (blueprints/plugins.py ~629). Also its reject / request-changes counterparts.
- Hooks: approve_hook_endpoint (blueprints/hooks.py ~430) → services/admin.py ~490.
- Skills: review_submission in apps/api/skillhub/services/submissions.py (reviewable state ADMIN_REVIEW).

Implement, enforced in the service layer (not just the UI):
1. No self-approval: the reviewer cannot be the submitter/author of what they approve (plugin version author or submitter, hook author, submission submitted_by). Raise a PermissionError mapped to 403 by the existing endpoint pattern. Apply to approve; reject and request-changes by the submitter are also blocked.
2. Scripts need extra approval: add a helper version_contains_scripts(plugin_version) that returns True if the materialized plugin tree (materialize_plugin_version / build_plugin_spec) or any pinned skill's reference_files contains a .py file. For such versions, approval requires EITHER two approvals from two distinct admins (neither the submitter) for the same content_hash, OR one approval plus a clean scan (a scan_results row for that subject and content_hash with verdict 'pass' and no 'secret' or 'serious' findings). If the requirement isn't met yet, the first approval is recorded but the version stays PENDING; return a clear status like "awaiting_second_approval". Versions without scripts keep today's single-approval behavior.
3. Scan gates (data may be empty today; code must handle that): if any scan_results row for the subject and content_hash has a 'secret' finding, approval is refused. If it has 'serious' findings, approval requires a non-empty override reason parameter; record an 'override' review event with that reason. No scan rows at all = no gate (and for script versions, falls back to the two-approver rule).
4. Audit: write a review_events row for every approve, reject, request_changes and override on plugin versions, hooks and skill submissions (actor, action, subject_type, subject_id, content_hash where available, reason). Use the ReviewEvent model; never update or delete rows. Write it inside the same transaction as the status change.
5. Count prior approvals for rule 2 from review_events (action 'approve', same subject and content_hash, distinct actors, excluding the submitter). A new content_hash (resubmission) starts the count over.

Tests (write, don't run): unit tests in the style of apps/api/tests/services/test_resubmit_changes_requested.py (mocks, no Postgres): self-approval blocked (plugin, hook, skill); no-script plugin approves with one admin; script plugin: first approval → awaiting_second_approval, second distinct admin → published; same admin twice → still awaiting; one approval + clean scan → published; secret finding → refused; serious finding without reason → refused, with reason → approved plus override event; review_events written for each decision; new content_hash resets the count.

When done: list files changed, any behavior you couldn't determine, and the pytest commands to run from apps\api (marking any that need Postgres).

```

