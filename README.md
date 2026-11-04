```
Runner tag: arc-server. It's the runner used by deploy-dev, deploy-prod, database-ops and
test-clean-migrations, so it can reach the database. Use it for the Publisher's scheduled
job, following the pattern in .gitlab/ci/database-ops.yml (main only, scheduled).
Keep the job disabled for now. DATABASE_URL protection and the token variable name are
still waiting on Zach; use placeholders and list them in the MR description.
```
```
Answers for part 2 (Publisher):

1. Runner tag: arc-server, the runner used by deploy-dev, deploy-prod, database-ops and
   test-clean-migrations; it can reach the database. Model the scheduled job on
   .gitlab/ci/database-ops.yml (main only, scheduled). Keep the job DISABLED until the
   sandbox test.

2. Token: a skillhub-plugins project access token for skillhub-publisher (Maintainer,
   created Oct 20, expires in 11 months) with ONLY write_repository scope, so no REST API.
   Change the GitLab client to plain git over HTTPS: fetch, commit the exact approved tree,
   create the tag, push. Use git ls-remote to check whether a tag exists and which commit it
   points to. Keep the read-back check before tagging and the "never move or delete a tag"
   guard. Tag format: <plugin-name>/v<version>.

3. CI variables: token in SKILLHUB_PUBLISHER_TOKEN (Protected, Masked). DATABASE_URL is
   Masked; I'm confirming it's Protected. Never print the token, a URL containing it, or
   DATABASE_URL in output, logs or errors.

4. Scrubbing: remove known secret VALUES (the token from settings) from error text; don't
   match token-shaped patterns. Tests use a harmless sentinel like "test-sentinel-value-123".
   No token-shaped literals, no string-splitting, nothing that gets around the DLP filter.
   If something is blocked, stop and tell me.

5. Revoked list: don't select QUARANTINED until you've shown me where revocation is set
   and which status means "revoked". Quarantine on dev meant drift, not revocation, and
   anything in the signed revoked list gets uninstalled from users.

6. Slug collisions: refuse to publish with a clear error. Optional settings argument on
   approve: OK.

7. Status: prod 059 was applied and verified on Nov 3. 060 still needs the dev apply and
   a prod pre-apply before the Publisher runs anywhere.

8. PROGRESS.md is local-only now: keep updating it, but never git add it.

Continue test-first, run requesting-code-review, give me the test commands, then I commit
part 2 by file name.
```
