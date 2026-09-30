

```
   $env:LITELLM_KEY = "sk-your-key-here"
```
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

   Invoke-RestMethod -Method Post -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" } -Body $body -ContentType "application/json"```
```
   curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
```
