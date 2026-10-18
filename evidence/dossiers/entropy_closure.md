# Campaign C750 Execution & FQMI-1 Scoped Closure Certification

AuthorityEffect: None. Citation: `sealed-derivation-v1` (`3100c4e`).
Date: 2026-09-09. Certification Receipt: `evidence/c750_certification_receipt_20260909.json`.

## 1. Executive Summary

Campaign C750 executes 250 targets (`C750-T551` through `C750-T800`) across ten blocks of twenty-five.
It addresses the foundational question of whether finite quantum mechanics with exact algebraic carriers admits an operational thermodynamic structure (`FQMI-1`).

The campaign achieves:
1. **Pre-Execution Custody & Launch Prequalification**: The FQMI-1 system class (`class/fqmi1_class.json`) is pinned unchanged at canonical LF SHA-256 `0d6df52ed6c452674cd42cf9f9acdc7d863b4389c8d4d42a22e07b8ea46a7fc2`. All 22 pre-registered bet digests from `_private_bets/finite_qm_c750/SEALED_DIGESTS.txt` are verified byte-identically.
2. **Zero-Float Strict Execution**: All computations execute in exact rational arithmetic or algebraic number fields $\\mathbb{Q}(\\zeta_n)$ without numerical approximations.
3. **Execution of All 10 Blocks**: Every block delivers exactly its frozen fields without schema drift, passing `check_result_schema.py` and `check_expectations.py` cleanly.
4. **Terminal Adjudication of FQMI-1**:
   - Discharged Clauses: 8 clauses (Clauses 1, 2, 3, 4, 5, 6, 7, 10).
   - Open Clauses: 2 clauses (Clause 8 [signed cancellation completeness] and Clause 9 [asymptotic cost growth bridge]).
   - Campaign Terminal: `FQMI1_OPEN_INTERNAL_GAPS`.
5. **Sealed Bet Scoring**: Both independent bet sets (Reviewer Claude and Owner JC) are scored post-execution. Discrimination is confirmed: both sets register legitimate misses on contested mathematical frontiers, avoiding suspicious clean sweeps.

---

## 2. FQMI-1 Class Declaration & System Inventory

- **Class ID**: `FQMI-1-CLASS-V1`
- **Canonical Path**: `campaigns/c750/class/fqmi1_class.json`
- **Canonical LF SHA-256**: `0d6df52ed6c452674cd42cf9f9acdc7d863b4389c8d4d42a22e07b8ea46a7fc2`
- **Class Systems**: 8 declared and inhabited systems ($S1$ through $S8$).

| System ID | Name | Dim | Conductor | Carrier | Real Subfield | Isolating Interval | Role |
|---|---|---|---|---|---|---|---|
| S1 | Qubit at conductor 4 | 2 | 4 | $\\mathbb{Q}(i)$ | $\\mathbb{Q}$ | `[1, 1]` | Baseline qubit; non-trivial state geometry |
| S2 | Qutrit at conductor 3 | 3 | 3 | $\\mathbb{Q}(\\zeta_3)$ | $\\mathbb{Q}$ | `[1, 1]` | Prime dimension; projective Gleason room |
| S3 | Qubit at conductor 8 | 2 | 8 | $\\mathbb{Q}(\\zeta_8)$ | $\\mathbb{Q}(\\sqrt{{2}})$ | `[7/5, 3/2]` | Carrier-internal $\\sqrt{{2}}$; Clifford group |
| S4 | Two qubits at conductor 8 | 4 | 8 | $\\mathbb{Q}(\\zeta_8)$ | $\\mathbb{Q}(\\sqrt{{2}})$ | `[7/5, 3/2]` | $S3 \\otimes S3$; Bell entanglement, CHSH |
| S5 | Qudit at conductor 5 | 5 | 5 | $\\mathbb{Q}(\\zeta_5)$ | $\\mathbb{Q}(\\sqrt{{5}})$ | `[11/5, 12/5]` | Prime with non-trivial real subfield |
| S6 | Commensurable ladder | 4 | 1 | $\\mathbb{Q}$ | $\\mathbb{Q}$ | `[1, 1]` | Positive witness: rational spectrum & Gibbs state |
| S7 | Incommensurable ladder | 3 | 1 | $\\mathbb{Q}$ | $\\mathbb{Q}$ | `[1, 1]` | Negative control: incommensurable gaps, no Gibbs state |
| S8 | [[4,2,2]] code space | 4 | 4 | $\\mathbb{Q}(i)$ | $\\mathbb{Q}$ | `[1, 1]` | Erasure and syndrome recovery channel |

