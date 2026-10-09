
```

Expand-Archive $env:USERPROFILE\Downloads\inference-hook-dlp-0.2.1-win-x64.zip $env:TEMP\dlp -Force
Get-ChildItem $env:TEMP\dlp
& "$env:TEMP\dlp\inference-hook-dlp\bin\dlp-hook.exe" --version
```
