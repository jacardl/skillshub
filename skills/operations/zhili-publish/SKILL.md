---
name: zhili-publish
description: |
  微信公众号草稿箱发布全流程。从 access_token 获取、草稿创建、HTML 排版到飞书汇报。用于 zhiliGitHub 长文（1500-2000字）和 zhiliComments 短评（800-2000字，2026-05-30 佳哥确认扩写到2000）的发布环节。

  ⚠️ 关键约束（2026-05-23 修正）：
  - 获取 token 必须用 POST https://api.weixin.qq.com/cgi-bin/stable_token，不能用 GET /cgi-bin/token（后者返回的 token 在素材接口报 errcode 40001）
  - 凭证预检 / token 刷新 / 上传封面 / 上传截图 / 创建草稿，每一步之前都要单独调用一次 stable_token
  - 作者字段固定填 `刘生`（2个中文字符不触发45110；留空也可，但填 `刘生` 更稳定）
  - 成功响应用 `if "media_id" in resp.json()` 判断，不能用 `errcode == 0`
  - 飞书汇报用 OC 格式：feishu:oc_034bc08420a2daed53561bfceba5b3bf
---

# 微信草稿箱发布流程（zhili-publish）

适用于「直隶按察使」公众号文章的草稿箱创建和发布。

---

## 卡兹克写作风格（zhili 统一文风规范）

> 本节为 khazix-style skill 的规范内容，所有 zhiliGitHub 长文和 zhiliComments 短评必须严格遵守。完整 canonical 参考：khazix-writer skill（KKKKhazix/khazix-skills）。

### 一句话概括

「有见识的普通人在认真聊一件打动他的事。」

### 核心价值观

- 永远好奇：面对新工具，不是「我会被取代吗」，是「我能用它玩点什么有意思的？」
- 讲人话：AI时代最稀缺的是「活人感」，大胆用「我觉得」「我认为」
- 真诚：可以不写，但绝不骗人
- 有所为有所不为：不追逐违背价值观的流量

### 五种文章原型

- 调查实验型：核心是「我替你去做了这件事」
- 产品体验型：核心是「跟我一起玩」
- 现象解读型：核心是「你注意到了吗？背后是什么？」
- 工具分享型：核心是「我发现了一个好东西」
- 方法论分享型：核心是「我把压箱底的东西掏给你了」

### 风格内核

节奏感：像跟朋友聊天，不像写报告。大量逗号制造口语停顿感，经常一句话自成一段来制造重点。

句式断裂：短句独立成段，制造停顿和重量感。如「壁垒。这个词以前是优势。现在是负债。」

知识输出方式：知识是「聊着聊着顺手掏出来」的，不是「下面我来给大家科普一下」。

亲自下场：最核心的写作基因，让读者感觉到「这个人真的做了这件事」。

人物画像法：从一个数据点出发，3-5句话让一个人物立体。

文化升维：聊完具体事情后，连接到更大的文化/哲学/历史参照物。

回环呼应：前面埋的钩子后面要响，文章要有闭合感。

对立面的理解与承认：先承认对方处境合理，再切入自己的角度。

### 绝对禁区

| 禁用词 | 替代表达 |
|--------|---------|
| 说白了 | 换句话说、说到底 |
| 意味着什么 | 说明、指向 |
| 这意味着 | 这说明 |
| 本质上 | 归根结底、说到底 |
| 换句话说 | 换言之、也就是说 |
| 不可否认 | 确实 |
| 综上所述 | 总之 |
| 总的来说 | 整体看 |

- **禁用标点**：冒号`：`、破折号`——`、双引号`""`
- **禁用开头**：`在当今AI快速发展的时代`、`随着技术的不断进步`、`让我们来看看`
- **禁用结构**：连续bullet list超过3个；大量加粗；不必要的小标题
- **假设性例子**：不能用「比如有一次...」编造场景
- **空泛工具名**：必须说具体名字（Claude Code、Seedance 2.0），不能说「AI工具」「某个模型」

### 推荐口语化词组

- 转场：说真的、怎么说呢、其实吧、回到xxx这块、顺着上面的再聊聊
- 判断：我有时候觉得、反正我觉得、这话听着有点刺耳但
- 自嘲：说实话我也不确定、愚钝如我、我自己也在摸索
- 情绪：太特么离谱了、给我整懵了、你敢信？？？、尼玛
- 拉近距离：很多朋友可能不知道、你想想看、屏幕前的你
- 口头禅：这玩意、不是哥们、有个屁的xxx、比较骚的事

### 开头必杀技

- 「事情是这样的。」简单直接
- 直接抛出一个让人？？？的荒诞事实
- 「最近被xxx刷屏了」
- 「这两天在网上刷到了一张图，很有意思」

### 四层质检体系

**L1 硬性规则**：禁用词零命中、禁用标点零命中、结构性套话零命中、空泛工具名零命中

