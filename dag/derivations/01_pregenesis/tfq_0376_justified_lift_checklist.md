# [TFQ-0376] justified-lift-checklist

> **Stage**: `PREGENESIS` | **Status**: `OPEN`  
> **UUID**: `e8432211-1bad-54e1-8889-1f40c1a73e5a`  
> **Parent Derivation**: [TFQ-0375](tfq_0375_chain_retraction_old_class.md)

---

## 1. Abstract & Formal Statement

Pre-Genesis `paper.md` section 15, opened at the checklist, says a claim that an extension is necessary or minimal must name the failed predicate, the admissible repairs, the extension class, the cost order, and tied minima. A finite census is exhaustive only on its declared domain, and a budget stop is not an obstruction result. Ledger row `WDP-P001-015` matches that boundary. The finite statement still required is those six checks as separate evidence states for a successor, a proposed lift, and a licensed transition. This node does not close those checks.

### Governing Obligation
A necessary or minimal extension still needs the six section-15 checks, and a budget stop remains incomplete search rather than an obstruction result.

---

## 2. Derivation Context & Mathematical Grounding

1. **Six Distinct Section-15 Evidence Checks (`Section15CheckSlot` in `lean4/CampaignTfq0376Pregenesis.lean`)**:
   - `FailedPredicate`: names the exact predicate failing on the current carrier/regime (e.g., `PreMssn.collapsed_observation_barrier` in `lean4/Imported/PreGenesisToMssn/Paper.lean` or `ChainRetraction.TwoPoints.no_chain_retraction` in `lean4/ChainRetraction.lean`).
   - `AdmissibleRepairs`: enumerates the admissible repair operations inside the declared repair space.
   - `ExtensionClass`: specifies the declared extension class $\mathcal{E}$ over which candidate lifts are drawn.
   - `CostOrder`: specifies the cost valuation / preorder comparing candidate extensions (`FiniteCostReport` in `code/rust/src/wdp/finite_cost_report.rs`).
   - `TiedMinima`: records the full set and cardinality of tied minimal-cost repairs in $\mathcal{E}$ (`tiedMinimaCount`).
   - `SearchCompleteness`: distinguishes `ExhaustiveOnDeclaredDomain(domainSize)` from `BudgetStoppedIncomplete(domainSize, checkedCount)` (`checkedCount < domainSize`), mirroring `CombinatoricsError::BudgetExceeded` in `code/rust/src/combinatorics/enumeration.rs` and `code/rust/src/combinatorics/color_constraints.rs`.
2. **Stage Separation (`TransitionStage`: `Successor`, `ProposedLift`, `LicensedTransition`)**:
   - `Successor` (`qualifiesAsSuccessor`) requires only a declared continuation step (`extensionClassDeclared = true`).
   - `ProposedLift` (`qualifiesAsProposedLift`) requires naming `FailedPredicate`, `AdmissibleRepairs` ($> 0$), and `ExtensionClass`, while leaving `CostOrder`, `TiedMinima`, or `SearchCompleteness` open.
   - `LicensedTransition` (`allSixChecksClosed` and `uniqueMinimalExtensionLicensed`) requires all six checks closed on an exhaustive census (`ExhaustiveOnDeclaredDomain`), with `uniqueMinimalExtensionLicensed` additionally requiring `tiedMinimaCount = 1`.
3. **Budget-Stop Non-Obstruction & Non-Minimality Fence**:
   - Under `BudgetStoppedIncomplete(domainSize, checkedCount)`, both `obstructionCertifiedOnDeclaredDomain` and `allSixChecksClosed` evaluate to `false` (`budget_stop_never_licenses_obstruction_or_minimal_lift`), and `uninspected_tail_witness_refutes_budget_stop_claims` exhibits an explicit 4-candidate domain where stopping at budget $B = 3$ misses the unique feasible / minimal-cost repair at index $3$.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignTfq0376Pregenesis.lean`](../../../lean4/CampaignTfq0376Pregenesis.lean) (`CampaignTfq0376Pregenesis.tfq0376_justified_lift_six_check_scope_certificate`)
- [`lean4/Imported/PreGenesisToMssn/Paper.lean`](../../../lean4/Imported/PreGenesisToMssn/Paper.lean) (`PreMssn.collapsed_observation_barrier`, `PreMssn.refine_separates`, `PreMssn.demand_accounting`)
- [`lean4/ChainRetraction.lean`](../../../lean4/ChainRetraction.lean) (`ChainRetraction.TwoPoints.no_chain_retraction`)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/combinatorics/enumeration.rs`](../../../code/rust/src/combinatorics/enumeration.rs) (`CombinatoricsError::violated_invariant`)
- [`code/rust/src/combinatorics/color_constraints.rs`](../../../code/rust/src/combinatorics/color_constraints.rs) (`minimum_color_violations`)
- [`code/rust/src/wdp/wdp_lggr_chromatic.rs`](../../../code/rust/src/wdp/wdp_lggr_chromatic.rs) (`ChromaticConstraintSystem::evaluate`, `triangle_two_color`)
- [`code/rust/src/wdp/finite_cost_report.rs`](../../../code/rust/src/wdp/finite_cost_report.rs) (`FiniteCostReport::new`)

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0376.py`](../../../checks/independent/tfq-0376.py) (`run_all_checks`)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch07_finite_obstruction_calculus.md`
