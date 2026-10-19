```
Copy-Item $env:USERPROFILE\.claude\settings.json $env:USERPROFILE\.claude\settings.before-installer.json
```
```
$code = @'
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
s = json.loads(p.read_text(encoding='utf-8'))
hooks = s.get('hooks', {})
removed = 0
for event in list(hooks):
    kept = [g for g in hooks[event] if not any('c4g-dlp-hooks-repo/client/hook.py' in h.get('command', '') for h in g.get('hooks', []))]
    removed += len(hooks[event]) - len(kept)
    if kept:
        hooks[event] = kept
    else:
        del hooks[event]
if not hooks:
    s.pop('hooks', None)
p.write_text(json.dumps(s, indent=2) + '\n', encoding='utf-8')
print('Removed', removed, 'manual DLP hook groups')
'@
python -c $code
```
