# WeChat API 关键踩坑记录

> 来源：zhilicomments 技能多次实操经验总结
> ⚠️ 2026-05-30 综合更新：基于 zhili-publish 统一结论修正

## access_token 获取（2026-05-30 确认正确方式）

✅ **必须用 `POST /cgi-bin/stable_token`**，不能用 GET `/cgi-bin/token`（后者返回的 token 在素材接口报 40001）。

```python
import urllib.request, json, os

APPID = 'wx38a91c353554588a'
with open(os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")) as f:
    app_secret = f.read().strip()

req = urllib.request.Request(
    "https://api.weixin.qq.com/cgi-bin/stable_token",
    data=json.dumps({"grant_type": "client_credential", "appid": APPID, "secret": app_secret}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    access_token = json.loads(r.read())["access_token"]
```

## media_id 类型决定用途（必须分清）

⚠️ **2026-05-30 修正**：封面图必须用 `type=image` 上传。

| 上传时 type= | 适用于 | 不适用于 |
|-------------|--------|---------|
| `type=image` | `draft/add` 的 `thumb_media_id` ✅ | - |
| `type=image` | `material/add_material`（永久素材） | - |
| `type=thumb` | ❌ 报 40007 invalid media_id | draft/add |

**结论**：封面图必须用 `type=image` 上传，返回的 `media_id` 用于草稿创建。`type=thumb` 会报 40007。

## urllib.request 上传优于 subprocess curl

WeChat 的 material/upload 接口对 curl subprocess 调用有静默失败问题（curl 返回空但 API 正常），建议始终用 urllib.request 构造 multipart/form-data：

```python
import urllib.request, json, ssl

boundary = '----PythonFormBoundary123456'
with open('/tmp/cover.png', 'rb') as f:
    img_data = f.read()
body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="media"; filename="cover.png"\r\n'
    f'Content-Type: image/png\r\n\r\n'
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

## 内容源可访问性（2026-05-20 实测）

| 来源 | 状态 | 备选方案 |
|------|------|----------|
| FlowUs（flowus.cn） | ❌ 服务器环境完全无法访问（网络超时） | 请用户复制粘贴全文，或截图发来 |
| 微信文章 | ❌ 滑块验证码墙，无法自动化 | 请用户复制粘贴全文，或截图发来 |
| Google Developers Blog | ❌ 访问超时（网络策略） | 请用户提供原文内容 |
| 普通网页 | ⚠️ 视网站反爬策略 | 优先用户复制粘贴，节省时间 |

**推荐获取优先级**：用户复制粘贴 > mmx vision 截图分析 > 自行搜索补充背景 > 尝试网页抓取

## 草稿创建前图片URL验证

如果 HTML 中包含配图（cover.png / 内嵌图片），必须在创建草稿前验证所有 `src="http://mmbiz.qpic.cn/` 指向的是本次实际上传的 mmbiz URL，而非残留的旧图。旧图会报 `40007 invalid media_id` 或显示异常图片。

## 中文乱码根因（2026-05-30 最终确认）

⚠️ **草稿创建时必须用 `ensure_ascii=False`**：

```python
# ✅ 正确
body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
req.add_header('Content-Type', 'application/json')  # 不带 charset=utf-8

# ❌ 错误：ensure_ascii=True 默认会将中文转为 \uXXXX，微信显示字面量
body = json.dumps(payload).encode('utf-8')  # ensure_ascii=True by default
```

**判断标准**：微信公众平台草稿箱前端显示正常中文 = 正确；显示 `\uXXXX` 字面量 = 错误，需重建草稿。