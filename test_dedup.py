"""Test deduplication logic"""
from datetime import datetime

# Simulate the dedup logic
seen_texts = set()

texts = [
    "Facebook广告投放技巧分享 #出海",
    "Facebook广告投放技巧分享 #出海",  # duplicate
    "谷歌SEO优化干货 #AI工具",
    "独立站推广方法 #流量获取",
    "独立站推广方法 #流量获取",  # duplicate
    "TikTok广告投放教程 #引流",
]

items = []
for text in texts:
    text_key = text[:80]
    if text_key in seen_texts:
        print(f"[SKIP (dup)] {text[:40]}")
        continue
    seen_texts.add(text_key)
    items.append(text)
    print(f"[ADD] {text[:40]}")

print(f"\nTotal: {len(items)} unique items from {len(texts)} raw")