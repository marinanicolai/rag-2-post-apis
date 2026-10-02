```
Subject: Follow-up: Skillhub review process action items

Hi all,

Thank you for today's meeting. From my notes, these are the tasks I'll be working on:

1. Email notifications: notify admins by email when a user submits a skill, plugin, or hook for review. Skillhub's notifications are currently in-app only, and email was designed as an extension but never built, so this includes setting up email delivery.

2. Admin approval guide: add a page in the admin section that walks admins through the approval process, including what to check and how to read the scan results.

3. Automated scanning before approval: design the backend so every submission is scanned in GitLab CI before it reaches an admin. We already have Bandit, Semgrep, detect-secrets, and a vulnerability scanner configured in the repo; they just aren't pointed at submissions yet.

4. LLM judge: use LiteLLM to add an AI review step that summarizes each submission and flags risks for the admin. Skillhub already has an LLM review step built in but turned off, so I'll build on it. It will support the admin's decision, not replace it, and the admin will always make the final call.

While reviewing the code, I also noticed a few gaps in the approval flow that would be good to address alongside this work: admins can currently approve their own submissions, there's no way to roll back to an earlier approved version, and audit log entries are deleted after 365 days.

I'll create stories for each of these in GitLab and share them once they're ready. Please let me know if I missed anything or if any priorities should change.

Thanks,
Marina
```
