

```
I ran test_bundle_hash.py: 18 passed. You mentioned 21 on an earlier run. Why the difference? Were tests removed, or did that run include other files?
```

**Next step:** run the second test file, which checks that new submissions store the 64-character hash. Run it from the `apps\api` folder:

```
cd apps\api
.\.venv\Scripts\python.exe -m pytest tests\services\test_submission_content_hash.py -q -p no:cacheprovider
```

As Claude Code warned, one test (`test_resubmit_replaces_legacy_16_char_hash_with_64_char_hash`) is **expected to fail** on this branch, because the resubmission bug fix is on the other branch. Any other failure would be worth looking at. If the tests need a database and can't connect, that's the PostgreSQL limitation we discussed, not a problem with the code.
