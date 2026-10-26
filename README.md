pip worked, but **it didn't replace anything**. The yellow warning says `vendor\yaml` already existed, probably empty from the earlier attempt, so pip skipped it. Clear it out and run again with `--upgrade`:

```powershell
Remove-Item -Recurse -Force vendor\yaml
pip install --target vendor --upgrade pyyaml
Remove-Item vendor\yaml\_yaml*.pyd -ErrorAction SilentlyContinue
```

The `.pyd` file is the compiled speed-up built for Python 3.14 only. Removing it leaves plain Python that runs on any version.

**Copy the license.** pip puts it in a separate folder next to `yaml`:
```powershell
Get-ChildItem vendor -Directory -Filter "pyyaml*dist-info" |
  Get-ChildItem -Recurse -Filter "LICENSE*" | Select-Object -First 1 |
  Copy-Item -Destination vendor\yaml\LICENSE
```

**Check:**
```powershell
(Get-ChildItem vendor\yaml -Filter *.py).Count
ls vendor
```
- The count should be **17**.
- `ls vendor` shows `yaml`, `pyyaml-6.0.3.dist-info`, maybe `_yaml`, and your `README.txt`. All of those can stay.

Ignore the pip upgrade notice.

Next, paste the `_ensure_yaml()` block into `client\__init__.py` and `app\__init__.py` if you haven't yet, and run the test:
```powershell
'{}' | python -I -S client\hook.py SessionStart
```
