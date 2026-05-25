import os
from pathlib import Path

FOOTER_BLOCK = '''
            <div class="chlm-footer">
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
            </div>
'''

FOOTER_CSS = '''
        .chlm-footer { background: linear-gradient(135deg, #1a2a4a, #0d1f30); border: 1px solid #2a4a6a; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; text-align: left; }
        .footer-brand { font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.8rem; }
        .footer-brand a { color: #4fc3f7; }
        .footer-desc { color: #aaa; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem; }
        .footer-section { color: #4fc3f7; font-weight: 600; font-size: 0.85rem; margin: 0.8rem 0 0.4rem; }
        .footer-channels { color: #ccc; font-size: 0.85rem; line-height: 1.8; }
        .footer-staff { color: #ccc; font-size: 0.85rem; line-height: 1.8; margin-top: 0.5rem; }
        .footer-cta { color: #4fc3f7; font-size: 0.9rem; font-weight: 600; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #2a4a6a; }
        .article-footer { margin-top: 0; padding-top: 1.5rem; border-top: none; }
'''

def add_footer_to_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    
    # Add footer CSS to existing style block (before closing </style>)
    if '.chlm-footer' not in content:
        content = content.replace('        @media (max-width: 768px) {', FOOTER_CSS + '\n        @media (max-width: 768px) {')
    
    # Add footer block before article-footer
    if FOOTER_BLOCK.strip() not in content:
        content = content.replace(
            '            <footer class="article-footer">',
            FOOTER_BLOCK + '\n            <footer class="article-footer">'
        )
    
    filepath.write_text(content, encoding='utf-8')
    print(f"[更新] {filepath.name}")

# Process all daily HTML files
daily_dir = Path("C:/Users/win11/.openclaw/workspace/chlm-website/blog/daily")
for f in sorted(daily_dir.glob("*.html")):
    add_footer_to_file(f)

print("\n✅ 全部更新完成")