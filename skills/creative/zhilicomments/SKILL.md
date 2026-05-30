---
name: zhiliComments
description: >
  微信公众号短评论发布技能，专为「直隶按察使」公众号的卡兹克风格评论方向定制。
  适用：一事一议的短观点、热评reaction、资讯点评（**800-1500字**，2026-05-24 佳哥确认）。
  触发条件：用户说「评论」「热评」「观点」「点评」「说两句」。
  **执行前必读**：每次写 HTML 前必须按顺序执行以下三步，再开始写作：
  1. 读取规范参考文件 `references/streambert-reference.html`，提取 CSS 检查清单（字体、层级、高亮、分隔线、blockquote、标签行、作者信息位置等）
  2. 按规范生成 HTML，内联所有 CSS
  3. 生成完毕后，对照第 1 步的检查清单逐项验证，合格后再推送草稿
---

# 直隶按察使 · 短评论发布技能

## 与 zhili-publish 的区别

| | zhili-publish | zhilicomments |
|--|---------------|---------------|
| 字数 | 1500-2000字 | 800-1500字 |
| 结构 | Evolver 六段式 | 卡兹克轻量短评式 |
| 配图 | 项目截图+封面 | 1-2张评论配图 |
| 用途 | 项目介绍/教程 | 热评/观点/Reaction |

## ✅ CSS 渲染规范：样式A（标准模板，2026-05-30 固化）

> ⚠️ zhilicomments 与 zhiliGitHub 共用样式A，无需读取 `references/streambert-reference.html`。直接按以下规范生成 HTML 即可。

### 样式A 核心参数

| 属性 | 值 |
|------|-----|
| 背景色 | `#f5f4ed`（羊皮纸） |
| 正文字体 | `Georgia, 'Noto Serif SC', serif` |
| H2 标题 | `border-left: 4px solid #1B365D`，左边框墨蓝高亮 |
| 强调色（数据/核心） | `#c9553d`（红棕色） |
| 强调色（关键词/重点） | `#1B365D`（墨蓝） |
| 警示/核心洞察背景 | `#fff3b0`（淡黄底） |
| 引言/摘要样式 | 左边框 `#1B365D` + `background:#f0efe8` + 斜体 |
| 分隔线 | `· · ·` 居中，`color:#c9553d` |
| 代码块 | `background:#1e1e1e`，白色文字 |
| 适合/不适合标签 | 同 zhiliGitHub |
| 正文段落 | `font-size:16px; line-height:1.85; color:#2c2c2c` |

### 正文高亮规则（zhilicomments 特有写法）

- **墨蓝高亮**（关键词/重点）：`<strong style="color:#1B365D;">`
- **红棕高亮**（数据/核心）：`<strong style="color:#c9553d;">`
- **黄底高亮**（警示/核心洞察）：`<strong style="background:#fff3b0;">`

### ❌ 禁止事项

- 禁止使用纯白色 `#ffffff` 背景
- 禁止使用 `#00d4aa` 等亮绿色作为主色调
- 禁止删除 `font-family` 中的 `Georgia`
- zhilicomments 正文不强制要求 mmbiz 图片（不同于 zhiliGitHub）

## 内容格式（卡兹克短评式）

> ⚠️ 核心原则：zhilicomments 的内容必须完全遵循卡兹克的写作风格，不是"类似"，是完全一致。字数 800-1500字，比长文短，但灵魂和长文一样。

### 写作要求（强制执行）

**篇幅**：800-1500字

**结构**：不分章节，不用「一、」「二、」「三、」小标题。从头到尾一口气顺下来，靠节奏和口语化转场推进。

**节奏感**：
- 句子要短。15-20字一顿。大量的逗号制造口语停顿感。
- 经常一句话独立成段，制造断裂和重点。
- 段落极短，很多段落只有2-3句话。

