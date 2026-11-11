```
Go with the quicker option: merge origin/main into docs/vitepress-theme-and-content in a worktree, resolve the config.ts conflict by keeping the docs branch's version (rawBase with the trailing-slash fix and absolute-path check), and don't push.

Then show me:
1. git diff --stat origin/main...HEAD, so I can confirm it's only apps/docs/, the repo docs, README.md, and the 4 web files.
2. The final config.ts base lines.
After I review, I'll push and check that build:docs and build:docs:prod still pass.
```
