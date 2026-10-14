
```
SELECT 'prod' AS env, id, username, email, kerberos_principal, role, created_at, last_login_at
FROM ai_marketplace.users
WHERE lower(username) = 'm1bcm03'
   OR lower(kerberos_principal) LIKE 'm1bcm03@%'
   OR lower(email) LIKE 'm1bcm03@%'
   OR lower(email) LIKE '%ben%miller%'
UNION ALL
SELECT 'dev', id, username, email, kerberos_principal, role, created_at, last_login_at
FROM ai_marketplace_dev.users
WHERE lower(username) = 'm1bcm03'
   OR lower(kerberos_principal) LIKE 'm1bcm03@%'
   OR lower(email) LIKE 'm1bcm03@%'
   OR lower(email) LIKE '%ben%miller%';
```
