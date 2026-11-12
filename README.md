```
Decisions:
- Notes endpoints are [division-scoped / cross-division like the admin queue]. Update the guide or adapter to match, with a test.
- Breaker question: [your answer, or "use your assumption and note it in the PR description"].

Then, on feature/llm-review-build:
1. Commit using your suggested split: Stage 2b, Stage 4 (incl. migration 062), Stage 5, Stage 6 groundwork, Stage 7. Clear commit messages, nothing unrelated, no secrets, don't touch .claude/settings.json.
2. Run whatever checks you can locally (ruff, mypy, unit tests). List which ones can't run here (web tests, BDD, Postgres-only), since CI will cover those.
3. Draft a PR description: what it solves, what it doesn't yet (llm_review.py, worker, CLI, enqueue endpoint, blocked by DLP), that the feature is off by default, that it adds migration 062, and the test status.
Don't push. I'll push and open the MR.
```
