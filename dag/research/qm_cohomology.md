# qm_cohomology.md — Cohomology / obstruction roadmap

**Scope:** Cohomology and obstruction roadmap across the `finite_quantum_mechanics` estate.  
**Target:** `qm_cohomology.md`  
**Target:** `qm_cohomology.md`  
**Updated:** 2026-10-11  

This roadmap details the cohomology, obstruction management, and duality machinery connecting discrete difference complexes to quantum realization across the `finite_quantum_mechanics` estate.

## Standing

The core mathematical architecture utilizes finite cochain complexes $C^0 \xrightarrow{\delta^0} C^1 \xrightarrow{\delta^1} C^2$ with $\delta^1 \delta^0 = 0$ as the underlying diagnostic framework for non-trivial circulation, exact repair, and topological obstruction.

Paper §1 states the shared spine is a **plan, not a proof**. The intended foundations arc is primitive difference (SRC-000) to registry-relative lift (SRC-001) to Banach quotient shadow of the repair cofiber (SRC-002) to obstruction-management calculus (SRC-004) to cochain cohomology as the **admission criterion** (SRC-010). SRC-010's lead sentence (`research/010_hilbert_space_cochains_qm_cohomology/hilbert_space_cochains_qm_cohomology.md`): cohomology diagnoses exactness, gluing, and persistent obstruction; it does **not** select Hilbert space, derive the Born rule, establish physical QM, or mint authority. Continuum physics from finite cochains is refused there (§9) and priced at GAP-F001-S000-002.

**What is Lean-proved on declared carriers (candidates, not admissions):**

- Integer primitive difference on Int, plus an abstract structure: `lean4/PrimitiveDifference.lean` — abstract `δ` with ZeroRel / residual quotient **and** later `diff x y := y - x` (`diff_self`, `same_iff_eq`, `diff_antisymm`, `diff_cocycle`). Those LGGR lemmas in the same file are integer-label factorization residuals, not the cited GOMC-01..13 package.
- Triangle coboundary law and H^1=0 on a 3-vertex / 3-edge / 1-face Int complex: `FiniteCochain.lean` `d1_d0_zero`, `coboundary_is_cocycle`, `d1_add_coboundary`, `non_trivial_circulation_not_coboundary`, `triangle_cocycle_is_coboundary`. Because a 2-cell is present, every 1-cocycle is a coboundary on this host. Concrete `(d0 α)(u,v) = α(v) - α(u)` is this file, not the abstract PrimitiveDifference structure.
- Cech d1 ∘ d0 = 0 over Z_2: `ContextualityObstruction.lean` `differential_squares_to_zero`. Cabello X1 has **no global section** (`x1_has_no_global_section`); product X2 has an exhibited section `[1,1,0,0]` (`x2_global_section_valid`). Lean does **not** prove `[c_X1]≠0` vs `[c_X2]=0` as the same H¹ (`lean4/ContextualityObstruction.lean`). No H¹, class representative, or vanishing_iff theorem is in that file. Campaign C1000 Block 07 receipts bind H¹(U,F;Z_2) classes to **Python / receipt paths** (`evidence/contextuality_obstruction_receipt.json`; `campaigns/c1000/block_07/result.json` `coefficient_groups_computed: [Z_2]` only). Receipt flag `vanishing_iff_global_section_proved` is not a Lean theorem.
- Exact rational 3-cycle price: `WorldCycle3Quotient.lean` `exact_iff_zero_charge`, `quotient_price_characterization` — price equals |charge| on **one unweighted** rational 3-cycle. `FiniteN3ResidualDual.lean` pairs a normalized period (1/3,1/3,1/3) with a residual beta=(1,1,1). Neither is the general weighted Phi_1 circulation dual of QMC-T1.
- Dual pairing bound plus Mermin–Peres sign parity: `DualWitness.lean` `dual_witness_certifies_trace_distance` (`|w·d| <= |d0|+|d1|` for coefficients in `{-1,0,1}`) and `mermin_peres_parity_obstruction`. Register: candidate mirror for QM-120, not QM_080 Theorems 5–6, not an Atlas admission.
- Admitted window, not a derived complex: `CochainWindow.lean` takes the chain law as a **structure field** and proves a 3-way `sector_trichotomy` (Exact / ActiveClosureFailure / ClosedResidual). `CellGrammar.lean` derives d1 d0 = 0 only after declared `boundarySquare` and dual pairings. General complexes do **not** inherit a proved coboundary law from primitive difference alone.
- Classifier without Refusal: `PointedObstructionClassifier.lean` is a Nat-valued 3-way split assuming Phi and Gamma as fields. No IllFormed / Refusal class.
- Adjacent, not admission: `CabelloSignPolytope.lean` is Z^4 parity uncolorability (header nonclaim: finite KS does not force Born). `SurfaceCodeToricTopology.lean` `homology_dimension_k2` is the integer identity `8-(4-1)-(4-1)=2`. That is not a group isomorphism or a computed homology of the 2×2 torus (`lean4/SurfaceCodeToricTopology.lean`). Keep the non-admission fence; drop the iso wording.

