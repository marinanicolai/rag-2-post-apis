```
   $dst  = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\classification.py"
   $rule = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\restrictions\restricted-paths.md"
   Copy-Item "$dst.bak" $dst -Force
   Copy-Item "$rule.bak" $rule -Force
```
```
   Summarize this record: Jane Testperson, SSN 123-45-6789
```
```
   function Last($n = 1) { Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail $n | ConvertFrom-Json | Format-List }
   Last
```