**L2 风格一致性**：开头具体当下、长短句交替、一句话独立成段至少3次、口语化词组至少8-10个、疑问句作为节奏刹车

**L3 内容质量**：每个观点有具体人/场景/细节支撑、知识聊着聊着顺手掏出来、至少一处文化升维、对立面的理解与承认

**L4 活人感终审**：情绪是体感记忆而非知识性描述、有只有卡兹克才会写出来的角度、语气是有见识的普通人在认真聊、从头到尾无断点

### 字数标准

| Skill | 字数 |
|-------|------|
| `zhiliGitHub` | 1500-2000字（纯中文，不含HTML/CSS标签） |
| `zhiliComments` | **800-1500字**（纯中文，不含HTML/CSS标签） |

> ⚠️ **2026-05-24 佳哥确认**：zhiliComments 短评规格为 800-1500字。过往 4000-5000字 规格已校正。字数验证命令：
> ```python
> import re
> html = open('/tmp/draft.html').read()
> cn = re.sub(r'<[^>]+>', '', html)
> cn = re.sub(r'[^\u4e00-\u9fff]', '', cn)
> print(f"中文字数: {len(cn)}")  # zhiliComments 必须在 800-1500
> ```

不求Star/转发/关注，纯观点文观点本身即是结束。

### zhiliGitHub 专属格式补充

- **截图上传**：使用 khazix-writer 的 `references/scripts/wechat-screenshot_upload.py`，批量传入 GitHub raw 截图 URL，自动下载并上传到微信素材库，返回 mmbiz URL。
- **固定尾部（必须包含）**：正文末尾必须包含 GitHub URL，字体用 Level 6 样式（`font-size:14px;color:#6b665b;font-family:monospace`）。
- **禁止 branding**：禁止在 HTML 正文中出现任何内部 branding（卡兹克/zhiliGitHub/zhiliComments/自动发布等）。

---

## 凭证预检（第一步，必做）

在任何耗时的写作工作之前，先验证 WeChat API 凭证：

## 凭证信息（直隶按察使）

> ⚠️ **AppSecret 绝对不能硬编码在 skill 里。** 优先从 `~/.hermes/keys/wx_appsecret.txt` 读取；文件不存在或读取失败时，向用户询问当前 AppSecret。

**读取顺序**：
1. `~/.hermes/keys/wx_appsecret.txt`（优先，自动更新）
2. 用户直接提供（文件不存在时）

**凭证预检 Python 示例（从文件读取）**：
```python
import urllib.request, json, os

# 读取 AppSecret
secret_file = os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")
if os.path.exists(secret_file):
    with open(secret_file) as f:
        app_secret = f.read().strip()
else:
    raise FileNotFoundError("请先提供当前 AppSecret，或将其写入 ~/.hermes/keys/wx_appsecret.txt")

req = urllib.request.Request(
    "https://api.weixin.qq.com/cgi-bin/stable_token",
    data=json.dumps({
        "grant_type": "client_credential",
        "appid": "wx38a91c353554588a",
        "secret": app_secret
    }).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    result = json.loads(r.read())
if "access_token" in result:
    print("凭证有效，access_token:", result["access_token"][:20] + "...")
else:
    print("凭证无效:", result)
    raise Exception(f"AppSecret 无效，请更新 ~/.hermes/keys/wx_appsecret.txt，当前值已失效")
```

- **有效响应**：包含 `access_token` 字段
- **无效凭证**：返回 `errcode 40125` = AppSecret 无效，更新文件后重试
- 凭证无效时立即汇报，不要先写文章

### Token 获取方式
>
> stable_token 返回有效 token 时权限更完整（素材接口推荐用）；GET 返回的 token 有效期同样是 7200 秒，但在部分接口可能报 40001，此时回退到 stable_token。

**标准流程**：
```python
import urllib.request, json, os

def get_token():
    secret_file = os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")
    with open(secret_file) as f:
        app_secret = f.read().strip()

    # ① 尝试 stable_token POST
    try:
        req = urllib.request.Request(
            "https://api.weixin.qq.com/cgi-bin/stable_token",
            data=json.dumps({
                "grant_type": "client_credential",
                "appid": "wx38a91c353554588a",
                "secret": app_secret
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
        if "access_token" in result:
            return result["access_token"]
        # stable_token 失败，打印错误继续尝试 GET
        print(f"stable_token 失败: {result.get('errmsg', result)}")
    except Exception as e:
        print(f"stable_token 异常: {e}")

    # ② 尝试 GET /cgi-bin/token（stable_token 失败时的 fallback）
    try:
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx38a91c353554588a&secret=" + app_secret
        with urllib.request.urlopen(url, timeout=10) as r:
            result = json.loads(r.read())
        if "access_token" in result:
            print("使用 GET /cgi-bin/token 获取的 token")
            return result["access_token"]
        print(f"GET /cgi-bin/token 也失败: {result.get('errmsg', result)}")
    except Exception as e:
        print(f"GET /cgi-bin/token 异常: {e}")

    # ③ 都失败
    raise Exception("无法获取 access_token，请确认 AppSecret 是否已更新")

ACCESS_TOKEN = get_token()
```

