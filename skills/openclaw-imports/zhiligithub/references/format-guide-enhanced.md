# zhiliGitHub 增强版 HTML 格式规范

> 本规范基于 `doc-kami-parchment` + `article-magazine` 整合升级，适用于「直隶按察使」GitHub 黑马长文（4000-8000字）。

---

## 一、视觉签名（核心不变，细节增强）

> **⚠️ 排版理念：章节标题 + 流式正文，与 zhiliComments 共用同一套渲染规范**
>
> 允许出现「一、XXX」「二、XXX」显性章节 h2 标题，靠装饰分隔线 `· · ·` 做章节内节奏划分。



| 属性 | 规范值 | 说明 |
|------|--------|------|
| 画布背景 | `#f5f4ed`（暖羊皮纸）或 `#ffffff`（用户可选） | 默认暖羊皮纸；用户明确要求纯白时替换 |
| 主文字色 | `#1f1d18`（近黑暖灰） | 不用纯黑 |
| 次文字色 | `#6b665b` | 元信息、来源等 |
| 强调色 | `#1B365D`（墨蓝） | 主 accent，唯一 |
| 高亮背景 | `#fff3b0`（淡黄） | 重点句子背景高亮 |
| 引用背景 | `#efeee5`（次级羊皮纸） | 引用块背景 |
| 装饰线色 | `#d4d1c5`（发丝线） | 分隔线 |

**新增辅助色（小声使用，不喧宾夺主）：**

| 色值 | 用途 |
|------|------|
| `#c9553d`（砖红） | 数字强调、数据高亮 |
| `#2d6a4f`（森绿） | 适合场景、绿色标签 |
| `#7c6f64`（暖灰） | 不适合场景、灰色标签 |
| `#e8e0d5`（浅米） | 信息卡片背景 |

---

## 二、标题层级（字阶增大，2026-05-20 与 article_io2026.html 完全对齐）

> ⚠️ 本规范已废弃，优先使用 format-guide.md 的 CSS 渲染层。保留此处仅作历史参考。

|| 元素 | 字号 | 字体 | 字重 | 颜色 | margin |
|------|------|------|------|------|------|--------|
| 大标题（h1） | 28px | Noto Serif SC, Georgia, serif | 700 | #1B365D | 0 0 8px 0 |
| h2 章节标题 | 20px | Noto Serif SC | 700 | #1B365D | 0 0 16px 0 |
| 正文段落 | 16px | Noto Serif SC | 400 | #2c2c2c | 0 0 28px 0 |
| 次要文字 | 13px | Noto Sans SC | 400 | #7c6f64 | — |

**标题示例：**
```html
<!-- 大标题 -->
<p style="font-family:'Noto Serif SC',serif;font-size:26px;font-weight:700;line-height:1.25;margin:0 0 12px 0;color:#1f1d18;text-align:left;">18k Stars！AI 终于能自己操作网页了？</p>

<!-- h2 章节 -->
<h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">二、项目介绍</h2>

<!-- h3 子节 -->
<p style="font-family:'Noto Serif SC',serif;font-size:17px;font-weight:600;margin:20px 0 10px 0;color:#1f1d18;text-align:left;">核心概念</p>
```

---

## 三、增强高亮体系（四种高亮方式）

### 3.1 关键词高亮（墨蓝色）
```html
<strong style="color:#1B365D;">通义千问</strong>
```

### 3.2 背景高亮（淡黄色，用于重点句子）
```html
<span style="background:#fff3b0;padding:2px 6px;border-radius:3px;">完全免费</span>
```
**使用场景**：数据亮点、一句话总结、核心结论

### 3.3 引用块（左侧墨蓝竖线 + 次级背景）
```html
<div style="border-left:3px solid #1B365D;padding:12px 16px;margin:16px 0;background:#efeee5;border-radius:0 4px 4px 0;">
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;font-style:italic;line-height:1.7;color:#6b665b;margin:0;">这句话摘自项目 README，表达了作者的核心观点。</p>
</div>
```

### 3.4 数据强调（砖红色大号数字）
```html
<span style="font-family:'Noto Serif SC',serif;font-size:24px;font-weight:700;color:#c9553d;">17.9k</span>
<span style="font-size:14px;color:#6b665b;"> Stars</span>
```

---

## 四、Pull Quote（独立观点引用）

Pull quote 放在正文中间，字号大于正文，制造视觉节奏停顿。

```html
<div style="margin:24px 0;padding:20px 24px;background:#f5f4ed;border-radius:4px;border-top:2px solid #1B365D;border-bottom:2px solid #d4d1c5;">
  <p style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:500;line-height:1.6;color:#1f1d18;margin:0 0 8px 0;text-align:left;">「AI 正在从独立应用变成网页的一部分。」</p>
  <p style="font-size:14px;color:#6b665b;margin:0;text-align:left;">—— 这不是预测，这是正在发生的事。</p>
</div>
```

