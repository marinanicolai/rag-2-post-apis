```
$hook = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\hook.py"
$cmd = 'type C:\Users\M3MXN08\Documents\confidential-test.docx'
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Bash"; tool_input=@{command=$cmd}} | ConvertTo-Json -Compress
$in | python $hook PreToolUse
$LASTEXITCODE
```
```
$cmd = 'python -c "import zipfile; print(zipfile.ZipFile(r''C:\Users\M3MXN08\Documents\confidential-test.docx'').read(''word/document.xml'')[:200])"'
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Bash"; tool_input=@{command=$cmd}} | ConvertTo-Json -Compress
$in | python $hook PreToolUse
$LASTEXITCODE
```
$lines = Get-Content .\client\hook.py
165..235 | ForEach-Object { "{0}: {1}" -f $_, $lines[$_-1] }
```
