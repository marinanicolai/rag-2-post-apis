```
git diff --stat ai_docs/notes/TRACE-SUMMARY.md

```
```
git stash push -m "TRACE-SUMMARY notes" ai_docs/notes/TRACE-SUMMARY.md
git pull
git branch -D feature/publish-data-model
git switch -c feature/publish-data-model
git log --oneline -1
```
