---
name: skill-github-sync
description: 将 Skills 同步到 GitHub 仓库（skillshub 公开仓库 + 私有专属仓库）。当用户说"同步skills到GitHub"、"上传skill到github"、"推送skill到远程"、"更新skillshub仓库"、"维护GitHub上的skill仓库"时使用此技能。包含完整的 GitHub API 推送流程：获取token、整理目录结构、计算文件sha、按层级创建/更新文件、生成README。
---

# Skill GitHub Sync

将本地 Skills 同步到 GitHub 仓库的完整流程。

## 核心流程

### 第一步：准备 GitHub PAT

读取 `~/.hermes/keys/github_token.txt`，用 GitHub API 验证写入权限。

### 第二步：扫描 Skill 目录结构

返回 skill 下所有文件的相对路径和内容。

### 第三步：通过 GitHub API 推送（防冲突）

每个文件：先 GET 获取 sha（如果存在），再 PUT content（带 sha 防冲突）。

### 第四步：生成 skillshub README

包含安装命令和7个岗位分类索引。

## 推送流程（每次新增技能）

### 铁律：上传 Skill 目录全部文件

上传时必须遍历 skill 根目录**所有文件和子目录**，不能只传 SKILL.md。需同步的文件类型：

- `SKILL.md` — 技能定义元文件
- `references/` — 参考文档（如 CSS 模板、API 文档）
- `scripts/` — 可执行脚本
- `templates/` — 内容模板
- `assets/` — 静态资源（图片、字体等）

### 完整推送代码

```python
import json, urllib.request, os, base64

TOKEN_FILE = os.path.expanduser("~/.hermes/keys/github_token.txt")
with open(TOKEN_FILE) as f:
    TOKEN = f.read().strip()
OWNER, REPO = "jacardl", "skillshub"
SKILL_BASE = "/root/.hermes/skills"

def api_request(method, path, data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
    body = json.dumps(data).encode() if data else None
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()), r.status

# 遍历 skill 目录下所有文件
skill_dir = f"{SKILL_BASE}/{category}/{skill_name}"
for root, dirs, files in os.walk(skill_dir):
    for file in files:
        local_file = os.path.join(root, file)
        rel_path = os.path.relpath(local_file, SKILL_BASE)  # e.g. "developer/skill-github-sync/references/css.html"
        remote_path = f"skills/{rel_path.replace(os.sep, '/')}"

        with open(local_file, "rb") as f:
            content_bytes = f.read()
        content_b64 = base64.b64encode(content_bytes).decode()

        # 获取已存在的 sha（防冲突）
        sha = None
        try:
            res, st = api_request("GET", remote_path)
            if st == 200:
                sha = res["sha"]
        except:
            pass

        # 写入
        msg = f"chore: add {remote_path}"
        payload = {"message": msg, "content": content_b64}
        if sha:
            payload["sha"] = sha
        res, st = api_request("PUT", remote_path, payload)
        print(f"{'✓' if st in (200,201) else '✗'} {remote_path}: {st}")
```

### 旧路径清理（如分类调整）

```python
old_path = f"skills/{old_category}/{skill_name}/SKILL.md"
try:
    res, st = api_request("GET", old_path)
    if st == 200:
        api_request("DELETE", old_path, {"message": f"chore: remove {old_path}", "sha": res["sha"]})
except:
    pass
```

**陷阱（2026-05-27 发现）**：
- `execute_code` sandbox 每次调用重置作用域，每次都要重新 `import os, json, base64`
- `requests` 库在 sandbox 中行为不稳，统一用 `urllib.request`
- `base64` 不自动导入，每次必须显式 `import base64`
- `while True` + 缩短标题循环会超时，改成 `while len(title) > target` 明确条件

## 注意事项

1. Token 权限：确认 PAT 有 `repo` 写入权限，只读 token 返回 403
2. 防冲突：每次 PUT 前先 GET 获取 sha，否则 409 Conflict
3. 目录结构：推送到 `skills/{岗位}/{skill名}/` 层级，README 在根目录
4. 私有仓库：zhiligithub/zhilicomments/zhili-publish/daily-news-report 用同名私有仓库
5. **更新 README**：添加新技能到对应分类表中，保持 README 与仓库实际内容一致
6. 验证：`GET /repos/jacardl/skillshub/contents/skills/{category}/{skill}/SKILL.md` 确认返回 200

## README 模板

```python
def generate_readme(skills_by_category):
    lines = [
        "# Skillshub",
        "",
        "佳哥私人 Skill 库，按岗位分类。",
        "",
        "## 安装命令",
        "",
        "```bash",
        "npx skills add jacardl/skillshub --path <path>",
        "```",
        "",
        "## 岗位分类索引",
        ""
    ]
    for cat, skills in skills_by_category.items():
        lines.append(f"### {cat}（{len(skills)}个）")
        for s in skills:
            lines.append(f"- [{s}](skills/{cat}/{s}/SKILL.md)")
        lines.append("")
    return "\n".join(lines)
```
