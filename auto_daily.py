"""
出海联盟网站 - 每日自动生成内容
从多个 Telegram 频道收集当天帖子，生成HTML博客文章并推送GitHub
"""

import os, sys, re, json, asyncio, subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ── Telegram ────────────────────────────────────────────────────────────────
from pyrogram import Client

# ── 配置 ────────────────────────────────────────────────────────────────────
WORKDIR = Path("C:/Users/win11/.openclaw/workspace/chlm-website")
TG_SESSION = "C:/Users/win11/.openclaw/workspace/tg-auto-poster"

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# 多频道采集 (每个频道设定不同采集量)
SOURCE_CHANNELS = [
    "@shouce",     # 出海用户手册
    "@chgq",        # 出海群
    "@chgx",        # 出海干货
]

# 各频道采集量配置 (chgx需要更多历史保证每天30条)
CHANNEL_LIMITS = {
    "@shouce": 50,
    "@chgq": 50,
    "@chgx": 150,  # 提高采集量确保每天30条
}

BLOG_DIR = WORKDIR / "blog" / "daily"

# ── 内容过滤 ─────────────────────────────────────────────────────────────────

# 条件A：主题关键词
TOPIC_KEYWORDS = [
    "Facebook广告投放", "facebook广告投放",
    "谷歌广告投放", "Google广告投放", "google广告投放",
    "TIKTOK广告投放", "TikTok广告投放", "tiktok广告投放",
    "INSTAGRAM广告投放", "Instagram广告投放", "instagram广告投放",
    "TELEGRAM广告投放", "Telegram广告投放", "telegram广告投放",
    "SEO干货", "seo干货",
    "AI干货", "ai干货", "AI工具", "ai工具",
    "广告投放", "独立站推广", "流量获取", "社媒营销",
    "出海营销", "跨境推广",
]

# 条件B：hashtag关键词
HASHTAG_KEYWORDS = [
    "#出海", "#担保", "#会员", "#代投", "#引流",
    "#数据", "#流量", "#支付", "#号商", "#通道",
    "#拉群", "#群发", "#搭建",
    "#广告投放", "#Facebook", "#TikTok", "#Instagram",
    "#SEO", "#AI营销", "#Telegram营销",
]


def is_relevant(text: str) -> bool:
    """检查内容是否与出海营销相关（主题关键词 OR hashtag关键词）"""
    for kw in TOPIC_KEYWORDS:
        if kw in text:
            return True
    for kw in HASHTAG_KEYWORDS:
        if kw in text:
            return True
    return False


FOOTER_HTML = """<div class="chlm-footer">
                <div class="footer-brand">出海联盟 @CHLM <a href="https://t.me/chlm">https://t.me/chlm</a></div>
                <div class="footer-desc">一个专注海外资源对接的专业社群<br>不代理 · 不中介 · 不参与任何具体业务<br>只为出海用户提供高质量、可信任的资源交流环境</div>
                <div class="footer-channels">
                    <div class="footer-section">社群信息：</div>
                    <div>交流大群：@ChuHaiDDD &nbsp;&nbsp; 交流大群：@ChuHaiEEE</div>
                    <div>公群频道：@CHGQ &nbsp;&nbsp; 供需频道：@CHGX &nbsp;&nbsp; 公告频道：@CHGG</div>
                    <div>出海大事件：@KuaiBao &nbsp;&nbsp; 出海黑名单：@ChuHaiFFF</div>
                </div>
                <div class="footer-staff">
                    <div class="footer-section">客服—安 妮 @ChuHaiHHH &nbsp;&nbsp; 客服—艾 琳 @ChuHaiKKK</div>
                    <div>担保—安东尼 @ChuHaiGGG &nbsp;&nbsp; 公群—布鲁斯 @ChuHaiXXX</div>
                </div>
                <div class="footer-cta">更多出海信息，请关注出海公告频道</div>
            </div>"""