**What is numerically checked, not exact:**

- `external:unlocated` computes D, d1 d0 = 0, weighted L1, Phi_1 via scipy HiGHS (`TOL = 1e-9`), Gamma_2, and a **3-way** trichotomy (`ExactClass` / `ClosedResidual` / `ActiveClosureFailure`). The module docstring itself refuses an infinite-precision solver. Tests: `external:unlocated` (negative controls on d1 d0 and coboundary invariance).
- `rungs.py` `h1_dim` uses SVD float ranks. Paper Rung 2 / §4 calling Phi_1 an **exact** LP is stronger than the live kernel and than FQM-E8's computational status.
- C1000 Block 07 Python (`external:unlocated`) is exact Z_2 linear algebra (zero floats on algebraic paths). That exactness is scoped to the declared coefficient group.

**What remains prose / ledger-ASSERTED:**

- SRC-000 QMC-T1..T6: source says PROVED; `claim_ledger.yaml` types them ASSERTED with evidence none; `source_inventory.yaml` SRC-000 `no_lean_file` / `no_test_file`.
- SRC-002 QM-002-C6 scalar Phi_1 equals Banach quotient-norm: paper status box OPEN for Lean weighted-L1 identity; ledger source_status says `phi1_eq_banachShadow` is not the inf identity. `002:QM-002-C7` refuses **Φ₁ = R_Λ** as ill-typed (scalar vs cofiber **object**). Non-identification of Cofib vs Q¹_sep is **`002:QM-002-C1`**. Unrestricted BanachShadow(Cofib) is **C8**. C3 even defines `Cofib(d0)=coker(d0)` as a specialization (`claims/claim_ledger.yaml`). Keep the scalar-identity OPEN and the type-separation fence; do **not** cite C7 for cofiber ≅ Q¹.
- SRC-004 GOMC-01..13: paper ledger marks PROVEN at `QM/GOMC_01..13`. Inventory SRC-004 `no_lean_file`. No `GOMC_*.lean` under `lean4/quantum_mechanics`. Physical QM from GOMC is refused in that paper (QM-004-C23).
- SRC-010 QM-010-C2 im(d0)⊆ker(d1): ledger type **OPEN**, evidence none, despite `FiniteCochain.coboundary_is_cocycle` on one Int triangle. PL-QM032-1..3 remain unlabeled MECHANIZED. `docs/claim_code_map.yaml` binds C1 to a phantom `*_lib` module. QM_010 imports a finite Hilbert packet and says cohomology does **not** derive Hilbert space; it does **not** assert nonexistence of Hilbert-valued cochains. Continuum lift of infinite-dimensional C^*(X;H) is priced at GAP-F001-S000-002, not by that sentence.
- SRC-080 C10–C12 (Thm 5 quotient duality, Thm 6 dual maximizer): ASSERTED, evidence none. Cited `TraceZeroDuality.lean` / `003_qm_trace_zero_duality.lean` are not in the application lake. SRC-080 `no_lean_file` / `no_test_file`.
- SRC-120 QM-120-C11 F2 cochain theorem (`QM.MerminPeresF2.mermin_peres_f2_cochain_obstruction`, ENC-1143): ASSERTED; cited Lean path absent; inventory `no_lean_file` / `no_test_file`. Later DualWitness is a different, narrower sign-parity statement.
- QM-001-C1 ForcedLift: CONDITIONAL, evidence none. GAP-FQM-011 discharged a tautological test, not C1. `research/001_tower_walk_registry_relative_interface_lift/code/test_qm_001_tower_walk.py` still asserts a dict comprehension. Firewall QM-001-C2: Phi_1(q)>0 does not imply LicensedLift.

