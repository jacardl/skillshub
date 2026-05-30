# FlowUs 数据库记录内容提取

## 背景

FlowUs MCP 返回的页面有两种类型：

1. **文档页面** (`page_type: "page"`, `parent.type: "workspace"`) — 内容在 `content[]` block 数组中
2. **数据库记录** (`parent.type: "database_id"`) — `content[]` 包含 JSON 字符串，真正的内容 URL 在 `properties` 中

当 FlowUs 作为「内容收集库」使用时（例如收集公众号文章链接），几乎所有记录都是数据库记录类型。

## 识别数据库记录

```python
page = get_page_result
parent_type = page.get('parent', {}).get('type')
# parent_type == 'database_id' → 数据库记录
# parent_type == 'workspace'   → 普通文档页面
```

## 提取存储的文章 URL

数据库记录的 `properties` 中常有以下字段存储原始文章链接：

```python
properties = page.get('properties', {})

# 常见字段名
url_field = properties.get('网址链接', {}) or properties.get('链接', {}) or properties.get('url', {})
article_url = url_field.get('url', '') if isinstance(url_field, dict) else ''

# 如果 content[] 包含 JSON 字符串（数据库记录常见格式）
content = page.get('content', [])
if content and isinstance(content[0], dict) and content[0].get('type') == 'text':
    try:
        inner = json.loads(content[0]['text'])
        article_url = inner.get('properties', {}).get('网址链接', {}).get('url', '')
    except:
        pass
```

## FlowUs 数据库记录字段示例

```json
{
  "object": "page",
  "id": "3f231620-a604-43ac-adb1-8c9f041f4379",
  "parent": {"type": "database_id", "database_id": "906a1472-befe-4502-8075-26d5a6e0db99"},
  "properties": {
    "标题": {"id": "title", "type": "title", "title": []},
    "网址链接": {
      "id": "33bb4b09-302b-4990-ad84-0682ead19f3f",
      "type": "url",
      "url": "https://mp.weixin.qq.com/s?__biz=..."
    },
    "标签": {
      "id": "3d2c93f0-d0b2-44ff-a3a8-f1a0eaf87b1f",
      "type": "multi_select",
      "multi_select": [{"name": "微信", "color": "green"}, ...]
    },
    "作者": {
      "id": "d0d0ef39-61d6-4a64-9d22-b626beb596d3",
      "type": "select",
      "select": {"name": "数字生命卡兹克", "color": "green"}
    }
  }
}
```

## 典型工作流

```
用户提供 FlowUs 分享链接
    ↓
API-getPage 获取页面元数据
    ↓
判断 parent.type == 'database_id' ?
    ↓ 是 → 从 properties['网址链接']['url'] 提取原始文章链接
    ↓ 否 → 从 content[] block 数组提取正文内容
    ↓
处理原始文章链接（可能是微信文章，需要用户复制粘贴内容）
```

## 已知局限

- **微信文章 URL**：从 FlowUs 提取的微信 `mp.weixin.qq.com` 链接通常需要登录态 cookie 才能访问，直接 curl 会返回"未知错误"。**不要浪费时间尝试**，请用户复制粘贴文章正文。
- **FlowUs MCP Session**：HTTP session 有时效（约几分钟无活动后过期），过期后返回 502 Bad Gateway。需要重新 initialize 获取新 session ID。
