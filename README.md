```
Select-String -Path client\hook.py -Pattern "UserPromptSubmit|PreToolUse|classif|file_name|filename" | Select-Object LineNumber, Line
```
```
Select-String -Path client\classification.py -Pattern "def |file_name|filename|ceiling" | Select-Object LineNumber, Line
```
