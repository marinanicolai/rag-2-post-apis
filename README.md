
```
Add-Type -AssemblyName System.IO.Compression.FileSystem
$z = [IO.Compression.ZipFile]::OpenRead("C:\temp\c4g-test\agenda.docx")
$z.Entries | Where-Object { $_.FullName -like "word/header*" -or $_.FullName -eq "word/document.xml" } | ForEach-Object {
  $t = (New-Object IO.StreamReader($_.Open())).ReadToEnd() -replace '<[^>]+>', ' ' -replace '\s+', ' '
  "$($_.FullName): $($t.Trim())"
}
$z.Dispose()
```
