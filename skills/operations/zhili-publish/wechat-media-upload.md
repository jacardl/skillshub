# WeChat 素材上传接口对照（2026-05-30 最新实测）

## 两条上传路线

| 路线 | API | type 参数 | 用途 | media_id 性质 | 能否用于草稿封面 |
|------|-----|-----------|------|--------------|----------------|
| 临时素材 | `media/upload` | thumb / image | 临时/测试 | 临时，有效期短 | ❌ 会报 40007 |
| 永久素材 | `material/add_material` | thumb | 封面图 | 永久 | ❌ 草稿封面报 40007（**2026-05-30 实测已废止，必须用 type=image**） |
| 永久素材 | `material/add_material` | image | 封面图 | 永久 | ✅ 草稿封面必须用 type=image |

## 草稿封面正确流程

```
① 获取 stable_token（POST /cgi-bin/stable_token）
② 用 material/add_material + type=image 上传封面（⚠️ 不是 type=thumb！）
③ 取返回的 media_id 填入 draft/add 的 thumb_media_id
④ 用 material/add_material + type=image 上传正文图
⑤ 取返回的 url 直接嵌入 HTML 的 <img src="...">
⑥ 创建草稿
```

## 封面图上传（2026-05-30 实测）

⚠️ urllib.request 构造 multipart/form-data 报 41005（media data missing），**必须用 curl -F 表单上传**：

```bash
ACCESS_TOKEN=$(...)
curl -s -X POST \
  "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${ACCESS_TOKEN}&type=image" \
  -F "media=@/tmp/cover.jpg;type=image/jpeg;filename=cover.jpg"
```

成功返回：
```json
{
  "media_id": "kiuyle4KZHC7JKxpTQssM...",
  "url": "http://mmbiz.qpic.cn/mmbiz_jpg/...",
  "item": []
}
```

- `thumb_media_id` → 取 `media_id` 字段
- 正文 `<img src="...">` → 取 `url` 字段（mmbiz URL）

## 错误特征

- `material/add_material` + `type=thumb` → **会报 40007**，草稿封面不能用 thumb 类型
- `material/add_material` + `type=image` + urllib.request → **报 41005**，必须用 curl -F
- `material/add_material` + `type=image` + curl -F → **成功**（2026-05-30 实测）