```
Before I push, check the hash impact (read-only):

Does hash_tree (or any content_hash) for an existing plugin_version get recomputed anywhere (verification, revocation check, publish, the marketplace index), or is the stored value always used?
For the one plugin in prod and the dev plugins, would the new renderer produce different installed bytes than before? If yes, would any stored hash, approval or revocation entry stop matching?
If there’s an impact, propose the smallest safe option (e.g. only new versions use the new renderer; existing versions keep their stored hash and bytes) and add a test.
Also tell me which tests in the 426-line rewrite of test_skills_download.py were removed (not just changed), so I can confirm we didn’t drop coverage.
```
