

```
curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json

```
```
claude plugin marketplace add https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
claude plugin install skillhub-spike-test@litellm
```
```
Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache" -Recurse -Filter hello.py
```
```
   git add .
   git commit -m "Spike test v2, same version"
   git push
```
```
   claude plugin marketplace update litellm
   claude plugin update skillhub-spike-test@litellm
```
