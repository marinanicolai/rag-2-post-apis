```
deactivate; cd ~ && rm -rf ~/scratch/unknown-check; unset DATABASE_URL
```
```
Check results: prod 32 users = 26 MAPPED, 6 UNMAPPED, 0 not found.
dev 33 = 27 MAPPED, 6 UNMAPPED, 0 not found. Divisions in table: 15.
Unmapped names (same on both): 'Consumer and Community Affairs' (3),
'Chief Operating Officer' (1), 'Management and Financial Services' (1),
'Supervision and Regulation' (1).

1. Give me a read-only query listing the divisions table (slug, name) so I can see
   whether these four already exist under another name.
2. Then do step 3: add --division unknown and --dry-run to the batch so it only touches
   users whose division is 'unknown', rolls back in dry-run mode, and prints what would
   change. Plan first, no code yet.
3. Separately, propose the DIVISION_SLUG_MAP additions for the four names. I'll get
   them approved before we add them, since divisions control skill access.
```
