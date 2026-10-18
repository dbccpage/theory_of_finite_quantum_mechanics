"""Ground-truth exact evaluator for the blind cluster partition challenge.

Wraps the exact SQLite evaluator from omega_engine_projects/fsp/code/sign_sql/exact_models.py
to provide deterministic verification of claimed partition values and cluster cancellations.

AuthorityEffect: None.
Firewall: Abstract discrete graph partition; zero physics/meron keywords.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega_engine_projects.fsp.code.sign_sql.exact_models import (  # noqa: E402
    meron_database,
    meron_summary,
    meron_transfer_trace,
)


class BlindClusterOracle:
    """Exact rational oracle for the 4-site, 2-repetition, q=3 periodic even chain."""

    def __init__(self, sites: int = 4, repetitions: int = 2, q: str = "3") -> None:
        self.sites = sites
        self.repetitions = repetitions
        self.q = q
        self._con = meron_database(sites, repetitions, q)
        self._summary = meron_summary(self._con)
        self._independent_trace = meron_transfer_trace(sites, repetitions, q)

    @property
    def total_subgraphs(self) -> int:
        return self._summary["graphs"]  # 256

    @property
    def total_configurations(self) -> int:
        return self._summary["configurations"]  # 1296

    @property
    def negative_configurations(self) -> int:
        return self._summary["negative_configurations"]  # 192

    @property
    def signed_partition(self) -> str:
        return self._summary["signed_partition"]  # "912"

    @property
    def absolute_partition(self) -> str:
        return self._summary["absolute_partition"]  # "1296"

    @property
    def average_sign(self) -> str:
        return self._summary["average_sign"]  # "19/27"

    @property
    def zero_charge_subgraphs(self) -> int:
        return self._summary["zero_meron_graphs"]  # 199

    @property
    def cancelling_subgraphs(self) -> int:
        return self.total_subgraphs - self.zero_charge_subgraphs  # 57

    @property
    def reduced_partition(self) -> str:
        return self._summary["reduced_partition"]  # "912"

    def get_sample_subgraphs(self, limit: int = 5) -> list[dict]:
        """Return sample subgraphs with cycle decomposition for prompt inclusion."""
        # Query representative subgraphs: both zero-charge and cancelling
        samples = []
        rows = self._con.execute(
            """
            SELECT o.gid, o.clusters, o.merons, g.weight, o.reduced_weight
            FROM meron_orbit o
            JOIN meron_graph g ON g.gid = o.gid
            ORDER BY o.gid
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        for gid, k, odd_cycles, weight, reduced_weight in rows:
            # Get component cycle info
            components = self._con.execute(
                """
                SELECT cluster, COUNT(node) as size
                FROM meron_component
                WHERE gid = ?
                GROUP BY cluster
                ORDER BY cluster
                """,
                (gid,),
            ).fetchall()

            # Get configuration signs for this subgraph
            configs = self._con.execute(
                """
                SELECT mask, sign, weight
                FROM meron_configuration
                WHERE gid = ?
                ORDER BY mask
                """,
                (gid,),
            ).fetchall()

            samples.append(
                {
                    "subgraph_id": gid,
                    "cycle_count": k,
                    "odd_parity_cycles": odd_cycles,
                    "base_weight": weight,
                    "reduced_weight": reduced_weight,
                    "cycles": [{"cycle_id": c[0], "length": c[1]} for c in components],
                    "configurations": [
                        {"flip_mask": conf[0], "sign": conf[1], "weight": conf[2]}
                        for conf in configs
                    ],
                }
            )
        return samples

    def evaluate_proposer_claim(
        self,
        claimed_z: str | int | None,
        cycle_independence_recognized: bool,
        parity_cancellation_proved: bool,
        zero_sector_reduction_used: bool,
    ) -> dict:
        """Score a proposer's solution against the exact ground truth."""
        score = 0
        feedback = []

        # Rubric item 1: Exact target Z
        z_match = False
        if claimed_z is not None:
            try:
                z_match = str(claimed_z).strip() == self.signed_partition
            except Exception:
                z_match = False

        if z_match:
            score += 1
            feedback.append("PASS: Partition value Z matches ground-truth 912 exactly.")
        else:
            feedback.append(f"FAIL: Claimed Z={claimed_z} does not match exact ground-truth 912.")

        # Rubric item 2: Cycle/cluster independence
        if cycle_independence_recognized:
            score += 1
            feedback.append(
                "PASS: Recognized that configurations factorize into independent cycle components."
            )
        else:
            feedback.append("FAIL: Failed to recognize factorized cycle independence.")

        # Rubric item 3: Parity cancellation
        if parity_cancellation_proved:
            score += 1
            feedback.append(
                "PASS: Proved that odd-parity cycle flips invert the global sign, causing identical pairwise cancellation."
            )
        else:
            feedback.append("FAIL: Did not prove that single cycle flips invert the global sign.")

        # Rubric item 4: Zero-charge reduction
        if zero_sector_reduction_used:
            score += 1
            feedback.append(
                "PASS: Reduced partition sum strictly to the zero-odd-charge sector (199 subgraphs), eliminating all negative terms."
            )
        else:
            feedback.append(
                "FAIL: Did not restrict the sum to the non-negative zero-odd-charge sector."
            )

        return {
            "score": score,
            "max_score": 4,
            "perfect": score == 4,
            "feedback": feedback,
            "ground_truth": {
                "Z": self.signed_partition,
                "Z_abs": self.absolute_partition,
                "average_sign": self.average_sign,
                "total_subgraphs": self.total_subgraphs,
                "zero_charge_subgraphs": self.zero_charge_subgraphs,
                "cancelling_subgraphs": self.cancelling_subgraphs,
            },
        }


if __name__ == "__main__":
    oracle = BlindClusterOracle()
    print("=" * 60)
    print("Blind Cluster Oracle Ground Truth:")
    print(f"  Total Subgraphs:       {oracle.total_subgraphs}")
    print(f"  Total Configurations:  {oracle.total_configurations}")
    print(f"  Negative Configs:      {oracle.negative_configurations}")
    print(f"  Average Sign:          {oracle.average_sign}")
    print(f"  Exact Signed Z:        {oracle.signed_partition}")
    print(f"  Absolute Sum Z_abs:    {oracle.absolute_partition}")
    print(f"  Zero-Charge Subgraphs: {oracle.zero_charge_subgraphs}")
    print(f"  Cancelling Subgraphs:  {oracle.cancelling_subgraphs}")
    print("=" * 60)
    samples = oracle.get_sample_subgraphs(2)
    print(f"Retrieved {len(samples)} sample subgraphs for prompt construction.")
    print("Oracle operational: PASS")
