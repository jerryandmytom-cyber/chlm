# 出海联盟 - 每日自动内容生成

## 功能

每天自动从 `@quanqiutufa` 频道收集当天帖子，生成博客文章并推送 GitHub → Render 自动部署。

## 使用方法

### 手动运行

```bash
cd C:\Users\win11\.openclaw\workspace\chlm-website

# 设置环境变量
$env:API_ID="31647981"
$env:API_HASH="956c44a96af04e285ab9b27e453e44ca"
$env:SESSION_STRING="..."

python auto_daily.py
```

### 自动运行（每日早上9点）

```bash
openclaw cron add --name "chlm-daily" \
  --schedule "cron 0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session-target isolated \
  --payload-kind agentTurn \
  --payload-message "运行: cd C:\Users\win11\.openclaw\workspace\chlm-website; python auto_daily.py"
```

## 输出

- `blog/daily/YYYY-MM-DD.html` - 每日资讯文章
- `sitemap.xml` - 自动更新

## 依赖

- pyrogram
- 已有 Telegram 会话（在 tg-auto-poster 中）

## 流程

1. 连接 Telegram 读取 @quanqiutufa 频道当天消息
2. 清理文本（移除链接、@、#等）
3. 生成结构化 HTML 博客文章
4. 更新 sitemap.xml
5. Git commit + push → Render 自动部署