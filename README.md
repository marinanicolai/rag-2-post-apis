```
    python scripts\make_hooks_json.py
$h = Get-Content -Raw hooks\hooks.json | ConvertFrom-Json
$cmd = $h.hooks.UserPromptSubmit[0].hooks[0].command.Replace('${CLAUDE_PLUGIN_ROOT}', "$PWD")
$cmd
'{"hook_event_name":"UserPromptSubmit","prompt":"my ssn is 219-09-1234"}' | cmd /c $cmd
$LASTEXITCODE
```
