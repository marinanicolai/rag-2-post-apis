

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
```
Get-Content "$env:USERPROFILE\.claude\plugins\cache\litellm\skillhub-spike-test\0.1.0\scripts\hello.py"
```
```
claude plugin uninstall skillhub-spike-test@litellm
claude plugin install skillhub-spike-test@litellm
Get-Content "$env:USERPROFILE\.claude\plugins\cache\litellm\skillhub-spike-test\0.1.0\scripts\hello.py"
```
```
git add .
git commit -m "Spike test, bump to 0.2.0"
git push
claude plugin marketplace update litellm
claude plugin update skillhub-spike-test@litellm
```
```
