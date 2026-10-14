```
Confirmed root cause: the enrichment preview for m1bcm03 shows division 'Research and Statistics' -> slug 'rr' (DIVISION_SLUG_MAP in staff_lookup.py), but ai_marketplace.divisions has no 'rr'. Prod slugs: bdm,coo,dcca,fs,if,it,legal,ma,mfs,oig,osec,rbops,rs,sr,unknown. The commit then fails on users_division_fkey and every request 500s.

1. Check: is 'rs' the slug for Research and Statistics (divisions table name column, migration 003 reference data)? Check git log/blame on DIVISION_SLUG_MAP for when 'rr' appeared, and compare every slug in the map against the 15 in the table. List all mismatches.
2. On a new branch from main (fix/division-slug-map): correct the map entries to the real slugs. Also make enrich_user safe: if the mapped slug isn't in divisions, fall back to 'unknown' (or leave division unchanged) and log a warning, instead of failing the commit. Add tests for both.
3. Give me read-only SQL to count prod users by division, so I can see who else is affected.
Show me the plan before editing.
```
