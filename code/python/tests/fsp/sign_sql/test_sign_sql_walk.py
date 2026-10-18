"""Tests pinning the key numbers of the sign-problem walk database.

Pinned:
  * the cancellation (severity) ratio in presentation A: exactly 1/15;
  * the non-negativity EXISTS = 1 for presentation B (a stored sign-free
    re-presentation of the same system exists);
  * the pricing-audit row count: 17 admissions void->rung7, split 10 licensed
    / 7 priced;
  * both presentations agree on the net total (1/2) -- the re-presentation
    changed the writing, not the thing written;
  * the Wheeler-DeWitt row is present, unique, and DECLARED, not derived.

AuthorityEffect: None.  These pins keep the toy honest; they prove nothing
about physics.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src.fsp.sign_sql.run_sign_sql as run_sign_sql  # noqa: E402


def queries_by_id() -> dict[str, str]:
    text = (run_sign_sql.BASE / "queries.sql").read_text(encoding="utf-8")
    return {qid: sql for qid, _title, sql in run_sign_sql.load_queries(text)}


class TestSignSql(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conn = run_sign_sql.build_db()
        cls.queries = queries_by_id()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()

    def rows(self, qid: str):
        cols, rows = run_sign_sql.run_query(self.conn, self.queries[qid])
        return cols, rows

    def test_q1_net_totals_agree_across_presentations(self) -> None:
        cols, rows = self.rows("q1")
        by_label = {r[cols.index("presentation")]: r for r in rows}
        for label in ("A_frustrated", "B_meron_repaired"):
            row = by_label[label]
            self.assertEqual(row[cols.index("sum_num")], 1, label)
            self.assertEqual(row[cols.index("common_den")], 2, label)
            # exactness guard: one shared denominator
            self.assertEqual(row[cols.index("distinct_dens")], 1, label)

    def test_q2_cancellation_ratio_in_A_is_exactly_1_over_15(self) -> None:
        cols, rows = self.rows("q2")
        by_label = {r[cols.index("presentation")]: r for r in rows}
        a = by_label["A_frustrated"]
        self.assertEqual(a[cols.index("ratio_num")], 1)
        self.assertEqual(a[cols.index("ratio_den")], 15)
        self.assertEqual(a[cols.index("l1_num")], 15)
        b = by_label["B_meron_repaired"]
        self.assertEqual(b[cols.index("ratio_num")], 1)
        self.assertEqual(b[cols.index("ratio_den")], 1)

    def test_q3_sign_free_presentation_exists(self) -> None:
        cols, rows = self.rows("q3")
        by_label = {r[cols.index("presentation")]: r for r in rows}
        self.assertEqual(
            by_label["B_meron_repaired"][cols.index("all_weights_nonnegative")], 1
        )
        self.assertEqual(
            by_label["A_frustrated"][cols.index("all_weights_nonnegative")], 0
        )
        for row in rows:
            self.assertEqual(row[cols.index("sign_free_presentation_exists")], 1)

    def test_q4_pricing_audit_row_count_and_split(self) -> None:
        cols, rows = self.rows("q4")
        self.assertEqual(len(rows), 17)
        priced = [r for r in rows if r[cols.index("priced")] == 1]
        self.assertEqual(len(priced), 7)   # imports #1..#6 + asymptotic frame
        tags = sorted(r[cols.index("price_tag")] for r in priced)
        self.assertEqual(tags, ["", "#1", "#2", "#3", "#4", "#5", "#6"])

    def test_q6_wheeler_dewitt_row_is_declared_not_derived(self) -> None:
        cols, rows = self.rows("q6")
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row[cols.index("standing")], "declared_boundary")
        self.assertEqual(row[cols.index("rung_name")], "wheeler_dewitt_boundary")
        self.assertIn("PP/021", row[cols.index("source")])


if __name__ == "__main__":
    unittest.main()