**口语化转场词**（自然穿插，不是每句都要用）：
- 转场：说真的、怎么说呢、其实吧、回到这块、顺着上面的
- 判断：我有时候觉得、反正我觉得、这话听着有点刺耳但
- 情绪：给我整懵了、太离谱了、太特么离谱了
- 拉近距离：很多朋友可能不知道、你想想看

**观点表达**：
- 亮出立场，不做理中客
- 用「我觉得」「我认为」「我有时候觉得」而不是「人们普遍认为」
- 承认自己的局限：「我也不是完全确定」「我自己有时候也会」
- 对立面理解：先承认对方处境合理，再切入自己的角度

**案例写法**：
- 用人物画像法：从一个数据点出发，快速代入具体人的完整人生
- 3-5句话让一个人物立体
- 不要编造，用真实细节

**收尾**：
- 金句或反问
- 不求 Star/转发/关注
- 纯观点文，观点本身即是结束

### 内容三段式（内化于心，不用外显）

这三个部分内化在文章里，不是显性的章节结构：

**第一部分（约200字）**：感性切入。从一个具体的、当下的事件或场景开始。不是宏大叙事，是"事情是这样的"的切入感。先建立情绪，让读者想知道"然后呢"。

**第二部分（约600-1000字）**：核心观点轰炸。每一个观点都有具体场景/人物/对话支撑。不是罗列，是聊着聊着自然展开。偏离主线了用一句扣主线句拉回来。至少用3-5个口语化表达。

**第三部分（约50-100字）**：金句或反问收尾。独立成段，一句话。短促有力。不需要号召行动，不需要"大家可以转发关注"，纯观点，纯态度。

### 卡兹克风格检查清单（写完必须自检）

**基础检查（任何不通过必须修复）**：

- [ ] 禁用词零命中：`说白了`、`意味着什么`、`这意味着`、`本质上`、`换句话说`、`不可否认`、`综上所述`
- [ ] 禁用标点零命中：冒号`：`、破折号`——`、双引号`""`
- [ ] 空泛工具名零命中：没有「AI工具」「某个模型」等表述
- [ ] 开头是否具体当下？第一句话是否让读者产生"然后呢"的冲动？
- [ ] 连续5句以上句式长度相近 = 节奏呆板（必须避免）

**风格检查（至少满足5/7）**：

- [ ] 一句话独立成段断裂效果（全文至少3次）
- [ ] 口语化词组自然穿插（全文至少5个不同表达）
- [ ] 疑问句作为节奏刹车（让读者停一秒）
- [ ] 人物画像法：3-5句话让一个人物立体
- [ ] 至少一处自嘲或承认不足
- [ ] 对立面的理解：先承认对方处境合理，再切入自己角度
- [ ] 结尾是金句或反问，不是号召行动

**活人感终审（最关键）**：

- [ ] 情绪表达是体感记忆（「我当时就愣住了」）而非知识性描述（「我感到震撼」）
- [ ] 有没有「只有卡兹克才会写出来的角度」，还是换一个AI博主也能写差不多？
- [ ] 语气是「有见识的普通人在认真聊」，不是「导师在教学生」
- [ ] 从头到尾读，有没有哪个地方注意力断掉了？（如果有，那个地方需要修复）

### 禁止出现（绝对禁区）

- 禁用词：`说白了`、`意味着什么`、`本质上`、`换句话说`、`不可否认`
- 禁用标点：冒号`：`、破折号`——`、双引号`""`（用「」或直接不加）
- 禁用开头：`在当今AI快速发展的时代`、`随着技术的不断进步`、`让我们来看看`
- 禁止连续使用 bullet point 罗列观点（超过2个就要改散文叙述）
- 禁止加粗小标题分隔板块（不用 `**小标题**`这种东西）

## ✍️ stop-slop 文风诊断（写完必查）

> stop-slop 是一套 AI 文风去除术，源于 CrewAI 社区的 `hardikpandya/stop-slop` 项目（7k+ Stars）。核心思路：AI 写东西有套路，套路让人读起来像机器，这套检查表专门治这个。
>
> **stop-slop 的框架**：Core Rules（8条铁律）→ Quick Checks（12问）→ Scoring（5维度50分，35分以下打回重写）
>
> 对中文写作来说，框架完全通用，但词条需要本地化重建。

