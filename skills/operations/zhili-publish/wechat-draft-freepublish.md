# WeChat 草稿箱 API 权限与实测要点（2026-05 实测）

## freepublish/submit 权限边界

微信草稿箱 API 分两个阶段：

| 阶段 | API | 权限要求 | 订阅号可用 |
|------|-----|---------|-----------|
| 创建草稿 | `draft/add` | 已认证订阅号/服务号 | ✅ |
| API 发布 | `freepublish/submit` | 需开通高级接口权限 | ❌ 返回 48001 |

**当 freepublish 返回 48001 时**：
1. 草稿已成功创建（`draft/add` 在调用 `freepublish` 之前已完成）
2. 不要重试发布 API，直接汇报用户手动发布
3. 手动路径：mp.weixin.qq.com → 草稿箱 → 找到文章 → 编辑 → 发布

## 草稿验证的正确方式

`draft/get` 和 `draft/batchget` 的 `no_content` 参数行为不同：

```python
# ❌ 错误方式：no_content=1 返回空列表（查不到内容）
POST /cgi-bin/draft/get
{"offset":0,"count":5,"no_content":1}
→ {"item":[]}

# ✅ 正确方式：no_content=0 返回完整内容（含 media_id、title、content）
POST /cgi-bin/draft/batchget
{"offset":0,"count":50,"no_content":0}
→ {"item":[{"media_id":"...","content":{"news_item":[{"title":"...","author":"刘生",...}]}}]}

# 查数量用 draft/count
GET /cgi-bin/draft/count?access_token=TOKEN
→ {"total_count": 3}
```

验证顺序：`draft/count` → `draft/batchget`（no_content=0）→ 确认标题存在

## 错误码速查

| errcode | 含义 | 处理 |
|---------|------|------|
| 48001 | freepublish 权限不足 | 草稿已创建，手动发布 |
| 40001 | token 过期 | 重新获取 stable_token |
| 40125 | AppSecret 无效 | 需用户提供新凭证 |
| 40007 | media_id 无效 | 检查 thumb_media_id 是否用 type=thumb 上传 |