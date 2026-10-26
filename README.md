## How to test (before and after)

Run in PowerShell from the repo root. No Claude or Word needed: this sends the hook the same kind of Bash command Claude used.

### 1. Set up a test file
Create a text file whose first line is a marking above the ceiling (any marking above INTERNAL FR from `DEFAULT_LADDER` in `client/classification.py`). Fake content only.

    $dir = "$env:TEMP\dlp-mr-test"
    New-Item -ItemType Directory -Force $dir | Out-Null
    Set-Content "$dir\memo.txt" "<MARKING ABOVE CEILING>`r`nTest memo. Fake content only."

Build the hook input: a Python one-liner that reads the file (the path is inside the quoted script):

    $cmd = "python -c `"print(open(r'$dir\memo.txt').read())`""
    $in = @{hook_event_name="PreToolUse"; session_id="mr-test"; cwd=$dir; tool_name="Bash"; tool_input=@{command=$cmd}} | ConvertTo-Json -Compress

### 2. Before: on main (bug)

    git fetch origin
    git switch --detach origin/main
    $in | python .\client\hook.py PreToolUse
    $LASTEXITCODE

Expected: no block message, exit code **0**. The command would run and read the file.

### 3. After: on this branch (fixed)

    git switch fix/bash-embedded-paths
    $in | python .\client\hook.py PreToolUse
    $LASTEXITCODE

Expected: "Blocked Bash of ...\memo.txt: ..." (classification-ceiling), exit code **2**.

### 4. Control: plain path (should block on both)

    $in2 = @{hook_event_name="PreToolUse"; session_id="mr-test"; cwd=$dir; tool_name="Bash"; tool_input=@{command="type $dir\memo.txt"}} | ConvertTo-Json -Compress
    $in2 | python .\client\hook.py PreToolUse
    $LASTEXITCODE

Expected: exit code **2** on both main and this branch. Plain paths were already detected; only paths inside quoted scripts were missed.

### 5. Unit tests (on this branch)

    python -m pytest tests\test_bash_file_refs.py -v
    python -m pytest tests 2>&1 | Select-Object -Last 1

Expected: 8 passed; full suite passes.

### 6. Clean up

    Remove-Item $dir -Recurse -Force

### Results (Marina, 2026-10-25)
| Step | main | this branch |
|---|---|---|
| One-liner (step 2/3) | exit 0, allowed | exit 2, blocked |
| Plain path (step 4) | exit 2 | exit 2 |
| Unit tests (step 5) | n/a | 8 passed |
| In Claude (Code tab, dev build) | Bash `allow`, file text reached the model | `PreToolUse deny classification-ceiling Bash` (14:51:12) |
