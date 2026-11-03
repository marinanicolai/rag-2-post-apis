```
We're starting the backlog. First item: download_skill returns a Python traceback
in its 500 response body (listed under side issues in docs/script-support/PROGRESS.md).

1. git checkout main && git pull, then create branch fix/download-skill-500-traceback.
2. Investigate: find download_skill and explain how the traceback reaches the response.
   Check whether other endpoints do the same.
3. Give me a plan before changing code: the fix (log the error on the server, return a
   generic error message to the user), which endpoints it covers, and the tests.
4. Wait for my OK. Then write the failing test first, then the fix.
5. Don't commit; I'll review the diff.
```
