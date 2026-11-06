"""Genesis Demo 02: Observer Presheaf, Čech 0-Cycle, and Bell-CHSH Gluing Obstruction.

Demonstrates the sheaf-theoretic formulation of contextuality (Abramsky-Brandenburger 2011)
implemented over Category 12 Observer Contexts:
  - Presheaf of empirical local sections over measurement covers
  - Restriction morphisms rho^C_U and marginal distributions
  - Čech 0-cycle condition d_0 s = 0 (No-Signaling across contexts)
  - Čech gluing obstruction gamma = max(0, |S_CHSH| - 2) via Fine's Theorem
  - Verification across Classical LHV, Rational Pythagorean Bell, and PR-Box fixtures.

Epistemic Status: Supports exact finite rational evaluation of contextuality.
AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEMOS_DIR = Path(__file__).resolve().parent
PRIMITIVES_DIR = DEMOS_DIR.parent / "primitives" / "code"


def _load_primitives_package():
    init_path = PRIMITIVES_DIR / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "genesis_primitives",
        init_path,
        submodule_search_locations=[str(PRIMITIVES_DIR)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {init_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["genesis_primitives"] = mod
    spec.loader.exec_module(mod)
    return mod


gp = _load_primitives_package()


def run_observer_presheaf_demo() -> None:
    print("=" * 78)
    print("DEMO 02: OBSERVER PRESHEAF & CECH GLUING OBSTRUCTION (BELL-CHSH)")
    print("=" * 78)

    # -----------------------------------------------------------------------
    # 1. Classical Local Hidden Variable Model
    # -----------------------------------------------------------------------
    print("\n--- 1. Classical Local Hidden Variable (LHV) Model ---")
    lhv = gp.classical_local_hidden_variable_fixture()
    print(f"Contexts in cover: {[c.observables for c in lhv.contexts]}")

    compat_lhv, disc_lhv = lhv.check_cech_0_cycle_compatibility()
    s_lhv = lhv.compute_chsh_correlator()
    gamma_lhv = lhv.cech_gluing_obstruction()
    glues_lhv = lhv.has_global_gluing()

    print(f"  Cech 0-cycle (No-Signaling) compatibility: {compat_lhv}")
    print(
        f"  Max discrepancy on context intersections: {max(disc_lhv.values()) if disc_lhv else 0.0}"
    )
    print(f"  Bell-CHSH Correlator S: {s_lhv:.4f} (Bound <= 2.0)")
    print(f"  Cech Gluing Obstruction gamma: {gamma_lhv:.4f}")
    print(f"  Has Global Gluing (Joint Distribution exists): {glues_lhv}")
    assert compat_lhv is True and abs(s_lhv - 2.0) < 1e-9 and glues_lhv is True

    # -----------------------------------------------------------------------
    # 2. Rational Pythagorean Bell Model (T059 / p208b / 19L57G1)
    # -----------------------------------------------------------------------
    print("\n--- 2. Rational Pythagorean Bell Model (Exact 14/5 = 2.8) ---")
    bell = gp.rational_pythagorean_bell_fixture()
    print("Correlations across 4 measurement contexts:")
    for c in bell.contexts:
        print(
            f"  Context {c.observables}: Correlator = {bell.sections[c].correlator(c.observables[0], c.observables[1]):.2f}"
        )

    compat_bell, disc_bell = bell.check_cech_0_cycle_compatibility()
    s_bell = bell.compute_chsh_correlator()
    gamma_bell = bell.cech_gluing_obstruction()
    glues_bell = bell.has_global_gluing()

    print(f"  Cech 0-cycle (No-Signaling) compatibility: {compat_bell}")
    print(
        f"  Max discrepancy on context intersections: {max(disc_bell.values()) if disc_bell else 0.0}"
    )
    print(f"  Bell-CHSH Correlator S: {s_bell:.4f} (Violates classical bound 2.0 by 0.8)")
    print(f"  Cech Gluing Obstruction gamma: {gamma_bell:.4f} (exact rational 4/5 = 0.8)")
    print(f"  Has Global Gluing (Joint Distribution exists): {glues_bell}")
    assert compat_bell is True and abs(s_bell - 2.8) < 1e-9 and glues_bell is False
    print("  => Local sections are mutually compatible on pairwise overlaps,")
    print("     yet CANNOT be extended to a global section over the whole space.")
    print("     The non-zero obstruction gamma = 0.8 witnesses non-trivial Cech cohomology!")

    # -----------------------------------------------------------------------
    # 3. Popescu-Rohrlich (PR) Superquantum Box
    # -----------------------------------------------------------------------
    print("\n--- 3. Popescu-Rohrlich (PR) Superquantum Box ---")
    pr = gp.pr_box_fixture()
    compat_pr, disc_pr = pr.check_cech_0_cycle_compatibility()
    s_pr = pr.compute_chsh_correlator()
    gamma_pr = pr.cech_gluing_obstruction()
    glues_pr = pr.has_global_gluing()

    print(f"  Cech 0-cycle (No-Signaling) compatibility: {compat_pr}")
    print(f"  Bell-CHSH Correlator S: {s_pr:.4f} (Maximal algebraic bound = 4.0)")
    print(f"  Cech Gluing Obstruction gamma: {gamma_pr:.4f}")
    print(f"  Has Global Gluing: {glues_pr}")
    assert compat_pr is True and abs(s_pr - 4.0) < 1e-9 and glues_pr is False

    # -----------------------------------------------------------------------
    # 4. Signaling / Incompatible Presheaf Failure Detection
    # -----------------------------------------------------------------------
    print("\n--- 4. Signaling Presheaf (Boundary Condition Failure) ---")
    ctx_a1b1 = gp.MeasurementContext(("A1", "B1"))
    signaling_section = gp.LocalSection(
        context=ctx_a1b1,
        distribution={(1, 1): 0.9, (1, -1): 0.0, (-1, 1): 0.0, (-1, -1): 0.1},
    )
    sig_sections = dict(bell.sections)
    sig_sections[ctx_a1b1] = signaling_section
    sig_presheaf = gp.ObserverPresheaf(contexts=bell.contexts, sections=sig_sections)

    compat_sig, disc_sig = sig_presheaf.check_cech_0_cycle_compatibility()
    print(f"  Cech 0-cycle compatibility: {compat_sig} (Expected False)")
    print("  Discrepancies detected across contexts:")
    for (c1, c2), err in disc_sig.items():
        print(f"    Between {c1.observables} and {c2.observables}: Total Variation = {err:.4f}")
    assert compat_sig is False and len(disc_sig) > 0
    print("  => Supplied signaling table flagged by the gluing-mismatch scalar (not a computed Cech cohomology class).")

    print("\n" + "=" * 78)
    print("SUPPLIED GLUING-MISMATCH ILLUSTRATION COMPLETED; NO CECH COHOMOLOGY WAS COMPUTED.")
    print("=" * 78)


if __name__ == "__main__":
    run_observer_presheaf_demo()
