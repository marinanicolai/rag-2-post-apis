```
git add client\hook.py client\cowork.py
git commit -m "hook.py: handle Cowork shell tool, VM paths and dragged-in files"
```
```
Select-String -Path client\hook.py -Pattern "uploaded_files"
```
```
@'
import io
p = "client/hook.py"
lines = io.open(p, encoding="utf-8").read().split("\n")
i = next(n for n, l in enumerate(lines) if l.strip() == "if pack.settings.scan_prompt_file_refs:")
ind = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
eol = "\r" if lines[i].endswith("\r") else ""
block = [
    ind + "for i, p in enumerate(cowork.uploaded_files(prompt), start=1):",
    ind + "    p = _resolve(p, cwd)",
    ind + "    if os.path.isfile(p):",
    ind + "        add_file(inputs, p, pack, 100 + i)",
]
lines[i:i] = [b + eol for b in block]
io.open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("inserted block B above line", i + 1)
'@ | python -
```
