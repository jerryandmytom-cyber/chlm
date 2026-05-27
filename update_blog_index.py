# -*- coding: utf-8 -*-
"""
更新博客列表页 blog/index.html
自动扫描 blog/daily/ 和 blog/special/ 目录，生成最新文章列表
"""
import os, re
from pathlib import Path
from datetime import datetime

WORKDIR = Path("C:/Users/win11/.openclaw/workspace/chlm-website")
BLOG_DIR = WORKDIR / "blog"
BLOG_INDEX = BLOG_DIR / "index.html"

def get_article_meta(filepath):
    """从HTML文章文件提取元数据，支持多种HTML格式"""
    content = filepath.read_text(encoding="utf-8")
    
    # 格式1: <span>YYYY-MM-DD</span> (每日资讯格式)
    date_match = re.search(r'<span>(\d{4}-\d{2}-\d{2})</span>', content)
    if not date_match:
        # 格式2: JSON-LD datePublished
        date_match = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"', content)
    date = date_match.group(1) if date_match else ""
    
    # 提取标题 (h1)
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    title = title_match.group(1) if title_match else ""
    
    # 提取内容条数
    count_match = re.search(r'(\d+) 条内容', content)
    count = count_match.group(1) if count_match else ""
    
    return date, title, count

def build_blog_index():
    """扫描所有文章，构建博客列表HTML"""
    daily_dir = BLOG_DIR / "daily"
    special_dir = BLOG_DIR / "special"
    
    daily_articles = []
    special_articles = []
    
    # 扫描每日资讯
    if daily_dir.exists():
        for f in sorted(daily_dir.glob("*.html"), reverse=True):
            date, title, count = get_article_meta(f)
            if date and title:
                url = f"https://chlm.onrender.com/blog/daily/{f.name}"
                daily_articles.append((date, title, count, url))
    
    # 扫描专题文章
    if special_dir.exists():
        for f in sorted(special_dir.glob("*.html"), reverse=True):
            date, title, count = get_article_meta(f)
            if date and title:
                url = f"https://chlm.onrender.com/blog/special/{f.name}"
                special_articles.append((date, title, count, url))
    
    # 扫描 SEO 深度文章 (blog/*.html 但非 index/daily/special)
    seo_articles = []
    for f in BLOG_DIR.glob("*.html"):
        if f.name in ("index.html",):
            continue
        date, title, count = get_article_meta(f)
        if date and title:
            url = f"https://chlm.onrender.com/blog/{f.name}"
            seo_articles.append((date, title, count, url))
    
    return special_articles, seo_articles, daily_articles

