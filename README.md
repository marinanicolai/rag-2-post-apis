```
 python scripts\build_zip.py
git add scripts hooks
git commit -m "Short readable hook command so Cowork's block banner shows the plugin name and reason"
```
```
   python -c "import ast; ast.parse(open('scripts/make_hooks_json.py', encoding='utf-8').read()); print('OK')"
   python scripts\make_hooks_json.py
   $h = Get-Content -Raw hooks\hooks.json | ConvertFrom-Json
   $cmd = $h.hooks.UserPromptSubmit[0].hooks[0].command.Replace('${CLAUDE_PLUGIN_ROOT}', "$PWD")
   $cmd
   '{"hook_event_name":"UserPromptSubmit","prompt":"my ssn is 219-09-1234"}' | cmd /c $cmd
   $LASTEXITCODE
```
