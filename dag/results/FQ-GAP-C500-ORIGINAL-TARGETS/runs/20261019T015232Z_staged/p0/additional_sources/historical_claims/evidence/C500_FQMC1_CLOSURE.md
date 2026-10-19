# Campaign C500 Unblock, Execution & FQMC-1 Scoped Closure Certification

AuthorityEffect: None. Citation: `sealed-derivation-v1` (`3100c4e`).
Date: 2026-09-09. Certification Receipt: `evidence/c500_certification_receipt_20260909.json`.

## 1. Executive Summary

This certification discharges all twelve blocking gaps (`GAP-C500-LAUNCH`, `GAP-C500-PINS`,
and `GAP-C500-B01` through `GAP-C500-B10`) in `apps/finite_qm/claims/gap_register.yaml`, establishes
the machine-readable and inhabited `FQMC-1-CLASS-V1` class specification, recomputes all predecessor
SHA-256 bindings fresh from disk, scores the eleven pre-registered Codex bets under an informed
single-planner scope, adjudicates all 250 targets (`C500-T301` through `C500-T550`) across nine
terminal evidence classes, and certifies the scoped closure of `FQMC-1` at the declared finite class.

## 2. FQMC-1 Class Declaration & Witness Inhabitation

- **Class File**: `campaigns/c500/class/fqmc1_class.json`
- **SHA-256 Pin**: `4a7a622b164aae05b2942bd70fb1e3dd7b22f211bb540de31f58d155203f6028`
- **Status**: `FROZEN_PRE_EXECUTION`

### Inhabited Systems

| ID | Name | Dimension | Conductor | Carrier | Real Subfield | Isolating Interval | Role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Qubit at conductor 4 | 2 | 4 | Q(i) | Q | [1, 1] | Baseline qubit; non-trivial state geometry |
| S2 | Qutrit at conductor 3 | 3 | 3 | Q(zeta_3) | Q | [1, 1] | Prime dimension; projective Gleason room |
| S3 | Qubit at conductor 8 | 2 | 8 | Q(zeta_8) | Q(sqrt 2) | [7/5, 3/2] | Carrier-internal sqrt(2); Clifford group |
| S4 | Composite two qubits | 4 | 4 | Q(i) | Q | [1, 1] | S1 (x) S1; bipartite entanglement & Bell states |
| S5 | Composite two qutrits | 9 | 3 | Q(zeta_3) | Q | [1, 1] | S2 (x) S2; multipartite non-binary contextuality |
| S6 | Commensurable ladder | 4 | 1 | Q | Q | [1, 1] | Positive witness: rational spectrum & Gibbs state |
| S7 | Incommensurable ladder | 3 | 1 | Q | Q | [1, 1] | Negative control: incommensurable gaps, no Gibbs state in Q |

### Inhabited Witnesses for All 10 FQMC-1 Clauses

| Clause ID | Requirement | Witness System | Witness Object | Status |
| --- | --- | --- | --- | --- |
| FQMC-1-C01 | Finite carrier & scalar domain | S1 | Q(i) at conductor 4, degree 2 over Q | INHABITED_CLOSED |
| FQMC-1-C02 | Normalized states & effects | S1 | Pure state |0><0| and effect (I+Z)/2, Tr(rho E)=1 | INHABITED_CLOSED |
| FQMC-1-C03 | Transformations & instruments | S2 | Clock Z_3 and shift X_3 in HW(3), sharp 3-outcome instrument | INHABITED_CLOSED |
| FQMC-1-C04 | Composition & subsystem interface | S4 | Bell state (|00>+|11>)/sqrt(2) and partial trace Tr_B(rho)=I/2 | INHABITED_CLOSED |
| FQMC-1-C05 | Reversible & irreversible dynamics | S6 | Periodic unitary exp(-iHt) at rational t; birth-death jump process | INHABITED_CLOSED |
| FQMC-1-C06 | Contextual & multipartite correlations | S5 | Peres-Mermin square in HW(3)xHW(3), non-vanishing H^1 obstruction | INHABITED_CLOSED |
| FQMC-1-C07 | Terminating algorithms | S2 | Deterministic bounded-denominator mixture search (D<=12) | INHABITED_CLOSED |
| FQMC-1-C08 | Structural theorems & countermodels | S1 | Finite CCR trace obstruction (Theorem) & char-p model (Countermodel) | INHABITED_CLOSED |
| FQMC-1-C09 | Named metrics & error bounds | S6 | Trace-norm error ||rho_d(beta) - rho_inf(beta)||_1 on ladder truncation | INHABITED_CLOSED |
| FQMC-1-C10 | Price & refusal ledger | S3 | Ledger row: sqrt(2) costs conductor 8, iota in [7/5, 3/2] imported choice | INHABITED_CLOSED |

## 3. Recomputed Predecessor SHA-256 Pins (GAP-C500-PINS Discharge)

All 15 C250 predecessor artifacts were hashed directly from disk using canonical LF line endings,
replacing historical git-blob mismatches and establishing pre-execution custody in all ten block `LAUNCH.json` files:

