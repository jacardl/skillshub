# WeChat API 凭证故障排查

## 核心原则

> **AppSecret 会频繁重置。** 任何时候收到 40125/40013 错误，都意味着凭证已失效，必须向用户要新凭证。不要换接口重试，不要尝试"绕过"。

## 错误码速查

| errcode | 含义 | 立即动作 |
|---------|------|---------|
| 40125 | AppSecret 无效（被重置） | 停止，**向用户要新 AppID + AppSecret** |
| 40013 | AppID 无效（完全错误或已注销） | 停止，向用户要新凭证 |
| 41004 | 缺少 appsecret 参数 | 检查 POST body 的 secret 字段拼写 |
| 40001 | access_token 过期 | 重新获取 stable_token 再重试 |

## 验证脚本（发布前必跑）

```python
import urllib.request, json

def check_wx_credentials(appid, secret):
    req = urllib.request.Request(
        "https://api.weixin.qq.com/cgi-bin/stable_token",
        data=json.dumps({
            "grant_type": "client_credential",
            "appid": appid,
            "secret": secret
        }).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    if "access_token" in result:
        return True, result["access_token"]
    else:
        return False, result

ok, token_or_err = check_wx_credentials("wx38a91c353554588a", "当前AppSecret")
if not ok:
    print(f"凭证无效，需要新凭证: {token_or_err}")
    # 立即向用户要新凭证，不要继续
```

## 时序建议

```
T+0   写作前：验证凭证（ok → 开始写作）
T+30  写作完成：重新验证凭证（如果 T+0 到 T+30 间隔较长）
T+30  凭证 ok：上传封面
T+31  上传正文截图
T+32  重新验证凭证
T+33  创建草稿
T+34  发布
```

**跨 step 的 token 刷新原则**：每执行一次写操作（上传素材/创建草稿）之前，单独调用一次 POST `cgi-bin/stable_token` 获取最新 token。

## session 记录的错误模式

**2026-05-24（本次session）**：用户上次发布 zhilicomments 时 AppSecret 被重置，换了新凭证（appid: wxa7f7f3e03c3d1f1a）。本次写作时用了旧 AppID（wx38a91c353554588a）+ 新 AppSecret，导致 errcode 40013。教训：**新凭证是一组完整的 (appid + appsecret)，不能混用新旧 AppID**。