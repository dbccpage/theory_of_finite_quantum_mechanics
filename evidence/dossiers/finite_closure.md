# Campaign C1000 Execution & FQMR-1 Closure Certification

AuthorityEffect: None. Citation: `sealed-derivation-v1` (`3100c4e`).
Date: 2026-09-09. Certification Receipt: `evidence/c1000_certification_receipt_20260909.json`.

---

## 1. Executive Summary

Campaign C1000 executes 250 targets (`C1000-T801` through `C1000-T1050`) across ten blocks of twenty-five in `apps/finite_qm`.
It addresses the foundational question of whether finite quantum mechanics over algebraic number fields $\mathbb{Q}(\zeta_n)$ supports relativistic kinematic structures, rotational symmetry, causality, and correlation bounds under the declared system class `FQMR-1-CLASS-V1`.

The campaign achieves:
1. **Pre-Execution Custody & Launch Prequalification**:
   - The system class `class/fqmr1_class.json` is verified unchanged and pinned at canonical LF SHA-256 `1e31d811a5245a8b8120bb3d35ad4868537d1bcc4d577d2fcdf13de0de087488`.
   - All 22 pre-registered bet digests from `_private_bets/finite_qm_c1000/SEALED_DIGESTS.txt` are verified byte-identically (100% match).
   - Precondition 5 departure (`UNMET_OWNER_AUTHORISED`) is audited: both bet sets were drafted by Claude (Opus 5) under owner authorization.
   - All 10 blocks maintain `independence_grade: BLIND` with respect to C750.
2. **Zero-Float Strict Execution**:
   - Every calculation across all 10 blocks executes in exact rational arithmetic or algebraic number fields $\mathbb{Q}(\zeta_n)$. No floating-point operations occur in any receipt or result field.
3. **Execution & Schema Conformance of All 10 Blocks**:
   - All 10 blocks deliver exactly their frozen schemas (`block_01/EXPECTED.json` through `block_10/EXPECTED.json`).
   - `check_result_schema.py --campaign c1000` reports 0 problems (`CONFORMS`).
   - `check_expectations.py check c1000` reports all 10 blocks clean with 0 unexplained nulls.
4. **Complete Terminal Closure of FQMR-1**:
   - Discharged Clauses: 10 of 10 clauses fully discharged.
   - Open Clauses: 0 open clauses.
   - Campaign Terminal Outcome: `FQMR1_CLOSED_AT_DECLARED_CLASS`.
5. **Sealed Bet Scoring & Anti-Clean-Sweep Audit**:
   - All 22 bet plaintexts revealed post-execution from private custody and scored strictly against ground truth.
   - Reviewer (Claude): 119 HIT, 9 MISS (93.0% net accuracy across NOT FORCED clauses).
   - Owner (JC): 101 HIT, 27 MISS (78.9% net accuracy across NOT FORCED clauses).
   - Clean sweep audit: Neither bettor achieved a clean sweep. Both recorded genuine mathematical misses on contested boundaries (Blocks 08, 09, 10 and standing bets).

---

## 2. FQMR-1 Class Declaration & System Inventory

- **Class ID**: `FQMR-1-CLASS-V1`
- **Canonical Path**: `campaigns/c1000/class/fqmr1_class.json`
- **Canonical LF SHA-256**: `1e31d811a5245a8b8120bb3d35ad4868537d1bcc4d577d2fcdf13de0de087488`
- **Class Members**: 11 declared and inhabited systems ($R1, R2, R3, B1, B2, C1, C2, Q1, Q2, X1, X2$).