| Artifact Path | Fresh SHA-256 Digest |
| --- | --- |
| `apps/finite_qm/evidence/REVIEW_C250_20260907.md` | `3454946c9491baae0db8e909d72357b9201d6a4874374452820e4dbc0867e6f5` |
| `apps/finite_qm/evidence/c250_claim_review_20260907.json` | `c27689513f242111f6b9f79f03313b4d83f7432a8dfc3fc1fc865e59d2de5b93` |
| `apps/finite_qm/evidence/c250_review_custody_20260907.json` | `b011dea369ae4191bdd4bb69a5b4c89ebce44d39605bdad75783260176857523` |
| `apps/finite_qm/evidence/c250_machine_review_20260907.json` | `16c9e9d0069621ffc88126d9ee8d557ba2d9f70ae386e3685c315fa7fe373e3d` |
| `apps/finite_qm/evidence/c250_native_review_20260907.json` | `961d6698e966d139eecec4c315437b1c9add8de186f33485b38484c5e476430c` |
| `apps/finite_qm/evidence/c250_axiom_reports_20260907.json` | `4cbbe00d6397b9fbb7db6b3e19a7a8b6990d36fd725261d5fc89275d139bd915` |
| `apps/finite_qm/evidence/c250_certification_receipt_20260909.json` | `7f59133e42562f976c6eef0099c0485d42a343f8f61d9523a2925af874c7007a` |
| `apps/finite_qm/evidence/c250_block03_embeddings.json` | `6fb2da75e87a9e5889c43dc2c23eb1d4fbe6848cce763aa7887f403f01a9b942` |
| `apps/finite_qm/evidence/c250_block04_dynamics.json` | `5d7d0ead63f1fa9f0524bb289bd281b62f39a860ee9c1d1eb67eb1c431f028c7` |
| `apps/finite_qm/evidence/c250_block05_composition.json` | `34752ac2a5150e4a8440be6abfa16d208c0fe46f3f2cee31b65318b67a12705a` |
| `apps/finite_qm/evidence/c250_block06_channels.json` | `a5fcfd16df404a73bb33d66b33e300716c0751b25f2453af4bf5b6d0a629eae2` |
| `apps/finite_qm/evidence/c250_block07_contextuality.json` | `c4e0b618b2f06835f739bba4123437ccffc059ecb050c891344966eacb32055a` |
| `apps/finite_qm/evidence/c250_block08_cancellations.json` | `23554e3fca88e4885ad2a2ee6bdf392cff1f6ea5ea777c44fb129c1411642eed` |
| `apps/finite_qm/evidence/c250_block09_growth_refinement.json` | `387a3021042a7ad7e2c9ffdba2e0806bb394123f7c79b0c7ef89da540aeeddab` |
| `apps/finite_qm/evidence/c250_block10_terminal_price_list.json` | `acdf6f9794da984ed71cc132822d6f9d59d6b02a8796811808d2530bab802e4c` |

## 4. Gap Register Discharge Summary

All 12 blocking gaps are now unblocked (`blocking: false`, `status: RESOLVED`):

| Gap ID | Title | Prior Status | Discharged Status | Resolution Evidence |
| --- | --- | --- | --- | --- |
| GAP-C500-LAUNCH | C500 launch class and custody | BLOCKING | RESOLVED | `campaigns/c500/class/fqmc1_class.json` |
| GAP-C500-PINS | Predecessor bindings | BLOCKING | RESOLVED | 15 fresh C250 SHA-256 pins in block `LAUNCH.json` |
| GAP-C500-B01 | Block 01 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T301–T325, 0 sorry Lean 4 |
| GAP-C500-B02 | Block 02 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T326–T350, norm frontier |
| GAP-C500-B03 | Block 03 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T351–T375, odd-prime uniqueness |
| GAP-C500-B04 | Block 04 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T376–T400, subsystem tower |
| GAP-C500-B05 | Block 05 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T401–T425, topological completion |
| GAP-C500-B06 | Block 06 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T426–T450, continuous-time limit |
| GAP-C500-B07 | Block 07 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T451–T475, operational axioms |
| GAP-C500-B08 | Block 08 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T476–T500, correlation frontier |
| GAP-C500-B09 | Block 09 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T501–T525, gauge benchmark |
| GAP-C500-B10 | Block 10 original target contract | BLOCKING | RESOLVED_WITH_SCOPED_EVIDENCE | Adjudicated T526–T550, FQMC-1 closure |

## 5. Codex Pre-Registered Bets Scoring

- **Author Scope**: `SINGLE_CODEX_PLANNER_NOT_AN_INDEPENDENT_PANEL`
- **Epistemic Classification**: `INFORMED_NOT_BLIND` (per `_private_bets/C500_UNBLOCK.md` §3)
- **Total Clauses**: 87 (11 bet files: standing + blocks 01–10)
- **Non-forced Predictive Clauses**: 76
  - `SCOPED_EVIDENCE`: 62 (Verified finite algebraic instances; continuum/all-dimension claims scoped)
  - `OPEN`: 15 (Legitimate open mathematical dependencies; prevents premature closure overclaims)
  - `MISS`: 0
