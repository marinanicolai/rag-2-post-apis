```
$src = "dist\inference-hook-dlp"; $out = "$env:TEMP\dlpbisect2"
New-Item -ItemType Directory $out -Force | Out-Null
Get-ChildItem $src -Force | Where-Object Name -ne ".claude-plugin" | ForEach-Object {
  Compress-Archive -Path "$src\.claude-plugin", $_.FullName -DestinationPath "$out\$($_.Name).zip" -Force
}
explorer $out
```
