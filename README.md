```
$z = [IO.Compression.ZipFile]::OpenRead("C:\temp\c4g-test\unmarked-autolabel.docx")
$x = (New-Object IO.StreamReader($z.GetEntry("docProps/custom.xml").Open())).ReadToEnd(); $z.Dispose()
[regex]::Matches($x, 'name="MSIP_Label_([0-9a-f-]+)_([^"]+)"\s*>\s*<vt:lpwstr>([^<]*)') | ForEach-Object {
  $val = $_.Groups[3].Value
  if ($_.Groups[2].Value -eq "SiteId") { $val = if ($val -eq $v) { "(matches tenant)" } else { "(MISMATCH)" } }
  "$($_.Groups[2].Value) = $val"
}
```
