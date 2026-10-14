```
Answers:
1. Branch from origin/main after git fetch.
2. Fallback: leave division unchanged and log a warning (don't write 'unknown', so we never overwrite a correct value).
3. Don't guess the osec spelling. First give me a read-only query that lists the distinct division names in boardstaff and bankstaff (the same source enrichment reads), with counts. I'll run it and send you the output, and then map every name to a slug that exists in the 15 live slugs (bdm,coo,dcca,fs,if,it,legal,ma,mfs,oig,osec,rbops,rs,sr,unknown).
Also: the live divisions table is the source of truth (rs, rbops, osec). Fix the map to those, reference bf41b71 in the commit message, add tests (Research and Statistics -> rs; an unmapped name doesn't break login), and note the migration 003 drift (rb/rr vs rbops/rs, no osec) in the MR description as a follow-up. Show me the diff before committing.
```
