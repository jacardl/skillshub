# 微信文章 HTML 格式反模式 & 已解决问题记录

## 2026-05-15 发现：图片上传格式错误（40137）+ curl 优于 urllib

**错误**：`{"errcode":40137,"errmsg":"invalid image format hint"}`

**根因**：WeChat `uploadimg` 接口只接受 JPEG，不接受 PNG。

**实测**：
| 文件 | 格式 | 上传结果 |
|------|------|----------|
| `supertonic_hero.png`（708KB） | PNG | ❌ 40137 |
| `supertonic_og.png`（52KB） | PNG | ❌ 40137 |
| `supertonic_body.jpg` | JPEG | ✅ 成功 |

**解决**：PNG 转 JPEG，或找其他 JPEG 图片。若 PIL 报 `OSError: image file is truncated`，说明图片文件损坏，需另找来源。

**附加发现**：`urllib.request` multipart 上传报 `41005 media data missing`，用 subprocess + curl 则正常：
```bash
curl -s -F 'media=@/path/to/image.jpg' \
  'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=TOKEN&type=image'
```

---

## 2026-05-15 发现：`<ol><li>` 内含 `<strong>` 导致渲染异常

**现象**：有序列表 `<ol>` 中，部分 `<li>` 序号后无内容（源码完整）。

**根因**：`<li>` 内含 `<strong>` 标签时，WeChat 编辑器渲染异常。

```html
<!-- ❌ 渲染异常：li 内含 strong -->
<li><strong>文本正则化（TN）</strong>：将数字...</li>

<!-- ✅ 正常：去掉 strong -->
<li>文本正则化（TN）：将数字...</li>
```

**结论**：列表项内容不要用 `<strong>` 加粗，改用纯文本。

---

## 2026-05-15 发现：session 脚本 `publish_html.py` 的双重错误

### 问题
`/tmp/publish_html.py` 生成微信草稿时：
1. HTML block 拼接用 `'\n\n'.join(blocks)` → JSON payload content 字段携带 `\n`
2. 每个 block 内部写成多行字符串 → 块内部有换行符

### 症状
微信文章预览中出现多余空白段落（视觉上表现为间隔点、段落间空白行）。

### 根因分析
`cleanup_html.py` 只能移除「整行为空」的行（`line.strip() == ''`），无法移除：
- JSON payload 中 block 间的 `\n\n`（这是 JSON 字符串值的一部分，不是文件中的独立空行）
- HTML 块内部的多行字符串换行（`'<p>...\n...</p>'` 的内部 `\n`）

### 修复
生成阶段必须遵守：
```python
# 每个块完全内联写成一行
blocks = [
    '<p style="...">第一段内容</p>',  # 单行，无内部换行
    '<p style="...">第二段内容</p>',
]
html_content = ''.join(blocks)  # 零分隔符
```

验证：
```bash
grep -n '^$' /tmp/article.html  # 应返回空
```

---

## 已知问题模式

| 模式 | 结果 | 正确做法 |
|------|------|----------|
| `''.join()` 无分隔符拼接 | block 直接拼接，零换行 | ✅ 标准做法 |
| `'\n\n'.join(blocks)` | JSON payload 带 `\n`，微信渲染多段落 | `''.join(blocks)` |
| 多行字符串块 | 块内部换行无法被 cleanup 移除 | block 完全内联单行 |
| `**bold**` 直接写在 HTML 里 | WeChat 原样显示 `**` 符号 | 生成 HTML 前先将 `**text**` 转为 `<strong>text</strong>` |
| `### 三级标题` 直接写在 HTML 里 | WeChat 原样显示 `###` 符号 | 去掉 `###` 前缀，用 `<p style="font-weight:bold">` |
| `<p bold>` 内嵌套 `<strong>**text**</strong>` | 双重加粗 | 纯文本 p bold 标签内直接放文字，不加 strong |

## 2026-05-15 发现：Markdown 语法写在 HTML 里被微信原样显示

### 正确转换规则

