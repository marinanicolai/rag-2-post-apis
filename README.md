Here's the pin test again, step by step. Clear the terminal (`cls`) before taking any screenshots so the key isn't visible.

**1. Set the new key**
```
$env:LITELLM_KEY = "sk-your-new-key"
```

**2. Register a pinned entry pointing to your v1 commit**
```
$body = @{
  name = "skillhub-spike-pinned"
  version = "0.1.0"
  source = @{
    source = "url"
    url = "https://gitlab.frb.gov/ai-program/platforms/tech-enablement/business-pilots/debates.git"
    sha = "3928a22a6d72d8f21bf9b012dc68ebdc08d59865"
  }
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" } -Body $body -ContentType "application/json"
```
If you get the same "only allowed to call routes: llm_api_routes" error, this key has the same limit, so tell Daniel.

**3. Check whether the pin was kept**
```
curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
```
Look at the `skillhub-spike-pinned` entry. Does its `source` include `"sha":"3928a22a..."`?

**4. If the sha is there, install it and check the code**
```
claude plugin marketplace update litellm
claude plugin install skillhub-spike-pinned@litellm
Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache\litellm\skillhub-spike-pinned" -Recurse -Filter hello.py | Get-Content
```
Your repo now has v2 code, so the result tells you everything:
- **Prints v1:** pinning works. Users get exactly the approved commit, even though the repo has moved on.
- **Prints v2:** the pin was ignored.
- **The sha was missing in step 3:** LiteLLM drops it, so pinning isn't supported.

Send the output from steps 2 and 3, and step 4 if you get that far.
