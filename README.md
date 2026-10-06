```
Hey, before I send this to Zach, could you sanity-check my plan?

The big picture: we want to let skills and plugins include scripts, but only if users get exactly the code an admin reviewed. The flow is: upload → quarantine → scan → admin review → the approved files get committed to a locked repo → Skillhub registers that exact commit in LiteLLM. My spike confirmed LiteLLM keeps the plugin pinned to the commit, even if the repo changes later.

That locked repo would be skillhub-approved-plugins. Only a Skillhub service account could push to it, with no force push, so its history becomes the record of what was approved and when. It's kept separate from the main Skillhub repo, because users clone it when they install a plugin, and it shouldn't contain app code or deploy secrets.

What I want to ask Zach for: Maintainer access to that repo, so I can protect main and the version tags, create a project access token for the service account, register a scan runner, and add a scheduled re-scan pipeline before locking main. After setup, we'd keep Maintainers to the service account plus one or two admins.

Does this make sense to you, or is there anything I'm missing before I send it?
```