| Member ID | Kind | Name | Conductor | Carrier | Real Subfield | Role in Campaign |
|---|---|---|---|---|---|---|
| R1 | Rotation element | Rational plane rotation ($3/5, 4/5$) | 1 | $\mathbb{Q}$ | $\mathbb{Q}$ | Infinite cyclic order by Niven; parameter $\theta$ is transcendental |
| R2 | Rotation group | Octahedral group (24 elements) | 1 | $\mathbb{Q}$ | $\mathbb{Q}$ | Conductor-1 finite rotation group via signed permutation matrices |
| R3 | Rotation group | Icosahedral group (60 elements) | 5 | $\mathbb{Q}(\sqrt{5})$ | $\mathbb{Q}(\sqrt{5})$ | Witness that finite rotation groups carry a computable conductor price ($c=5$) |
| B1 | Boost element | Rational boost ($\gamma = 5/4, v=3/5$) | 1 | $\mathbb{Q}$ | $\mathbb{Q}$ | Rational boost in $\mathbb{Q}$; generates infinite cyclic group with growing denominators |
| B2 | Boost pair | Orthogonal rational boosts | 1 | $\mathbb{Q}$ | $\mathbb{Q}$ | Non-collinear boost composition generating Wigner rotation with $\cos\theta=40/41$ |
| C1 | Causal order | Three-element V poset | null | Order only | None | Smallest poset with a spacelike pair; base case for microcausality |
| C2 | Causal order | Four-element diamond poset | null | Order only | None | Spacelike pair with common past and future; microcausality witness |
| Q1 | Quantum bipartite | Two qubits at conductor 4 | 4 | $\mathbb{Q}(i)$ | $\mathbb{Q}$ | $\sqrt{2}$ absent; Tsirelson bound $2\sqrt{2}$ NOT attained |
| Q2 | Quantum bipartite | Two qubits at conductor 8 | 8 | $\mathbb{Q}(\zeta_8)$ | $\mathbb{Q}(\sqrt{2})$ | $\sqrt{2}$ present; Tsirelson bound $2\sqrt{2}$ exactly attained |
| X1 | Contextuality scenario | Cabello 18-ray Peres-Mermin | 1 | $\mathbb{Q}$ | $\mathbb{Q}$ | Contextual scenario with non-zero 1-cocycle in $H^1(U, F; \mathbb{Z}_2)$ |
| X2 | Contextuality scenario | Classical product scenario | 1 | $\mathbb{Q}$ | $\mathbb{Q}$ | Non-contextual negative control with vanishing cohomology class |

---

## 3. Ten Block Execution & Terminal Outcomes

| Block | Title | Global Targets | Terminal Outcome | Key Mathematical Evidence |
|---|---|---|---|---|
| B01 | Causal Order & Incidence Algebra | T801..T825 | `CAUSAL_ORDER_ADMITTED_NOT_SUPPLIED` | Causal order is external data (`ADMITTED`). Once admitted, Alexandrov intervals, Mobius inversion, and incidence algebra are carrier-internal over $\mathbb{Q}$ at conductor 1. |
| B02 | No-Signalling & Locality | T826..T850 | `NO_SIGNALLING_DERIVED_FROM_ADMITTED_COMPOSITION` | No-signalling is derived from admitted bilinear tensor product via linear uniqueness of partial trace. No signalling rival found within search bound. |
| B03 | Rotation Group Prices | T851..T875 | `ROTATION_GROUPS_CLOSE_AT_COMPUTED_PRICE` | Finite rotation groups close over $\mathbb{Q}(\zeta_c)$ at computable conductor prices: tetrahedral ($c=1$), octahedral ($c=1$), icosahedral ($c=5$). Cyclic $C_n$ costs $\mathrm{rad}(n)$ or $2\,\mathrm{rad}(n)$. |
| B04 | Boost Non-Closure | T876..T900 | `BOOSTS_EXACT_BUT_NEVER_FINITE` | Individual rational boosts exist in $\mathbb{Q}$. However, no non-trivial finite boost group exists over any field of characteristic 0 because eigenvalues $e^{\pm \eta}$ have infinite multiplicative order. |
| B05 | Boost Composition & Aperiodicity | T901..T925 | `TWO_BOOST_COMPOSITION_APERIODIC` | Non-collinear rational boost composition yields Wigner rotation with rational cosine (e.g. $40/41$). By Niven's theorem, angle is irrational multiple of $\pi$, generating an aperiodic quasi-crystal orbit. |
| B06 | Tsirelson Bound Attainment | T926..T950 | `TSIRELSON_ATTAINED_IFF_EIGHT_DIVIDES_CONDUCTOR` | Tsirelson correlation $2\sqrt{2}$ is attained in cyclotomic finite quantum mechanics if and only if $8 \mid c$, corresponding to the presence of $\sqrt{2} \in \mathbb{Q}(\zeta_c)$. |
| B07 | Contextuality Cohomology | T951..T975 | `OBSTRUCTION_CLASSES_COMPUTED_EXACTLY` | Quantum contextuality in the Peres-Mermin square ($X1$) is an exact non-zero sheaf cohomology class in $H^1(U, F; \mathbb{Z}_2)$. Classical scenario ($X2$) has $[c_{X2}]=0$ with an explicit global section. |
| B08 | Finite Microcausality | T976..T1000 | `FINITE_MICROCAUSALITY_CRITERION_AT_SCOPE` | Under non-degeneracy, spacelike observable commutativity $[A(x), A(y)]=0$ is obstructed on posets whose incomparability graph contains an odd cycle (e.g. 3-element antichain $C3$). |
| B09 | Parameter Dichotomy | T1001..T1025 | `PARAMETERS_REFUSED_ELEMENTS_CARRIED` | Unified dichotomy proved: a finite carrier holds algebraic elements of a 1-parameter group, never the continuous parameter itself (angle, rapidity, time). Parameter transcendence proved via Lindemann-Weierstrass. |
| B10 | FQMR-1 Terminal Synthesis | T1026..T1050 | `FQMR1_CLOSED_AT_DECLARED_CLASS` | Assembled complete 40-row price list (14 elements, 6 admitted, 8 derived, 12 refused). All 10 FQMR-1 clauses discharged with zero internal gaps. |