> ⚠️ **凭证失效是高频事件**：AppSecret 每次重置后旧凭证永久失效（errcode 40125）。当 API 返回 40125 或 40013 时，不要换其他接口重试，立即向用户要新凭证。流程：验证凭证有效性 → 写作 → 上传素材前再次验证凭证有效性（如果中间间隔较长）。

> ⚠️ **Token 有效期与多步发布的矛盾**：access_token 有效期 7200 秒，但完整发布流程（验证→写作→上传封面→上传截图→创建草稿）可能跨多步。mid-session 遇到 `errcode: 40001` = token 过期，立即重新获取 token 再重试。**已上传的 media_id 是永久素材，无需重新上传。**
>
> 推荐时序：①获取token → ②写作 → ③重新获取token → ④上传封面 → ⑤上传截图 → ⑥重新获取token → ⑦创建草稿
# 若文件 /root/.hermes/keys/wx_appsecret.txt 不存在，raise Exception 提示用户写入
- errcode 40125 表示凭证永久无效，需用户提供新的 AppSecret 并更新文件

## 发布流程

### 步骤 0：草稿删除禁令（2026-05-27 最高优先级）

**未经用户明确允许，绝不删除草稿箱中的任何内容。**

即使发现编码问题需要重建草稿，也必须先确认用户意图。可以同时存在多篇正常草稿，待用户确认后再清理。**绝不在未验证修复有效前删除任何草稿。**

### 步骤 1：获取 access_token（必须用 stable_token）

> ⚠️ 旧版 `cgi-bin/token`（GET）返回的 token 在素材接口报 40001。**必须用 `cgi-bin/stable_token`（POST）**。

### 步骤 2：清空旧草稿

微信草稿箱 API 不支持批量删除，需要逐个查询并删除。

**查询草稿列表**：
```bash
curl -s -X GET "https://api.weixin.qq.com/cgi-bin/draft/count?access_token=ACCESS_TOKEN"
# 返回 {"count": N}
```

**获取草稿 media_id 列表**：
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"offset": 0, "count": 50, "no_content": 0}'
```

从响应中提取每篇草稿的 `media_id`。

**删除旧草稿**（每篇一条）：
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"media_id": "MEDIA_ID"}'
```

### 步骤 2.5：上传封面和正文图片（先于草稿创建）

**⚠️ 全角标点清理（每次发布前必做）**：

微信草稿创建前，必须用 Python 检查并清理 HTML 中的全角标点：
```python
html = open('/tmp/article.html').read()
html = html.replace('\uff1a', '')   # 全角冒号 U+FF1A
html = html.replace('\u2014', '-') # em dash U+2014
html = html.replace('\u2013', '-') # en dash U+2013
html = html.replace('\uff02', '"')  # 全角双引号
with open('/tmp/article.html', 'w') as f:
    f.write(html)
```
禁用标点清单：`：` `——` `""` `''`（任何出现都必须在发布前清理）

**⚠️ 必须用 `type=image`！** 旧版 `type=thumb` 会导致草稿创建报 40007 invalid media_id。实测正确流程：封面图 resize 到 300×300 px + quality=85，调用 `add_material?type=image`，返回的 `media_id` 即作为 `thumb_media_id` 传入草稿。

**生成封面图**：短评文章若无可用截图，用 Python PIL 生成纯色封面（800×400，背景色 `#1B365D`，白色居中标题文字），保存到 `/tmp/cover_{article_slug}.png`，上传后得到 `thumb_media_id`。**封面字体必须用 `NotoSansCJK-Bold.ttc` 完整路径**，路径：`/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc`（实测此路径可用，其他路径可能报错）。

**⚠️ Token 刷新原则（必须用 stable_token）**：每执行一次写操作（上传素材 / 创建草稿）之前，单独调用一次 POST `cgi-bin/stable_token` 获取最新 token，再执行操作。不要跨操作复用 token。

