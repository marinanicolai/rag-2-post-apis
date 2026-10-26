```
#!/usr/bin/env python
"""Generate hooks/hooks.json (Windows host / Cowork) and hooks/hooks.posix.json.

    python scripts/make_hooks_json.py          # rewrite both files
    python scripts/make_hooks_json.py --check  # exit 1 if the committed files are stale

Why generated: in the Claude desktop app (Cowork) plugin hooks run on the Windows
host. The command must start powershell.exe, find the plugin folder and run
scripts/dlp_hook_launcher.ps1, and it has to survive whichever shell the app uses
to run it (cmd.exe, Git Bash, or a direct exec) without "$" or quotes being
re-interpreted. -EncodedCommand (base64 UTF-16LE) contains neither, so the
readable bootstrap below is encoded once per event here.

The bootstrap finds the plugin folder from CLAUDE_PLUGIN_ROOT (exported to plugin
hooks), then a cached root, then a search of the app's plugin folders; it loads the
launcher with [scriptblock]::Create so a policy that blocks .ps1 files does not
stop it; it fails closed (exit 2 on UserPromptSubmit / PreToolUse) when the plugin
folder cannot be found, unless DLP_FAIL_MODE=open.
"""

from __future__ import annotations

import base64
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOTSTRAP = r"""
$ErrorActionPreference = 'SilentlyContinue'
$ev = '__EVENT__'
$launcher = 'scripts/dlp_hook_launcher.ps1'
$base = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { [IO.Path]::GetTempPath() }
$state = Join-Path $base 'inference-hook-dlp'
$cache = Join-Path $state 'root.txt'
$r = $env:CLAUDE_PLUGIN_ROOT
if (-not $r -or -not (Test-Path -LiteralPath (Join-Path $r $launcher))) {
  $r = $null
  if (Test-Path -LiteralPath $cache) {
    $c = ([IO.File]::ReadAllText($cache)).Trim()
    if ($c -and (Test-Path -LiteralPath (Join-Path $c $launcher))) { $r = $c }
  }
}
if (-not $r) {
  $roots = @()
  foreach ($b in @($env:LOCALAPPDATA, $env:APPDATA)) { if ($b) { $roots += @(Get-ChildItem -Path $b -Filter 'Claude*' -Directory) } }
  if ($env:USERPROFILE) { $roots += @(Get-Item -LiteralPath (Join-Path $env:USERPROFILE '.claude')) }
  $hit = $roots | Where-Object { $_ } | ForEach-Object { Get-ChildItem -LiteralPath $_.FullName -Recurse -Depth 10 -File -Filter 'dlp_hook_launcher.ps1' } |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.Directory.Parent.FullName 'client/hook.py') } |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($hit) {
    $r = $hit.Directory.Parent.FullName
    [void](New-Item -ItemType Directory -Force -Path $state)
    [IO.File]::WriteAllText($cache, $r)
  }
}
if (-not $r) {
  $open = ("" + $env:DLP_FAIL_MODE).Trim().ToLower() -eq 'open'
  if ($ev -eq 'SessionStart') {
    [Console]::Out.Write('{"systemMessage":"inference-hook-dlp: plugin folder not found on this computer; hooks cannot run."}')
    exit 0
  }
  if (($ev -eq 'UserPromptSubmit' -or $ev -eq 'PreToolUse') -and -not $open) {
    [Console]::Error.Write('Claude usage restrictions could not be checked (plugin folder not found), so this action is blocked (fail mode closed).')
    exit 2
  }
  exit 0
}
$ErrorActionPreference = 'Stop'
& ([scriptblock]::Create([IO.File]::ReadAllText((Join-Path $r $launcher)))) -Root $r -HookEvent $ev
exit $LASTEXITCODE
"""

TOOL_MATCHER = "Read|Edit|Write|MultiEdit|NotebookEdit|Bash|Grep|Glob|WebFetch|WebSearch|Task|Agent|mcp__.*"
POST_MATCHER = "Read|Bash|Grep|WebFetch|mcp__.*"  # mcp__.* includes Cowork's mcp__workspace__bash

EVENTS = [
    # (event, matcher or None, timeout seconds, status message)
    ("SessionStart", None, 60, "Loading usage restrictions"),
    ("UserPromptSubmit", None, 40, "Checking prompt against usage restrictions"),
    ("PreToolUse", TOOL_MATCHER, 50, "Checking tool input against usage restrictions"),
    ("PostToolUse", POST_MATCHER, 50, None),
]


def encoded(event: str) -> str:
    script = BOOTSTRAP.replace("__EVENT__", event).strip()
    return base64.b64encode(script.encode("utf-16-le")).decode("ascii")


def build(windows: bool) -> dict:
    hooks: dict = {}
    for event, matcher, timeout, status in EVENTS:
        if windows:
            cmd = ("powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass "
                   f"-EncodedCommand {encoded(event)}")
        else:
            cmd = f'python3 "${{CLAUDE_PLUGIN_ROOT}}/client/hook.py" {event}'
        h: dict = {"type": "command", "command": cmd, "timeout": timeout}
        if status:
            h["statusMessage"] = status
        entry: dict = {"hooks": [h]}
        if matcher:
            entry = {"matcher": matcher, **entry}
        hooks[event] = [entry]
    desc = ("inference-hook-dlp hooks for the Windows host (Claude desktop app / Cowork, Claude Code on Windows). "
            "Each command is scripts/make_hooks_json.py's bootstrap, base64-encoded; it runs scripts/dlp_hook_launcher.ps1."
            if windows else
            "inference-hook-dlp hooks for macOS/Linux Claude Code hosts (calls python3 directly).")
    return {"description": desc, "hooks": hooks}


def main(argv: list[str]) -> int:
    check = "--check" in argv
    stale = []
    for name, windows in (("hooks.json", True), ("hooks.posix.json", False)):
        path = os.path.join(ROOT, "hooks", name)
        text = json.dumps(build(windows), indent=2) + "\n"
        if check:
            try:
                current = open(path, encoding="utf-8").read()
            except OSError:
                current = ""
            if current != text:
                stale.append(name)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"wrote {os.path.relpath(path, ROOT)}")
    if stale:
        print("stale: " + ", ".join(stale) + " (run python scripts/make_hooks_json.py)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```
