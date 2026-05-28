# 配图工作流：先拿 URL，后写 HTML

## 核心原则（一句话）

> **永远不要在拿到 mmbiz URL 之前写 HTML。**

发布脚本的 `check_article_images()` Gate 会拦截无图发布，但这意味着你会在最后一步被打回来重新上传图片、重新写 HTML、重新发布——浪费时间。

**正确的顺序是把图片工作做在前面**，这样写 HTML 时直接填入 URL，不用返工。

---

## 强制执行顺序

```
Step 1  下载项目截图/GIF/视频
Step 2  上传到微信 media/uploadimg，获取 mmbiz URL
Step 3  记录每个 URL 对应的「插入位置」（如：section 二 banner、section 五 demo）
Step 4  写 HTML — 在对应位置直接嵌入 <img src="mmbiz_url">
Step 5  发布 — Gate 会检查 HTML 中的 mmbiz URL（这时一定有了）
```

**违反这个顺序 = 被 Gate 拦截 = 返工**

---

## 具体操作

### Step 1: 下载项目截图

```bash
# 查项目有哪些图片
curl -s "https://api.github.com/repos/{owner}/{repo}/contents" | python3 -c "import sys,json; data=json.load(sys.stdin); [print(f['name'], f.get('download_url','')) for f in data if isinstance(f,dict) and f.get('type')=='file' and any(f['name'].endswith(ext) for ext in ['.png','.gif','.jpg','.jpeg'])]"

# 备选：GitHub OG 图（总有，除非项目私有）
curl -s "https://github.com/{owner}/{repo}" | grep -o 'https://opengraph.githubassets.com[^"]*' | head -1

# 下载到 /tmp/
curl -s "https://opengraph.githubassets.com/.../{owner}/{repo}" -o /tmp/project_og.png
```

**常见项目图片目录**（优先查这些）：
```
README.md 同级
assets/
docs/images/
screenshots/
demo.gif / demo.mp4
```

**项目完全没有图片时**：用 GitHub OG 图（见上面 curl 命令），在 HTML 中标注「项目暂无截图，用 GitHub OG 图代替」。

### Step 2: 上传到微信获取 mmbiz URL

⚠️ **封面图和正文图都走 `material/add_material`**：
- 封面图：`type=image` → 取返回的 `media_id` 作为 `thumb_media_id`（⚠️ 不是 `type=thumb`）
- 正文图：`type=image` → 取返回的 `url` 作为 mmbiz URL 嵌入 HTML

```python
import urllib.request, json, base64, os
from PIL import Image

APPID = "wx38a91c353554588a"
with open(os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")) as f:
    APPSECRET = f.read().strip()

# 获取 token
req = urllib.request.Request(
    "https://api.weixin.qq.com/cgi-bin/stable_token",
    data=json.dumps({"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET}).encode(),
    headers={"Content-Type": "application/json"}, method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    token = json.loads(r.read())["access_token"]

def upload_image_for_article(token, image_path):
    """上传正文图片，返回 mmbiz URL（用于 HTML img src）"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    boundary = "----PythonFormBoundary7MA4YWxkTrZu0gW"
    with open(image_path, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="image.png"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["url"]  # mmbiz URL

def upload_thumb_for_draft(token, image_path):
    """上传封面图，返回 media_id（用于 draft/add thumb_media_id）
    ⚠️ 必须用 type=image，不是 type=thumb！"""
    # resize 到 300×300 + JPEG 压缩（确保 <64KB）
    img = Image.open(image_path).resize((300, 300), Image.LANCZOS)
    tmp = "/tmp/thumb_upload.jpg"
    img.convert("RGB").save(tmp, "JPEG", quality=85)
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    boundary = "----PythonFormBoundary7MA4YWxkTrZu0gW"
    with open(tmp, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["media_id"]

# 示例
mmbiz_url = upload_image_for_article(token, '/tmp/project_screenshot.png')
thumb_media_id = upload_thumb_for_draft(token, '/tmp/cover.png')
```

### Step 3: 记录插入位置

用简单注释记录，不要凭记忆：

```
mmbiz_url  →  section 二、项目介绍 banner
mmbiz_url  →  section 五、实战场景 demo GIF
```

### Step 4: 写 HTML 时直接嵌入

```html
<h2 style="...">二、xxx 是什么？</h2>
<img src="http://mmbiz.qpic.cn/mmbiz_png/kiuyle4KZHC7JK.../0?from=appmsg" style="width:100%;border-radius:6px;margin:12px 0;" />
<p style="...">项目简介正文...</p>
```

### Step 5: 发布

```bash
python3 scripts/publish_zhili.py "标题" "作者" "摘要" "$(cat /tmp/article.html)" --cover-path /tmp/cover.jpg
```

输出中确认：
```
[INFO] 检测到 N 张正文图片（mmbiz URL）
[OK] 草稿创建成功!
```

---

## Gate 拦截的错误长什么样

如果跳过 Step 1-3，直接写 HTML 然后发布，会看到：

```
[INFO] 检测到 0 张正文图片（mmbiz URL）
[ERROR] 发布被拦截：HTML 正文中未找到任何 mmbiz 图片！
       必须先上传项目截图到 WeChat（media/uploadimg），获取 mmbiz URL 后嵌入 HTML。
```

遇到这个 = 返工 = 浪费时间。

---

## 快速自检（发布前必查）

```bash
# 检查 HTML 中有没有 mmbiz
grep -c 'mmbiz' /tmp/article.html
# 应该 ≥ 1

# 检查有没有未转换的 Markdown bold
grep -n '\*\*' /tmp/article.html
# 应该返回空
```
