That worked: PyYAML 6.0.3 installed into `vendor` from your internal mirror, with no warning this time. The license copy ran silently, which is normal when it succeeds.

**1. Check the files:**
```powershell
(Get-ChildItem vendor\yaml -Filter *.py).Count
Test-Path vendor\yaml\LICENSE
Test-Path vendor\yaml\_yaml*.pyd
```
You should get **17**, **True**, **False** (the `.pyd` is gone).

**2. Paste the `_ensure_yaml()` block** into `client\__init__.py` (above the first `from client import` line) and at the end of `app\__init__.py`, if you haven't already. It's the block from my earlier message, starting with `def _ensure_yaml() -> None:`.

**3. Run the test.** `-S` hides your installed packages, so this only passes if the `vendor` copy is used:
```powershell
'{}' | python -I -S client\hook.py SessionStart
```
✅ You should see JSON containing **"Organization usage restrictions are active"**.

**4. If it passes, commit:**
```powershell
git add vendor client\__init__.py app\__init__.py
git commit -m "Bundle pure-Python PyYAML so hooks run without pip packages"
```

Send me the step 3 output.
