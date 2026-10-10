```
node --version
node -e "require('fs').copyFileSync(process.argv[1], process.argv[2]); console.log('guide copy ok')" "$src" "$env:TEMP\nodetest.md"
Set-Content "$env:TEMP\neutral.md" "hello"
node -e "require('fs').copyFileSync(process.argv[1], process.argv[2]); console.log('neutral copy ok')" "$env:TEMP\neutral.md" "$env:TEMP\neutral2.md"
```
