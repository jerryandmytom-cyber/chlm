# -*- coding: utf-8 -*-
from pathlib import Path
import re

BASE = Path("C:/Users/win11/.openclaw/workspace/chlm-website")
BLOG = BASE / "blog"

print("=== SEO修复开始 ===\n")

# ============================================================
# 修复1: sitemap 格式错误 + 补充专题文章
# ============================================================
entries = []

main_pages = [
    ("https://chlm.onrender.com/", "2026-05-26", "weekly", "1.0"),
    ("https://chlm.onrender.com/index.html", "2026-05-26", "weekly", "1.0"),
    ("https://chlm.onrender.com/about.html", "2026-05-26", "monthly", "0.8"),
    ("https://chlm.onrender.com/faq.html", "2026-05-26", "weekly", "0.9"),
    ("https://chlm.onrender.com/resources.html", "2026-05-26", "monthly", "0.8"),
    ("https://chlm.onrender.com/testimonials.html", "2026-05-26", "monthly", "0.7"),
    ("https://chlm.onrender.com/join.html", "2026-05-26", "weekly", "0.9"),
    ("https://chlm.onrender.com/directory.html", "2026-05-26", "monthly", "0.7"),
    ("https://chlm.onrender.com/blog/cross-border-guide.html", "2026-05-26", "monthly", "0.7"),
    ("https://chlm.onrender.com/blog/", "2026-05-26", "daily", "0.8"),
]

for loc, lastmod, freq, pri in main_pages:
    entries.append((loc, lastmod, freq, pri))

for f in sorted((BLOG / "daily").glob("*.html")):
    ds = f.stem
    entries.append((f"https://chlm.onrender.com/blog/daily/{ds}.html", ds, "weekly", "0.6"))

for f in sorted((BLOG / "special").glob("*.html")):
    ds = f.stem
    entries.append((f"https://chlm.onrender.com/blog/special/{ds}.html", ds, "weekly", "0.6"))

urls_xml = ""
for loc, lastmod, freq, pri in entries:
    urls_xml += f"\n  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls_xml + "\n</urlset>"
(BASE / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
print(f"[OK] sitemap.xml 修复完成，共 {len(entries)} 个URL")

# ============================================================
# 修复3: blog/index.html 补充 canonical
# ============================================================
idx = (BLOG / "index.html").read_text(encoding="utf-8")
if 'rel="canonical"' not in idx:
    idx = idx.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    <link rel="canonical" href="https://chlm.onrender.com/blog/">', 1)
    (BLOG / "index.html").write_text(idx, encoding="utf-8")
    print("[OK] blog/index.html 已补充 canonical")
else:
    print("[SKIP] blog/index.html 已有 canonical")

# ============================================================
# 修复4: blog/daily/*.html 补充完整 OG 标签
# ============================================================
for f in (BLOG / "daily").glob("*.html"):
    content = f.read_text(encoding="utf-8")
    ds = f.stem
    year = ds[:4]
    month = ds[5:7]
    day = ds[8:10]
    date_display = f"{year}年{month}月{day}日"
    title = f"出海资讯TG社群日报 {date_display}"

    if 'property="og:title"' in content:
        print(f"[SKIP] {f.name} 已有 OG")
        continue

    og = f'''
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="出海联盟{date_display}广告投放与营销干货资讯汇总，覆盖Facebook、Google、TikTok、Instagram、Telegram等平台投放策略及AI工具应用。">
    <meta property="og:image" content="https://chlm.onrender.com/public/logo.jpg">
    <meta property="og:url" content="https://chlm.onrender.com/blog/daily/{ds}.html">
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{ds}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="出海联盟{date_display}广告投放与营销干货资讯汇总。">
    <meta name="twitter:image" content="https://chlm.onrender.com/public/logo.jpg">'''

    content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">' + og, 1)
    f.write_text(content, encoding="utf-8")
    print(f"[OK] {f.name} OG标签已补充")

# ============================================================
# 专题文章 OG 标签
# ============================================================
for f in (BLOG / "special").glob("*.html"):
    content = f.read_text(encoding="utf-8")
    ds = f.stem
    m = re.search(r'<title>(.*?) - 出海联盟 CHLM</title>', content)
    if not m:
        print(f"[SKIP] {f.name} 无title")
        continue
    title = m.group(1)

    if 'property="og:title"' in content:
        print(f"[SKIP] {f.name} 已有 OG")
        continue

    og = f'''
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="出海联盟@shouce精华内容汇总，涵盖出海实战经验、资源对接、行业洞察等深度内容。">
    <meta property="og:image" content="https://chlm.onrender.com/public/logo.jpg">
    <meta property="og:url" content="https://chlm.onrender.com/blog/special/{ds}.html">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="出海联盟@shouce精华内容汇总。">
    <meta name="twitter:image" content="https://chlm.onrender.com/public/logo.jpg">'''

    content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">' + og, 1)
    f.write_text(content, encoding="utf-8")
    print(f"[OK] {f.name} OG标签已补充")

print("\n=== 全部修复完成，准备推送 ===")