---

## 4. FQMR-1 Clause Adjudication

All 10 clauses of `FQMR-1-CLASS-V1` are fully discharged:

| Clause ID | Clause Name | Witness | Status | Adjudication Rationale |
|---|---|---|---|---|
| FQMR-1-C01 | Causal Order Status | C1 | **DISCHARGED** | Established in Block 01: causal order is typed `ADMITTED`; incidence algebra and Mobius inversion are carrier-internal over $\mathbb{Q}$ at conductor 1. |
| FQMR-1-C02 | Composition & Marginal | Q1 | **DISCHARGED** | Established in Block 02: partial trace is linearly unique on $\mathcal{B}(\mathcal{H}_1) \otimes \mathcal{B}(\mathcal{H}_2)$ over algebraic fields. |
| FQMR-1-C03 | No-Signalling Verdict | Q1 | **DISCHARGED** | Established in Block 02: no-signalling is derived from tensor composition; no signalling rival found within declared bound. |
| FQMR-1-C04 | Element Inventory with Price | R3 | **DISCHARGED** | Established in Block 03: icosahedral group requires $\mathbb{Q}(\sqrt{5})$ and costs conductor 5; tetrahedral and octahedral cost conductor 1. |
| FQMR-1-C05 | Group Closure Verdict | B1 | **DISCHARGED** | Established in Block 04: rational boosts exist in $\mathbb{Q}$, but no finite boost group exists in characteristic 0 (eigenvalue theorem). |
| FQMR-1-C06 | Parameter Verdict | B1 | **DISCHARGED** | Established in Block 09: rapidity $\eta = \log(2)$ is transcendental by Lindemann-Weierstrass; typed `REFUSED_TRANSCENDENTAL`. |
| FQMR-1-C07 | Terminating Algorithms | R2 | **DISCHARGED** | Established in Block 03 & 07: octahedral enumeration (24) and sheaf cohomology solver terminate constructively. |
| FQMR-1-C08 | Structural Verdicts | C2 | **DISCHARGED** | Established in Block 08: microcausality admitted on bipartite incomparability graphs; obstructed on odd cycles. |
| FQMR-1-C09 | Correlation Attainment | Q2 | **DISCHARGED** | Established in Block 06: Tsirelson bound $2\sqrt{2}$ attained if and only if $8 \mid c$; comparison of $Q1$ ($c=4$) vs $Q2$ ($c=8$) verified. |
| FQMR-1-C10 | Price Ledger | R3 | **DISCHARGED** | Established in Block 10: Complete 40-row terminal price list assembled, pricing external admissions and algebraic carrier requirements. |

---

## 5. The Element-versus-Parameter Dichotomy

The central unifying theorem of Campaign C1000, proved in Block 09 (Target C1000-T1008) and verified in `test_group_parameter.py`, is the **Element-versus-Parameter Dichotomy**:

$$\text{Over an algebraic number field } K, \text{ an algebraic matrix } U = \exp(i A \theta) \text{ with algebraic non-zero spectrum has } \theta \in K \iff U = I.$$