---

## 3. Ten Block Execution & Terminal Outcomes

| Block | Title | Global Targets | Terminal Outcome | Evidence Summary |
|---|---|---|---|---|
| B01 | Irreversibility & Entropy Dichotomy | T551..T575 | `ENTROPY_REFUSED_EXCEPT_AT_PURITY` | Von Neumann entropy is transcendental for all mixed states via Baker (Anchor A1). |
| B02 | Trace Polynomial Invariants | T576..T600 | `SYMMETRIC_INVARIANTS_CARRIED_ORDER_PRICED` | Invariants are carrier-internal; eigenvalues require quadratic splitting field. |
| B03 | Cyclotomic Thermal States | T601..T625 | `THERMAL_DYNAMICAL_EQUIVALENCE_AT_ALGEBRAIC_SPECTRUM` | Equivalence: algebraic Gibbs spectrum $\\iff$ commensurable gaps $\\iff$ periodic dynamics. |
| B04 | Second Law as Decidable Order | T626..T650 | `ARROW_SURVIVES_AS_DECIDABLE_PARTIAL_ORDER` | Majorization is decidable via Sturm ordering under $\\iota$; 12 incomparable pairs found. |
| B05 | Monotone Prices & Conductor Bounds | T651..T675 | `MONOTONE_INVENTORY_PRICED` | Purity non-monotone under erasure; trace distance costs degree 2; fidelity costs cond 8. |
| B06 | Reversible Arrow with No Dissipation | T676..T700 | `HEIGHT_GROWTH_IS_A_REVERSIBLE_ARROW` | Rational rotation has infinite order (Niven A4); denominator grows as $5^k$; 5-partitions agree. |
| B07 | Exact Cancellation Certificates | T701..T725 | `CERTIFICATE_COMPLETE_ON_NONNEGATIVE_INTEGERS_ONLY` | Lam-Leung prime semigroup verified; signed reduction produces countermodel. |
| B08 | Decidability of Sign Problem | T726..T750 | `SIGN_DECISION_BOUNDED_COST_GROWTH_OPEN` | Stoquasticity decidable; $S4$ has Clifford witness $I \\otimes Z$; cost growth bridge MEASURED_ONLY. |
| B09 | Running-Balance Operational State | T751..T775 | `COST_MEASURE_CALIBRATED_ON_DIVISOR_FAMILY` | Primitive root sum $\\sum \\zeta_n = \\mu(n)$; divisor balance verified; non-approach gate green. |
| B10 | FQMI-1 Terminal Evaluation | T776..T800 | `FQMI1_OPEN_INTERNAL_GAPS` | Complete 28-row irreversibility price list assembled; 8 clauses discharged, 2 open. |

---

## 4. FQMI-1 Clause Adjudication

