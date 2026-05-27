# skillshub

佳哥的 Hermes Agent 技能库中央索引。

## 安装技能

从本仓库安装指定技能（仓库目录下 `skills/` 子目录中的技能可直接安装）：

```bash
npx skills add jacardl/skillshub --path skills/<category>/<skill-name>
```

示例（安装 aihot）：

```bash
npx skills add jacardl/skillshub --path skills/operations/aihot
```

> 提示：`--path` 参数填写仓库中技能对应的子目录路径，见下方分类表。

## 可直接安装的技能

以下技能已推送至本仓库，可直接用上述命令安装：

| 技能 | 路径 | 说明 |
|------|------|------|
| aihot | `skills/operations/aihot` | AI 热点资讯查询 |
| daily-news-report | `skills/operations/daily-news-report` | 每日早间新闻推送 |
| github-daily-trending | `skills/operations/github-daily-trending` | GitHub 黑马发现引擎 |
| hv-analysis | `skills/product/hv-analysis` | 横纵分析法深度研究 |
| khazix-writer | `skills/operations/khazix-writer` | 公众号长文写作风格 |
| neat-freak | `skills/operations/neat-freak` | 会话知识清理 |
| obsidian | `skills/productivity/obsidian` | Obsidian 笔记 |
| scrapling | `skills/operations/scrapling` | 自适应网页抓取 |
| 9router | `skills/operations/9router` | 本地/远程 AI 网关 |
| skill-maintenance | `skills/software-development/skill-maintenance` | 技能库维护流程 |

## 全量技能分类

以下为本地全部技能索引，部分技能仍在本地维护，陆续推送中。

### 运营（operations）
`aihot` / `daily-news-report` / `github-daily-trending` / `xurl` / `yuanbao` / `scrapling` / `khazix-writer` / `neat-freak` / `9router` / `ad-creative` / `creative-ops-copilot` / `dogfood` / `creative-thought-partner`

### 产品（product）
`hv-analysis` / `arxiv` / `polymarket` / `llm-wiki` / `blogwatcher` / `claude-design` / `sketch` / `excalidraw` / `ideation`

### 助理（productivity）
`notion` / `obsidian` / `himalaya` / `feishu-file-transfer` / `linear` / `maps` / `pdf` / `pptx` / `powerpoint` / `apple-notes` / `apple-reminders` / `findmy` / `imessage` / `macos-computer-use`

### 开发（software-development）
`claude-code` / `codex` / `opencode` / `hermes-agent` / `github-pr-workflow` / `github-code-review` / `github-issues` / `github-repo-management` / `python-debugpy` / `node-inspect-debugger` / `systematic-debugging` / `test-driven-development` / `webhook-subscriptions` / `skill-creator` / `skill-maintenance` / `frontend-design` / `subagent-driven-development` / `native-mcp`

### 研究（research）
`evaluating-llms-harness` / `weights-and-biases` / `jupyter-live-kernel` / `dspy` / `scrapling`

### 创意（creative）
`ascii-art` / `p5js` / `pixel-art` / `manim-video` / `baoyu-comic` / `baoyu-infographic` / `popular-web-designs` / `brand-guidelines` / `canvas-design` / `excalidraw` / `humanizer` / `ideation` / `sketch` / `architecture-diagram`

### AI/模型（ai-model）
`llama-cpp` / `serving-llms-vllm` / `huggingface-hub` / `obliteratus` / `claude-api` / `native-mcp` / `9router` / `scrapling` / `godmode`

## 维护

技能库按7个岗位分类，详情见 [skill-maintenance](skills/software-development/skill-maintenance/)。