```bash
# 获取（刷新）token — 必须用 stable_token POST，GET /cgi-bin/token 返回的 token 在素材接口报 40001
ACCESS_TOKEN=$(python3 -c "
import urllib.request, json, os
secret_file = os.path.expanduser('~/.hermes/keys/wx_appsecret.txt')
with open(secret_file) as f:
    app_secret = f.read().strip()
req = urllib.request.Request(
    'https://api.weixin.qq.com/cgi-bin/stable_token',
    data=json.dumps({'grant_type':'client_credential','appid':'wx38a91c353554588a','secret':app_secret}).encode(),
    headers={'Content-Type':'application/json'},
    method='POST'
)
with urllib.request.urlopen(req, timeout=10) as r:
    print(json.loads(r.read())['access_token'])
")

# 上传封面（type=image，⚠️ 不是 type=thumb！草稿封面必须用 type=image 才会被接受）
curl -s -X POST \
  "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${ACCESS_TOKEN}&type=image" \
  -H "Content-Type: multipart/form-data; boundary=----PythonFormBoundary7MA4YWxkTrZu0gW" \
  -d $'------PythonFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="media"; filename="cover.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'"$(cat /tmp/cover.jpg | base64)"$'\r\n------PythonFormBoundary7MA4YWxkTrZu0gW--'

# 上传正文截图（type=image，返回 mmbiz URL）
curl -s -F "access_token=$ACCESS_TOKEN" -F "type=image" \
  -F "media=@/tmp/screenshot.png" \
  "https://api.weixin.qq.com/cgi-bin/material/add_material"
```

响应示例（成功）：
```json
{"media_id":"kiuyle4KZHC7JKxpTQssMKFZgn...","url":"http://mmbiz.qpic.cn/mmbiz_png/...","item":[]}
```
- `media_id`：封面用 thumb_media_id，正文图片取响应中 `url` 字段作为 mmbiz URL
- **遇到 40001 → 重新获取 token 重试**，已上传成功的 media_id 不需要重新上传

**写完 Python 脚本后、发送 API 请求前，必须执行以下检查**。任何一项不通过，立即汇报用户，不要继续。

**检查项 1 — JSON 结构**：确认 `thumb_media_id`、`title`、`digest`、`content` 四个必填字段存在且非空。

**检查项 2 — 正文 branding 清理**：
```python
content = draft_data["articles"][0]["content"]
forbidden = ["zhiliGitHub", "zhiliComments", "卡兹克", "zhiligithub", "zhilicomments"]
for kw in forbidden:
    assert kw not in content, f"正文包含禁止词: {kw}"
assert "自动发布" not in content, "正文包含禁止词: 自动发布"
```

两项都通过后，方可发送 `draft/add` 请求。

### 步骤 3：创建新草稿

使用 `mpnews` 类型（图文消息）创建草稿，HTML 内容通过 `content` 字段传输。

**CSS 固定格式**：
```html
<body style="background-color:#f5f4ed;font-family:Georgia,'Times New Roman',serif;margin:0;padding:0;">
  <h1 style="font-size:28px;color:#1B365D;margin:20px 0 10px;">标题</h1>
  <h2 style="font-size:20px;color:#1B365D;margin:18px 0 8px;">章节标题</h2>
  <p style="font-size:16px;line-height:1.85;margin:12px 0;">正文段落...</p>
</body>
```

**注意**：
- 标题和正文中如有 `**粗体**`，转为 `<strong style="color:#e63946;">粗体文字</strong>`
- 换行符保留 `\n`
- 图片用 `【图片】` 标注，最终由编辑手动插入

**创建草稿请求**：
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "thumb_media_id": "THUMB_MEDIA_ID",
      "title": "文章标题",
      "author": "刘生",
      "digest": "摘要（可选）",
      "content": "<body>...</body>",
      "need_open_comment": 1,
      "only_fans_can_comment": 0,
      "original": 1
    }]
  }'
