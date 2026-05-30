#!/usr/bin/env python3
"""
微信草稿箱 Unicode 验证脚本
用法: python3 wechat-unicode-verify.py <media_id>

原理: 对比 ensure_ascii=True vs ensure_ascii=False 的 JSON 序列化行为
      ensure_ascii=False → WeChat 前端显示 \uXXXX 字面量（BUG）
      ensure_ascii=True  → WeChat 前端正常显示中文（正确）
"""
import sys
import json
import subprocess
import urllib.request
import ssl

APPID = "wx38a91c353554588a"

def get_token():
    with open("/root/.hermes/keys/wx_appsecret.txt") as f:
        app_secret = f.read().strip()
    req = urllib.request.Request(
        "https://api.weixin.qq.com/cgi-bin/stable_token",
        data=json.dumps({"grant_type": "client_credential", "appid": APPID, "secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    if "access_token" not in result:
        raise Exception(f"Token 获取失败: {result}")
    return result["access_token"]

def get_draft_content(token, media_id):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}",
        data=json.dumps({"media_id": media_id}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read())

def check_unicode_bug(content_raw):
    """
    检查 content 字段是否含 \uXXXX 字面量（ensure_ascii=False 的特征）
    返回 True = 有bug（\uXXXX字面量），False = 正常
    """
    import re
    # 匹配 \u 后跟4位十六进制数字的转义序列字面量（不是被JSON库编码后的普通字符）
    # 真正的 Unicode 转义（JSON标准编码）应该是形如 "\\u4e2d" 的转义序列
    # WeChat bug 显示的是原始字面量 \u4e2d（无反斜杠转义）
    literal_pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
    matches = literal_pattern.findall(content_raw)
    return len(matches) > 0

def main():
    if len(sys.argv) < 2:
        print("用法: python3 wechat-unicode-verify.py <media_id>")
        sys.exit(1)

    media_id = sys.argv[1]
    token = get_token()

    draft = get_draft_content(token, media_id)
    items = draft.get("item", [])
    if not items:
        print("未找到草稿")
        sys.exit(1)

    news_item = items[0].get("content", {}).get("news_item", [{}])[0]
    title = news_item.get("title", "")
    content = news_item.get("content", "")

    print(f"标题: {title}")
    print(f"正文长度: {len(content)} 字符")

    # 检查正文中的 Unicode 字面量
    has_bug = check_unicode_bug(content)

    # 额外检查：对比序列化差异
    test_payload = {"title": "测试", "content": "<p>中文</p>"}
    serialized_true = json.dumps(test_payload)
    serialized_false = json.dumps(test_payload, ensure_ascii=False)

    print("\n--- 序列化对比 ---")
    print(f"ensure_ascii=True:  {serialized_true}")
    print(f"ensure_ascii=False: {serialized_false}")

    if has_bug:
        print("\n❌ 检测到 \\uXXXX 字面量，ensure_ascii=False 导致的 BUG 仍存在")
        print("建议: 检查 publish_zhili.py 中所有 json.dumps() 调用，改用 json.dumps(payload)（默认 ensure_ascii=True）")
        sys.exit(1)
    else:
        print("\n✅ 未检测到 \\uXXXX 字面量，中文显示正常")
        sys.exit(0)

if __name__ == "__main__":
    main()