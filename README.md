```
git switch --detach origin/main
$in | python .\client\hook.py PreToolUse
$LASTEXITCODE
```
```
git switch fix/bash-embedded-paths
$in | python .\client\hook.py PreToolUse
$LASTEXITCODE
```
```
$in2 = @{hook_event_name="PreToolUse"; session_id="mr-test"; cwd=$dir; tool_name="Bash"; tool_input=@{command="type $dir\memo.txt"}} | ConvertTo-Json -Compress
$in2 | python .\client\hook.py PreToolUse
$LASTEXITCODE
```