```
- `thumb_media_id`：**必须字段**，来自 `material/add_material?type=image`（⚠️ 不是 type=thumb）。封面图必须 resize 到 ≤64KB（建议 300×300 px + quality=85 → ~15KB）。草稿不带 thumb_media_id 会报 `40007 invalid media_id`；用 type=thumb 传也会报 40007，必须用 type=image。
- `author`：**固定填 `刘生`**，不要留空（实测留空不影响创建，但不填更稳定）
- ⚠️ **`content_source_url` 字段禁止出现**：API 文档列出此字段，但实测包含该字段（即使是空字符串 `"content_source_url": ""`）会导致 **44003 empty news data**。完全不传该字段才能创建成功。
- ⚠️ **`articles` 必须小写**：`Articles`（大写A）会导致 44003，只接受小写 `articles`
- 成功响应：`{"media_id": "xxx", "item": [{"index": 0, "ad_count": 0}]}`
- ⚠️ **成功响应不返回 `errcode` 字段！** 不能用 `if resp.json().get("errcode") == 0` 判断成功，必须用 `if "media_id" in resp.json()`。

> ⚠️ **中文乱码问题（`\\uXXXX` 序列在 WeChat API 响应中的含义）**：
> - WeChat `draft/get` API 对 title/author 字段的响应永远以 `\\uXXXX` 格式序列化（这是 WeChat 的序列化行为，不是错误）
> - `ensure_ascii=True`（默认）时：中文 JSON 序列化为 `\uXXXX`，WeChat 存储后**前端草稿箱正确显示中文**（正常）
> - `ensure_ascii=False` 时：中文以 UTF-8 原始字节发送，WeChat 存储后**前端草稿箱显示 `\uXXXX` 字面量**（bug）
> ### 中文乱码：标题正常但正文显示 `\uXXXX` 的差异根因
>
> `ensure_ascii=False` 对 title 和 content 的影响**不一致**：
> - **title 字段**（纯文本）：WeChat 存储/检索时 raw UTF-8 处理正常，标题在前端显示中文，**不受 ensure_ascii=False 影响**
> - **content 字段**（含 HTML）：WeChat 有额外的 HTML 处理管道，raw UTF-8 在该 pipeline 中被错误处理，导致 `\uXXXX` 字面量泄露到前端草稿箱
>
> **验证方式**：对比同一草稿的标题和正文在前端的显示——标题正常、正文显示 `\uXXXX` → 确认是 `ensure_ascii=False` 的 content 字段特有 bug
>
> **结论**：必须用 `json.dumps(payload)` 默认参数（`ensure_ascii=True`），不能用 `ensure_ascii=False`。仅修复 title 的 JSON 序列化是不够的，必须 content 也用 `ensure_ascii=True`。
>
> ⚠️ **`draft/get` API 返回值永远包含 `\uXXXX`**：这是 WeChat API 对所有字段的序列化行为，不是错误判断依据。**判断标准是前端草稿箱显示**，不是 API 返回值。

### 步骤 3：创建新草稿

草稿创建成功后，通过飞书汇报：

**飞书 target ID（必须用 OC 格式，不要用 topic 格式）**：

```
feishu:oc_034bc08420a2daed53561bfceba5b3bf
```

> ⚠️ `send_message` API 若使用 `topic:xxx` 格式会报 `invalid receive_id`（errcode 230001）。正确格式是 `feishu:` + oc ID，不是 `feishu:topic:`。
>
> ⚠️ **常见 target 错误**：
> - `target: "feishu"` → `invalid receive_id`：平台层要求 oc 格式，必须用 `feishu:oc_...`
> - `target: "origin"` → `Unknown platform: origin`：不是有效平台名
> - `target: "feishu:oc_..."` → 正确格式
>
> 如果不确定当前可用的飞书 target，先用 `send_message action=list` 列出所有可用 target，再取 `feishu:oc_...` 格式的那个（通常第一个 DM 目标）。
```
feishu:oc_034bc08420a2daed53561bfceba5b3bf
```
> ⚠️ `send_message` API 若使用 `topic:xxx` 格式会报 `invalid receive_id`（errcode 230001）。正确格式是 `feishu:` + oc ID，不是 `feishu:topic:`。

**成功汇报模板**：
```markdown
✅ 文章已推送到微信草稿箱

标题：xxx
作者：刘生
中文字数：xxx 字
截图：x张（已上传微信素材库）
封面：已上传

⚠️ freepublish/submit 需要高级权限，订阅号请手动发布：
1. 登录 mp.weixin.qq.com
2. 进入内容与互动 → 草稿箱
3. 找到文章 → 编辑 → 发布

**本次任务模型调用记录**

| 调用项 | 模型/工具 |
|--------|----------|
| 文章生成 | MiniMax-M2.7-highspeed |
| 项目数据采集 | CDP Browser |
| 封面图生成 | Python PIL (Pillow) |
| 微信草稿箱发布 | WeChat Draft API（手动发布） |

**本次任务全部完成 ✅**
```

**失败汇报模板**：
```
❌ 发布失败
错误码：xxx
错误信息：xxx
原因：...
```

## 关键教训（血泪教训，实录）

### 🚫 绝不在未验证修复方案前删除任何草稿

**事件**：草稿正文存在 `ensure_ascii=False` 导致的 Unicode 编码问题，用户要求修复并重新创建草稿。在未验证修复方案是否有效之前，错误地批量删除了所有旧草稿（cmux/AIRI/Olah），导致全部草稿丢失。

**正确流程**：
1. 用修复后的代码创建**新草稿**（先不删旧草稿）
2. 验证新草稿前端显示**正常中文**（标题+正文都要正常）
3. 确认正常后，**再删除**旧的问题草稿
4. 如果验证失败，**保留旧草稿**作为备份

**核心约束**：在未收到用户明确「可以删除」的许可之前，草稿箱里的任何内容都不得删除。这是一条铁律。

### 📋 草稿删除的正确判断流程

```
修复代码 → 创建新草稿 → 验证前端显示正常？ → [是] 用户确认可以删除旧草稿 → 删除旧草稿
                                                        ↓
                                                    [否] → 保留旧草稿，修复代码后重试
