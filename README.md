

```
Read /tmp/investigate_output.txt — that's the full output of /tmp/investigate_duplicates.sql run against ai_marketplace_dev.

Answers to your questions:
- Kept row: for each group, keep the published row with the un-suffixed slug. If none is un-suffixed, keep the published one with the most installs, then the oldest created_at. Drafts with a random suffix are never kept.
- Hooks: every "offers-a-one-time-onboarding-tour..." row gets removed (all my test submissions, 0 installs). Don't keep any of them.
- If two PUBLISHED rows in a group have different content (e.g. privacy-engineer vs privacy-engineer-2), don't touch them — list them for me.
- Reviews unique constraint: skip-and-flag as you suggested, don't blind re-point.

Now write /tmp/cleanup_duplicates.sql: SET search_path TO ai_marketplace_dev; preview SELECT first, then UPDATEs (status = 'removed' + re-pointing) inside BEGIN ... ROLLBACK.

```

```
psql "$DEV_DATABASE_URL" -c "SET search_path TO ai_marketplace_dev;" -f /tmp/investigate_duplicates.sql > /tmp/investigate_output.txt 2>&1
```