### 中文 stop-slop 检查表（zhilicomments 版，每篇必查）

**第一步：数一数有没有这些废话填充词**

| # | 中文废话 | 替换建议 |
|---|---------|---------|
| 1 | 值得注意的是 | 直接删，后面直接说观点 |
| 2 | 实际上、其实 | 直接删，事实不需要铺垫 |
| 3 | 那么、那么就 | 很多是噪音，可删 |
| 4 | 大家/我们都知道 | 谁？直接说 |
| 5 | 从某种意义上来说 | 要说就说清楚 |
| 6 | 归根结底 | 直接说结论 |
| 7 | 不得不承认 | 直接删 |
| 8 | 想必、应该（猜测语气） | 不确定就别用 |
| 9 | 毫无疑问 | 直接删，显得心虚 |
| 10 | 必须承认 | 直接删 |
| 11 | 我想说的是 | 删，直接开口就说 |
| 12 | 相信大家都知道 | 谁？不点名就说 |

**出现3个以上，这篇文章就已经有 AI 味了。**

**第二步：检查句式结构（5条）**

- [ ] 没有「首先、其次、最后、总之」套路（三板斧）
- [ ] 没有「一方面、另一方面」平衡结构（假辩证）
- [ ] 没有「随着…的发展」宏大叙事开头
- [ ] 没有无主语句（「已被广泛认可」「这一观点受到关注」）
- [ ] 没有因果废话（「因为 X，所以 X，这说明」）

**第三步：快速 12 问（英文原版，可跳过直接看中译）**

| # | 问题 | 中文版 |
|---|------|--------|
| 1 | Any filler phrases? | 有废话填充词吗？ |
| 2 | Any em-dashes? | 有破折号吗？（中文破折号可保留，这条忽略） |
| 3 | Starting sentences with "It's..."? | 有「它是…」「这是…」开头吗？ |
| 4 | Passive voice? | 有被动语态吗？（中文无此问题，跳过） |
| 5 | Weasel words? | 有模糊词吗？（想必、应该、可能） |
| 6 | Complex words where simple ones exist? | 能用一个字说清楚用了两个字吗？ |
| 7 | Any AI-sounding buzzwords? | 有AI黑话吗？（颠覆、创新、引领、赋能） |
| 8 | Sentence length variation? | 句长有变化吗？（连续10句一样长=呆板） |
| 9 | Read it out loud? | 读出来顺口吗？（不顺口就要改） |
| 10 | Generic examples? | 案例具体吗？（张三李四王五，要具体到人） |
| 11 | Does the writing sound like a robot? | 读起来像机器吗？ |
| 12 | Did you actually mean what you wrote? | 你真的想表达这个吗？ |

**综合判断**：12问里超过4个「有问题」→ 打回修改。

### stop-slop 评分（可选，不强制）

| 维度 | 满分 | 得分 | 说明 |
|------|------|------|------|
| 直接性 | 10 | __/10 | 没有废话填充词，直接进入 |
| 节奏感 | 10 | __/10 | 句长有变化，一句话独立成段 |
| 信任感 | 10 | __/10 | 不吹不黑，承认局限 |
| 真实感 | 10 | __/10 | 体感记忆，不是知识描述 |
| 密度 | 10 | __/10 | 信息量大，没有废话段落 |
| **总分** | **50** | **__/50** | **35分以下必须重写** |

### stop-slop 中文适配的核心差异

英文 stop-slop 说「No em-dashes」，但中文破折号用法完全不同——这条直接忽略。

英文 stop-slop 里有大量商业黑话替换表（如 navigate → handle，leverage → use），中文对应的黑话池：

```
突破瓶颈 → 解决
赋能 → 帮助
持续迭代 → 更新
深度赋能 → 提高
构建生态 → 攒人
引领变革 → 搅局
核心价值 → 好处
解决方案 → 方法
```

