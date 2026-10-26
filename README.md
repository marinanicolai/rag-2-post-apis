```
# inference-hook-dlp: Windows host launcher for the Claude desktop app (Cowork) and Claude Code.
#
# The Claude desktop app runs plugin hooks on the Windows HOST, not inside the Linux task VM,
# so "python3 ..." in hooks.json either does not exist or hits the Microsoft Store alias, the
# hook errors out, and the runtime treats an errored hook as "allow" (silent fail open).
#
# hooks/hooks.json starts powershell.exe with a small encoded bootstrap that locates the plugin
# folder and runs THIS file as a script block (so a Group Policy that forbids .ps1 files does not
# stop it). This launcher:
#   1. saves the hook JSON from stdin to a temp file (raw bytes),
#   2. finds a real CPython >= 3.10 (DLP_HOOK_PYTHON, cached choice, Anaconda/Miniconda,
#      python.org installs, the py launcher, python.exe on PATH; never ...\WindowsApps\...),
#   3. runs client\hook.py <event> --stdin-file <temp> and relays stdout, stderr and exit code,
#   4. FAILS CLOSED (exit 2 for UserPromptSubmit / PreToolUse) when no interpreter is usable or
#      the hook times out, unless DLP_FAIL_MODE=open.
#
# State and diagnostics: %LOCALAPPDATA%\inference-hook-dlp\  (python.txt, launcher.log)
# Paths use '/' so the same file can be exercised with pwsh on Linux (tests); Windows accepts both.
# Delete python.txt to force interpreter re-discovery.

param(
    [Parameter(Mandatory = $true)][string]$Root,
    [Parameter(Mandatory = $true)][string]$HookEvent
)

$ErrorActionPreference = 'Stop'

$Budgets = @{ 'SessionStart' = 40000; 'UserPromptSubmit' = 25000; 'PreToolUse' = 35000; 'PostToolUse' = 35000 }
$HookTimeoutMs = if ($Budgets.ContainsKey($HookEvent)) { $Budgets[$HookEvent] } else { 25000 }
$ProbeTimeoutMs = 10000

$base = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { [IO.Path]::GetTempPath() }
$StateDir = Join-Path $base 'inference-hook-dlp'
try { [void](New-Item -ItemType Directory -Force -Path $StateDir) } catch { }
$LogPath = Join-Path $StateDir 'launcher.log'
$CachePath = Join-Path $StateDir 'python.txt'
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Write-Log([string]$msg) {
    try {
        if ((Test-Path -LiteralPath $LogPath) -and ((Get-Item -LiteralPath $LogPath).Length -gt 1MB)) {
            Move-Item -LiteralPath $LogPath -Destination ($LogPath + '.1') -Force
        }
        $line = '{0} [{1}] pid={2} {3}' -f (Get-Date).ToUniversalTime().ToString('o'), $HookEvent, $PID, $msg
        [IO.File]::AppendAllText($LogPath, $line + [Environment]::NewLine, $Utf8)
    } catch { }
}

function Write-Raw([IO.Stream]$stream, [string]$text) {
    if (-not $text) { return }
    $bytes = $Utf8.GetBytes($text)
    $stream.Write($bytes, 0, $bytes.Length)
    $stream.Flush()
}

function Exit-FailClosed([string]$why) {
    Write-Log ("FAIL: " + $why)
    $mode = ("" + $env:DLP_FAIL_MODE).Trim().ToLower()
    $stdout = [Console]::OpenStandardOutput()
    $stderr = [Console]::OpenStandardError()
    if ($HookEvent -eq 'SessionStart') {
        $note = "inference-hook-dlp cannot run on this computer ($why). " +
                $(if ($mode -eq 'open') { 'Fail mode is open: actions are NOT being checked.' }
                  else { 'Every prompt and tool call will be blocked until this is fixed.' }) +
                " See $LogPath."
        $obj = @{ systemMessage = $note; hookSpecificOutput = @{ hookEventName = 'SessionStart'; additionalContext = $note } }
        Write-Raw $stdout (ConvertTo-Json $obj -Compress -Depth 4)
        exit 0
    }
    if (($HookEvent -eq 'UserPromptSubmit' -or $HookEvent -eq 'PreToolUse') -and $mode -ne 'open') {
        Write-Raw $stderr ("Claude usage restrictions could not be checked ($why), so this action is blocked " +
                           "(fail mode closed). Ask your administrator; details in $LogPath.")
        exit 2
    }
    exit 0
}

function Format-Arg([string]$a) {
    # Quote for the Windows command-line parser (CommandLineToArgvW rules).
    if ($a -eq '') { return '""' }
    if ($a -notmatch '[\s"]') { return $a }
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.Append('"')
    $bs = 0
    foreach ($ch in $a.ToCharArray()) {
        if ($ch -eq '\') { $bs++; continue }
        if ($ch -eq '"') { [void]$sb.Append('\' * (2 * $bs + 1)); [void]$sb.Append('"'); $bs = 0; continue }
        if ($bs) { [void]$sb.Append('\' * $bs); $bs = 0 }
        [void]$sb.Append($ch)
    }
    if ($bs) { [void]$sb.Append('\' * (2 * $bs)) }
    [void]$sb.Append('"')
    return $sb.ToString()
}

function Invoke-Proc([string]$file, [string[]]$argv, [int]$timeoutMs) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $file
    $psi.Arguments = (($argv | ForEach-Object { Format-Arg $_ }) -join ' ')
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $true
    $psi.StandardOutputEncoding = $Utf8
    $psi.StandardErrorEncoding = $Utf8
    $psi.EnvironmentVariables['PYTHONIOENCODING'] = 'utf-8'
    $psi.EnvironmentVariables['PYTHONUTF8'] = '1'
    $psi.EnvironmentVariables['CLAUDE_PLUGIN_ROOT'] = $Root
    $p = [System.Diagnostics.Process]::Start($psi)
    $p.StandardInput.Close()
    $outTask = $p.StandardOutput.ReadToEndAsync()
    $errTask = $p.StandardError.ReadToEndAsync()
    if (-not $p.WaitForExit($timeoutMs)) {
        try { $p.Kill() } catch { }
        return @{ TimedOut = $true; Code = -1; Out = ''; Err = '' }
    }
    $p.WaitForExit()
    return @{ TimedOut = $false; Code = $p.ExitCode; Out = $outTask.Result; Err = $errTask.Result }
}

function Test-Python([string]$exe, [string[]]$extra) {
    if (-not $exe) { return $false }
    if ($exe -match '\\WindowsApps\\') { return $false }
    if (($exe -match '[\\/]') -and -not (Test-Path -LiteralPath $exe)) { return $false }
    try {
        $r = Invoke-Proc $exe ($extra + @('-c', 'import sys,zipfile,zlib,json; sys.exit(0 if sys.version_info >= (3, 10) else 3)')) $ProbeTimeoutMs
        return (-not $r.TimedOut) -and $r.Code -eq 0
    } catch { return $false }
}

function Split-Spec([string]$spec) {
    $parts = $spec.Split('|')
    $extra = @()
    if ($parts.Length -gt 1 -and $parts[1].Trim()) { $extra = @($parts[1].Trim() -split '\s+') }
    return @{ Exe = $parts[0].Trim(); Extra = $extra }
}

function Find-Python {
    # Fast path: a cached choice whose executable still exists is trusted without a probe
    # (a probe costs one extra Python start per hook). Delete python.txt to re-probe.
    if (-not $env:DLP_HOOK_PYTHON -and (Test-Path -LiteralPath $CachePath)) {
        try {
            $s = Split-Spec (([IO.File]::ReadAllText($CachePath)).Trim())
            if ($s.Exe -and (Test-Path -LiteralPath $s.Exe) -and $s.Exe -notmatch '\\WindowsApps\\') { return $s }
        } catch { }
    }
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($env:DLP_HOOK_PYTHON) { $candidates.Add($env:DLP_HOOK_PYTHON) }
    if (Test-Path -LiteralPath $CachePath) {
        try { $candidates.Add(([IO.File]::ReadAllText($CachePath)).Trim()) } catch { }
    }
    $fixed = @()
    foreach ($b in @($env:USERPROFILE, $env:LOCALAPPDATA, $env:ProgramData)) {
        if (-not $b) { continue }
        foreach ($n in @('anaconda3', 'Anaconda3', 'miniconda3', 'Miniconda3')) { $fixed += (Join-Path (Join-Path $b $n) 'python.exe') }
    }
    foreach ($f in $fixed) { if (Test-Path -LiteralPath $f) { $candidates.Add($f) } }
    $globs = @()
    if ($env:LOCALAPPDATA) { $globs += (Join-Path $env:LOCALAPPDATA 'Programs/Python/Python3*/python.exe') }
    if ($env:ProgramFiles) { $globs += (Join-Path $env:ProgramFiles 'Python3*/python.exe') }
    foreach ($glob in $globs) {
        try { Get-ChildItem -Path $glob -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | ForEach-Object { $candidates.Add($_.FullName) } } catch { }
    }
    $py = Get-Command py.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($py) { $candidates.Add($py.Source + '|-3') }
    foreach ($n in @('python.exe', 'python3.exe')) {
        Get-Command $n -All -ErrorAction SilentlyContinue | ForEach-Object { $candidates.Add($_.Source) }
    }
    $seen = @{}
    foreach ($spec in $candidates) {
        if (-not $spec -or $seen.ContainsKey($spec)) { continue }
        $seen[$spec] = $true
        $s = Split-Spec $spec
        if (Test-Python $s.Exe $s.Extra) {
            try { [IO.File]::WriteAllText($CachePath, $spec, $Utf8) } catch { }
            Write-Log ("interpreter: " + $spec)
            return $s
        }
        Write-Log ("rejected interpreter: " + $spec)
    }
    return $null
}

# ---------------------------------------------------------------------------- main

$tmp = $null
try {
    $hookPy = Join-Path (Join-Path $Root 'client') 'hook.py'
    if (-not (Test-Path -LiteralPath $hookPy)) { Exit-FailClosed "client/hook.py not found under $Root" }

    $tmp = Join-Path ([IO.Path]::GetTempPath()) ('dlp-hook-' + [Guid]::NewGuid().ToString('N') + '.json')
    $in = [Console]::OpenStandardInput()
    $ms = New-Object IO.MemoryStream
    $in.CopyTo($ms)
    [IO.File]::WriteAllBytes($tmp, $ms.ToArray())

    $python = Find-Python
    if (-not $python) { Exit-FailClosed 'no usable Python 3.10+ found (set DLP_HOOK_PYTHON to the full path of python.exe)' }

    $argv = @($python.Extra) + @('-I', '-X', 'utf8', $hookPy, $HookEvent, '--stdin-file', $tmp)
    $r = Invoke-Proc $python.Exe $argv $HookTimeoutMs
    if ($r.TimedOut) { Exit-FailClosed ("hook exceeded {0} s" -f ($HookTimeoutMs / 1000)) }
    if ($r.Code -ne 0 -and $r.Code -ne 2) {
        # Python crashed before producing a verdict (import error, syntax error...).
        Write-Log ("hook exit {0}: {1}" -f $r.Code, ($r.Err -replace '\s+', ' ').Substring(0, [Math]::Min(600, ($r.Err -replace '\s+', ' ').Length)))
        Exit-FailClosed ("hook.py exited with code {0}" -f $r.Code)
    }
    Write-Raw ([Console]::OpenStandardOutput()) $r.Out
    Write-Raw ([Console]::OpenStandardError()) $r.Err
    exit $r.Code
} catch {
    Exit-FailClosed ("launcher error: " + $_.Exception.Message)
} finally {
    if ($tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
}
```