```

### 🐛 thumb_media_id 不可复用（2026-05-29 新增）

**现象**：复用上一草稿的 thumb_media_id 创建新草稿时，报 `40007 invalid media_id`。

**根因**：微信 `material/add_material` 上传的封面图 media_id 是**一次性绑定**的，与该次上传会话绑定。上一草稿的 thumb_media_id 对新草稿无效。

**正确流程**：
1. 获取新 token
2. 上传封面图（`add_material type=image`）→ 获取**新** thumb_media_id
3. 立即用这个新 thumb_media_id 创建草稿

**错误模式**：
```python
# ❌ 错误：复用旧 thumb_media_id
thumb1 = upload_thumb(token1, cover1)  # 第一次上传
draft1 = create_draft(token1, thumb1)   # 第一次创建草稿，成功
token2 = refresh_token()                # token1 可能过期
thumb2 = upload_thumb(token2, cover2) # 又上传一次封面（浪费）
draft2 = create_draft(token2, thumb1)  # ❌ thumb1 复用，报 40007
```

**正确模式**：
```python
# ✅ 正确：每次草稿创建前单独上传封面
token = get_token()
thumb = upload_thumb(token, cover)  # 只上传一次
draft = create_draft(token, thumb)
```

### 🐛 草稿封面：media_id 是「草稿级」绑定，不可跨草稿复用（2026-05-29 新增）

**现象**：复用上一草稿的 `thumb_media_id` 创建新草稿时，报 `40007 invalid media_id`。

**根因**：`material/add_material` 返回的 `media_id` 是一次性绑定到该草稿的，与上传 token 无关（token 刷新后依然有效，但 media_id 本身只绑定它创建时所在的草稿）。

**⚠️ 重要澄清**：不是「token 过期导致 media_id 失效」，而是「每个新草稿必须用新上传的 `type=image` media_id」。上一草稿的封面 media_id 对新草稿来说永远是 `40007`，即使 token 本身有效。

**正确流程**：
```
① 获取新 token
② upload 封面上传（add_material type=image）→ 新 media_id
③ 创建草稿（立即用②的 media_id）
```
不要试图跨草稿复用封面 media_id。

### 中文乱码问题（`\\uXXXX` 序列在 WeChat API 响应中的含义）
### 中文乱码问题（最终确认，2026-05-30）
> ⚠️ **2026-05-30 多次实测最终确认**：必须用 `ensure_ascii=False` + `Content-Type: application/json`（无 charset）。
> - `ensure_ascii=True`（默认）将中文转为 `\\uXXXX`，WeChat 存储后前端显示字面量 ❌
> - `ensure_ascii=False` 发送原始 UTF-8，WeChat 自己推断编码，前端正确显示中文 ✅
> - 关键：**Content-Type 绝对不能带 charset=utf-8**（WeChat JSON 处理管线无法解码）
>
> ```python
> payload = json.dumps({"articles": [{...content...}]},
>     ensure_ascii=False).encode("utf-8")
> # Content-Type: application/json（不附带 charset=utf-8）
> ```
⚠️ **`draft/get` API 返回值永远包含 `\\uXXXX`**：这是 WeChat API 对所有字段的序列化行为，不是错误判断依据。**判断标准是前端草稿箱显示**，不是 API 返回值。

微信标题有严格的字节限制（errcode 45003）。**先在本地用 Python 预检标题字节数，提前发现问题**，不要等到 API 返回 45003 才去猜。

```python
def calc_title_bytes(title):
    """中文全角字符各占3字节，英文/数字/半角各占1字节，空格占1字节"""
    return sum(3 if ord(c) >= 0x3000 else (2 if '\u4e00' <= c <= '\u9fff' else 1) for c in title)

# 实测通过阈值：纯中文 ≤25字节（实测）；含英文+中文混合 ≤28字节（保守估算）
# 实测失败案例：65字节（"Anthropic 开源职业插件系统：让 AI 先懂行，再干活"含全角冒号）

title = "让 AI 先懂行再干活"
print(calc_title_bytes(title))  # 25 → 通过
title2 = "Anthropic 开源职业插件：让 AI 先懂行，再干活"
print(calc_title_bytes(title2))  # 65 → 超限，需精简
```

**经验阈值**（实测 2026-05）：
- 纯中文标题：≤25字节（约8-9个汉字）
- 含英文+中文混合标题：≤16字符（**英文单词每个占1-2字节，中文每个占2-3字节，极易超标**）
- 全角冒号`：`、全角顿号`、`每个额外占3字节，尽量避免
- **安全实践**：标题中含英文时，先预检实际字节数。`"AI写作去机器味GitHub项目7天"`（18字符）在WeChat报45003，`"AI写作去机器味GitHub项目"`（16字符）成功——差距就在英文字母累加的字节数上。

**安全缩短算法（避免 while 死循环）**：

❌ 错误模式（死循环风险）：无限循环 `while title_bytes > N` + `title.replace("X", "")`，当 replace 返回原字符串时循环永不终止：

```python
# ❌ 危险代码 — replace 找不到子串时返回原字符串，while 条件不变 → 死循环
while title_bytes > 28:
    title = title.replace("来了", "").replace("自托管", "")  # 一旦这两个子串被删光，后续 replace 均返回原字符串，死循环
    title_bytes = calc_title_bytes(title)
