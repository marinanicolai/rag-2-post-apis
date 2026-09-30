

```
(Get-Content .claude-plugin\plugin.json) -replace '"0.1.0"', '"0.2.0"' | Set-Content .claude-plugin\plugin.json
```
```
Get-Content .claude-plugin\plugin.json
```
```
git add .
git commit -m "Spike test, bump to 0.2.0"
git push
claude plugin marketplace update litellm
claude plugin update skillhub-spike-test@litellm
```
