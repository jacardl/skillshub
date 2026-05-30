# WeChat Draft API 关键约束（2026-05-26 实测）

## 草稿创建 payload 约束

### 1. `content_source_url` 禁止出现

WeChat 官方文档在 `draft.add` 的 articles 项中列出了 `content_source_url` 字段，**但实测包含该字段（即使是空字符串）会导致 `44003 empty news data`错误**。

**正确做法**：完全不传 `content_source_url` 字段。

```python
# ✅ 正确：完全不写 content_source_url
payload = {
    "articles": [{
        "title": "标题",
        "author": "刘生",
        "thumb_media_id": "MEDIA_ID",
        "content": "<body>...</body>",
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "original": 1,
    }]
}

# ❌ 错误：包含 content_source_url，即使空字符串也会 44003
payload = {
    "articles": [{
        "title": "标题",
        "content_source_url": "",  # 禁止！会导致 44003
        "content": "<body>...</body>",
        ...
    }]
}
```

### 2. `thumb_media_id` 是必填字段

草稿不带 `thumb_media_id` 会报 `40007 invalid media_id`。**即使脚本用 `--skip-cover`，也需要传入一个有效的 media_id**。

获取方式：`POST /cgi-bin/material/add_material?access_token=TOKEN&type=image`（注意：必须是 type=image，type=thumb 返回的 media_id 在 draft/add 时报 invalid media_id）。

### 3. `articles` 必须小写

`Articles`（大写A）会导致 `44003 empty news data`，API 只接受小写 `articles`。

### 4. 成功响应判断

成功时返回：
```json
{"media_id": "xxx", "item": [{"index": 0, "ad_count": 0}]}
```

⚠️ **成功响应不包含 `errcode` 字段**。不能用 `errcode == 0` 判断，必须用 `if "media_id" in response`。

### 5. 中文标题必须用 ensure_ascii=True（默认 JSON 序列化）

`ensure_ascii=False` 发送 UTF-8 原始字节，WeChat 存储/解码有误，前端草稿箱显示 `\uXXXX` 字面量（如 `\uff1a` 而非 `：`）而非正常中文。

**修复方案**：使用 `json.dumps(payload)` 默认参数（`ensure_ascii=True`），中文变为 `\uXXXX` 转义序列，WeChat 能正确解码存入并在前端正常显示。

```python
# ✅ 正确：ensure_ascii=True（默认）
create_resp = subprocess.run(["curl", "-s", "-X", "POST",
    f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(payload)],  # ensure_ascii=True by default
    capture_output=True, text=True)

# ❌ 错误：ensure_ascii=False 会导致前端显示 Unicode escape 字面量
create_resp = subprocess.run(["curl", "-s", "-X", "POST",
    f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(payload, ensure_ascii=False)],
    capture_output=True, text=True)
```

**验证**：`draft/get` API 返回的 title 中若有未解码的 `\uXXXX`（如 `Olah\u4e0e\u6559\u7687`），前端可能显示乱码；应返回正常解码中文。

## 凭证相关

### 6. Token 获取必须用 stable_token

`GET /cgi-bin/token` 返回的 token 在 `material/add_material` 接口报 `40001 invalid access_token`。

必须用：`POST https://api.weixin.qq.com/cgi-bin/stable_token`

### 7. 凭证失效特征

`errcode: 40001` = token 过期，重新获取即可。`errcode: 40125` = AppSecret 永久失效，需要用户提供新凭证。

### 8. 草稿箱接口不需要 author 字段

author 字段是可选的。传 `刘生`（2个中文字）不触发任何错误，留空也可以。但内容中的作者信息位置另有规范（HTML 底部作者：刘生）。

## 错误码速查

| errcode | 含义 | 处理 |
|---------|------|------|
| 44003 | empty news data | 检查：① content_source_url 字段是否出现 ② articles 是否小写 ③ content 是否为空 |
| 40007 | invalid media_id | 必须用 `material/add_material?type=image` 获取 thumb_media_id，`media/upload?type=thumb` 的返回不兼容 |
| 40001 | access_token 无效 | 重新获取 token |
| 40125 | AppSecret 无效 | 用户提供新凭证 |
| 45003 | title size out of limit | 缩短标题，中文全角标点（，！？）各占3字节。建议中文标题 ≤22 字符（或 UTF-8 字节数 ≤22） |
| 45110 | author/digest 超长 | 缩短摘要，控制在 54 字节以内（英文约 54 字符，中文约 18-20 字） |

## 草稿创建成功判断

⚠️ **成功响应不返回 `errcode` 字段！** 不能用 `if resp.json().get("errcode") == 0` 判断，必须用 `if "media_id" in resp.json()`。

成功响应：
```json
{"media_id": "kiuyle4KZHC7JKxpTQssMNkO6BPcv3MnCNCJxlTv5zym...", "item": [{"index": 0, "ad_count": 0}]}
```

失败响应（含 errcode）：
```json
{"errcode": 40007, "errmsg": "invalid media_id hint: [...]"}
```

## 兜底清理（已基本不再需要）

若已用 `ensure_ascii=False` 产生了 `\uXXXX` 字面量，用 regex 单字符替换纠正（不要用 encode/decode 方式，会二次解码乱码）：

```python
content = re.sub(r'\\u([a-fA-F0-9]{4})', lambda m: chr(int(m.group(1), 16)), content)
```