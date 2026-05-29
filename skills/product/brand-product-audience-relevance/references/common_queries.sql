-- Brand/Product Audience Relevance common queries
-- Updated: 2026-05-28

-- ============================================================
-- 1. Current cid schema checks
-- ============================================================

select count(*) as report_sources
from cid.dim_report_source;

select count(*) as audience_segments
from cid.dim_audience_segment;

select count(*) as profile_rows
from cid.fact_segment_profile_value;

select count(*) as entity_metric_rows
from cid.fact_segment_entity_metric;

select count(*) as entity_bucket_rows
from cid.fact_segment_entity_bucket;

-- ============================================================
-- 2. Current 30-table schema examples
-- These work against the currently verified database.
-- ============================================================

-- 人群画像
select *
from cid.v_segment_profile_values
where segment_name = '事业成熟期x一线'
  and level1_category = '人口统计学'
order by source_row;

-- 某人群在某品类下的品牌或明细排行
select *
from cid.v_segment_entity_metrics
where segment_name = '事业成熟期x一线'
  and domain = 'purchase'
  and level2_category = '美妆个护'
order by one_id desc nulls last;

-- 某人群 App 偏好
select *
from cid.v_segment_entity_metrics
where segment_name = '事业成熟期x一线'
  and domain = 'media'
order by tgi desc nulls last;

-- 某人群购买金额分桶
select
  m.segment_name,
  m.level2_category,
  m.entity_name,
  b.bucket_group,
  b.bucket_label,
  b.one_id,
  b.ratio
from cid.v_segment_entity_metrics m
join cid.fact_segment_entity_bucket b on b.metric_id = m.metric_id
where m.segment_name = '事业成熟期x一线'
  and m.domain = 'purchase'
  and b.bucket_group = 'purchase_amount'
order by m.one_id desc nulls last, b.bucket_order;

-- ============================================================
-- 3. 70-table target schema examples
-- Use after dim_audience_segment is extended and all 70 files are imported.
-- ============================================================

-- 40 个主分析人群
select segment_code, segment_name, age_band_label, city_tier, segment_total_one_id
from cid.dim_audience_segment
where is_primary_analysis_segment
order by age_band_code, city_tier;

-- 30 个辅助人群
select segment_code, segment_name, life_stage, city_tier, segment_total_one_id
from cid.dim_audience_segment
where is_auxiliary_segment
order by life_stage, city_tier;

-- 主分析人群的美妆个护购买 AI
with base as (
  select
    s.segment_code,
    s.segment_name,
    s.segment_total_one_id,
    coalesce(sum(m.one_id) filter (
      where m.domain = 'purchase'
        and m.entity_type = 'category'
        and m.entity_name = '美妆个护'
    ), 0) as target_one_id
  from cid.dim_audience_segment s
  left join cid.fact_segment_entity_metric m on m.segment_id = s.segment_id
  where s.is_primary_analysis_segment
  group by s.segment_code, s.segment_name, s.segment_total_one_id
),
universe as (
  select
    sum(target_one_id)::numeric as target_total,
    sum(segment_total_one_id)::numeric as universe_total
  from base
)
select
  b.segment_code,
  b.segment_name,
  b.target_one_id,
  b.segment_total_one_id,
  b.target_one_id::numeric / nullif(b.segment_total_one_id, 0) as ratio,
  u.target_total / nullif(u.universe_total, 0) as universe_rate,
  100 * (b.target_one_id::numeric / nullif(b.segment_total_one_id, 0))
    / nullif(u.target_total / nullif(u.universe_total, 0), 0) as affinity_index
from base b
cross join universe u
order by affinity_index desc nulls last;

-- 主分析人群的女性画像 AI
with base as (
  select
    s.segment_code,
    s.segment_name,
    s.segment_total_one_id,
    coalesce(sum(p.one_id) filter (
      where p.level1_category = '人口统计学'
        and p.level2_category = '性别'
        and p.level3_value = '女'
    ), 0) as target_one_id
  from cid.dim_audience_segment s
  left join cid.fact_segment_profile_value p on p.segment_id = s.segment_id
  where s.is_primary_analysis_segment
  group by s.segment_code, s.segment_name, s.segment_total_one_id
),
universe as (
  select
    sum(target_one_id)::numeric as target_total,
    sum(segment_total_one_id)::numeric as universe_total
  from base
)
select
  b.segment_code,
  b.segment_name,
  b.target_one_id,
  b.segment_total_one_id,
  100 * (b.target_one_id::numeric / nullif(b.segment_total_one_id, 0))
    / nullif(u.target_total / nullif(u.universe_total, 0), 0) as affinity_index
from base b
cross join universe u
order by affinity_index desc nulls last;

-- ============================================================
-- 4. Future brand_product schema examples
-- Use after analysis results are loaded into brand_product tables.
-- ============================================================

-- 某次分析的双目标前 10
select
  r.analysis_id,
  s.objective,
  s.rank,
  s.segment_code,
  s.score,
  s.evidence_summary,
  s.plain_explanation
from brand_product.analysis_run r
join brand_product.audience_score s on s.run_id = r.run_id
where r.analysis_id = 'dabao_jinghuashuang'
  and s.rank <= 10
order by s.objective, s.rank;

-- 某个人群的逐字段证据
select
  r.analysis_id,
  e.objective,
  e.segment_code,
  e.feature_label,
  e.feature_family,
  e.affinity_index,
  e.p_value,
  e.percentile_score
from brand_product.analysis_run r
join brand_product.audience_evidence e on e.run_id = r.run_id
where r.analysis_id = 'dabao_jinghuashuang'
  and e.segment_code = '1825x三线'
order by e.objective, e.feature_family, e.feature_label;
