```
Decisions:
1. ops/deploys.md: remove the /ai/www/cgi-bin/... directory layout. Describe it generically ("dev and prod are separate directories on the deploy server; see the runbook and repo rules for exact paths").
2. backend/mcp-server.md: use angle-bracket placeholders for paths, consistent with the other pages.
3. The token in .claude/settings.json: without printing its value, tell me (a) whether it's in committed history or only my local changes, (b) which commit added it, (c) what kind of token it is and what it can access, and (d) how to move it out of the repo. Don't change that file yet.

Then commit the doc fixes locally and give me git diff --stat for the branch. Don't push.
```