```

✅ 正确模式（有限次替换，最多7次）：

```python
def safe_shorten_title(title, max_bytes=25):
    """逐词删除直到字节数达标，最多尝试预定义列表中的一项，超出则截断"""
    def calc(t):
        return sum(3 if ord(c) >= 0x3000 else (2 if '\u4e00' <= c <= '\u9fff' else 1) for c in t)
    if calc(title) <= max_bytes:
        return title
    # 预定义删除计划（按优先级）：优先删短词/虚词，保留实词
    removals = ["来了", "自托管", "开源", "GitHub", "系统", "4万星"]
    for pattern in removals:
        working = title
        while pattern in working and calc(working) > max_bytes:
            working = working.replace(pattern, "", 1)
        if calc(working) <= max_bytes:
            return working
    # 保底截断（取前N个字符）
    chars = []
    byte_count = 0
    for c in title:
        char_bytes = 3 if ord(c) >= 0x3000 else (2 if '\u4e00' <= c <= '\u9fff' else 1)
        if byte_count + char_bytes > max_bytes:
            break
        chars.append(c)
        byte_count += char_bytes
    return ''.join(chars)

title = safe_shorten_title("GitHub 4万星！自托管 Waifu 伴侣来了")
print(title)  # 安全结果，绝不死循环
```

| errcode | 含义 | 处理方式 |
|---------|------|----------|
| 45003 | 标题字节超限 | 用上面函数预检，压缩到 ≤25字节后再重试 |
| 45004 | digest 字节超限 | 缩短摘要，≤54字节（约18个混合字符） |

**错误码表（已修正）**：

| errcode | errmsg | 含义 | 处理方式 |
|---------|--------|------|---------|
| - | （无 errcode 字段） | `draft/add` 成功 | 响应含 `media_id` 字段即成功 |
| 0 | ok | 其他 API 成功 | - |
| 40001 | invalid credential | access_token 无效或已过期 | 重新获取 token |
| 40125 | invalid appsecret | AppSecret 无效 | 不能重试，需用户提供新凭证 |
| 40007 | invalid media_id | thumb_media_id 无效 | 需先上传封面图（type=image resize到≤64KB），且**不可复用旧草稿的 thumb_media_id**（每次必须重新上传）**必须用 type=image（type=thumb 2026-05-30 实测导致 40007，报错记录已废止）** |
| 40007 | invalid media_id | thumb_media_id 复用时报40007 | 已创建草稿的 thumb_media_id 不能用于新草稿，每次上传封面必须使用**全新的 media_id** |
| 44004 | size limit | 多媒体文件超限 | 检查封面图大小 |
| 40013 | invalid appid | AppID 无效 | 检查 AppID 是否正确 |
| 41005 | media data missing | 上传文件为空或格式错误 | 用 `curl -F` 替代 urllib.request 构造 multipart（urllib.request 报 41005，curl -F 成功） |
| 42001 | access_token expired | token 过期 | 重新获取 |
| 45003 | title size out of limit | 标题字节超限 | 缩短标题，预检函数：纯中文≤25字节，英文+中文混合≤28字节 |
| 45003 | title size out of limit | 标题字节超限 | 缩短标题，预检函数：纯中文≤10字符（含标点），英文+中文混合≤16字符 |
| 45003 | title size out of limit | 混合标题18字符仍报45003 | 实测`AI写作去机器味GitHub项目7天`(18字符)失败，`AI写作去机器味GitHub项目`(16字符)成功。根因：微信检查字节数而非字符数，中文×2-3字节+英文×1字节混合后易超限。安全阈值：**含英文时≤16字符**，纯中文≤10字符 |
| 45003 | title size out of limit | 纯中文12字报45003 | `免费域名这件事，为什么突然变天了`（12字符）报45003，缩短到`免费域名为什么突然变天了`（11字符）成功。微信对标题字段有额外编码开销，实测纯中文安全阈值为**≤10字符**，不是「汉字×2字节」的乐观估算 |
## 标题字节超限（45003）

**根因**：微信标题字段采用 GBK 编码（中文=2字节，英文/空格=1字节），纯中文12字即可能超限，含英文标题更易超标。

**安全阈值**：纯中文≤25字节，含英文+中文混合≤20字节。安全实践：写完先在本地预检，用 `references/safe_title_shorten.py` 快速验证。

**修复**：用 `safe_shorten_title()` 自动压缩，绝不死循环：
```bash
python3 references/safe_title_shorten.py "你的原始标题"
```
| 45004 | digest size out of limit | digest 字节超限 | 缩短摘要，≤54字节（约18个混合字符） |
| 45004 | digest size out of limit | 实测27字符中文摘要仍报45004 | WeChat 计算的是**字节数而非字符数**。`"stop-slop：专治AI机器味，上线一周6000星"`（27字符，~54字节）超限，缩减到 `~`18字符后成功 |
| 45110 | author field invalid | author 字段含非法字符 | 固定填 `刘生`，不要留空 |
| 44003 | empty news data | payload 结构不完整 | 检查 `articles`（小写）、`thumb_media_id` 是否存在 |
| 48001 | api unauthorized | freepublish 权限不足 | 草稿已创建，手动在 mp.weixin.qq.com 发布 |

---

## 常见错误处理

> 📋 新增参考：`references/wechat-draft-freepublish.md` — freepublish 权限边界与草稿验证正确方式（2026-05 实测）

> ⚠️ **2026-05-30 最终确认（已实测验证）**：问题根因是 `json.dumps()` 的 `ensure_ascii` 参数与 WeChat HTML 处理管道的交互。
> - `ensure_ascii=False` 时：中文以 UTF-8 原始字节发送，WeChat HTML pipeline 正确解码，前端**正常显示中文** ✅
> - `ensure_ascii=True`（默认）时：中文 JSON 序列化为 `\\uXXXX`，WeChat 存储后前端显示 `\uXXXX` 字面量 ❌
>
> **结论**：必须用 `json.dumps(payload, ensure_ascii=False)` + `Content-Type: application/json`（不附带 `charset=utf-8`）。

### 📋 `ensure_ascii=False` 是错误方案（2026-05-30 已确认）

> ⚠️ **已确认为错误方案**，不要使用 `ensure_ascii=False`。正确的修复方法是：
> - 全局搜索两个 publish_zhili.py 中的 `ensure_ascii=False`，**全部改为默认参数**（删除 `ensure_ascii=False`）
> - 同时删除 `Content-Type` 头中的 `; charset=utf-8`

**受影响的位置**：
- `/root/.hermes/skills/openclaw-imports/zhiligithub/scripts/publish_zhili.py` 第 443 行、第 564 行
- `/root/.openclaw/skills/zhili-publish/scripts/publish_zhili.py` 第 390 行、第 506 行

**验证修复是否完成**：在两个脚本中搜索 `ensure_ascii=False`，搜索结果必须为空。

**判断标准**：
- `draft/get` API 返回的 content 永远是 `\\uXXXX` 格式（WeChat API 序列化行为，非错误）
- 关键看微信公众平台草稿箱前端是否显示正常中文（不是 `\\uXXXX` 字面量）
- 若前端显示 `\\uXXXX` 字面量，说明草稿创建时用了 `ensure_ascii=True`（默认值），需要删除重建并改用 `ensure_ascii=False`

## 参考文件

- `references/wechat-title-limits.md` — 微信标题字数限制实测（纯中文≤10字符，混合≤16字符，2026-05 更新）

## 触发条件

用户说「发布」「推送到微信」「草稿箱」「发文章」「出稿」且上下文是 zhiliGitHub 或 zhiliComments 文章完成时，触发本 skill。

## 附：发布后草稿验证（确保中文正确显示）

创建草稿后，用以下方式验证标题是否正确存储：

```python
# python3 -c "
import json, subprocess, os, ssl, urllib.request

