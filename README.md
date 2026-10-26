```
"name,ssn`r`nAda,219-09-1234" | Set-Content $env:TEMP\roster.txt
$payload = @{ hook_event_name = 'PreToolUse'; tool_name = 'Read'; cwd = "$PWD";
              tool_input = @{ file_path = "$env:TEMP\roster.txt" } } | ConvertTo-Json -Compress
$enc = $h.hooks.PreToolUse[0].hooks[0].command.Split(' ')[-1]
$payload | powershell -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -EncodedCommand $enc
$LASTEXITCODE
```
