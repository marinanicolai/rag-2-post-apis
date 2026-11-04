```
Goal: write docs/script-support/IMPLEMENTATION-GUIDE.md, the single document an agent
follows to implement the rest of the ADR. It must be specific enough that an agent with no
other context builds the right thing.

Sources (read-only; don't change code or anything in skillhub-plugins):
- docs/script-support/adr-amendment.md (the approved ADR amendment) and PROGRESS.md
- the Oct 20 Publisher plan under docs/
- this repo's models, migrations 058/059, publish_plugins.py, the audit script, and the
  .gitlab/ci deploy files (the DLP hook may block some; list what you couldn't read)
- ..\skillhub-plugins: README.md, .gitlab-ci.yml, skillhub-rules.yml, the folder layout
  (hooks/, plugins/, skills/), the tag rules

Investigate first, then write the guide with these sections:
1. Invariants: what an admin reviewed is exactly what users get; Postgres is the source of
   truth; skillhub-plugins holds approved versions only; tags never move; LLM review is
   advisory only.
2. System map: the two repos, the database, and the 7-step approval-and-publish flow.
3. The skillhub-plugins contract: folder layout for a published plugin, tag format
   <plugin-name>/v<version>, commit author and message, what its CI does on every push,
   and what the Publisher must and must not do there. Flag anything the README doesn't settle.
4. Data model: 058 columns, 059 (renderer marker), the planned 060 (hook_versions).
5. Build order with acceptance criteria per part: 060, Publisher (plus the revoked[] fix),
   LLM review, LiteLLM registration. For each part: files to touch, tests that prove it,
   the settings flag, and its "done" definition.
6. Deploy and data rules learned this week: name the schema explicitly (salt1 defaults to
   dev), pre-apply migrations the new code depends on (the prod job runs alembic after
   unpacking code), read-only checks with BEGIN READ ONLY, never print credentials.
7. Working rules for agents: DLP hook (hand test commands to the human), test:api
   baseline, plan-then-OK-then-TDD, commit per part, one branch / one MR.
8. Open questions with owners: publish token and signing (Zach), job runner location
   (infra), LLM model, key and data policy (Daniel), forceRemoveDeletedPlugins in LiteLLM,
   how untrusted files reach CI scanning.

Process: draft it, then run /council on the draft and fix what it finds. Use /prompt-forge
for section 7 so its instructions read as clear agent rules. Show me the open questions and
any conflicts between the ADR, the README and the code before the final version. Don't commit.
```
