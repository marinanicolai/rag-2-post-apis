

```powershell
$hook = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\hook.py"
```

```powershell
Test-Path $hook
```

It should say **True**.

```powershell
$in | python $hook PreToolUse
```

```powershell
$LASTEXITCODE
```

`$in` is still saved from before, so you don't need to type it again. Send me a photo of the output.