Paper §3 working surface is 166 ASSERTED + 75 UNTYPED = 241 (README disagrees: 162+90=252). Those count disagreements are inventory hygiene, not cohomology theorems.

Live crate `use_cases/`: **42** use-case `.py` files plus `__init__.py`. That listing is not a 43-count census theorem. GAP-FQM-003’s “five kernel routines under legacy `code/`” clause is still stale (legacy `code/` is absent).

## Gaps

### GAP-F001-S000-001 — Exact duality gap certificate (`open_bridge`; not priced unclosable)

**Why open.** QM_080 Theorem 5 asserts finite-dimensional quotient duality for Phi_tr (spectral dual-ball lemma + Sion); Theorem 6 asserts a compact dual maximizer (`research/080_...` §2.6–2.7). `DualWitness.lean` bounds a 2-integer pairing and proves Mermin–Peres sign parity. FQM-E3 is a sampled fixture (paper §4: a vanishing sampled gap is not a certificate). Atlas-review finding ATLAS-REV-01 records an earlier wrong identification of the dual of C_1/ker d1 with ker of the adjoint.

This gap has two distinct mathematical objects that the register currently conflates:

1. **Operator / trace-norm dual** of QM_080 (matrix witnesses, divergence-free adjoint condition, operator-norm ball). Closing this is a convex-analysis / Lean matrix task; it is not a cochain LP.
2. **Circulation dual of Phi_1** (QMC-T1): Phi_1([omega]) = max { z^T omega : d0^T z = 0, |z_e| <= w_e }. Live `cochain.phi_1` is primal HiGHS only. `WorldCycle3Quotient` / `FiniteN3ResidualDual` are unweighted 3-cycle shadows of (2), not (1).

**Closable:** conditional (finite Phi_1 primal/dual over Q plus Lean duality on declared graphs: yes; general operator duality: separate open_bridge).

### NEW-QMC-T1-PHI1-DUAL — Phi_1 circulation dual not mechanized (not yet in the register)

**Why open.** SRC-000 claims QMC-T1 PROVED from an LP proof and primal/dual tests. Ledger types it ASSERTED. Inventory: no tests, no Lean. `cochain.phi_1` has no dual LP and no exact attainment proof. The 3-cycle Lean price is |charge| without weights.

**Closable:** yes, on declared finite graphs.

### GAP-F001-S000-002 — Continuum Hilbert lift (`continuum_interface`; PRICED_CONTINUUM_INTERFACE)

**Why open.** No source constructs a map from finite graph cochains (integer/rational weights, finite labels) to infinite-dimensional Hilbert space. QM_122 §6 refuses the lift; QM_010 forbids continuum physics from finite cochains. Canonical [X,P]=i hbar I has no finite-dimensional representation (Wintner–Wielandt). Cited `code/continuum_lift.py` and `code_rs/src/continuum.rs` do not exist at those paths; live kernels are `external:unlocated` (numpy floats) and `external:sha256:55ada06a22f283b8ab22c727842fcf9667a4d938e834ac676c1a7231bb3c2f3b` (exact rationals). `ContinuumLiftBoundary.lean` is 2x2 Int, not a completion functor.

**Closable inside the finite programme:** no. Marked **priced-continuum**. Infinite-dimensional Hilbert cochain cohomology C^*(X;H) for complete H is the same priced interface, not a finite-carrier task.