APPID = 'wx38a91c353554588a'
with open(os.path.expanduser('~/.hermes/keys/wx_appsecret.txt')) as f:
    APPSECRET = f.read().strip()

# get token
result = subprocess.run(['curl', '-s', '-X', 'POST',
    'https://api.weixin.qq.com/cgi-bin/stable_token',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({'appid': APPID, 'secret': APPSECRET, 'grant_type': 'client_credential'})],
    capture_output=True, text=True)
ACCESS_TOKEN = json.loads(result.stdout)['access_token']

# list drafts
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(
    f'https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={ACCESS_TOKEN}',
    data=json.dumps({'offset': 0, 'count': 20}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
    items = json.loads(resp.read().decode('utf-8')).get('item', [])
    for item in items:
        content = item.get('content', {})
        ni = content.get('news_item', [{}])[0] if content.get('news_item') else {}
        print(ni.get('title', 'N/A'), '|', ni.get('author', 'N/A'))
"
```

**判断标准**：
- `draft/get` API 返回的 title 永远是 `\uXXXX` 格式（WeChat API 序列化行为，非错误）
- 关键看微信公众平台草稿箱前端是否显示正常中文（不是 `\uXXXX` 字面量）
- 若前端显示乱码（`\uXXXX` 字面量），说明草稿创建时用了 `ensure_ascii=False`，需要删除重建
- **根因**：`ensure_ascii=False` 导致中文以 UTF-8 原始字节发送，WeChat 存储错误；修复方法是用 `json.dumps(payload)` 默认参数（`ensure_ascii=True`）