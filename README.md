```
Let's start fresh in a **new terminal**, so nothing old gets in the way. Run each step and check the result before moving on.

**1. TLS fix**
```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

**2. Set the key from the clipboard.** Copy the full key (starting with `sk-`) first, then:
```
$env:LITELLM_KEY = (Get-Clipboard).Trim()
$env:LITELLM_KEY.Substring(0,3)
```
It must show `sk-`. If it doesn't, copy the key again. Then run `cls`.

**3. Register the pinned plugin**
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
You should get a success response.

**4. Check the catalog for the sha.** This is the screenshot for Abyane:
```
curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
```

**5. Install it**
```
claude plugin marketplace add https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
claude plugin marketplace update litellm
claude plugin install skillhub-spike-pinned@litellm
```

**6. Revoke it in LiteLLM**
```
Invoke-RestMethod -Method Delete -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins/skillhub-spike-pinned" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" }
```

**7. Check whether it's still on your machine**
```
claude plugin marketplace update litellm
claude plugin list
Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache\litellm" -Recurse -Filter hello.py
```

If anything fails, stop there and send me that step's output, with the key hidden.
```
