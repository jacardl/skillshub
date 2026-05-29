# Agent Guide

更新时间：2026-05-28

本指南给接手 agent 使用。目标是对用户提供的 brand 或 product，输出 40 个年龄城市人群的相关性排序，并保留证据链。

## 工作流程

1. 标准化输入

识别用户给的是品牌、产品、产品族、URL、文本还是内部 id。若只有 product，先补齐 brand，因为 brand 会影响产品相关性。

2. 补齐公开信息

优先查官方网站，其次使用权威公开来源。记录来源 URL 和抓取日期。产品属性统一写为：品牌、规格、属性、价格、买点、卖点。

3. 检查 CID 直接观测

检查 CID 中是否有品牌名、产品名、品类名、相关 App 或画像字段。

匹配状态规则：

- `observed`：CID 中有品牌、产品或明确实体的直接观测。
- `category_observed`：CID 中没有品牌/产品直接观测，但有明确品类或强相关实体可严格计算。
- `inferred`：只能使用代理变量。
- `needs_confirmation_for_proxy`：只能代理推断且用户尚未确认时，先暂停并说明原因。

4. 设计特征

特征必须来自 CID 可解释字段：

- 购买数据：品类购买、品牌购买、购买频次、购买金额。
- 画像数据：性别、年龄、婚姻、人生阶段、文化水平、收入、支出等。
- 媒体行为：媒体分类和 App。

优先使用可直接计算 `one_id / ratio / tgi` 的字段。媒体分类可以由 App 级别指标聚合得到触达倾向。

5. 分开定义两套目标

`conversion` 通常关注：

- 品类购买基础。
- 购买/消费承接。
- 购物、社交、搜索、内容等转化触点。

`brand_mind` 通常关注：

- 品牌或品类心智基础。
- 目标人群与产品定位的匹配。
- 社交、视频、新闻、阅读等内容触达。

两套目标分别输出，不把它们合成一个总分。

6. 生成配置并运行

复制 `config/template.json` 为新文件，填完后运行：

```bash
/Users/apple/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
agent_capabilities/brand_product_audience_relevance/scripts/analyze_brand_product.py \
--config agent_capabilities/brand_product_audience_relevance/config/<your_config>.json \
--out-dir outputs/brand_product_audience
```

7. 检查输出

必须确认：

- `ranking.csv` 有 40 条数据行。
- `evidence.csv` 有每个目标、每个人群、每个特征的证据行。
- 报告中有来源审计、产品属性、直接命中检查、评分方法、Top 10、全量 40 人群排序和解读边界。

8. 更新项目文档

完成任务后更新：

- `PROJECT_NOTES.md`
- `PROJECT_PROGRESS.md`

如果新增了稳定方法、命令、文件路径或未解决问题，也要写入项目笔记。

## 解释要求

输出给用户时保留数值证据，同时增加直白解释。示例：

```text
“18-25岁x三线”排名靠前，主要因为他们在美妆个护购买上的亲和力更高，
说明这个人群里真正买过相关品类的人更多；同时购物和社交 App 触达更强，
更容易完成种草到下单。
```

不要只输出结论，也不要输出隐藏思考过程。应输出可审计证据：用到哪些字段、AI、p 值、来源 URL、抓取日期和边界说明。

## 重要边界

- Score 是 40 个人群内的相对证据强度，不是实际转化率，也不是品牌认知率。
- 卡方检验在大样本下容易显著，排序仍应主要看 AI 方向和相对强度。
- 30 个人生阶段城市切片只作为辅助解释，不参与主排名。
- 没有用户级原始数据时，不做多变量归因。
- 如果后续拿到品牌或产品直接数据，应优先替换品类或代理结果。
