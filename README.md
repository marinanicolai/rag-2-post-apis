```
    Get-Content $HOME\.claude\settings.json
Get-ChildItem .claude -Force
Select-String -Path README.md -Pattern "install|settings.json|hooks" -Context 0,3
```

