```
$p = "C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo\restrictions\PACK.md"
$t = [IO.File]::ReadAllText($p)
$t = $t.Replace('default_label: "ee3ed885-71ee-4006-b0ff-7ad0a5952b31"', 'default_label: "68bd301d-c681-4bd2-b9e4-03440f3370c0"')
[IO.File]::WriteAllText($p, $t, (New-Object Text.UTF8Encoding $false))
(Select-String $p -Pattern 'default_label: "68bd301d').Count
git diff --stat restrictions\PACK.md

```
