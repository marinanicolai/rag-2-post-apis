```
$zip = "$HOME\Desktop\inference-hook-dlp.zip"
Test-Path $zip
(Get-Acl $zip).Access | Select-Object IdentityReference, FileSystemRights, AccessControlType
```
