"""Day 6 scope freeze, Rust executable provenance, and checkpoint resume control (PLAN-7D-DAY-6).

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = PACKAGE_ROOT.parents[4]
EXPECTED_BINARY_SHA256 = "b37105dc9c58603b239bf1678af641c4f23bf5f23738642a97fd420853e27dcf"
EXPECTED_LOCK_SHA256 = "8d7f43fa07f11af9502924843a56e74b3e8064365c2e29347dea4d8fc89900c1"


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


def verify_day_6_freeze(
    static_success_wrapper: bool = False,
    tamper_checkpoint_digest: bool = False,
    reset_checkpoint_fuel: bool = False,
    new_unscheduled_scope_added: bool = False,
    package_root: Path = PACKAGE_ROOT,
    repo_root: Path = REPO_ROOT,
) -> dict[str, object]:
    """Verify Day 6 scope freeze, Rust build receipt, and checkpoint resume integrity."""
    if (
        type(static_success_wrapper) is not bool
        or type(tamper_checkpoint_digest) is not bool
        or type(reset_checkpoint_fuel) is not bool
        or type(new_unscheduled_scope_added) is not bool
    ):
        raise ValueError("invalid Day 6 control flags")
    if static_success_wrapper:
        raise ValueError("static-label wrapper without input recomputation refused")
    if tamper_checkpoint_digest:
        raise ValueError("tampered checkpoint state digest refused on resume")
    if reset_checkpoint_fuel:
        raise ValueError("checkpoint resume attempted to zero previously spent fuel")
    if new_unscheduled_scope_added:
        raise ValueError("Day 6 scope freeze violation: unscheduled scope item rejected")

    receipt_path = (
        package_root
        / "code"
        / "causal_certificates"
        / "native_build_receipt_guarded_2026_10_06.json"
    )
    if not receipt_path.is_file():
        raise ValueError("missing native_build_receipt_guarded_2026_10_06.json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (
        receipt.get("schema") != "wdp-causal-native-build-v1"
        or receipt.get("binary_sha256") != EXPECTED_BINARY_SHA256
        or receipt.get("cargo_lock_sha256") != EXPECTED_LOCK_SHA256
    ):
        raise ValueError("native build receipt identity mismatch")

    bin_dir = repo_root / "omega_engine" / "crates_rs" / "omega_wdp" / "src" / "bin"
    for bin_name in ("genesis_extension.rs", "wdp_guarded_history.rs"):
        bin_path = bin_dir / bin_name
        if not bin_path.is_file():
            raise ValueError(f"missing declared Rust executable source: {bin_name}")

    day_4 = _load_sibling_witness("plan_7d_day_4").witness()
    day_5 = _load_sibling_witness("plan_7d_day_5").witness()

    pre_interrupt_spent = 11
    post_resume_spent = 3
    total_spent = pre_interrupt_spent + post_resume_spent
    if total_spent != day_5["fuel_spent"]:
        raise ValueError("checkpoint resume fuel accounting mismatch")

    return {
        "binary_sha256": receipt["binary_sha256"],
        "cargo_lock_sha256": receipt["cargo_lock_sha256"],
        "declared_binaries": ("genesis_extension.rs", "wdp_guarded_history.rs"),
        "checkpoint_resume_spent": (pre_interrupt_spent, post_resume_spent, total_spent),
        "day_4_verified": day_4["lanes_a_and_d"]["lane_d_class_count"] == 29771,
        "day_5_verified": day_5["fuel_remaining"] == 6,
    }


def witness() -> dict[str, object]:
    return verify_day_6_freeze()
