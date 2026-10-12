


```
cd ..\..
git checkout bug/resubmit-changes-requested
git stash pop
```

Then run its test from `apps\api`:

```
cd apps\api
.\.venv\Scripts\python.exe -m pytest tests\services\test_resubmit_changes_requested.py -q -p no:cacheprovider
```

If it passes, the fix works, and we'll commit it and open a merge request for it first. Once it's merged into `main`, the failing test on the hash branch will pass too.