| 内容格式 | HTML 写法 |
|----------|-----------|
| `**粗体文字**` | `<strong style="color:#e63946;">粗体文字</strong>` |
| `**一、痛点切入**`（章节标题） | `<h2 style="...">一、痛点切入</h2>` |
| `**核心概念**`（小节 bold 标题） | `<p style="font-weight:bold;">核心概念</p>`（不要嵌套 `<strong>`） |
| `### 环境要求`（子标题） | `<p style="font-weight:bold;">环境要求</p>`（去掉 `###`） |
| `• **需求**：描述`（列表项） | `<li style="margin:0 0 4px 0;"><strong>需求</strong>：描述</li>`（不要手动加 `•`，WeChat 自带） |

### ⚠️ 双重加粗陷阱
```html
<!-- ❌ 双重加粗 -->
<p style="font-weight:bold;"><strong>**核心概念**</strong></p>

<!-- ✅ 正确 -->
<p style="font-weight:bold;">核心概念</p>
```

### 验证命令
```bash
# 检查是否还有未转换的 ** 和 ###
grep -n '\*\*\|###' /tmp/article.html  # 应返回空

# 检查是否有 • 符号出现在 <li> 内
grep -n '<li[^>]*>[^<]*•' /tmp/article.html  # 应返回空
```

---

## WeChat 渲染器行为备注

WeChat 公众平台的 HTML 渲染器会对以下情况产生额外段落：
- `content` 字段 JSON 值中连续出现的 `\n`（即使在 JSON 字符串内部）
- HTML 源码中的连续空行（`<p>...</p>\n\n<p>...</p>`）

**结论**：生成阶段零换行是唯一可靠方案，cleanup 是辅助验证而非主要修复手段。

---

## 2026-05-20 发现：图片无法显示 + 白色文字对比度问题

### 问题 1：图片无法显示

**现象**：文章中很多图片在微信中无法显示

**根因**：
- 使用了外部 URL（如 GitHub rawusercontent、rawcdn等）而非微信素材库 URL
- 微信文章正文中的图片必须使用 `uploadimg` 接口上传，获取 `mmbiz.qpic.cn` 域名的 URL

**解决方案**：
```python
# ✅ 正确：使用 mmbiz URL
<img src="http://mmbiz.qpic.cn/mmbiz/xxx/0" style="...">

# ❌ 错误：使用外部 URL
<img src="https://raw.githubusercontent.com/...">
```

**发布前检查**：
```bash
# 检查是否还有非 mmbiz 图片
grep -o 'src="[^"]*"' /tmp/article.html | grep -v mmbiz
# 应返回空
```

### 问题 2：白色文字与白色背景对比度

**现象**：Page Agent 封面图使用 GitHub 截图，白色背景+白色文字/徽章，在微信白色底上完全看不清

**根因**：GitHub README 截图常有透明/白色背景 + 白色徽章（badge）、标签、统计数据

**解决方案**：
- **禁止**直接使用 GitHub README 截图作为封面或正文用图
- 如必须使用带白色元素的截图，在截图下方添加**深色背景衬底**（如 `#1a1a2e` 纯色块）增加对比度
- 用 PIL 给截图加边框/背景：
```python
from PIL import Image, ImageOps

img = Image.open("screenshot.png").convert("RGBA")
# 添加深色背景
background = Image.new('RGBA', img.size, (26, 26, 46, 255))  # #1a1a2e
combined = Image.alpha_composite(background, img)
combined.convert('RGB').save("output_with_bg.jpg", "JPEG")
```

### 问题 3：封面图必须是深色主题

**现象**：封面图使用白色背景，在微信文章列表中不突出

**要求**：
- 尺寸：900×383（信息图比例）或 900×900（方图）
- **背景必须是深色**（推荐 `#1a1a2e` / `#16213e` / `#0f0f23` 等）
- 文字使用白色或亮色，确保清晰可读

**封面图生成 Prompt 示例**：
```
A dark themed cover image for a tech article about AI agents, deep dark blue background (#1a1a2e), white text showing "Page Agent" title and "17.9k Stars", modern minimalist style, no white backgrounds
```

---

## 已验证的封面图/配图生成方案

| 工具 | 优点 | 缺点 |
|------|------|------|
| Sensenova | 质量高，可控制风格 | 需配置 API Key |
| MiniMax | 国内可用 | 质量不稳定 |
| PIL 纯代码 | 无需外部服务 | 仅限叠加背景/边框 |
| 手动 PS | 完全可控 | 效率低 |
