```
32 users in prod (ai_marketplace) and 33 in dev have division = 'unknown' stored.
Read the batch enrichment code (batch_enrichment.py and its tests) and tell me:
1. How it's run (command, arguments), and whether it can target only users whose
   division is 'unknown'.
2. What it writes, and what happens for users the staff DB doesn't find (does it
   leave 'unknown', set NULL, or overwrite with something else?).
3. Whether it's safe to run on dev first, then prod, and how to dry-run it.
Don't run anything; report only.
```
```
Yes to step 2, but first finish Task A (the leak branch) so we don't mix branches.
Then create a branch from main, feature/enrichment-unknown-check, and write the read-only
script:
- Input: the usernames with division = 'unknown' (it can run the SELECT itself, read-only,
  for a schema I pass with --schema; refuse to run without it).
- For each: StaffLookupService.lookup_user, then print the staff division name, the mapped
  slug, whether that slug exists in the divisions table, and found / not found.
- Summary at the end: counts, plus the distinct unmapped division names.
- No enrich_user, no commits, a read-only transaction. It must run on salt1 (SIGALRM).
- Give me the exact salt1 commands, like the audit (scratch clone, venv, --schema).
Hold off on step 3 (filter plus --dry-run) until we've seen the check's output.
```
