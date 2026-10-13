```
On branch feature/publish-data-model (from current main, which has plugins-spine, migrations 047-057, and the full SHA-256 bundle hash). Implement migration 058 and its models for Skillhub plugin script support. Scope: data model only. Do NOT build the publisher, approval rules, scanning, or LiteLLM code yet.

RULES: Edit and create files only. Don't run Python, alembic, or git commit. Never read .env files or .gitlab/ci/deploy-*.yml. Don't read docs/ or ai_docs/; only open the models, existing migrations (047-057, to copy their style), and tests you need. First check that no branch already has a 058 migration (git log --all -- "libs/db/migrations/versions/058*"); if one exists, stop and tell me.

Follow the existing conventions: SQLAlchemy models in libs/db/skillhub_db/models, status columns as String(20) with native_enum=False (like PluginStatus), idempotent migrations (IF NOT EXISTS / existence checks, as the CI rules require), and a working downgrade.

Migration 058:
1. plugin_versions, add: publish_status String(20) NOT NULL default 'not_published' (values: not_published, pending, publishing, published, failed); published_commit_sha String(40) NULL; published_tag String(255) NULL, unique when set; published_repo_at timestamptz NULL (published_at already means approval time, keep it); publish_error Text NULL; publish_attempts Integer NOT NULL default 0.
2. plugins, add active_version_id (FK to plugin_versions.id, NULL, ON DELETE SET NULL) if it doesn't already exist. If an equivalent column exists, tell me and skip.
3. New table scan_results: id, subject_type String(20) ('plugin_version' | 'skill_version' | 'hook'), subject_id uuid, content_hash String(64) (the exact content scanned), scanner String(64), scanner_version String(64), verdict String(20) ('pass' | 'warn' | 'block' | 'error'), findings JSONB (each finding has severity: 'secret' | 'serious' | 'other'), created_at. Unique on (subject_type, subject_id, content_hash, scanner, scanner_version). Index on (subject_type, subject_id).
4. New table review_events (append-only): id, actor_id (FK users, NULL for system), action String(32) (submit, scan, approve, reject, request_changes, override, publish, publish_failed, revoke, rollback), subject_type, subject_id, content_hash String(64) NULL, reason Text NULL, details JSONB NULL, created_at default now(). Add a Postgres trigger that raises on UPDATE and DELETE of review_events. Downgrade drops the trigger and table.
5. New table jobs: id, kind String(20) ('scan' | 'publish'), subject_type, subject_id, state String(20) ('pending' | 'running' | 'done' | 'failed'), attempts Integer default 0, next_attempt_at timestamptz, locked_by String(64) NULL, locked_at timestamptz NULL, last_error Text NULL, created_at, updated_at. Unique on (kind, subject_type, subject_id) so the same work can't be queued twice. Index on (state, next_attempt_at).

Models: add or extend the SQLAlchemy models to match (PluginVersion fields, Plugin.active_version, ScanResult, ReviewEvent, Job), with Python constants or enums for the allowed values. ReviewEvent gets no update helpers.

Tests (write them, don't run them): model-level unit tests that don't need a database where possible (allowed values, defaults); and a DB-backed test file (it will run in CI) that checks review_events rejects UPDATE and DELETE, and the jobs and scan_results unique constraints.

When done: list every file created or changed, anything you couldn't determine, and the pytest commands to run from apps\api (marking which need Postgres).

```
