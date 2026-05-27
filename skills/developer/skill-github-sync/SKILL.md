---
name: skill-github-sync
description: 将 Skills 同步到 GitHub 仓库（skillshub 公开仓库 + 私有专属仓库）。当用户说"同步skills到GitHub"、"上传skill到github"、"推送skill到远程"、"更新skillshub仓库"、"维护GitHub上的skill仓库"时使用此技能。包含完整的 GitHub API 推送流程：获取token、整理目录结构、计算文件sha、按层级创建/更新文件、生成README。
---

# Skill GitHub Sync

将本地 Skills 同步到 GitHub 仓库的完整流程。

## 现有分类（必须使用）

| 英文分类 | 中文名 | 说明 |
|---------|--------|------|
| `ai` | AI模型 | knowledge-agent, 9router |
| `assistant` | 助理 | babysit, do, make-plan, mem-search, smart-explore, wiki-* |
| `creative` | 创意 | remotion-best-practices, wowerpoint, brandkit |
| `developer` | 开发 | design-is, version-bump, taste-skill, neat-freak |
| `operations` | 运营 | aihot, baoyu-url-to-markdown, github-daily-trending, scrapling |
| `product` | 产品 | conducting-user-interviews, hv-analysis, llm-wiki, markdown-to-report |

**铁律**：不要新增分类，只在现有分类中添加技能。

## 核心流程

### 第一步：读取 Token

从 `~/.hermes/keys/github_token.txt` 读取 GitHub PAT。

### 第二步：读取仓库目录结构（必须）

**同步前必须先读取仓库现有结构**，确认目标分类存在：

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/jacardl/skillshub/contents/skills" | \
  grep '"name"'
```

### 第三步：映射本地分类到远程分类

本地 `.claude/skills/` 使用中文分类名（如 `运营/`、`产品/`），需映射到英文分类：

| 本地分类 | 远程分类 |
|---------|---------|
| `运营/` | `operations/` |
| `产品/` | `product/` |
| `助理/` | `assistant/` |
| `创意/` | `creative/` |
| `开发/` | `developer/` |
| `AI模型/` | `ai/` |

### 第四步：上传 Skill 文件

遍历 skill 目录下所有文件，使用 GitHub API 上传：
- 先 GET 获取已存在文件的 sha（防冲突）
- 再 PUT 上传（带 sha 则更新，不带则创建）

### 第五步：生成 README（每次必须）

同步完成后，读取仓库所有技能，生成 README.md。

## 推送命令示例（curl）

```bash
TOKEN=$(cat ~/.hermes/keys/github_token.txt)
REPO="jacardl/skillshub"
BASE="/c/Users/jacar/.claude/skills"

# 上传到 operations
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"chore: add SKILL.md","content":"'"$(base64 -w 0 "$BASE/运营/baoyu-url-to-markdown/SKILL.md")"'"}' \
  "https://api.github.com/repos/$REPO/contents/skills/operations/baoyu-url-to-markdown/SKILL.md"

# 上传到 product
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"chore: add SKILL.md","content":"'"$(base64 -w 0 "$BASE/产品/markdown-to-report/SKILL.md")"'"}' \
  "https://api.github.com/repos/$REPO/contents/skills/product/markdown-to-report/SKILL.md"
```

## 注意事项

1. **先读仓库结构**：每次同步前必须 GET `/repos/{owner}/{repo}/contents/skills` 确认分类存在
2. **使用英文分类名**：operations, product, assistant, creative, developer, ai
3. **不要新增分类**：如果仓库没有对应分类，将技能放入最接近的现有分类
4. **生成 README**：同步完成后必须更新 README.md
5. **Token 权限**：确认 PAT 有 `repo` 写入权限

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