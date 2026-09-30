

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
```
   curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
```
```
Invoke-RestMethod -Method Post -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" } -Body $body -ContentType "application/json"
```
```
Hi , the spike is going well. One last test needs to register a plugin through the LiteLLM API (POST /claude-code/plugins) to check whether it can pin a plugin to a specific commit. My virtual keys are limited to llm_api_routes, so the call is refused. Could you give me a key with management route access on dev-2, or run one registration call for me? I can send you the exact command.
```
