# QUADRANT INDEX: Epistemic Map of the Witnessed Difference Programme

**Package:** `atlas/finite_obstruction_calculus/witnessed_difference_programme`  
**Edition:** 2.4.5 (Restructured 2026-11-06)  
**Author:** Worker 1 (Composition & Four-Quadrant Restructuring Specialist)  
**Audience:** Human Mathematicians, System Architects, and Autonomous LLM Agents  

---

## 1. Executive Summary & Epistemic Boundary

The Witnessed Difference Programme (WDP) is a rigorous finite mathematical framework establishing observer-relative distinction, linear obstruction calculus, guarded schedule topology, and report-based measurement reconstruction.

To eliminate confusion between established mathematical results, active open derivations, obsolete historical artifacts, and long-term unclosed obligations, the programme is structured into a **Four-Quadrant Epistemic Architecture**:

```text
witnessed_difference_programme/
│
├── QUADRANT_INDEX.md                               <-- You are here: Master Epistemic Directory Map
├── README.md                                       <-- High-level overview and reproduction profiles
├── witnessed_difference_programme.md               <-- Master 278-page monograph (Dimension 1)
├── witnessed_difference_programme.pdf              <-- Typeset PDF publication (Dimension 1)
├── witnessed_difference_programme.tex              <-- LaTeX publication source (Dimension 1)
├── witnessed_difference_programme_claim_ledger.md  <-- Canonical 154-claim ledger (Dimension 1)
├── wd2_finite_distinction_carriers_and_history_escape_claim_ledger.md <-- WD2 claim ledger (Dimension 1)
├── pyproject.toml, uv.lock, LICENSE, LICENSE-CODE  <-- Package configuration & licensing
├── MANIFEST.sha256, SHA256SUMS, source_provenance.json, zenodo_metadata.json <-- Integrity manifests
│
├── code/                                           <-- Codebase: Production, Tests & Derivation Controls
│   ├── witnessed_difference/                       <-- Dimension 1: Production Python modules (+ finite_distinction.py)
│   ├── rust/                                       <-- Dimension 1: Native exact rational solver crate (wdp_finite_witness)
│   ├── finite_observation/, calibrated_recovery/, joint_recovery/ ... <-- Dimension 1: Subsystems
│   ├── derivation_controls/                        <-- Dimension 2: 155 negative controls & boundary checks
│   ├── unit_tests/                                 <-- Dimension 1: Comprehensive unit tests (+ test_finite_distinction.py)
│   └── tests/                                      <-- Dimension 1: Integration & property tests (+ test_finite_distinction.py)
│
├── docs/                                           <-- Four-Quadrant Documentation Spine
│   ├── README.md                                   <-- Master Documentation Navigation Matrix
│   ├── 01_substantiated/                           <-- Quadrant 1: Exists / Substantiated (Verified proofs & notes)
│   ├── 02_requiring_derivation/                    <-- Quadrant 2: Requires Derivation (Open proofs & active targets)
│   ├── 03_deletion_and_archive/                    <-- Quadrant 3: Can Be Deleted / Quarantined (Withdrawn & historical)
│   └── 04_roadmap_and_gaps/                        <-- Quadrant 4: Remains to be Derived (Bridge register & continuum)
│
├── lean4/                                          <-- Formal Lean 4 Verification Spine
│   ├── lakefile.lean, lean-toolchain, lake-manifest.json <-- Lake configuration
│   ├── claim_map.md, axiom_report.txt              <-- Theorem-to-claim mappings and axiom reports
│   ├── WitnessedDifference.lean                    <-- Root module exporting the formal spine
│   ├── WitnessedDifference/                        <-- Dimension 1: 101 formal modules (+ FiniteDistinction.lean)
│   └── axioms/                                     <-- Dimension 3: Consolidated 55 individual *_axioms.txt logs
│
├── evidence/                                       <-- Dimension 1: 17 JSON formal execution receipts
├── manifests/                                      <-- Dimension 1: Verification and coverage manifests
└── jupyter_notebooks/                              <-- Dimension 1: 12 illustrative replay notebooks
```

---

## 2. Fast O(1) Epistemic Lookup Matrix

