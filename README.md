```
'{}' | powershell -NoProfile -Command "& ([scriptblock]::Create((Get-Content -Raw scripts\dlp_hook_launcher.ps1))) -Root '$PWD' -HookEvent SessionStart"
$LASTEXITCODE
```
```
Get-Content $env:LOCALAPPDATA\inference-hook-dlp\launcher.log -Tail 3
```

