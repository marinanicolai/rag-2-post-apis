```
ps aux | grep -E "php-fpm|php-cgi|httpd|apache2|nginx|lsphp" | grep -v grep
cat /etc/os-release | head -3
rpm -qa 2>/dev/null | grep -i php || dpkg -l 2>/dev/null | grep -i php
```
