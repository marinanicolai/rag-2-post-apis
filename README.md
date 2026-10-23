```
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Read"; tool_input=@{file_path="C:\Users\M3MXN08\Documents\confidential-test.docx"}} | ConvertTo-Json -Compress
$in | python .\client\hook.py PreToolUse
$LASTEXITCODE
```
