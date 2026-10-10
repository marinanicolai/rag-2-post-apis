```
$repo = "C:/Users/M3MXN08/repo/c4g-dlp-hooks-repo"
$h = Get-Content "$repo/hooks/hooks.json" -Raw | ConvertFrom-Json
$hooksJson = ($h.hooks | ConvertTo-Json -Depth 20) -replace '\$\{CLAUDE_PLUGIN_ROOT\}', $repo
$out = "{`n  `"enabledPlugins`": {},`n  `"hooks`": $hooksJson`n}"
$null = $out | ConvertFrom-Json
[IO.File]::WriteAllText("C:\temp\c4g-test\.claude\settings.json", $out, (New-Object Text.UTF8Encoding $false))
Get-Content C:\temp\c4g-test\.claude\settings.json
```
