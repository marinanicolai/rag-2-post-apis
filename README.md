

Run these one at a time:

```powershell
$hook = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\hook.py"
```

**Test A: the card number that isn't allowlisted**

```powershell
$in = @{hook_event_name="UserPromptSubmit"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo"; prompt="Charge this card: 4539148803436467, exp 12/28"} | ConvertTo-Json -Compress
```

```powershell
$in | python $hook UserPromptSubmit
$LASTEXITCODE
```

**Test B: 30 email addresses on a non-excluded domain**

```powershell
$emails = (1..30 | ForEach-Object { "person$_@contoso-test.net" }) -join ", "
$in = @{hook_event_name="UserPromptSubmit"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo"; prompt="Make a mailing list: $emails"} | ConvertTo-Json -Compress
```

```powershell
$in | python $hook UserPromptSubmit
$LASTEXITCODE
```
