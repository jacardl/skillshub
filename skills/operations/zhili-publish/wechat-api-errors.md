# WeChat API 错误码与媒体上传参考（2026-05-30 最新）

> ⚠️ 旧版 AppSecret 已失效（errcode 40125），当前凭证在 `~/.hermes/keys/wx_appsecret.txt`

## 常见错误码速查

| errcode | errmsg | 含义 | 处理方式 |
|---------|--------|------|----------|
| - | （无 errcode 字段） | `draft/add` 成功 | 响应含 `media_id` 字段即成功 |
| 0 | ok | 其他 API 成功 | - |
| 40001 | invalid credential | access_token 无效或已过期 | 重新获取 token |
| 40125 | invalid appsecret | AppSecret 无效 | 不能重试，需用户提供新凭证 |
| 40007 | invalid media_id | thumb_media_id 无效 | **必须用 type=image 上传封面（type=thumb 已废止，2026-05-30 实测报 40007）** |
| 44004 | size limit | 多媒体文件超限 | 检查封面图大小 |
| 40013 | invalid appid | AppID 无效 | 检查 AppID 是否正确 |
| 41002 | appid missing | 缺少 appid 参数 | 检查请求参数（可能是 token 获取方式错误） |
| 41005 | media data missing | 上传文件为空或格式错误 | 用 curl -F 替代 urllib.request 构造 multipart |
| 42001 | access_token expired | token 过期 | 重新获取 |
| 45003 | title size out of limit | 标题字节超限 | 缩短标题：纯中文≤25字节，含英文+中文混合≤16字符 |
| 45004 | digest size out of limit | digest 字节超限 | 缩短摘要，≤18字符 |
| 45110 | author field invalid | author 字段含非法字符 | 固定填 `刘生` |
| 44003 | empty news data | payload 结构不完整 | 检查 `articles`（小写）、`thumb_media_id` 是否存在 |
| 48001 | api unauthorized | freepublish 权限不足 | 草稿已创建，手动在 mp.weixin.qq.com 发布 |

## Token 获取（必须用 stable_token POST）

```bash
curl -s -X POST \
  "https://api.weixin.qq.com/cgi-bin/stable_token" \
  -H "Content-Type: application/json" \
  -d '{"appid": "wx38a91c353554588a", "secret": "'$(cat ~/.hermes/keys/wx_appsecret.txt)'", "grant_type": "client_credential"}'
```

成功响应：`{"access_token": "104_xxx", "expires_in": 7200}`

## 封面图上传（2026-05-30 实测唯一可行路径）

**必须用 `type=image` + `curl -F`**，urllib.request 构造 multipart 报 41005。

```bash
ACCESS_TOKEN=$(...)
curl -s -X POST \
  "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${ACCESS_TOKEN}&type=image" \
  -F "media=@/tmp/cover.jpg;type=image/jpeg;filename=cover.jpg"
```

返回的 `media_id` 直接作为 `thumb_media_id` 传入 `draft/add`。