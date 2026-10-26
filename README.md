```
@'
import io
p = "scripts/make_hooks_json.py"
lines = io.open(p, encoding="utf-8").read().split("\n")
eol = "\r" if lines[0].endswith("\r") else ""
lines = [l.rstrip("\r") for l in lines]
f = next(n for n, l in enumerate(lines) if l.strip().startswith("for event, matcher, timeout, status in EVENTS"))
ind = lines[f][: len(lines[f]) - len(lines[f].lstrip())] + "    "
i = next(n for n in range(f, len(lines)) if lines[n].strip() == "if windows:")
j = next(n for n in range(i, len(lines)) if lines[n].strip() == "else:")
posix = lines[j + 1].strip()
new = [
    ind + "if windows:",
    ind + "    cmd = ('powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass '",
    ind + "           '-File \"${CLAUDE_PLUGIN_ROOT}/scripts/dlp_hook_launcher.ps1\" '",
    ind + "           '-Root \"${CLAUDE_PLUGIN_ROOT}\" -HookEvent ' + event)",
    ind + "else:",
    ind + "    " + posix,
]
lines[i : j + 2] = new
io.open(p, "w", encoding="utf-8", newline="").write("\n".join(l + eol for l in lines[:-1]) + lines[-1])
print("fixed lines", i + 1, "to", j + 2)
'@ | python -
python -c "import ast; ast.parse(open('scripts/make_hooks_json.py', encoding='utf-8').read()); print('OK')"
```
