```
Select-String -Path .\restrictions\*.md -Pattern "\{label\}|\{level\}|\{marking\}|\{labels\}" | Select-Object Filename, LineNumber, Line
```
```
Set-Content "C:\Users\M3MXN08\repo\dlp-demo-files\Q3_budget_RESTRICTED_FR.txt" "Test file. Fake content only."
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Read"; tool_input=@{file_path="C:\Users\M3MXN08\repo\dlp-demo-files\Q3_budget_RESTRICTED_FR.txt"}} | ConvertTo-Json -Compress
$msg = $in | python .\client\hook.py PreToolUse 2>&1 | Out-String
$msg
```
