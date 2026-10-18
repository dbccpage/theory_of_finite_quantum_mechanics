from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


import argparse
import json
from pathlib import Path
from typing import Any


def calculate_dashboard_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate Q^1 dashboard metrics over a collection of certificate ledger rows.

    Supports Rule[user_global] claim hygiene by presenting bounded statistics.
    """
    total = len(rows)
    representation_invalid_count = 0
    exact_certificate_count = 0
    closed_residual_count = 0
    open_obstruction_count = 0

    valid_q1_norms: list[int] = []
    class_id_distribution: dict[str, int] = {}

    for row in rows:
        status = row.get("terminal_status", "RepresentationInvalid")
        class_id = row.get("algebraic_class_id", "representation-invalid:unknown")
        class_id_distribution[class_id] = class_id_distribution.get(class_id, 0) + 1

        if status == "RepresentationInvalid":
            representation_invalid_count += 1
        elif status == "Exact":
            exact_certificate_count += 1
            valid_q1_norms.append(0)
        elif status == "ClosedResidual":
            closed_residual_count += 1
            try:
                norm_val = int(row.get("q1_norm", 0))
            except (ValueError, TypeError):
                norm_val = 0
            valid_q1_norms.append(norm_val)
        elif status == "OpenObstruction":
            open_obstruction_count += 1
            try:
                norm_val = int(row.get("q1_norm", 0))
            except (ValueError, TypeError):
                norm_val = 0
            valid_q1_norms.append(norm_val)

    valid_count = len(valid_q1_norms)
    if valid_count > 0:
        q1_zero_rate = sum(1 for n in valid_q1_norms if n == 0) / valid_count
        mean_q1_norm = sum(valid_q1_norms) / valid_count
    else:
        q1_zero_rate = 0.0
        mean_q1_norm = 0.0

    return {
        "metrics": {
            "q1_zero_rate": q1_zero_rate,
            "mean_q1_norm": mean_q1_norm,
            "closed_residual_count": closed_residual_count,
            "open_obstruction_count": open_obstruction_count,
            "exact_certificate_count": exact_certificate_count,
            "representation_invalid_count": representation_invalid_count,
            "total_certificates_evaluated": total,
        },
        "algebraic_class_distribution": class_id_distribution,
    }


def format_dashboard_report(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    dist = result["algebraic_class_distribution"]

    lines = [
        "==================================================",
        "          OMEGA PARITY Q^1 / l^1 DASHBOARD        ",
        "==================================================",
        f"Total Certificates Evaluated : {metrics['total_certificates_evaluated']}",
        f"Exact Certificates (Norm=0)  : {metrics['exact_certificate_count']}",
        f"Closed Obstruction Residuals  : {metrics['closed_residual_count']}",
        f"Open Obstruction Contradictions: {metrics['open_obstruction_count']}",
        f"Invalid Representations       : {metrics['representation_invalid_count']}",
        "--------------------------------------------------",
        f"Q^1 Zero Rate (Exact / Valid): {metrics['q1_zero_rate']:.4%}",
        f"Mean Q^1/l^1 Obstruction Norm : {metrics['mean_q1_norm']:.4f}",
        "--------------------------------------------------",
        "Algebraic Class ID Distribution:",
    ]
    for cid, count in sorted(dist.items()):
        lines.append(f"  - {cid:35} : {count} occurrences")
    lines.append("==================================================")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Majorana Parity Q^1 / l^1 dashboard metric aggregator"
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        required=True,
        help="Path to certificate_ledger.jsonl",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON results instead of report",
    )
    args = parser.parse_args()

    ledger_path = args.ledger
    if not ledger_path.exists():
        print(f"Error: Ledger file {ledger_path} does not exist.")
        return 1

    rows: list[dict[str, Any]] = []
    with ledger_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    results = calculate_dashboard_metrics(rows)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_dashboard_report(results))

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

