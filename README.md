```
Get-ChildItem dist\inference-hook-dlp -Recurse -Include *.docx,*.xlsx,*.pptx,*.pdf,*.msg | Select-Object FullName, Length
```
```
$src = "dist\inference-hook-dlp"; $out = "$env:TEMP\dlpbisect"
New-Item -ItemType Directory $out -Force | Out-Null
Get-ChildItem $src | ForEach-Object { Compress-Archive $_.FullName "$out\$($_.Name).zip" -Force }
explorer $out
```
