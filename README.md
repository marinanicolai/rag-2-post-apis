```
git fetch
git branch -a | Select-String publisher
git log --oneline main..origin/feature/publisher-core
```
```
  git worktree add ..\amp-publisher feature/publisher-core
```
```
