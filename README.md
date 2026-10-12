


**1. Save the bug fix** with a stash, since it isn't verified yet:

```
git stash push -u -m "resubmit fix: GATE3 -> CHANGES_REQUESTED + tests (unverified)" -- apps/api/skillhub/services/submissions.py apps/api/tests/services/test_resubmit_changes_requested.py
```

**2. Switch to the feature branch:**

```
git checkout feature/script-support-hash-and-plugin-version
```

**3. Run the hash tests** from the repo root, using the project's existing environment:

```
.\apps\api\.venv\Scripts\python.exe -m pytest libs/python-common/tests/test_bundle_hash.py -q -p no:cacheprovider
```

You should see all tests pass. Claude Code mentions 21 passed on an earlier run.

Send me the result. Later, you can remove the extra virtual environment you created at the root with `Remove-Item -Recurse .venv`, since it isn't needed.
