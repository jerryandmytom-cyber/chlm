import urllib.request
import re

req = urllib.request.Request('https://chlm.cc/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
r = urllib.request.urlopen(req)
html = r.read().decode()

with open(r'C:\Users\win11\.openclaw\workspace\chlm-website\source_homepage.html', 'w', encoding='utf-8') as f:
    f.write(html)

imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|gif|webp|svg|ico)', html)
for i in imgs:
    print(i)

# Also try relative paths with uploads
uploads = re.findall(r'/wp-content/uploads/[^"\']+', html)
for u in uploads:
    print('REL:', u)