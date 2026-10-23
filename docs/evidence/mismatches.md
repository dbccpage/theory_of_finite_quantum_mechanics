# Status and evidence mismatches

Part of the [evidence map](README.md). AuthorityEffect: None. Generated; every flag the grading rules raise is listed. A flag is a report, not a change: no node status was altered.

| Flag | Count |
|---|---|
| `proved_lean_below_e3`: PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt | 219 |
| `proved_lean_external_only`: PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout | 53 |
| `receipt_not_current`: A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit | 0 |
| `computational_no_runnable_test`: COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited | 126 |
| `proved_prose_no_in_repo_document`: PROVED_PROSE with no in-repo source document cited | 13 |
| `broken_reference`: A cited in-repo path or symbol cannot be found in this checkout | 55 |
| `receipt_names_uncited_module`: A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence) | 27 |

## `proved_lean_below_e3` (219)

PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-GEN-SUPPLY-NO-OP](nodes/PG-GEN-SUPPLY-NO-OP.md) | GENESIS | `PROVED_LEAN` | E0 | 690 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PG-GEN-NO-RETURN](nodes/PG-GEN-NO-RETURN.md) | GENESIS | `PROVED_LEAN` | E0 | 660 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [L1-GS000-EDGEWISE-L1](nodes/L1-GS000-EDGEWISE-L1.md) | L1_EMERGENCE | `PROVED_LEAN` | E2 | 462 | grade E2; 6 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](nodes/L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 144 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [PGW-POLICY-ENDPOINT-ALL-SEPARATED](nodes/PGW-POLICY-ENDPOINT-ALL-SEPARATED.md) | GENESIS | `PROVED_LEAN` | E0 | 135 | grade E0; 1 Lean reference(s) cited, 0 in this checkout |
| [PG-GEN-IRREFLEXIVE-DISTINCT](nodes/PG-GEN-IRREFLEXIVE-DISTINCT.md) | GENESIS | `PROVED_LEAN` | E0 | 115 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-C2-RUN-FORWARD-EVERY-HISTORY](nodes/PGW-C2-RUN-FORWARD-EVERY-HISTORY.md) | GENESIS | `PROVED_LEAN` | E0 | 110 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [FQ-PRIMDIFF-QUOTIENT-KERNEL](nodes/FQ-PRIMDIFF-QUOTIENT-KERNEL.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 99 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [DS-QM060-SUPERPOSITION-QUOTIENT-FIBER](nodes/DS-QM060-SUPERPOSITION-QUOTIENT-FIBER.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 68 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](nodes/DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 67 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [GP-FIN-GAUSS-MATRIX-ALGEBRA](nodes/GP-FIN-GAUSS-MATRIX-ALGEBRA.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 67 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS](nodes/PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md) | GENESIS | `PROVED_LEAN` | E0 | 57 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [FQ-CABELLO-NO-INTEGER-FRAME](nodes/FQ-CABELLO-NO-INTEGER-FRAME.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 56 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [DS-QM063-HOLONOMY-COHERENT-INTENSITY](nodes/DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 55 | grade E2; 6 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [FQ-CONTEXTUALITY-CECH-F2](nodes/FQ-CONTEXTUALITY-CECH-F2.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 51 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [PG-GEN-ONGOING-OBSTRUCTION](nodes/PG-GEN-ONGOING-OBSTRUCTION.md) | GENESIS | `PROVED_LEAN` | E0 | 51 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [DS-QM070-PRODUCT-NONFACTORIZATION](nodes/DS-QM070-PRODUCT-NONFACTORIZATION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 50 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM120-MERMIN-PERES-F2-OBSTRUCTION](nodes/DS-QM120-MERMIN-PERES-F2-OBSTRUCTION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 50 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [PG-GEN-ONGOING-FEWEST-CHANGES](nodes/PG-GEN-ONGOING-FEWEST-CHANGES.md) | GENESIS | `PROVED_LEAN` | E0 | 49 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](nodes/DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 48 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [DS-QM212-MAJORANA-PROBLEM](nodes/DS-QM212-MAJORANA-PROBLEM.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 48 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](nodes/MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 47 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [PGW-D2-INITIAL-POINTED](nodes/PGW-D2-INITIAL-POINTED.md) | GENESIS | `PROVED_LEAN` | E0 | 46 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD](nodes/PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD.md) | GENESIS | `PROVED_LEAN` | E0 | 41 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN0-GROUND-INERTIA](nodes/PGW-SN0-GROUND-INERTIA.md) | MSSN_SN | `PROVED_LEAN` | E0 | 33 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN1-SUPPLY-NOT-ADMISSION](nodes/PGW-SN1-SUPPLY-NOT-ADMISSION.md) | MSSN_SN | `PROVED_LEAN` | E0 | 32 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN2-OPAQUE-COLLAPSE](nodes/PGW-SN2-OPAQUE-COLLAPSE.md) | MSSN_SN | `PROVED_LEAN` | E0 | 31 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN3-COST-TWO-UNARY-MARK](nodes/PGW-SN3-COST-TWO-UNARY-MARK.md) | MSSN_SN | `PROVED_LEAN` | E0 | 30 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [L1-QM020-THM1-DIRECT-NORMALIZATION](nodes/L1-QM020-THM1-DIRECT-NORMALIZATION.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 26 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [COMP-C1-CANONICAL-SEPARATED-ALPHABET](nodes/COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) | COMPUTATION | `PROVED_LEAN` | E2 | 25 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [PGW-GO-REACH-CEILING](nodes/PGW-GO-REACH-CEILING.md) | GENESIS | `PROVED_LEAN` | E0 | 25 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-GO-CONTRACTION-STEP2-STEP3](nodes/PGW-GO-CONTRACTION-STEP2-STEP3.md) | GENESIS | `PROVED_LEAN` | E0 | 24 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-GO-MULTIPLICITY-MONOTONE](nodes/PGW-GO-MULTIPLICITY-MONOTONE.md) | GENESIS | `PROVED_LEAN` | E0 | 23 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY](nodes/FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 22 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [PGW-GO-TWO-RELATIONS-SWAP](nodes/PGW-GO-TWO-RELATIONS-SWAP.md) | GENESIS | `PROVED_LEAN` | E0 | 22 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [FQ-COMMUTATOR-TRACE-OBSTRUCTION](nodes/FQ-COMMUTATOR-TRACE-OBSTRUCTION.md) | FINITE_QM_DYNAMICS | `PROVED_LEAN` | E2 | 21 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [PG-GEN-REWRITING-COMMUTATION](nodes/PG-GEN-REWRITING-COMMUTATION.md) | GENESIS | `PROVED_LEAN` | E2 | 21 | grade E2; 6 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](nodes/DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 20 | grade E2; 4 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION](nodes/FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 20 | grade E2; 9 Lean reference(s) cited, 9 in this checkout (replay: none 9) |
| [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](nodes/L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 19 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](nodes/PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) | MSSN_SN | `PROVED_LEAN` | E0 | 18 | grade E0; 5 Lean reference(s) cited, 0 in this checkout |
| [DS-QM073-FINITE-CHSH-AND-PR-BOX](nodes/DS-QM073-FINITE-CHSH-AND-PR-BOX.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 17 | grade E2; 5 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [DS-QM102-SYNDROME-CAPACITY-BOUND](nodes/DS-QM102-SYNDROME-CAPACITY-BOUND.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 16 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [COMP-C5-TM0-STEP-SIMULATION](nodes/COMP-C5-TM0-STEP-SIMULATION.md) | COMPUTATION | `PROVED_LEAN` | E2 | 15 | grade E2; 7 Lean reference(s) cited, 7 in this checkout (replay: none 7) |
| [DS-QM074-NO-SIGNALING-MARGINAL](nodes/DS-QM074-NO-SIGNALING-MARGINAL.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 15 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS](nodes/DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 14 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-FIXED-TRIPLE-VARIETY](nodes/MUB6-FIXED-TRIPLE-VARIETY.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 14 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [CQFT-FINITE-STRICT-POSET-SPACELIKE](nodes/CQFT-FINITE-STRICT-POSET-SPACELIKE.md) | CAUSAL_QFT | `PROVED_LEAN` | E2 | 13 | grade E2; 10 Lean reference(s) cited, 10 in this checkout (replay: none 10) |
| [COMP-C5-CLOSURES-HALTING](nodes/COMP-C5-CLOSURES-HALTING.md) | COMPUTATION | `PROVED_LEAN` | E2 | 12 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [MUB6-SZOLLOSI-TWO-CIRCULANT](nodes/MUB6-SZOLLOSI-TWO-CIRCULANT.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 12 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [COMP-C6-EVAL-HAS-A-CODE](nodes/COMP-C6-EVAL-HAS-A-CODE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 10 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-PHASE-FIBER-QUOTIENT](nodes/FQ-PHASE-FIBER-QUOTIENT.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 10 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-TENSOR-LU-RIVAL-EXCLUSION](nodes/FQ-TENSOR-LU-RIVAL-EXCLUSION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 10 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [COMP-C6-TM2-OUTPUT-FORM](nodes/COMP-C6-TM2-OUTPUT-FORM.md) | COMPUTATION | `PROVED_LEAN` | E2 | 9 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [COMP-C6-TM0-HALTING-EQUIVALENCE](nodes/COMP-C6-TM0-HALTING-EQUIVALENCE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 8 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [PGW-GO-LEFTOVER-UNBOUNDEDNESS](nodes/PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) | GENESIS | `PROVED_LEAN` | E0 | 8 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION](nodes/MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION.md) | MAJORANA | `PROVED_LEAN` | E2 | 7 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [MUB6-MOMENT-EVALUATION-FLAT](nodes/MUB6-MOMENT-EVALUATION-FLAT.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 7 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [L1-QM122-CIRCLE-SELECTOR-BOUNDARY](nodes/L1-QM122-CIRCLE-SELECTOR-BOUNDARY.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 6 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [MUB6-SZOLLOSI-618-SYSTEM](nodes/MUB6-SZOLLOSI-618-SYSTEM.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 6 | grade E2; 7 Lean reference(s) cited, 7 in this checkout (replay: none 7) |
| [AUTHF-CLASS-RELATIVE-TRANSPORT](nodes/AUTHF-CLASS-RELATIVE-TRANSPORT.md) | COMPUTATION | `PROVED_LEAN` | E2 | 5 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](nodes/DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 5 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [PGW-COLLAPSE-WITHOUT-INSTANCES](nodes/PGW-COLLAPSE-WITHOUT-INSTANCES.md) | GENESIS | `PROVED_LEAN` | E0 | 5 | grade E0; 1 Lean reference(s) cited, 0 in this checkout |
| [PGW-GO-H1-CANCELLATION-EXCESS](nodes/PGW-GO-H1-CANCELLATION-EXCESS.md) | GENESIS | `PROVED_LEAN` | E0 | 5 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN-E12-CIRCULATION-FUNCTIONAL](nodes/PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) | MSSN_SN | `PROVED_LEAN` | E0 | 5 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](nodes/QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 5 | grade E2; 10 Lean reference(s) cited, 10 in this checkout (replay: none 10) |
| [AUTH-DTM1-TOKEN-CODE-ROUNDTRIP](nodes/AUTH-DTM1-TOKEN-CODE-ROUNDTRIP.md) | COMPUTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [AUTH-G5A-CLASS-RELATIVE-TRANSPORT](nodes/AUTH-G5A-CLASS-RELATIVE-TRANSPORT.md) | COMPUTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [COMP-C3-BOUNDED-REACH-DECIDABLE](nodes/COMP-C3-BOUNDED-REACH-DECIDABLE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [COMP-C7-MACHINE-HALTING-UNDECIDABLE](nodes/COMP-C7-MACHINE-HALTING-UNDECIDABLE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [FQ-DISCRETE-DYNAMICS-DICHOTOMY](nodes/FQ-DISCRETE-DYNAMICS-DICHOTOMY.md) | FINITE_QM_DYNAMICS | `PROVED_LEAN` | E2 | 4 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-IMPL-REALIFICATION-ADAPTER](nodes/FQ-IMPL-REALIFICATION-ADAPTER.md) | IMPLEMENTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-GLUING-G3-OPAQUE](nodes/MUB6-GLUING-G3-OPAQUE.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 4 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED](nodes/PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED.md) | GENESIS | `PROVED_LEAN` | E0 | 4 | grade E0; 5 Lean reference(s) cited, 0 in this checkout |
| [PGW-GO-H2-STATE-RAISING-GAUGE](nodes/PGW-GO-H2-STATE-RAISING-GAUGE.md) | GENESIS | `PROVED_LEAN` | E0 | 4 | grade E0; 5 Lean reference(s) cited, 0 in this checkout |
| [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](nodes/PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) | GENESIS | `PROVED_LEAN` | E0 | 4 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [QCV-CONCATENATION-THRESHOLD-DICHOTOMY](nodes/QCV-CONCATENATION-THRESHOLD-DICHOTOMY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 9 Lean reference(s) cited, 9 in this checkout (replay: none 9) |
| [QCV-NET-RATE-BACKLOG-DICHOTOMY](nodes/QCV-NET-RATE-BACKLOG-DICHOTOMY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 4 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [COMP-C7-NF-REACH-UNDECIDABLE](nodes/COMP-C7-NF-REACH-UNDECIDABLE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 3 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [DFM-BOOST-PLANE-LEAN](nodes/DFM-BOOST-PLANE-LEAN.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 3 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DFM-JARLSKOG-QUARTET-INVARIANCE](nodes/DFM-JARLSKOG-QUARTET-INVARIANCE.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 3 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [FQ-DISCRETE-TIME-STONE-AMBIGUITY](nodes/FQ-DISCRETE-TIME-STONE-AMBIGUITY.md) | FINITE_QM_DYNAMICS | `PROVED_LEAN` | E2 | 3 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-IMPL-WDP-AMPLITUDE-BRIDGE](nodes/FQ-IMPL-WDP-AMPLITUDE-BRIDGE.md) | IMPLEMENTATION | `PROVED_LEAN` | E2 | 3 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY](nodes/FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 3 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [FQ-U1-TRANSPORT-N-TORSION](nodes/FQ-U1-TRANSPORT-N-TORSION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 3 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-180-RESIDUAL-COUNT](nodes/MUB6-180-RESIDUAL-COUNT.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 3 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-CORNER-ROUTING-DEPHASING](nodes/MUB6-CORNER-ROUTING-DEPHASING.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 3 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS](nodes/MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 3 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](nodes/PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) | GENESIS | `PROVED_LEAN` | E0 | 3 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-GO-H3-TWIN-FILLS-HOLONOMY](nodes/PGW-GO-H3-TWIN-FILLS-HOLONOMY.md) | GENESIS | `PROVED_LEAN` | E0 | 3 | grade E0; 6 Lean reference(s) cited, 0 in this checkout |
| [PGW-WDP-EXACT-SEQUENCE-H1-Q1](nodes/PGW-WDP-EXACT-SEQUENCE-H1-Q1.md) | WDP | `PROVED_LEAN` | E0 | 3 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [QCV-OVERHEAD-GROWTH-CRITERION](nodes/QCV-OVERHEAD-GROWTH-CRITERION.md) | COMPUTATION | `PROVED_LEAN` | E2 | 3 | grade E2; 13 Lean reference(s) cited, 13 in this checkout (replay: none 13) |
| [AUTHF-TERMINAL-ACCEPT-BIT](nodes/AUTHF-TERMINAL-ACCEPT-BIT.md) | COMPUTATION | `PROVED_LEAN` | E2 | 2 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [AUTHF-TRANSITION-INVARIANTS](nodes/AUTHF-TRANSITION-INVARIANTS.md) | COMPUTATION | `PROVED_LEAN` | E2 | 2 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [COMP-C3-VERDICT-SOUND](nodes/COMP-C3-VERDICT-SOUND.md) | COMPUTATION | `PROVED_LEAN` | E2 | 2 | grade E2; 7 Lean reference(s) cited, 7 in this checkout (replay: none 7) |
| [COMP-C4-STEPE-UNCAPPED](nodes/COMP-C4-STEPE-UNCAPPED.md) | COMPUTATION | `PROVED_LEAN` | E2 | 2 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [DFM-EW-DOUBLET-REDUCTION](nodes/DFM-EW-DOUBLET-REDUCTION.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 2 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY](nodes/DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 2 | grade E2; 4 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-BELL-CLASSICAL-JOINT-EXTENSION](nodes/FQ-BELL-CLASSICAL-JOINT-EXTENSION.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 2 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FSP-INVOLUTION-PAIR-CANCELLATION](nodes/FSP-INVOLUTION-PAIR-CANCELLATION.md) | FERMION_SIGN | `PROVED_LEAN` | E2 | 2 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [L1-FRAMEWORK-KKT-CERT](nodes/L1-FRAMEWORK-KKT-CERT.md) | L1_EMERGENCE | `PROVED_LEAN` | E2 | 2 | grade E2; 2 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [L1-QM002-O022A-PHI1-QUOTIENT](nodes/L1-QM002-O022A-PHI1-QUOTIENT.md) | L1_EMERGENCE | `PROVED_LEAN` | E2 | 2 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [L1-QM020-THM6-P1-SCOPE-FENCE](nodes/L1-QM020-THM6-P1-SCOPE-FENCE.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 2 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-CAUCHY-BINET-MINOR-BOUND](nodes/MUB6-CAUCHY-BINET-MINOR-BOUND.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 2 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-COMMUTATIVE-FLAT-REAL-POINT](nodes/MUB6-COMMUTATIVE-FLAT-REAL-POINT.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 2 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-CONCRETE-PROJECTORS](nodes/MUB6-CONCRETE-PROJECTORS.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 2 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [MUB6-QUADRATIC-LIFT-386](nodes/MUB6-QUADRATIC-LIFT-386.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 2 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-TAO-MATRIX-CHM](nodes/MUB6-TAO-MATRIX-CHM.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 2 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [PGW-MU1-MINIMUM-NOT-UNIQUE-L](nodes/PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) | GENESIS | `PROVED_LEAN` | E0 | 2 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-PFP-CARRIER-ORIGIN-NILPOTENCY](nodes/PGW-PFP-CARRIER-ORIGIN-NILPOTENCY.md) | IMPLEMENTATION | `PROVED_LEAN` | E0 | 2 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-RESPONSE-EXISTENCE-MARK-PROGRESS](nodes/PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md) | GENESIS | `PROVED_LEAN` | E0 | 2 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-WDP-FILLED-TRIANGLE](nodes/PGW-WDP-FILLED-TRIANGLE.md) | WDP | `PROVED_LEAN` | E0 | 2 | grade E0; 1 Lean reference(s) cited, 0 in this checkout |
| [AUTHF-REPLAY-BOUND-SUBMISSION](nodes/AUTHF-REPLAY-BOUND-SUBMISSION.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [AUTHF-TERMINAL-CLOSED-TWO-SIDED](nodes/AUTHF-TERMINAL-CLOSED-TWO-SIDED.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [AUTHF-TRANSITION-ADEQUACY](nodes/AUTHF-TRANSITION-ADEQUACY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [COMP-C2-LETTER-RENAME-COMMUTES](nodes/COMP-C2-LETTER-RENAME-COMMUTES.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [COMP-C2-ONE-HOLE-CONTEXTS](nodes/COMP-C2-ONE-HOLE-CONTEXTS.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [COMP-C3-RUNNER-NEEDS-BLANKS](nodes/COMP-C3-RUNNER-NEEDS-BLANKS.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [COMP-C6-FINITE-MARKS](nodes/COMP-C6-FINITE-MARKS.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [COMP-C8-BINARY-CODING](nodes/COMP-C8-BINARY-CODING.md) | COMPUTATION | `PROVED_LEAN` | E2 | 1 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED](nodes/DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 1 | grade E2; 5 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [DS-QM081-CPTP-MONOTONE-NOT-SELECTING](nodes/DS-QM081-CPTP-MONOTONE-NOT-SELECTING.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM081-STOCHASTIC-L1-CONTRACTION](nodes/DS-QM081-STOCHASTIC-L1-CONTRACTION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO](nodes/DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [FQ-BELL-RATIONAL-VIOLATION-14-5](nodes/FQ-BELL-RATIONAL-VIOLATION-14-5.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-BORN-NORMALIZATION-REDUNDANCY](nodes/FQ-BORN-NORMALIZATION-REDUNDANCY.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-BUSCH-EFFECT-FRAME](nodes/FQ-BUSCH-EFFECT-FRAME.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 1 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION](nodes/FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-POWER-RULE-P2-SELECTION](nodes/FQ-POWER-RULE-P2-SELECTION.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [FQ-SORKIN-READOUT-CLASS-QM208](nodes/FQ-SORKIN-READOUT-CLASS-QM208.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](nodes/L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [L1-QM020-THM7-REPRESENTATION-CAPACITY](nodes/L1-QM020-THM7-REPRESENTATION-CAPACITY.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [L1-QM122-BORN-PAIRING-NONUNIQUE](nodes/L1-QM122-BORN-PAIRING-NONUNIQUE.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 1 | grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [MAJ-GIN-INVOLUTION-PAIR-CANCEL](nodes/MAJ-GIN-INVOLUTION-PAIR-CANCEL.md) | MAJORANA | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MAJ-TRIVIAL-H1-NO-CLOSED](nodes/MAJ-TRIVIAL-H1-NO-CLOSED.md) | MAJORANA | `PROVED_LEAN` | E2 | 1 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS](nodes/MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-CONCRETE-MOMENT-FLATNESS](nodes/MUB6-CONCRETE-MOMENT-FLATNESS.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 1 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-FOURIER-DITA-FAMILY-CHM](nodes/MUB6-FOURIER-DITA-FAMILY-CHM.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 1 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-FOURTH-BASIS-FLAT-MOMENTS](nodes/MUB6-FOURTH-BASIS-FLAT-MOMENTS.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-SZOLLOSI-COMMON-RAYS](nodes/MUB6-SZOLLOSI-COMMON-RAYS.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 1 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-SZOLLOSI-GAUGED-666](nodes/MUB6-SZOLLOSI-GAUGED-666.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 1 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [PGW-CONTEXT-COUNT-FORMULA](nodes/PGW-CONTEXT-COUNT-FORMULA.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-COUNT-INVARIANCE-TRANSPORT](nodes/PGW-COUNT-INVARIANCE-TRANSPORT.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-INCIDENCE-CONSTRUCTION-BETTI](nodes/PGW-INCIDENCE-CONSTRUCTION-BETTI.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-MSSN-CIRCULATION-OBSTRUCTION](nodes/PGW-MSSN-CIRCULATION-OBSTRUCTION.md) | MSSN_SN | `PROVED_LEAN` | E0 | 1 | grade E0; 5 Lean reference(s) cited, 0 in this checkout |
| [PGW-PRUNING-LEMMAS-COST-TWO](nodes/PGW-PRUNING-LEMMAS-COST-TWO.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | grade E0; 5 Lean reference(s) cited, 0 in this checkout |
| [PGW-QUOTIENT-RETENTION](nodes/PGW-QUOTIENT-RETENTION.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-REPLAY-NECESSITY](nodes/PGW-REPLAY-NECESSITY.md) | PREGENESIS | `PROVED_LEAN` | E0 | 1 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN-ENDPOINT-LEMMA](nodes/PGW-SN-ENDPOINT-LEMMA.md) | MSSN_SN | `PROVED_LEAN` | E0 | 1 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [AUTH-G5C-TERMINALIZATION-CONSEQUENCE](nodes/AUTH-G5C-TERMINALIZATION-CONSEQUENCE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [AUTHF-DTM0-HALT-IFF-STATE](nodes/AUTHF-DTM0-HALT-IFF-STATE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [AUTHF-DTM1-ROUNDTRIP](nodes/AUTHF-DTM1-ROUNDTRIP.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [AUTHF-HALT-NOT-POLICY](nodes/AUTHF-HALT-NOT-POLICY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [AUTHF-LOGICAL-EXTERNALITY](nodes/AUTHF-LOGICAL-EXTERNALITY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [AUTHF-MATHLIB-HALTING-BRIDGE](nodes/AUTHF-MATHLIB-HALTING-BRIDGE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [AUTHF-PD-EXTENSION-NONUNIQUE](nodes/AUTHF-PD-EXTENSION-NONUNIQUE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [AUTHF-SELF-RECEIPT-TOY](nodes/AUTHF-SELF-RECEIPT-TOY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [AUTHF-TAPE-CONTROL-REPORTS](nodes/AUTHF-TAPE-CONTROL-REPORTS.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [AUTHF-TERMINAL-BOOL-FIXTURE](nodes/AUTHF-TERMINAL-BOOL-FIXTURE.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [COMP-C4-SUPPLY-GROWTH](nodes/COMP-C4-SUPPLY-GROWTH.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [COMP-C5-MARK-BUDGET-RULE-LIST](nodes/COMP-C5-MARK-BUDGET-RULE-LIST.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [CQFT-NO-SIGNALLING-PRODUCT-LEAN](nodes/CQFT-NO-SIGNALLING-PRODUCT-LEAN.md) | CAUSAL_QFT | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [DFM-CABIBBO-CP-PHASE-ZERO](nodes/DFM-CABIBBO-CP-PHASE-ZERO.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [DFM-CKM-CYCLE-COUNT](nodes/DFM-CKM-CYCLE-COUNT.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [DFM-SM-ANOMALY-NC-THREE](nodes/DFM-SM-ANOMALY-NC-THREE.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DFM-TREE-CHORD-COORDINATES](nodes/DFM-TREE-CHORD-COORDINATES.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DFM-WEINBERG-PROJECTORS-RHO](nodes/DFM-WEINBERG-PROJECTORS-RHO.md) | DRESSING_FIELD | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY](nodes/DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY.md) | FINITE_QM_DYNAMICS | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM064-074-083-ANNEX-REDIRECT-ROWS](nodes/DS-QM064-074-083-ANNEX-REDIRECT-ROWS.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM073-BELL-THEOREM-OBSTRUCTED](nodes/DS-QM073-BELL-THEOREM-OBSTRUCTED.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION](nodes/DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](nodes/DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [DS-QM090-093-QM-UNIQUENESS-TIER3](nodes/DS-QM090-093-QM-UNIQUENESS-TIER3.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [DS-QM094-EVERETT-RELATIVE-STATE-CONTACT](nodes/DS-QM094-EVERETT-RELATIVE-STATE-CONTACT.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-ENTROPY-DICHOTOMY-BAKER](nodes/FQ-ENTROPY-DICHOTOMY-BAKER.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 0 | grade E2; 7 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY](nodes/FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY.md) | FINITE_QM_DYNAMICS | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-FIVE-IMPORT-PROXY-SEPARATION](nodes/FQ-FIVE-IMPORT-PROXY-SEPARATION.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-INTERFERENCE-NONDESCENT](nodes/FQ-INTERFERENCE-NONDESCENT.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED](nodes/FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [FQ-QM207-231-FINITE-MAP-CONTROLS](nodes/FQ-QM207-231-FINITE-MAP-CONTROLS.md) | FINITE_QM_STRUCTURE | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [FQ-TSIRELSON-SOS-Q-SQRT2](nodes/FQ-TSIRELSON-SOS-Q-SQRT2.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [GP-DROP-ONE-CENSUS](nodes/GP-DROP-ONE-CENSUS.md) | FINITE_QM_CORE | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [IMPL-LGGR-FINITE-RESULTS-LEAN](nodes/IMPL-LGGR-FINITE-RESULTS-LEAN.md) | IMPLEMENTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 7 Lean reference(s) cited, 7 in this checkout (replay: none 7) |
| [IMPL-THYMUS-SCREENING-SOUNDNESS](nodes/IMPL-THYMUS-SCREENING-SOUNDNESS.md) | IMPLEMENTATION | `PROVED_LEAN` | E0 | 0 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [L1-GS001-GAUGE-L1](nodes/L1-GS001-GAUGE-L1.md) | L1_EMERGENCE | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [L1-OPERATOR-LIFT-TRACE-EMBED-013](nodes/L1-OPERATOR-LIFT-TRACE-EMBED-013.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [L1-QM003-C17-COMPOSABLE-FACTORIZATION](nodes/L1-QM003-C17-COMPOSABLE-FACTORIZATION.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [L1-QM020-C10-BRANCH-LOCALIZATION](nodes/L1-QM020-C10-BRANCH-LOCALIZATION.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [L1-QM020-THM3-ROW-SPARSITY](nodes/L1-QM020-THM3-ROW-SPARSITY.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [L1-QM020-THM5-PHASE-AVERAGED-SHADOW](nodes/L1-QM020-THM5-PHASE-AVERAGED-SHADOW.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [L1-QM121-LADDER-RUNGS-2-6](nodes/L1-QM121-LADDER-RUNGS-2-6.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](nodes/L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | grade E2; 7 Lean reference(s) cited, 6 in this checkout (replay: none 6) |
| [L1-WDP-CH08-C01-REPLICA-L1](nodes/L1-WDP-CH08-C01-REPLICA-L1.md) | L1_EMERGENCE | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MAJ-ENVELOPE-NAT-ARITHMETIC](nodes/MAJ-ENVELOPE-NAT-ARITHMETIC.md) | MAJORANA | `PROVED_LEAN` | E2 | 0 | grade E2; 11 Lean reference(s) cited, 11 in this checkout (replay: none 11) |
| [MAJ-KITAEV-EDGE-INDEX-DISJOINT](nodes/MAJ-KITAEV-EDGE-INDEX-DISJOINT.md) | MAJORANA | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-BALANCED-648-QUADRATIC](nodes/MUB6-BALANCED-648-QUADRATIC.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [MUB6-CLOSE-COLUMNS-EXCLUSION](nodes/MUB6-CLOSE-COLUMNS-EXCLUSION.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-COVER56-CURVATURE-PREMISE](nodes/MUB6-COVER56-CURVATURE-PREMISE.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-EMPTY-VARIETY-MOMENT-NONPSD](nodes/MUB6-EMPTY-VARIETY-MOMENT-NONPSD.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-HAAGERUP-MATRIX-CHM](nodes/MUB6-HAAGERUP-MATRIX-CHM.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-INTERFACE-COUNTERMODEL](nodes/MUB6-INTERFACE-COUNTERMODEL.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-KARLSSON-AFFINE-ANSATZ](nodes/MUB6-KARLSSON-AFFINE-ANSATZ.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1) |
| [MUB6-ROUTE-C-LABEL-ARITHMETIC](nodes/MUB6-ROUTE-C-LABEL-ARITHMETIC.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-SZOLLOSI-BOX-368-EXCLUSION](nodes/MUB6-SZOLLOSI-BOX-368-EXCLUSION.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2) |
| [MUB6-TAO-LAURENT-NORM-NINE](nodes/MUB6-TAO-LAURENT-NORM-NINE.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-TRANSITION-BALANCE-SYZYGY](nodes/MUB6-TRANSITION-BALANCE-SYZYGY.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [MUB6-WORD-PROJECTOR-EXTRACTION](nodes/MUB6-WORD-PROJECTOR-EXTRACTION.md) | MUTUALLY_UNBIASED_BASES | `PROVED_LEAN` | E2 | 0 | grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3) |
| [PG-GEN-SUPPLY-ERASURE](nodes/PG-GEN-SUPPLY-ERASURE.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-CANONICAL-KEY-CLASSIFICATION](nodes/PGW-CANONICAL-KEY-CLASSIFICATION.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 5 Lean reference(s) cited, 0 in this checkout |
| [PGW-CHALLENGE0-INERTIA-SECOND-TOKEN](nodes/PGW-CHALLENGE0-INERTIA-SECOND-TOKEN.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-COLLECTION-EXTENSIONALITY](nodes/PGW-COLLECTION-EXTENSIONALITY.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 4 Lean reference(s) cited, 0 in this checkout |
| [PGW-FAITHFUL-DESCENT-ROUND-TRIP](nodes/PGW-FAITHFUL-DESCENT-ROUND-TRIP.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 2 Lean reference(s) cited, 0 in this checkout |
| [PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE](nodes/PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE.md) | PREGENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-MU1-ARITY-INDEXED-TIE-FAMILY](nodes/PGW-MU1-ARITY-INDEXED-TIE-FAMILY.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-SN-REPRESENTATION-QUOTIENT](nodes/PGW-SN-REPRESENTATION-QUOTIENT.md) | MSSN_SN | `PROVED_LEAN` | E0 | 0 | grade E0; 3 Lean reference(s) cited, 0 in this checkout |
| [PGW-WDP-POINTED-APARTNESS](nodes/PGW-WDP-POINTED-APARTNESS.md) | WDP | `PROVED_LEAN` | E0 | 0 | grade E0; 1 Lean reference(s) cited, 0 in this checkout |
| [QCV-QUBIT-BLOCH-DECAY-EXACT](nodes/QCV-QUBIT-BLOCH-DECAY-EXACT.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |
| [QCV-REPAIR-NEEDED-BUT-COSTLY](nodes/QCV-REPAIR-NEEDED-BUT-COSTLY.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4) |
| [QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS](nodes/QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS.md) | COMPUTATION | `PROVED_LEAN` | E2 | 0 | grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5) |

## `proved_lean_external_only` (53)

PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-GEN-SUPPLY-NO-OP](nodes/PG-GEN-SUPPLY-NO-OP.md) | GENESIS | `PROVED_LEAN` | E0 | 690 | all 2 cited Lean reference(s) lie outside this checkout |
| [PG-GEN-NO-RETURN](nodes/PG-GEN-NO-RETURN.md) | GENESIS | `PROVED_LEAN` | E0 | 660 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-POLICY-ENDPOINT-ALL-SEPARATED](nodes/PGW-POLICY-ENDPOINT-ALL-SEPARATED.md) | GENESIS | `PROVED_LEAN` | E0 | 135 | all 1 cited Lean reference(s) lie outside this checkout |
| [PG-GEN-IRREFLEXIVE-DISTINCT](nodes/PG-GEN-IRREFLEXIVE-DISTINCT.md) | GENESIS | `PROVED_LEAN` | E0 | 115 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-C2-RUN-FORWARD-EVERY-HISTORY](nodes/PGW-C2-RUN-FORWARD-EVERY-HISTORY.md) | GENESIS | `PROVED_LEAN` | E0 | 110 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS](nodes/PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md) | GENESIS | `PROVED_LEAN` | E0 | 57 | all 4 cited Lean reference(s) lie outside this checkout |
| [PG-GEN-ONGOING-OBSTRUCTION](nodes/PG-GEN-ONGOING-OBSTRUCTION.md) | GENESIS | `PROVED_LEAN` | E0 | 51 | all 3 cited Lean reference(s) lie outside this checkout |
| [PG-GEN-ONGOING-FEWEST-CHANGES](nodes/PG-GEN-ONGOING-FEWEST-CHANGES.md) | GENESIS | `PROVED_LEAN` | E0 | 49 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-D2-INITIAL-POINTED](nodes/PGW-D2-INITIAL-POINTED.md) | GENESIS | `PROVED_LEAN` | E0 | 46 | all 2 cited Lean reference(s) lie outside this checkout |
| [PG-PREGEN-CONSTRUCTIVE-SUMMARY](nodes/PG-PREGEN-CONSTRUCTIVE-SUMMARY.md) | PREGENESIS | `PROVED_LEAN` | E3 | 42 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD](nodes/PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD.md) | GENESIS | `PROVED_LEAN` | E0 | 41 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-SN0-GROUND-INERTIA](nodes/PGW-SN0-GROUND-INERTIA.md) | MSSN_SN | `PROVED_LEAN` | E0 | 33 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-SN1-SUPPLY-NOT-ADMISSION](nodes/PGW-SN1-SUPPLY-NOT-ADMISSION.md) | MSSN_SN | `PROVED_LEAN` | E0 | 32 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-SN2-OPAQUE-COLLAPSE](nodes/PGW-SN2-OPAQUE-COLLAPSE.md) | MSSN_SN | `PROVED_LEAN` | E0 | 31 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-SN3-COST-TWO-UNARY-MARK](nodes/PGW-SN3-COST-TWO-UNARY-MARK.md) | MSSN_SN | `PROVED_LEAN` | E0 | 30 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-REACH-CEILING](nodes/PGW-GO-REACH-CEILING.md) | GENESIS | `PROVED_LEAN` | E0 | 25 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-CONTRACTION-STEP2-STEP3](nodes/PGW-GO-CONTRACTION-STEP2-STEP3.md) | GENESIS | `PROVED_LEAN` | E0 | 24 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-MULTIPLICITY-MONOTONE](nodes/PGW-GO-MULTIPLICITY-MONOTONE.md) | GENESIS | `PROVED_LEAN` | E0 | 23 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-TWO-RELATIONS-SWAP](nodes/PGW-GO-TWO-RELATIONS-SWAP.md) | GENESIS | `PROVED_LEAN` | E0 | 22 | all 4 cited Lean reference(s) lie outside this checkout |
| [PG-SN-OFF-IMAGE-REFUSAL](nodes/PG-SN-OFF-IMAGE-REFUSAL.md) | PREGENESIS | `PROVED_LEAN` | E3 | 19 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](nodes/PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) | MSSN_SN | `PROVED_LEAN` | E0 | 18 | all 5 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-LEFTOVER-UNBOUNDEDNESS](nodes/PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) | GENESIS | `PROVED_LEAN` | E0 | 8 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-COLLAPSE-WITHOUT-INSTANCES](nodes/PGW-COLLAPSE-WITHOUT-INSTANCES.md) | GENESIS | `PROVED_LEAN` | E0 | 5 | all 1 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-H1-CANCELLATION-EXCESS](nodes/PGW-GO-H1-CANCELLATION-EXCESS.md) | GENESIS | `PROVED_LEAN` | E0 | 5 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-SN-E12-CIRCULATION-FUNCTIONAL](nodes/PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) | MSSN_SN | `PROVED_LEAN` | E0 | 5 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED](nodes/PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED.md) | GENESIS | `PROVED_LEAN` | E0 | 4 | all 5 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-H2-STATE-RAISING-GAUGE](nodes/PGW-GO-H2-STATE-RAISING-GAUGE.md) | GENESIS | `PROVED_LEAN` | E0 | 4 | all 5 cited Lean reference(s) lie outside this checkout |
| [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](nodes/PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) | GENESIS | `PROVED_LEAN` | E0 | 4 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](nodes/PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) | GENESIS | `PROVED_LEAN` | E0 | 3 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-GO-H3-TWIN-FILLS-HOLONOMY](nodes/PGW-GO-H3-TWIN-FILLS-HOLONOMY.md) | GENESIS | `PROVED_LEAN` | E0 | 3 | all 6 cited Lean reference(s) lie outside this checkout |
| [PGW-WDP-EXACT-SEQUENCE-H1-Q1](nodes/PGW-WDP-EXACT-SEQUENCE-H1-Q1.md) | WDP | `PROVED_LEAN` | E0 | 3 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-MU1-MINIMUM-NOT-UNIQUE-L](nodes/PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) | GENESIS | `PROVED_LEAN` | E0 | 2 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-PFP-CARRIER-ORIGIN-NILPOTENCY](nodes/PGW-PFP-CARRIER-ORIGIN-NILPOTENCY.md) | IMPLEMENTATION | `PROVED_LEAN` | E0 | 2 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-RESPONSE-EXISTENCE-MARK-PROGRESS](nodes/PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md) | GENESIS | `PROVED_LEAN` | E0 | 2 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-WDP-FILLED-TRIANGLE](nodes/PGW-WDP-FILLED-TRIANGLE.md) | WDP | `PROVED_LEAN` | E0 | 2 | all 1 cited Lean reference(s) lie outside this checkout |
| [PGW-CONTEXT-COUNT-FORMULA](nodes/PGW-CONTEXT-COUNT-FORMULA.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-COUNT-INVARIANCE-TRANSPORT](nodes/PGW-COUNT-INVARIANCE-TRANSPORT.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-INCIDENCE-CONSTRUCTION-BETTI](nodes/PGW-INCIDENCE-CONSTRUCTION-BETTI.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-MSSN-CIRCULATION-OBSTRUCTION](nodes/PGW-MSSN-CIRCULATION-OBSTRUCTION.md) | MSSN_SN | `PROVED_LEAN` | E0 | 1 | all 5 cited Lean reference(s) lie outside this checkout |
| [PGW-PRUNING-LEMMAS-COST-TWO](nodes/PGW-PRUNING-LEMMAS-COST-TWO.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | all 5 cited Lean reference(s) lie outside this checkout |
| [PGW-QUOTIENT-RETENTION](nodes/PGW-QUOTIENT-RETENTION.md) | GENESIS | `PROVED_LEAN` | E0 | 1 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-REPLAY-NECESSITY](nodes/PGW-REPLAY-NECESSITY.md) | PREGENESIS | `PROVED_LEAN` | E0 | 1 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-SN-ENDPOINT-LEMMA](nodes/PGW-SN-ENDPOINT-LEMMA.md) | MSSN_SN | `PROVED_LEAN` | E0 | 1 | all 4 cited Lean reference(s) lie outside this checkout |
| [IMPL-THYMUS-SCREENING-SOUNDNESS](nodes/IMPL-THYMUS-SCREENING-SOUNDNESS.md) | IMPLEMENTATION | `PROVED_LEAN` | E0 | 0 | all 2 cited Lean reference(s) lie outside this checkout |
| [PG-GEN-SUPPLY-ERASURE](nodes/PG-GEN-SUPPLY-ERASURE.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-CANONICAL-KEY-CLASSIFICATION](nodes/PGW-CANONICAL-KEY-CLASSIFICATION.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | all 5 cited Lean reference(s) lie outside this checkout |
| [PGW-CHALLENGE0-INERTIA-SECOND-TOKEN](nodes/PGW-CHALLENGE0-INERTIA-SECOND-TOKEN.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-COLLECTION-EXTENSIONALITY](nodes/PGW-COLLECTION-EXTENSIONALITY.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | all 4 cited Lean reference(s) lie outside this checkout |
| [PGW-FAITHFUL-DESCENT-ROUND-TRIP](nodes/PGW-FAITHFUL-DESCENT-ROUND-TRIP.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | all 2 cited Lean reference(s) lie outside this checkout |
| [PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE](nodes/PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE.md) | PREGENESIS | `PROVED_LEAN` | E0 | 0 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-MU1-ARITY-INDEXED-TIE-FAMILY](nodes/PGW-MU1-ARITY-INDEXED-TIE-FAMILY.md) | GENESIS | `PROVED_LEAN` | E0 | 0 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-SN-REPRESENTATION-QUOTIENT](nodes/PGW-SN-REPRESENTATION-QUOTIENT.md) | MSSN_SN | `PROVED_LEAN` | E0 | 0 | all 3 cited Lean reference(s) lie outside this checkout |
| [PGW-WDP-POINTED-APARTNESS](nodes/PGW-WDP-POINTED-APARTNESS.md) | WDP | `PROVED_LEAN` | E0 | 0 | all 1 cited Lean reference(s) lie outside this checkout |

## `receipt_not_current` (0)

A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit. Ordered by downstream nodes, most first.

None.

## `computational_no_runnable_test` (126)

COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](nodes/PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 683 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-CLOSED-BASELINE-TERMINATES](nodes/PGW-CLOSED-BASELINE-TERMINATES.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 136 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-GENESIS-THREE-AXIS-VERDICT](nodes/PGW-GENESIS-THREE-AXIS-VERDICT.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 124 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-RUNG0-INHERITANCE-REPLAY](nodes/PGW-RUNG0-INHERITANCE-REPLAY.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 123 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-FORCED-CENSUS-COLUMN](nodes/PGW-FORCED-CENSUS-COLUMN.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 109 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM062-U1-SELECTOR-LAYERS](nodes/DS-QM062-U1-SELECTOR-LAYERS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 70 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-RUNG2B-STAKE-MENU](nodes/PGW-RUNG2B-STAKE-MENU.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 42 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0125](nodes/TFQ-0125.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 40 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0126](nodes/TFQ-0126.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 39 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0127](nodes/TFQ-0127.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 38 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0129](nodes/TFQ-0129.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 34 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0166](nodes/TFQ-0166.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 32 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [COMP-C1-FIRST-SEPARATION-REPLAY](nodes/COMP-C1-FIRST-SEPARATION-REPLAY.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E2 | 30 | 6 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0131](nodes/TFQ-0131.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 30 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0013](nodes/TFQ-0013.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 29 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0015](nodes/TFQ-0015.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E0 | 27 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0018](nodes/TFQ-0018.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 24 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0019](nodes/TFQ-0019.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 23 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0043](nodes/TFQ-0043.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 23 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0020](nodes/TFQ-0020.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 22 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0021](nodes/TFQ-0021.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 21 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0022](nodes/TFQ-0022.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 20 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0133](nodes/TFQ-0133.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 20 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0023](nodes/TFQ-0023.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 19 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0024](nodes/TFQ-0024.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 16 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0197](nodes/TFQ-0197.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 16 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0025](nodes/TFQ-0025.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 15 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0048](nodes/TFQ-0048.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E0 | 15 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0198](nodes/TFQ-0198.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 14 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM061-BUILDABILITY-SET-S](nodes/DS-QM061-BUILDABILITY-SET-S.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 12 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0028](nodes/TFQ-0028.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 12 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0029](nodes/TFQ-0029.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 11 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0030](nodes/TFQ-0030.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 10 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM030-UNGRADED-OVERCOUNT](nodes/DS-QM030-UNGRADED-OVERCOUNT.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 9 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0144](nodes/TFQ-0144.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 9 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [AUTH-TC0-TAPE-CONTROL-TYPING](nodes/AUTH-TC0-TAPE-CONTROL-TYPING.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E2 | 8 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM030-GRADED-PATHSUM](nodes/DS-QM030-GRADED-PATHSUM.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 8 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [AUTH-TC2-FINITE-TRANSITION-CONTRACT](nodes/AUTH-TC2-FINITE-TRANSITION-CONTRACT.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E2 | 7 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0146](nodes/TFQ-0146.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 7 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0137](nodes/TFQ-0137.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 6 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0147](nodes/TFQ-0147.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 5 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0154](nodes/TFQ-0154.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 5 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM030-TRANSFER-OPERATOR-SHADOW](nodes/DS-QM030-TRANSFER-OPERATOR-SHADOW.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM090-092-AUTHORITY-FIREWALL](nodes/DS-QM090-092-AUTHORITY-FIREWALL.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-ALPHA-LICENSE-BINDING-M1-M8](nodes/PGW-ALPHA-LICENSE-BINDING-M1-M8.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E0 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0034](nodes/TFQ-0034.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 4 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0148](nodes/TFQ-0148.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 4 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM021-IDEMPOTENT-CONDITIONING](nodes/DS-QM021-IDEMPOTENT-CONDITIONING.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0035](nodes/TFQ-0035.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0149](nodes/TFQ-0149.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0172](nodes/TFQ-0172.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 4 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0176](nodes/TFQ-0176.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 3 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [DFM-BPHZ-SECTOR-KERNEL](nodes/DFM-BPHZ-SECTOR-KERNEL.md) | DRESSING_FIELD | `COMPUTATIONALLY_CHECKED` | E2 | 2 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [DFM-TREE-CHANGE-GLZ-SYMANZIK-U](nodes/DFM-TREE-CHANGE-GLZ-SYMANZIK-U.md) | DRESSING_FIELD | `COMPUTATIONALLY_CHECKED` | E2 | 2 | 3 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](nodes/DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-TRACE-ZERO-DUALITY-K23](nodes/FQ-TRACE-ZERO-DUALITY-K23.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E2 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0036](nodes/TFQ-0036.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0045](nodes/TFQ-0045.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E0 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0049](nodes/TFQ-0049.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0134](nodes/TFQ-0134.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0150](nodes/TFQ-0150.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 2 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0189](nodes/TFQ-0189.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 2 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM032-FINITE-FEYNMAN-SHADOW](nodes/DS-QM032-FINITE-FEYNMAN-SHADOW.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-CABELLO-FRAME-POLYTOPE-146](nodes/FQ-CABELLO-FRAME-POLYTOPE-146.md) | FINITE_QM_CORE | `COMPUTATIONALLY_CHECKED` | E2 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [GP-GAP-EXACT-DUALITY](nodes/GP-GAP-EXACT-DUALITY.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [MUB6-PRODUCT-TRIPLE-LOWER-BOUND](nodes/MUB6-PRODUCT-TRIPLE-LOWER-BOUND.md) | MUTUALLY_UNBIASED_BASES | `COMPUTATIONALLY_CHECKED` | E2 | 1 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0037](nodes/TFQ-0037.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0046](nodes/TFQ-0046.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0138](nodes/TFQ-0138.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0140](nodes/TFQ-0140.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0151](nodes/TFQ-0151.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0155](nodes/TFQ-0155.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0160](nodes/TFQ-0160.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 1 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0193](nodes/TFQ-0193.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 1 | 5 in-repo Rust or Python symbol(s) cited, none a test |
| [AUTHF-REPLAY-SUBSTITUTIONS](nodes/AUTHF-REPLAY-SUBSTITUTIONS.md) | COMPUTATION | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM032-CONTINUUM-LIMIT-CONDITIONAL](nodes/DS-QM032-CONTINUUM-LIMIT-CONDITIONAL.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS](nodes/DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM041-HEISENBERG-PICTURE-FINITE](nodes/DS-QM041-HEISENBERG-PICTURE-FINITE.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM093-SURVIVAL-THEOREM](nodes/DS-QM093-SURVIVAL-THEOREM.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM206-BOUNDARY-SYNTHESIS](nodes/DS-QM206-BOUNDARY-SYNTHESIS.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [DS-QM207-211-FIVE-IMPORT-CASCADE](nodes/DS-QM207-211-FIVE-IMPORT-CASCADE.md) | FINITE_QM_STRUCTURE | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-GAP-REAL-EMBEDDING-CHOICE](nodes/FQ-GAP-REAL-EMBEDDING-CHOICE.md) | FINITE_QM_DYNAMICS | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [FQ-IMPL-PAIRING-AUDIT](nodes/FQ-IMPL-PAIRING-AUDIT.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [MUB6-SZOLLOSI-FULLBOX-UNRESOLVED](nodes/MUB6-SZOLLOSI-FULLBOX-UNRESOLVED.md) | MUTUALLY_UNBIASED_BASES | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS](nodes/MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS.md) | MUTUALLY_UNBIASED_BASES | `COMPUTATIONALLY_CHECKED` | E2 | 0 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [PG-GEN-SAMENESS-REFINEMENTS](nodes/PG-GEN-SAMENESS-REFINEMENTS.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-BOUNDED-TIE-CENSUS](nodes/PGW-BOUNDED-TIE-CENSUS.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-BRANCH-TREES-AND-ROLES](nodes/PGW-BRANCH-TREES-AND-ROLES.md) | GENESIS | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [PGW-PFP-C4-CERTIFICATE](nodes/PGW-PFP-C4-CERTIFICATE.md) | IMPLEMENTATION | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0041](nodes/TFQ-0041.md) | FINITE_QCD | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0047](nodes/TFQ-0047.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0051](nodes/TFQ-0051.md) | FINITE_TOPOLOGICAL | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0128](nodes/TFQ-0128.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0130](nodes/TFQ-0130.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0132](nodes/TFQ-0132.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0135](nodes/TFQ-0135.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0136](nodes/TFQ-0136.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0139](nodes/TFQ-0139.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0141](nodes/TFQ-0141.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0142](nodes/TFQ-0142.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0143](nodes/TFQ-0143.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0145](nodes/TFQ-0145.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0152](nodes/TFQ-0152.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0153](nodes/TFQ-0153.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 1 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0156](nodes/TFQ-0156.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0157](nodes/TFQ-0157.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0158](nodes/TFQ-0158.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0159](nodes/TFQ-0159.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0161](nodes/TFQ-0161.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0162](nodes/TFQ-0162.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | 2 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0163](nodes/TFQ-0163.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0164](nodes/TFQ-0164.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
| [TFQ-0165](nodes/TFQ-0165.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | 0 in-repo Rust or Python symbol(s) cited, none a test |
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

## `proved_prose_no_in_repo_document` (13)

PROVED_PROSE with no in-repo source document cited. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](nodes/PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) | GENESIS | `PROVED_PROSE` | E0 | 134 | no in-repo non-generated document among the counted sources |
| [PGW-IDENTITY-IS-INDEX-NOT-PROFILE](nodes/PGW-IDENTITY-IS-INDEX-NOT-PROFILE.md) | GENESIS | `PROVED_PROSE` | E0 | 132 | no in-repo non-generated document among the counted sources |
| [PGW-MINIMAL-OR-INITIAL-REFUSED](nodes/PGW-MINIMAL-OR-INITIAL-REFUSED.md) | GENESIS | `PROVED_PROSE` | E0 | 132 | no in-repo non-generated document among the counted sources |
| [PGW-SEALED-TERMINAL-STATEMENT](nodes/PGW-SEALED-TERMINAL-STATEMENT.md) | GENESIS | `PROVED_PROSE` | E0 | 131 | no in-repo non-generated document among the counted sources |
| [PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE](nodes/PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md) | MSSN_SN | `PROVED_PROSE` | E0 | 27 | no in-repo non-generated document among the counted sources |
| [PGW-WDP-FAILED-SAMENESS](nodes/PGW-WDP-FAILED-SAMENESS.md) | WDP | `PROVED_PROSE` | E0 | 10 | no in-repo non-generated document among the counted sources |
| [PGW-WDP-DEGREE-K-TORSION-BALANCE](nodes/PGW-WDP-DEGREE-K-TORSION-BALANCE.md) | WDP | `PROVED_PROSE` | E0 | 9 | no in-repo non-generated document among the counted sources |
| [PGW-SN-POSTNIKOV-REFUSAL](nodes/PGW-SN-POSTNIKOV-REFUSAL.md) | MSSN_SN | `PROVED_PROSE` | E0 | 7 | no in-repo non-generated document among the counted sources |
| [PGW-WDP-TRICHOTOMY-BOUNDS](nodes/PGW-WDP-TRICHOTOMY-BOUNDS.md) | WDP | `PROVED_PROSE` | E0 | 2 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E18-L1-TIES-L2-CENTER](nodes/PGW-SN-E18-L1-TIES-L2-CENTER.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E19-TORSION-ERASED-OVER-Q](nodes/PGW-SN-E19-TORSION-ERASED-OVER-Q.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E20-OBSERVER-COMPLETION](nodes/PGW-SN-E20-OBSERVER-COMPLETION.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |
| [PGW-SN-E21-REPAIR-RANK](nodes/PGW-SN-E21-REPAIR-RANK.md) | MSSN_SN | `PROVED_PROSE` | E0 | 0 | no in-repo non-generated document among the counted sources |

## `broken_reference` (55)

A cited in-repo path or symbol cannot be found in this checkout. Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-PRIMDIFF-AXIOMS](nodes/PG-PRIMDIFF-AXIOMS.md) | PREGENESIS | `DEFINITION` | E3 | 497 | path not found: code/python/src/majorana/tests/unit/test_primitive_difference.py |
| [GP-IMPORT-CONTINUOUS-TIME](nodes/GP-IMPORT-CONTINUOUS-TIME.md) | L1_TO_L2 | `IMPORTED_ASSUMPTION` | E2 | 96 | path not found: lean4/quantum_mechanics/H016ContinuousDynamicsFork.lean |
| [TFQ-0125](nodes/TFQ-0125.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 40 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/finite_qm_engine.py |
| [TFQ-0127](nodes/TFQ-0127.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 38 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/operational_axiom_selection.py |
| [TFQ-0129](nodes/TFQ-0129.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 34 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/born_normalization.py |
| [TFQ-0131](nodes/TFQ-0131.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 30 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0320](nodes/TFQ-0320.md) | FINITE_OBSTRUCTION | `SOURCE_RECORD` | E0 | 28 | path not found: code/python/src/majorana/tests/unit/test_primitive_difference.py |
| [TFQ-0206](nodes/TFQ-0206.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E0 | 27 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0207](nodes/TFQ-0207.md) | ENGINE_CUSTODY | `OPEN` | E1 | 26 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0208](nodes/TFQ-0208.md) | ENGINE_CUSTODY | `OPEN` | E0 | 25 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0215](nodes/TFQ-0215.md) | ENGINE_CUSTODY | `OPEN` | E1 | 18 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channel.py |
| [TFQ-0144](nodes/TFQ-0144.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 9 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/busch_effects.py |
| [TFQ-0146](nodes/TFQ-0146.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 7 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channel.py |
| [TFQ-0226](nodes/TFQ-0226.md) | ENGINE_CUSTODY | `OPEN` | E1 | 7 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0137](nodes/TFQ-0137.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 6 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/discrete_dynamics.py |
| [TFQ-0147](nodes/TFQ-0147.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 5 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channels_stinespring.py |
| [TFQ-0149](nodes/TFQ-0149.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 3 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/simplicial_complex_qm.py |
| [TFQ-0176](nodes/TFQ-0176.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 3 | path not found: code/python/src/mub/mub_verify/a1_collar_swarm.py |
| [TFQ-0230](nodes/TFQ-0230.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E1 | 3 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.CauchyCircleCompletion.RegPhaseSeq.add_assoc_equiv not found in lean4/U1CauchyCircleCompletion.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.CauchyCircleCompletion.quad_half_angle_squares_to_u345 not found in lean4/U1CauchyCircleCompletion.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.ChebyshevCauchyBridge.HermitianMat2Qi.pureProjector_born_pairing not found in lean4/U1ChebyshevCauchyBridge.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.ChebyshevCauchyBridge.circleRatPow_eq_chebyshev not found in lean4/U1ChebyshevCauchyBridge.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.ChebyshevCauchyBridge.taylor_circle_norm_defect_identity not found in lean4/U1ChebyshevCauchyBridge.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.CyclotomicTorsionTower.ratPhaseQuot_divisible not found in lean4/U1CyclotomicTorsionTower.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.PhaseSynthesis.u1_phase_completion_synthesis not found in lean4/U1PhaseSynthesis.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.PythagoreanObstruction.no_rational_one_param_group_through_u345 not found in lean4/U1PythagoreanObstruction.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.QuadraticTowerAndCayleyStone.chebT2Pow_succ not found in lean4/U1QuadraticTowerAndCayleyStone.lean |
| [FQ-GAP-U1-CIRCLE](nodes/FQ-GAP-U1-CIRCLE.md) | FINITE_QM_CORE | `CONDITIONAL` | E2 | 2 | symbol U1Fable.QuadraticTowerAndCayleyStone.u345_k2_double_angle_recovery not found in lean4/U1QuadraticTowerAndCayleyStone.lean |
| [TFQ-0177](nodes/TFQ-0177.md) | IMPLEMENTATION_SIBLING | `OPEN` | E1 | 2 | path not found: code/python/src/mub/mub_verify/a1_collar_swarm.py |
| [TFQ-0231](nodes/TFQ-0231.md) | ENGINE_CUSTODY | `SOURCE_RECORD` | E0 | 2 | path not found: code/python/src/majorana/tests/support/domain/shared_kernel/obstruction.py |
| [TFQ-0138](nodes/TFQ-0138.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/dynamics_dichotomy.py |
| [TFQ-0138](nodes/TFQ-0138.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/heisenberg_representation_uniqueness.py |
| [TFQ-0140](nodes/TFQ-0140.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/continuous_time_locality_limit.py |
| [TFQ-0140](nodes/TFQ-0140.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/norm_approximation_frontier.py |
| [TFQ-0151](nodes/TFQ-0151.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/discrete_walk_engines.py |
| [TFQ-0315](nodes/TFQ-0315.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 1 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [L1-QM121-LADDER-RUNGS-2-6](nodes/L1-QM121-LADDER-RUNGS-2-6.md) | L1_TO_L2 | `PROVED_LEAN` | E2 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0130](nodes/TFQ-0130.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/higher_dim_entanglement.py |
| [TFQ-0130](nodes/TFQ-0130.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/quantum_protocols.py |
| [TFQ-0135](nodes/TFQ-0135.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/contextuality_f2.py |
| [TFQ-0135](nodes/TFQ-0135.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/mermin_peres.py |
| [TFQ-0136](nodes/TFQ-0136.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/quantum_correlation.py |
| [TFQ-0136](nodes/TFQ-0136.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/tensor_commuting_correlation_frontier.py |
| [TFQ-0152](nodes/TFQ-0152.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/stabilizer_codes.py |
| [TFQ-0159](nodes/TFQ-0159.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/composition_tensor_mub.py |
| [TFQ-0162](nodes/TFQ-0162.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/branch_finegraining.py |
| [TFQ-0162](nodes/TFQ-0162.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/everett_tree.py |
| [TFQ-0163](nodes/TFQ-0163.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/cancellation_certificates.py |
| [TFQ-0163](nodes/TFQ-0163.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/interference.py |
| [TFQ-0165](nodes/TFQ-0165.md) | IMPLEMENTATION_CORE | `COMPUTATIONALLY_CHECKED` | E0 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/tower_topological_completion.py |
| [TFQ-0182](nodes/TFQ-0182.md) | IMPLEMENTATION_SIBLING | `COMPUTATIONALLY_CHECKED` | E1 | 0 | path not found: code/python/src/majorana/majorana/core/gf2_diagnostic.py |
| [TFQ-0183](nodes/TFQ-0183.md) | IMPLEMENTATION_SIBLING | `OPEN` | E1 | 0 | path not found: code/python/src/majorana/majorana/carriers/tetron_carrier.py |
| [TFQ-0289](nodes/TFQ-0289.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |
| [TFQ-0316](nodes/TFQ-0316.md) | FINITE_HILBERT | `SOURCE_RECORD` | E1 | 0 | path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py |

## `receipt_names_uncited_module` (27)

A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence). Ordered by downstream nodes, most first.

| Node | Stage | Status | Grade | Downstream | Detail |
|---|---|---|---|---|---|
| [PG-INERT-DIAMOND](nodes/PG-INERT-DIAMOND.md) | PREGENESIS | `DEFINITION` | E3 | 774 | a replay receipt names this node for lean4/InertDiamond.lean, but the node's lean, rust and source fields do not cite it |
| [PG-SIX-OPERATIONS](nodes/PG-SIX-OPERATIONS.md) | PREGENESIS | `DEFINITION` | E3 | 752 | a replay receipt names this node for lean4/SixOperations.lean, but the node's lean, rust and source fields do not cite it |
| [PG-COLLAPSE-BARRIER](nodes/PG-COLLAPSE-BARRIER.md) | PREGENESIS | `PROVED_LEAN` | E3 | 685 | a replay receipt names this node for lean4/CollapseBarrier.lean, but the node's lean, rust and source fields do not cite it |
| [PG-DEMAND-ACCOUNTING](nodes/PG-DEMAND-ACCOUNTING.md) | PREGENESIS | `PROVED_LEAN` | E3 | 555 | a replay receipt names this node for lean4/DemandAccounting.lean, but the node's lean, rust and source fields do not cite it |
| [PG-REFINE-SEPARATES](nodes/PG-REFINE-SEPARATES.md) | PREGENESIS | `PROVED_LEAN` | E3 | 553 | a replay receipt names this node for lean4/RefineSeparates.lean, but the node's lean, rust and source fields do not cite it |
| [PG-OLD-IMAGE-INJECTIVE](nodes/PG-OLD-IMAGE-INJECTIVE.md) | PREGENESIS | `PROVED_LEAN` | E3 | 552 | a replay receipt names this node for lean4/OldImageInjective.lean, but the node's lean, rust and source fields do not cite it |
| [PG-SN-CARRIER](nodes/PG-SN-CARRIER.md) | MSSN_SN | `PROVED_LEAN` | E3 | 551 | a replay receipt names this node for lean4/SnCarrierPfp.lean, but the node's lean, rust and source fields do not cite it |
| [PG-OBLIGATION-MONOID](nodes/PG-OBLIGATION-MONOID.md) | MSSN_SN | `PROVED_LEAN` | E3 | 503 | a replay receipt names this node for lean4/ObligationMonoid.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](nodes/PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) | WDP | `OPEN` | E3 | 502 | a replay receipt names this node for lean4/WdpBridgeObligations.lean, but the node's lean, rust and source fields do not cite it |
| [PG-PRIMDIFF-AXIOMS](nodes/PG-PRIMDIFF-AXIOMS.md) | PREGENESIS | `DEFINITION` | E3 | 497 | a replay receipt names this node for lean4/PrimdiffAxioms.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-DEGREE1-WINDOW](nodes/PG-WDP-DEGREE1-WINDOW.md) | WDP | `DEFINITION` | E3 | 496 | a replay receipt names this node for lean4/WdpDegree1Window.lean, but the node's lean, rust and source fields do not cite it |
| [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](nodes/L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) | L1_TO_L2 | `CONDITIONAL` | E3 | 461 | a replay receipt names this node for lean4/ResidualSectorWeights.lean, but the node's lean, rust and source fields do not cite it |
| [PG-ROOT-DIFF-STRUCTURE](nodes/PG-ROOT-DIFF-STRUCTURE.md) | PREGENESIS | `ADMITTED_PRIMITIVE` | E3 | 233 | a replay receipt names this node for lean4/RootDiffStructure.lean, but the node's lean, rust and source fields do not cite it |
| [PG-ADMISSION-FLOOR](nodes/PG-ADMISSION-FLOOR.md) | PREGENESIS | `PROVED_LEAN` | E3 | 129 | a replay receipt names this node for lean4/AdmissionFloor.lean, but the node's lean, rust and source fields do not cite it |
| [PG-HISTORY-REPORT-CRITERION](nodes/PG-HISTORY-REPORT-CRITERION.md) | PREGENESIS | `PROVED_LEAN` | E3 | 58 | a replay receipt names this node for lean4/HistoryReport.lean, but the node's lean, rust and source fields do not cite it |
| [PG-PREGEN-CONSTRUCTIVE-SUMMARY](nodes/PG-PREGEN-CONSTRUCTIVE-SUMMARY.md) | PREGENESIS | `PROVED_LEAN` | E3 | 42 | a replay receipt names this node for lean4/PregenConstructive.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-QUOTIENT-EXACT-SEQUENCE](nodes/PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) | WDP | `PROVED_LEAN` | E3 | 40 | a replay receipt names this node for lean4/WdpQuotientSequence.lean, but the node's lean, rust and source fields do not cite it |
| [PG-FREE-MONOID-NONISO](nodes/PG-FREE-MONOID-NONISO.md) | PREGENESIS | `PROVED_LEAN` | E3 | 37 | a replay receipt names this node for lean4/FreeMonoidNoniso.lean, but the node's lean, rust and source fields do not cite it |
| [FSP-WILSON-DIRAC-GAMMA5](nodes/FSP-WILSON-DIRAC-GAMMA5.md) | FERMION_SIGN | `IMPORTED_ASSUMPTION` | E3 | 22 | a replay receipt names this node for lean4/CampaignFspWilsonDiracGamma5.lean, but the node's lean, rust and source fields do not cite it |
| [PG-SN-OFF-IMAGE-REFUSAL](nodes/PG-SN-OFF-IMAGE-REFUSAL.md) | PREGENESIS | `PROVED_LEAN` | E3 | 19 | a replay receipt names this node for lean4/SnOffImageRefusal.lean, but the node's lean, rust and source fields do not cite it |
| [L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE](nodes/L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.md) | L1_TO_L2 | `PROVED_LEAN` | E3 | 12 | a replay receipt names this node for lean4/PhaseBlindFiber.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-PROTECTED-QUESTIONS](nodes/PG-WDP-PROTECTED-QUESTIONS.md) | WDP | `PROVED_LEAN` | E3 | 9 | a replay receipt names this node for lean4/WdpProtectedQuestions.lean, but the node's lean, rust and source fields do not cite it |
| [L1-WDP-REALIFICATION-J](nodes/L1-WDP-REALIFICATION-J.md) | L1_TO_L2 | `DEFINITION` | E3 | 5 | a replay receipt names this node for lean4/RealificationJ.lean, but the node's lean, rust and source fields do not cite it |
| [PG-CHAIN-RETRACTION](nodes/PG-CHAIN-RETRACTION.md) | PREGENESIS | `PROVED_LEAN` | E3 | 5 | a replay receipt names this node for lean4/ChainRetraction.lean, but the node's lean, rust and source fields do not cite it |
| [L1-U1-SELECTOR-OTHER-SEGMENT](nodes/L1-U1-SELECTOR-OTHER-SEGMENT.md) | L1_TO_L2 | `OPEN` | E3 | 0 | a replay receipt names this node for lean4/U1SelectorSegment.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-DIAGNOSTIC-NOT-ROUTING](nodes/PG-WDP-DIAGNOSTIC-NOT-ROUTING.md) | WDP | `DEFINITION` | E3 | 0 | a replay receipt names this node for lean4/WdpDiagnosticRouting.lean, but the node's lean, rust and source fields do not cite it |
| [PG-WDP-GROWTH-NO-REPAIR](nodes/PG-WDP-GROWTH-NO-REPAIR.md) | WDP | `PROVED_LEAN` | E3 | 0 | a replay receipt names this node for lean4/WdpGrowthNoRepair.lean, but the node's lean, rust and source fields do not cite it |