FOOTER_CSS = """
        .chlm-footer {{ background: linear-gradient(135deg, #1a2a4a, #0d1f30); border: 1px solid #2a4a6a; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; text-align: left; }}
        .footer-brand {{ font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.8rem; }}
        .footer-brand a {{ color: #4fc3f7; }}
        .footer-desc {{ color: #aaa; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem; }}
        .footer-section {{ color: #4fc3f7; font-weight: 600; font-size: 0.85rem; margin: 0.8rem 0 0.4rem; }}
        .footer-channels {{ color: #ccc; font-size: 0.85rem; line-height: 1.8; }}
        .footer-staff {{ color: #ccc; font-size: 0.85rem; line-height: 1.8; margin-top: 0.5rem; }}
        .footer-cta {{ color: #4fc3f7; font-size: 0.9rem; font-weight: 600; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #2a4a6a; }}
        .article-footer {{ margin-top: 0; padding-top: 1.5rem; border-top: none; }}
"""

def make_html_article(title: str, date_str: str, items: list) -> str:
    """生成单篇博客HTML"""
    
    items_html = ""
    for source, text in items:
        # 转义HTML特殊字符
        safe_source = source.replace("<", "&lt;").replace(">", "&gt;")
        safe_text = text.replace("<", "&lt;").replace(">", "&gt;")
        items_html += f"""
        <div class="news-item">
            <div class="news-source">{safe_source}</div>
            <div class="news-text">{safe_text}</div>
        </div>"""
    
    date_display = datetime.now().strftime("%Y年%m月%d日")
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — 出海联盟 CHLM</title>
    <meta name="description" content="出海联盟{date_str}广告投放与营销干货资讯汇总，覆盖Facebook、Google、TikTok、Instagram、Telegram等平台投放策略及AI工具应用。">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="每日广告投放与营销干货汇总，涵盖Facebook/Google/TikTok/Instagram/Telegram广告及SEO、AI工具。">
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{date_str}">
    <link rel="canonical" href="https://chlm.onrender.com/blog/daily/{date_str}.html">
    
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "datePublished": "{date_str}",
      "dateModified": "{date_str}",
      "author": {{ "@type": "Organization", "name": "出海联盟", "url": "https://chlm.onrender.com" }},
      "publisher": {{ "@type": "Organization", "name": "出海联盟", "url": "https://chlm.onrender.com" }},
      "description": "每日广告投放与营销干货资讯汇总",
      "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://chlm.onrender.com/blog/daily/{date_str}.html" }}
    }}
    </script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #0a0a0f; color: #e0e0e0; line-height: 1.7; }}
        a {{ color: #4fc3f7; text-decoration: none; }}
        a:hover {{ color: #81d4fa; }}
        
        header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-bottom: 1px solid #2a2a4a; padding: 1rem 0; position: sticky; top: 0; z-index: 100; }}
        nav {{ max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1.5rem; }}
        .logo {{ font-size: 1.5rem; font-weight: 700; color: #fff; }}
        .logo span {{ color: #4fc3f7; }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{ color: #b0b0b0; font-size: 0.95rem; }}
        .nav-links a:hover {{ color: #4fc3f7; }}
        
        .breadcrumb {{ max-width: 1000px; margin: 1.5rem auto 0; padding: 0 1.5rem; font-size: 0.85rem; color: #888; }}
        .breadcrumb a {{ color: #4fc3f7; }}
        
        .container {{ max-width: 900px; margin: 0 auto; padding: 3rem 1.5rem; }}
        
        .article-header {{ margin-bottom: 2.5rem; border-bottom: 1px solid #2a2a4a; padding-bottom: 1.5rem; }}
        .article-header h1 {{ font-size: 2rem; color: #fff; margin-bottom: 0.8rem; line-height: 1.3; }}
        .article-meta {{ display: flex; gap: 1.5rem; font-size: 0.85rem; color: #888; flex-wrap: wrap; }}
        .article-meta span {{ display: flex; align-items: center; gap: 0.4rem; }}
        
        .ai-summary {{ background: linear-gradient(135deg, #1a2a3a, #0d1f2e); border: 1px solid #2a4a6a; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }}
        .ai-summary h2 {{ color: #4fc3f7; font-size: 1rem; margin-bottom: 0.8rem; }}
        .ai-summary p {{ color: #ccc; font-size: 0.95rem; }}
        .ai-summary ul {{ color: #ccc; font-size: 0.9rem; margin-top: 0.5rem; padding-left: 1.5rem; }}
        
        .topics-bar {{ display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 2rem; }}
        .topic-tag {{ background: #1a2a4a; color: #4fc3f7; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem; }}
        
        .news-item {{ background: linear-gradient(135deg, #1a1a2e, #141428); border: 1px solid #2a2a4a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.2rem; }}
        .news-source {{ color: #4fc3f7; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 1px; }}
        .news-text {{ color: #ccc; font-size: 0.95rem; line-height: 1.8; white-space: pre-wrap; word-break: break-word; }}
        
        {FOOTER_CSS}
        
        footer {{ background: #0a0a0f; border-top: 1px solid #1a1a2e; padding: 2rem 1.5rem; margin-top: 4rem; }}
        .footer-content {{ max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }}
        .footer-links {{ display: flex; gap: 1.5rem; }}
        .footer-links a {{ color: #666; font-size: 0.85rem; }}
        .footer-links a:hover {{ color: #4fc3f7; }}
        .footer-copy {{ color: #555; font-size: 0.8rem; }}
        
        @media (max-width: 768px) {{
            .nav-links {{ display: none; }}
            .article-header h1 {{ font-size: 1.5rem; }}
            .article-meta {{ flex-direction: column; gap: 0.5rem; }}
            .footer-channels div {{ font-size: 0.8rem; }}
            .footer-staff div {{ font-size: 0.8rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">出海<span>联盟</span></div>
            <ul class="nav-links">
                <li><a href="/">首页</a></li>
                <li><a href="/about.html">关于我们</a></li>
                <li><a href="/faq.html">常见问题</a></li>
                <li><a href="/resources.html">出海资源</a></li>
                <li><a href="/join.html">加入我们</a></li>
                <li><a href="/blog/">博客</a></li>
            </ul>
        </nav>
    </header>
    
    <div class="breadcrumb">
        <a href="/">首页</a> &rsaquo; <a href="/blog/">博客</a> &rsaquo; <a href="/blog/daily/">每日资讯</a> &rsaquo; {date_str}
    </div>
    
    <main class="container">
        <article>
            <header class="article-header">
                <h1>{title}</h1>
                <div class="article-meta">
                    <span>📅 {date_str}</span>
                    <span>🤖 自动生成</span>
                    <span>📢 {len(items)} 条内容</span>
                </div>
            </header>
            
            <div class="ai-summary">
                <h2>📋 今日要点</h2>
                <p>出海联盟每日资讯汇总，涵盖以下热门主题：</p>
                <ul>
                    <li>Facebook / Google / TikTok / Instagram / Telegram 广告投放</li>
                    <li>SEO优化技巧与AI工具应用</li>
                    <li>独立站推广与流量获取策略</li>
                </ul>
            </div>
            
            <div class="topics-bar">
                <span class="topic-tag">#广告投放</span>
                <span class="topic-tag">#Facebook</span>
                <span class="topic-tag">#TikTok</span>
                <span class="topic-tag">#SEO</span>
                <span class="topic-tag">#AI工具</span>
                <span class="topic-tag">#出海营销</span>
            </div>
            
            <section class="news-list">
                {items_html if items_html else "<p style='color:#888;text-align:center;padding:2rem;'>今日暂无相关新内容，请稍后再访问。</p>"}
            </section>
            
            {FOOTER_HTML}
            
            <footer class="article-footer">
                <p>出海联盟 CHLM · 海外最早的出海资源社区</p>
                <p style="margin-top:0.5rem;"><a href="https://t.me/chlm">📢 订阅出海资讯频道</a> · <a href="https://t.me/chgx">📚 更多文章</a></p>
            </footer>
        </article>
    </main>
    
    <footer>
        <div class="footer-content">
            <div class="footer-links">
                <a href="/">首页</a>
                <a href="/about.html">关于我们</a>
                <a href="/faq.html">常见问题</a>
                <a href="/resources.html">出海资源</a>
                <a href="/join.html">加入我们</a>
            </div>
            <div class="footer-copy">© 2019-2026 出海联盟 CHLM · 海外最早的出海资源社区</div>
        </div>
    </footer>
</body>
</html>"""
    
    return html


def update_sitemap(date_str: str) -> bool:
    """更新 sitemap.xml"""
    sitemap_file = WORKDIR / "sitemap.xml"
    if not sitemap_file.exists():
        return False
    
    content = sitemap_file.read_text(encoding="utf-8")
    if f"blog/daily/{date_str}.html" in content:
        return False
    
    new_entry = f"""
  <url>
    <loc>https://chlm.onrender.com/blog/daily/{date_str}.html</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>
  </url>"""
    
    content = content.replace("</urlset>", f"{new_entry}</urlset>")
    sitemap_file.write_text(content, encoding="utf-8")
    print(f"[更新] sitemap.xml 已添加 daily/{date_str}.html")
    return True


def run_cmd(cmd: list[str]) -> str:
    """执行 git 命令"""
    try:
        result = subprocess.run(cmd, cwd=WORKDIR, capture_output=True, text=True, encoding="utf-8")
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


# ── 主程序 ───────────────────────────────────────────────────────────────────

async def main():
    print(f"[每日生成器] 启动 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_display = datetime.now().strftime("%Y年%m月%d日")
    
    # ── 1. 连接 Telegram ────────────────────────────────────────────────────
    app = Client(
        "auto_poster",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        workdir=TG_SESSION,
    )
    
    await app.start()
    print(f"[连接] Telegram 已连接")
    
    items: list[tuple[str, str]] = []
    seen_texts: set[str] = set()  # 去重：按内容哈希
    cutoff = datetime.now().replace(hour=0, minute=0, second=0)
    
    # ── 2. 遍历所有频道采集 ─────────────────────────────────────────────────
    for ch in SOURCE_CHANNELS:
        print(f"[扫描] 频道: {ch}")
        try:
            async for msg in app.get_chat_history(ch, limit=CHANNEL_LIMITS.get(ch, 50)):
                raw_text = msg.caption or msg.text or ""
                if not raw_text:
                    continue
                if msg.date.replace(tzinfo=None) < cutoff:
                    continue
                if not is_relevant(raw_text):
                    continue
                
                source = msg.chat.username or msg.chat.title or ch.replace("@", "")
                text = raw_text[:1500]
                if len(text) >= 20:
                    # 去重：按内容前80字符的哈希去重
                    text_key = text[:80]
                    if text_key in seen_texts:
                        continue
                    seen_texts.add(text_key)
                    # 附加 hashtags
                    hashtags = " #出海联盟 #出海供需 #担保 #供应 #需求 #东南亚大事件 #数据 #流量 #账号 #群发 #拉群 #搭建 #支付 #海外"
                    items.append((source, text + hashtags))
                    # 安全打印（避免emoji编码问题）
                    safe_preview = text[:40].encode('ascii', 'replace').decode('ascii')
                    print(f"  + {source} | {safe_preview}...")
        except Exception as e:
            print(f"[错误] 扫描 {ch} 失败: {e}")
            continue
    
    await app.stop()
    
    # ── 3. 生成 HTML ─────────────────────────────────────────────────────────
    title = f"出海资讯日报 {date_display}"
    html = make_html_article(title, date_str, items)
    
    out_file = BLOG_DIR / f"{date_str}.html"
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"[生成] {out_file.name}")
    
    # ── 4. 更新 sitemap + 博客列表 ─────────────────────────────────────────
    sitemap_updated = update_sitemap(date_str)
    
    # 更新博客列表
    import subprocess
    result = subprocess.run(
        [sys.executable, "update_blog_index.py"],
        cwd=WORKDIR,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    print(f"[博客列表] {result.stdout.strip()}")
    blog_index_updated = True
    
    # ── 5. Git 推送 ──────────────────────────────────────────────────────────
    changes = run_cmd(["git", "status", "--porcelain"])
    if not changes.strip():
        print("[跳过] 没有内容变更")
        return
    
    run_cmd(["git", "add", str(out_file.relative_to(WORKDIR))])
    if sitemap_updated:
        run_cmd(["git", "add", "sitemap.xml"])
    run_cmd(["git", "add", "blog/index.html"])
    
    commit_msg = f"自动更新: 出海资讯日报 {date_display} ({len(items)}条内容)"
    run_cmd(["git", "commit", "-m", commit_msg])
    result = run_cmd(["git", "push", "origin", "main"])
    
    print(f"[完成] 已推送 {len(items)} 条内容")
    print(f"[提示] Render 部署预计2-3分钟内完成")


if __name__ == "__main__":
    asyncio.run(main())