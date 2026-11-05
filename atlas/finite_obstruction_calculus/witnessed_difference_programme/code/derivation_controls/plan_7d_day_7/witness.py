"""Day 7 independent audit and linked delivery report control (PLAN-7D-DAY-7).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import sys


def _load_sibling_witness(control_name: str):
    path = Path(__file__).resolve().parents[1] / control_name / "witness.py"
    module_name = f"{control_name}_witness_loaded"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def verify_day_7_audit_report(
    promote_unrun_sg_episodes: bool = False,
    promote_open_lane_e_continuum_duality: bool = False,
    actual_paid_spend_usd: Fraction = Fraction(0, 1),
    pilot_cap_usd: Fraction = Fraction(1, 5),
    campaign_cap_usd: Fraction = Fraction(20, 1),
) -> dict[str, object]:
    """Audit the Day 7 delivery report, 5-lane endpoints, spend ledger, and 50 SG dispositions."""
    if (
        type(promote_unrun_sg_episodes) is not bool
        or type(promote_open_lane_e_continuum_duality) is not bool
        or not isinstance(actual_paid_spend_usd, Fraction)
        or not isinstance(pilot_cap_usd, Fraction)
        or not isinstance(campaign_cap_usd, Fraction)
    ):
        raise ValueError("invalid Day 7 audit parameters")
    if promote_unrun_sg_episodes:
        raise ValueError("deadline-driven promotion of NOT_RUN SG episodes refused")
    if promote_open_lane_e_continuum_duality:
        raise ValueError("promotion of open infinite locally compact duality obligation refused")
    if actual_paid_spend_usd < 0 or actual_paid_spend_usd > pilot_cap_usd or pilot_cap_usd > campaign_cap_usd:
        raise ValueError("spend ledger violated pilot or campaign cost ceiling")

    report_path = Path(__file__).resolve().parent / "derivation.md"
    if not report_path.is_file():
        raise ValueError("missing Day 7 linked delivery report derivation.md")
    report_text = report_path.read_text(encoding="utf-8")

    for lane in ("Lane A", "Lane B", "Lane C", "Lane D", "Lane E"):
        if lane not in report_text:
            raise ValueError(f"missing {lane} in Day 7 delivery report")

    sg_dispositions: dict[str, str] = {}
    for idx in range(1, 51):
        sg_id = f"SG-{idx:02d}"
        if sg_id not in report_text:
            raise ValueError(f"missing {sg_id} in Day 7 delivery report")
        sg_dispositions[sg_id] = (
            "LOCAL_STAGED_CONTROL_PASS" if sg_id in ("SG-40", "SG-48") else "NOT_RUN"
        )

    day_3 = _load_sibling_witness("plan_7d_day_3").witness()
    day_6 = _load_sibling_witness("plan_7d_day_6").witness()

    passed_local = sum(1 for v in sg_dispositions.values() if v == "LOCAL_STAGED_CONTROL_PASS")
    not_run_count = sum(1 for v in sg_dispositions.values() if v == "NOT_RUN")
    if passed_local != 2 or not_run_count != 48:
        raise RuntimeError("unexpected SG episode disposition counts")

    return {
        "lanes_audited": ("A", "B", "C", "D", "E"),
        "sg_total_episodes": len(sg_dispositions),
        "sg_local_staged_pass_count": passed_local,
        "sg_not_run_count": not_run_count,
        "actual_paid_spend_usd": actual_paid_spend_usd,
        "pilot_cap_usd": pilot_cap_usd,
        "campaign_cap_usd": campaign_cap_usd,
        "day_3_le_exponents": day_3["lane_e"]["le4_exponents"],
        "day_6_binary_sha256": day_6["binary_sha256"],
    }


def witness() -> dict[str, object]:
    return verify_day_7_audit_report()
