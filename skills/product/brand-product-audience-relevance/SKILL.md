---
name: brand-product-audience-relevance
description: Analyze brand or product relevance against CID audience data. Use when Codex needs to evaluate a brand, product, product family, or URL against CID age-city audiences; generate conversion and brand-mind audience rankings; compute Affinity Index and Chi-Square evidence; inspect CID Excel or PostgreSQL data; create auditable reports with sources, product attributes, numeric evidence, and plain-language explanations.
---

# Brand Product Audience Relevance

## Overview

Use this skill to turn a user-provided brand/product into a CID audience relevance analysis. The default output is a 40-row `年龄段 x 城市级别` ranking with two separate objectives: `conversion` and `brand_mind`.

## Core Rules

- Treat the 40 `年龄段 x 城市级别` segments as the primary ranking universe.
- Treat the 30 `人生阶段 x 城市级别` segments as auxiliary evidence only.
- Use strict observed CID evidence first: Affinity Index and Chi-Square on observed counts.
- If the product has no direct CID hit but its category is observed, set `match_status` to `category_observed`.
- If only proxy variables are available, stop and ask the user before producing inferred rankings.
- Keep `conversion` and `brand_mind` separate. Do not collapse them into one score.
- Record external source URL and crawl/read date for brand/product enrichment.
- Normalize product attributes to: 品牌、规格、属性、价格、买点、卖点.
- Explain results with both numeric evidence and plain-language interpretation.

## Workflow

1. Standardize the input.

Identify whether the user supplied a brand, product, product family, URL, or free text. If only a product is supplied, enrich the brand from official or public sources.

2. Check CID observability.

Search CID terms for brand, product, product family, category, media entities, and useful profile variables. Use:

- `observed` for direct brand/product/entity evidence.
- `category_observed` when the relevant CID category is observable but brand/product is not.
- `inferred` only after user confirmation.

3. Create an analysis config.

Copy `references/config_template.json` to a working config path and fill product attributes, sources, features, objectives, and plain-language phrases. Use `references/dabao_jinghuashuang_example.json` as a concrete example.

4. Run the Excel analyzer.

```bash
python3 skills/brand-product-audience-relevance/scripts/analyze_brand_product.py \
  --config path/to/config.json \
  --source-dir "/Users/apple/Downloads/User/CID 人群" \
  --out-dir outputs/brand_product_audience
```

The script emits:

- `*_ranking.csv`: 40 primary audiences with conversion and brand-mind ranks.
- `*_evidence.csv`: feature-level AI, Chi-Square, p-value, and percentile evidence.
- `*_report.md`: auditable Markdown report.

5. Validate the output.

Confirm:

- `primary_segments=40`
- `auxiliary_segments=30`
- ranking CSV has 40 data rows
- report includes sources, product attributes, direct-hit check, methods, Top 10, full 40-row ranking, and boundaries

6. Summarize for the user.

Lead with the result files and top audience patterns. Mention `match_status` and the biggest data boundary. Keep detailed tables in the generated report/CSV.

## Database Utilities

Use PostgreSQL only when reachable. Current default connection:

```text
host=127.0.0.1
port=5444
database=radar
user=radar
password=radar
schema=cid
```

Check table counts:

```bash
python3 skills/brand-product-audience-relevance/scripts/check_database.py
```

Run a read-only SQL query and output CSV:

```bash
python3 skills/brand-product-audience-relevance/scripts/run_readonly_sql.py \
  --sql "select count(*) as n from cid.dim_audience_segment"
```

Use `references/common_queries.sql` for reusable query patterns.

## References

- `references/workflow.md`: fuller operating guide and quality rules.
- `references/data_contract.md`: CID Excel layout, config schema, and output schema.
- `references/database.md`: database status, target schema extensions, and future `brand_product` schema.
- `references/common_queries.sql`: reusable SQL snippets.
- `references/config_template.json`: blank analysis config.
- `references/dabao_jinghuashuang_example.json`: completed example config.

Load only the specific reference needed for the task.
