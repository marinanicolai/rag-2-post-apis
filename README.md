```
bash
cd ~/scratch && git clone --depth 1 -b feature/enrichment-unknown-check https://gitlab.frb.gov/ai-program/platforms/tech-enablement/coding-tools/ai-marketplace.git unknown-check
cd unknown-check
python3 -m venv --system-site-packages .venv && source .venv/bin/activate
pip install "psycopg[binary]" psycopg2-binary opentelemetry-api
```
```
set -a; source /ai/www/cgi-bin/ai-marketplace/.env; set +a
export DATABASE_URL="postgresql+psycopg2://${DATABASE_URL#*://}"
export PYTHONPATH=apps/api:libs/db:libs/python-common:scripts
unset PGOPTIONS
```
```
python scripts/enrichment_unknown_check.py --schema ai_marketplace_dev | tee /tmp/unknown-check-dev.txt
```
```
python scripts/enrichment_unknown_check.py --schema ai_marketplace | tee /tmp/unknown-check-prod.txt
```
