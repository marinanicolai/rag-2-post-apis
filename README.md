```
python3 -m venv --system-site-packages .venv-audit
source .venv-audit/bin/activate
pip install "psycopg[binary]"
PYTHONPATH=apps/api:libs/db:libs/python-common python scripts/audit_plugin_renderer_hashes.py --schema ai_marketplace
```

