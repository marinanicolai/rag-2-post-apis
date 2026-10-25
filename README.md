```
               $tools = "C:\Users\M3MXN08\repo\dlp-installer"
   python $tools\make_manifest.py --version 0.2.2-dev --tag dev --plugin-dir . --out $tools\dev-hashes.json --allow-dirty
   python $tools\install.py --uninstall
   $devsha = (Get-FileHash "$tools\dev-hashes.json" -Algorithm SHA256).Hash
   $opts = @("--manifest", "$tools\dev-hashes.json", "--manifest-sha256", $devsha, "--source", ".")
   python $tools\install.py @opts
```
