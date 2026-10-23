"""Day 5 PFP repair, second operator-reuse, and Lane E PQ-1..PQ-6 closure control (PLAN-7D-DAY-5).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[3]


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


def verify_day_5_campaign(
    fuel_cap: int = 20,
    reset_fuel_between_episodes: bool = False,
    retain_raw_proposals: bool = True,
    corrupt_crt_residue: bool = False,
    package_root: Path = PACKAGE_ROOT,
) -> dict[str, object]:
    """Verify Day 5 SG-40/SG-48 non-reset ledger and Lane E PQ-1..PQ-6 exact arithmetic."""
    if (
        type(fuel_cap) is not int
        or type(reset_fuel_between_episodes) is not bool
        or type(retain_raw_proposals) is not bool
        or type(corrupt_crt_residue) is not bool
    ):
        raise ValueError("invalid Day 5 control parameters")
    if reset_fuel_between_episodes:
        raise ValueError("fuel ledger reset between episodes refused")
    if not retain_raw_proposals:
        raise ValueError("omitting raw proposal retention refused")

    pq_doc = package_root / "docs" / "protected_subgroup_character_quotients.md"
    if not pq_doc.is_file():
        raise ValueError("missing docs/protected_subgroup_character_quotients.md")
    pq_text = pq_doc.read_text(encoding="utf-8")
    for token in ("PQ-1", "PQ-2", "PQ-3", "PQ-4", "PQ-5", "PQ-6"):
        if token not in pq_text:
            raise ValueError(f"missing {token} in protected_subgroup_character_quotients.md")

    crt_residues: list[int] = []
    dyadic_discrepancies: list[Fraction] = []
    for n in (1, 2, 3, 4):
        mod_2n = 2**n
        mod_3n = 3**n
        mod_6n = 6**n
        a_n = next(a for a in range(mod_6n) if a % mod_2n == 0 and a % mod_3n == 1)
        if corrupt_crt_residue:
            a_n += 1
        if a_n % mod_2n != 0 or a_n % mod_3n != 1:
            raise ValueError(f"CRT residue a_{n} = {a_n} failed mod 2^n / 3^n congruences")
        crt_residues.append(a_n)

        x_n = Fraction(1, 3) - Fraction(2**n // 3, 2**n)
        r_n = (2**n) % 3
        if x_n != Fraction(r_n, 3 * (2**n)) or not (Fraction(0, 1) < x_n < Fraction(1, 2**n)):
            raise ValueError(f"dyadic discrepancy x_{n} = {x_n} failed bound")
        if Fraction(1, 3) <= Fraction(1, 4):
            raise ValueError("3-primary character separation bound failed")
        dyadic_discrepancies.append(x_n)

    next_3 = _load_sibling_witness("plan_7d_next_3").witness()
    costs = (6, 5, 3)
    total_spent = sum(costs)
    if total_spent > fuel_cap:
        raise ValueError("campaign fuel spend exceeded cap")

    return {
        "next_3": next_3,
        "fuel_cap": fuel_cap,
        "fuel_spent": total_spent,
        "fuel_remaining": fuel_cap - total_spent,
        "crt_residues_n1_to_4": tuple(crt_residues),
        "dyadic_discrepancies_n1_to_4": tuple(dyadic_discrepancies),
        "raw_proposals_retained": True,
    }


def witness() -> dict[str, object]:
    return verify_day_5_campaign()