### GAP-FQM-003 — Cofiber–Banach bridge and four-way classifier unimplemented (`missing_implementation`)

**Why open.** Register still says the cofiber-to-Banach bridge, V_Q, and Exact / ClosedResidual / ActiveClosureFailure / **Refusal** classifier do not exist as code, and that legacy `code/` holds only five kernel routines. The five-routine clause is **stale** against the live tree (`external:unlocated` has 42 use-case `.py` files plus `__init__.py`; legacy `code/` is absent). The **named objects** were not found as implementations: QM_005 V_Q packet verifier, four-way classifier including Refusal, QM_006 descent audit, QM_002 cofiber-to-Banach bridge. `cochain.py` is a 3-way diagnostic. `CochainWindow.sector_trichotomy` is 3-way. QM-002-C6 remains an unmechanized scalar identity. Object-level cofiber identification with Q¹_sep is fenced by **C1**, not C7. GAP-FQM-003 is missing_implementation of described algorithms, not a Phi_1-identity gap. Paper Rung 7 mis-cites this ID as the measurement problem.

**Closable:** conditional for the finite scalar identity and 4-way certificates; object-level cofiber identified with Q^1_sep is refused (C1); Φ₁=R_Λ is ill-typed (C7).

### GAP-C1000-007 — Presheaf cohomology obstruction classes off Z_2 (`open_question`)

**Why open.** Block 07 Python/receipts compute H^1 over Z_2 for two declared scenarios. Lean proves d1(d0 s)=0 over Z_2 and global-section presence/absence; it does not prove the H¹ class. DualWitness Mermin–Peres is sign-parity, not Cech cohomology. H^1 over Z, Q, or Z[zeta_n], and coefficient-dependent contextuality, remain open. QM_120 operator provenance stays imported. Finite KS / Cabello does not close Born uniqueness (GAP-F001-S000-004, separate Born team).

**Closable:** yes, as a finite-scenario computation plus a classification of ring-dependent verdicts. Relativistic / infinite covers are out of scope.

### NEW-QM-010-HILBERT-COCHAIN — Hilbert-space cochains: Lean OPEN; finite Hilbert-packet adapter missing (not yet in the register)

**Why open.** QM-010-C2 is OPEN in the application ledger. FiniteCochain proves the complex law on one Int triangle; that is not a receipted bind of PL-QM032-1..3. QM_010 imports a finite Hilbert packet and refuses deriving Hilbert space from cohomology. No operator-valued cochain complex is implemented in the opened kernels. Infinite-dimensional Hilbert cochain cohomology is priced with GAP-F001-S000-002.

**Closable:** conditional for (i) receipting existing finite complex-law Lean as C2/C4 and (ii) a finite Hilbert-packet adapter with certificates. Do not convert “no implemented operator-valued cochain” into “QM_010 proves nonexistence.”

### NEW-GOMC-LEAN-ABSENT — GOMC obstruction calculus cited Lean is not in this tree (not yet in the register)

**Why open.** QM_004 ledger marks GOMC-01..13 PROVEN. Inventory SRC-004 `no_lean_file`. Grep finds no GOMC theorems in `lean4/quantum_mechanics`. `PrimitiveDifference.localGreenGlobalRed_*` and `WorldLGGRWitness.lean` are integer-label residuals / Bool regressions, not the GOMC package. Physical QM from GOMC is refused.

**Closable:** conditional to rebuild the finite LGGR/firewall lemmas in-tree and rebind or withdraw the PROVEN tags. Not a derivation of QM.

### NEW-QM-001-C1-FORCED-LIFT — Registry-relative ForcedLift implication unevidenced (not yet in the register; not a cohomology existence proof)

**Why open.** Ledger types C1 CONDITIONAL, evidence none. GAP-FQM-011 discharged a tautological test and emptied a phantom claim-map; it left C1 unevidenced. Phi_1>0 does not license a Hilbert lift (QM-001-C2 fence). Unconditional uniqueness of Hilbert / Born / CPTP is refused by the paper.

