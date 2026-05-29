# Database Notes

更新时间：2026-05-28

## 连接信息

```text
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5444
POSTGRES_DB=radar
POSTGRES_USER=radar
POSTGRES_PASSWORD=radar
POSTGRES_SCHEMA=cid
```

## 当前状态

当前 PostgreSQL 中已校验的是原 30 个人生阶段城市表版本：

| 表 | 行数 |
|---|---:|
| `cid.dim_report_source` | 30 |
| `cid.dim_audience_segment` | 30 |
| `cid.fact_segment_profile_value` | 15450 |
| `cid.fact_segment_entity_metric` | 51729 |
| `cid.fact_segment_entity_bucket` | 620932 |

新增 40 个年龄城市主分析表尚未正式落库。当前 `scripts/analyze_brand_product.py` 直接读取 Excel，确保 40 个主分析人群已经可以分析。

## 数据库检查

```bash
/Users/apple/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
agent_capabilities/brand_product_audience_relevance/scripts/check_database.py \
--host 127.0.0.1 --port 5444 --dbname radar --user radar --password radar
```

## 只读 SQL 查询

```bash
/Users/apple/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
agent_capabilities/brand_product_audience_relevance/scripts/run_readonly_sql.py \
--sql "select count(*) as n from cid.dim_audience_segment"
```

`run_readonly_sql.py` 只允许 `select`、`with`、`explain` 开头的查询，并以 CSV 输出结果，适合其他 agent 做数据库抽取和校验。

## 当前 schema 常用视图

```sql
select * from cid.v_segment_profile_values;
select * from cid.v_segment_entity_metrics;
select * from cid.v_segment_entity_affinity;
```

## 70 表目标 schema 扩展

为了同时保存 40 个主分析切片和 30 个辅助切片，`cid.dim_audience_segment` 建议增加以下字段：

```sql
alter table cid.dim_audience_segment
  add column if not exists segment_type text,
  add column if not exists segment_axis text,
  add column if not exists age_band_code text,
  add column if not exists age_band_label text,
  add column if not exists life_stage text,
  add column if not exists city_tier_raw text,
  add column if not exists is_primary_analysis_segment boolean default false,
  add column if not exists is_auxiliary_segment boolean default false;
```

字段含义：

- `segment_type='age_city'`：40 个主分析切片。
- `segment_type='life_stage_city'`：30 个辅助切片。
- `segment_axis='age_band'`：年龄段维度。
- `segment_axis='life_stage'`：人生阶段维度。
- `city_tier_raw`：Excel 文件名中的原始城市线级。
- `city_tier`：标准城市线级，其中 `四线五线` 统一为 `四五线`。
- `is_primary_analysis_segment=true`：参与 brand/product 主排序。
- `is_auxiliary_segment=true`：只参与辅助解释。

## 推荐分析层 schema

后续可新增独立 `brand_product` schema，避免把分析结果混入 CID 原始事实层：

```sql
create schema if not exists brand_product;

create table if not exists brand_product.analysis_run (
  run_id bigserial primary key,
  analysis_id text not null,
  input_name text not null,
  normalized_name text not null,
  match_status text not null,
  report_date date not null,
  created_at timestamptz default now()
);

create table if not exists brand_product.analysis_source (
  source_id bigserial primary key,
  run_id bigint not null references brand_product.analysis_run(run_id),
  source_name text not null,
  url text not null,
  crawl_date date not null,
  usage text
);

create table if not exists brand_product.product_attribute (
  run_id bigint primary key references brand_product.analysis_run(run_id),
  brand text,
  specification text,
  attributes text,
  price text,
  buy_points text,
  sell_points text
);

create table if not exists brand_product.audience_score (
  run_id bigint not null references brand_product.analysis_run(run_id),
  segment_code text not null,
  objective text not null,
  rank int not null,
  score numeric(8,4) not null,
  evidence_summary text,
  plain_explanation text,
  primary key (run_id, segment_code, objective)
);

create table if not exists brand_product.audience_evidence (
  run_id bigint not null references brand_product.analysis_run(run_id),
  segment_code text not null,
  objective text not null,
  feature_key text not null,
  feature_label text not null,
  feature_family text,
  feature_kind text,
  one_id bigint,
  segment_total_one_id bigint,
  ratio numeric,
  universe_rate numeric,
  affinity_index numeric,
  chi_square numeric,
  p_value numeric,
  percentile_score numeric,
  primary key (run_id, segment_code, objective, feature_key)
);
```

## 重建导入提醒

原有入库脚本位置：

```text
outputs/cid_persona_design/ingest_cid_persona.py
```

当前脚本历史上用于 30 表入库。扩展到 70 表时，需要把 `scripts/analyze_brand_product.py` 中的文件名识别逻辑同步回入库脚本：

- `{age_code} {city} Persona Report ...`
- `{life_stage}x{city} Persona Report ...`
- `四线五线` 标准化为 `四五线`
- `segment_type`、`segment_axis`、`age_band_code`、`age_band_label`、`life_stage` 等字段写入维表

重建前应先备份或确认可覆盖，再删除旧 schema。
