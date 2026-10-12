```
git stash -u
.\.venv\Scripts\python.exe -m pytest tests\test_division_enforcement.py -q -p no:cacheprovider --tb=no
git stash pop
```
```
cd ..\..
git add -A
git commit -m "fix: admin review rejects all submissions; resubmit after changes requested

- review_submission checked stale gate2_* states; only ADMIN_REVIEW exists now
- resubmit referenced removed SubmissionStatus.GATE3_CHANGES_REQUESTED
- review endpoint returns 400 (not 404) for invalid state transitions"
git push -u origin bug/resubmit-changes-requested
```
