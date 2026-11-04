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
