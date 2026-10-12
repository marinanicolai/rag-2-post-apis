```

bash
cd ~
git clone --depth 1 --branch tmp/compare-sql "$(git -C /ai/www/cgi-bin/ai-marketplace-dev remote get-url origin)" ~/compare-sql
cp ~/compare-sql/tmp/compare_dev_prod.sql ~/compare_dev_prod.sql
head -5 ~/compare_dev_prod.sql
```
