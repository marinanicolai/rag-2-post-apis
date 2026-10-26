```
$zip = Get-Item dist\inference-hook-dlp.zip
$newest = Get-ChildItem .claude-plugin, hooks, client, app, restrictions, vendor, scripts, skills, config -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notmatch '__pycache__' } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
"zip:    $($zip.LastWriteTime)"
"newest: $($newest.LastWriteTime)  $($newest.FullName)"
if ($newest.LastWriteTime -gt $zip.LastWriteTime) { "STALE - rebuild" } else { "UP TO DATE" }
```