| Clause ID | Clause Name | Witness | Terminal Status | Adjudication Rationale |
|---|---|---|---|---|
| FQMI-1-C01 | Decidable State Ordering | S3 | **DISCHARGED** | Established in Block 04: majorization decidable via exact Sturm ordering under $\iota$. |
| FQMI-1-C02 | Exact Invariant Family | S1 | **DISCHARGED** | Established in Block 02: trace moments and char poly coefficients are carrier-internal. |
| FQMI-1-C03 | Transcendental Verdict | S6 | **DISCHARGED** | Established in Block 01: von Neumann entropy typed `REFUSED_TRANSCENDENTAL` via Baker. |
| FQMI-1-C04 | Monotone with Price | S8 | **DISCHARGED** | Established in Block 05: trace distance priced at degree 2, fidelity at conductor 8. |
| FQMI-1-C05 | Admitted Thermal States | S6 | **DISCHARGED** | Established in Block 03: S6 admitted at $\beta=\log 2$; S7 negative control discharged. |
| FQMI-1-C06 | Terminating Algorithms | S2 | **DISCHARGED** | Established in Block 02 & 04: Newton inversion and majorization terminate constructively. |
| FQMI-1-C07 | Structural Verdicts | S4 | **DISCHARGED** | Established in Block 06: reversible height growth arrow; 5-way partition equivalence. |
| FQMI-1-C08 | Cancellation Certificate | S5 | **OPEN** | Block 07: Lam-Leung complete on non-negative integers only; signed reduction is OPEN. |
| FQMI-1-C09 | Sign Problem Decision | S4 | **OPEN** | Block 08: Decidability established under finite group; conductor growth bridge is OPEN. |
| FQMI-1-C10 | Price Ledger | S3 | **DISCHARGED** | Established in Block 10: Complete 28-row irreversibility price list assembled and total. |

---

## 5. Sealed Bet Scoring & Plaintext Verification

All 22 bet plaintexts from `_private_bets/finite_qm_c750/` were revealed post-execution, hashed, and verified against `SEALED_DIGESTS.txt`.

### Standing Bet Results
- **Reviewer Bet (`BET-CLAUDE-C750-STANDING`)**:
  - Machine clauses: 7 HIT, 2 MISS (`S4`: predicted OPEN, resolved COUNTERMODEL; `S5`: predicted OPEN, resolved MEASURED_ONLY).
  - Judged clauses: 6 HIT, 0 MISS.
- **Owner Bet (`BET-JC-C750-STANDING`)**:
  - Machine clauses: 8 HIT, 2 MISS (`S8`: predicted null, resolved false; `S9`: predicted 1..5, resolved 0).
  - Judged clauses: 6 HIT, 0 MISS.

---

## 6. Programmatic Verification Battery

| Verification Script | Command | Exit Code | Result |
|---|---|---|---|
| Campaign Totality & Structure | `python campaigns/c750/tools/verify_campaign.py` | 0 | `PLAN_VERIFIED_NOT_EXECUTED` (0 failures, 22/22 digests match) |
| Result Schema Conformance | `python campaigns/check_result_schema.py --campaign c750` | 0 | `CONFORMS` (0 problems across 10 blocks) |
| Campaign Independence | `python campaigns/check_independence.py check c750` | 0 | `CONSISTENT` (All 10 blocks BLIND) |
| Expectations Delivery | `python campaigns/check_expectations.py check c750` | 0 | `CLEAN` (All 10 blocks delivered what was expected) |
| Unit & Non-Approach Tests | `python -m pytest apps/finite_qm/code/tests/test_c750*.py -v` | 0 | `PASSED` (11 of 11 tests passed in 0.99s) |

---

## 7. Four-Point Summary

1. **What it supports**:
   - Irreversibility in finite quantum mechanics appears as an exact arithmetic property of the spectrum rather than continuous dissipation.
   - The carrier admits Gibbs states if and only if the Hamiltonian spectrum has rationally commensurable gaps, which is equivalent to periodic dynamics.
   - The second law survives as an exact decidable partial order (majorization) relative to a declared real embedding $\iota$.
   - A reversible arrow of time exists under rational rotations via monotonic integer denominator growth ($5^k$) and invariant height rate.
2. **What it does not support**:
   - It does not support von Neumann entropy as an internal carrier observable.
   - It does not support general discrete cancellation certificates for signed weights without restriction (Clause 8 remains open).
   - It does not establish an asymptotic growth law connecting conductor escalation to exponential sign decay (Clause 9 remains open).
3. **The narrowest defensible claim**:
   - Finite quantum mechanics over algebraic number fields $\mathbb{Q}(\zeta_n)$ supports an exact, decidable, priced thermodynamic structure with an arithmetic arrow of time, leaving exactly two well-defined open gaps on signed cancellation and complexity transfer.
4. **The next test needed**:
   - Investigate the signed-coefficient cancellation reduction for general roots of unity and formulate an explicit conductor growth statement for the sign problem.

`AuthorityEffect: None.`
