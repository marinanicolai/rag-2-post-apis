```
$cert = Get-ChildItem Cert:\LocalMachine\Root | Where-Object { $_.Subject -match 'Zscaler' } | Select-Object -First 1
if ($cert) {
  Export-Certificate -Cert $cert -FilePath $env:USERPROFILE\zscaler.cer | Out-Null
  certutil -encode $env:USERPROFILE\zscaler.cer $env:USERPROFILE\zscaler-root-ca.crt
  Write-Host "Exported: $($cert.Subject)"
} else {
  Write-Host "No Zscaler cert found"
}
```
```
docker cp $env:USERPROFILE\zscaler-root-ca.crt e38d5b322416:/usr/local/share/ca-certificates/zscaler-root-ca.crt
```
