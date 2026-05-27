# GEO Strategy Report Skill

GEO (Generative Engine Optimization) 策略分析报告自动生成 Skill。

基于AI搜索监控输出的多维度CSV数据，自动生成完整的优化策略报告。

## 功能特点

- ✅ 结论先行结构，核心发现放在开头
- ✅ 可见度 × 准确率 四象限优先级矩阵分析
- ✅ 完整的Buzzword竞品竞争分析（新增功能）
- ✅ AI模型投入预算分配（按现有可见度倾斜）
- ✅ 来源渠道洞察
- ✅ 分阶段执行路线图

## 输入数据格式

CSV需要包含以下Sheet：

| Sheet | 必填 | 说明 |
|-------|------|------|
| Report Summary | ✅ | 产品信息、时间范围 |
| Brand Visibility | ✅ | 品牌可见度排名 |
| Product Buzzwords | ✅ | 本品buzzword统计 |
| Brand Leaderboard | ✅ | 竞品排行榜，包含竞品buzzwords |
| Visibility - Role x Keyword | ✅ | 人群 × 关键词 可见度矩阵 |
| Accuracy - Role x Keyword | ✅ | 人群 × 关键词 准确率矩阵 |
| Visibility - Role x Competitor | ✅ | 人群 × 竞品 可见度 |
| ... | ... | 详见 SKILL.md |

## 输出报告结构

1. 核心结论速览
2. AI用户问询全链路与GEO优化定位
3. 数据维度说明
4. 人群 × 关键词 优先级矩阵（四象限分析）
5. 竞品分析（人群 × 竞品 × Buzzword）
6. AI模型优化策略 + 预算分配
7. 来源数据洞察
8. 分阶段执行路线图

## 示例

完整示例报告：`../../memory/research/geo-strategy/凯迪拉克XT5-GEO策略分析报告-2026-04-18.md`

## License

Apache-2.0
