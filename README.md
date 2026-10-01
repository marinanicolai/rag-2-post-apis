```
he ADR is ready for your review: [link to MR, or see attached].

I did the LiteLLM spike on dev-2 with a test plugin. The main finding: plugins added through the LiteLLM UI follow the live Git branch, so an author can change the code after approval and it reaches users with no admin action. But plugins registered through the API with a pinned commit stay on exactly that commit, even after the repo changes.

Based on that, I'm proposing option 2 with conditions: Skillhub stays the review gate for submitted scripts, and on approval it registers the plugin in LiteLLM through the API, pinned to the reviewed commit. The full test results are in the ADR.

Thanks to Daniel for helping with the API access. Happy to walk through it if that's easier.
```
