```
@'
import json, os, zipfile
root = os.getcwd()
name = json.load(open(".claude-plugin/plugin.json", encoding="utf-8"))["name"]
include = [".claude-plugin", "hooks", "client", "app", "restrictions", "vendor", "scripts", "skills", "config"]
skip_dirs = {"__pycache__", ".pytest_cache"}
os.makedirs("dist", exist_ok=True)
out = os.path.join("dist", name + ".zip")
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for top in include:
        if not os.path.exists(top):
            print("skip (not in repo):", top); continue
        for d, dirs, files in os.walk(top):
            dirs[:] = [x for x in dirs if x not in skip_dirs]
            for f in files:
                if f.endswith((".pyc", ".log", ".jsonl")):
                    continue
                full = os.path.join(d, f)
                zf.write(full, os.path.relpath(full, root).replace(os.sep, "/")); n += 1
print("wrote", out, "with", n, "files")
'@ | python -
```
