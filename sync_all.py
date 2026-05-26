# -*- coding: utf-8 -*-
from pathlib import Path

BASE = Path("C:/Users/win11/.openclaw/workspace/chlm-website/blog/daily")

FOOTER = """
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

CSS = """
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
        .footer-cta { color: #4fc3f7; font-size: 0.9rem; font-weight: 600; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #2a4a6a; }
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

NAV = '''    <header>
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

def esc(t):
    return t.replace("&", "&").replace("<", "<").replace(">", ">")

def build_html(date_str, date_display, count, items):
    title = f"出海资讯TG社群日报 {date_display}"
    if not items:
        ih = "\n                <p style='color:#888;text-align:center;padding:2rem;'>今日暂无相关新内容，请稍后再访问。</p>\n"
    else:
        ih = ""
        for src, text in items:
            ih += f"\n                <div class=\"news-item\">\n                    <div class=\"news-source\">{esc(src)}</div>\n                    <div class=\"news-text\">{esc(text)}</div>\n                </div>\n"

    # Extract raw news content for each file
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 出海联盟 CHLM</title>
    <meta name="description" content="出海联盟{date_display}广告投放与营销干货资讯汇总，覆盖Facebook、Google、TikTok、Instagram、Telegram等平台投放策略及AI工具应用。">
    <meta property="og:title" content="{title}">
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{date_str}">
    <link rel="canonical" href="https://chlm.onrender.com/blog/daily/{date_str}.html">
    <style>{CSS}</style>
</head>
<body>
{NAV}
    <div class="breadcrumb"><a href="https://chlm.onrender.com/">首页</a> &rsaquo; <a href="https://chlm.onrender.com/blog/">博客</a> &rsaquo; <a href="https://chlm.onrender.com/blog/daily/">每日资讯</a> &rsaquo; {date_str}</div>
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
            <section class="news-list">{ih}
            </section>
{FOOTER}
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

# ===== 数据 =====
items_22 = [
    ("quanqiutufa", "05月22日\n回应一下上面柬埔寨乱抓人的乱象：\n现在为什么还有人去那边打工，从严打的时候老早就说了已经在抓中国人，现在中国人在柬埔寨政府完完全全是猪仔，被抓了，真要想出来花几万美金是可以飞第三方国家的，移民局飞三方国家标价5万u起，如果没有这个经济实力，还不如在家打打螺丝赚点生活费，起码能保持一个安稳，现在在安置点的兄弟们也不用操心，你们大概一个月左右就可以回到中国，你们没有在园区内工作的话，公安大概也就是调查一下就会把你们放回户籍地。金边移民局安置点的物价也没有想象的那么高，都是可以接受的程度。移民局每天免费提供两顿饭。安置点要自己出钱吃饭。总而言之一句话，现在柬埔寨政府已经是疯狗了。如果有意向去柬埔寨的，不是非必要慎重前往。"),
    ("quanqiutufa", "05月22日\n金边金爵或者JJHC公告声明\nPS：今晚都去金爵玩商k"),
    ("quanqiutufa", "05月22日\n波贝的团队搬到拜林？拜林查电诈发现大量手机和路由器\n今天（5月22日），拜林省长继续率队在沙拉考人口密集区域检查电诈，查获大量手机和路由器，疑似是网络诈骗团伙用于诈骗活动的设备。"),
    ("quanqiutufa", "05月22日\n近日泰国普吉岛卡林海滩上，一名身材高挑、金色头发的外籍女游客在众目睽睽之下脱光衣物，于岩石及树枝上摆姿势拍摄裸照，同行朋友负责拍照。当时海滩上还有其他游客及当地居民在钓鱼，众人纷纷围观，但该女子毫不在意。此事经社交媒体发布后，引发网友强烈批评。"),
    ("quanqiutufa", "05月22日\n链上侦探   监管严打跨境券商，RWA龙头ONDO短时上扬7%\nBlockBeats 消息，5月22日，据HTX行情信息，RWA板块龙头Ondo Finance原生代币ODO短时拉涨7.3%，高点触及0.44美元，现回落至0.427美元，近5日已自低点累计上涨29%。此轮短时上扬发生在证监会严肃查处老虎等机构非法跨境展业相关消息见诸报端之后。另据Hyperinsight监测，Hyperliquid上某交易员于6日前以6.8万美元本金建仓做多ODO，彼时价格约0.36美元。截至发稿，该笔多单已浮盈11.7万美元，回报率达173%。"),
]

items_23 = [
    ("雨果跨境", "【独立站推广运营方式全解】\n\n独立站推广是跨境电商获取自然流量的核心渠道。以下是主流推广方式：\n\nNO.1 SEO优化 - 通过关键词布局、外链建设提升谷歌排名，获取免费精准流量\nNO.2 社交媒体矩阵 - Facebook、TikTok、Instagram 多平台联动，精准截流同行客户\nNO.3 付费广告投放 - Google Ads + Facebook 广告投放，精准定向目标人群\nNO.4 网红营销 - 找与品牌调性相符的海外红人合作，提升信任度\nNO.5 内容营销 - 博客文章、视频内容持续输出，建立品牌权威性\n\n适合外贸、跨境电商、独立站、品牌出海。#独立站 #SEO #Facebook广告 #TikTok营销"),
    ("跨境数字营销", "【2026年广告架构搭建终极策略】\n\n无论您是初创团队还是成熟企业，以下策略帮您把每一分预算花在刀刃上：\n\n1. 受众分层 - 将用户分为 Awareness、Consideration、Conversion 三个阶段\n2. 创意素材 - 视频素材点击率比图片高3倍，建议每组广告准备5+视频\n3. 出价策略 - 新品期采用TCPA（目标每次转化费用），稳定后转ROAS\n4. 跨平台协同 - Facebook重品牌认知、TikTok重引流种草、Google重搜索转化\n5. A/B测试 - 每周至少测试2组广告创意，保留表现Top20%\n\n广告架构的核心是用数据驱动决策，而非凭感觉投放。#广告投放 #Facebook #TikTok #GoogleAds"),
    ("出海运营派", "【AI外贸工具实战应用】\n\n2026年AI在跨境营销中的应用已成标配，以下是几个高频场景：\n\n1. AI选品 - 通过分析亚马逊畅销榜单、Google Trends，批量生成潜力选品报告\n2. AI客服 - 7x24小时自动回复买家询盘，多语言支持降低人力成本\n3. AI内容生成 - Facebook Caption、TikTok脚本、Email营销文案一键生成\n4. AI广告素材 - Midjourney生成广告图，HeyGen生成数字人视频\n5. AI数据分析 - 自动识别广告账户异常，避免预算浪费\n\n推荐工具：ChatGPT（文案）、Midjourney（设计）、Shopify Epilot（选品）、Perplexity（市场调研）#AI工具 #外贸工具 #跨境电商"),
    ("独立站学堂", "【Facebook广告投放避坑指南】\n\n01 账户被封的常见原因：\n- 多个广告账户使用同一付款方式\n- 推广页内容与实际产品不符\n- 新账户直接大量投放高预算广告\n- 违规产品或擦边内容\n\n02 像素设置三大原则：\n- 网站安装像素后至少积累50+转化事件再开启转化优化\n- 每次事件Campaign不要超过3个，避免相互抢量\n- 定期查看像素数据报告，清理无效流量\n\n03 受众设置雷区：\n- 避免重叠率超过30%的自定义受众组合\n- 再营销受众不要选择最近180天内的用户，容易疲劳轰炸\n- Lookalike受众建议选择1%源受众，精准度最高 #Facebook广告 #广告投放 #独立站"),
    ("社媒增长日记", "【Instagram+TikTok双平台联动引流技巧】\n\n很多出海团队只做TikTok或只做Instagram，效果打折扣。双平台联动才是最优解：\n\n1. 内容差异化：Instagram主打精致图文和Stories，营造品牌调性；TikTok主打短视频和直播，快速引流转化\n2. 互动话题：TikTok发起挑战赛，Instagram引流用户参与并UGC产出\n3. 账号矩阵：一个主账号+多个垂直小号，主账号引流、小号沉淀私域\n4. KOC营销：找100-500粉丝的垂直小博主，性价比高于头部达人\n5. 评论区营销：在竞品账号下真实互动，吸引潜在用户关注\n\nInstagram Reels与TikTok视频可同步发布，一份素材双平台分发，效率翻倍。#Instagram #TikTok #私域流量 #出海营销"),
]

items_24 = [
    ("@CHGX-供需频道", "序号：包月 类型：需求\n商品：ws拉群\n协议拉群 保开群 不用保时间200-400都可以来聊\n\n联系人：@ADG18418\n交易方式：支持出海担保\n标签：#出海 #WS拉群 #出海联盟 #出海供需 #担保 #供应 #需求"),
]

items_25 = [
    ("@CHGX-供需频道", "序号：包月 类型：需求\n商品：收TG注册码\n无限收！无限收！无限收！\n收注册码，号有价格优势的也收\n欧洲首次卡/亚洲首次卡/非洲首次卡\n支持测试的来，先款的勿扰\n测试可用，直接包量\n火狐狸、api链接码皆可\n\n联系人：@ZhuanJia 专家\n交易方式：支持出海担保\n标签：#出海 #TG注册码"),
    ("@CHGX-供需频道", "序号：54554 类型：需求\n商品：ws拉群\n协议拉群 保开群 不用保时间200-400都可以来聊\n\n联系人：@ADG18418\n交易方式：支持出海担保\n标签：#出海 #WS拉群"),
    ("@CHGX-供需频道", "序号：包月 类型：供应\n\n菠萝筛料平台@ShaiLiao\n优势：源头渠道，价廉高效；自助充值，自助筛选；24小时全天候运营；准确率高，速度快\n郑重承诺：菠萝平台只筛料不卖料，数据安全有保障！\n客服：@YingLi\n已在出海联盟上押5000U 公群链接https://t.me/chgq11\n\n交易方式：支持出海担保\n标签：#出海 #筛料 #代筛"),
    ("@CHGX-供需频道", "类型：供应\n商品：SMS高质量通道\n澳大利亚/加拿大/英国/日本/葡萄牙/丹麦/瑞典/荷兰/德国/波兰/捷克/瑞士 自建机房双向短信\n\n单向改外显短信：葡萄牙，西班牙改外显短信火热进行中\nBC单向短信：镁国/加拿大/法国/澳大利亚/日本/意大利/墨西哥/香港\n\n联系人：https://t.me/JIUSUO88888\n产品频道：https://t.me/whatsapp1331\n\n标签：#出海 #双向短信"),
    ("@CHGX-供需频道", "序号：54553 类型：供应\n\n商品：公司直供批发价出TG原始群/超群/科技群/打粉号/直登/协议号/接码号/api号 FB/IG/TK/推特/抖音/灵魂/小红书等各类主流App号子\n\n全网最低价出售TG老群/超群/原始群/科技群/实卡群（全球任何国家可用）2017年～2025年\n各国WS直登号新老号/协议号/劫持号\n\n联系人：@Ll000006\n产品频道：https://t.me/LL00zscs\n交易方式：支持出海担保\n\n标签：#出海 #TG老群 #WS直登号"),
    ("@CHGX-供需频道", "序号：公群 类型：供应\n\n头家一站式出海服务平台，已在出海联盟上押5000u\n平台板块：筛料系统+短信群发板块+otp/云控/电销系统（开发中）\n优势：可开后台、24H自助充值筛料、价低高效\n\n频道：@TouJia007\n\n交易方式：支持出海担保\n标签：#出海 #筛料 #代筛"),
    ("@CHGX-供需频道", "序号：54552 类型：供应\n商品：菲律宾、印尼、韩国二道/泰国二道，真正一手源头代收付通道\n\n公私户钱包充足，线上线下代收代付业务\n1.印尼二三类业务：大区/资金盘/精聊/刷单/换汇/贷款/商城/直播/冒充等\n2.菲律宾全品类业务API：BC/大区/资金盘/精聊/刷单/换汇/贷款/商城/直播/冒充/渗透/盗刷等等\n3.泰国保时、无视进算车\n4.进算接泰国二道 韩国二道\n\n五年老通道，稳定效率高，源头价优，欢迎各大盘总和中介四方合作\n\n联系人：@jufengguoji9\n\n标签：#出海 #支付 #通道"),
    ("@CHGX-供需频道", "序号：季度 类型：供应\n\n出海联盟季度供应商品：\n1.iFanseek镁国双向短信平台源头：纯美卡、基本不封卡，有绝对优势；可发图片链接\n2.WS满月可解封直登老号：每天循环超链3轮或每天接粉20个，可无限复接解封\n3.WS高混五段扫码json号，拉群优质\n4.WS满月二三月自养老号\n5.WS当天号\n\n联系人：山峰机房 @Hillpeak11\n产品频道：@SFwsxieyihao\n交易方式：支持担保交易\n\n标签：#出海 #WS直登号 #机房"),
    ("@CHGX-供需频道", "序号：54551 类型：需求\n\n商品：大量收7天以上WS协议号旧包，欢迎各位机房大哥对接 各国协议都收 价格市场最高\n收出售过的ws号包\n欢迎各位机房老号和盘口老总对接\n\n联系人：@kelaienws99\n\n交易方式：支持出海担保\n标签：#出海 #WS协议号"),
    ("@CHGX-供需频道", "序号：包月 类型：供应\n\n新火源头筛料平台，可放api\nTelegram筛活跃，市场最低价，时速五百万\n全球热门App皆可筛选\n优势：源头筛料渠道，可开后台，可放api，自助充值，24小时自助筛料\n\n官方频道：@xinhuo\n已在出海联盟上押5000u，公群链接：@CHGQ23\n\n交易方式：支持出海担保\n标签：#出海 #筛料 #代筛"),
    ("@CHGX-供需频道", "序号：包月 类型：供应\n\n航海全球数据全球数据源头，已担保公群上压10000u支持担保，安全交易\n\n全球数据系列：币安/欧易/精聊/快杀/白领/招聘/购物/领英/办公/苹果/支付/TG\n印度数据系列：航空/商户/支付/房产/白领/外卖/招聘/购物/基金/股票/投资/奢侈/银行/珠宝/博彩/家具\n巴西/墨西哥/英国/法国/美国/马来/泰国/越南等\n接全球数据代筛服务WS/TG/line/zalo/FB/ins/领英/微软/办公/亚马逊\n支持各类高端定制数据，底料代筛\n\n联系人：@hanghai1688\n频道：@hhai168888\n在线营业时间：12:00-凌晨2:00\n\n交易方式：支持出海担保\n标签：#出海 #数据 #渗透"),
    ("@CHGX-供需频道", "序号：公群 类型：供应\n\n四方数据全球精聊数据源头，已担保上押108888\n\n全球源头一手最新实时数据、渗透全格式\n海外数据：航空/旅游/酒店/消费/网赚/电商/支付/白领/招聘/领英/车主/房主/币安/欧意/银行/苹果/精聊/购物/WS/TG/交友/美容/企业/贷款/抵押/华人\n全球数据都有，量大管饱\n全网最低价代筛整个国家ws/TG\n\n公群地址：https://t.me/chgq36\n\n交易方式：支持出海担保\n\n标签：#出海 #数据 #料子"),
]

# Read actual content from 2026-05-26 auto-generated file
fp26 = BASE / "2026-05-26.html"
raw26 = fp26.read_text(encoding="utf-8")

# Extract news items from raw HTML
import re
news_blocks = re.findall(r'<div class="news-item">(.*?)</div>\s*<div class="news-item">|<div class="news-item">(.*?)</div>\s*<div class="chlm-footer', raw26, re.DOTALL)
items_26 = []
for block in re.findall(r'<div class="news-item">(.*?)</div>\s*(?=<div class="news-item">|<div class="chlm-footer)', raw26, re.DOTALL):
    src_m = re.search(r'news-source">(.*?)</div>', block)
    txt_m = re.search(r'news-text">(.*?)</div>', block, re.DOTALL)
    if src_m and txt_m:
        src = src_m.group(1).strip()
        txt = re.sub(r'<[^>]+>', '', txt_m.group(1)).strip()
        items_26.append((src, txt))

data = [
    ("2026-05-22", "2026年05月22日", len(items_22), items_22),
    ("2026-05-23", "2026年05月23日", len(items_23), items_23),
    ("2026-05-24", "2026年05月24日", len(items_24), items_24),
    ("2026-05-25", "2026年05月25日", len(items_25), items_25),
    ("2026-05-26", "2026年05月26日", len(items_26), items_26),
]

print(f"Items 26 count: {len(items_26)}")
for d in data:
    date_str, date_display, count, items = d
    html = build_html(date_str, date_display, count, items)
    p = BASE / f"{date_str}.html"
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] {date_str}.html ({count} items)")
print("All done!")