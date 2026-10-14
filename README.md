```
Decision: the live divisions table is the source of truth (rs, rbops, osec), since seed_data.py, the tests and shared-types/divisions.ts all agree with it.
On fix/division-slug-map from main:
1. Fix DIVISION_SLUG_MAP to the live slugs: every entry must exist in the 15 prod slugs. List each change (old -> new) in the commit message, and reference bf41b71.
2. Add the safety net: if the mapped slug isn't in divisions, leave division unchanged (or use 'unknown') and log a warning, so enrichment can never fail the commit again.
3. Tests: Research and Statistics -> rs; an unknown division name doesn't break login.
4. Don't touch migration 003 in this MR. Write a short note in the MR description that 003 disagrees with the live table (rb/rr vs rbops/rs, no osec), as a follow-up.
Show me the diff before committing.
```
