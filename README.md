```
You read the original ADR 0001. The approved amendment (Oct 13) is now at
docs/script-support/adr-amendment.md. It has the 7-step flow, the skillhub-plugins
publisher, hook_versions, LLM review, the build order, and "tags are never moved or
deleted". Re-check your conflicts against it. My calls on what's left:
1. Dependencies: scripts are Python standard library only for now (skillhub-rules.yml is
   the enforced rule). Dependency declarations stay an open question.
2. Scan timing: both exist. Pre-approval scanning of submissions is ADR step 5 (open
   question: how files reach CI); skillhub-plugins does the post-publish weekly re-scan.
   Record both.
3. Visibility: follow the code (publish_plugins.py partitions by division). List it as an
   ADR correction for Zach.
4. Pin target: users pin the commit sha; the tag is the human-readable name. Protected
   tags aren't the same as immutable, so the guide must say only skillhub-publisher creates
   tags and nobody updates or deletes them. Flag the GitLab setting to confirm with Zach.
Then write the guide.
```
```
Decisions: 1) defer the trigger to 061, log it. 2) stricter pin rule. 3) include
expected_content_hash in part 1. 4) yes, editing an approved hook creates a new version
that needs review; existing pins stay. 5) one MR, five commits, part 2 enforcement behind a
setting. 6) yes, pre-apply with approvals paused (prod by Zach).
Approved. Build part 1 test-first, run requesting-code-review, give me the test commands.
```
