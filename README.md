```
I'm planning database changes for script support in Skillhub. Do not change any code yet; just investigate and report.

1. List the existing database models related to skills, plugins, versions, submissions, reviews, and audit (for example SkillVersion, PluginVersion, audit_log). For each, show its fields, how it's identified (primary key), and how it relates to the others.
2. How are uploaded submission files stored today: in database columns, on disk, or elsewhere? Where in the code does that happen?
3. How is a submission's status tracked (pending, approved, changes requested, denied), and where are review decisions recorded?
4. Is there anything today like a content hash (for example SHA-256) on uploaded files or versions?
5. How are database changes made: the Alembic setup, where migrations live, and the naming pattern of recent migrations?

Cite file paths for each answer. Keep it short. Don't include hostnames or secrets.
```
