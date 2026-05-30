# 封面图上传与 type 参数（2026-05-30 实测）

## 结论

**草稿封面上传必须用 `type=image`**，`type=thumb` 的旧版记录（2026-05-28 早期版本）已废弃。

验证结果（2026-05-30）：
- `type=image` + `material/add_material` → 返回 `media_id` → `draft/add` 成功 ✅
- `type=thumb` + `material/add_material` → 返回 `media_id` → `draft/add` 报 `40007 invalid media_id` ❌

## 正确流程

```python
import urllib.request, json, ssl, os

APPID = 'wx38a91c353554588a'
with open(os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")) as f:
    app_secret = f.read().strip()

# 1. 获取 token（stable_token POST）
req = urllib.request.Request(
    "https://api.weixin.qq.com/cgi-bin/stable_token",
    data=json.dumps({"grant_type":"client_credential","appid":APPID,"secret":app_secret}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    ACCESS_TOKEN = json.loads(r.read())["access_token"]

# 2. 上传封面（type=image，不是 type=thumb）
boundary = '----PythonFormBoundary123456'
with open('/tmp/cover.jpg', 'rb') as f:
    img_data = f.read()
body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
    f'Content-Type: image/jpeg\r\n\r\n'
).encode('utf-8') + img_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={ACCESS_TOKEN}&type=image'
req = urllib.request.Request(url, data=body, method='POST')
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
ctx = ssl.create_default_context()
ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
    result = json.loads(resp.read())
    media_id = result['media_id']  # 直接作为 thumb_media_id

# 3. 创建草稿（ensure_ascii=True）
payload = {
    "articles": [{
        "thumb_media_id": media_id,
        "author": "刘生",
        "title": "标题",
        "content": html_content,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
        "original": 1,
    }]
}
resp = urllib.request.urlopen(
    f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}",
    data=json.dumps(payload).encode('utf-8'),  # ensure_ascii=True by default
    method='POST'
)
```

## 与旧版冲突说明

- `social-media/zhilicomments/references/wechat-pitfalls.md`（旧版）记录 `type=thumb` 可用 → **已废止**
- `openclaw-imports/zhili-publish/references/wechat-api-errors.md`（旧版）记录 `type=thumb` → **已废止**
- 本文件为 2026-05-30 最新实测，**必须用 `type=image`**