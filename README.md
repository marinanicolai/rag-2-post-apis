```
$h = Get-Content -Raw hooks\hooks.json | ConvertFrom-Json
$env:CLAUDE_PLUGIN_ROOT = "$PWD"
$enc = $h.hooks.SessionStart[0].hooks[0].command.Split(' ')[-1]
'{}' | powershell -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -EncodedCommand $enc
$LASTEXITCODE
```
