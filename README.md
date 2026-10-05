```
$z = [IO.Compression.ZipFile]::OpenRead("C:\temp\c4g-test\word-labeled.docx")
$z.Entries | Where-Object FullName -like "word/header*" | ForEach-Object {
  $t = (New-Object IO.StreamReader($_.Open())).ReadToEnd() -replace '<[^>]+>', ''
  "$($_.FullName): $($t.Trim())"
}
$z.Dispose()
```
