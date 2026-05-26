"""
出海联盟专题文章采集
从 @shouce 采集精华帖子生成专题文章，更新博客列表并推送到GitHub
"""

import os, re, subprocess
from datetime import datetime
from pathlib import Path

from pyrogram import Client

WORKDIR = Path("C:/Users/win11/.openclaw/workspace/chlm-website")
BLOG_DIR = WORKDIR / "blog"
TG_SESSION = WORKDIR.parent / "tg-auto-poster"

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

NAV_HTML = '''    <header>
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
    </header>'''

CSS_BASE = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #0a0a0f; color: #e0e0e0; line-height: 1.7; }
        a { color: #4fc3f7; text-decoration: none; }
        a:hover { color: #81d4fa; }
        header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-bottom: 1px solid #2a2a4a; padding: 1rem 0; position: sticky; top: 0; z-index: 100; }
        nav { max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1.5rem; }
        .nav-logo { display: flex; align-items: center; }
        .nav-logo-icon { height: 40px; width: auto; }
        .nav-links { display: flex; gap: 2rem; list-style: none; }
        .nav-links a { color: #b0b0b0; font-size: 0.95rem; }
        .nav-links a:hover { color: #4fc3f7; }
        .nav-cta { background: #4fc3f7; color: #0a0a0f; padding: 0.5rem 1.2rem; border-radius: 20px; font-weight: 600; font-size: 0.9rem; }
        .nav-cta:hover { background: #81d4fa; color: #0a0a0f; }
        .breadcrumb { max-width: 1000px; margin: 1.5rem auto 0; padding: 0 1.5rem; font-size: 0.85rem; color: #888; }
        .breadcrumb a { color: #4fc3f7; }
        .container { max-width: 900px; margin: 0 auto; padding: 3rem 1.5rem; }
        .article-header { margin-bottom: 2.5rem; border-bottom: 1px solid #2a2a4a; padding-bottom: 1.5rem; }
        .article-header h1 { font-size: 2rem; color: #fff; margin-bottom: 0.8rem; line-height: 1.3; }
        .article-meta { display: flex; gap: 1.5rem; font-size: 0.85rem; color: #888; flex-wrap: wrap; }
        .article-meta span { display: flex; align-items: center; gap: 0.4rem; }
        .ai-summary { background: linear-gradient(135deg, #1a2a3a, #0d1f2e); border: 1px solid #2a4a6a; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
        .ai-summary h2 { color: #4fc3f7; font-size: 1rem; margin-bottom: 0.8rem; }
        .ai-summary p { color: #ccc; font-size: 0.95rem; }
        .ai-summary ul { color: #ccc; font-size: 0.9rem; margin-top: 0.5rem; padding-left: 1.5rem; }
        .topics-bar { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 2rem; }
        .topic-tag { background: #1a2a4a; color: #4fc3f7; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem; }
        .news-item { background: linear-gradient(135deg, #1a1a2e, #141428); border: 1px solid #2a2a4a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.2rem; }
        .news-source { color: #4fc3f7; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 1px; }
        .news-text { color: #ccc; font-size: 0.95rem; line-height: 1.8; white-space: pre-wrap; word-break: break-word; }
        .chlm-footer { background: linear-gradient(135deg, #1a2a4a, #0d1f30); border: 1px solid #2a4a6a; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; text-align: left; }
        .footer-brand { font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.8rem; }
        .footer-brand a { color: #4fc3f7; }
        .footer-desc { color: #aaa; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem; }
        .footer-section { color: #4fc3f7; font-weight: 600; font-size: 0.85rem; margin: 0.8rem 0 0.4rem; }
        .footer-channels { color: #ccc; font-size: 0.85rem; line-height: 1.8; }
        .footer-staff { color: #ccc; font-size: 0.85rem; line-height: 1.8; margin-top: 0.5rem; }
        .footer-cta { color: #4fc3f7; font-size: 0.9rem; font-weight: 600; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #2a4a6as; }
        .article-footer { margin-top: 0; padding-top: 1.5rem; border-top: none; text-align: center; color: #555; font-size: 0.85rem; }
        .article-footer a { color: #4fc3f7; }
        footer { background: #0a0a0f; border-top: 1px solid #1a1a2e; padding: 2rem 1.5rem; margin-top: 4rem; }
        .footer-content { max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
        .footer-links { display: flex; gap: 1.5rem; }
        .footer-links a { color: #666; font-size: 0.85rem; }
        .footer-links a:hover { color: #4fc3f7; }
        .footer-copy { color: #555; font-size: 0.8rem; }
        @media (max-width: 768px) { .nav-links { display: none; } .article-header h1 { font-size: 1.5rem; } .article-meta { flex-direction: column; gap: 0.5rem; } }
"""

FOOTER_HTML = """
            <div class="chlm-footer">
                <div class="footer-brand">出海联盟 @CHLM <a href="https://t.me/chlm">https://t.me/chlm</a></div>
                <div class="footer-desc">一个专注海外资源对接的专业社群<br>不代理 · 不中介 · 不参与任何具体业务<br>只为出海用户提供高质量、可信任的资源交流环境</div>
                <div class="footer-channels">
                    <div class="footer-section">社群信息：</div>
                    <div>交流大群：@ChuHaiDDD &nbsp;&nbsp; 交流二群：@ChuHaiEEE</div>
                    <div>公群频道：@CHGQ &nbsp;&nbsp; 供需频道：@CHGX &nbsp;&nbsp; 公告频道：@CHGG</div>
                    <div>出海大事件：@KuaiBao &nbsp;&nbsp; 出海黑名单：@ChuHaiFFF</div>
                </div>
                <div class="footer-staff">
                    <div class="footer-section">客服—安 妮 @ChuHaiHHH &nbsp;&nbsp; 客服—艾 琳 @ChuHaiKKK</div>
                    <div>担保—安东尼 @ChuHaiGGG &nbsp;&nbsp; 公群—布鲁斯 @ChuHaiXXX</div>
                </div>
                <div class="footer-cta">更多出海信息，请关注出海公告频道</div>
            </div>
"""

def esc(t):
    return t.replace("&", "&").replace("<", "<").replace(">", ">")

def make_article(title, slug, date_str, date_display, count, items):
    items_html = ""
    for src, text in items:
        items_html += f"\n                <div class=\"news-item\">\n                    <div class=\"news-source\">{esc(src)}</div>\n                    <div class=\"news-text\">{esc(text)}</div>\n                </div>"

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 出海联盟 CHLM</title>
    <meta name="description" content="出海联盟{date_display}@shouce精华内容汇总">
    <meta property="og:title" content="{title}">
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{date_str}">
    <link rel="canonical" href="https://chlm.onrender.com/blog/{slug}.html">
    <style>{CSS_BASE}</style>
</head>
<body>
{NAV_HTML}
    <div class="breadcrumb"><a href="https://chlm.onrender.com/">首页</a> &rsaquo; <a href="https://chlm.onrender.com/blog/">博客</a> &rsaquo; <a href="https://chlm.onrender.com/blog/special/">专题文章</a> &rsaquo; {date_str}</div>
    <main class="container">
        <article>
            <header class="article-header">
                <h1>{title}</h1>
                <div class="article-meta">
                    <span>{date_str}</span>
                    <span>自动生成</span>
                    <span>{count} 条内容</span>
                </div>
            </header>
            <div class="ai-summary">
                <h2>今日要点</h2>
                <p>出海联盟@shouce每日精华内容汇总，涵盖出海实战经验、资源对接、行业洞察等深度内容。</p>
            </div>
            <div class="topics-bar">
                <span class="topic-tag">#出海干货</span>
                <span class="topic-tag">#实战经验</span>
                <span class="topic-tag">#资源对接</span>
                <span class="topic-tag">#行业洞察</span>
            </div>
            <section class="news-list">{items_html}
            </section>
{FOOTER_HTML}
            <footer class="article-footer">
                <p>出海联盟 CHLM - 海外最早的出海资源社区</p>
                <p style="margin-top:0.5rem;"><a href="https://t.me/chlm">订阅出海资讯频道</a> &middot; <a href="https://t.me/chgx">更多文章</a></p>
            </footer>
        </article>
    </main>
    <footer>
        <div class="footer-content">
            <div class="footer-links"><a href="https://chlm.onrender.com/">首页</a><a href="https://chlm.onrender.com/about.html">关于我们</a><a href="https://chlm.onrender.com/faq.html">常见问题</a><a href="https://chlm.onrender.com/resources.html">出海资源</a><a href="https://chlm.onrender.com/join.html">加入我们</a></div>
            <div class="footer-copy">&copy; 2019-2026 出海联盟 CHLM - 海外最早的出海资源社区</div>
        </div>
    </footer>
</body>
</html>'''

def make_blog_index(special_entries):
    """生成博客列表index.html"""
    special_html = ""
    for date_str, title, count, desc in special_entries:
        slug = f"special/{date_str}"
        special_html += f'''
        <div class="post-item">
            <div class="post-date">{date_str}</div>
            <div class="post-title"><a href="https://chlm.onrender.com/blog/{slug}.html">{title}</a></div>
            <div class="post-meta"><span>{count} 条内容</span><span>{desc}</span></div>
        </div>
'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>博客 - 出海联盟 CHLM</title>
    <meta name="description" content="出海联盟博客，提供每日出海资讯、广告投放干货、跨境营销策略等内容。">
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
        .container {{ max-width: 900px; margin: 0 auto; padding: 3rem 1.5rem; }}
        .page-header {{ margin-bottom: 3rem; border-bottom: 1px solid #2a2a4a; padding-bottom: 1.5rem; }}
        .page-header h1 {{ font-size: 2.5rem; color: #fff; margin-bottom: 0.5rem; }}
        .page-header p {{ color: #888; font-size: 0.95rem; }}
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
    <main class="container">
        <div class="page-header">
            <h1>博客</h1>
            <p>出海联盟每日资讯汇总，涵盖广告投放、SEO、AI工具等出海营销干货</p>
        </div>
        <div class="section-title">专题文章</div>
{special_html}
        <div class="section-title">每日资讯</div>
        <div class="post-item">
            <div class="post-date">2026-05-26</div>
            <div class="post-title"><a href="https://chlm.onrender.com/blog/daily/2026-05-26.html">出海资讯TG社群日报 2026年05月26日</a></div>
            <div class="post-meta"><span>9 条内容</span><span>菲律宾bc数据/TG注册码/筛料平台/SMS通道等出海资源</span></div>
        </div>
        <div class="post-item">
            <div class="post-date">2026-05-25</div>
            <div class="post-title"><a href="https://chlm.onrender.com/blog/daily/2026-05-25.html">出海资讯TG社群日报 2026年05月25日</a></div>
            <div class="post-meta"><span>12 条内容</span><span>Facebook/Google/TikTok广告、筛料平台、数据服务等出海资源</span></div>
        </div>
        <div class="post-item">
            <div class="post-date">2026-05-24</div>
            <div class="post-title"><a href="https://chlm.onrender.com/blog/daily/2026-05-24.html">出海资讯TG社群日报 2026年05月24日</a></div>
            <div class="post-meta"><span>1 条内容</span><span>WS拉群需求</span></div>
        </div>
        <div class="post-item">
            <div class="post-date">2026-05-23</div>
            <div class="post-title"><a href="https://chlm.onrender.com/blog/daily/2026-05-23.html">出海资讯TG社群日报 2026年05月23日</a></div>
            <div class="post-meta"><span>5 条内容</span><span>广告投放/SEO/AI工具/社媒引流实战技巧</span></div>
        </div>
        <div class="post-item">
            <div class="post-date">2026-05-22</div>
            <div class="post-title"><a href="https://chlm.onrender.com/blog/daily/2026-05-22.html">出海资讯TG社群日报 2026年05月22日</a></div>
            <div class="post-meta"><span>5 条内容</span><span>柬埔寨安全提醒、链上监测等资讯</span></div>
        </div>
    </main>
    <footer>
        <div class="footer-content">
            <div class="footer-links"><a href="https://chlm.onrender.com/">首页</a><a href="https://chlm.onrender.com/about.html">关于我们</a><a href="https://chlm.onrender.com/faq.html">常见问题</a><a href="https://chlm.onrender.com/resources.html">出海资源</a><a href="https://chlm.onrender.com/join.html">加入我们</a></div>
            <div class="footer-copy">&copy; 2019-2026 出海联盟 CHLM - 海外最早的出海资源社区</div>
        </div>
    </footer>
</body>
</html>'''


def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, cwd=WORKDIR, capture_output=True, text=True, encoding="utf-8")
        return r.stdout + r.stderr
    except Exception as e:
        return str(e)


async def main():
    print(f"[专题采集] 启动 {datetime.now().strftime('%Y-%m-%d %H:%M:%spush')}")

    date_str = datetime.now().strftime("%Y-%m-%d")
    date_display = datetime.now().strftime("%Y年%m月%d日")

    app = Client("auto_poster", api_id=API_ID, api_hash=API_HASH,
                 session_string=SESSION_STRING, workdir=str(TG_SESSION))
    await app.start()

    items = []
    seen = set()

    # 采集历史帖子（移除日期过滤，采集所有可用帖子）
    async for msg in app.get_chat_history("@shouce", limit=200):
        raw_text = msg.caption or msg.text or ""
        if not raw_text:
            continue
        text = raw_text[:1500]
        if len(text) < 20:
            continue
        key = text[:80]
        if key in seen:
            continue
        seen.add(key)
        src = msg.chat.username or msg.chat.title or "shouce"
        items.append((src, text))

    await app.stop()

    print(f"[采集] @shouce 今日获得 {len(items)} 条")

    if not items:
        print("[跳过] 没有新内容")
        return

    # 生成专题文章
    title = f"出海干货 @shouce {date_display}"
    slug = f"special/{date_str}"
    article_html = make_article(title, slug, date_str, date_display, len(items), items)

    specials_dir = BLOG_DIR / "special"
    specials_dir.mkdir(parents=True, exist_ok=True)
    article_path = specials_dir / f"{date_str}.html"
    article_path.write_text(article_html, encoding="utf-8")
    print(f"[生成] {article_path.name}")

    # 更新博客列表
    # 读取已有专题文章
    existing_specials = []
    for f in sorted((BLOG_DIR / "special").glob("*.html"), reverse=True)[:10]:
        fname = f.stem  # e.g. 2026-05-26
        html_content = f.read_text(encoding="utf-8")
        # 从标题中提取日期描述
        m = re.search(r"出海干货 @shouce (\d{4}年\d{1,2}月\d{1,2}日)", fname.replace("-", ""))
        if not m:
            m = re.search(r"(\d{4}-\d{2}-\d{2})", fname)
        date_for_list = fname  # use filename
        # 从文件读取标题
        title_m = re.search(r"<title>(.*?) - 出海联盟 CHLM</title>", html_content)
        item_title = title_m.group(1) if title_m else fname
        # 读取条数
        count_m = re.search(r"<span>(\d+) 条内容</span>", html_content)
        count = count_m.group(1) if count_m else "?"
        existing_specials.append((date_for_list, item_title, count, "出海实战经验与行业洞察"))
        print(f"  已有专题: {date_for_list} - {item_title[:40]}")

    blog_index_html = make_blog_index(existing_specials)
    (BLOG_DIR / "index.html").write_text(blog_index_html, encoding="utf-8")
    print(f"[更新] blog/index.html")

    # Git push
    changes = run_cmd(["git", "status", "--porcelain"])
    if not changes.strip():
        print("[跳过] 没有内容变更")
        return

    run_cmd(["git", "add", str(article_path.relative_to(WORKDIR)), "blog/index.html"])
    run_cmd(["git", "commit", "-m", f"专题文章: @shouce {date_display} ({len(items)}条)"])
    result = run_cmd(["git", "push", "https://github.com/jerryandmytom-cyber/chlm", "main"])
    print(f"[推送] 完成")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 测试模式：从已存在的文件中更新列表
        existing_specials = []
        for f in sorted((BLOG_DIR / "special").glob("*.html"), reverse=True)[:10]:
            fname = f.stem
            html_content = f.read_text(encoding="utf-8")
            title_m = re.search(r"<title>(.*?) - 出海联盟 CHLM</title>", html_content)
            item_title = title_m.group(1) if title_m else fname
            count_m = re.search(r"<span>(\d+) 条内容</span>", html_content)
            count = count_m.group(1) if count_m else "?"
            existing_specials.append((fname, item_title, count, "出海实战经验与行业洞察"))

        blog_index_html = make_blog_index(existing_specials)
        (BLOG_DIR / "index.html").write_text(blog_index_html, encoding="utf-8")
        print(f"[OK] 更新 blog/index.html，专题文章共 {len(existing_specials)} 篇")
        print(f"[推送] ", end="")
        print(run_cmd(["git", "add", "blog/index.html"]))
        print(run_cmd(["git", "commit", "-m", "更新博客列表：专题文章同步"]))
        print(run_cmd(["git", "push", "https://github.com/jerryandmytom-cyber/chlm", "main"]))
    else:
        asyncio.run(main())
