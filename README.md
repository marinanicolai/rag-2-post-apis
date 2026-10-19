```
Found it. The admin detail panel shows name and description fine (verified in prod). What’s missing is the SKILL.md frontmatter inside content: Hameed’s files start with “# context-throw” and have no ---\nname: …\ndescription: …\n--- block, so once published the skill has no name/description metadata. Read-only first, then propose:

On submit (form path), if content has no frontmatter, prepend a frontmatter block built from the form’s name and description, safely quoted (yaml.safe_dump) so the “→”, quotes, colons and backticks survive. If frontmatter exists but lacks name/description, fill them from the form fields. Add tests with his exact shape.
In the admin detail panel, show a warning badge when content has no frontmatter.
Check whether the publisher/install path (or anything that builds SKILL.md) also depends on frontmatter.
Give me a guarded UPDATE (BEGIN; SELECT before; UPDATE; SELECT after; ROLLBACK) that prepends frontmatter for SKL-39MQ14 and SKL-66Y9R9 only, and tell me whether it changes content_hash and approvals.
Put 1 and 2 on the current fix branch. No prod writes.
```
