```
1. Before deciding: does revocation in the signed marketplace look up versions by hash? If so, confirm your recommendation still lets us revoke both old and new versions. If you can't guarantee that, use the alternative: leave hash_tree alone and only change line 628. Explain which you chose and why.
2. Go with your recommendation (match either the new bundle hash or the old sha256(content)). No backfill.
3. Branch from main. First, move the uncommitted change in apps/api/tests/fixtures/staff_data.py out of the way (stash it or commit it on its own branch) so it doesn't end up in this branch. Tell me where you put it.
4. Leave it as is, but add a short comment in the code explaining the 16- vs 64-character difference for older rows.
```
