```
Create docs/script-support/adr-amendment.md with exactly the content between the
BEGIN and END markers (don't include the markers). Then apply my four calls and write the
guide. The 7-step flow is reconstructed from the text: mark it "reconstructed, confirm
with Marina". Leave the two untracked 060 files alone. Don't commit.

BEGIN
# ADR Amendment: Skillhub Plugin Script Support — Implementation Plan

Oct 13, 2026 · @Marina

## Status and context

This amendment turns the approved ADR on plugin and script distribution into a concrete data model and build order. It keeps the ADR's core guarantee: the exact files an admin reviewed are the files users receive, and any change needs a new review.

It is informed by a code investigation of ai-marketplace main (after plugins-spine merged, migrations 047-057) and an external architecture review. Status: proposed, for Zach's review.

## Decision summary

Postgres is the source of truth for every plugin version, identified by the hash of its exact content. The skillhub-plugins repo and the LiteLLM catalog are views of approved versions that can be rebuilt from it.

Approval and publish flow, 7 steps (diagram in the Google Doc; steps reconstructed from the text, confirm with Marina):

1. Submit: a user uploads a new plugin version; it is stored in Postgres with its content hash.
2. Automated scans: deterministic scanners and the LLM review run and store scan_results.
3. Admin review: the admin reads the files, findings and judge summary.
4. Approval rules in the API: no self-approval; a version with a script needs two approvers, or one approver plus a clean scan.
5. Publish job: approval enqueues a publish job in the jobs table.
6. Commit and tag: skillhub-publisher commits the exact approved tree to skillhub-plugins, creates the tag, and the commit sha is recorded.
7. LiteLLM registration: the approved commit sha is registered so users install that exact version.

Nothing reaches the repo until an admin approves. The robot account skillhub-publisher, not the submitter, commits the approved files, so the commit holds exactly the reviewed bytes.

## Changes to the original design

Six additions and one refinement to the design note "Skillhub Script Support: Data Model Design Note":

| Change | Why |
| :---- | :---- |
| Append-only review_events table | The current audit log deletes entries after 365 days; an audit trail that can be edited or expire is not proof of what was approved |
| Three-level scan results with recorded justifications | Blocking on every finding floods admins until they approve without reading |
| Approval rules enforced in the API | Self-approval is currently allowed; the API can be called directly, so a UI-only check is not enough |
| Active version pointer per plugin | Rollback becomes pointing at an earlier approved version, with no second review |
| One jobs table for scans and publishing | The app has no background job system; threads die with the process under CGI, so failed work would be lost without retry |
| LLM review through LiteLLM, as a scanner and a judge | Pattern scanners catch known bad calls but cannot say whether a script does what its description claims; a model-written review gives admins that context in plain language |
| Plugins keep content_hash (hash_tree) as their canonical hash; no second bundle hash | It is already a full 64-character digest of the exact tree the gate validated, and revocation and the signed marketplace index depend on it. Skills use the new bundle hash (merged). |

## Data model

Migration 058 adds publishing, scanning, audit and jobs. Migration 060 adds hook versions. Migration 059 (Oct 21) adds a renderer marker so that already-approved versions keep the exact SKILL.md bytes they were approved with. All three are idempotent (IF NOT EXISTS), per the CI rules.

### Migration 058

| Table | Change | Key columns |
| :---- | :---- | :---- |
| plugin_versions | Extend | publish_status (not_published, pending, publishing, published, failed), published_commit_sha, published_tag (unique), published_repo_at, publish_error, publish_attempts |
| plugins | Extend | active_version_id, for rollback |
| scan_results | New | subject type and id, content_hash of the exact content scanned, scanner and version, verdict, findings with severity (JSONB); unique per subject, hash and scanner |
| review_events | New, append-only | actor, action (submit, scan, approve, reject, override, publish, revoke), subject, content_hash, reason, timestamp; a database trigger rejects UPDATE and DELETE |
| jobs | New | kind (scan, publish), subject, state, attempts, next attempt time, lock, last error |

published_at already means approval time, so the repo commit time gets its own column.

### Migration 060

hook_versions (hook, version, hook_config, reference_files, content hash). plugin_version_hooks then points at a hook version instead of the live, editable hook row. Existing hooks are backfilled as version 1.

Today a plugin version pins the live hook row, so its contents cannot be re-derived after an edit. The git commit snapshots hook content at publish time, so 060 is not needed for publishing, but it must land before hooks may carry scripts.

## Rules

**Script policy.** Python only (no shell or JavaScript). Scripts may not make network calls, start other programs, or run dynamic code (eval, exec).

**Scan levels.**

| Level | Example | Effect |
| :---- | :---- | :---- |
| Secret | API key or password in a file | Always blocks |
| Serious | Forbidden call such as subprocess | Blocks unless an admin records a justification (stored as a review event) |
| Other | Style or low-risk findings | Warning only |

**LLM review (scanner and judge).** Skillhub sends each submitted version to a model through the LiteLLM gateway. The result has two parts:

* **Scanner:** findings with a severity, stored as a scan_results row with scanner = llm-review, tied to the content hash like any other scanner.
* **Judge:** a plain-language summary for the admin: what the scripts do, whether that matches the description, and a recommendation (approve, ask for changes, reject) with reasons.

The admin sees both on the review page next to the other scanners. The review is advisory: the admin decides.

**Governance.**

* No self-approval, enforced in the API.
* A version that contains a script needs two approvers, or one approver plus a clean scan.
* Every upload is a new version with a fresh review. Rollback to an earlier approved version needs no second review.
* The LLM review never counts as a clean scan and never approves or blocks on its own. Submissions are untrusted text and can contain instructions aimed at the model, so only the deterministic scanners and human approvers decide.
* The repo stays append-only: tags are never moved or deleted. Revocation flags the version in the database, adds it to the signed revoked list, and (later) removes it from LiteLLM.

## Implementation order and status

Done:

* Protected skillhub-plugins repo: no merges, history rewrites or tag moves; secret detection, SAST and custom Skillhub Semgrep rules; weekly re-scan
* skillhub-publisher service account, tested
* LiteLLM spike: a sha-pinned registration installs the exact commit; a removed plugin stops loading after catalog refresh
* Full SHA-256 bundle hash for skills and submissions, including reference files (merged)

Next, in order:

1. Migration 058 and models: done, merged to main
2. Approval rules in the API (no self-approval, two approvers or one plus a clean scan): done, merged to main and deployed to prod on Oct 20
3. Publisher, GitLab part: on approval, a job commits the approved tree to skillhub-plugins, tags it, and records the commit sha. Idempotent: an existing tag on the same tree counts as success. Planned on Oct 20 as five merge requests, with a scheduled main-only pipeline as the job runner; the publish token and signing questions are with Zach.
4. Migration 060, hook versions
5. CI scanning of submissions
6. LLM review through LiteLLM: scanner findings and judge summary stored in scan_results and shown on the review page
7. LiteLLM registration, behind a setting that stays off until service account access arrives (requested)

## Open questions and consequences

Open questions:

* [ ] How do untrusted submission files reach GitLab CI for scanning without landing in an installable repo? Options: a separate non-installable scan project, or a pipeline that receives the files as an artifact. Needs a short spike.
* [ ] Does LiteLLM's generated marketplace.json allow forceRemoveDeletedPlugins: true, so revoked plugins are uninstalled rather than only disabled? Test once access arrives.
* [ ] Where does the job runner run: a cron entry on the app server, or a scheduled GitLab pipeline? The publisher plan prefers a scheduled pipeline if GitLab runners can reach the prod database; asking the infrastructure team.
* [ ] LLM review: which model and LiteLLM key to use, whether submission content may be sent to it under data policy, and how the prompt keeps submitted text clearly separated from instructions. To confirm with Daniel.
* [ ] Managed Claude Code settings via MDM (allow only the Skillhub catalog, block local plugins): an IT request. Without them, users can still install plugins from other sources.

Consequences:

* Approval no longer waits on GitLab or LiteLLM; a failed publish is visible and retried instead of lost.
* Two hashes stay in the system by design: the skill bundle hash and the plugin tree hash.
* review_events cannot be cleaned up by the app; retention becomes a deliberate policy decision.
END
```
