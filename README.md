```
  On branch feature/script-support-hash-and-plugin-version (just rebased onto main, which now includes plugins-spine). Follow-up to commit 4ad774f: pass reference_files into compute_bundle_hash so the bundle hash covers everything a reviewer sees.

Edit files only: don't run Python, don't commit, don't touch migrations.
1. Read libs/python-common/skillhub_common/bundle_hash.py and find every caller of compute_bundle_hash (submissions.py, review_queue.py, skills.py, and any spine code that now has reference_files available).
2. Where reference_files is available at the call site (e.g. submissions carrying reference files through review), pass it in. If compute_bundle_hash doesn't accept reference_files yet, add it as an optional parameter with a deterministic, order-independent encoding (sort by path; include path and content bytes). Existing hashes for bundles WITHOUT reference files must stay byte-identical.
3. Don't change the plugin tree hash (hash_tree). Revocation depends on it.
4. Fix the stale compute_content_hash in skill_version_service.py (around line 195) and the seed factories' hash to use compute_bundle_hash, if they compute a content hash differently.
5. Add tests in libs/python-common/tests/test_bundle_hash.py: same files in different order → same hash; changing a reference file's content or path → different hash; no reference files → identical to the previous hash for the same input.
Show me the diff summary and the pytest command (from apps\api) for test_bundle_hash.py, test_submission_content_hash.py, test_reference_files_review_carrythrough.py, and test_resubmit_changes_requested.py.
```
