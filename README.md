```
mkdir -p ~/scratch && cd ~/scratch
git clone <repo-url> audit-am && cd audit-am
git fetch origin fix/skill-download-frontmatter && git checkout FETCH_HEAD
python3 -m venv .venv-audit && source .venv-audit/bin/activate
pip install -e libs/python-common -e libs/db -e apps/api
export PGOPTIONS='-c default_transaction_read_only=on'
PYTHONPATH=apps/api:libs/db:libs/python-common python scripts/audit_plugin_renderer_hashes.py
```
