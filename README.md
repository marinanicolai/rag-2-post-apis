```
Ignore my lockfile message, that was meant for another session.

Design decision: notes endpoints are [division-scoped / cross-division like the admin queue]. Update the guide or the adapter to match.

Yes, apply the fixes in the order you proposed: UI mismatches, invariant and isolation tests, endpoint and adapter fixes, then judge and storage hardening. Write the failing test first for each, and leave everything uncommitted until I review.

For llm_review.py: it's blocked by DLP, so don't try to work around the block. Write out exactly what that module must provide (functions, signatures, behavior) so I can implement it or get it reviewed separately.
```
