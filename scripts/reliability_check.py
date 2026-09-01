#!/usr/bin/env python3
"""Read-only-style production checks for the math learning system.

The script follows the reliability discipline used by the English project, but
checks math-specific invariants: a question must lead to a real type cluster,
the 880 image bank must be usable, and self-assessment records must remain
valid.  `init_db` is called first only to apply the project's idempotent schema
migrations/backfill before inspection.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"
FRONTEND_ROOT = ROOT / "frontend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import db  # noqa: E402
import server  # noqa: E402


def _scalar(conn, sql: str, args: tuple = ()) -> int:
    return int(conn.execute(sql, args).fetchone()[0])


def _assert_zero(conn, sql: str, label: str) -> None:
    count = _scalar(conn, sql)
    assert count == 0, f"{label}: {count}"


def check_question_and_type_integrity(conn) -> None:
    assert _scalar(conn, "SELECT COUNT(*) FROM questions") > 0, "题库为空"
    assert _scalar(conn, "SELECT COUNT(*) FROM types") > 0, "题型库为空"
    _assert_zero(conn, "SELECT COUNT(*) FROM questions WHERE TRIM(type_name)=''", "存在空题型题目")
    _assert_zero(
        conn,
        """SELECT COUNT(*) FROM questions q
           LEFT JOIN types t ON t.name=q.type_name
           WHERE t.name IS NULL""",
        "题目指向不存在的题型",
    )
    _assert_zero(
        conn,
        """SELECT COUNT(*) FROM types t
           LEFT JOIN questions q ON q.type_name=t.name
           WHERE q.id IS NULL""",
        "存在没有题目的题型",
    )


def check_curated_explanations(conn) -> None:
    fields = ("intuition", "trigger", "example_stem")
    for field in fields:
        _assert_zero(
            conn,
            f"SELECT COUNT(*) FROM types WHERE curated=1 AND TRIM({field})=''",
            f"已归纳题型缺少 {field}",
        )
    json_fields = ("steps_json", "pitfalls_json", "example_steps_json", "variants_json", "figures_json")
    rows = conn.execute(
        "SELECT name," + ",".join(json_fields) + " FROM types WHERE curated=1"
    ).fetchall()
    for row in rows:
        for field in json_fields:
            try:
                value = json.loads(row[field])
            except json.JSONDecodeError as exc:
                raise AssertionError(f"题型 {row['name']} 的 {field} 不是 JSON") from exc
            assert isinstance(value, list), f"题型 {row['name']} 的 {field} 不是数组"
    for field in ("steps_json", "pitfalls_json", "example_steps_json"):
        _assert_zero(
            conn,
            f"SELECT COUNT(*) FROM types WHERE curated=1 AND (TRIM({field})='' OR {field}='[]')",
            f"已归纳题型缺少 {field}",
        )


def check_880_assets_and_clusters(conn) -> None:
    rows = conn.execute(
        "SELECT number, stem_html, type_name FROM questions WHERE paper='lilin880' ORDER BY number"
    ).fetchall()
    assert rows, "缺少李林880题库"
    numbers = [int(row["number"]) for row in rows]
    assert len(numbers) == len(set(numbers)), "李林880题号重复"
    for row in rows:
        assert str(row["type_name"]).strip(), f"880 第 {row['number']} 题没有题型/待归纳题簇"
        refs = re.findall(r"src=[\"']([^\"']+)", str(row["stem_html"]))
        refs = [ref.split("?", 1)[0].lstrip("/") for ref in refs if ref.split("?", 1)[0].lstrip("/").startswith("880/")]
        assert refs, f"880 第 {row['number']} 题没有题图"
        for ref in refs:
            asset = (FRONTEND_ROOT / ref).resolve()
            assert asset.is_relative_to(FRONTEND_ROOT.resolve()), f"880 题图越界: {ref}"
            assert asset.is_file() and asset.stat().st_size > 0, f"880 题图缺失: {ref}"


def check_learning_record_integrity(conn) -> None:
    _assert_zero(
        conn,
        """SELECT COUNT(*) FROM attempts
           WHERE result NOT IN ('correct','wrong','fuzzy')
              OR reason NOT IN ('','idea','calculation','speed')
              OR (reason<>'' AND result<>'wrong')
              OR elapsed_seconds < 0 OR elapsed_seconds > 86400""",
        "作答记录不合法",
    )
    _assert_zero(
        conn,
        """SELECT COUNT(*) FROM attempts a
           LEFT JOIN questions q ON q.id=a.question_id
           WHERE q.id IS NULL""",
        "作答记录指向不存在的题目",
    )
    _assert_zero(
        conn,
        """SELECT COUNT(*) FROM type_progress p
           LEFT JOIN types t ON t.name=p.type_name
           WHERE t.name IS NULL OR p.status NOT IN ('learning','mastered')""",
        "题型掌握状态不合法",
    )
    _assert_zero(
        conn,
        """SELECT COUNT(*) FROM type_progress
           WHERE status='mastered' AND type_name LIKE '李林880·%·待归纳'""",
        "待归纳880题簇被标记掌握",
    )


def check_api_shape(conn) -> None:
    assert server.health() == {"ok": True}
    tree = server.tree()
    visible = sum(
        len(group["types"])
        for subject in tree
        for chapter in subject["chapters"]
        for group in chapter["groups"]
    )
    expected = _scalar(
        conn,
        "SELECT COUNT(*) FROM types t WHERE EXISTS(SELECT 1 FROM questions q WHERE q.type_name=t.name)",
    )
    assert visible == expected, f"题型树可见数 {visible} != 数据库可达数 {expected}"


CHECKS = (
    check_question_and_type_integrity,
    check_curated_explanations,
    check_880_assets_and_clusters,
    check_learning_record_integrity,
    check_api_shape,
)


def main() -> int:
    conn = db.connect()
    try:
        db.init_db(conn)
        for check in CHECKS:
            check(conn)
            print(f"OK math.{check.__name__}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
