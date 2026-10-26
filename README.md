```
Get-ExecutionPolicy -List
'{}' | powershell -NoProfile -ExecutionPolicy Bypass -File scripts\dlp_hook_launcher.ps1 -Root "$PWD" -HookEvent SessionStart
$LASTEXITCODE
```
