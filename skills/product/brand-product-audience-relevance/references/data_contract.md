# Data Contract

更新时间：2026-05-28

## 源文件

默认源目录：

```text
/Users/apple/Downloads/User/CID 人群
```

文件类型：`.xlsx`

sheet 名称：

```text
人群画像
```

## 主分析文件

40 个 `年龄段 x 城市级别` 文件，命名模式：

```text
{年龄段代码} {城市线级} Persona Report {YYYYMMDD} {HHMMSS}.xlsx
```

年龄段代码：

| 代码 | 标准标签 |
|---|---|
| `1825` | `18-25岁` |
| `2530` | `25-30岁` |
| `3035` | `30-35岁` |
| `3540` | `35-40岁` |
| `4045` | `40-45岁` |
| `4550` | `45-50岁` |
| `5055` | `50-55岁` |
| `55+` | `55岁以上` |

城市线级标准值：

```text
一线、新一线、二线、三线、四五线
```

原始文件里的 `四线五线` 标准化为 `四五线`，同时保留原始值用于审计。

## 辅助文件

30 个 `人生阶段 x 城市级别` 文件，命名模式：

```text
{人生阶段}x{城市线级} Persona Report {YYYYMMDD} {HHMMSS}.xlsx
```

人生阶段：

```text
事业成熟期、孕产时期、求职时期、老年黄金期、育儿时期、适婚时期
```

辅助文件只用于解释，不参与 40 个主分析人群的排名分数。

## Excel 数据段

1. 人群画像

字段含义：

- 一级分类：如人口统计学、支出、收入等。
- 二级分类：如性别、年龄段细分、婚姻状态、人生阶段、文化水平等。
- 三级分类：如女、已婚、月收入区间等。
- `ONE ID`：该三级分类下的人数。
- `RATIO`：该三级分类占本切片总人数比例。
- `TGI`：倾向指数。
- 空数值代表 0 人，不能丢弃。

2. 购买数据

包含：

- 品类购买。
- 品类下品牌或明细购买。
- 购买频次分桶。
- 购买金额分桶。

3. 媒体行为

媒体大类：

```text
新闻资讯、金融理财、移动购物、系统工具、教育学习、数字阅读、移动音乐、移动视频、生活服务、办公商务、出行服务、手机游戏、移动社交
```

每个媒体大类下有具体 App，并包含：

- `ONE ID`
- `RATIO`
- `TGI`
- `日均使用频次`
- `日均使用时长`

## 配置文件契约

配置文件是 JSON，核心字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `analysis_id` | 是 | 输出文件前缀的一部分，只用英文、数字、下划线 |
| `input_name` | 是 | 用户原始输入 |
| `product_name` | 是 | 标准化后的品牌/产品名 |
| `report_title` | 是 | 报告标题 |
| `report_date` | 是 | 分析日期 |
| `match_status` | 是 | `observed`、`category_observed`、`inferred` |
| `direct_match_terms` | 是 | 用于 CID 命中检查的关键词 |
| `strict_observed_terms` | 否 | 严格观测实体列表 |
| `sources` | 是 | 外部来源 URL 和抓取日期 |
| `product_attributes` | 是 | 品牌、规格、属性、价格、买点、卖点 |
| `features` | 是 | 购买、画像、媒体特征 |
| `objectives` | 是 | `conversion` 和 `brand_mind` 证据族 |
| `plain_phrases` | 否 | 特征的直白解释话术 |
| `plain_closing` | 否 | 两套目标的结尾解释 |
| `auxiliary` | 否 | 用哪些特征生成辅助人生阶段解释 |

## 输出文件契约

### `*_ranking.csv`

一行代表一个主分析人群，共 40 行数据。

关键字段：

- `audience`
- `segment_code`
- `age_band`
- `city_tier`
- `segment_total_one_id`
- `match_status`
- `conversion_rank`
- `conversion_score`
- `conversion_evidence`
- `conversion_plain_explanation`
- `brand_mind_rank`
- `brand_mind_score`
- `brand_mind_evidence`
- `brand_mind_plain_explanation`
- `auxiliary_life_stage_evidence`

### `*_evidence.csv`

一行代表一个目标、一个人群、一个特征的证据。

关键字段：

- `objective`
- `audience`
- `feature_key`
- `feature_label`
- `feature_family`
- `feature_kind`
- `one_id`
- `segment_total_one_id`
- `ratio`
- `universe_rate`
- `affinity_index`
- `chi_square`
- `p_value`
- `percentile_score`

### `*_report.md`

面向人读的审计报告，必须包含：

- 结论口径。
- 来源审计。
- 产品属性归一化。
- CID 直接命中检查。
- 评分方法。
- Top 10。
- 40 个年龄城市人群并排排序。
- 解读边界。