> 📌 **格式规范**：HTML/CSS 格式规范见 `references/format.md`（含 Kami 羊皮纸视觉系统 + 增强版模板）
> 📌 **API 踩坑**：WeChat API 实操经验见 `references/wechat-pitfalls.md`

## 发布流程

```
获取内容 → 生成/下载配图 → 写HTML → 创建草稿 → 完成
```

### 第一步：获取内容

用户提供：评论对象（链接/标题/截图）+ 核心观点（一句话）+ 支撑素材（可选）

**推荐获取优先级**：用户复制粘贴 > mmx vision 截图分析 > 自行搜索补充背景 > 尝试网页抓取

详细内容见 `references/wechat-pitfalls.md` 的「内容源可访问性」章节。

### 第二步：配图（可选）

短评论可以无图，但如果配图：

1. 用 PIL 生成信息图（900×383 或 900×900）：`/tmp/cover.jpg`
2. 上传获取 `media_id`（必须用 urllib.request 构造 multipart）

关键踩坑见 `references/wechat-pitfalls.md`。

> ⚠️ **封面图必须用 `type=image`**（2026-05-30 实测）。旧版记录 `type=thumb` 可用为错误信息。`type=thumb` 返回的 media_id 在 `draft/add` 时报 `40007 invalid media_id`，**必须用 `type=image`**。

### 第三步：写 HTML

> ⚠️ **写 HTML 时优先复制** `references/format.md` 中的增强版 HTML 模板（含 Pull Quote、装饰线、标签卡片等完整样式）。

排版规则：
- block 元素必须单独一行，不能有换行符分隔
- 禁止 ul/li，用 `•` 代替
- 只用 `margin-bottom` 控制间距，不管 `margin-top`
- 所有样式内联
- 标题 ≥10字，卡兹克风格，观点鲜明，有情绪张力

### 第四步：创建草稿

关键踩坑见 `references/wechat-pitfalls.md` 的 `urllib.request` 上传章节。

凭证从 `references/config.md` 读取：APPID、APPSECRET。

草稿创建关键参数：
```python
# ⚠️ 必须用 ensure_ascii=False，直接传 UTF-8 原文
# ensure_ascii=True（默认）会将中文转为 \\uXXXX 字面量，微信预览渲染器直接显示为乱码
# Content-Type 必须是 application/json，不带 charset=utf-8（否则微信 JSON 处理管线无法解码原始 UTF-8）
payload = json.dumps({
    "articles": [{
        "title": "标题",
        "author": "刘生",
        "digest": "摘要",
        "content": html_content,
        "thumb_media_id": media_id,  # 必须用 type=image 上传（type=thumb 会报 40007）
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}, ensure_ascii=False).encode('utf-8')  # Content-Type: application/json（无 charset）
```

> ⚠️ **草稿创建前必须验证 HTML 中的图片URL**：如果文章有配图（cover.jpg / cover.png），必须确认 HTML 里使用的是本次实际上传的图片 media_id 对应的 mmbiz URL，而不是上一次残留的旧URL。验证方法：检查 HTML 中所有 `src="http://mmbiz.qpic.cn/` 是否与封面图的 url 一致。如果用了旧图，微信会报 `40007` 或显示异常。

## access_token 获取（2026-05-28 实测正确方式）
## access_token 获取（2026-05-30 确认）

必须用 **stable_token POST**，不能用 GET `/cgi-bin/token`（后者返回的 token 在素材接口报 40001）。

```python
import urllib.request, json, os

APPID = 'wx38a91c353554588a'
with open(os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")) as f:
    app_secret = f.read().strip()

req = urllib.request.Request(
    "https://api.weixin.qq.com/cgi-bin/stable_token",
    data=json.dumps({"grant_type":"client_credential","appid":APPID,"secret":app_secret}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    access_token = json.loads(r.read())["access_token"]
```

## urllib.request 上传优于 subprocess curl

