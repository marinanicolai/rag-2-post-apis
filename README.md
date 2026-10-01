Access control is checked in the UI, but this command also shows every field LiteLLM stores for your skills. Run it **before** cleaning up, while the entries still exist. Your key should still be set in the same terminal:

```
Invoke-RestMethod -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" } | ConvertTo-Json -Depth 5
```

Look for any field about teams, users, organizations, or access groups. If there isn't one, that supports the "no per-team control" finding. Remember to `cls` before taking a screenshot.

**Cleanup**

1. Uninstall the test plugins from Claude Code and remove the marketplace:
   ```
   claude plugin uninstall skillhub-spike-test@litellm
   claude plugin uninstall skillhub-spike-pinned@litellm
   claude plugin marketplace remove litellm
   ```

2. Delete both entries from LiteLLM:
   ```
   Invoke-RestMethod -Method Delete -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins/skillhub-spike-test" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" }
   Invoke-RestMethod -Method Delete -Uri "https://martinai-dev-2-api.test.frb.gov/claude-code/plugins/skillhub-spike-pinned" -Headers @{ Authorization = "Bearer $env:LITELLM_KEY" }
   ```
   If either fails, delete it from the **Skills** page in the UI instead.

3. Confirm the catalog is empty:
   ```
   curl.exe https://martinai-dev-2-api.test.frb.gov/claude-code/marketplace.json
   ```
   It should end with `"plugins":[]`.

4. Remove the key from your terminal session:
   ```
   Remove-Item Env:LITELLM_KEY
   ```

5. Delete the test keys in the LiteLLM UI under **Virtual Keys**, including the one that appeared in the earlier screenshot. If Daniel created the management key for you, let him know you're done so he can remove or keep it.

The test files are still on `main` in the `debates` repo. If the repo was repurposed just for this spike, you can leave them. If it needs its old content back, that's in the history at commit `cbf1466`, and the repo owner can decide whether to restore it.