**Closable:** yes for registry-schema checkers (does not create Hilbert uniqueness). Unconditional Hilbert uniqueness is refused, not closable on a finite carrier.

### Related register rows the cohomology walk must not over-claim

- GAP-FQM-011 is **discharged** (2026-09-04) as a false C1-test; it is not a close of ForcedLift or of Phi_1.
- GAP-F001-S000-004 / 010 (Gleason) are Born-team OPEN (CONDITIONAL). Finite Cabello / Mermin cohomology does not yield dense-sphere uniqueness.
- Paper Rung 7 mis-cites GAP-FQM-003 (missing algorithms) as the measurement problem. That is a citation error, not a cohomology close.

## Effort and resources

Estimates are operator judgment. Priced-continuum items are **not closable** inside the finite programme. Person-week/month numbers are not certificates; residual duration words sit under this fence.

| ID | Closable | Effort (operator judgment) | Skills |
| --- | --- | --- | --- |
| NEW-QMC-T1-PHI1-DUAL | yes | Exact rational primal/dual on declared graphs plus Lean on the 3-cycle and a second fixture | LP duality, exact Q arithmetic, Lean |
| GAP-F001-S000-001 (finite Phi_1 dual) | conditional | Overlaps T1; general operator duality remains a separate open_bridge | finite LP duality, exact arithmetic, Lean 4 |
| GAP-F001-S000-001 (QM_080 Thm 5–6) | conditional | Not discharged by more 2-integer pairings | convex analysis, spectral theorem, Lean matrix analysis |
| GAP-FQM-003 (scalar Phi_1 = quotient norm + 4-way certificates) | conditional | Object-level cofiber identification refused (C1); Φ₁=R_Λ ill-typed (C7) | Banach quotients, exact LP, Lean, classifier certificates |
| GAP-C1000-007 | yes | Finite scenario cohomology over Z/Q/cyclotomic coefficients plus classification of ring-dependent verdicts | Cech/presheaf cohomology, exact linear algebra over rings, Lean 4 |
| NEW-QM-010-HILBERT-COCHAIN | conditional | Receipt existing finite complex-law Lean as C2/C4; finite Hilbert-packet adapter with certificates | homological algebra, Lean 4, finite Hilbert packets |
| NEW-GOMC-LEAN-ABSENT | conditional | Rebuild finite LGGR/firewall lemmas in-tree; not a derivation of QM | obstruction calculus, Lean 4, authority-fence typing |
| NEW-QM-001-C1-FORCED-LIFT | no (unconditional Hilbert uniqueness); yes (schema checkers) | Registry-schema checkers | claim certificates, registry typing |
| GAP-F001-S000-002 | priced-continuum | n/a | functional analysis; not a finite-carrier task |

## What would change our mind

The cochain **admission criterion** (SRC-010 / paper §1) would close as a **finite diagnostic**, not as a derivation of QM, if and only if all of the following hold on **declared** finite complexes and coefficient rings, with existing files named as evidence:

1. **Complex law, receipted.** im(d0) subseteq ker(d1) is a ledger-bound theorem (QM-010-C2 / PL-QM032-1) on a stated class of complexes, not only an Int triangle plus a `Window.chain` field. Cell-grammar derivations must list their declared `boundarySquare` and dual pairings.
2. **Exact Phi_1 with dual.** For declared finite weighted graphs, Phi_1 is computed by an exact rational (or cyclotomic) primal **and** dual LP, with Lean attainment on the 3-cycle and at least one second fixture, and QMC-T1 rebound from ASSERTED. Numerical HiGHS with `TOL=1e-9` is then a regression, not the theorem.
3. **Four-way classifier.** Exact / ClosedResidual (ClosedNonexact) / ActiveClosureFailure / **IllFormed-Refusal** is implemented, tested with negative controls (missing residual adapter iota, ill-typed s, undecided certificates), and bound to QM-010-C3. A 3-way diagnostic is not the paper's admission table.
4. **Non-selection fence kept.** Closing admission does **not** select Hilbert, Born, CPTP, or authority. QM-001-C2 and QM-010-C5/C8 remain fences. Phi_1>0 never licenses a Hilbert lift. Object-level Cofib vs Q¹_sep stays refused (C1). Φ₁=R_Λ stays ill-typed (C7).
5. **Contextuality classes named by ring.** Cabello / product (and at least one further scenario) have H^1 computed over Z_2 **and** over Z or Q (or a declared cyclotomic), with an explicit example whose verdict flips or a proof that it does not. DualWitness sign-parity is not this class. Lean global-section theorems are not this class until bound as H¹.
6. **Lost ENC files rebound or withdrawn.** ENC-1143 (MerminPeres F2), ENC-0225 (TraceZeroDuality), and GOMC-01..13 are either lake-replayed in this tree or the source PROVEN tags are withdrawn. Compiling DualWitness / PrimitiveDifference LGGR does not substitute.

