# S(n) Tower Architecture Code & Verification Harness

**AuthorityEffect:** None.

## Overview

This directory provides the canonical Python source models and test suites for the S(n) tower. The curriculum notebooks they accompanied were retired on 2026-10-06.

The Python models formalize the internal algebraic shadow and pedagogical laboratories across four distinct layers:

1. **Core Stages ($S(0)$ through $S(6)$)**: Ground inertia, lone mark subsingleton collapse, symmetric permutation retention, cost-2 separation floors, complete graph orbit closures, external continuation demand, and section lift/retraction descent identities ($\rho_N \circ \alpha_N = \operatorname{id}$).
2. **Formal Mathematical Realizations**: Simplicial boundary complexes ($\partial^2 = 0$), bounded quantifier $\Delta_0$ evaluation, 2-polygraph confluence rewrites, monadic adjunctions ($F \dashv G$), dagger categories, de Bruijn shift dynamics, RGB epistemic quarantine, filtered ind-objects, discrete Hodge decomposition, and autopoietic read-only reflection.
3. **Downstream Domain Applications**: Topological relational join pullbacks, dual-channel linear session protocols, Third Layer Law boundary enforcement, discrete Regge metric Gram positive-definiteness ($G > 0$), and 4D hinge deficit angles.
4. **Verification Machinery (Layer 4)**: Bounded Quantifier Alternation Monitors ($k \le 12$), DDA 14-tuple event ledgers with fuel conservation, Kleene 3-valued truth logic ($0, 1, 2$), and the Layer 4 RGB Tripartite Authority Separation Firewall.

---

## Module Layout

| File | Purpose | Primary Exports |
| :--- | :--- | :--- |
| [`sn_core.py`](sn_core.py) | Track 000 Core Stages | `S0Ground`, `S1Supply`, `S2Collapse`, `S3Separation`, `S4Orbit`, `S5Continuation`, `S6Descent` |
| [`sn_realizations.py`](sn_realizations.py) | Track 010 Realizations | `Simplex1`, `Simplicial1Skeleton`, `irreflexive_cut`, `bounded_forall`, `bounded_exists`, `Polygraph2`, `AdjunctionCochain`, `DaggerArrow`, `debruijn_shift`, `authority_filter`, `RGBChannel`, `FilteredIndObject`, `DialectProjection`, `DiscreteHodge`, `HashimotoGraph`, `AutopoieticAudit` |
| [`sn_applications.py`](sn_applications.py) | Track 020 Applications | `topological_relational_join`, `SessionChannel`, `DownstreamApplication`, `ReggeMetric`, `ReggeCurvature` |
| [`sn_verification.py`](sn_verification.py) | Track 030 Verification | `AlternationMonitor`, `DDAEventRecord`, `Kleene3Logic`, `VerificationRGBFirewall` |
| [`check_sn.py`](check_sn.py) | Grammar Conformance | EBNF grammar recognizer verifying `sn.ebnf` against test cases |
| [`tests/`](tests/) | Unit & Conformance Tests | Targeted pytest suites for all models and grammar |

---

## Verification CLI Commands

All commands are pinned to Python 3.12 under Windows (`py -3.12`).

### Run Targeted Pytest Suites

```bash
# Run S(n) core models test suite
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_core.py

# Run S(n) mathematical realizations test suite
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_realizations.py

# Run downstream applications test suite
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_applications.py

# Run Layer 4 verification test suite
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_verification.py

# Run EBNF grammar conformance test suite
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_grammar.py
```

---

## Pedagogical & Claim Discipline Invariants

1. **AuthorityEffect:** `None.`
2. **Non-Conflation Fences:**
   - Realization $\neq$ Genesis extension
   - Application $\neq$ Realization
   - Verification $\neq$ Genesis authority
   - $\rho_N \circ \alpha_N = \operatorname{id}$ (Section retraction identity)
3. **Epistemic Classifications:** All assertions in this package represent bounded computational checks and formal models within toy settings.
