```
$repo = "C:/Users/M3MXN08/repo/c4g-dlp-hooks-repo"
$s = "$env:USERPROFILE\.claude\settings.json"
if (Test-Path $s) { Copy-Item $s "$s.bak" -Force; $cfg = Get-Content $s -Raw | ConvertFrom-Json } else { New-Item -ItemType Directory -Force (Split-Path $s) | Out-Null; $cfg = [pscustomobject]@{} }
$h = ((Get-Content "$repo/hooks/hooks.json" -Raw) -replace '\$\{CLAUDE_PLUGIN_ROOT\}', $repo) | ConvertFrom-Json
$cfg | Add-Member -NotePropertyName hooks -NotePropertyValue $h.hooks -Force
[IO.File]::WriteAllText($s, ($cfg | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding $false))
"hooks added: " + ((Get-Content $s -Raw | ConvertFrom-Json).hooks.PSObject.Properties.Name -join ", ")
```
```
