# Epic: Safe Script Support for Skillhub Submissions

## Summary
Skillhub blocks all executable code in submissions (`denied_paths` in `allowlist_policy.py`). This epic proposes allowing helper scripts under layered controls, starting with a policy proposal (v3) for the policy owner and security review. Admin review of every script stays the main control.

## Why
- Skills can't ship helper scripts, which limits what they can do.
- A "packages must be in Nexus" rule alone isn't safe. The main risk is the script's own code, and our PyPI mirror appears to serve old, vulnerable versions.

## Proposed controls
- **Admin code review:** kept as the main control.
- **Dependency check:** packages must be pinned, hashed, and on the approved mirror, with a vulnerability lookup.
- **Static scan:** flags network calls, file deletion, `subprocess`, `eval`, and runtime installs for the reviewer.
- **Runtime restrictions:** limit network and file access (ties to #74 sandboxing).

## Issues
1. Draft policy v3 with the policy owner and security review
2. Confirm mirror behavior (open proxy or curated, Firewall, https)
3. Build the dependency check, tested on sample submissions only
4. Add a findings panel to the admin review
5. Add a static scan of script code
6. Design runtime restrictions
7. Re-scan approved scripts on a schedule

## Rollout
Scripts stay blocked until v3 is approved. After approval, scripts start in warn-only mode: admins review every script with automated findings, and automatic blocking is added once results are reviewed.

## Related
#74: Add plugin system for skills (script support deferred)