WeChat 的 material/upload 接口对 curl subprocess 调用有静默失败问题（curl 返回空但 API 正常），建议始终用 urllib.request 构造 multipart/form-data：

```python
import urllib.request, json, ssl

boundary = '----PythonFormBoundary123456'
with open('/tmp/cover.jpg', 'rb') as f:
    img_data = f.read()
body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
    f'Content-Type: image/jpeg\r\n\r\n'
).encode('utf-8') + img_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image'
req = urllib.request.Request(url, data=body, method='POST')
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
ctx = ssl.create_default_context()
ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
    result = json.loads(resp.read())
    media_id = result['media_id']
```

## 封面图规格

- 尺寸：900×383（信息图比例）或 900×900（方图）
- 风格：深色背景 + 高对比文字，观点鲜明
- 可用 PIL 纯代码生成

## 创意增强：观点提炼与角度深化

写短评前，先用以下流程找到最独特的观点，再动笔。

### 第一步：用「角度法」找到最有张力的切入点（ad-creative）

拿到一个话题/事件，先用 ad-creative 的 8 大角度类型枚举所有可能方向：

| 角度类型 | 适合哪种话题 |
|---|---|
| **痛点型** | 这件事让谁难受？怎么个难受法？ |
| **结果型** | 这么做了/不这么做的结果差多少？ |
| **社会证明型** | 谁在这么做？规模多大？ |
| **好奇心型** | 反常识事实是什么？ |
| **对比型** | 这个和通常的做法真正区别在哪？ |
| **紧迫感型** | 再不关注就来不及了？ |
| **身份认同型** | 什么样的人在乎这个？ |
| **反主流型** | 普遍看法哪里错了？ |

**操作方法**：枚举 3-5 个角度，每个角度用一句话写出核心，然后比较哪个最有情绪张力、最独特，选定后再动笔。

### 第二步：用「悖论挖掘」提升观点深度（creative-thought-partner）

选定角度后，用四大驱动检验是否足够深：

**Driver 1 - 模式识别**：这件事，业界/大众通常怎么想？我选的切入点和他们的认知差在哪？

**Driver 2 - 悖论挖掘（最重要）**：
- 有没有「表面看是这样，实际上恰好相反」的核心洞察？
- 大多数人觉得 A，我为什么觉得 B？
- 有没有一个大多数人不愿承认但确实是事实的矛盾？

**Driver 3 - 命名未命名**：能不能给这个洞察起一个让人一听就记住的名字？

**Driver 4 - 对比创造**：如果有人完全相反地理解这件事，会失去什么？

### 第三步：炼句强化标题和开头

**标题炼句**（≥10字，卡兹克风格）：

| ✅ 强标题 | ❌ 弱标题 |
|---|---|
| 反直觉（"为什么越骂越火"） | 平铺直叙 |
| 具体场景（"程序员开始用AI摸鱼"） | 抽象概念（"AI改变工作方式"） |
| 情绪张力（"这个事恶心到我了"） | 无情绪 |
| 身份锁定（"做独立开发的才懂"） | 面向所有人 |

**开头写法**：第一句就要制造「然后呢」冲动。不要从「随着AI发展」这种宏大叙事开始，从一个具体的、当下的、能让读者立刻代入的场景切入。

### 第四步：观点轰炸层的节奏控制

- **疑问句刹车**：每隔 2-3 段抛出一个问题，让读者停一下
- **先承认对立面**：对方处境合理，但……（然后反转）
- **体感记忆**：「我当时就愣住了」比「让我感到震惊」有力 10 倍
- **自嘲**：承认自己也会犯错，增加信任感

## 注意事项

- 正文配图可选，有则用深色信息图风格
- 观点要有立场，不做理中客
- 结尾不求 Star/项目地址，纯观点文
- **禁用词（严禁出现）**：`说白了`、`意味着什么`、`本质上`、`换句话说`、`不可否认`、`冒号`、`破折号`
- 所有文字 **`text-align:left`**，无例外
- **禁止连续 bullet list**，超过2个观点必须改散文叙述
