"""Inspect, snapshot or check WDP. A changed baseline never approves its own diff."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from paper_contract.audit import (  # noqa: E402
    AuditReport,
    PaperBaseline,
    compare,
    fingerprint,
    integrity_issues,
)
from paper_contract.inventory import BASELINE, worktree_snapshot  # noqa: E402
from paper_contract.models import ResearchPaper  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["inspect", "snapshot", "schema", "baseline", "check"])
    parser.add_argument("--paper-root", type=Path, default=ROOT)
    parser.add_argument("--repository", default="dbccpage/the_symbol_game")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--trusted-baseline", type=Path, help="Required for check; obtain independently from the reviewed base commit")
    args = parser.parse_args(argv)
    try:
        if args.command == "schema":
            import json
            payload = json.dumps(ResearchPaper.model_json_schema(), indent=2) + "\n"
            status = 0
        else:
            paper = worktree_snapshot(args.paper_root, repository=args.repository)
            issues = integrity_issues(paper)
            if args.command == "check":
                if args.trusted_baseline is None:
                    parser.error("check requires --trusted-baseline; no automatic use of an edited local baseline")
                baseline = PaperBaseline.model_validate_json(args.trusted_baseline.read_bytes())
                report = compare(baseline, paper)
                candidate_baseline = args.paper_root / BASELINE
                if not candidate_baseline.is_file() or candidate_baseline.read_bytes() != args.trusted_baseline.read_bytes():
                    report = AuditReport(matches_baseline=False, changes=report.changes,
                                         issues=(*report.issues, "candidate baseline missing/changed relative to independently trusted baseline"))
                payload, status = report.model_dump_json(indent=2) + "\n", 0 if report.matches_baseline else 1
            elif args.command in {"baseline", "snapshot"}:
                if args.output is None:
                    parser.error("baseline/snapshot requires an explicit --output")
                if issues:
                    raise ValueError("refuse a baseline/snapshot with integrity issues: " + "; ".join(issues))
                obj = fingerprint(paper) if args.command == "baseline" else paper
                payload, status = obj.model_dump_json(indent=2) + "\n", 0
            else:
                import json
                payload = json.dumps({
                    "authority_effect": "None", "files": len(paper.artifacts()),
                    "sections": len(paper.manuscript.sections), "equations": len(paper.manuscript.equations),
                    "canonical_claims": sum(c.register_kind == "canonical" for c in paper.claim_ledger.records),
                    "supplement_claims": sum(c.register_kind != "canonical" for c in paper.claim_ledger.records),
                    "issues": issues,
                }, indent=2) + "\n"
                status = int(bool(issues))
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
        return status
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"paper contract refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
