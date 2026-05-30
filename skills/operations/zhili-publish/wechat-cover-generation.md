# 封面图片生成方案（2026-05 实测）

## 方案对比

| 方案 | 工具 | 中文字体支持 | 适用场景 |
|------|------|------------|---------|
| AI 生成 | `mmx image generate` | ✅ 原生渲染 | 首选方案 |
| PIL 绘图 | Python Pillow + DejaVuSans | ❌ 方块字 | 备用方案（仅英文标题） |

## 方案一：mmx AI 生成（首选，2026-05 实测有效）

```bash
mmx image generate \
  --prompt "A sleek tech cover image for [项目名]. Deep navy blue background (#1B365D). Top area: large bold Chinese text '[中文标题]' in vibrant teal/green color (#00d4aa). Middle: English subtitle '[英文副标题]' in white. Bottom left: hashtags '[标签]' in smaller muted text. Clean, modern, professional tech aesthetic. Text-focused hero image, no people, no clutter." \
  --width 896 \
  --height 512 \
  --out /tmp/cover_ai.jpg \
  --response-format url \
  --quiet
```

**参数约束**：
- `--width` 和 `--height` 必须是 8 的倍数，且在 512-2048 之间
- 900×383 无法满足（900 不是 8 的倍数，384 低于最小值 512）
- 推荐尺寸：896×512 或 1920×1080

**输出**：`/tmp/cover_ai.jpg`（JPEG，~50KB）

**优点**：中文标题由 AI 模型原生渲染，无字体缺失问题
**缺点**：依赖 mmx CLI 工具和网络

## 方案二：PIL 绘图（仅限英文标题）

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (900, 383), "#1B365D")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
draw.text((50, 50), "English Title Only", fill="#00d4aa", font=font)
img.save("/tmp/cover.jpg")
```

**致命问题**：DejaVuSans.ttf 不含 CJK 字形，中文全部渲染为空白方块。

## WeChat 封面上传

封面必须用 `type=thumb` 上传得到 `thumb_media_id`，用于 `draft/add` 的 `thumb_media_id` 字段：

```bash
ACCESS_TOKEN=$(curl -s -X POST "https://api.weixin.qq.com/cgi-bin/stable_token" \
  -H "Content-Type: application/json" \
  -d '{"appid":"wx38a91c353554588a","secret":"07b4dc2d64ddbe6f53707977dbabdbbe"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -s -X POST \
  "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$ACCESS_TOKEN&type=thumb" \
  -F "media=@/tmp/cover_ai.jpg;type=image/jpeg"
```

成功响应：
```json
{"media_id":"kiuyle4KZHC7JKxpTQssMJK1r6G8uWxp1-h9GuIF8lsK...","url":"http://mmbiz.qpic.cn/..."}
```

## 尺寸要求

微信封面图建议 900×383 像素（或 2:1 比例）。mmx 输出的 896×512 可以接受，微信会自动裁剪。

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `width must be multiple of 8` | 宽度 900 不是 8 的倍数 | 改为 896 |
| `height must be between 512 and 2048` | 高度 384 低于最小值 | 改为 512 |
| 中文标题渲染为方块 | PIL 使用 DejaVu 字体 | 改用 mmx image generate |