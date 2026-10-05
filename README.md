```
$p = "C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo\restrictions\PACK.md"
$t = [IO.File]::ReadAllText($p)
$t = $t.Replace('site_id: "custom.xml"', "site_id: `"$v`"")
[IO.File]::WriteAllText($p, $t, (New-Object Text.UTF8Encoding $false))
(Select-String $p -Pattern 'site_id: "[0-9a-f-]{36}"').Count
```
