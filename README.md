```
$m = "C:\temp\mp-test"
New-Item -ItemType Directory -Force "$m\.claude-plugin", "$m\copytest\.claude-plugin" | Out-Null
Set-Content "$m\.claude-plugin\marketplace.json" '{"name":"mp-test","owner":{"name":"test"},"plugins":[{"name":"copytest","source":"./copytest"}]}'
Set-Content "$m\copytest\.claude-plugin\plugin.json" '{"name":"copytest","version":"0.0.1"}'
Set-Content "$m\copytest\a.md" "hello"
Set-Content "$m\copytest\b.md" "Anything above RESTRICTED FR is denied."
cd C:\temp\c4g-test
claude plugin marketplace add C:\temp\mp-test
claude plugin install copytest@mp-test --scope project
```
