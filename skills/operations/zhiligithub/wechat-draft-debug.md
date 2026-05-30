# 微信草稿排版问题诊断手册

## 有序列表（`<ol>`）渲染异常

**现象**：HTML 源码中 `<ol>` 的所有 `<li>` 项完整，但微信编辑器预览中部分序号后无内容显示。

**典型案例**（Supertonic 草稿）：
```
预览显示：
1.                    ← 内容为空
2. 文本正则化          ← 正常
3.                    ← 内容为空
4. Grapheme-to-Phoneme ← 正常
5. 流式输出            ← 正常

源码（完整）：
<ol>
  <li>文本正则化（TN）：将数字...<li>
  <li>Grapheme-to-Phoneme（G2P）...
  <li>声学模型推理：将音素序列...
  <li>声码器（Vocoder）：将 mel 频谱...
  <li>流式输出：支持分块合成...
</ol>
```

**根因（已确认）**：`<li>` 内含 `<strong>` 标签时，WeChat 编辑器渲染异常，导致序号后内容为空。

**修复方法**：去掉所有 `<li>` 内的 `<strong>` 标签，改用纯文本。

```html
<!-- ❌ 有 <strong> 导致渲染异常 -->
<ol>
  <li><strong>文本正则化（TN）</strong>：将数字、缩写...→ 预览中显示为空</li>
  <li><strong>Grapheme-to-Phoneme（G2P）</strong>：将文字转化为音素...→ 正常</li>
</ol>

<!-- ✅ 纯文本，正常显示 -->
<ol>
  <li>文本正则化（TN）：将数字、缩写...→ 预览正常</li>
  <li>Grapheme-to-Phoneme（G2P）：将文字转化为音素...→ 预览正常</li>
</ol>
```

**排查步骤**：
1. 读取草稿 HTML 源码，确认所有 `<li>` 项在源码层面完整
2. 检查 `<li>` 内是否有 `<strong>` 标签——这是渲染异常的根因
3. 若有 → 去掉 `<strong>`，保留纯文本 → 重建草稿
4. 若无 → 可能是其他 WeChat 编辑器 bug，尝试重建草稿

**mmx vision describe 诊断命令**：
```bash
bash -c 'source ~/.hermes/.env && mmx vision describe "/path/to/screenshot.jpg" --prompt "精确描述这张微信公众号草稿截图里，哪些列表项（有序或无序）只有序号/圆点但没有文字内容。列出具体序号。" --output json'
```

---

## 多余空行（blank lines between blocks）

**根因**：Python 生成 HTML 时 block 元素间用了 `'\\n\\n'.join()` 或多行字符串块，导致 JSON payload 携带 `\\n`，微信将连续换行渲染为额外段落。

**表现**：
- `<p>` 标签之间出现孤立圆点 `•`（微信把空段落渲染成了列表项符号）
- 本应是紧凑段落的区域出现大段空白

**排查**：
```bash
# 1. 检查 HTML 源码是否有纯空行
grep -n '^$' /tmp/article.html

# 2. 检查 JSON payload 中的换行符数量
python3 -c "
import json
with open('/tmp/article.html') as f:
    html = f.read()
payload = json.dumps({'content': html}, ensure_ascii=False)
print(f'换行符: {payload.count(chr(10))} (应为 0)')
"
```

**解决方案**：
- 生成阶段：每个 HTML block 完全写成一行，用 `''.join(blocks)` 拼接
- 清理阶段：`cleanup_html.py` 移除纯空行（但无法清除块内部换行）
- 最干净方案：inline 单行块 + `''.join()`

---

## Markdown 语法残留（`**`、`###`、`•`）

**现象**：草稿预览中 `**文字**` 原样显示、`### 标题` 显示为普通文本、`•` 出现在列表项内形成双重 bullet。

**根因**：format-guide.md 使用 Markdown 语法写内容，但微信编辑器不转换 Markdown，必须 agent 主动转 HTML。

**生成后必查**：
```bash
# 应返回空
grep -n '\\*\\*\\|#\#\\|#•' /tmp/article.html
```

| 内容写法 | 正确 HTML |
|----------|-----------|
| `**粗体**` | `<strong>粗体</strong>` |
| `### 子标题` | `<p style="font-weight:bold;">子标题</p>` |
| `• **概念**：描述` | `<li><strong>概念</strong>：描述</li>` |

---

## 双重加粗陷阱

**现象**：预览中 `**<strong>文字</strong>**` 原样显示。

**根因**：p 已有 `font-weight:bold`，内部又套了 `<strong>`，导致 Markdown `**` 未被解析为标签的一部分直接输出。

**正确做法**：
```html
<!-- ✅ p bold 标签内直接放纯文本 -->
<p style="font-weight:bold;margin:0 0 8px 0;font-size:16px;">核心概念</p>

<!-- ❌ 嵌套 strong -->
<p style="font-weight:bold;margin:0 0 8px 0;font-size:16px;"><strong>核心概念</strong></p>

<!-- ❌ Markdown 未转义，** 原样显示 -->
<p style="font-weight:bold;margin:0 0 8px 0;font-size:16px;">**核心概念**</p>
```

---

## draft/add 返回值误判（item/ad_count 不是错误）

**现象**：调用 `draft/add` 返回如下 JSON，agent 误判为失败：
```json
{
  "media_id": "kiuyle4KZ...",
  "item": [{"index": 0, "ad_count": 2}]
}
```

