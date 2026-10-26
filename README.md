```
 python -c "import ast; ast.parse(open('client/hook.py', encoding='utf-8').read())"
```
```
'{}' | python client\hook.py SessionStart
```
```
$task = Join-Path $env:TEMP 'cw6\task1'
New-Item -ItemType Directory -Force "$task\host-cwd", "$task\uploads" | Out-Null
"name,ssn`r`nAda,219-09-1234" | Set-Content "$task\uploads\roster.txt"
$cwd = "$task\host-cwd"
function T($label, $obj) {
  $obj | ConvertTo-Json -Compress -Depth 5 | python client\hook.py $obj.hook_event_name | Out-Null
  "{0,-38} exit {1}" -f $label, $LASTEXITCODE
}
T 'shell cat upload (want 2)'        @{ hook_event_name='PreToolUse'; cwd=$cwd; tool_name='mcp__workspace__bash'; tool_input=@{ command='cat /sessions/abc/mnt/uploads/roster.txt' } }
T 'python -c open() (want 2)'        @{ hook_event_name='PreToolUse'; cwd=$cwd; tool_name='mcp__workspace__bash'; tool_input=@{ command="python3 -c `"print(open('/sessions/abc/mnt/uploads/roster.txt').read())`"" } }
T 'cd then relative (want 2)'        @{ hook_event_name='PreToolUse'; cwd=$cwd; tool_name='mcp__workspace__bash'; tool_input=@{ command='cd /sessions/abc/mnt/uploads && wc -l roster.txt' } }
T 'dragged-in file (want 2)'         @{ hook_event_name='UserPromptSubmit'; cwd=$cwd; prompt="<uploaded_files><file><file_path>$task\uploads\roster.txt</file_path></file></uploaded_files>`nSummarize" }
T 'harmless shell (want 0)'          @{ hook_event_name='PreToolUse'; cwd=$cwd; tool_name='mcp__workspace__bash'; tool_input=@{ command='echo hello' } }
```
