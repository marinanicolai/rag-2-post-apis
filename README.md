
```
New-Item -ItemType Directory -Force $env:USERPROFILE\source\repos\dlp-0.2.1 | Out-Null
Copy-Item $env:TEMP\dlp\inference-hook-dlp $env:USERPROFILE\source\repos\dlp-0.2.1\ -Recurse -Force
& "$env:USERPROFILE\source\repos\dlp-0.2.1\inference-hook-dlp\bin\dlp-hook.exe" --version
```
