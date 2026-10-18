from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_certificate(path: Path) -> dict[str, Any]:
    """Load a certificate or ledger row JSON."""
    with path.open("r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        raise ValueError(f"File {path} is empty")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        if lines:
            return json.loads(lines[0])
        raise


def run_diff(cert_a: dict[str, Any], cert_b: dict[str, Any]) -> dict[str, Any]:
    """Perform comparative forensic diff between two certificates."""
    hash_a = cert_a.get("carrier_hash")
    hash_b = cert_b.get("carrier_hash")
    status_a = cert_a.get("terminal_status")
    status_b = cert_b.get("terminal_status")
    class_a = cert_a.get("algebraic_class_id")
    class_b = cert_b.get("algebraic_class_id")

    same_hash = (hash_a == hash_b) and (hash_a is not None)
    same_status = (status_a == status_b) and (status_a is not None)
    same_class = (class_a == class_b) and (class_a is not None)

    if not same_hash:
        mutation = "detected"
    elif status_a != status_b or class_a != class_b:
        mutation = "detected (unstable evaluation deviation)"
    else:
        mutation = "none"

    return {
        "same_carrier_hash": same_hash,
        "same_terminal_status": same_status,
        "same_q1_class": same_class,
        "transport_mutation": mutation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Forensic certificate comparator and transport mutation detector"
    )
    parser.add_argument("cert_a", type=Path, help="Path to first certificate or ledger JSON")
    parser.add_argument("cert_b", type=Path, help="Path to second certificate or ledger JSON")
    args = parser.parse_args()

    try:
        cert_a = load_certificate(args.cert_a)
        cert_b = load_certificate(args.cert_b)

        res = run_diff(cert_a, cert_b)

        print(f"same carrier_hash: {str(res['same_carrier_hash']).lower()}")
        print(f"same terminal_status: {str(res['same_terminal_status']).lower()}")
        print(f"same q1_class: {str(res['same_q1_class']).lower()}")
        print(f"transport mutation: {res['transport_mutation']}")
        return 0
    except Exception as e:
        print(f"Error executing diff: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

