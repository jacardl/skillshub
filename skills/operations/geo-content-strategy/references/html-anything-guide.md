# html-anything 工具链整合笔记

## 安装状态（2026-05-19）

- html-anything 克隆到 `/tmp/html-anything`（git clone --depth 1）
- 服务运行在 `http://localhost:3000`（`pnpm -F @html-anything/next dev`）
- pnpm 10.33.2 安装在 `~/.npm-global/bin/pnpm`
- 已安装 coding agent：Claude Code（`/usr/local/bin/claude`）、OpenClaw、Hermes

---

## html-anything 的价值

html-anything 是一个"AI agent 写 HTML"的编辑器，核心能力：

1. **75 个 skill 模板**（deck/article/social/data-report 等）
2. **Claude Code 等 8 个 coding agent 驱动**（复用已有登录，无需 API key）
3. **SSE 流式生成**（实时看页面一点点生成）
4. **一键导出微信/X/知乎/PNG**（juice CSS 内联解决微信排版）

对 GEO 工作流的直接帮助：
- 把 GEO 报告数据变成精美的 HTML 页面
- 微信排版导出（最大痛点）
- 小红书卡片生成（`card-xiaohongshu` skill）
- 演示幻灯片（`deck-*` skills）

---

## MCP 桥接方案

**目标**：让 Hermes 能直接调用 html-anything 的 `/api/convert`（SSE 流式 HTML 生成）。

**方案**：写 Python stdio MCP server，桥接到 `localhost:3000`。

**文件**：
- Server 脚本：`/Users/apple/.hermes/mcp-servers/html-anything/server.py`
- Hermes config：已添加 `mcp_servers.html-anything` 到 `~/.hermes/config.yaml`

**MCP 工具（3个）**：
- `mcp_html-anything_list_agents` — 列出可用 coding agents
- `mcp_html-anything_list_templates` — 列出 16 个模板技能
- `mcp_html-anything_convert` — 内容转 HTML（SSE 流式）

**验证状态**：全部 3 个工具调用成功，convert 完整流程通顺。

---

## 演示结果（2026-05-19）

**请求内容**：燕之屋 GEO 洞察报告（360条回答/90%提及率/平台表现/竞品提及）

**输出**：
- HTML 大小：18,698 chars
- 图表：13 个 Chart.js
- 表格：1 个
- 布局：Tailwind CSS + Inter/Noto Sans SC 字体
- 生成时间：~100s（Claude Code + MiniMax 模型）

---

## 使用场景

1. **GEO 报告排版**：用 `data-report` skill 把 GEO 数据变成可视化报告
2. **微信文章排版**：`article-magazine` → juice 内联 CSS → 直接粘贴微信
3. **客户演示 deck**：用 `deck-guizang-editorial` / `deck-swiss-international` 做 PPT
4. **小红书内容卡片**：用 `card-xiaohongshu` skill 生成配图

---

## 已知限制

- html-anything 本身是 Next.js 应用，需要单独启动服务（`pnpm -F @html-anything/next dev`）
- 生成依赖本地 coding agent（Claude Code 等），需提前安装并登录
- SSE 流式响应需要 120s timeout
- 尚未重启 Hermes 验证 MCP server 是否在重启后自动加载（config 已写入，需验证）