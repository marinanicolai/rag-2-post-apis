```
cd C:\Users\M3MXN08\repo
Rename-Item skillhub-spike-test-plugin skillhub-spike-test-plugin-old
git clone <debates-url> skillhub-spike-test-plugin
cd skillhub-spike-test-plugin
git checkout -b cleanup
git rm pip.ini madi-config-page.png madi-homepage-working.png madi-homepage.png madi-websocket-connected.png
git commit -m "Clean up repo for reuse"
git push -u origin cleanup
```
