"""Reproduction entry for WDP Paper 001 finite checks."""

from __future__ import annotations

import json

import sn_mssn_checks


def main() -> int:
    report = sn_mssn_checks.run_reproduction()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
