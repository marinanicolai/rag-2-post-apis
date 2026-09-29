
# Epic: Investigate Script Support for Skillhub

## What I'm looking into
Right now Skillhub blocks all scripts in submissions, which makes sense for security. But some skills would be a lot more useful with small helper scripts. I'm investigating what the backend would need so we could safely allow scripts in the future, with admin review still in place.

## What I've found so far
- Checking packages against our Nexus PyPI mirror is doable. Each package page lists its files with hashes, so the backend can confirm a package and version exist with one request.
- The mirror seems to include very old versions (for example, `requests` from 2012), so "it's in Nexus" may not mean it's been vetted.
- A package check alone isn't enough. The bigger risk is what the script itself does, so admins would still need to review the code.

## What I want to figure out
1. Who owns `allowlist_policy.py`, and what they'd need to see before considering a change
2. Whether the mirror is curated or just proxies PyPI, and whether we have Sonatype Firewall
3. How the backend would check dependencies at submission (pinned versions, hashes, known vulnerabilities) without running any submitted code
4. How to show these findings to admins during review
5. Whether we can scan scripts for risky patterns like network calls or file deletion
6. What limits scripts would need at runtime (ties to the sandboxing work deferred in #74)

## Outcome
A proposal for the policy owner and security review, with a prototype of the dependency check tested on sample submissions. Scripts stay blocked unless a policy change is approved.
