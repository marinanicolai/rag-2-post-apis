```
    $err = $r.Err
    if ($r.Code -eq 2 -and $err -and -not $err.StartsWith('inference-hook-dlp')) { $err = 'inference-hook-dlp: ' + $err }
    Write-Raw ([Console]::OpenStandardError()) $err
```
