```
@'
import io, re
p = "client/hook.py"
src = io.open(p, encoding="utf-8").read()
lines = src.split("\n")
start = next(i for i, l in enumerate(lines) if l.strip() == "elif tool in cowork.SHELL_TOOLS:")
end = next(i for i in range(start, len(lines)) if "add_file(inputs, p, pack, i)" in lines[i])
base = lines[start][: len(lines[start]) - len(lines[start].lstrip())]
b, bb = base + "    ", base + "        "
block = [
    lines[start].rstrip(),
    b + 'cmd = tool_input.get("command")',
    b + "cmd = cmd if isinstance(cmd, str) else _json_text(tool_input)",
    b + 'inputs.segments.append(_text_segment("tool_use", "assistant", cmd, tool_name=tool))',
    b + 'if tool == "mcp__workspace__bash":',
    bb + "refs = cowork.shell_refs(cmd, cwd, pack.settings.bash_max_files, _state_dir())",
    b + "else:",
    bb + "refs = _bash_file_refs(cmd, cwd, pack.settings.bash_max_files)",
    b + "for i, p in enumerate(refs, start=1):",
    bb + "add_file(inputs, p, pack, i)",
]
eol = "\r" if lines[start].endswith("\r") else ""
lines[start : end + 1] = [l + eol for l in block]
io.open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("rewrote lines", start + 1, "to", end + 1)
'@ | python -
```
