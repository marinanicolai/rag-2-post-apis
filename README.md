```
Here's an internal team update on the Skillhub script-support work, written to post in Teams or a team channel:

---

**Update: script support in Skillhub**

Right now Skillhub blocks all scripts in submitted plugins. Some plugins really need them, like the PDF text-extraction plugin, so I've been working out how we could allow scripts safely.

**What I've done**
- Ran a spike on our LiteLLM dev instance to test it as the way plugins reach people's machines
- Wrote an ADR with the findings and a recommendation, now with Zach for review
- Reviewed the Skillhub codebase with Claude Code to see what we can build on

**What I found**
- LiteLLM can safely distribute plugins only if each one is locked to the exact commit an admin reviewed. That works through its API, but not through its UI, where a plugin follows the live branch and the author can change code after approval.
- My recommendation: Skillhub stays the review gate. After an admin approves a plugin, Skillhub registers it in LiteLLM pinned to that reviewed commit. Everyone can install it, and they only get the approved version.
- We already have scanning tools in the repo (Bandit, Semgrep, detect-secrets, a vulnerability scanner), but they're turned off in CI and don't scan submissions yet. They're a good starting point for checking submitted scripts.

**Gaps to fix before scripts ship**
- Admins can currently approve their own submissions.
- There's no way to roll back to an earlier approved version.
- The audit log deletes entries after 365 days, and its tamper protection isn't set up in our migrations. We should confirm the retention period we actually need.

**Next steps**
- Get Zach's feedback on the ADR
- Work with Abyane on the backend design
- Plan the fixes above as part of the script-support work

Happy to walk anyone through the details.

---

Claude Code also flagged two authentication issues: a fallback login path that skips Kerberos, and a dev-only login that's live in the same app. I'd raise those directly with Zach or your security contact rather than in a team-wide post, so they get handled without spreading the details widely. If you meant a different tool update, tell me which one and I'll redo it.
```
