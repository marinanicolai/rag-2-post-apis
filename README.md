You're on the fix branch now.

**Step 2: look at the two rules**

Run these one at a time:

```powershell
Get-ChildItem .\restrictions | Select-Object Name
```

This lists all the rule files.

```powershell
Get-Content (Get-ChildItem .\restrictions\*card*.md).FullName
```

This shows the payment-card rule.

```powershell
Get-Content (Get-ChildItem .\restrictions\*bulk*.md).FullName
```

This shows the bulk-contacts rule.

```powershell
Select-String -Path .\tests\* -Pattern "card|bulk" -List | Select-Object Path
```


