```
## What
- Shared compute_bundle_hash (libs/python-common/skillhub_common/bundle_hash.py): full 64-char SHA-256, order-independent, used in submissions, review queue, and skills.
- reference_files included in the hash, so it covers everything a reviewer sees. Bundles without reference files hash byte-identically to before.
- Forks copy the parent's content_hash (already the behavior in social.py after main's fork refactor).
- Seed factories use compute_bundle_hash instead of the old 16-char hash.
- Plugin tree hash (hash_tree) unchanged; revocation depends on it.
- No migration (existing columns hold 64 chars).

## Why
Step one of script support (approved ADR): the hash pins exactly what an admin reviewed.

## Testing
- test_bundle_hash, test_submission_content_hash, test_reference_files_review_carrythrough, test_resubmit_changes_requested: 45 passed.
- Fork integration tests need Postgres: CI.
- Pre-existing failures, unrelated: test_content_hash.py, test_versioning_integration.py, test_admin_approvals.py (20, all from the removed short_desc field or Flask-era API changes). Tracked in the test cleanup issue.
```
