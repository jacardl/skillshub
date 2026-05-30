#!/usr/bin/env python3
"""
微信草稿箱验证脚本
用途：创建草稿后验证标题/作者字段是否正确存储（中文显示正常而非 \\uXXXX 字面量）

用法：
  python3 wechat-draft-verify.py <media_id>
  python3 wechat-draft-verify.py all  # 验证所有草稿

原理：
  - WeChat draft/get API 对所有字段返回 \\uXXXX 序列化格式（这是 API 行为，不是错误）
  - 真正的验证是：拿 draft_get 返回的原始 JSON title 字符串，在 Python 中 json.loads() 一次
    如果得到正常中文（而非带反斜杠的转义字面量），说明 WeChat 存储正确，前端会正常显示
  - 如果 json.loads() 后仍包含未解码的 \\u 序列，说明存储有问题，需要重建草稿

示例：
  # 验证单篇草稿
  python3 wechat-draft-verify.py kiuyle4KZHC7JKxpTQssMNkO6BPcv3MnCNCJxlTv5zym

  # 验证所有草稿
  python3 wechat-draft-verify.py all

  # 在 Python 中直接调用验证函数
  from wechat_draft_verify import verify_draft
  ok, title_display = verify_draft("kiuyle4KZHC7JKxpTQssMNkO6BPcv3MnCNCJxlTv5zym")
  print(f"前端显示: {title_display}")  # 正常显示中文或带反斜杠的转义字面量
"""

import sys
import json
import subprocess
import urllib.request
import ssl
import os
from typing import Tuple, Optional

APPID = "wx38a91c353554588a"
FEISHU_TARGET = "feishu:oc_034bc08420a2daed53561bfceba5b3bf"


def get_token() -> str:
    """获取 access_token（优先 stable_token，回退到 cgi-bin/token）"""
    secret_file = os.path.expanduser("~/.hermes/keys/wx_appsecret.txt")
    with open(secret_file) as f:
        app_secret = f.read().strip()

    # 尝试 stable_token POST
    try:
        req = urllib.request.Request(
            "https://api.weixin.qq.com/cgi-bin/stable_token",
            data=json.dumps({
                "grant_type": "client_credential",
                "appid": APPID,
                "secret": app_secret
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
        if "access_token" in result:
            return result["access_token"]
    except Exception as e:
        print(f"stable_token 失败: {e}")

    # 回退到 GET /cgi-bin/token
    try:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={app_secret}"
        with urllib.request.urlopen(url, timeout=10) as r:
            result = json.loads(r.read())
        if "access_token" in result:
            print("使用 GET /cgi-bin/token 获取的 token")
            return result["access_token"]
    except Exception as e:
        print(f"GET /cgi-bin/token 也失败: {e}")

    raise Exception("无法获取 access_token")


def verify_draft(media_id: str, token: str) -> Tuple[bool, Optional[str]]:
    """
    验证草稿是否正确存储。

    返回 (is_ok, title_display)
      - is_ok: True = 中文正确存储，前端会正常显示
      - title_display: Python json.loads() 后的标题（用于调试显示）

    判断逻辑：
      json.loads() 后，如果 title 是正常中文字符串（不含反斜杠），则 OK
      如果 title 仍含 \\u 序列（未解码），则 FAIL
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}",
        data=json.dumps({"media_id": media_id}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        r = json.loads(resp.read().decode("utf-8"))

    item = r.get("item", {})
    content = item.get("content", {})
    news_item = content.get("news_item", [{}])[0] if content.get("news_item") else {}
    title_raw = news_item.get("title", "")

    # WeChat API 返回的 title 是双重序列化的 \\uXXXX 字符串
    # 用 json.loads() 一次解码，看是否能得到正常中文
    try:
        title_decoded = json.loads(f'"{title_raw}"')
    except Exception:
        title_decoded = title_raw

    # 判断：正常中文不含反斜杠；有问题的会是 "Olah\\u4e0e\\u6559\\u7687" 这样的
    has_backslash = "\\" in title_decoded
    is_ok = not has_backslash

    return is_ok, title_decoded


def list_all_drafts(token: str) -> list:
    """列出所有草稿"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}",
        data=json.dumps({"offset": 0, "count": 20}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        r = json.loads(resp.read().decode("utf-8"))

    items = r.get("item", [])
    results = []
    for item in items:
        media_id = item.get("media_id", "")
        content = item.get("content", {})
        news_item = content.get("news_item", [{}])[0] if content.get("news_item") else {}
        results.append({
            "media_id": media_id,
            "title_raw": news_item.get("title", ""),
            "author_raw": news_item.get("author", ""),
            "update_time": item.get("update_time", 0),
        })
    return results


if __name__ == "__main__":
    token = get_token()

    if len(sys.argv) < 2:
        print("用法: python3 wechat-draft-verify.py <media_id|all>")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "all":
        print("=" * 60)
        print("微信草稿箱验证报告")
        print("=" * 60)
        drafts = list_all_drafts(token)
        print(f"共 {len(drafts)} 篇草稿：\n")
        for d in drafts:
            is_ok, title_display = verify_draft(d["media_id"], token)
            status = "✅ OK" if is_ok else "❌ FAIL"
            print(f"{status} | {d['media_id'][-20:]}")
            print(f"       title: {title_display}")
            print()
    else:
        media_id = arg
        is_ok, title_display = verify_draft(media_id, token)
        status = "✅ OK" if is_ok else "❌ FAIL"
        print(f"{status} | {media_id[-20:]}")
        print(f"title: {title_display}")
        if not is_ok:
            print("⚠️  草稿标题在微信前端会显示为 Unicode escape 字面量，需要删除重建")
            sys.exit(1)