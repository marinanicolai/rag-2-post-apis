```
mkdir -p ~/backups && chmod 700 ~/backups
cp /tmp/$USER-cmp/prod_before_sync_*.dump /tmp/$USER-cmp/commit.out /tmp/$USER-cmp/dryrun.out ~/backups/
chmod 600 ~/backups/*
ls -lh ~/backups/
```
