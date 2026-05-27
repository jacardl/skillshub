# skillshub

佳哥的 Hermes Agent 技能库中央索引。

## 安装技能

从本仓库安装指定技能：

```bash
npx skills add jacardl/skillshub --path skills/<category>/<skill-name>
```

示例（安装 aihot）：

```bash
npx skills add jacardl/skillshub --path skills/operations/aihot
```

从其他仓库安装：

```bash
npx skills add <user>/<repo>
```

## 技能分类

### 运营（operations）
| 技能 | 说明 |
|------|------|
| aihot | AI 热点资讯查询 |
| ad-creative | 广告文案生成 |
| daily-news-report | 每日早间新闻推送 |
| github-daily-trending | GitHub 黑马发现引擎 |
| xurl | X/Twitter 操作 |
| yuanbao | 元宝群组管理 |
| scrapling | 自适应网页抓取 |

### 产品（product）
| 技能 | 说明 |
|------|------|
| hv-analysis | 横纵分析法深度研究 |
| arxiv | 学术论文搜索 |
| polymarket | 预测市场查询 |
| llm-wiki | LLM 知识库 |
| blogwatcher | 博客订阅监控 |
| claude-design | 设计单页 HTML |
| sketch | HTML 原型设计 |

### 助理（productivity）
| 技能 | 说明 |
|------|------|
| notion | Notion API |
| obsidian | Obsidian 笔记 |
| himalaya | 邮件终端客户端 |
| feishu-file-transfer | 飞书大文件传输 |
| linear | Linear 项目管理 |
| maps | 地理编码/路径规划 |
| pdf | PDF 处理 |
| pptx | PPTX 编辑 |

### 开发（software-development）
| 技能 | 说明 |
|------|------|
| claude-code | Claude Code 委托编码 |
| codex | OpenAI Codex 委托 |
| opencode | OpenCode 委托 |
| github-pr-workflow | PR 全流程 |
| github-code-review | 代码审查 |
| github-issues | Issue 管理 |
| python-debugpy | Python 远程调试 |
| node-inspect-debugger | Node.js 调试 |
| systematic-debugging | 系统调试方法论 |
| test-driven-development | TDD 开发流程 |
| webhook-subscriptions | Webhook 事件驱动 |
| skill-creator | 技能创建工具 |
| skill-maintenance | 技能库维护流程 |

### 研究（research）
| 技能 | 说明 |
|------|------|
| evaluating-llms-harness | LLM 基准测试 |
| weights-and-biases | 实验跟踪 |
| jupyter-live-kernel | 实时 Jupyter |
| dspy | DSPy 声明式编程 |
| scrapling | 网页抓取 |

### 创意（creative）
| 技能 | 说明 |
|------|------|
| ascii-art | ASCII 艺术生成 |
| p5js | p5.js 创意编程 |
| pixel-art | 像素艺术 |
| manim-video | 数学动画视频 |
| baoyu-comic | 知识漫画 |
| baoyu-infographic | 信息图设计 |
| popular-web-designs | 54 种设计系统参考 |
| brand-guidelines | Anthropic 品牌规范 |
| canvas-design | 设计 PNG/PDF 画布 |
| excalidraw | 手绘风格架构图 |
| humanizer | AI 文本人性化 |

### AI/模型（ai-model）
| 技能 | 说明 |
|------|------|
| llama-cpp | 本地 GGUF 推理 |
| serving-llms-vllm | vLLM 高吞吐服务 |
| huggingface-hub | HF 模型管理 |
| obliteratus | LLM 拒绝率消除 |
| claude-api | Claude API 封装 |
| native-mcp | MCP 客户端配置 |
| 9router | 9Router 网关 |

## 维护

技能库按7个岗位分类，详情见 [skill-maintenance](skills/software-development/skill-maintenance/)。