| Dimension | Directory / Location | Epistemic Status | Intended Action for Automated Agents & LLMs |
|---|---|---|---|
| **Dimension 1: What Exists** | `code/witnessed_difference/`<br>`lean4/WitnessedDifference/`<br>`docs/01_substantiated/`<br>`witnessed_difference_programme.md` | **SUBSTANTIATED**<br>Formally proved theorems, passing test suites, and verified claims. | **TRUST & REUSE**<br>Use as verified ground truth for imports, type definitions, and proven theorems. |
| **Dimension 2: Requires Derivation** | `docs/02_requiring_derivation/`<br>`code/derivation_controls/` | **OPEN / ACTIVE CONJECTURE**<br>Active research targets, 5 outstanding derivations, Meron limits, and open Lean targets. | **SOLVE & FALSIFY**<br>Active targets for derivation agents; do NOT treat statements as proved theorems. |
| **Dimension 3: Can Be Deleted / Archive** | `docs/03_deletion_and_archive/`<br>`lean4/axioms/`<br>*(Purged `.aux`, `.log`, `.toc`)* | **QUARANTINED / OBSOLETE**<br>14 withdrawn swarm transcripts, historical code snapshots, transient build files. | **IGNORE IN GENERAL SEARCH**<br>Exclude from symbol indexing and retrieval to prevent false positive matches. |
| **Dimension 4: Remains to be Derived** | `docs/04_roadmap_and_gaps/`<br>`dag/wdp_derivation_dag.json`<br>`dag/derivation_dag.json` | **UNCLOSED GAP / ROADMAP**<br>Enlarged Genesis bridge obligations (GEN-WDP-O01..O05), `omega_codex` pre-merge tractability gate, and continuum limits. | **PLAN & TRACK**<br>Long-term architectural milestones; consult `dag/wdp_derivation_dag.json` and `docs/04_roadmap_and_gaps/WDP_DERIVATION_DAG.md` for pre-merge debt accounting. |

---

## 3. Quadrant 1: What Exists in this Programme (Substantiated Core Assets)

### 3.1 Formal Lean 4 Verification Spine (`lean4/WitnessedDifference/`)
101 formally verified modules containing over 340 theorems and lemmas without `sorry` or `admit`:
- `FiniteDistinction.lean`: Formalization of finite Moore machine horizon relations $R_n$, proving equivalence properties (`Wd2.related_refl`, `symm`, `trans`), monotonic refinement (`related_mono`), and permanent fixed-point stabilization (`related_stable`), with the 5-state sharp witness (`sharp_m5_bound`).
- `FiniteDistinctionAxiomReport.lean`: Axiom census verifying that `related_stable` and `sharp_m5_bound` depend on zero axioms.
- `Core.lean`, `Obstruction.lean`, `ObserverResolution.lean`: The degree-1 obstruction window, repair quotient, and pigeonhole resolution bounds.
- `GuardedScheduleTopology.lean`: 37 theorems classifying the real no-$(c+1)$-equal arrangement complement for paired removals/additions.
- `GuardedChainTransport.lean`, `SparseChainTransportBounds.lean`: Minimum-sweep chain transport constructions with polynomial bounds.
- `ExactProgressQuotient.lean`, `CertifiedProgress.lean`: Exact progress quotient and rank monotonicity.
- `BehavioralQuotient.lean`: Abstract Setoid behavioral quotient.
- `ClassicalCorner.lean`, `EmpiricalModel.lean`, `PacketAdapter.lean`: Classical corner reductions, empirical model tables, and CHSH bounds.

### 3.2 Production Python Implementation (`code/`)
- `code/witnessed_difference/`: 35 production modules including `finite_distinction.py` (Moore machine simulation, signatures, stabilization, separating words, report factorization, `FiniteAutomaton`, `distinction_relation`), `cochains.py`, `obstruction.py`, `exact_linear.py`, `quantum.py`, `simplicial.py`, `outcomes.py`.
- `code/unit_tests/` and `code/tests/`: Comprehensive regression suites including `test_finite_distinction.py` (8/8 passing unit and property tests) and 115 passing observation tests.
- `code/rust/`: Native Rust crate `wdp_finite_witness` implementing exact rational LP solvers with zero-authority refusal semantics.

