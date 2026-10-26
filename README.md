```
if windows:
            cmd = ('powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass '
                   '-File "${CLAUDE_PLUGIN_ROOT}/scripts/dlp_hook_launcher.ps1" '
                   '-Root "${CLAUDE_PLUGIN_ROOT}" -HookEvent ' + event)
```
