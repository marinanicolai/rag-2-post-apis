```
@'
import re, zipfile, pathlib, collections
pats = {
  "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
  "card": r"\b(?:\d[ -]?){15,16}\b",
  "aws_key": r"AKIA[0-9A-Z]{16}",
  "private_key": r"BEGIN [A-Z ]*PRIVATE KEY",
  "marking": r"(RESTRICTED|CONFIDENTIAL)[ _-]*\(?FR",
}
names = zipfile.ZipFile("dist/inference-hook-dlp.zip").namelist()
for n in names:
    p = pathlib.Path(n)
    if not p.is_file(): continue
    t = p.read_text(errors="ignore")
    hits = {k: len(re.findall(v, t)) for k, v in pats.items()}
    hits = {k: c for k, c in hits.items() if c}
    if hits: print(n, hits)
'@ | Set-Content $env:TEMP\scan_zip.py
python $env:TEMP\scan_zip.py
```