### 3.3 Substantiated Monograph & Proof Notes (`docs/01_substantiated/`)
- `witnessed_difference_programme.md`: Master 278-page publication monograph.
- `witnessed_difference_programme_claim_ledger.md`: 154 canonical claim rows (27 definitions, 82 finite propositions, 15 conditional results, 2 typing propositions, 27 nonclaims, 1 synthesis).
- `wd2_claim_ledger.md`: Rows `WD2-L1` through `WD2-T6`.
- `wd2_finite_distinction_carriers.md`: Absorbed manuscript for finite distinction carriers and history escape.
- `guarded_schedule_topology.md`, `sparse_guarded_chain_transport.md`, `sharp_certified_progress_theorem.md`, `complex_tensor_balancing.md`, `dyadic_refinement_and_duality.md`, `cs_q_presentation_completion.md`, `protected_subgroup_character_quotients.md`, `universal_epistemic_no_go_theorem.md`.
- `derivations/`: 20 completed derivation notes covering table models, rejection rule reuse, and native future retention.

---

## 4. Quadrant 2: What Requires Derivation (Active Open Proofs & Conjectures)

### 4.1 The Five Outstanding Derivation Targets (`docs/02_requiring_derivation/five_outstanding_derivations.md`)
1. **Target 1 (Sharp Observer Completion with Distinct Realization and Repair Images):** WDP-DIM-1 written proof exists; open component is the constructive realization of original physical repair operations (`GEN-WDP-O02`).
2. **Target 2 (Coherence inside Guarded Five-Edit Model Swap Components):** Star-shaped legality condition proved (`GEN-WDP-69`, Appendix P.20); open component is coherence under general non-star-shaped guards and higher cells (`GEN-WDP-O03`).
3. **Target 3 (Minimum-Cost Realizable Observation for Future Operations):** Eight-state table model solved (`docs/01_substantiated/derivations/realizable_observation.md`); open component is physical instrument realization and dynamic vs. static equivalence outside declared tables.
4. **Target 4 (Rejection-Rule Reuse across Changing Representations and Tasks):** Nine-element image carriers solved (`docs/01_substantiated/derivations/rejection_rule_reuse.md`); open component is recursive re-entry across changing checkers and institutional authorization legitimacy (`GEN-WDP-O05`).
5. **Target 5 (Future-Faithful Native Five-Edit Model Compression):** Horizon $h=2$ bound solved (`docs/01_substantiated/derivations/native_future_retention.md`, `NativeFutureCompression.lean`); open component is the sharp general-horizon retention converse for native observers on larger carriers.

### 4.2 Meron Field-Limit Continuum Targets (`docs/02_requiring_derivation/meron_field_limit_derivations/`)
- **Target M1:** Prove or refute missing uniform spatial and time-dependent correlation estimates for joint $(L, M)$ thermodynamic limit.
- **Target M2:** Cumulant bounds and topology for Gaussian spacetime field.
- **Target M3:** All-$M$ spectral gap statement or proof of fixed-carrier bypass.
- **Target M4:** Construction of native physical observation and repair adapters.
- **Target M5:** Repair Chapter 23 toric-code kernel and adaptivity under explicit noise models.
- Active proof draft in progress: `open_derivations/meron_spacetime_limit/` (`meron_spacetime_proof.md`, `meron_spacetime_finite_checks.py`).

### 4.3 Affine Support Noise Thickening (`docs/02_requiring_derivation/affine_thickening_conjecture.md`)
- Finite reduction for affine supports thickened by bounded independent measurement error $\varepsilon > 0$, replacing Appendix Y's discrete finite-fiber argument.

### 4.4 WD2 Distinction Carrier General Proofs (`docs/02_requiring_derivation/wd2_open_targets.md`)
- General Lean 4 formalization of Lemma `WD2-L1` (word kernel agreement), Theorem `WD2-T2` (pigeonhole bound $N \le |S| - b_0$), Theorem `WD2-T3` (no-escape criterion), Theorem `WD2-T4` (distinguishing sequence length $n+1$), Theorem `WD2-T5` (report factorization), and Theorem `WD2-T6` (minimal quotient universal property).

---

## 5. Quadrant 3: What Can Be Deleted / Quarantined (Obsolete & Historical Artifacts)

### 5.1 Permanently Deleted Clutter
- Transient LaTeX build artifacts purged from root: `witnessed_difference_programme.aux` (122 KB), `.log` (101 KB), `.toc` (41 KB).
- Omitted redundant standalone satellite release packaging: `032_...zip` (118 KB), duplicate standalone `pyproject.toml`, and duplicate standalone licenses.

