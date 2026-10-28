```
git switch -c fix/slim-cowork-zip
code scripts\build_zip.py
```
```
skip_files = {
    "restrictions/tests.yaml", "config/rules_tests.yaml",
    "scripts/make_sample_files.py", "scripts/zscaler_probe.py",
    "scripts/proxy_selftest.py", "scripts/send_sample.py", "scripts/smoke_test.py",
}
```
```
                full = os.path.join(d, f)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                if rel in skip_files:
                    continue
                zf.write(full, rel); n += 1
```
