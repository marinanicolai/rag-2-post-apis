```
Not A or B: fix items 1-8 now, tests first. #5 (publish_plugins.py crash on a NULL pin) and
#7 (approving the wrong division's row) touch code that's already live, so they can't wait.
Also now: a test that approval enqueues a publish job, and add scripts/tests to the CI test
command (I'll edit .gitlab-ci.yml myself; give me the exact line). Run the tests after each
group.
Decisions: 1) expected_content_hash: record as not delivered; follow-up is a preview
endpoint plus the client sending the hash. 2) Refuse to publish an older version when a
newer one is published, with a clear error. 3) hash_tree framing: no change; flag to Zach,
plan a versioned hash later.
Follow-up MR: the bare-repo end-to-end test, the admin route HTTP tests, FakeRepo
strictness, and the lower-priority list. Log them in PROGRESS.md.
```
