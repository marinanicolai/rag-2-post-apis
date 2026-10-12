```
Go with (c): only the hash work now (tasks 1, 2 and 5 on this branch), based on origin/main. Defer the PluginVersion columns and that migration until feature/plugins-spine is merged into main.

Important: main is at migration 046 and plugins-spine already uses 047-057. Avoid adding a migration in this branch if the Submission.content_hash change doesn't require one. If it does, stop and tell me before creating it, so we can avoid a numbering clash.

Also stash ai_docs/notes/TRACE-SUMMARY.md separately with a clear message; I didn't mean to include it.

Show me the revised plan before writing code.
```
