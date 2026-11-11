```
cd /ai/www/cgi-bin/ai-marketplace
set -a && source .env && set +a
export PYTHONPATH="$PWD/apps/api:$PWD/libs/db:$PWD/libs/python-common"
.venv/bin/alembic -c libs/db/alembic.ini current
```
