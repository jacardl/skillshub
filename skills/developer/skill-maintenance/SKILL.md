---
name: skill-maintenance
description: 维护技能库整洁，系统性整理、分类、清理重复和低频技能。当用户说「整理技能库」「skills太乱了」「删除重复技能」「技能库查重」「技能分类」「整理skills」时触发。
---

# Skill Maintenance

定期维护技能库，识别重复/低频技能，保持7个岗位分类整洁有序。

## 7个固定岗位分类（2026-05-27 整理）

- **运营**：zhiliGitHub / zhiliComments / zhili-publish / daily-news-report / github-daily-trending / khazix-writer / aihot / ad-creative / xurl / yuanbao / scrapling / creative-ops-copilot / creative-thought-partner / dogfood / gif-search / humanizer / neat-freak / baoyu-comic / baoyu-infographic / architecture-diagram / ideation
- **产品**：hv-analysis / arxiv / polymarket / llm-wiki / research-paper-writing / blogwatcher / claude-design / sketch / excalidraw
- **助理**：himalaya / notion / obsidian / feishu-file-transfer / linear / maps / pdf / pptx / powerpoint / apple-notes / apple-reminders / findmy / imessage / macos-computer-use
- **开发**：claude-code / codex / opencode / hermes-agent / github-pr-workflow / github-code-review / github-issues / github-repo-management / codebase-inspection / python-debugpy / node-inspect-debugger / debugging-hermes-tui-commands / systematic-debugging / test-driven-development / requesting-code-review / spike / webhook-subscriptions / kanban-orchestrator / kanban-worker / writing-plans / plan / 9router / native-mcp / subagent-driven-development / hermes-agent-skill-authoring / godmode / skill-creator / frontend-design
- **研究**：evaluating-llms-harness / weights-and-biases / jupyter-live-kernel / dspy / scrapling
- **创意**：ascii-art / p5js / pixel-art / manim-video / excalidraw / sketch / architecture-diagram / popular-web-designs / design-md / brand-guidelines / canvas-design / humanizer / pretext
- **AI模型**：llama-cpp / serving-llms-vllm / huggingface-hub / obliteratus / claude-api / native-mcp / godmode / 9router / scrapling

**实际统计**：89个 SKILL.md 文件，92个去重技能名

## 维护流程

### 1. 每周检查清单

每次维护按顺序执行：

1. **检测新安装技能**：`npx skills list` 找出新增技能
2. **归类新技能**：对照7个岗位分类，归入现有分类（不新增分类）
3. **查重**：`skills_list` + `skill_view` 两两对比描述，相似度>70%则标记删除
4. **清理空目录**：含 DESCRIPTION.md 但无 SKILL.md 的目录 stub
5. **验证CSS铁律**：检查各技能 references/streambert-reference.html 存在性

### 已删除技能记录（2026-05-27）

- **重复删除**：zhilicomments-publish（与zhiliComments功能完全相同）
- **低频边缘领域**：spotify / youtube-content / heartmula / airtable / google-workspace / teams-meeting-pipeline / comfyui / touchdesigner-mcp / audiocraft-audio-generation / pretext / songsee / songwriting-and-ai-music / minecraft-modpack-server / pokemon-player / openhue
- **空目录清理**：diagramming / gaming / smart-home / gifs / inference-sh / domain（含DESCRIPTION.md但无SKILL.md的stub）
- **功能重复**：ideation（与creative-ideation重复）

### 2. 删除技能标准

满足以下任意条件建议删除（删除前必须提醒用户确认）：
- 与现有技能功能完全重复（描述重叠>70%）
- 长期未使用（边缘领域如音乐/游戏/家居控制）
- 依赖外部服务已失效
- 描述过时且无法修复

### 分类调整规则

- 新技能归入现有7个分类，不新建分类
- apple/* 技能统一归入助理岗位
- 公众号相关技能（zhili*）固定在运营岗位
- anthropics/skills 安装后归入现有分类：brand-guidelines/canvas-design→创意，claude-api→AI模型，frontend-design/skill-creator→开发，pdf/pptx→助理
- ideation 类技能统一删除，保留主要技能

### 4. 删除流程

删除前必须：
1. 列出待删除技能及删除理由
2. 等待用户确认
3. 执行 `skill_manage(action='delete', name='xxx')`
4. 更新分类统计

### 5. 验证步骤

维护完成后输出：
- 当前技能总数（SKILL.md 文件数）
- 各分类技能数量
- 本次新增/删除/调整列表
- 遗留待处理项

## GitHub API 推送权限要求（陷阱）

向 jacardl/skillshub 推送技能文件使用 GitHub REST API（blobs/trees/commits/refs）。**必须使用有写入权限的 Token**：

- **Classic PAT**（推荐）：在 https://github.com/settings/tokens/new 创建，勾选 `repo` scope
- **Fine-grained PAT**：在 https://github.com/settings/tokens 创建，需单独设置：
  - Permissions → Repository access → 选择具体仓库（如 `jacardl/skillshub`）
  - Repository permissions → Contents 设置为 **Read and write**（默认只有 Read）

**验证方法**：创建 blob 时不报 403 即代表有写入权限
```bash
curl -s -X POST -H "Authorization: token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"content":"test","encoding":"utf-8"}' \
  "https://api.github.com/repos/jacardl/skillshub/git/blobs"
# 成功返回 {"sha":"..."}，403 = 无写入权限
```

Token 凭证保存路径：`~/.hermes/keys/github_token.txt`

### GitHub 推送路径规范

所有技能推送到 `jacardl/skillshub` 时，路径格式统一为：

```
skills/{category}/{skill-name}/SKILL.md
```

示例：
```
skills/operations/aihot/SKILL.md
skills/product/hv-analysis/SKILL.md
skills/developer/skill-github-sync/SKILL.md
skills/ai/9router/SKILL.md
```

技能先读取内容 → 推送到新路径 → 删除旧路径文件（如果有）。

推送完成后验证：
```bash
# 列出所有技能路径
curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/jacardl/skillshub/git/trees/main?recursive=1" | \
  python3 -c "import sys,json; [print(f['path']) for f in json.load(sys.stdin)['tree'] if f['path'].endswith('SKILL.md')]"
```

## 快速命令

```bash
# 统计SKILL.md文件数
find ~/.hermes/skills -name "SKILL.md" | wc -l

# 列出所有技能名（去重）
find ~/.hermes/skills -name "SKILL.md" | xargs -I{} dirname {} | xargs -I{} basename {} | sort -u | wc -l

# 清理空目录stub（含DESCRIPTION.md但无SKILL.md）
find ~/.hermes/skills -maxdepth 2 -name "DESCRIPTION.md" | while read f; do dir=$(dirname "$f"); [ ! -f "$dir/SKILL.md" ] && echo "$dir"; done

# 检查重复描述（两两比对）
skills_list | grep -A2 "description"
```

## 注意事项

- 删除技能后需更新分类统计
- API keys/tokens/credentials 一律 [REDACTED]
- 技能库实际文件数可能少于技能名数量（存在软链接/重命名）
- 维护后向用户汇报结果，不要静默完成
- skill-maintenance 自身归入助理岗位（productivity）