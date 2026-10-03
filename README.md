Abyane asked for a specific check: register a plugin with a `sha`, then read `/claude-code/marketplace.json` back and confirm the `sha` is there. Your install test already proves it works indirectly, but showing it directly in the catalog gives him exact evidence. You can also test revocation in the same session.

You'll need the management key again, so check with Daniel if you deleted it. Your test repo still has v1 at the pinned commit.

**Part 1: Show the sha in the catalog**

1. Set the key and register the pinned entry:
   ```
   $env:LITELLM_KEY = "sk-your-management-key"

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

2. Read the catalog back, which is exactly what Claude Code sees:
   ```
   curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
   ```
   Look for `"sha":"3928a22a..."` inside the entry's `source`. Take a screenshot, after clearing the terminal with `cls` so the key isn't visible.

**Part 2: Test revocation**

3. Install it and confirm it works:
   ```
   claude plugin marketplace add https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
   claude plugin install skillhub-spike-pinned@litellm
   ```

4. Revoke it by deleting it from LiteLLM:
   ```
   Invoke-RestMethod -Method Delete -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins/skillhub-spike-pinned" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" }
   ```

5. Refresh the catalog on your machine and see what happens:
   ```
   claude plugin marketplace update litellm
   claude plugin list
   Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache\litellm" -Recurse -Filter hello.py
   ```
   If the plugin is still listed and `hello.py` is still there, revoking in LiteLLM doesn't remove it from machines that already have it.

**Clean up**
```
claude plugin uninstall skillhub-spike-pinned@litellm
claude plugin marketplace remove litellm
Remove-Item Env:LITELLM_KEY
```

