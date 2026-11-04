```
[same Rules paragraph, but branch feature/publisher-core, and without the council line]

This branch was empty and is now at current main. The Oct 20 Publisher plan (merged from
docs/publisher-plan) is under docs/. Follow it unless something has changed since
(migration 059 is now on main and prod). Tell me which of its five merge requests we can
finish today, then start with the first.

Task: ADR step 3, Publisher (GitLab part). On approval, enqueue a 'publish' job (jobs
table, migration 058). A worker command commits the exact approved tree to skillhub-plugins
via the GitLab API as skillhub-publisher, creates an immutable tag, and records
published_commit_sha, published_tag, published_repo_at, publish_status, publish_attempts and
publish_error. Idempotent: an existing tag on the same tree counts as success. Retry with
backoff; never move or delete tags. Write a review_events 'publish' row. Token, repo and
signing come from settings, off unless enabled. Expose the worker as one CLI command
(cron or a scheduled pipeline can run it). Also fix publish_plugins.py so revoked versions
go into the signed revoked[] list.
```
