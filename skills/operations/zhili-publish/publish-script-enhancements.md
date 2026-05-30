# publish_zhili.py 脚本增强记录（2026-05-30）

## 文件路径支持增强

**修改文件**：`/root/.hermes/skills/openclaw-imports/zhiligithub/scripts/publish_zhili.py`

**修改位置**：main() 函数中，`content = args.content or ""` 之后新增：

```python
content = args.content or ""
if content and os.path.exists(content):
    with open(content, 'r', encoding='utf-8') as f:
        content = f.read()
```

**效果**：传入 HTML 文件路径而非文件内容时，脚本自动读取文件内容。支持：
```bash
python publish_zhili.py "标题" "作者" "摘要" /tmp/article.html --cover-path /tmp/cover.png
```

**影响**：解决了通过 subprocess 调用时无法通过 stdin 传 HTML 内容的限制。

---

## ensure_ascii 修复记录（2026-05-30）

**问题**：草稿正文在前端显示 `\uXXXX` 字面量而非中文。

**根因**：`json.dumps(payload, ensure_ascii=False)` 发送原始 UTF-8 字节，WeChat HTML pipeline 错误处理。

**修复**：移除所有 `ensure_ascii=False` 参数，恢复为 `json.dumps(payload)` 默认值。

**修改位置**：
- `/root/.hermes/skills/openclaw-imports/zhiligithub/scripts/publish_zhili.py` 第 443 行、第 564 行
- `/root/.openclaw/skills/zhili-publish/scripts/publish_zhili.py` 第 390 行、第 506 行

**验证**：搜索 `ensure_ascii=False` 结果应为空。

**⚠️ 重要结论**：
- `ensure_ascii=True`（默认）：中文转为 `\uXXXX`，WeChat 前端**正确显示中文**
- `ensure_ascii=False`：中文以 UTF-8 原始字节发送，WeChat 前端**显示 `\uXXXX` 字面量**

结论：**所有 `json.dumps()` 调用都不能带 `ensure_ascii=False` 参数**。

---

## WeChat API token 端点说明

- **stable_token**（POST `cgi-bin/stable_token`）：当前主要获取方式
- **GET token**（GET `cgi-bin/token`）：stable_token 失败时的 fallback
- 两个端点都能获取有效 token，但 stable_token 在素材接口更稳定
- errcode 41004 = `appsecret missing`：通常是请求体格式问题，不是凭证问题
- errcode 40125 = 凭证永久失效，需用户提供新 AppSecret