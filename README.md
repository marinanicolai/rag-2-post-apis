```
Add-Type -AssemblyName System.IO.Compression.FileSystem
$z = [IO.Compression.ZipFile]::OpenRead("C:\temp\c4g-test\word-labeled.docx")
$x = (New-Object IO.StreamReader($z.GetEntry("docProps/custom.xml").Open())).ReadToEnd(); $z.Dispose()
$v = ([regex]'_SiteId"\s*>\s*<vt:lpwstr>([^<]+)').Match($x).Groups[1].Value
$v | Set-Clipboard; "length: $($v.Length)"
```
