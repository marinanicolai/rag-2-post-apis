```
The DLP hook is disabled now, so you can run Python again.
Continue the plan on fix/download-skill-500-traceback, scope B:
1. Run both new test files and confirm every new test fails for the right reason
   (the leak), adjusting any mock setup that fails for the wrong reason.
2. Make the five fixes: download_skill returns {"detail": ...} only and logs with
   exc_info=True; the four str(e) handlers return fixed messages and log the error.
3. Re-run the new tests plus the existing tests in those files, and ruff on the touched files.
4. Update PROGRESS.md side issues on this branch.
Don't commit. Show me the diff summary and test results.
```