### 5.2 Quarantined Superseded Swarms (`docs/03_deletion_and_archive/superseded_swarms/`)
- 14 historical multi-agent swarm transcripts from earlier exploratory passes, withdrawn in `README.md` and retained only for archive provenance:
  `swarm_empirical_repair.md`, `swarm_functional_classification.md`, `swarm_higher_category.md`, `swarm_legacy_observers.md`, `swarm_observer_adapter_completeness.md`, `swarm_observer_descent.md`, `swarm_original_genesis_observer.md`, `swarm_original_genesis_observer_formal.md`, `swarm_policy_observer_adapter.md`, `swarm_qm_reconstruction.md`, `swarm_quantum_measurement.md`, `swarm_relational_retention.md`, `swarm_retention_choices.md`, `swarm_self_reference_bridges.md`.

### 5.3 Consolidated Lean Axiom Clutter (`lean4/axioms/`)
- 55 historical individual `*_axioms.txt` logs moved from `lean4/` root into `lean4/axioms/`, restoring `lean4/` to a clean, canonical state.

### 5.4 Quarantined Source Archives (`docs/03_deletion_and_archive/source_archive/`)
- `coda_component_packages/`: 113 `.lean` and 214 `.py` files from historical snapshots.
- `meron_model_generation_history/`: Exploratory prompt logs.
- `toric_code_chapter_23_import.md`: Working draft absorbed into Chapter 23.

---

## 6. Quadrant 4: What Remains to be Derived (Roadmap & Epistemic Gaps)

### 6.1 The Five Enlarged Genesis Bridge Obligations (`docs/04_roadmap_and_gaps/genesis_bridge_register.md`)
- **`GEN-WDP-O01`:** Primitive Admission Floor & Context Floor (carrier/signature/law/challenge-generation floor).
- **`GEN-WDP-O02`:** Observer & Repair Realization (source transition/admission systems to WDP bridge by preservation/reflection maps; broad native repair realization).
- **`GEN-WDP-O03`:** Guarded History Coherence, higher cells, global site, quotient functor.
- **`GEN-WDP-O04`:** Continuum / Physics Reconstruction (Lieb–Robinson bound, Trotter cochain extinction, spatial-mesh field theory, Gaussian field law).
- **`GEN-WDP-O05`:** Institutional / Operational / Authorization legitimacy (independent evaluator/grantor separation).

### 6.2 Master Derivation DAG & Standalone WDP Pre-Merge DAG Synchronization
- Standalone WDP DAG: `dag/wdp_derivation_dag.json` and `dag/WDP_DERIVATION_DAG.md` (mirrored at `docs/04_roadmap_and_gaps/WDP_DERIVATION_DAG.md`), classifying all 68 core WDP/WD2 nodes into **30 Discharged/Definitions**, **30 Finite & Tractable Pre-Merge Obligations** (`COMPLETE_BEFORE_OMEGA_CODEX_MERGE`), and **8 Deferred Continuum/External Obligations**.
- Master Gate `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS` in `dag/derivation_dag.json` (Status: `OPEN`).
- Corresponds to derivation records `TFQ-0559` through `TFQ-0587`.
- Next required test: Choose an orientation-sensitive source transition system on `FiniteGenesisWindow` and prove or refute whether `wdpPairDefect` is a preservation-and-reflection morphism for it.

### 6.3 Continuum & Physical Reconstruction Limits
- Non-perturbative construction of interacting quantum fields on discrete carriers.
- Derivation of the Born rule and projective measurement updates from finite distinction carrier stabilization.
- Full mechanized equivalence between native Rust exact rational solvers and Lean 4 cochain transport.

---

## 7. Compliance & Integrity Attestation
This four-quadrant redefinition is fully compliant with:
1. **Clean Architecture Layer Isolation:** Zero host I/O in Lean or Python mathematical kernels.
2. **Claim Hygiene Rule:** No ungrounded claims, no hype verbs, all open questions explicitly marked as unverified targets.
3. **Estate Derivation DAG Consistency:** Fully aligned with `dag/derivation_dag.json` and standalone `dag/wdp_derivation_dag.json` records `TFQ-0559` through `TFQ-0587`.
4. **Tooling & Test Invariance:** 100% pass rate maintained across `pytest` suites and `lake build`.
