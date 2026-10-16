Repeat the **three-line block**: uninstall, change the text, install. Do it once per word you want to test. Here are ready-to-paste versions, one at a time:

**Test 1: "RESTRICTED" alone**

```powershell
claude plugin uninstall copytest@mp-test --scope project
Set-Content C:\temp\mp-test\copytest\b.md "This is RESTRICTED."
claude plugin install copytest@mp-test --scope project
```

**Test 2: "CONFIDENTIAL FR"**

```powershell
claude plugin uninstall copytest@mp-test --scope project
Set-Content C:\temp\mp-test\copytest\b.md "Anything above CONFIDENTIAL FR is denied."
claude plugin install copytest@mp-test --scope project
```

**Test 3: "INTERNAL FR"** (the ceiling level, likely allowed)

```powershell
claude plugin uninstall copytest@mp-test --scope project
Set-Content C:\temp\mp-test\copytest\b.md "This is INTERNAL FR."
claude plugin install copytest@mp-test --scope project
```

After each one, note **failed (EPERM)** or **installed**. If an install fails, the uninstall line in the next test will say the plugin isn't installed. That's fine, just continue.
