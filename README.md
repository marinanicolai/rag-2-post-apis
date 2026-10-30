```
   $t = "$env:TEMP\dlptest"; New-Item -ItemType Directory $t -Force | Out-Null
Set-Content "$t\one.txt" "SECURE FR"
Set-Content "$t\clean.txt" "hello world"
Compress-Archive "$t\one.txt" "$t\one-label.zip" -Force
Compress-Archive "$t\clean.txt" "$t\clean.zip" -Force
```
