from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def first_keyword(sql: str) -> str:
    stripped = sql.lstrip()
    if not stripped:
        return ""
    return stripped.split(None, 1)[0].lower()


def ensure_readonly(sql: str) -> None:
    keyword = first_keyword(sql)
    if keyword not in {"select", "with", "explain"}:
        raise SystemExit("Only read-only SQL starting with SELECT, WITH, or EXPLAIN is allowed.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="5444")
    parser.add_argument("--dbname", default="radar")
    parser.add_argument("--user", default="radar")
    parser.add_argument("--password", default="radar")
    parser.add_argument("--vendor", default="outputs/cid_persona_design/vendor")
    parser.add_argument("--sql")
    parser.add_argument("--file")
    args = parser.parse_args()

    if bool(args.sql) == bool(args.file):
        raise SystemExit("Pass exactly one of --sql or --file.")

    sql = args.sql if args.sql else Path(args.file).read_text(encoding="utf-8")
    ensure_readonly(sql)

    vendor = Path(args.vendor)
    if vendor.exists():
        sys.path.insert(0, str(vendor))
    import psycopg

    try:
        with psycopg.connect(
            host=args.host,
            port=int(args.port),
            dbname=args.dbname,
            user=args.user,
            password=args.password,
            connect_timeout=5,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                columns = [desc.name for desc in cur.description or []]
                writer = csv.writer(sys.stdout)
                writer.writerow(columns)
                for row in cur:
                    writer.writerow(row)
    except Exception as exc:
        raise SystemExit(
            "Could not run PostgreSQL query. Check that the local database is running "
            f"and reachable at {args.host}:{args.port}. Original error: {exc}"
        ) from exc


if __name__ == "__main__":
    main()