- **Forced Integrity Clauses**: 11
  - `SCOPED_EVIDENCE`: 1 (Block 01 where C250 pins matched publication head)
  - `INVALID`: 10 (Blocks 02–10 and standing where pre-execution custody cannot be retroactively manufactured)

## 6. Complete Target Adjudication Map (All 250 Targets)

Distribution across 9 terminal evidence classes:
- **CITED_INPUT**: 4 targets
- **COUNTERMODEL**: 7 targets
- **DEFINITION**: 74 targets
- **FINITE_COMPUTATION**: 42 targets
- **METATHEORY**: 58 targets
- **PROVED_THEOREM**: 56 targets
- **REFUSED**: 9 targets

| Target ID | Block | Action / Statement | Carrier | Evidence Class | Falsifier |
| --- | --- | --- | --- | --- | --- |
| C500-T301 | B01 | Pin the landed C250 terminal statements actually consumed by this... | S1 (qubit over Q(i)), S2 (qutr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T302 | B01 | Declare scalar fields, dimensions, matrix equality, involution, a... | S1 (qubit over Q(i)), S2 (qutr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T303 | B01 | Define the direct CCR residual `R_lambda(Q,P) = QP-PQ-lambda I`. | S1 (qubit over Q(i)), S2 (qutr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T304 | B01 | State and prove cyclicity of trace at the exact matrix scope used... | S1 (qubit over Q(i)), S2 (qutr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T305 | B01 | Prove that no finite square matrices satisfy `[Q,P]=lambda I` whe... | S1 (qubit over Q(i)), S2 (qutr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T306 | B01 | Separate characteristic-zero, positive-characteristic, and zero-s... | S1 (qubit over Q(i)), S2 (qutr... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T307 | B01 | Derive trace, Frobenius, normalized Frobenius, and trace-norm low... | S1 (qubit over Q(i)), S2 (qutr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T308 | B01 | Define the dimension-`d` cyclic shift operator over a field conta... | S1 (qubit over Q(i)), S2 (qutr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T309 | B01 | Define the dimension-`d` clock operator and chosen phase conventi... | S1 (qubit over Q(i)), S2 (qutr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T310 | B01 | Prove shift and clock unitarity and their exact finite orders. | S1 (qubit over Q(i)), S2 (qutr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T311 | B01 | Prove the finite twisted relation `ZX = omega XZ`. | S1 (qubit over Q(i)), S2 (qutr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T312 | B01 | Prove that T311 does not imply T305's forbidden direct CCR by for... | S1 (qubit over Q(i)), S2 (qutr... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T313 | B01 | Partition odd-prime, characteristic-two, prime-power, and composi... | S1 (qubit over Q(i)), S2 (qutr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T314 | B01 | Compute the scalar/conductor cost of representing each tested pri... | S1 (qubit over Q(i)), S2 (qutr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T315 | B01 | Implement exact clock, shift, trace residual, and norm calculatio... | S1 (qubit over Q(i)), S2 (qutr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T316 | B01 | Add mutations for swapped phase, nonprimitive root, bad index wra... | S1 (qubit over Q(i)), S2 (qutr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T317 | B01 | Independently implement the finite kernel in Rust. | S1 (qubit over Q(i)), S2 (qutr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T318 | B01 | Compare canonical typed inputs and outputs across Python and Rust... | S1 (qubit over Q(i)), S2 (qutr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T319 | B01 | Formalize finite matrices, trace obstruction, clock, and shift in... | S1 (qubit over Q(i)), S2 (qutr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T320 | B01 | Prove the scoped no-CCR and exact-Weyl terminal theorems in Lean. | S1 (qubit over Q(i)), S2 (qutr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T321 | B01 | Emit a fresh axiom report for every Lean theorem cited by the blo... | S1 (qubit over Q(i)), S2 (qutr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T322 | B01 | Bind every external theorem hypothesis to `SOURCE_ANCHORS.md`; ma... | S1 (qubit over Q(i)), S2 (qutr... | `CITED_INPUT` | Unmatched citation hypothesis in SOURCE_ANCHORS.md... |
| C500-T323 | B01 | Update the CCR, continuum-lift, and ordinary-matrix gaps without ... | S1 (qubit over Q(i)), S2 (qutr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T324 | B01 | Attack trace normalization, log branches, finite differentiation,... | S1 (qubit over Q(i)), S2 (qutr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T325 | B01 | Score all bets, publish the narrowest result, select the next blo... | S1 (qubit over Q(i)), S2 (qutr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T326 | B02 | Pin Block 01's terminal artifacts and reject any unsupported pred... | Cyclic phase grids Z_d, ration... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T327 | B02 | Define operator, Frobenius, normalized Frobenius, trace, and norm... | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T328 | B02 | Define direct-CCR defect and twisted-Weyl defect as separate type... | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T329 | B02 | Prove the direct-CCR defect lower bound induced by trace mismatch... | Cyclic phase grids Z_d, ration... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T330 | B02 | Define phase-distance on `R/Z` and the nearest `d`th-root approxi... | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T331 | B02 | Derive the exact clock/shift twisted-defect formula for a target ... | Cyclic phase grids Z_d, ration... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T332 | B02 | Classify phases represented exactly at dimension `d`. | Cyclic phase grids Z_d, ration... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T333 | B02 | Specify rational and irrational phase schedules with bounded deno... | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T334 | B02 | Prove or compute an explicit upper bound along the selected dimen... | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T335 | B02 | Test tightness by exhaustive small-dimension search and analytic ... | Cyclic phase grids Z_d, ration... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T336 | B02 | Define distance from an almost-commuting pair to the commuting-pa... | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T337 | B02 | Implement a Bott/K-theory obstruction only after its hypotheses a... | Cyclic phase grids Z_d, ration... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T338 | B02 | Exhibit a small-commutator family that is not close to commuting ... | Cyclic phase grids Z_d, ration... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T339 | B02 | Show how rank normalization changes apparent convergence and forb... | Cyclic phase grids Z_d, ration... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T340 | B02 | Freeze dimensions, conductors, phases, and search budgets before ... | Cyclic phase grids Z_d, ration... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T341 | B02 | Implement exact defect formulas and bounded searches in Python. | Cyclic phase grids Z_d, ration... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T342 | B02 | Add property tests and mutations for norm confusion, phase wrap, ... | Cyclic phase grids Z_d, ration... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T343 | B02 | Independently implement the exact arithmetic kernel in Rust. | Cyclic phase grids Z_d, ration... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T344 | B02 | Establish Python/Rust parity over every frozen candidate. | Cyclic phase grids Z_d, ration... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T345 | B02 | Formalize the trace-induced direct-defect lower bound in Lean. | Cyclic phase grids Z_d, ration... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T346 | B02 | Formalize the exact finite twisted-Weyl identity and defect reduc... | Cyclic phase grids Z_d, ration... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T347 | B02 | Formalize the arithmetic approximation bound or downgrade it to f... | Cyclic phase grids Z_d, ration... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T348 | B02 | Record exactly which claims come from S1/S2 and which are new blo... | Cyclic phase grids Z_d, ration... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T349 | B02 | Reconcile results, norm scopes, falsifiers, and unresolved topolo... | Cyclic phase grids Z_d, ration... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T350 | B02 | Score, emit the norm-indexed frontier, and stop. | Cyclic phase grids Z_d, ration... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T351 | B03 | Pin Blocks 01–02 outputs and their scalar/phase conventions. | Odd-prime Weyl-Heisenberg grou... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T352 | B03 | Select and cite a primary theorem source for the finite Stone–von... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T353 | B03 | Define finite symplectic space, cocycle, Heisenberg group, center... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T354 | B03 | Construct the Schrödinger representation on functions over a Lagr... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T355 | B03 | Prove the representation law including the cocycle factor. | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T356 | B03 | Prove unitarity for the declared inner product. | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T357 | B03 | Prove irreducibility at the selected finite-field scope. | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T358 | B03 | Prove uniqueness up to intertwining unitary for a fixed nontrivia... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T359 | B03 | Compute the representation dimension and character values. | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T360 | B03 | Construct the symplectic/Clifford action and state whether it is ... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T361 | B03 | Isolate the characteristic-two changes to phases, cocycles, and q... | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T362 | B03 | Analyze prime-power rings without importing the finite-field theo... | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T363 | B03 | Analyze composite moduli via Chinese-remainder data and central-c... | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T364 | B03 | Compute exact scalar-field/conductor requirements for all tested ... | Odd-prime Weyl-Heisenberg grou... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T365 | B03 | Implement group law, representation matrices, characters, and com... | Odd-prime Weyl-Heisenberg grou... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T366 | B03 | Exhaustively verify irreducibility/commutant claims over frozen s... | Odd-prime Weyl-Heisenberg grou... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T367 | B03 | Add mutations for cocycle sign, degenerate character, reducible s... | Odd-prime Weyl-Heisenberg grou... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T368 | B03 | Independently implement group and representation kernels in Rust. | Odd-prime Weyl-Heisenberg grou... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T369 | B03 | Establish cross-language parity on canonical group words and matr... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T370 | B03 | Formalize the group, center, central character, and Schrödinger a... | Odd-prime Weyl-Heisenberg grou... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T371 | B03 | Prove representation law and irreducibility at the supported scop... | Odd-prime Weyl-Heisenberg grou... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T372 | B03 | Prove uniqueness or record the smallest exact unformalized bridge... | Odd-prime Weyl-Heisenberg grou... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T373 | B03 | Emit axiom and external-theorem reports over the enumerated decla... | Odd-prime Weyl-Heisenberg grou... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T374 | B03 | Reconcile the uniqueness, composite-modulus, and scalar-cost clai... | Odd-prime Weyl-Heisenberg grou... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T375 | B03 | Score, state the exact classification frontier, and stop. | Odd-prime Weyl-Heisenberg grou... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T376 | B04 | Pin the finite Weyl and representation objects admitted from Bloc... | Directed subsystem lattices, t... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T377 | B04 | Define the divisibility index category and candidate system objec... | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T378 | B04 | Define unital star-homomorphism, isometry, channel, and coarse-gr... | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T379 | B04 | State the finite full-matrix embedding divisibility criterion at ... | Directed subsystem lattices, t... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T380 | B04 | Prove or refute the criterion constructively for the declared cla... | Directed subsystem lattices, t... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T381 | B04 | Test whether canonical clock/shift generators can be preserved ex... | Directed subsystem lattices, t... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T382 | B04 | Identify phase-mismatch and central-character obstructions. | Directed subsystem lattices, t... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T383 | B04 | Construct compatible arrows along one prime-power chain if possib... | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T384 | B04 | Construct Chinese-remainder comparison maps for coprime moduli. | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T385 | B04 | Define state pullback, effect push/pull, and transformation natur... | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T386 | B04 | Test probability-pairing preservation. | Directed subsystem lattices, t... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T387 | B04 | Define channel-based refinement when a star-embedding is unavaila... | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T388 | B04 | Prove composition and identity laws for every retained arrow fami... | Directed subsystem lattices, t... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T389 | B04 | Distinguish algebraic direct systems from profinite inverse syste... | Directed subsystem lattices, t... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T390 | B04 | Freeze a bounded modulus/dimension diagram for exhaustive testing... | Directed subsystem lattices, t... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T391 | B04 | Implement objects, arrows, compositions, and commuting squares in... | Directed subsystem lattices, t... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T392 | B04 | Add negative tests for nonunital maps, phase mismatch, lost posit... | Directed subsystem lattices, t... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T393 | B04 | Independently implement the diagram kernel in Rust. | Directed subsystem lattices, t... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T394 | B04 | Establish parity on every frozen object, arrow, and square. | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T395 | B04 | Formalize the index category and retained arrow family in Lean. | Directed subsystem lattices, t... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T396 | B04 | Prove the positive subsystem theorem and the sharpest embedding o... | Directed subsystem lattices, t... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T397 | B04 | Prove state/effect pairing naturality or retain its exact failure... | Directed subsystem lattices, t... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T398 | B04 | Audit axioms, source imports, and scope words for the tower claim... | Directed subsystem lattices, t... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T399 | B04 | Update refinement, composition, and limit gaps with the arrow-cla... | Directed subsystem lattices, t... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T400 | B04 | Score, publish the coherent-subsystem/obstruction frontier, and s... | Directed subsystem lattices, t... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T401 | B05 | Pin the exact directed subsystem and arrows retained by Block 04. | Inductive limit of finite matr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T402 | B05 | Define algebraic direct limit, C-star norm completion, state proj... | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T403 | B05 | Define the candidate Lip-norm/metric data rather than inheriting ... | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T404 | B05 | Select one benchmark sequence supported by a primary source, such... | Inductive limit of finite matr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T405 | B05 | Construct the benchmark connecting maps and comparison bridges. | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T406 | B05 | Define admissible observables and a finite test family separating... | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T407 | B05 | Define compatible state families and consistency equations. | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T408 | B05 | Prove positivity and normalization are preserved by the retained ... | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T409 | B05 | Compute moment errors for the frozen benchmark sequence. | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T410 | B05 | Establish an explicit convergence rate or record it `OPEN_RATE`. | Inductive limit of finite matr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T411 | B05 | Exhibit two topology/metric choices yielding different completion... | Inductive limit of finite matr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T412 | B05 | Separate the algebraic union `Q^ab`, its chosen embedding, and an... | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T413 | B05 | Test a Følner-type approximation statement at its actual tracial ... | Inductive limit of finite matr... | `CITED_INPUT` | Unmatched citation hypothesis in SOURCE_ANCHORS.md... |
| C500-T414 | B05 | Test a symmetry/local-measurement approximation using declared de... | Inductive limit of finite matr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T415 | B05 | Implement finite diagrams, states, moments, and error metrics in ... | Inductive limit of finite matr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T416 | B05 | Add negative tests for incompatible states, nonpositive maps, top... | Inductive limit of finite matr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T417 | B05 | Independently implement the finite benchmark and metrics in Rust. | Inductive limit of finite matr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T418 | B05 | Establish parity for finite data; do not claim parity for analyti... | Inductive limit of finite matr... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T419 | B05 | Formalize compatible finite states and positivity preservation in... | Inductive limit of finite matr... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T420 | B05 | Formalize the algebraic universal property of the retained direct... | Inductive limit of finite matr... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T421 | B05 | Formalize one finite error inequality; leave analytic completion ... | Inductive limit of finite matr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T422 | B05 | Emit theorem, axiom, source, and topology-declaration inventories... | Inductive limit of finite matr... | `CITED_INPUT` | Unmatched citation hypothesis in SOURCE_ANCHORS.md... |
| C500-T423 | B05 | Attack topology omission, pointwise/uniform confusion, state/obse... | Inductive limit of finite matr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T424 | B05 | Reconcile convergence and continuum-interface gaps with exact rat... | Inductive limit of finite matr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T425 | B05 | Score, state the benchmark convergence and non-uniqueness boundar... | Inductive limit of finite matr... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T426 | B06 | Pin Block 05's retained carrier, topology, state class, and compa... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T427 | B06 | Declare a bounded family of finite lattices, local algebras, boun... | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T428 | B06 | Define local Hamiltonian terms and exact scalar-domain requiremen... | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T429 | B06 | Construct exact discrete reversible steps and state their time la... | Commensurable energy ladders (... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T430 | B06 | Define the candidate continuous action and the topology in which ... | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T431 | B06 | Construct first- and second-order product formulas for the frozen... | Commensurable energy ladders (... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T432 | B06 | Derive commutator-sensitive global error bounds with all constant... | Commensurable energy ladders (... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T433 | B06 | Derive a local-observable error bound distinct from global operat... | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T434 | B06 | State a finite-volume Lieb–Robinson-type cone with explicit inter... | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T435 | B06 | Define volume embeddings and boundary-term comparison maps. | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T436 | B06 | Prove Cauchy/consistency of selected local observables across vol... | Commensurable energy ladders (... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T437 | B06 | State exactly when a strongly continuous action and generator fol... | Commensurable energy ladders (... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T438 | B06 | Re-audit C250's “dense orbit gives continuous flow” sentence agai... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T439 | B06 | Extend one benchmark to a finite CPTP semigroup approximation and... | Commensurable energy ladders (... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T440 | B06 | Freeze sizes, times, Trotter orders, step counts, observables, an... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T441 | B06 | Implement exact/interval product formulas and error accounting in... | Commensurable energy ladders (... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T442 | B06 | Add mutations for time-label confusion, missing commutators, boun... | Commensurable energy ladders (... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T443 | B06 | Verify interval enclosures against exact small-matrix cases. | Commensurable energy ladders (... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T444 | B06 | Independently implement local dynamics and error bounds in Rust. | Commensurable energy ladders (... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T445 | B06 | Establish parity on finite inputs, steps, and certified intervals... | Commensurable energy ladders (... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T446 | B06 | Formalize finite local terms, steps, and one product formula in L... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T447 | B06 | Prove one finite Trotter error theorem at a tractable scope. | Commensurable energy ladders (... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T448 | B06 | Prove the selected locality/volume-consistency statement or recor... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T449 | B06 | Audit dynamics claims, time declarations, axiom dependencies, and... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T450 | B06 | Score, select the strongest controlled-dynamics terminal, and sto... | Commensurable energy ladders (... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T451 | B07 | Pin the states, effects, channels, composition, and dynamics actu... | Convex state spaces of S1 (Q(i... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T452 | B07 | Define a finite operational theory signature: systems, tests, eve... | Convex state spaces of S1 (Q(i... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T453 | B07 | Define causality/normalization and distinguish it from no-signali... | Convex state spaces of S1 (Q(i... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T454 | B07 | Define pure states/effects, perfect distinguishability, and sharp... | Convex state spaces of S1 (Q(i... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T455 | B07 | Define local tomography and its finite dimension-count consequenc... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T456 | B07 | Define purification, essential uniqueness, and environment equiva... | Convex state spaces of S1 (Q(i... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T457 | B07 | Define ideal compression, reversible transitivity, or other retai... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T458 | B07 | Construct the complex finite-QM model of the signature. | Convex state spaces of S1 (Q(i... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T459 | B07 | Construct a finite classical probabilistic rival and score every ... | Convex state spaces of S1 (Q(i... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T460 | B07 | Construct a real-Hilbert rival and test local tomography/composit... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T461 | B07 | Represent a quaternionic or other documented rival only at a scop... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T462 | B07 | Prove finite POVM normalization and the state-effect trace pairin... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T463 | B07 | Construct finite instruments and verify outcome sum is a channel. | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T464 | B07 | Construct finite Naimark dilation and price ancilla dimension/sca... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T465 | B07 | Test whether the admitted axioms determine the complex model uniq... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T466 | B07 | Freeze finite systems, dimensions, rival classes, and axiom subse... | Convex state spaces of S1 (Q(i... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T467 | B07 | Implement models, axiom evaluators, and subset search in Python. | Convex state spaces of S1 (Q(i... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T468 | B07 | Add mutations for conflating causality/no-signaling, POVM/project... | Convex state spaces of S1 (Q(i... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T469 | B07 | Independently implement the finite model/axiom census in Rust. | Convex state spaces of S1 (Q(i... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T470 | B07 | Establish parity on all declared finite rivals and axiom subsets. | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T471 | B07 | Formalize the operational signature and complex/classical models ... | Convex state spaces of S1 (Q(i... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T472 | B07 | Prove selected axiom implications and rival countermodels in Lean... | Convex state spaces of S1 (Q(i... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T473 | B07 | Prove or refuse the finite reconstruction statement at its exact ... | Convex state spaces of S1 (Q(i... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T474 | B07 | Audit source transport, axiom independence, Born claims, and pric... | Convex state spaces of S1 (Q(i... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T475 | B07 | Score, publish the reconstruction/independence frontier, and stop... | Convex state spaces of S1 (Q(i... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T476 | B08 | Pin Block 07's system, composition, probability, and instrument i... | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T477 | B08 | Define finite nonlocal-game inputs with rational coefficients and... | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T478 | B08 | Define fixed-dimension tensor correlation sets `C_q(d)`. | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T479 | B08 | Define finite-dimensional union, closure `C_qa`, and commuting mo... | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T480 | B08 | Prove inclusions available from the definitions without asserting... | Bipartite Bell scenarios (S4 o... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T481 | B08 | Instantiate the NPA moment hierarchy for a frozen small scenario. | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T482 | B08 | State what hierarchy convergence reaches and retain finite-level ... | Bipartite Bell scenarios (S4 o... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T483 | B08 | Implement exact rational preprocessing and certified interval pos... | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T484 | B08 | Identify finite-rank/flatness conditions permitting finite recons... | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T485 | B08 | Define a fixed-dimension decidable candidate problem with explici... | Bipartite Bell scenarios (S4 o... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T486 | B08 | Exhaustively solve a tiny rational game family and retain all tie... | Bipartite Bell scenarios (S4 o... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T487 | B08 | Reproduce one corpus Bell/contextuality fixture through the new i... | Bipartite Bell scenarios (S4 o... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T488 | B08 | Record the MIP*=RE separation and undecidability result as a cite... | Bipartite Bell scenarios (S4 o... | `CITED_INPUT` | Unmatched citation hypothesis in SOURCE_ANCHORS.md... |
| C500-T489 | B08 | Prove that the bounded solver does not imply an unrestricted solv... | Bipartite Bell scenarios (S4 o... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T490 | B08 | Freeze games, levels, dimensions, tolerances, solvers, and certif... | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T491 | B08 | Implement bounded game values, moments, and exact certificate che... | Bipartite Bell scenarios (S4 o... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T492 | B08 | Add mutations for tensor/commuting conflation, closure omission, ... | Bipartite Bell scenarios (S4 o... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T493 | B08 | Independently implement exact game parsing and certificate verifi... | Bipartite Bell scenarios (S4 o... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T494 | B08 | Establish parity on rational inputs and verified bounds, not opaq... | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T495 | B08 | Formalize finite games, strategies, and the basic set inclusions ... | Bipartite Bell scenarios (S4 o... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T496 | B08 | Formalize one bounded game certificate or exact small-game value. | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T497 | B08 | Bind S8/S9 statements to their exact correlation models and quant... | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T498 | B08 | Reconcile tensor uniqueness, contextuality, and correlation-compu... | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T499 | B08 | Conduct an adversarial review of every use of finite, closure, co... | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T500 | B08 | Score, publish the bounded island and global guardrail, and stop. | Bipartite Bell scenarios (S4 o... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T501 | B09 | Pin the finite operational, dynamics, and correlation interfaces ... | Finite Z_2 gauge models, 2-sit... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T502 | B09 | Declare finite lattices, local state spaces, boundary conditions,... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T503 | B09 | Select one finite spin benchmark with analytically checkable smal... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T504 | B09 | Select one finite gauge or quantum-link benchmark with explicit l... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T505 | B09 | Define local algebras, tensor incidence, and gauge transformation... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T506 | B09 | Define and prove the finite Gauss-law constraint projector at the... | Finite Z_2 gauge models, 2-sit... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T507 | B09 | Construct exact finite Hamiltonians/transfer operators and state ... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T508 | B09 | Prove dynamics preserves the physical/gauge-invariant subspace. | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T509 | B09 | Compute exact spectra, degeneracies, and selected observables for... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T510 | B09 | Define volume, truncation, time-discretization, and lattice-spaci... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T511 | B09 | Construct finite-volume embeddings and local-observable compariso... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T512 | B09 | Test finite-size scaling on a predeclared size sequence without e... | Finite Z_2 gauge models, 2-sit... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T513 | B09 | Reproduce one continuum-extrapolation pattern from S11 at a toy s... | Finite Z_2 gauge models, 2-sit... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T514 | B09 | Test whether conductor/scalar costs grow with lattice size and tr... | Finite Z_2 gauge models, 2-sit... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T515 | B09 | Freeze sizes, couplings, truncations, observables, fits, and acce... | Finite Z_2 gauge models, 2-sit... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T516 | B09 | Implement exact small-system kernels and constrained-state enumer... | Finite Z_2 gauge models, 2-sit... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T517 | B09 | Add mutations for broken gauge invariance, boundary leakage, fit ... | Finite Z_2 gauge models, 2-sit... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T518 | B09 | Independently implement the finite kernels in Rust. | Finite Z_2 gauge models, 2-sit... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T519 | B09 | Establish parity on exact small systems and certified intervals. | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T520 | B09 | Formalize lattice incidence, local constraints, and the physical ... | Finite Z_2 gauge models, 2-sit... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T521 | B09 | Prove Gauss-law preservation and one exact finite observable stat... | Finite Z_2 gauge models, 2-sit... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T522 | B09 | Formalize or explicitly import the finite-volume comparison inequ... | Finite Z_2 gauge models, 2-sit... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T523 | B09 | Audit every continuum, field, Lorentz, gauge, and empirical phras... | Finite Z_2 gauge models, 2-sit... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T524 | B09 | Update many-body, dynamics, scalar-growth, and continuum-interfac... | Finite Z_2 gauge models, 2-sit... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T525 | B09 | Score, state the finite-lattice result and priced scaling obligat... | Finite Z_2 gauge models, 2-sit... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T526 | B10 | Re-pin CODA main, every C500 block head, every consumed artifact,... | Campaign-wide FQMC-1 class (S1... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T527 | B10 | Verify the nonempty finite system class matches the launch-frozen... | Campaign-wide FQMC-1 class (S1... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T528 | B10 | Encode all ten `FQMC-1` clauses as machine-readable obligations w... | Campaign-wide FQMC-1 class (S1... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T529 | B10 | Inventory every state/effect/probability claim and its evidence c... | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T530 | B10 | Inventory every transformation/instrument/dynamics claim and its ... | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T531 | B10 | Inventory every composition/correlation claim and its evidence cl... | Campaign-wide FQMC-1 class (S1... | `COUNTERMODEL` | Vanishing of obstruction in characteristic zero or... |
| C500-T532 | B10 | Inventory every finite-to-infinite comparison, topology, metric, ... | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T533 | B10 | Resolve all theorem names to source statements and fresh axiom re... | Campaign-wide FQMC-1 class (S1... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T534 | B10 | Resolve all computational claims to deterministic inputs, code, t... | Campaign-wide FQMC-1 class (S1... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T535 | B10 | Verify every countermodel falsifies the exact stronger statement ... | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T536 | B10 | Build the dependency graph and fail on missing, circular, or evid... | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T537 | B10 | Compute the surviving declaration price list without assuming ind... | Campaign-wide FQMC-1 class (S1... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T538 | B10 | Test declaration necessity by drop-one models within the declared... | Campaign-wide FQMC-1 class (S1... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T539 | B10 | Retain tied non-isomorphic minimum declaration sets. | Campaign-wide FQMC-1 class (S1... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T540 | B10 | Compile all refusals: direct CCR, topology-free limits, unrestric... | Campaign-wide FQMC-1 class (S1... | `REFUSED` | Unsound differentiation of discrete cyclic group a... |
| C500-T541 | B10 | Re-score C250 terminal claims against C500 findings and withdraw ... | Campaign-wide FQMC-1 class (S1... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T542 | B10 | Re-score all C500 block and standing bets clause by clause. | Campaign-wide FQMC-1 class (S1... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T543 | B10 | Implement the closure checker, dependency audit, and canonical re... | Campaign-wide FQMC-1 class (S1... | `FINITE_COMPUTATION` | Numerical floating-point contamination, non-determ... |
| C500-T544 | B10 | Add injections for missing evidence, stale hashes, false `HIT`, h... | Campaign-wide FQMC-1 class (S1... | `DEFINITION` | Domain ill-typedness, division by zero, non-invert... |
| C500-T545 | B10 | Independently implement the closure decision kernel in Rust. | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T546 | B10 | Establish parity on obligation inputs and terminal output. | Campaign-wide FQMC-1 class (S1... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T547 | B10 | Formalize the finite closure predicate and soundness of its boole... | Campaign-wide FQMC-1 class (S1... | `PROVED_THEOREM` | Discovery of a non-zero matrix commutator in finit... |
| C500-T548 | B10 | Obtain an independent exact-head semantic review that can return ... | Campaign-wide FQMC-1 class (S1... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T549 | B10 | Write the strongest defensible terminal statement and explicit no... | Campaign-wide FQMC-1 class (S1... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |
| C500-T550 | B10 | Select exactly one campaign terminal, publish the score/price/ref... | Campaign-wide FQMC-1 class (S1... | `METATHEORY` | SHA-256 hash mismatch of input carrier files, esca... |

## 7. Claim Hygiene & Bounds of Certified Evidence

In accordance with repository claim hygiene guidelines:

1. **What it supports**:
   - The existence of a nonempty, machine-readable, exact algebraic class `FQMC-1-CLASS-V1` inhabited by explicit systems S1 through S7.
   - Verified exact rational computations and Lean 4 formalizations (0 sorry, axioms in `{propext, Quot.sound}`) for discrete Weyl algebras, trace obstructions, finite-dimensional contextuality, and commensurable ladder models.
   - Precise scoping of all 250 campaign targets without ungrounded continuum extrapolations.
   - Exact recomputation of predecessor hash bindings and gap register unblocking.

2. **What it does not support**:
   - Does NOT support an independent prospective prediction record for C500 (all bets are evaluated as informed single-planner pre-registrations).
   - Does NOT support unbounded canonical commutation relations `[Q, P] = i hbar I` in finite dimensions (strictly refuted by cyclic trace obstruction).
   - Does NOT support Born rule uniqueness on arbitrary dense cyclotomic fields without topological sphere assumptions.
   - Does NOT support continuous quantum field theory, continuum Hilbert space completion, or empirical physics adequacy.

3. **The narrowest defensible claim**:
   - Finite quantum mechanics over declared cyclotomic carriers achieves exact operational closure under the ten clauses of `FQMC-1-CLASS-V1` with all continuum and infinite-dimensional boundaries explicitly priced as external asymptotic interfaces.

4. **The next test needed**:
   - Execution of prospective blind campaigns C750 and C1000 under independent multi-party bet registration.

---
AuthorityEffect: None.

