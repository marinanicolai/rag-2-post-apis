

```powershell
Rename-Item '.\tests\test_bash_file_refs,py' 'test_bash_file_refs.py'
```

```powershell
Get-ChildItem .\tests\test_bash*
```

It should now show `test_bash_file_refs.py`.

Then run the new tests:

```powershell
python -m pytest tests\test_bash_file_refs.py -v
```

You should see **8 PASSED**.

The earlier full test run didn't include your 8 tests, because of the comma. So run the full suite once more too:

```powershell
python -m pytest tests -q 2>&1 | Select-Object -Last 2
```

If everything passes, commit and push:

```powershell
git add client/hook.py tests/test_bash_file_refs.py
git status
```

Only those two files should be under "Changes to be committed".

```powershell
git commit -m "Detect file paths inside quoted scripts and run scripts in Bash commands" -m "The Bash file-reference check treated a quoted one-liner as a single token, so a path inside it (for example python -c with zipfile on a labeled .docx) was never inspected. Paths inside tokens and inside scripts a command runs are now checked the same way. Adds tests in tests/test_bash_file_refs.py."
```

```powershell
git push -u origin fix/bash-embedded-paths
```

Then open the merge request with the description from before. Send me a photo of the 8 tests, and of the push if anything looks off.