---

## 五、信息卡片（数据卡片 + 适合/不适合标签）

### 5.1 GitHub 元信息卡片
```html
<div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0;padding:14px 16px;background:#efeee5;border-radius:6px;border:1px solid #d4d1c5;">
  <span style="background:#1B365D;color:#f5f4ed;padding:3px 10px;font-size:13px;border-radius:3px;">⭐ 17.9k</span>
  <span style="background:#1B365D;color:#f5f4ed;padding:3px 10px;font-size:13px;border-radius:3px;">TypeScript</span>
  <span style="background:#1B365D;color:#f5f4ed;padding:3px 10px;font-size:13px;border-radius:3px;">MIT</span>
  <span style="color:#6b665b;font-size:13px;padding:3px 0;">GitHub: alibaba/page-agent</span>
</div>
```

### 5.2 适合/不适合场景标签
```html
<div style="margin:10px 0;padding:12px 16px;background:#f0f7f4;border-radius:4px;border-left:3px solid #2d6a4f;">
  <p style="font-size:14px;color:#1f1d18;margin:0 0 4px 0;"><strong style="color:#2d6a4f;">✅ 适合场景：</strong>给产品快速加 AI 助手、做无障碍工具、SaaS 后台 Copilot</p>
</div>
<div style="margin:10px 0;padding:12px 16px;background:#f7f5f3;border-radius:4px;border-left:3px solid #7c6f64;">
  <p style="font-size:14px;color:#1f1d18;margin:0 0 4px 0;"><strong style="color:#7c6f64;">❌ 不适合：</strong>跨应用操作、极高数据安全要求、频繁变动的复杂页面</p>
</div>
```

---

## 六、代码块（保持深色，细节优化）

```html
<pre style="background:#1e1e1e;border-radius:6px;padding:16px 20px;margin:16px 0;overflow-x:auto;"><code style="font-family:Consolas,'Courier New',monospace;color:#e8e8e8;font-size:14px;line-height:1.6;white-space:pre;">npm install page-agent</code></pre>
```

**内联代码：**
```html
<code style="font-family:Consolas,'Courier New',monospace;color:#c9553d;font-size:14px;background:#f0ece5;padding:1px 5px;border-radius:3px;">&lt;script&gt;</code>
```

---

## 七、装饰性分隔线（章节分隔）

用纯 CSS 符号做装饰，不用图片：

```html
<!-- 小圆点分隔线 -->
<div style="display:flex;align-items:center;justify-content:center;gap:12px;margin:32px 0;color:#d4d1c5;">
  <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
  <span style="font-family:'Noto Serif SC',serif;color:#6b665b;font-size:14px;">· · ·</span>
  <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
</div>
```

---

## 八、正文图片 + Figure Caption

```html
<!-- 配图 -->
<img src="mmbiz_url" style="width:100%;border-radius:6px;margin:16px 0;" />
<!-- 图注 -->
<p style="font-size:13px;color:#6b665b;font-style:italic;margin:0 0 20px 0;text-align:left;">▲ Page Agent 工作流程图：用户指令 → DOM 提取 → LLM 决策 → 执行操作</p>
```

---

