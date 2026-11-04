```
Thanks for flagging it. Delete test_plugin_publisher_helpers.py; don't keep the
split-string fixtures.
Rewrite the scrubber to remove known secret VALUES (the GitLab token and any other secret
from settings) from error text, rather than matching token-shaped patterns. Tests set the
token setting to a harmless sentinel like "test-sentinel-value-123" and assert it's removed.
No token-shaped literals anywhere, no string-splitting, and no other ways around the DLP
filter. If a test or file still gets blocked, stop and tell me; don't rework it to get past
the filter.
Don't ask Information Security for an exception for now. If we later need pattern-based
scrubbing, I'll raise it with them.
Then continue part 2.
```
