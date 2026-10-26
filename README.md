```
  ## Run the DLP hooks in Cowork (Claude desktop app)

The hooks worked in Claude Code but never ran in Cowork. This branch fixes the five root causes and was tested end to end in Cowork on 2026-10-26.

### Root causes → fixes

| # | Problem in Cowork | Fix |
|---|---|---|
| 1 | Hooks lived in `.claude/settings.json`, which Cowork never reads | Ship them in the plugin's `hooks/hooks.json`; install the plugin by uploading the zip (Customize → Plugins) |
| 2 | Hard-coded `C:/Users/...` paths | `${CLAUDE_PLUGIN_ROOT}` (Cowork substitutes it) |
| 3 | Bare `python`: if not found, the hook errors and Claude carries on (fail open) | `scripts/dlp_hook_launcher.ps1` finds a real Python 3.10+ (Anaconda, python.org, `py -3`, PATH; never the Store alias) and **fails closed** (exit 2) if none, on crash or on timeout. `DLP_FAIL_MODE=open` overrides. Log: `%LOCALAPPDATA%\inference-hook-dlp\launcher.log` |
| 4 | `client/pack.py` and `app/rules.py` import PyYAML at load, so the hook crashes on machines without it | Pure-Python PyYAML 6.0.3 bundled in `vendor/` (MIT), used only when the host has none (`_ensure_yaml()` in `client/__init__.py`, `app/__init__.py`) |
| 5 | Cowork's shell is `mcp__workspace__bash` with VM paths (`/sessions/<id>/mnt/...`); dragged-in files arrive in an `<uploaded_files>` block. Hook looked for VM paths on the host, found nothing, allowed | New `client/cowork.py` maps VM paths to host paths (task uploads/outputs, connected folders learned from Read calls or found under Downloads/Documents/Desktop/OneDrive). `hook.py` treats `mcp__workspace__bash` like `Bash`, finds VM paths inside quoted code and after `cd`, and checks every file in `<uploaded_files>` |

Also:
- `hook.py` accepts `--stdin-file` (used by the launcher)
- Block messages start with `inference-hook-dlp:`
- The hook command is short and readable, so Cowork's banner shows the reason instead of the command filling it

### Files
- New: `hooks/hooks.posix.json`, `scripts/dlp_hook_launcher.ps1`, `scripts/make_hooks_json.py` (generates both hooks files; don't edit `hooks.json` by hand), `scripts/build_zip.py`, `client/cowork.py`, `vendor/`
- Changed: `hooks/hooks.json`, `client/hook.py`, `client/__init__.py`, `app/__init__.py`
- `.gitignore`: `dist/`

Build the upload zip with `python scripts/build_zip.py` → `dist/inference-hook-dlp.zip`.

### Test evidence (Cowork, Claude-3p desktop app, Windows 11)
Decision log `%LOCALAPPDATA%\inference-hook-dlp\client-decisions.jsonl`, rows with `cwd` under `local-agent-mode-sessions`:

| Case | Result |
|---|---|
| New task | `SessionStart` loaded pack frb-baseline, 12 rules |
| Typed prompt with an SSN | `UserPromptSubmit deny pii-ssn`, banner shows `inference-hook-dlp: Prompt blocked: ...` |
| Dragged-in file with an SSN | `UserPromptSubmit deny pii-ssn` |
| `cat` on a working-folder file via the shell | `PreToolUse mcp__workspace__bash deny pii-ssn` |
| Normal prompt / harmless shell commands | `allow` |

Local: `pytest tests/test_zscaler_spec.py` passes; the launcher was tested through the generated `hooks.json` commands (allow → 0, deny → 2, no Python → fail closed).

### Known limitations / follow-ups
- **Chat tab is not covered.** Plugin hooks never run there; that needs Purview/Zscaler or a server-side hook.
- The launcher runs with `-File`. That works where the PowerShell execution policy is not set by GPO (MachinePolicy/UserPolicy `Undefined`, as on the test machine). Testers on stricter machines: check `Get-ExecutionPolicy -List`.
- A shell command on a connected folder the hook cannot locate is currently allowed (PostToolUse still flags the output). Making it fail closed is a possible follow-up.
- `classification-label-required` blocks every unlabelled file, including plain text; one `classification-ceiling` prompt deny (09:43) needs a look for false positives.
- Existing Claude Code installs that run hooks from `~/.claude/settings.json` should remove that block once the plugin is installed, or the checks run twice.
```
