```
git checkout main
git pull
git worktree add ..\amp-publisher -b feature/publisher-core origin/main
git worktree add ..\amp-hook-versions -b feature/hook-versions-060 origin/main
git worktree add ..\amp-llm-review -b feature/llm-review origin/main
git worktree list
```