def generate_index_html(special_articles, seo_articles, daily_articles):
    """生成博客列表页HTML"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 构建专题文章HTML
    special_html = ""
    for date, title, count, url in special_articles:
        special_html += f'''
        <div class="post-item">
            <div class="post-date">{date}</div>
            <div class="post-title"><a href="{url}">{title}</a></div>
            <div class="post-meta"><span>{count} 条内容</span><span>出海实战经验与行业洞察</span></div>
        </div>'''
    
    # 构建 SEO 深度文章 HTML
    seo_html = ""
    for date, title, count, url in seo_articles:
        seo_html += f'''
        <div class="post-item">
            <div class="post-date">{date}</div>
            <div class="post-title"><a href="{url}">{title}</a></div>
            <div class="post-meta"><span>深度文章</span><span>SEO友好内容</span></div>
        </div>'''
    
    # 构建每日资讯HTML
    daily_html = ""
    for date, title, count, url in daily_articles:
        daily_html += f'''
        <div class="post-item">
            <div class="post-date">{date}</div>
            <div class="post-title"><a href="{url}">{title}</a></div>
            <div class="post-meta"><span>{count} 条内容</span></div>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://chlm.onrender.com/blog/">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>博客 - 出海联盟 CHLM</title>
    <meta name="description" content="出海联盟博客，提供每日出海资讯、广告投放干货、跨境营销策略等内容。">
    <meta property="og:title" content="博客 - 出海联盟 CHLM">
    <meta property="og:description" content="每日出海资讯汇总，涵盖广告投放、SEO、AI工具等出海营销干货">
    <meta property="og:type" content="website">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "出海联盟博客",
      "description": "每日出海资讯、广告投放干货、跨境营销策略",
      "url": "https://chlm.onrender.com/blog/",
      "publisher": {{ "@type": "Organization", "name": "出海联盟", "url": "https://chlm.onrender.com" }}
    }}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #0a0a0f; color: #e0e0e0; line-height: 1.7; }}
        a {{ color: #4fc3f7; text-decoration: none; }}
        a:hover {{ color: #81d4fa; }}
        header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-bottom: 1px solid #2a2a4a; padding: 1rem 0; position: sticky; top: 0; z-index: 100; }}
        nav {{ max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1.5rem; }}
        .nav-logo {{ display: flex; align-items: center; }}
        .nav-logo-icon {{ height: 40px; width: auto; }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ color: #b0b0b0; font-size: 0.95rem; }}
        .nav-links a:hover {{ color: #4fc3f7; }}
        .nav-cta {{ background: #4fc3f7; color: #0a0a0f; padding: 0.5rem 1.2rem; border-radius: 20px; font-weight: 600; font-size: 0.9rem; }}
        .nav-cta:hover {{ background: #81d4fa; color: #0a0a0f; }}
        .breadcrumb {{ max-width: 1000px; margin: 1.5rem auto 0; padding: 0 1.5rem; font-size: 0.85rem; color: #888; }}
        .breadcrumb a {{ color: #4fc3f7; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 3rem 1.5rem; }}
        .page-header {{ margin-bottom: 3rem; border-bottom: 1px solid #2a2a4a; padding-bottom: 1.5rem; }}
        .page-header h1 {{ font-size: 2.5rem; color: #fff; margin-bottom: 0.5rem; }}
        .page-header p {{ color: #888; font-size: 0.95rem; }}
        .page-header .last-update {{ color: #4fc3f7; font-size: 0.85rem; margin-top: 0.5rem; }}
        .section-title {{ color: #4fc3f7; font-size: 1.1rem; margin-bottom: 1.2rem; font-weight: 600; padding-top: 1rem; border-top: 1px solid #2a2a4a; }}
        .section-title:first-of-type {{ border-top: none; padding-top: 0; }}
        .post-item {{ background: linear-gradient(135deg, #1a1a2e, #141428); border: 1px solid #2a2a4a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem; }}
        .post-item:hover {{ border-color: #4fc3f7; }}
        .post-date {{ color: #4fc3f7; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 1px; }}
        .post-title {{ color: #fff; font-size: 1rem; font-weight: 600; margin-bottom: 0.4rem; }}
        .post-title a {{ color: #fff; }}
        .post-title a:hover {{ color: #4fc3f7; }}
        .post-meta {{ color: #666; font-size: 0.8rem; display: flex; gap: 1rem; }}
        footer {{ background: #0a0a0f; border-top: 1px solid #1a1a2e; padding: 2rem 1.5rem; margin-top: 4rem; }}
        .footer-content {{ max-width: 900px; margin: 0 auto; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }}
        .footer-links {{ display: flex; gap: 1.5rem; }}
        .footer-links a {{ color: #666; font-size: 0.85rem; }}
        .footer-links a:hover {{ color: #4fc3f7; }}
        .footer-copy {{ color: #555; font-size: 0.8rem; }}
        .empty {{ color: #666; text-align: center; padding: 3rem; }}
        @media (max-width: 768px) {{ .nav-links {{ display: none; }} .page-header h1 {{ font-size: 1.8rem; }} }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="https://chlm.onrender.com/#hero" class="nav-logo">
                <img class="nav-logo-icon" src="https://chlm.onrender.com/public/logo.jpg" alt="CHLM">
                <span style="color:#fff;font-weight:700;font-size:1.2rem;margin-left:8px;">出海联盟</span>
            </a>
            <ul class="nav-links">
                <li><a href="https://chlm.onrender.com/#hero">首页</a></li>
                <li><a href="https://chlm.onrender.com/#services">服务</a></li>
                <li><a href="https://chlm.onrender.com/#about">关于</a></li>
                <li><a href="https://chlm.onrender.com/#rules">规则</a></li>
                <li><a href="https://chlm.onrender.com/blog/">博客</a></li>
            </ul>
            <a href="https://t.me/CHLM" class="nav-cta" target="_blank">加入社群</a>
        </nav>
    </header>
    
    <div class="breadcrumb">
        <a href="https://chlm.onrender.com/">首页</a> &rsaquo; 博客
    </div>
    
    <main class="container">
        <div class="page-header">
            <h1>博客</h1>
            <p>出海联盟每日资讯汇总，涵盖广告投放、SEO、AI工具等出海营销干货</p>
            <div class="last-update">最后更新：{today}</div>
        </div>
'''

    if special_articles:
        html += '        <div class="section-title">专题文章</div>\n'
        html += special_html + "\n"
    
    if seo_articles:
        html += '        <div class="section-title">深度文章</div>\n'
        html += seo_html + "\n"
    
    if daily_articles:
        html += '        <div class="section-title">每日资讯</div>\n'
        html += daily_html + "\n"
    
    if not special_articles and not seo_articles and not daily_articles:
        html += '        <div class="empty">暂无文章内容</div>\n'
    
    html += f'''
    </main>
    <footer>
        <div class="footer-content">
            <div class="footer-links"><a href="https://chlm.onrender.com/">首页</a><a href="https://chlm.onrender.com/about.html">关于我们</a><a href="https://chlm.onrender.com/faq.html">常见问题</a><a href="https://chlm.onrender.com/resources.html">出海资源</a><a href="https://chlm.onrender.com/join.html">加入我们</a></div>
            <div class="footer-copy">&copy; 2019-2026 出海联盟 CHLM - 海外最早的出海资源社区</div>
        </div>
    </footer>
</body>
</html>'''
    
    return html

def main():
    print("[博客列表] 扫描文章目录...")
    special, seo, daily = build_blog_index()
    
    print(f"  专题文章: {len(special)} 篇")
    print(f"  深度文章: {len(seo)} 篇")
    print(f"  每日资讯: {len(daily)} 篇")
    
    if not daily and not special and not seo:
        print("[警告] 没有找到任何文章!")
        return
    
    html = generate_index_html(special, seo, daily)
    BLOG_INDEX.write_text(html, encoding="utf-8")
    print(f"[完成] blog/index.html 已更新")

if __name__ == "__main__":
    main()