### Three Instances of the Dichotomy:
1. **Spatial Rotation**:
   - Element $R_\theta = \begin{pmatrix} 3/5 & -4/5 \\ 4/5 & 3/5 \end{pmatrix} \in \mathrm{SO}(2, \mathbb{Q})$ has exact rational entries.
   - Parameter $\theta = \arccos(3/5)$ is transcendental by the Lindemann-Weierstrass theorem.
2. **Lorentz Boost**:
   - Element $B_\eta = \begin{pmatrix} 5/4 & 3/4 \\ 3/4 & 5/4 \end{pmatrix} \in \mathrm{SO}^+(1,1, \mathbb{Q})$ has exact rational entries.
   - Parameter (rapidity) $\eta = \log(2)$ is transcendental by the Lindemann-Weierstrass theorem.
3. **Time Evolution**:
   - Unitary element $U(t) = \exp(-i H t)$ has algebraic matrix entries.
   - Parameter (time) $t$ is transcendental whenever $H$ has non-zero algebraic spectrum and $U(t) \neq I$.

### Independent Agreement with C750:
Running under `independence_grade: BLIND` with zero cross-campaign consumption, Campaign C750 established that inverse temperature $\beta$ in thermal states $\rho = \exp(-\beta H)/Z$ is transcendental whenever the state has algebraic spectrum and non-zero gaps.
C1000 and C750 therefore independently converge on the same foundational insight: **a finite algebraic carrier holds the operational symmetry and transformation elements, never the continuous Lie parameters.**

---

## 6. Programmatic Verification Battery

| Verification Gate | Command | Exit Code | Result | Audit Note |
|---|---|---|---|---|
| Campaign Totality & Structure | `python apps/finite_qm/campaigns/c1000/tools/verify_campaign.py` | 0 | `PLAN_VERIFIED_LAUNCH_BLOCKED` | 0 structure errors; Precondition 5 departure authorized by owner. |
| Schema Conformance | `python apps/finite_qm/campaigns/check_result_schema.py --campaign c1000` | 0 | `CONFORMS` | All 10 blocks report 0 problems. |
| Independence Grade | `python apps/finite_qm/campaigns/check_independence.py check c1000` | 0 | `CONSISTENT` | All 10 blocks verified BLIND. |
| Expectations Delivery | `python campaigns/check_expectations.py check c1000` | 0 | `CLEAN` | All 10 blocks delivered all expected keys; 0 unexplained nulls. |
| Targeted Test Suites | `python -m pytest apps/finite_qm/code/tests/test_*.py` | 0 | `95 PASSED` | 11 C1000 test files pass in exact rational arithmetic. |

---

## 7. Claim Hygiene & Four-Point Summary

1. **What this campaign supports**:
   - Finite quantum mechanics over algebraic number fields $\mathbb{Q}(\zeta_n)$ supports exact finite rotation groups ($T, O, I$) at computable conductor prices ($c=1, 1, 5$).
   - Exact individual Lorentz boosts with rational velocity exist in $\mathbb{Q}$, but no non-trivial finite boost group exists in characteristic 0.
   - The composition of two non-collinear rational boosts generates an aperiodic quasi-crystal orbit in state space via Niven's theorem.
   - The Tsirelson quantum correlation bound $2\sqrt{2}$ is attained if and only if $8 \mid c$.
   - Quantum contextuality is certified as a non-zero sheaf cohomology class in $H^1(U, F; \mathbb{Z}_2)$.
   - The element-versus-parameter dichotomy holds across rotations, boosts, and time evolution.
2. **What this campaign does NOT support**:
   - Does not derive spacetime or approximate pseudo-Riemannian manifolds from causal posets.
   - Does not construct continuous Lie groups or Lie algebras over the finite carrier.
   - Does not claim physical emergence of relativistic quantum field theory.
   - Does not assert multi-party consensus for pre-registered bets (Precondition 5 departed under owner authorization).
3. **The narrowest defensible claim**:
   - Campaign C1000 formally and constructively establishes that finite quantum mechanics over algebraic number fields supports exact rotational symmetry and kinematic boost transformations, while strictly separating group elements from group parameters and pricing external causal, composition, and carrier requirements across a complete 40-row ledger.
4. **The next test needed**:
   - Extend the element-versus-parameter dichotomy to multiparameter gauge groups over algebraic number fields and investigate finite representation bounds for non-compact semisimple Lie algebras.

`AuthorityEffect: None.`
