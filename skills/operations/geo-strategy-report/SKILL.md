---
name: geo-strategy-report
description: GEO 策略分析报告生成技能 — 基于多维度 CSV 数据（可见度×准确率×人群×关键词×竞品×AI模型）生成完整的 GEO 优化策略报告，包含四象限优先级矩阵、竞品 Buzzword 分析、预算分配和分阶段执行路线图。
tags: [GEO, 策略分析, 品牌分析]
related_skills: [geo-keyword-research, competitor-discovery]
---

# GEO Strategy Report Skill

**version**: 1.2.0
**author**: ou_44aa34f24ae6620744e640c79080944c
**description**: 基于 AI 搜索可见度和准确率数据，生成完整的 GEO 优化策略报告（含售前演示版 / 品牌内部分析版双模式）

---

## When to use

- 用户需要基于 GEO 监控数据生成策略分析报告
- 已有多 Sheet CSV 数据包含：可见度矩阵、准确率矩阵、竞品数据、Buzzword 统计
- 需要输出结论先行、重点在执行计划的完整报告
- **售前演示场景**：向已有 GEO 深度理解的客户现场讲解，侧重竞品格局和策略方向
- **品牌内部分析场景**：给内部团队诊断现状，侧重数据明细和执行细节

---

## Input Data Requirements

输入 CSV 需要包含以下 Sheet：

| Sheet | Content | Required |
|-------|---------|----------|
| Report Summary | 产品信息、导出日期、维度计数 | ✅ Yes |
| Brand Visibility | 品牌总可见度排名 | ✅ Yes |
| Product Buzzwords | 本品 Buzzword 及提及次数 | ✅ Yes |
| Brand Leaderboard | 完整排行榜，包含竞品 Buzzwords | ✅ Yes |
| Visibility - Role x Keyword | 人群 × 关键词 可见度矩阵 | ✅ Yes |
| Accuracy - Role x Keyword | 人群 × 关键词 准确率矩阵 | ✅ Yes |
| Visibility - Role x Competitor | 人群 × 竞品 可见度 | ✅ Yes |
| Visibility - Keyword x Model | 关键词 × AI 模型 可见度 | ✅ Yes |
| Sources - Top Domains | 引用来源域名 Top | ✅ Yes |
| Sources - By Category | 引用来源分类统计 | ✅ Yes |
| Alerts | 系统告警 | Optional |

---

## Two Output Modes: 售前版 vs 内部分析版

### 模式A：售前演示版（Pre-sales）
适用于面对已有 GEO 深度理解客户的现场演示和讲解。
特点：
- **无科普**：跳过 AI 搜索基础知识普及，直接进入品牌/竞品分析
- **竞品全名**：直接提竞品名称和具体Buzzword战场，无需代号
- **话术封装**：每个模块附「现场可直接引用的讲解话术」
- **结论前置**：P0/P1/P2/P3 分级清晰，客户当场能记住优先级
- **无报价内容**：策略报告不含投入产出测算，报价私下单独沟通
- **7-8 模块结构**：核心结论→可见度现状→竞品格局→四象限→核心路径→人群×赛道→AI模型策略→执行路线图

### 模式B：品牌内部分析版（Internal Diagnostic）
适用于给内部团队（SEO/市场/品牌）做现状诊断。
特点：
- **数据明细**：全量表格输出，L1-L5内容分层精细
- **CSV 原始数据引用**：清晰标注数据来源和置信度
- **执行计划详细**：含周度动作、检查点、责任方
- **含告警模块**：Alerts sheet 数据直接呈现
- **9 模块结构**：在一的基础上增加「数据维度说明」「来源域名详细分析」

---

## Output Report Structure

1. **一、核心结论速览** — 结论先行
2. **二、AI 用户问询全链路与 GEO 优化定位** — 决策路径分阶段优先级（内部分析版含，售前版跳过）
3. **三、数据维度说明** — 维度和指标定义（内部分析版含，售前版跳过）
4. **四、人群 × 关键词 优先级矩阵（可见度 × 准确率）** — 四象限详细分析
   - 4.1 优势象限（高可见+高准确）
   - 4.2 优化象限（高可见+低准确）→ 最高优先级
   - 4.3 机会象限（低可见+高准确）→ 高优先级
   - 4.4 盲区象限（低可见+低准确）→ 中长期
5. **五、竞品分析（人群 × 竞品 × Buzzword）**
   - 5.1 人群 × 竞品优势对比
   - 5.2 Buzzword 竞争分析（本品统计 + 竞争策略 + 策略总结）
6. **六、AI 模型优化策略**
   - 6.1 投入策略按平均可见度倾斜
   - 6.2 整体预算分配
7. **七、来源数据洞察** — Top 域名 + 分类 + 策略启示（内部分析版含，售前版简略）
8. **八、分阶段执行路线图** — 紧急止血/增长扩量/竞品拦截/持续维护
9. **附：现场话术** — 售前版专有，可直接引用的讲解话术（内部分析版不含）

---

## Analysis Principles

1. **结论优先**：用户最先看到核心发现，不需要翻到最后
2. **优先级清晰**：P0/P1/P2/P3 明确，用户知道先做什么
3. **Buzzword 竞争策略**：
   - 重叠赛道 → 差异化抢
   - 你有竞品少 → 全力强化抢占
   - 竞品已经占死 → 差异化避战
   - 低频词 → 保持即可
4. **ROI 导向**：先修复已经有曝光但匹配错的（立刻见效），再给高匹配缺曝光的加量，最后抢竞品强势人群
5. **AI 模型倾斜**：按照你在各模型的现有可见度分配预算，基础好的模型 ROI 更高

---

## Case Reference

- **`references/guizhi-presales-case.md`** — 桂格发酵燕麦售前演示版完整案例，含竞品Buzzword矩阵格式、人群×赛道格式、演示话术封装格式、内容分层L1-L5格式、置信度标注规范。本案例是验证本skill输出的参考基准。

---

**输出格式与交付规范**

> ⚠️ **用户明确要求：仅生成 Markdown 格式输出，不渲染 HTML。不调用 html-anything。**

1. 生成报告内容（Markdown 格式）
2. 将 Markdown 文件保存到 `~/final_report/geo-strategy/<product>-geo-strategy-report.md`
3. 通过飞书发送文件路径给用户

**目录规范**：
- 报告 Markdown：`final_report/geo-strategy/<product>-geo-strategy-report.md`
- 原始 CSV：`final_report/data/<product>-geo-raw.csv`
- 分析结果：`final_report/geo-strategy/`

---

## Changelog

### 1.2.0 (2026-05-20)
- 新增「Two Output Modes」章节：明确区分售前演示版（Pre-sales）和品牌内部分析版（Internal Diagnostic）的适用场景、结构差异和输出特点
- 售前版核心规范：无科普/竞品全名/话术封装/P0-P3分级/无报价/现场可直接讲解
- 内部分析版核心规范：数据明细/CSV原始数据引用/详细执行计划/含告警模块
- 报告输出路径：`~/final_report/geo-strategy/<product>-geo-strategy-report.md`（售前版标记 `-presales`，内部分析版标记 `-internal`）

### 1.1.0 (2026-05-19)
- 新增输出格式与交付规范（html-anything 渲染 + final_report 目录结构）
- 明确 HTML 预览 URL 交付流程

### 1.0.0 (2026-04-18)
- 初始版本
- 完整支持多维度可见度×准确率分析
- 新增 Buzzword 竞品竞争分析
- 结论先行结构
- 分阶段执行路线图