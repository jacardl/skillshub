---
name: radar-data-collection
description: 雷达数据采集 Skill — 采集金价、国际政治、AI热讯，写入 PostgreSQL 向量数据库，验证新闻真实性，按日期归档。
metadata: { "openclaw": { "emoji": "🛰️" } }
---

# 雷达数据采集 Skill

每日 06:00 北京时间执行。采集金价、国际政治、AI热讯，写入 `radar` 数据库的 `news_articles` 和 `gold_prices` 表。

## 数据源

| 类型 | 来源 | 数量 |
|------|------|------|
| 国际金价 | Kitco（伦敦现货，USD/盎司）| 1 条 |
| 国内金价 | 权威国内平台（沪金现货，CNY/克）| 1 条 |
| 国际政治 | 9Router tavily 搜索 | 10 条 |
| AI热讯 | aihot.virxact.com 精选 | 10 条 |

## 采集步骤

### 第一步：确认日期
```bash
date -d '+8 hour' '+%Y-%m-%d'
```
article_date = 北京时间今天日期

### 第二步：采集金价（browser CDP）

1. 用 browser 工具打开 https://www.kitco.com/charts/livegold.html
2. 提取伦敦现货金价（USD/盎司）
3. 国内金价用 9Router 搜索"沪金现货 今日价格"
4. 计算涨跌幅度

字段：`intl_price_usd`, `intl_price_change`, `domestic_price_cny`, `domestic_price_change`

### 第三步：采集国际政治（9Router tavily）

搜索 query：`international political news today`
筛选来源：Reuters / AP / AFP / Al Jazeera / BBC / FT
验证：每条必须附来源 URL，缺失则丢弃

**内容增强要求（强制，服务下游推送）**
1. 每条必须生成 **中英对照标题**：
   - 中文标题（意译清楚）
   - English Headline（保留原文）
2. 每条必须生成 **事件介绍**（至少2句）：
   - 句1：发生了什么（核心事实）
   - 句2：背景或潜在影响（为什么值得关注）
3. 国际政治采集目标：**10~12条**（优先覆盖亚太 / 中东·欧洲 / 美洲）
4. 若原始结果只有标题，需对来源页做一次抓取补全摘要（9Router fetch-combo 或 scrapling）

字段写入规范：
- `title`：写中文标题（便于推送直读）
- `content`：按固定模板存储：
  ```
  中文标题：...
  English Headline: ...
  事件介绍：...
  背景/影响：...
  ```
- `source`, `url`, `category='politics'`, `lang='zh'`

### 第四步：采集 AI 热讯（aihot.virxact.com）

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 aihot-skill/0.2.0"
curl -s -H "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/items?mode=selected&take=10"
```

解析返回的 JSON，取 `title`、`publishedAt`、`summary`、`source`、`url`
字段：`category='ai'`, `lang='zh'`

### 第五步：向量 embedding（Ollama 本地）

```bash
# Ollama 地址（nomic-embed-text，768维）
OLLAMA_URL="http://localhost:11434/api/embeddings"
MODEL="nomic-embed-text"

# 对每条 title+content（前500字）调用 embedding
curl -s -X POST "$OLLAMA_URL" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"prompt\":\"$TEXT\"}" \
  | python3 -c "import sys,json; print(','.join(map(str,json.load(sys.stdin)['embedding'])))"
```

维度 768，写入 `embedding` 字段（格式：`'[v1,v2,...]'`）。

### 第六步：写入数据库

```bash
# 金价写入
docker exec radar-db psql -U radar -d radar -c \
  "INSERT INTO gold_prices (price_date, intl_price_usd, intl_price_change, domestic_price_cny, domestic_price_change)
   VALUES ('${ARTICLE_DATE}', ${INTL_PRICE}, ${INTL_CHANGE}, ${DOMESTIC_PRICE}, ${DOMESTIC_CHANGE})
   ON CONFLICT (price_date) DO UPDATE SET
     intl_price_usd = EXCLUDED.intl_price_usd,
     intl_price_change = EXCLUDED.intl_price_change,
     domestic_price_cny = EXCLUDED.domestic_price_cny,
     domestic_price_change = EXCLUDED.domestic_price_change;"

# 新闻写入（每条一条INSERT）
docker exec radar-db psql -U radar -d radar -c \
  "INSERT INTO news_articles (article_date, category, title, content, source, url, lang, embedding)
   VALUES ('${ARTICLE_DATE}', '${CATEGORY}', '${TITLE}', '${CONTENT}', '${SOURCE}', '${URL}', '${LANG}',
           '[${EMBEDDING}]');"
```

### 第七步：验证数据

采集完成后执行：
```sql
SELECT article_date, category, COUNT(*) FROM news_articles GROUP BY article_date, category;
SELECT * FROM gold_prices WHERE price_date = '${ARTICLE_DATE}';
```
确认条数符合预期（国际政治≥10条，aihot≥8条），缺条则补采。

并抽查国际政治结构完整性（必须含中英对照+事件介绍）：
```sql
SELECT COUNT(*) FROM news_articles
WHERE article_date='${ARTICLE_DATE}' AND category='politics'
  AND content LIKE '%English Headline:%'
  AND content LIKE '%事件介绍：%';
```
若不达标，继续补采并覆盖更新。

## 数据库连接

```
Host: localhost:5444
Database: radar
User: radar
Password: radar
```

连接方式：`docker exec radar-db psql -U radar -d radar -c "SQL"`

## 错误处理

- 向量API失败：跳过 embedding，先写入文本数据，稍后重试
- 网络超时：最多重试2次，间隔30秒
- 数据不足：发送飞书通知给用户，说明缺条原因
- 所有异常记录到 `memory/YYYY-MM-DD.md`

## 输出

完成后输出简洁报告：
```
🛰️ 数据采集完成 [日期]
✅ 金价：国际 ${INTL_PRICE} (${CHANGE}) / 国内 ${DOMESTIC_PRICE}
✅ 国际政治：${N} 条
✅ AI热讯：${N} 条
⏱️ 耗时：${SEC}s
```