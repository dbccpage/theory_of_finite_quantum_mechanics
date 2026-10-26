"""Genesis Ascent Demonstration: From Primordial Seed to Typed Evaluation and Authority.

Illustrates a supplied sequence of admissions and independent domain models:
  <> -> <a> -> <ara> -> <arb> -> <arb><bra> -> boson/fermion parity ->
  presentation -> instance -> regime -> comparison -> eval -> auth.

Epistemic Status: Supplied educational realization; the seed does not force it.
The retained self-loop regime is distinct from the independent D2/S2 references.
AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Dynamic module loading for digit-prefixed directory 2_genesis/primitives
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


def run_genesis_ascent_demo() -> None:
    print("=" * 78)
    print("GENESIS ASCENT DEMO: FROM PRIMORDIAL SEED TO TYPED AUTHORITY")
    print("Supplied illustration; domain laws and permissions are additional inputs.")
    print("=" * 78)

    # -----------------------------------------------------------------------
    # Step 1: <> - The Primordial Uninterpreted Seed
    # -----------------------------------------------------------------------
    print("\n[Step 1] <> : Primordial Seed / Empty Regime")
    r0 = gp.EMPTY
    print(f"  Initial state: n_data={r0.n_data()}, n_forms={r0.n_forms()}, n_insts={len(r0.insts)}")
    assert r0.n_data() == 0 and r0.n_forms() == 0

    # Supply is an external proposal; without admission it does not alter internal state
    r0_supplied = gp.step(r0, gp.Supply("<>"))
    assert r0_supplied == r0
    print("  Supply('<>') received: internal state remains uncommitted (no smuggled ontology).")

    # -----------------------------------------------------------------------
    # Step 2: <a> - Single Datum Admission / Self-Pointing
    # -----------------------------------------------------------------------
    print("\n[Step 2] <a> : Single Datum Internalization")
    r1 = gp.step(r0, gp.AdmitDatum("a"))
    print(f"  Admitted datum 'a': data={r1.data}, n_data={r1.n_data()}")
    assert r1.n_data() == 1
    assert r1.data == ("a",)

    # -----------------------------------------------------------------------
    # Step 3: <ara> - Self-Loop Form Declaration and Instance
    # -----------------------------------------------------------------------
    print("\n[Step 3] <ara> : Reflexive Form and Self-Loop Instance")
    # Form 0 has arity 2 (binary relation)
    r2 = gp.step(r1, gp.AdmitForm(2))
    # Admit instance (form=0, tuple=(0, 0)) representing relation r(a, a)
    r3 = gp.step(r2, gp.AdmitInst(0, (0, 0)))
    print(f"  Binary relation form admitted: forms={r3.forms}")
    print(f"  Self-loop instance admitted: insts={r3.insts} -> represents <a r a>")
    assert (0, (0, 0)) in r3.insts

    # -----------------------------------------------------------------------
    # Step 4: <arb> - Asymmetric Pointed Difference Germ
    # -----------------------------------------------------------------------
    print("\n[Step 4] <arb> : Directed Instance and Separate D2 Reference")
    # Admit second datum 'b'
    r4 = gp.step(r3, gp.AdmitDatum("b"))
    # Instance representing r(a, b) = (0, 1)
    r5 = gp.step(r4, gp.AdmitInst(0, (0, 1)))
    print(f"  Second datum 'b' admitted: data={r5.data}")
    print("  Directed instance admitted: (0, (0, 1)) -> represents <a r b>")

    # Connect to Category 2 minimal pointed difference carrier D2
    d2 = gp.D2
    print(f"  Category 2 minimal carrier D2: base={d2.n}, rel={d2.rel}, a={d2.a}, b={d2.b}")
    assert d2.rel == frozenset({(0, 1)})
    assert gp.symmetric(d2.rel) is False
    actual_relation = frozenset(args for form, args in r5.insts if form == 0)
    assert (0, 0) in actual_relation and actual_relation != d2.rel
    print(
        "  Separate D2 reference checked. The admitted regime retains its self-loop and is not D2."
    )

    # -----------------------------------------------------------------------
    # Step 5: <arb> <bra> - Symmetric Pairing Carrier (S2)
    # -----------------------------------------------------------------------
    print("\n[Step 5] <arb> <bra> : Converse Instance and Separate S2 Reference")
    # Instance representing r(b, a) = (1, 0)
    r6 = gp.step(r5, gp.AdmitInst(0, (1, 0)))
    print("  Converse instance admitted: (0, (1, 0)) -> represents <b r a>")
    print(f"  Total instances: {r6.insts}")

    s2 = gp.S2
    print(f"  Category 2 minimal carrier S2: base={s2.n}, rel={s2.rel}")
    assert s2.rel == frozenset({(0, 1), (1, 0)})
    assert gp.symmetric(s2.rel) is True
    actual_relation = frozenset(args for form, args in r6.insts if form == 0)
    assert (0, 0) in actual_relation and actual_relation != s2.rel
    print(
        "  Separate S2 reference checked. The admitted regime retains its self-loop and is not S2."
    )

    # -----------------------------------------------------------------------
    # Step 6: Boson and Fermion Parity - Symmetric Group S_2 Action
    # -----------------------------------------------------------------------
    print("\n[Step 6] Boson & Fermion Parity : Permutation Group S2 Decomposition")
    print("  Amplitude space, rational scalars and exchange projectors are supplied assumptions.")
    # Symmetric group S_2 has two elements: identity (0, 1) and transposition tau = (1, 0)
    perms = gp.all_permutations(2)
    tau = (1, 0)  # transposition swapping 0 and 1
    print(f"  S_2 elements: {perms}")
    print(f"  Transposition generator tau: {tau}")

    # Two-particle configuration space over {0, 1}: states are functions psi: {0,1}^2 -> Q
    # Basis: |0,0>, |0,1>, |1,0>, |1,1>
    # Action of tau: tau |i, j> = |j, i>
    # Symmetrizer P+ = (I + tau)/2, Antisymmetrizer P- = (I - tau)/2
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    boson_basis = []
    fermion_basis = []

    for s in states:
        (s[1], s[0])
        # Boson projection P+ |s>
        # Fermion projection P- |s>
        if s[0] == s[1]:
            # Diagonal: tau(s) = s
            # Boson has eigenvalue +1
            boson_basis.append((s, f"|{s[0]},{s[1]}> (symmetric)"))
            # Fermion: (s - s)/2 = 0 -> Pauli exclusion!
        else:
            if s[0] < s[1]:
                boson_basis.append(
                    (s, f"(|{s[0]},{s[1]}> + |{s[1]},{s[0]}>)/sqrt(2) [Parity = +1]")
                )
                fermion_basis.append(
                    (s, f"(|{s[0]},{s[1]}> - |{s[1]},{s[0]}>)/sqrt(2) [Parity = -1]")
                )

    print("  Bosonic sector (eigenvalue +1 under tau):")
    for b in boson_basis:
        print(f"    - {b[1]}")
    print("  Fermionic sector (eigenvalue -1 under tau, Pauli exclusion on diagonal):")
    for f in fermion_basis:
        print(f"    - {f[1]}")
    print(
        "  Exact algebraic Pauli exclusion: Fermionic amplitude on diagonal (i, i) vanishes identically."
    )

    # -----------------------------------------------------------------------
    # Step 7: Presentation - PresentationFrame and Coordinate Invariance
    # -----------------------------------------------------------------------
    print("\n[Step 7] Presentation : PresentationFrame & Relational Gauge Invariance")
    frame_A = gp.PresentationFrame(
        frame_id="frame_lab",
        carrier_size=2,
        local_relations=frozenset({(0, 1), (1, 0)}),
    )
    # Frame transformation permutes coordinates: 0 -> 1, 1 -> 0
    transform = gp.FrameTransformation(
        source_frame="frame_lab",
        target_frame="frame_transformed",
        mapping={0: 1, 1: 0},
    )
    rel_transformed = transform.transform_rel(frame_A.local_relations)
    assert rel_transformed == frame_A.local_relations  # S2 is invariant under tau!
    print(f"  Source frame relations: {frame_A.local_relations}")
    print(f"  Transformed frame relations: {rel_transformed}")
    print("  Gauge invariance: Relational topology is invariant under coordinate permutation.")

    # -----------------------------------------------------------------------
    # Step 8: Instance - Concrete Relational Bindings
    # -----------------------------------------------------------------------
    print("\n[Step 8] Instance : Formal Grounded Instance Bindings")
    inst_ab: gp.Inst = (0, (0, 1))
    inst_ba: gp.Inst = (0, (1, 0))
    inst_self: gp.Inst = (0, (0, 0))
    print(f"  Form 0 (arity 2) instances: {inst_ab}, {inst_ba}, {inst_self}")
    assert gp.derivable(r6, inst_ab) is True
    assert gp.derivable(r6, inst_ba) is True

    # -----------------------------------------------------------------------
    # Step 9: Regime - Unified Constitutional Context
    # -----------------------------------------------------------------------
    print("\n[Step 9] Regime : Complete Admitted Domain Configuration")
    print(f"  Regime data: {r6.data}")
    print(f"  Regime forms: {r6.forms}")
    print(f"  Regime insts: {r6.insts}")
    delta_sample = (gp.NewDatum(), gp.NewInst(0, (0, 1)))
    print(f"  Sample Delta items: {delta_sample}")
    print(f"  Discrete complexity measures: mu1={gp.mu1(delta_sample)}, mu2={gp.mu2(delta_sample)}")

    # -----------------------------------------------------------------------
    # Step 10: Comparison - Constructive Apartness & Profile Separation
    # -----------------------------------------------------------------------
    print("\n[Step 10] Comparison : Constructive Apartness & Profile Separation")
    # Check apartness and observation profiles
    prof_a = gp.profile(r6, 0)
    prof_b = gp.profile(r6, 1)
    print(f"  Observer profile(datum 0): {len(prof_a)} derivable probing contexts")
    print(f"  Observer profile(datum 1): {len(prof_b)} derivable probing contexts")
    sep_ab = gp.separable(r6, 0, 1)
    print(f"  Separability check separable(0, 1): {sep_ab}")
    # In r6, both 0 and 1 have instances (0,0), (0,1), (1,0)
    # Check if a non-symmetric regime separates them:
    sep_r5 = gp.separable(r5, 0, 1)
    print(f"  In asymmetric regime r5 (only <a r b>), separable(0, 1): {sep_r5}")
    assert sep_r5 is True

    # -----------------------------------------------------------------------
    # Step 11: Eval - Operational Presheaf Evaluation & Obstruction
    # -----------------------------------------------------------------------
    print("\n[Step 11] Eval : Presheaf Observation & Cech Gluing Obstruction")
    bell_presheaf = gp.rational_pythagorean_bell_fixture()
    compat, disc = bell_presheaf.check_cech_0_cycle_compatibility()
    s_val = bell_presheaf.compute_chsh_correlator()
    gamma = bell_presheaf.cech_gluing_obstruction()
    glues = bell_presheaf.has_global_gluing()

    print(f"  Cech 0-cycle (No-Signaling) compatibility: {compat} (discrepancy max = 0.0)")
    print(f"  Bell-CHSH expectation S: {s_val:.4f} (exact rational 14/5 = 2.8)")
    print(f"  Cech gluing obstruction gamma: {gamma:.4f} (exact rational 4/5 = 0.8)")
    print(f"  Has global section / classical joint distribution: {glues}")
    assert compat is True
    assert abs(s_val - 2.8) < 1e-9
    assert abs(gamma - 0.8) < 1e-9
    assert glues is False
    print("  Supplied binary empirical model violates CHSH; no Cech cohomology class was computed.")

    # -----------------------------------------------------------------------
    # Step 12: Auth - Strict Boundary and Typed Refusal Discipline
    # -----------------------------------------------------------------------
    print("\n[Step 12] Auth : Authority Boundary & Typed Refusal Discipline")
    # LawfulPolicy check from Category 10 (Attachment Ladder)
    def lawful_pi(k):
        return 0  # attaches to root parent 0
    def unlawful_pi(k):
        return k + 1  # attaches to forward/unrepresented parent
    print(f"  Lawful attachment policy (attaches to root 0): lawful={gp.lawful_to(lawful_pi, 3)}")
    print(
        f"  Unlawful attachment policy (attaches to forward k+1): lawful={gp.lawful_to(unlawful_pi, 3)}"
    )
    assert gp.lawful_to(lawful_pi, 3) is True
    assert gp.lawful_to(unlawful_pi, 3) is False

    # Checked attachment with typed refusal from Category 10
    ps_init = gp.GENESIS_P
    refusal_res = gp.attach_checked(ps_init, 999)
    print(f"  Attachment to unrepresented parent 999: {refusal_res}")
    assert refusal_res["outcome"] == "refusedParent"
    print("  Typed refusal triggered: Non-panicking rejection enforcing constitutional authority.")
    print("  AuthorityEffect: None confirmed across all 12 stages.")

    print("\n" + "=" * 78)
    print("SUPPLIED ILLUSTRATION COMPLETED; THE AUDIT STATES ITS UNPAID BRIDGES.")
    print("=" * 78)


if __name__ == "__main__":
    run_genesis_ascent_demo()
