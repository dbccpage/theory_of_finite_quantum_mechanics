"""Replay the finite instances checked by proved_rows."""

from __future__ import annotations

import json

from witnessed_difference.proved_rows import replay_proved_rows


def main() -> int:
    report = replay_proved_rows()
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
