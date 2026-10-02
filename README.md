```
I'm working with an architect on adding script support to Skillhub (the ai-marketplace app). Investigate this repository and answer the questions below. For each answer, cite the file paths you found it in. If something isn't in this repo, say "not found here" instead of guessing.

1. What is Skillhub technically: a custom app our team built, or a hosted product? What's the stack, and how is it built and deployed by the pipelines?
2. How do users authenticate (SSO, tokens, none)?
3. How does the submission pipeline work today? Find where submissions are validated (for example validate_plugin and allowlist_policy.py / denied_paths), and list exactly what is checked and blocked.
4. Is there any existing scanning step (static analysis, secret scanning, dependency or vulnerability checks) in CI that could be reused for scanning submitted scripts?
5. Approval flow: who can approve submissions? Is there anything preventing a submitter from approving their own submission?
6. Can an approved version be revoked or rolled back? How?
7. Is there an audit trail of submissions and approvals? Where is it stored, and is there any retention setting?
8. Is LiteLLM referenced anywhere (gateway URL, Claude Code base URL, keys, or plugin registration)?

Write the answers as a short summary I can share with an external architect. Do NOT include secrets, keys, tokens, internal hostnames, IP addresses, or personal names. Replace any of those with placeholders like <internal-host>.
```
```
I'm working with an architect on adding script support to Skillhub (the ai-marketplace app). Investigate this Salt repository and answer the questions below. For each answer, cite the file paths (states, pillars, templates) you found it in. If something isn't here, say "not found here" instead of guessing.

1. Which database does Skillhub use (type and version), and how is it provisioned and configured by Salt?
2. What schemas or tables relate to Skillhub submissions, approvals, users, and roles, if any are defined or referenced here?
3. How are database users and permissions set up? Which roles can write approval or submission data?
4. Is there any audit logging configured (database audit logs, history tables, log shipping), and what are the retention or backup settings?
5. Is LiteLLM managed by Salt? If so, how is it configured (its own database, keys, admin access, the Claude Code plugin marketplace)?
6. How are secrets handled (Salt pillar, vault, environment variables)? Describe the mechanism only, not the values.

Write the answers as a short summary I can share with an external architect. Do NOT include secrets, passwords, keys, connection strings, internal hostnames, IP addresses, or personal names. Replace any of those with placeholders like <internal-host>.
```
