---
name: radar-daily-report
description: 雷达每日报告推送 Skill — 从 PostgreSQL 读取今日数据，组装三条飞书消息（金价 / AI热讯+国际政治 / GitHub黑马），周六发周报，月末发月报。
metadata: { "openclaw": { "emoji": "📡" } }
---

# 雷达每日报告推送 Skill

每日 07:00 北京时间执行。从 `radar` 数据库读取今日数据，发送三条飞书消息。

## 执行步骤

### 第一步：确认日期和报告类型

```bash
date -d '+8 hour' '+%Y-%m-%d'
date -d '+8 hour' '+%u'
date -d '+8 hour' '+%d'
```

- 星期几（1=周一 ... 6=周六, 7=周日）
- 今天是否月末（dd == 每月最后一天？）

报告类型判断：
- 每月最后一天 → **黑马月报**（数据来源 `?since=monthly`）
- 周六 → **黑马周报**（数据来源 `?since=weekly`）
- 其他 → **黑马日报**（数据来源 无参数URL）

### 第二步：从数据库读取金价

```bash
docker exec radar-db psql -U radar -d radar -t -c \
  "SELECT intl_price_usd, intl_price_change, domestic_price_cny, domestic_price_change
   FROM gold_prices WHERE price_date = '${ARTICLE_DATE}';"
```

格式：「国际金价 ${INTL} USD/盎司（${CHANGE}%）」「国内金价 ${DOMESTIC} 元/克」

### 第三步：从数据库读取新闻

```bash
# AI热讯
docker exec radar-db psql -U radar -d radar -t -c \
  "SELECT title, source, url FROM news_articles
   WHERE article_date = '${ARTICLE_DATE}' AND category = 'ai'
   ORDER BY blacklist_score DESC NULLS LAST LIMIT 10;"

# 国际政治
docker exec radar-db psql -U radar -d radar -t -c \
  "SELECT title, source, url FROM news_articles
   WHERE article_date = '${ARTICLE_DATE}' AND category = 'politics'
   ORDER BY blacklist_score DESC NULLS LAST LIMIT 10;"
```

> 国际政治内容增强要求（强制）：
> 1) 每条必须 **中英对照**（中文标题 + English Headline）
> 2) 每条必须有 **事件介绍**（至少 2 句：发生了什么 + 背景/影响）
> 3) 禁止只贴标题；需要可读摘要
> 4) 若数据库仅有标题，需基于来源链接补充一句背景信息后再输出

### 第四步：采集 GitHub 黑马数据

用 curl 直接采集 GitHub Trending：
- 日报 → `https://github.com/trending`
- 周报 → `https://github.com/trending?since=weekly`
- 月报 → `https://github.com/trending?since=monthly`

黑马分算法：
```
黑马分 = 周期新增⭐ × 小项目加成 × 新项目加权
小项目加成：<5k ×2.0 | 5k~20k ×1.5 | 20k~100k ×1.0 | ≥100k ×0.8
新项目加权（创建<30天）：×1.5
```

取前 10 条，每条附：序号、名称（语言）⭐总stars | 周期新增、增长率、是否新项目、黑马分、简介、链接

### 第五步：发送三条飞书消息

---

**消息一：💰 生活服务**
```
💰 国际金价
伦敦现货：${INTL_PRICE} USD/盎司（${INTL_CHANGE}）
沪金现货：${DOMESTIC_PRICE} 元/克（${DOMESTIC_CHANGE}）

📊 简评：${COMMENT}
💡 建议：${SUGGESTION}
```

---

**消息二：🌐 资讯速递**
```
🤖 AI热讯
1. [标题]（来源 · 时间）
2. ...

🌍 国际政治（中英对照版）
🔴 亚太
1. 中文标题：...
   English Headline: ...
   事件介绍：...（发生了什么）...（背景或影响）
   来源：Reuters/AP/AFP/BBC/FT

🔵 中东·欧洲
1. 中文标题：...
   English Headline: ...
   事件介绍：...（发生了什么）...（背景或影响）
   来源：...

🟢 美洲·其他
1. 中文标题：...
   English Headline: ...
   事件介绍：...（发生了什么）...（背景或影响）
   来源：...
```

国际政治写作规范：
- 每条事件介绍建议 60~120 字中文，信息密度优先
- 中文标题要意译清楚，英文标题保留原文关键信息
- 至少覆盖 5 条国际政治事件（不足则标注“今日可验证国际政治事件不足”）

---

**消息三：💻 开源黑马**（${REPORT_TYPE}）

**黑马日报🌙 / 黑马周报🌅 / 黑马月报🌕**

| # | 项目 | 语言 | 总⭐ | 周期新增 | 增长率 | 🆕 | 黑马分 |
|---|------|------|------|----------|--------|-----|--------|
| 1 | xxx | Python | 12.3k | +2.1k | +21% | 🆕 | 3150 |

每条附链接：https://github.com/owner/repo

---

### 第六步：存档

将三条消息合并存档到：
```
workspace/daily-reports/YYYY-MM-DD.md
workspace/daily-reports/YYYY-MM-DD-gh.md（黑马部分）
```

## 数据库连接

```
Host: localhost:5444
Database: radar
User: radar
Password: radar
```

## 错误处理

- 数据库无今日数据：发送「数据采集中，请稍后」并标记
- GitHub curl 失败：最多重试2次，换 CloakBrowser 兜底
- 缺条（国际政治<10条/aihot<10条）：报告中标注「部分数据待补充」
- 所有异常记录到 `memory/YYYY-MM-DD.md`

## 输出

发送完成后输出：
```
📡 每日报告推送完成 [日期]
💰 金价：国际 ${INTL} / 国内 ${DOMESTIC}
🌐 资讯：AI热讯 ${N}条 + 国际政治 ${N}条
💻 黑马：${REPORT_TYPE} ${N}条
⏱️ 耗时：${SEC}s
```