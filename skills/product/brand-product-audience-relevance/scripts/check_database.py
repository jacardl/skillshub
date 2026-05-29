from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="5444")
    parser.add_argument("--dbname", default="radar")
    parser.add_argument("--user", default="radar")
    parser.add_argument("--password", default="radar")
    parser.add_argument("--vendor", default="outputs/cid_persona_design/vendor")
    args = parser.parse_args()

    vendor = Path(args.vendor)
    if vendor.exists():
        sys.path.insert(0, str(vendor))
    import psycopg

    queries = [
        ("cid.dim_report_source", "select count(*) from cid.dim_report_source"),
        ("cid.dim_audience_segment", "select count(*) from cid.dim_audience_segment"),
        ("cid.fact_segment_profile_value", "select count(*) from cid.fact_segment_profile_value"),
        ("cid.fact_segment_entity_metric", "select count(*) from cid.fact_segment_entity_metric"),
        ("cid.fact_segment_entity_bucket", "select count(*) from cid.fact_segment_entity_bucket"),
    ]

    try:
        with psycopg.connect(
            host=args.host,
            port=int(args.port),
            dbname=args.dbname,
            user=args.user,
            password=args.password,
            connect_timeout=5,
        ) as conn:
            for label, sql in queries:
                value = conn.execute(sql).fetchone()[0]
                print(f"{label}\t{value}")
    except Exception as exc:
        raise SystemExit(
            "Could not connect to PostgreSQL. Check that the local database is running "
            f"and reachable at {args.host}:{args.port}. Original error: {exc}"
        ) from exc


if __name__ == "__main__":
    main()
