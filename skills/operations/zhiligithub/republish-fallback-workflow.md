# 复扒发布（Republish）Fallback 工作流

> 当用户说「重新发布」「用 zhiliGitHub 重新写作并发布」，而原始内容源不可达时的标准工作流。

---

## 触发条件

用户要求重新发布一篇已写过但未找到的文章，典型场景：

- "flowus find X" 搜索返回 0 条
- FlowUs API 返回 500 / semantic_search 报错
- 原始平台（GitHub、微信文章链接等）已删除或 404

---

## 选择性执行原则（重要）

当用户说「执行1，不/别管2」时，意味着选择性执行：

- 只执行指定的明确动作
- 不要试图同时解决所有悬而未决的问题
- 搜不到就搜不到，删掉坏草稿就删，不要给出完整解决方案

→ **不要被未解决的文章卡住执行路径。**

---

## 标准工作流

### Step 1：检查本地缓存文件

标准命名规范：

```
/root/article_{slug}.md        # 已转换的 HTML 内容（未发布的草稿）
/root/{slug}-article.txt       # 原始纯文本内容
/root/{slug}_article.md        # 备用格式
/tmp/article_{slug}.html      # 临时草稿
```

```bash
# 快速搜索本地文件
ls /root/ | grep -i "article\|ppt\|saas\|freqtrade\|cli"
grep -rl "关键词" /root/*.txt /root/*.md 2>/dev/null | head -5
```

### Step 2：本地文件存在 → 读取并重建 HTML

```python
# 读取本地缓存
with open('/root/article_saaskit.txt', encoding='utf-8') as f:
    content = f.read()

# 检查内容是否含【场景标签】（khazix-writer 格式）
if '【' in content:
    # 需要转换场景标签为 HTML bold p 标签
    pass

# 直接重建草稿（见下方 Step 3）
```

### Step 3：本地文件不存在 → 尝试原始来源重建

按优先级尝试：

1. **GitHub API**：`GET /repos/{owner}/{repo}` 查 stars/description
2. **GitHub README**：`GET /repos/{owner}/{repo}/contents/README.md` + base64 解码
3. **用户粘贴**：请用户复制正文内容
4. **mmx vision**：用户截图 → AI 分析内容
5. **完全重建**：根据标题和关键词从公开信息重建文章

> ⚠️ **重要约束**：不要从记忆/推测重建草稿。内容源不可达时，**停下来请求用户提供内容**。草稿箱只能看标题+摘要，看不到正文，乱码直接上线才发现，代价高。

### Step 4：GitHub API 特殊情况

某些 GitHub 仓库存在但 API 返回 404（如私有仓库镜像、已删除仓库的引用）。处理方式：

```bash
# 搜索 GitHub（绕过直接 API 404）
curl -s "https://api.github.com/search/repositories?q=关键词+仓库名" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); ..."

# 备选：用项目描述中的关键字符搜索
curl -s "https://api.github.com/search/repositories?q=描述关键词" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); [print(x['full_name'], x['stargazers_count']) for x in d.get('items',[])[:5]]"
```

---

## 封面图 Fallback（GitHub OG 图失败时）

GitHub OG 图 `https://opengraph.githubassets.com/1/{owner}/{repo}` 可能返回 42 字节（失败），处理方式：

```python
# PIL 生成封面图（完全离线，无需 API key）
from PIL import Image, ImageDraw, ImageFont

def create_cover(path, title_text, subtitle_text, accent_color, bg_color=(255,255,255)):
    W, H = 900, 383
    img = Image.new('RGB', (W, H), bg_color)
    d = ImageDraw.Draw(img)
    
    # 左侧强调条
    d.rectangle([0, 0, 6, H], fill=accent_color)
    
    # 标题和副标题
    d.text((40, 80), title_text, fill=(30, 30, 30), font=font_large)
    d.text((40, 150), subtitle_text, fill=(100, 100, 100), font=font_sub)
    
    # Stars badge
    d.rounded_rectangle([W-200, 30, W-40, 70], radius=8, fill=accent_color)
    
    # 底部装饰线
    d.rectangle([40, H-20, W-40, H-16], fill=accent_color)
    
    img.save(path, "JPEG", quality=90)
```

常用 accent_color 取值：
- 蓝色（技术工具）：`(0, 123, 189)`
- 橙色（PPT/演示）：`(250, 100, 0)`
- 绿色（量化/金融）：`(0, 150, 100)`
- 紫色（AI/创意）：`(142, 36, 170)`

---

## 已知不可达来源（不要再浪费时间）

| 来源 | 错误 | 替代 |
|------|------|------|
| `api.anspire.cn` | DNS 不可达（服务器环境） | Bocha API / 用户粘贴 |
| 搜狗微信搜索 | 超时 | 用户复制正文 |
| 微信滑块验证码 | WeChat 反爬 | 用户复制 / mmx vision |
| GitHub `raw.githubusercontent.com` | 超时 | GitHub API + base64 解码 |
| 9Router fetch-combo/jina | 返回 404 | 直接 API / 用户粘贴 |
| FlowUs REST API search | 返回 0 条（workspace 索引限制） | 用户粘贴 / 其他来源 |

---

## 复扒发布完整流程图

```
用户要求复扒「X」
    │
    ▼
检查 /root/ 本地缓存文件
    │
    ├── 存在 → 读取内容 → 转换 HTML → 重建草稿
    │
    └── 不存在
            │
            ▼
        尝试原始来源（GitHub API / FlowUs / 微信链接）
            │
            ├── 成功 → 读取内容 → 转换 HTML → 重建草稿
            │
            └── 失败
                    │
                    ▼
                请用户粘贴正文 或 mmx vision 截图分析
                    │
                    ▼
                重建内容 → 转换 HTML → 重建草稿（须用户确认）
```

---

## 凭证说明

**WeChat AppSecret**：
- 文件路径可能不可靠（`/root/.hermes/keys/wx_appsecret.txt` 未必存在）
- 若文件不存在，用记忆中 hardcode 的值：`07b4dc2d64ddbe6f53707977dbabdbbe`
- 会话文件不存 API 响应，只存消息历史，不要依赖 session 文件查 token

---

## 本 session 实录（2026-05-21）

**案例一：选择性执行原则**

用户说「执行1，不总管2」—— 要求删掉草稿箱里乱码的 CLI 文章（action 1），不要被未解决的 PPT 文章（action 2）卡住。

→ **原则**：用户明确指定动作时，只执行那个动作，不试图同时解决所有悬而未决的问题。

**案例二：从记忆重建导致乱码**

CLI 文章（Feishu/WeCom/DingTalk CLI 对比）是从记忆重建的，草稿箱里中文全部变成 `\u4eb2\u6d4b` 乱码序列。根因：HTML 中的中文字符被 Python JSON 序列化时双重编码。

→ **原则**：内容源不可达时，**停下来请求用户提供内容**。不要从记忆/推测重建草稿。草稿箱只能看标题+摘要，看不到正文，乱码直接上线才发现。

**案例三：AppSecret 文件路径不可靠**

`/root/.hermes/keys/wx_appsecret.txt` 路径不存在。会话文件不存 API 响应，只存消息历史。

→ **处理**：AppSecret 硬编码在记忆中，直接用 hardcode 重新获取 token。不依赖文件路径。

**本次执行记录**：草稿箱 1 篇乱码 CLI 文章 → 已删除，草稿箱清空至 0 篇。
