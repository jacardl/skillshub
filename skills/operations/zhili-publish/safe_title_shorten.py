#!/usr/bin/env python3
"""
微信标题压缩工具（zhili-publish 配套脚本）
=========================================
问题：微信标题有严格的字节限制（errcode 45003），超限直接拒绝创建草稿。
方案：按优先级逐词删除，直到字节数达标。最坏情况保底截断，绝不死循环。

用法：
    python3 references/safe_title_shorten.py "原始标题"

字节计算规则（WeChat GBK编码）：
    中文、全角标点 → 各占 2 字节
    英文、数字、空格、半角标点 → 各占 1 字节

实测阈值（2026-05）：
    纯中文 ≤ 25 字节（约10个汉字）
    含英文+中文混合 ≤ 20 字节（英文单词每个1-2字节，混合后极容易超限）
    安全阈值：统一用 ≤ 20 字节最稳
"""

import sys

def calc_gbk_bytes(title: str) -> int:
    """计算微信标题字节数（GBK编码规则）"""
    total = 0
    for c in title:
        if '\u4e00' <= c <= '\u9fff' or c in '、。，；：！？""''（）【】':
            total += 2
        else:
            total += 1
    return total

def safe_shorten_title(title: str, max_bytes: int = 20) -> str:
    """安全缩短标题，绝不死循环。"""
    if calc_gbk_bytes(title) <= max_bytes:
        return title
    
    removals = [
        "三个", "热门", "开源", "最", "的", "它们",
        "GitHub", "项目", "系统", "框架",
    ]
    
    for pattern in removals:
        working = title
        for _ in range(7):
            if calc_gbk_bytes(working) <= max_bytes:
                return working
            if pattern not in working:
                break
            working = working.replace(pattern, "", 1)
    
    # 保底截断
    chars, byte_count = [], 0
    for c in title:
        char_bytes = 2 if '\u4e00' <= c <= '\u9fff' or c in '、。，；：！？""''（）【】' else 1
        if byte_count + char_bytes > max_bytes:
            break
        chars.append(c)
        byte_count += char_bytes
    return ''.join(chars)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 safe_title_shorten.py \"原始标题\"")
        sys.exit(1)
    
    title = sys.argv[1]
    original_bytes = calc_gbk_bytes(title)
    shortened = safe_shorten_title(title)
    shortened_bytes = calc_gbk_bytes(shortened)
    
    status = "✅" if shortened_bytes <= 20 else "❌"
    print(f"原标题: {title}")
    print(f"  → {original_bytes} 字节 → {'通过' if original_bytes <= 20 else '超限'}")
    print(f"精简后: {shortened}")
    print(f"  → {shortened_bytes} 字节 → {'✅通过' if shortened_bytes <= 20 else '❌仍超限'}")