What would **not** change our mind:

- More Cabello ray counts, more SVD ranks, more HiGHS fixtures, or renaming GAP-FQM-003 while V_Q / Refusal / cofiber bridge remain unimplemented.
- A green `lake build` or pytest suite (paper §7 / README Non-claims: mechanical success is not semantic validity).
- Promoting ForcedLift from a dict-comprehension test.
- Treating finite KS / Cech Z_2 obstruction as Gleason uniqueness.
- Constructing infinite-dimensional Hilbert space, continuous sphere topology, or CCR [X,P]=i hbar I **inside** the finite programme. Those remain GAP-F001-S000-002 (**priced-continuum**, not closable here). A finite Hilbert-packet **adapter** with imported quantum side can close the SRC-010 adapter definition; it does not close the continuum lift.

Until those admission items exist as named files, the finite presentation **does not close** on cochain cohomology, and the obstruction exhibited is: exactness is proved on declared hosts; the dual, the four-way classifier, Hilbert-valued cochains, and off-Z_2 classes are not.

## Sources opened

- `README.md`
- `finite_quantum_mechanics.md` (§0, §1 Rungs 1–2, §3–§5, §7, §9)
- `claims/gap_register.yaml` (GAP-F001-S000-001/002, GAP-FQM-003, GAP-FQM-011 note, GAP-C1000-007, atlas_review_findings)
- `claims/claim_ledger.yaml` (000:QMC-T1..T6, 001:QM-001-C1/C2/C5/C6, 002:QM-002-C1/C3/C6/C7/C8, 010:QM-010-C2, 080:C10–C12, 120:QM-120-C11)
- `claims/source_inventory.yaml` (SRC-000, SRC-001, SRC-002, SRC-004, SRC-010, SRC-080, SRC-120)
- `sources/` listing; retained `122_...` and `060_...`
- `research/` listing; `research/README.md`; confirmed `research/finite_qm_roadmaps` **did not exist** before this write
- `research/000_...`; `research/001_...`; `research/002_...`; `research/004_...`; `research/010_...`; `research/080_...`; `research/120_...`
- `external:unlocated` listing; `use_cases/cochain.py`; `use_cases/rungs.py`
- `external:unlocated` listing; `contextuality_obstruction.py`; `tests/unit/test_cochain.py`
- `external:unlocated` listing (no `src/continuum.rs`)
- `lean4/quantum_mechanics/`: `PrimitiveDifference.lean`, `FiniteCochain.lean`, `CochainWindow.lean`, `CellGrammar.lean`, `ContextualityObstruction.lean`, `WorldCycle3Quotient.lean`, `FiniteN3ResidualDual.lean`, `DualWitness.lean`, `PointedObstructionClassifier.lean`, `WorldLGGRWitness.lean`, `CabelloSignPolytope.lean`, `SurfaceCodeToricTopology.lean`, `ContextualityThresholds.lean`; confirmed `lean4/quantum_mechanics/original_lean_20260809` **absent**; no `GOMC_*.lean`
- `campaigns/c1000/block_07/RESULT.md`; `result.json`; `evidence/contextuality_obstruction_receipt.json`
