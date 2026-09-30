```
I need to find and remove duplicate entries in the Skillhub library (skills and hooks), and then stop new duplicates from getting in. We are working against the DEV database first. Do NOT touch main/prod in this session.

Context:
- Users are seeing duplicate skills in the library, and the Hooks page shows duplicates too.
- I know of 3 hook entries titled "Offers a one-time onboarding tour on first session in a repo, then stays silent." (SessionStart, community, submitted by Nicolai, Marina). Those were my test submissions. One has the description "testing purposes." All 3 can go unless one of them is referenced somewhere.

Step 1: Investigate (read-only, no writes)
- Find the database connection config for dev and confirm out loud which environment/database you're connected to before running anything.
- Find the tables/models for skills, hooks, and anything related (submissions, versions, categories, votes/installs, review history, join tables).
- Write SELECT queries that find duplicates in skills and in hooks. Treat rows as duplicates when they have the same name/title (case- and whitespace-insensitive), OR the same content/config (for example the same SKILL.md body or the same hook JSON config + event type).
- For each duplicate group, show me: id, name, type/event, status (approved/pending/denied), submitter, created_at, updated_at, and counts of dependent rows (installs, votes, reviews, plugin references).
- Explain how duplicates got in. For example: missing unique constraint, resubmission creating a new row instead of a new version, or seeding scripts running twice.

Stop here and show me the report. Wait for my approval before any write.

Step 2: Dedup plan (after I approve)
- For each group, propose which row to KEEP. Default rules: prefer approved over pending/denied, then the one with the most dependent rows, then the oldest.
- For the rows being removed, re-point dependent rows (installs, votes, reviews, references) to the kept row, merging counts where needed. Don't orphan anything.
- Prefer a soft delete/archive if the schema supports it. If it doesn't, tell me before hard-deleting.

Step 3: Script
- Write it as a reusable, idempotent migration or script (in the repo's existing migration pattern), wrapped in a transaction.
- Give it a --dry-run mode that prints exactly what would change.
- Back up the affected tables (or export the affected rows) before applying.
- Run the dry run on dev, show me the output, then apply on dev only after I confirm.
- Re-run the Step 1 queries afterward to prove zero duplicates remain.

Step 4: Prevention
- Add a unique constraint/index on the normalized name per type, if the data model allows it. If it conflicts with versioning, explain the tradeoff and propose an alternative.
- Add a duplicate check in the skill and hook submission flow (API and admin review): warn the submitter and flag it for the admin reviewer when a similar name or identical content already exists.
- Add tests for the duplicate check.

Deliverables: the investigation report, the migration/script with dry-run, the prevention changes on a feature branch, and a short summary I can put in the PR/MR so the same script can go through the SDLC review and be run against main later.
```