**正确理解**：
- `errcode: 0`（隐含）= API 调用成功
- `media_id` 存在 = 草稿已创建
- `item` 数组含 `ad_count` = 广告素材计数（正常返回，不代表失败）

**正确判断**：
```python
# ✅ 正确
if draft_result.get('errcode') == 0 and draft_result.get('media_id'):
    print(f"✅ 草稿创建成功，media_id: {draft_result['media_id']}")

# ❌ 误判：检查 'item' in draft_result → 永远为 True（item 存在=失败？）
if 'item' in draft_result:
    print("失败")  # 错误判断
```

**备用验证**：调用 `draft/count` 确认草稿总数是否增加。

---

## freepublish/submit 返回 48001（api unauthorized）

**错误**：`errcode: 48001, errmsg: api unauthorized rid: ...`

**根因**：微信「群发」接口（`freepublish/submit`）仅限已认证的公众号（服务号/订阅号）使用，普通个人订阅号没有权限。

**解决方案**：草稿创建成功（`errcode: 0` + `media_id`）后，**告知用户到微信公众平台后台手动发布**。这是正常流程，草稿 API 本身已经成功。

**标准结束语**：
```
✅ 草稿已创建
media_id：xxx
请登录微信公众平台 mp.weixin.qq.com → 草稿箱 → 找到文章 → 发布
```

---

## 中文内容显示为 `\uXXXX` 转义序列（Unicode Double-Encoding）

**现象**：微信草稿预览中，中文字符全部变成 `\u4eb2\u6d4b` 这样的 Unicode 转义序列，完全无法阅读。

**典型表现**：
- 标题/正文里中文全变 `\\u4eb2\\u6d4b\\u4e09\\u5927`
- **草稿标题显示正常，正文显示 `\uXXXX` 字面量**
- **三篇草稿正文全部显示相同的 `\uXXXX` 内容**——说明 JSON 序列化层出了问题

**根因（已验证 2026-05-27）**：`publish_zhili.py` 中 `json.dumps(payload, ensure_ascii=False)` 将中文以 UTF-8 原始字节发送，微信的 HTML content pipeline 错误处理 raw UTF-8，导致 Unicode 转义字面量泄露到前端。**`fix_double_encoded_content()` 函数无法阻止此问题**，它只能检测已存在的 `\uXXXX` 序列，是被动修复而非主动防御。

**⚠️ 正文 HTML 同样受影响**：不只是 title 字段，content 字段（含 HTML）中的中文同样受 `ensure_ascii=False` 影响产生 `\uXXXX` 显示。title 字段 WeChat raw UTF-8 处理正常（不受影响），content 字段的 HTML pipeline 不同，ensure_ascii=False 全链路触发。

**已验证的修复**：两处 `json.dumps(payload)` 改用默认参数（`ensure_ascii=True`），中文变成 `\uXXXX` 形式，WeChat 能正确解码前端显示正常中文。

**触发路径**：
```python
# ❌ 错误：ensure_ascii=False → 中文变 raw UTF-8 → WeChat 前端显示 \uXXXX
data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

# ✅ 正确：ensure_ascii=True（默认）→ 中文变 \uXXXX → WeChat 前端显示正常中文
data = json.dumps(payload).encode("utf-8")  # 或明确写 ensure_ascii=True
```

**已修复位置**：
- `publish_zhili.py` line 443：`json.dumps(payload)`（原为 `ensure_ascii=False`）
- `publish_zhili.py` line 564：`json.dumps(payload)`（原为 `ensure_ascii=False`）

**诊断命令**：
```python
import re

def detect_unicode_escape(html_content):
    """检测 HTML 中是否存在字面 \\uXXXX 序列"""
    matches = re.findall(r'\\u[0-9a-fA-F]{4}', html_content)
    if matches:
        print(f"[WARN] 检测到 {len(matches)} 个 \\uXXXX 字面序列")
        return True
    return False
```

**症状对比诊断**：
| 字段 | 显示正常 | 显示 \uXXXX |
|------|----------|-------------|
| title | ✅（WeChat raw UTF-8 处理正常） | 需改 ensure_ascii=True |
| content | — | content 字段 HTML pipeline 不同，ensure_ascii=False 全链路触发 |

**验证修复**：发布后预览应显示正常中文字符，无任何 `\u` 字符。

---

## thumb_media_id 报错 invalid（40007）

**错误**：`errcode: 40007, errmsg: invalid media_id hint`

**常见原因**：

| 上传接口 | type 参数 | 返回字段 | 能否用于 draft/add thumb_media_id |
|----------|-----------|----------|-----------------------------------|
| `media/upload` | `type=thumb` | `thumb_media_id`（临时） | ❌ 不兼容，40007 |
| `material/add_material` | `type=thumb` | `media_id` | ❌ 不兼容，40007 |
| `material/add_material` | `type=image` | `media_id` | ✅ 唯一正确方式 |

**⚠️ publish_zhili.py 历史 bug**：原脚本 `upload_thumb_material` 用 `type=thumb`，会报 40007。已 patch 为 `type=image`。

**正确做法**：
```python
# 用 type=image 上传封面图
resp = requests.post(
    f'https://api.weixin.qq.com/cgi-bin/material/add_material'
    f'?access_token={token}&type=image',
    files={'media': ('cover.jpg', img_data, 'image/jpeg')}
)
media_id = resp.json()['media_id']  # ← 拿这个当 thumb_media_id

# 创建草稿
draft_payload = {
    "articles": [{
        "title": "...",
        "thumb_media_id": media_id,  # ← 传入上面的 media_id
        ...
    }]
}
```
