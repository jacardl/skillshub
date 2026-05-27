# html-anything MCP Server 接入参考

> ⚠️ **用户当前偏好：禁用 HTML 渲染。** 关键词研究和策略报告只输出 Markdown，不调用 html-anything。本文件仅作技术存档参考。

## 概述

`html-anything` 是一个本地 Next.js 应用，托管于 `http://localhost:3000`。它通过调用本地安装的 Coding Agent CLI（Claude Code 等）将内容渲染为 HTML。

## 架构

```
Hermes → MCP client (Python/stdio) → localhost:3000/api/convert → Claude Code CLI → SSE HTML stream
```

MCP server 脚本位置：`~/.hermes/mcp-servers/html-anything/server.py`

## 调用方式

### 方式1：直接 HTTP 调用（推荐，用于 Skill 自动化）

```python
import urllib.request, json

payload = json.dumps({
    "agent": "claude",
    "templateId": "data-report",  # 模板ID，见下表
    "content": "# 报告标题\n\n报告正文...",
    "format": "text"
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:3000/api/convert",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

resp = urllib.request.urlopen(req, timeout=180)
body = resp.read().decode("utf-8", errors="ignore")

# 解析 SSE，提取 HTML
html_parts = []
for line in body.split('\n'):
    if line.startswith('data: '):
        try:
            d = json.loads(line[6:])
            if d.get('type') == 'delta':
                html_parts.append(d['text'])
            elif d.get('type') == 'done':
                break
        except:
            pass

full_html = ''.join(html_parts)
```

### 方式2：MCP stdio 协议（已配置在 config.yaml）

```yaml
mcp_servers:
  html-anything:
    command: python3
    args: ["/Users/apple/.hermes/mcp-servers/html-anything/server.py"]
```

工具名：`mcp_html-anything_convert`，`mcp_html-anything_list_templates`，`mcp_html-anything_list_agents`

## 可用模板 ID

| 模板ID | 名称 | 适用场景 |
|--------|------|----------|
| data-report | 数据报告 | 分析报告、舆情报告 |
| article-magazine | 杂志文章 | 长文排版 |
| blog-post | 博客文章 | 博客风格 |
| deck-guizang-editorial | 贵志杂志风幻灯片 | 演示文稿 |
| deck-swiss-international | 瑞士国际风幻灯片 | 演示文稿 |
| deck-hermes-cyber | 爱马仕赛博风 | 演示文稿 |
| card-xiaohongshu | 小红书卡片 | 社交卡片 |
| card-twitter | X/Twitter 卡片 | 社交卡片 |
| doc-kami-parchment | 和纸羊皮卷文档 | 文档 |

## 服务管理

```bash
# 启动（工作目录 /tmp，用于 HTTP 预览服务）
python3 -m http.server 8765

# 检查 html-anything 服务是否在线
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# 检查已安装的 Coding Agent
curl -s http://localhost:3000/api/agents | python3 -c "import json,sys; d=json.load(sys.stdin); print('已安装:', d['installedCount'])"
```

## 输出流程

1. 生成 HTML → 保存到 `~/final_report/<分类>/<name>.html`
2. 确保 `python3 -m http.server 8765` 运行中（工作目录 `/tmp`）
3. 发给用户：`http://localhost:8765/<文件名>.html`

## 已知问题

- 生成超时：Claude Code 首次启动较慢，建议 timeout 设为 180s
- SSE 解析：只处理 `data: ` 开头的 JSON 行，`event: xxx` 行忽略
- 生成大报告时 HTML 可能超过 50KB，注意文件大小