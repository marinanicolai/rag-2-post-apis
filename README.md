```
rm -rf ~/compare-sql
df -h ~ /tmp
du -sh ~/* ~/.[!.]* 2>/dev/null | sort -h | tail -10
```
```
mkdir -p /tmp/$USER-cmp && chmod 700 /tmp/$USER-cmp
git clone --depth 1 --filter=blob:none --sparse --branch tmp/compare-sql "$(git -C /ai/www/cgi-bin/ai-marketplace-dev remote get-url origin)" /tmp/$USER-cmp/repo
git -C /tmp/$USER-cmp/repo sparse-checkout set tmp
cp /tmp/$USER-cmp/repo/tmp/compare_dev_prod.sql /tmp/$USER-cmp/
head -5 /tmp/$USER-cmp/compare_dev_prod.sql
```
