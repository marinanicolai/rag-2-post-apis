```
cd ~/scratch/audit-am
python3 -m venv .venv-audit
source .venv-audit/bin/activate
pip install -e libs/python-common -e libs/db -e apps/api
export PGOPTIONS='-c default_transaction_read_only=on'
PYTHONPATH=apps/api:libs/db:libs/python-common python scripts/audit_plugin_renderer_hashes.py
```
