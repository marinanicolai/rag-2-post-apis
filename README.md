```
Yes, I'd recommend option 2: use LiteLLM for distribution, with Skillhub as the review gate.

The spike showed LiteLLM can lock a plugin to the exact commit an admin reviewed, as long as it's registered through the API. So the flow would be: a user submits a plugin with scripts to Skillhub, Skillhub runs automated checks, an admin reviews and approves it, and then Skillhub registers it in LiteLLM pinned to that commit. Users only ever get the reviewed version, and we don't have to build our own distribution system.

The main trade-offs: LiteLLM's catalog is public and has no per-team access control, and the Skillhub backend would need a management-level LiteLLM key. If either of those is a dealbreaker, option 1 (Skillhub stores and serves the code itself) gives us full control, but it's more work to build.
```