## 九、完整模板（zhiliGitHub 增强版 HTML）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>文章标题</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:0;background:#f5f4ed;">
<div style="max-width:678px;margin:0 auto;padding:0 12px;font-size:16px;line-height:1.7;color:#1f1d18;text-align:left;background:#f5f4ed;">

  <!-- 分类标签 -->
  <p style="font-size:12px;font-weight:500;letter-spacing:0.1em;color:#1B365D;margin:24px 0 12px 0;text-align:left;">GitHub · 黑马项目</p>

  <!-- 大标题 -->
  <p style="font-family:'Noto Serif SC',serif;font-size:26px;font-weight:700;line-height:1.25;margin:0 0 16px 0;color:#1f1d18;text-align:left;">18k Stars！AI 终于能自己操作网页了？</p>

  <!-- 副标题 -->
  <p style="font-size:17px;line-height:1.6;color:#6b665b;margin:0 0 20px 0;text-align:left;">阿里巴巴开源 Page Agent，纯前端实现自然语言操控网页，GitHub 17.9k Stars。</p>

  <!-- 作者信息 -->
  <p style="font-size:13px;color:#6b665b;margin:0 0 28px 0;padding-bottom:16px;border-bottom:1px solid #d4d1c5;text-align:left;">AhaAaron · 2026年5月20日 · 阅读约 8 分钟</p>

  <!-- ========== 一、痛点切入 ========== -->
  <h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">一、痛点切入</h2>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;">事情是这样的。</p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;">你用过那种复杂的企业后台系统吗？提交一个差旅报销，要点击十几个按钮，填五六个表单，弄错一步就得重来。</p>

  <!-- ========== 二、项目介绍 ========== -->
  <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin:32px 0;color:#d4d1c5;">
    <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
    <span style="font-family:'Noto Serif SC',serif;color:#6b665b;font-size:14px;">· · ·</span>
    <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
  </div>

  <h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">二、Page Agent 是什么？</h2>

  <!-- GitHub 元信息卡片 -->
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0;padding:14px 16px;background:#efeee5;border-radius:6px;border:1px solid #d4d1c5;">
    <span style="background:#1B365D;color:#f5f4ed;padding:3px 10px;font-size:13px;border-radius:3px;">⭐ <span style="font-family:'Noto Serif SC',serif;font-weight:700;">17.9k</span></span>
    <span style="background:#1B365D;color:#f5f4ed;padding:3px 10px;font-size:13px;border-radius:3px;">TypeScript</span>
    <span style="background:#1B365D;color:#f5f4ed;padding:3px 10px;font-size:13px;border-radius:3px;">MIT</span>
    <span style="color:#6b665b;font-size:13px;padding:3px 0;">github.com/alibaba/page-agent</span>
  </div>

  <!-- 项目配图 -->
  <img src="mmbiz_url" style="width:100%;border-radius:6px;margin:16px 0;" />
  <p style="font-size:13px;color:#6b665b;font-style:italic;margin:0 0 20px 0;text-align:left;">▲ Page Agent 项目 Banner</p>

  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;"><strong style="color:#1B365D;">一句话描述：</strong>Page Agent 相当于网页里的「AI 操作员」，只需要一行 <code style="font-family:Consolas,'Courier New',monospace;color:#c9553d;font-size:14px;background:#f0ece5;padding:1px 5px;border-radius:3px;">&lt;script&gt;</code> 标签，就能用大白话操控任意 Web 界面。</p>

  <!-- 核心概念 -->
  <p style="font-family:'Noto Serif SC',serif;font-size:17px;font-weight:600;margin:20px 0 10px 0;color:#1f1d18;text-align:left;">核心概念</p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 8px 0;color:#1f1d18;text-align:left;padding-left:16px;text-indent:-16px;">• <strong style="color:#1B365D;">DOM 驱动：</strong>直接读取和操作页面 DOM 结构，不需要截图，不需要多模态模型。</p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 8px 0;color:#1f1d18;text-align:left;padding-left:16px;text-indent:-16px;">• <strong style="color:#1B365D;">BYO LLM：</strong>支持所有兼容 OpenAI API 格式的模型，也可对接本地 Ollama 离线运行。</p>

  <!-- Pull Quote -->
  <div style="margin:24px 0;padding:20px 24px;background:#f5f4ed;border-radius:4px;border-top:2px solid #1B365D;border-bottom:1px solid #d4d1c5;">
    <p style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:500;line-height:1.6;color:#1f1d18;margin:0 0 8px 0;text-align:left;">「给每个网页配一个智能助手，随时待命、随叫随到。」</p>
    <p style="font-size:14px;color:#6b665b;margin:0;text-align:left;">这不是愿景，这是 Page Agent 正在做的事。</p>
  </div>

  <!-- ========== 三、怎么用 ========== -->
  <h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">三、怎么用？</h2>

  <p style="font-family:'Noto Serif SC',serif;font-size:17px;font-weight:600;margin:20px 0 10px 0;color:#1f1d18;text-align:left;">方式一：一行代码集成</p>
  <pre style="background:#1e1e1e;border-radius:6px;padding:16px 20px;margin:12px 0;overflow-x:auto;"><code style="font-family:Consolas,'Courier New',monospace;color:#e8e8e8;font-size:14px;line-height:1.6;">&lt;script src="https://cdn.jsdelivr.net/npm/page-agent@1.8.2/dist/iife/page-agent.demo.js" crossorigin="true"&gt;&lt;/script&gt;</code></pre>

  <!-- 引用块 -->
  <div style="border-left:3px solid #1B365D;padding:12px 16px;margin:16px 0;background:#efeee5;border-radius:0 4px 4px 0;">
    <p style="font-family:'Noto Serif SC',serif;font-size:15px;font-style:italic;line-height:1.7;color:#6b665b;margin:0;">⚠️ 注意：Demo CDN 仅用于技术评估，使用阿里免费的测试 LLM API。国内用户推荐用 npm 镜像版本。</p>
  </div>

  <!-- 适合/不适合 -->
  <div style="margin:16px 0;padding:12px 16px;background:#f0f7f4;border-radius:4px;border-left:3px solid #2d6a4f;">
    <p style="font-size:14px;color:#1f1d18;margin:0 0 4px 0;"><strong style="color:#2d6a4f;">✅ 适合场景：</strong>给产品快速添加 AI 助手功能的前端开发者、需要简化复杂后台操作的产品经理/运营、做无障碍辅助工具的开发团队。</p>
  </div>
  <div style="margin:12px 0;padding:12px 16px;background:#f7f5f3;border-radius:4px;border-left:3px solid #7c6f64;">
    <p style="font-size:14px;color:#1f1d18;margin:0 0 4px 0;"><strong style="color:#7c6f64;">❌ 不适合：</strong>需要跨应用操作、对数据安全有极高要求、页面结构极其复杂或频繁变动的网站。</p>
  </div>

  <!-- ========== 四、技术亮点 ========== -->
  <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin:32px 0;color:#d4d1c5;">
    <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
    <span style="font-family:'Noto Serif SC',serif;color:#6b665b;font-size:14px;">· · ·</span>
    <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
  </div>

  <h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">四、技术亮点</h2>

  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 8px 0;color:#1f1d18;text-align:left;padding-left:16px;text-indent:-16px;">1. <strong style="color:#1B365D;">纯前端架构：</strong>一行 CDN 脚本或 NPM 安装，不需要后端服务，不需要 Python 环境，不需要无头浏览器。</p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 8px 0;color:#1f1d18;text-align:left;padding-left:16px;text-indent:-16px;">2. <strong style="color:#1B365D;">DOM 驱动精准高效：</strong>直接操作页面 DOM，不需要截图识别，不需要多模态模型，速度更快、成本更低。</p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 8px 0;color:#1f1d18;text-align:left;padding-left:16px;text-indent:-16px;">3. <strong style="color:#1B365D;">自然语言交互：</strong>用户无需编写任何代码，关键操作前展示规划步骤，遇到歧义主动询问。</p>

  <!-- 背景高亮重点 -->
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:16px 0;color:#1f1d18;text-align:left;background:#fff3b0;padding:10px 14px;border-radius:4px;"><strong style="color:#c9553d;font-size:18px;">💡 核心洞察：</strong>Page Agent 代表了 AI 从「独立应用」变成「网页一部分」的重要趋势。</p>

  <!-- ========== 五、行业观察 ========== -->
  <h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">五、行业观察</h2>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;">传统的 Selenium、Playwright 定位是「外部控制」—— 你从外面去操控网页。而 Page Agent 直接住在网页里，成为页面本身的一部分。</p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;"><strong style="color:#1B365D;">方向是明确的：未来的网页会越来越「听得懂人话」。</strong></p>

  <!-- ========== 六、总结 ========== -->
  <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin:32px 0;color:#d4d1c5;">
    <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
    <span style="font-family:'Noto Serif SC',serif;color:#6b665b;font-size:14px;">· · ·</span>
    <span style="flex:1;max-width:60px;height:1px;background:#d4d1c5;display:inline-block;"></span>
  </div>

  <h2 style="font-family:'Noto Serif SC',serif;font-size:20px;font-weight:700;margin:28px 0 14px 0;color:#1f1d18;text-align:left;">六、总结</h2>

  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;"><strong style="color:#c9553d;">Page Agent 的核心价值：把 AI 从聊天窗口里拽出来，塞进网页里。</strong></p>

  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;">GitHub：<a href="https://github.com/alibaba/page-agent" style="color:#1a73e8;text-decoration:none;">github.com/alibaba/page-agent</a></p>
  <p style="font-family:'Noto Serif SC',serif;font-size:16px;line-height:1.7;margin:0 0 14px 0;color:#1f1d18;text-align:left;">如果你觉得这个项目有意思，欢迎 Star 支持开源 🧬</p>
  <p style="font-size:13px;color:#6b665b;margin:0 0 32px 0;padding-top:12px;border-top:1px solid #d4d1c5;text-align:left;">📌 数据来源：GitHub，2026-05-19 | 项目：alibaba/page-agent</p>

</div>
</body>
</html>
```

---

## 十、发布前自检清单

| 检查项 | 标准 |
|--------|------|
| `**` Markdown bold 残留 | 0 处 |
| 纯空行数量 | 0 |
| mmbiz 图片数量 | ≥1（正文必须） |
| Google Fonts 字体 | Noto Serif SC + Noto Sans SC |
| 强调色数量 | 主色 #1B365D，不滥用辅助色 |
| 章节分隔 | 装饰线 `· · ·` |
| Pull quote | 有（独立观点句） |
| 信息卡片 | GitHub 元信息、适合/不适合标签 |
| 背景高亮 | 有（重点句子用 `#fff3b0`） |
