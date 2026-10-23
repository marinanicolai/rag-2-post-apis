

```powershell
Get-ChildItem .\tests\test_bash*
```

- If it shows `test_bash_file_refs.py`, it's fine.
- If it shows `test_bash_file_refs,py`, rename it:
  ```powershell
  Rename-Item .\tests\test_bash_file_refs,py test_bash_file_refs.py
  ```

**Before committing, run the two checks:**

```powershell
python -m pytest tests\test_bash_file_refs.py -v
```

You should see **8 PASSED**.

```powershell
$cmd = 'python -c "import zipfile; print(zipfile.ZipFile(r''C:\Users\M3MXN08\Documents\confidential-test.docx'').read(''word/document.xml'')[:200])"'
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Bash"; tool_input=@{command=$cmd}} | ConvertTo-Json -Compress
$in | python .\client\hook.py PreToolUse
$LASTEXITCODE
```


