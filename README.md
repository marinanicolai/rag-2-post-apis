---
status: proposed
date: 2026-10-01
decision-makers: Zach Vida
consulted: Daniel Odukoya
informed:
---

# Review and distribute user-submitted plugin scripts

## Context and Problem Statement

Skillhub lets people in the organization submit skills, hooks, and plugins, which admins review and then approve, request changes on, or deny. Today all executable code is blocked in submissions (`denied_paths` in `allowlist_policy.py`), so plugins can't include helper scripts.

Some plugins need scripts to be useful. For example, a plugin that extracts text from PDFs needs a script to read the files; instructions alone can't do it. We want a way to support scripts like this safely. We first looked at relying on packages from our internal Nexus mirror, but that approach won't work in our environment.

The core concern is the scripts themselves. When a user submits a plugin with scripts, those scripts will run on other people's machines. So we need two things: a way to check every submitted script before it's approved, and a way to make sure the exact script that was checked is the one users receive.

How should Skillhub check the scripts users submit, and distribute them so users only ever receive the reviewed version?

## Decision Drivers

* Every script a user submits must be checked and approved before anyone can install it
* Security: users must receive exactly the code an admin approved, and nothing else
* Control over where plugin code is stored and who can access it
* Implementation and maintenance effort for the team
* Fit with tools we already run (Skillhub, LiteLLM)
* Experience for users discovering and installing plugins in Claude Code

## Considered Options

* **Option 1:** Skillhub stores and serves the full plugin source code
* **Option 2:** LiteLLM's Claude Code plugin marketplace handles distribution, with Skillhub as the review gate and catalog
* **Option 3:** Ship script dependencies through Nexus (ruled out)

## Decision Outcome

Proposed: **Option 2, with conditions.** Pending review by the decision-maker.

The spike showed that LiteLLM is unsafe as configured through its UI, because entries follow a live Git branch. However, entries registered through the LiteLLM API with a pinned commit (`sha`) deliver exactly the approved code, even after the repository changes. That makes Option 2 workable if Skillhub becomes the only path into LiteLLM:

1. An author submits a plugin to Skillhub.
2. Skillhub runs automated checks on the submitted scripts, then an admin reviews the code at that specific commit and approves it.
3. Skillhub's backend registers the plugin in LiteLLM through the API, pinned to that commit.
4. Any later change requires a new Skillhub review and a new pinned registration.

### How submitted scripts are checked

Pinning only guarantees that users get the reviewed version; the review itself is what decides whether a script is safe. These checks apply under either option and are proposed, not yet built:

* **Admin code review (main control):** an admin reads every script and checks what it actually does.
* **Automated scan at submission:** Skillhub flags risky patterns for the reviewer, such as network calls, file deletion, access to credential paths, `subprocess`, `eval`/`exec`, and installing packages at runtime. The scan informs the review; it doesn't replace it.
* **Dependency check:** scripts must declare the packages they use with exact versions. Since the Nexus route is ruled out, how dependencies are approved and installed is still an open question for the follow-up work.
* **Review is tied to a commit:** the admin approves a specific commit, and that same commit is what gets pinned, so what was reviewed is exactly what users receive.

### Consequences

* Good, because users only receive admin-reviewed code, pinned to an exact commit
* Good, because we reuse LiteLLM's existing marketplace endpoint instead of building our own
* Good, because Skillhub keeps its role as the review and approval gate
* Bad, because skills added directly in the LiteLLM UI are not pinned; this path must be restricted or kept admin-only by process
* Bad, because Skillhub's backend needs a LiteLLM key with management route access, which must be stored securely
* Bad, because the catalog is public and has no per-team access control
* Bad, because LiteLLM calls its catalog the "Skill Hub," which may confuse users alongside our Skillhub

### Confirmation

* Review of this ADR by the project owner
* Security review of how Skillhub stores the management key and registers pinned plugins
* A test confirming that a plugin registered by Skillhub installs the approved commit after the repository changes

## Pros and Cons of the Options

### Option 1: Skillhub stores and serves the full plugin source code

Skillhub keeps the approved plugin files and exposes its own marketplace endpoint that Claude Code can install from.

* Good, because we fully control storage, review, versioning, and access
* Good, because the admin review flow already lives in Skillhub
* Good, because access could be limited by team or user
* Bad, because it's more work to build and maintain, including a marketplace endpoint compatible with Claude Code

### Option 2: LiteLLM plugin marketplace, Skillhub as review gate and catalog

Approved plugins are registered in LiteLLM through its API, pinned to the reviewed commit. Users install from LiteLLM's catalog.

* Good, because API registration with a `sha` locks users to the approved commit (verified in the spike)
* Good, because it reuses a gateway we already run
* Bad, because the UI cannot pin, so UI-added entries follow the live branch
* Bad, because the catalog is public, entries are visible immediately, and there's no per-team access control
* Neutral, because scripts still run on users' machines, so admin code review remains essential under either option

### Option 3: Ship script dependencies through Nexus

* Bad, because the project owner confirmed this won't work in our environment
* Bad, because a package-source rule doesn't address the main risk, which is the script's own code
* Bad, because our PyPI mirror appears to serve old versions (for example, `requests` 0.10.3), so "available in Nexus" doesn't mean vetted

## More Information

### Spike findings (LiteLLM v1.100.0, dev-2 instance, September 30 to October 1, 2026)

A throwaway plugin with a skill and a small script was registered in LiteLLM and installed in Claude Code.

| Question | Result |
| --- | --- |
| Is the catalog (`/claude-code/marketplace.json`) protected? | No, it's public with no auth |
| Can a skill be hidden until approved? | Not in the UI; skills are visible as soon as they're added. The API has an `enabled` field (default `true`); creating disabled entries was not tested |
| Can the UI pin a branch or commit? | No; only repo URL (HTTPS only) and subfolder |
| Are scripts installed on users' machines? | Yes, copied to the local plugin cache with no review step in LiteLLM |
| Unpinned: does a code push reach new installs? | Yes, immediately, under the same version label |
| Unpinned: does a version bump in the repo reach existing installs? | Yes, updated 0.1.0 to 0.2.0 with no admin action; LiteLLM still showed 0.1.0 |
| Can the API pin a commit? | Yes; the `sha` is stored and installs deliver that exact commit |
| Pinned: does it follow repo changes or version bumps? | No, it stayed at the pinned commit (0.1.0) |
| What key does API registration need? | One with management route access; LLM API keys are refused |
| Can access be limited by team or user? | No; skill records have no team, user, or access group fields |

### Related

* LiteLLM docs: https://docs.litellm.ai/docs/tutorials/claude_code_plugin_marketplace
* #74: Add plugin system for skills (script support deferred)
