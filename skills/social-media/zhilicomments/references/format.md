# zhilicomments HTML 格式规范

> 本文件为 zhilicomments 技能的视觉排版参考手册。
> **基准版本：Streambert 文章（2026-05-22，已验证合规发布）。**
> 参考原文：`/tmp/draft.html`

## 🚨 CSS 规范（已验证正确版本 · 2026-05-23）

> ⚠️ **教训（2026-05-23）**：曾误以为 h2 纯文本无边框，实际 Streambert 文章 h2 有 `border-left:4px solid #00d4aa`。所有 CSS 值必须以 `references/streambert-reference.html` 为准，禁止凭记忆填写。

```html
body style="background-color:#f5f4ed;font-family:Georgia,'Times New Roman',serif;margin:0;padding:0;"
div style="max-width:680px;margin:0 auto;padding:24px 16px 60px 16px;"
```

### 各层级样式

| 层级 | 元素 | CSS |
|------|------|-----|
| Level 1 | h1 | `font-size:28px;font-weight:bold;color:#1B365D;margin:20px 0 10px;line-height:1.3` |
| Level 2 | h2 | `font-size:20px;font-weight:bold;color:#1B365D;border-left:4px solid #00d4aa;padding-left:12px;margin:28px 0 12px 0` |
| Level 3 | h3 | （如需：`color:#2d6a4f`） |
| Level 4 | 正文p | `font-size:16px;line-height:1.85;color:#2c2c2c;margin:0 0 14px 0` |
| Level 5 | blockquote | `font-size:18px;font-style:italic;color:#1f1d18;border-left:3px solid #c9553d;padding:12px 16px;margin:20px 0;background:#efeee5;border-radius:0 4px 4px 0` |
| Level 6 | code | `font-size:14px;font-family:Menlo,Consolas,monospace;background:#f0ede5;padding:2px 6px;border-radius:3px` |
| Level 7 | 行内强调 | `strong style="color:#1B365D;font-weight:bold"`（深蓝）/ `strong style="color:#c9553d;font-weight:bold"`（红色）|

### 关键要点

- **h2**：必须 `border-left:4px solid #00d4aa;padding-left:12px`
- **p 间距**：`margin:0 0 14px 0`
- **图片**：`width:100%;max-width:680px;border-radius:4px;margin:16px 0;`
- **blockquote**：斜体，3px 红色左边框，`border-radius:0 4px 4px 0`，背景 `#efeee5`
- **底部链接**：`font-size:14px;color:#6b665b;font-family:monospace;`

---

## 排版规则

- **block 元素必须单独一行**
- 禁止 ul/li，用 `•` 代替
- 只用 `margin-bottom` 控制间距，不管 `margin-top`
- 所有样式内联

## 禁用词（严禁出现）

`说白了`、`意味着什么`、`本质上`、`双引号`、`冒号`、`破折号`

## CSS 合规性自动验证脚本

```python
import re

html = open('/tmp/article.html').read()

checks = [
    ("h2 has border-left:4px solid #00d4aa", 'border-left:4px solid #00d4aa' in html),
    ("h2 has padding-left:12px", 'padding-left:12px' in html),
    ("blockquote border-left:3px solid #c9553d", 'border-left:3px solid #c9553d' in html),
    ("blockquote has border-radius", 'border-radius:0 4px 4px 0' in html),
    ("blockquote background #efeee5", 'background:#efeee5' in html),
    ("strong color 1B365D present", 'color:#1B365D' in html),
    ("strong color c9553d present", 'color:#c9553d' in html),
    ("p margin-bottom 14px", 'margin:0 0 14px 0' in html),
    ("footer color #6b665b", 'color:#6b665b' in html),
    ("font-family Georgia", 'font-family:Georgia' in html),
]

failed = [(n, r) for n, r in checks if not r]
if failed:
    print("CSS检查未通过:")
    for n, r in failed:
        print(f"  {n}")
    raise AssertionError("CSS检查未通过")
else:
    print("CSS全部通过")
```
