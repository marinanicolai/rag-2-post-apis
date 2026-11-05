```
Before fixing anything, give me a status table for the whole ADR implementation, measured
against docs/script-support/IMPLEMENTATION-GUIDE.md. One row per part (060, Publisher,
revoked list, CI job, LLM review, LiteLLM registration, CI scanning). Columns:
- Status: done / in progress / not started / blocked
- Committed? (commit hash, or "uncommitted")
- Proof: which tests exist, and whether they ACTUALLY RAN and passed (say "not run" if
  they need Postgres or were blocked)
- What's left, in one line
- Blocked on (person or decision)
- How I can see it working myself on dev, in plain steps (a page to open, a query to run,
  or a repo/tag to look at)
Plain language. Don't count anything as done unless it's committed and its tests ran.
```
