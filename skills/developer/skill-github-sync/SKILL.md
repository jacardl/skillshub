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

## 推送命令示例

推送到 jacardl/skillshub（公开仓库）：

```python
import base64, os, requests

token_path = os.path.expanduser("~/.hermes/keys/github_token.txt")
with open(token_path) as f:
    token = f.read().strip()

headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
OWNER = "jacardl"
REPO = "skillshub"
BRANCH = "main"

def push_file(owner, repo, file_path, content, branch, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    get_resp = requests.get(url, headers=headers)
    sha = get_resp.json().get("sha") if get_resp.status_code == 200 else None
    payload = {
        "message": f"Add {file_path}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch
    }
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, headers=headers, json=payload)
    return resp.status_code, resp.json()

def scan_skill_dir(base_path, skill_name):
    files = []
    skill_path = os.path.join(base_path, skill_name)
    for root, dirs, filenames in os.walk(skill_path):
        for fname in filenames:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, base_path)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            files.append({"path": rel_path, "content": content})
    return files

# 按分类整理推送
skills_by_category = {
    "operations": ["aihot", "daily-news-report", "github-daily-trending"],
    "product": ["hv-analysis"],
    "ai-model": ["claude-api"],
}

for category, skill_names in skills_by_category.items():
    for skill_name in skill_names:
        skill_path = f"skills/{category}/{skill_name}"
        files = scan_skill_dir(os.path.expanduser("~/.hermes/skills"), skill_name)
        for f in files:
            dest = f"{skill_path}/{os.path.basename(f['path'])}"
            status, data = push_file(OWNER, REPO, dest, f["content"], BRANCH, token)
            print(f"{status} {dest}")
```

## 注意事项

1. Token 权限：确认 PAT 有 `repo` 写入权限，只读 token 返回 403
2. 防冲突：每次 PUT 前先 GET 获取 sha，否则 409 Conflict
3. 目录结构：推送到 `skills/{岗位}/{skill名}/` 层级，README 在根目录
4. 私有仓库：zhiligithub/zhilicomments/zhili-publish/daily-news-report 用同名私有仓库
5. 验证结果：检查 `https://api.github.com/repos/{owner}/{repo}/contents/{path}`

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
