```
Go ahead with Phase 1.
1. Description limit: yes, 1024. It matches the Claude skill frontmatter limit for description, so a skill that passes our form also works when installed. Use the same number in the server validator, the DB constraint (if any), the form hint and the counter.
2. js-yaml: no, don't add a client dependency. The server is the source of truth: it parses the frontmatter and returns a clear 400 naming the field and problem, and the form shows that message. If the form currently pre-fills name/description from an uploaded SKILL.md, tell me how it does that first; if it needs parsing, prefer a small server "validate/preview" endpoint over a second YAML parser in the browser.
Keep Phase 2 on hold as planned. When Phase 1 is pushed, give me the MR link and the read-only SQL for affected submissions.
```
