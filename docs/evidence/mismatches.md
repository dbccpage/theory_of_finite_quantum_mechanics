# Status and evidence mismatches

Part of the [evidence map](README.md). AuthorityEffect: None. Generated; every flag the grading rules raise is listed. A flag is a report, not a change: no node status was altered.

| Flag | Count |
|---|---|
| `proved_lean_below_e3`: PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt | 0 |
| `proved_lean_external_only`: PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout | 0 |
| `receipt_not_current`: A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit | 33 |
| `computational_no_runnable_test`: COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited | 157 |
| `proved_prose_no_in_repo_document`: PROVED_PROSE with no in-repo source document cited | 4 |
| `broken_reference`: A cited in-repo path or symbol cannot be found in this checkout | 52 |
| `receipt_names_uncited_module`: A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence) | 11 |

## `proved_lean_below_e3` (0)

PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt. Ordered by downstream nodes, most first.

None.

## `proved_lean_external_only` (0)

PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout. Ordered by downstream nodes, most first.

None.

## `receipt_not_current` (33)

A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [FQ-CONTEXTUALITY-CECH-F2](nodes/FQ-CONTEXTUALITY-CECH-F2.md) | FINITE_QM_CORE | `PROVED_LEAN` | E3 | 51 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [DS-QM120-MERMIN-PERES-F2-OBSTRUCTION](nodes/DS-QM120-MERMIN-PERES-F2-OBSTRUCTION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E3 | 50 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](nodes/DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E3 | 48 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [CT-MARLETTO-VEDRAL-2017-SOURCE](nodes/CT-MARLETTO-VEDRAL-2017-SOURCE.md) | CONSTRUCTOR_THEORY | `SOURCE_RECORD` | E1 | 29 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [TFQ-0213](nodes/TFQ-0213.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E1 | 20 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [TFQ-0225](nodes/TFQ-0225.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E1 | 8 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-STONE-CONTINUOUS-TIME](nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md) | FINITE_QM_DYNAMICS | `CONDITIONAL` | E3 | 2 | lean4/U1PhaseSynthesis.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-STONE-CONTINUOUS-TIME](nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md) | FINITE_QM_DYNAMICS | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-STONE-CONTINUOUS-TIME](nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md) | FINITE_QM_DYNAMICS | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-STONE-CONTINUOUS-TIME](nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md) | FINITE_QM_DYNAMICS | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-STONE-CONTINUOUS-TIME](nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md) | FINITE_QM_DYNAMICS | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-STONE-CONTINUOUS-TIME](nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md) | FINITE_QM_DYNAMICS | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1CauchyCircleCompletion.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1CauchyCircleCompletion.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1CayleyProjectiveCircle.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1CayleyProjectiveCircle.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1ChebyshevCauchyBridge.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1ChebyshevCauchyBridge.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1ChebyshevCauchyBridge.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1CyclotomicTorsionTower.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1PhaseSynthesis.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1PhaseSynthesis.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1PhaseSynthesis.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1PythagoreanObstruction.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s) |
| [FQ-TRACE-ZERO-DUALITY-K23](nodes/FQ-TRACE-ZERO-DUALITY-K23.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 2 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [GP-GAP-EXACT-DUALITY](nodes/GP-GAP-EXACT-DUALITY.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 1 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [CT-ENTANGLING-PHASE-FINITE-TARGET](nodes/CT-ENTANGLING-PHASE-FINITE-TARGET.md) | CONSTRUCTOR_THEORY | `PROVED_LEAN` | E3 | 0 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](nodes/DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |
| [TFQ-0316](nodes/TFQ-0316.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 0 | lean4/DualWitness.lean: replay failed against 1 receipt(s) |

## `computational_no_runnable_test` (157)

COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](nodes/PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E3 | 719 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-GS000-EDGEWISE-L1](nodes/L1-GS000-EDGEWISE-L1.md) | L1_EMERGENCE | `COMPUTATIONALLY_CHECKED` | E3 | 469 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-GENESIS-THREE-AXIS-VERDICT](nodes/PGW-GENESIS-THREE-AXIS-VERDICT.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E2 | 126 | 4 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-RUNG0-INHERITANCE-REPLAY](nodes/PGW-RUNG0-INHERITANCE-REPLAY.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E3 | 125 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-FORCED-CENSUS-COLUMN](nodes/PGW-FORCED-CENSUS-COLUMN.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E3 | 111 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM062-U1-SELECTOR-LAYERS](nodes/DS-QM062-U1-SELECTOR-LAYERS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 71 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM063-HOLONOMY-COHERENT-INTENSITY](nodes/DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 56 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM070-PRODUCT-NONFACTORIZATION](nodes/DS-QM070-PRODUCT-NONFACTORIZATION.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 50 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-RUNG2B-STAKE-MENU](nodes/PGW-RUNG2B-STAKE-MENU.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E1 | 44 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0125](nodes/TFQ-0125.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 40 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0126](nodes/TFQ-0126.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 39 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0127](nodes/TFQ-0127.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 38 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0129](nodes/TFQ-0129.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 34 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0013](nodes/TFQ-0013.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 33 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0166](nodes/TFQ-0166.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 32 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0015](nodes/TFQ-0015.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 31 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [COMP-C1-FIRST-SEPARATION-REPLAY](nodes/COMP-C1-FIRST-SEPARATION-REPLAY.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E3 | 30 | 6 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0131](nodes/TFQ-0131.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 30 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0018](nodes/TFQ-0018.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 28 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0019](nodes/TFQ-0019.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 27 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0020](nodes/TFQ-0020.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 26 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0021](nodes/TFQ-0021.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 25 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0022](nodes/TFQ-0022.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 24 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0023](nodes/TFQ-0023.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 23 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0043](nodes/TFQ-0043.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 23 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0024](nodes/TFQ-0024.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 20 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0133](nodes/TFQ-0133.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 20 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0025](nodes/TFQ-0025.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 19 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM073-FINITE-CHSH-AND-PR-BOX](nodes/DS-QM073-FINITE-CHSH-AND-PR-BOX.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 17 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM102-SYNDROME-CAPACITY-BOUND](nodes/DS-QM102-SYNDROME-CAPACITY-BOUND.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 16 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0197](nodes/TFQ-0197.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 16 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM074-NO-SIGNALING-MARGINAL](nodes/DS-QM074-NO-SIGNALING-MARGINAL.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 15 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0028](nodes/TFQ-0028.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 15 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0048](nodes/TFQ-0048.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E0 | 15 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS](nodes/DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 14 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0029](nodes/TFQ-0029.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 14 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0198](nodes/TFQ-0198.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 14 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0030](nodes/TFQ-0030.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 13 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM061-BUILDABILITY-SET-S](nodes/DS-QM061-BUILDABILITY-SET-S.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 12 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM030-UNGRADED-OVERCOUNT](nodes/DS-QM030-UNGRADED-OVERCOUNT.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 9 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0144](nodes/TFQ-0144.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 9 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [AUTH-TC0-TAPE-CONTROL-TYPING](nodes/AUTH-TC0-TAPE-CONTROL-TYPING.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E3 | 8 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM030-GRADED-PATHSUM](nodes/DS-QM030-GRADED-PATHSUM.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 8 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [AUTH-TC2-FINITE-TRANSITION-CONTRACT](nodes/AUTH-TC2-FINITE-TRANSITION-CONTRACT.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E3 | 7 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0146](nodes/TFQ-0146.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 7 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM122-CIRCLE-SELECTOR-BOUNDARY](nodes/L1-QM122-CIRCLE-SELECTOR-BOUNDARY.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 6 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0137](nodes/TFQ-0137.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 6 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](nodes/DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 5 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0147](nodes/TFQ-0147.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 5 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0154](nodes/TFQ-0154.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 5 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM030-TRANSFER-OPERATOR-SHADOW](nodes/DS-QM030-TRANSFER-OPERATOR-SHADOW.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM090-092-AUTHORITY-FIREWALL](nodes/DS-QM090-092-AUTHORITY-FIREWALL.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-DISCRETE-DYNAMICS-DICHOTOMY](nodes/FQ-DISCRETE-DYNAMICS-DICHOTOMY.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-IMPL-REALIFICATION-ADAPTER](nodes/FQ-IMPL-REALIFICATION-ADAPTER.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E3 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-ALPHA-LICENSE-BINDING-M1-M8](nodes/PGW-ALPHA-LICENSE-BINDING-M1-M8.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E1 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0034](nodes/TFQ-0034.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0148](nodes/TFQ-0148.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 4 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM021-IDEMPOTENT-CONDITIONING](nodes/DS-QM021-IDEMPOTENT-CONDITIONING.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-DISCRETE-TIME-STONE-AMBIGUITY](nodes/FQ-DISCRETE-TIME-STONE-AMBIGUITY.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-IMPL-WDP-AMPLITUDE-BRIDGE](nodes/FQ-IMPL-WDP-AMPLITUDE-BRIDGE.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E3 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-U1-TRANSPORT-N-TORSION](nodes/FQ-U1-TRANSPORT-N-TORSION.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0035](nodes/TFQ-0035.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0149](nodes/TFQ-0149.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0172](nodes/TFQ-0172.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 4 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0176](nodes/TFQ-0176.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [DFM-BPHZ-SECTOR-KERNEL](nodes/DFM-BPHZ-SECTOR-KERNEL.md) | DRESSING_FIELD | `COMPUTATIONALLY_CHECKED` | E2 | 2 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [DFM-TREE-CHANGE-GLZ-SYMANZIK-U](nodes/DFM-TREE-CHANGE-GLZ-SYMANZIK-U.md) | DRESSING_FIELD | `COMPUTATIONALLY_CHECKED` | E2 | 2 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](nodes/DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 2 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-CABELLO-FRAME-POLYTOPE-146](nodes/FQ-CABELLO-FRAME-POLYTOPE-146.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-POWER-RULE-P2-SELECTION](nodes/FQ-POWER-RULE-P2-SELECTION.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-SORKIN-READOUT-CLASS-QM208](nodes/FQ-SORKIN-READOUT-CLASS-QM208.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-TRACE-ZERO-DUALITY-K23](nodes/FQ-TRACE-ZERO-DUALITY-K23.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM020-THM6-P1-SCOPE-FENCE](nodes/L1-QM020-THM6-P1-SCOPE-FENCE.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0036](nodes/TFQ-0036.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0045](nodes/TFQ-0045.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E0 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0049](nodes/TFQ-0049.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0134](nodes/TFQ-0134.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0150](nodes/TFQ-0150.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0189](nodes/TFQ-0189.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM032-FINITE-FEYNMAN-SHADOW](nodes/DS-QM032-FINITE-FEYNMAN-SHADOW.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO](nodes/DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-BELL-RATIONAL-VIOLATION-14-5](nodes/FQ-BELL-RATIONAL-VIOLATION-14-5.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-BUSCH-EFFECT-FRAME](nodes/FQ-BUSCH-EFFECT-FRAME.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [GP-GAP-EXACT-DUALITY](nodes/GP-GAP-EXACT-DUALITY.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM020-THM7-REPRESENTATION-CAPACITY](nodes/L1-QM020-THM7-REPRESENTATION-CAPACITY.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM122-BORN-PAIRING-NONUNIQUE](nodes/L1-QM122-BORN-PAIRING-NONUNIQUE.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [MUB6-PRODUCT-TRIPLE-LOWER-BOUND](nodes/MUB6-PRODUCT-TRIPLE-LOWER-BOUND.md) | MUTUALLY_UNBIASED_BASES | `COMPUTATIONALLY_CHECKED` | E2 | 1 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0037](nodes/TFQ-0037.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0046](nodes/TFQ-0046.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0138](nodes/TFQ-0138.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0140](nodes/TFQ-0140.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0151](nodes/TFQ-0151.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0155](nodes/TFQ-0155.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0160](nodes/TFQ-0160.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0193](nodes/TFQ-0193.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 5 in-repo Rust or Python symbol(s) cited, none a test |
| [AUTHF-REPLAY-SUBSTITUTIONS](nodes/AUTHF-REPLAY-SUBSTITUTIONS.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM032-CONTINUUM-LIMIT-CONDITIONAL](nodes/DS-QM032-CONTINUUM-LIMIT-CONDITIONAL.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS](nodes/DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM041-HEISENBERG-PICTURE-FINITE](nodes/DS-QM041-HEISENBERG-PICTURE-FINITE.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM064-074-083-ANNEX-REDIRECT-ROWS](nodes/DS-QM064-074-083-ANNEX-REDIRECT-ROWS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](nodes/DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM093-SURVIVAL-THEOREM](nodes/DS-QM093-SURVIVAL-THEOREM.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM094-EVERETT-RELATIVE-STATE-CONTACT](nodes/DS-QM094-EVERETT-RELATIVE-STATE-CONTACT.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM206-BOUNDARY-SYNTHESIS](nodes/DS-QM206-BOUNDARY-SYNTHESIS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM207-211-FIVE-IMPORT-CASCADE](nodes/DS-QM207-211-FIVE-IMPORT-CASCADE.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY](nodes/FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-GAP-REAL-EMBEDDING-CHOICE](nodes/FQ-GAP-REAL-EMBEDDING-CHOICE.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-IMPL-PAIRING-AUDIT](nodes/FQ-IMPL-PAIRING-AUDIT.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED](nodes/FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-QM207-231-FINITE-MAP-CONTROLS](nodes/FQ-QM207-231-FINITE-MAP-CONTROLS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-TSIRELSON-SOS-Q-SQRT2](nodes/FQ-TSIRELSON-SOS-Q-SQRT2.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-OPERATOR-LIFT-TRACE-EMBED-013](nodes/L1-OPERATOR-LIFT-TRACE-EMBED-013.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM003-C17-COMPOSABLE-FACTORIZATION](nodes/L1-QM003-C17-COMPOSABLE-FACTORIZATION.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM020-THM3-ROW-SPARSITY](nodes/L1-QM020-THM3-ROW-SPARSITY.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM020-THM5-PHASE-AVERAGED-SHADOW](nodes/L1-QM020-THM5-PHASE-AVERAGED-SHADOW.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [L1-QM121-LADDER-RUNGS-2-6](nodes/L1-QM121-LADDER-RUNGS-2-6.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [MUB6-SZOLLOSI-FULLBOX-UNRESOLVED](nodes/MUB6-SZOLLOSI-FULLBOX-UNRESOLVED.md) | MUTUALLY_UNBIASED_BASES | `COMPUTATIONALLY_CHECKED` | E3 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS](nodes/MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS.md) | MUTUALLY_UNBIASED_BASES | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [PG-GEN-SAMENESS-REFINEMENTS](nodes/PG-GEN-SAMENESS-REFINEMENTS.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-PFP-C4-CERTIFICATE](nodes/PGW-PFP-C4-CERTIFICATE.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0041](nodes/TFQ-0041.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0047](nodes/TFQ-0047.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0051](nodes/TFQ-0051.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0128](nodes/TFQ-0128.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0130](nodes/TFQ-0130.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0132](nodes/TFQ-0132.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0135](nodes/TFQ-0135.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0136](nodes/TFQ-0136.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0139](nodes/TFQ-0139.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0141](nodes/TFQ-0141.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0142](nodes/TFQ-0142.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0143](nodes/TFQ-0143.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0145](nodes/TFQ-0145.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0152](nodes/TFQ-0152.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0153](nodes/TFQ-0153.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0156](nodes/TFQ-0156.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0157](nodes/TFQ-0157.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0158](nodes/TFQ-0158.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0159](nodes/TFQ-0159.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0161](nodes/TFQ-0161.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0162](nodes/TFQ-0162.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0163](nodes/TFQ-0163.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0164](nodes/TFQ-0164.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0165](nodes/TFQ-0165.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0168](nodes/TFQ-0168.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0169](nodes/TFQ-0169.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0170](nodes/TFQ-0170.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0173](nodes/TFQ-0173.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0174](nodes/TFQ-0174.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 5 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0175](nodes/TFQ-0175.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0178](nodes/TFQ-0178.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0180](nodes/TFQ-0180.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0182](nodes/TFQ-0182.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0187](nodes/TFQ-0187.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0190](nodes/TFQ-0190.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0194](nodes/TFQ-0194.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0196](nodes/TFQ-0196.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 5 in-repo Rust or Python symbol(s) cited, none a test |

## `proved_prose_no_in_repo_document` (4)

PROVED_PROSE with no in-repo source document cited. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PGW-SN-E18-L1-TIES-L2-CENTER](nodes/PGW-SN-E18-L1-TIES-L2-CENTER.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E19-TORSION-ERASED-OVER-Q](nodes/PGW-SN-E19-TORSION-ERASED-OVER-Q.md) | MSSN_SN | `PROVED_PROSE` | E2 | 0 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E20-OBSERVER-COMPLETION](nodes/PGW-SN-E20-OBSERVER-COMPLETION.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E21-REPAIR-RANK](nodes/PGW-SN-E21-REPAIR-RANK.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |

## `broken_reference` (52)

A cited in-repo path or symbol cannot be found in this checkout. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-PRIMDIFF-AXIOMS](nodes/PG-PRIMDIFF-AXIOMS.md) | PREGENESIS | `DEFINITION` | E3 | 508 | path not found: code/python/src/majorana/tests/unit/test_primitive_difference.py |
| [TFQ-0125](nodes/TFQ-0125.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 40 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/finite_qm_engine.py |
| [TFQ-0127](nodes/TFQ-0127.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 38 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/operational_axiom_selection.py |
| [TFQ-0129](nodes/TFQ-0129.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 34 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/born_normalization.py |
| [TFQ-0320](nodes/TFQ-0320.md) | FINITE_OBSTRUCTION | `SOURCE_RECORD` | E0 | 32 | path not found: code/python/src/majorana/tests/unit/test_primitive_difference.py |
| [TFQ-0131](nodes/TFQ-0131.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 30 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0206](nodes/TFQ-0206.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E1 | 27 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0207](nodes/TFQ-0207.md) | ENGINE_CUSTODY | `OPEN` | E1 | 26 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0208](nodes/TFQ-0208.md) | ENGINE_CUSTODY | `OPEN` | E0 | 25 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0215](nodes/TFQ-0215.md) | ENGINE_CUSTODY | `OPEN` | E1 | 18 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channel.py |
| [TFQ-0144](nodes/TFQ-0144.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 9 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/busch_effects.py |
| [TFQ-0146](nodes/TFQ-0146.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 7 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channel.py |
| [TFQ-0226](nodes/TFQ-0226.md) | ENGINE_CUSTODY | `OPEN` | E1 | 7 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0137](nodes/TFQ-0137.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 6 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/discrete_dynamics.py |
| [TFQ-0147](nodes/TFQ-0147.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 5 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channels_stinespring.py |
| [TFQ-0149](nodes/TFQ-0149.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 3 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/simplicial_complex_qm.py |
| [TFQ-0176](nodes/TFQ-0176.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 3 | path not found: code/python/src/mub/mub_verify/a1_collar_swarm.py |
| [TFQ-0230](nodes/TFQ-0230.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E1 | 3 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.CauchyCircleCompletion.RegPhaseSeq.add_assoc_equiv not found in lean4/U1CauchyCircleCompletion.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.CauchyCircleCompletion.quad_half_angle_squares_to_u345 not found in lean4/U1CauchyCircleCompletion.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.pureProjector_born_pairing not found in lean4/U1ChebyshevCauchyBridge.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.ChebyshevCauchyBridge.circleRatPow_eq_chebyshev not found in lean4/U1ChebyshevCauchyBridge.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.ChebyshevCauchyBridge.taylor_circle_norm_defect_identity not found in lean4/U1ChebyshevCauchyBridge.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.CyclotomicTorsionTower.ratPhaseQuot_divisible not found in lean4/U1CyclotomicTorsionTower.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.PhaseSynthesis.u1_phase_completion_synthesis not found in lean4/U1PhaseSynthesis.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.QuadraticTowerAndCayleyStone.chebT2Pow_succ not found in lean4/U1QuadraticTowerAndCayleyStone.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E3 | 2 | symbol U1Finite.QuadraticTowerAndCayleyStone.u345_k2_double_angle_recovery not found in lean4/U1QuadraticTowerAndCayleyStone.lean |
| [TFQ-0177](nodes/TFQ-0177.md) | IMPLEMENTATION_SIBLING | `OPEN` | E1 | 2 | path not found: code/python/src/mub/mub_verify/a1_collar_swarm.py |
| [TFQ-0231](nodes/TFQ-0231.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E0 | 2 | path not found: code/python/src/majorana/tests/support/domain/shared_kernel/obstruction.py |
| [TFQ-0138](nodes/TFQ-0138.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/dynamics_dichotomy.py |
| [TFQ-0138](nodes/TFQ-0138.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/heisenberg_representation_uniqueness.py |
| [TFQ-0140](nodes/TFQ-0140.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/continuous_time_locality_limit.py |
| [TFQ-0140](nodes/TFQ-0140.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/norm_approximation_frontier.py |
| [TFQ-0151](nodes/TFQ-0151.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/discrete_walk_engines.py |
| [TFQ-0315](nodes/TFQ-0315.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [L1-QM121-LADDER-RUNGS-2-6](nodes/L1-QM121-LADDER-RUNGS-2-6.md) | L1_TO_L2 | `COMPUTATIONALLY_CHECKED` | E3 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0130](nodes/TFQ-0130.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/higher_dim_entanglement.py |
| [TFQ-0130](nodes/TFQ-0130.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/quantum_protocols.py |
| [TFQ-0135](nodes/TFQ-0135.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/contextuality_f2.py |
| [TFQ-0135](nodes/TFQ-0135.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/mermin_peres.py |
| [TFQ-0136](nodes/TFQ-0136.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/quantum_correlation.py |
| [TFQ-0136](nodes/TFQ-0136.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/tensor_commuting_correlation_frontier.py |
| [TFQ-0152](nodes/TFQ-0152.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/stabilizer_codes.py |
| [TFQ-0159](nodes/TFQ-0159.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/composition_tensor_mub.py |
| [TFQ-0162](nodes/TFQ-0162.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/branch_finegraining.py |
| [TFQ-0162](nodes/TFQ-0162.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/everett_tree.py |
| [TFQ-0163](nodes/TFQ-0163.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cancellation_certificates.py |
| [TFQ-0163](nodes/TFQ-0163.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/interference.py |
| [TFQ-0165](nodes/TFQ-0165.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/tower_topological_completion.py |
| [TFQ-0182](nodes/TFQ-0182.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/majorana/core/gf2_diagnostic.py |
| [TFQ-0289](nodes/TFQ-0289.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0316](nodes/TFQ-0316.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |

## `receipt_names_uncited_module` (11)

A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence). Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-INERT-DIAMOND](nodes/PG-INERT-DIAMOND.md) | PREGENESIS | `DEFINITION` | E3 | 811 | a replay receipt names this node for lean4/InertDiamond.lean, but the node's lean, rust and source fields do not cite it |
| [PG-SIX-OPERATIONS](nodes/PG-SIX-OPERATIONS.md) | PREGENESIS | `DEFINITION` | E3 | 789 | a replay receipt names this node for lean4/SixOperations.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](nodes/PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) | WDP | `OPEN` | E3 | 513 | a replay receipt names this node for lean4/WdpBridgeObligations.lean, but the node's lean, rust and source fields do not cite it |
| [PG-PRIMDIFF-AXIOMS](nodes/PG-PRIMDIFF-AXIOMS.md) | PREGENESIS | `DEFINITION` | E3 | 508 | a replay receipt names this node for lean4/PrimdiffAxioms.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-DEGREE1-WINDOW](nodes/PG-WDP-DEGREE1-WINDOW.md) | WDP | `DEFINITION` | E3 | 507 | a replay receipt names this node for lean4/WdpDegree1Window.lean, but the node's lean, rust and source fields do not cite it |
| [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](nodes/L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) | L1_TO_L2 | `CONDITIONAL` | E3 | 468 | a replay receipt names this node for lean4/ResidualSectorWeights.lean, but the node's lean, rust and source fields do not cite it |
| [PG-ROOT-DIFF-STRUCTURE](nodes/PG-ROOT-DIFF-STRUCTURE.md) | PREGENESIS | `ADMITTED_PRIMITIVE` | E3 | 263 | a replay receipt names this node for lean4/RootDiffStructure.lean, but the node's lean, rust and source fields do not cite it |
| [FSP-WILSON-DIRAC-GAMMA5](nodes/FSP-WILSON-DIRAC-GAMMA5.md) | FERMION_SIGN | `IMPORTED_ASSUMPTION` | E3 | 22 | a replay receipt names this node for lean4/FermionSignWilsonDiracGamma5.lean, but the node's lean, rust and source fields do not cite it |
| [L1-WDP-REALIFICATION-J](nodes/L1-WDP-REALIFICATION-J.md) | L1_TO_L2 | `DEFINITION` | E3 | 5 | a replay receipt names this node for lean4/RealificationJ.lean, but the node's lean, rust and source fields do not cite it |
| [L1-U1-SELECTOR-OTHER-SEGMENT](nodes/L1-U1-SELECTOR-OTHER-SEGMENT.md) | L1_TO_L2 | `OPEN` | E3 | 0 | a replay receipt names this node for lean4/U1SelectorSegment.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-DIAGNOSTIC-NOT-ROUTING](nodes/PG-WDP-DIAGNOSTIC-NOT-ROUTING.md) | WDP | `DEFINITION` | E3 | 0 | a replay receipt names this node for lean4/WdpDiagnosticRouting.lean, but the node's lean, rust and source fields do not cite it |

