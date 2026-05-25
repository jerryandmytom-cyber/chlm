import re, sys
code = open('C:/Users/win11/.openclaw/workspace/chlm-website/auto_daily.py', 'r', encoding='utf-8').read()

# Check limit position
m = re.search(r'limit=CHANNEL_LIMITS', code)
if m:
    print('[OK] CHANNEL_LIMITS inserted')
else:
    print('[FAIL] CHANNEL_LIMITS not found')
    sys.exit(1)

# Check chgx config
m = re.search(r'@chgx.*?150', code, re.DOTALL)
if m:
    print('[OK] @chgx configured as 150')
else:
    print('[FAIL] @chgx config not found')
    sys.exit(1)

# Check safe print
if "encode('ascii', 'replace')" in code:
    print('[OK] Safe print added')
else:
    print('[WARN] Safe print not found')

print('[OK] Code verification passed')