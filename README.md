```
Get-ChildItem Cert:\LocalMachine\Root | Sort-Object Subject | Select-Object Subject, Thumbprint | Format-Table -Auto -Wrap
```
```
curl -v https://deb.nodesource.com 2>&1 | grep -i issuer
```
