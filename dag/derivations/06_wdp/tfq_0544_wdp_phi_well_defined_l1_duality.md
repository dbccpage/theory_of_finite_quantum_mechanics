# [TFQ-0544] wdp-phi-well-defined-l1-duality

> **Stage**: `WDP` | **Status**: `CONDITIONAL`  
> **UUID**: `e9c07c57-ad2e-591b-9c5f-34c327144059`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

On integer triples, the triangle coboundary is d0(f0, f1, f2) = (f1 - f0, f2 - f1, f2 - f0). For all integer vertex triples f and g, d0(f0 + g0, f1 + g1, f2 + g2) equals the componentwise sum of d0(f) and d0(g), and (delta + d0(g)) - d0(f + g) equals delta - d0(f). The sum of absolute residual entries is unchanged by that shift. For delta = (1, 1, 0), every integer repair has absolute residual sum at least 2, and the repair (0, 1, 0) has absolute residual sum 2. For every integer vertex triple g, delta + d0(g) has absolute residual sum at least 2 at every integer repair, and the repair (g0, 1 + g1, g2) has absolute residual sum 2.

### Governing Obligation
Return the same Φ_J for every representative of a class, report attainment only under the finite-dimensional norm hypothesis, and treat weighted-ℓ¹ strong duality as imported, accepting an instance only with a matching repair and bounded circulation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Finite-dimensional convex (linear-programming) strong duality, REF-MATH-005 Rockafellar Convex Analysis, specialized to the declared weighted graph complex (assumption)`
- **Admitted**: `Attainment hypothesis: repair space finite-dimensional over R or C and J a norm, not a seminorm (assumption)`

### Further Prerequisites
- [TFQ-0538](tfq_0538_wdp_quotient_defect_root_p.md) wdp-quotient-defect-root-p
- [TFQ-0522](../05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md) sn-e08-weighted-l1-duality

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Standing text is the integer triangle coboundary: linearity, residual identity under a vertex shift, and absolute residual sum 2 for delta = (1, 1, 0) and for each integer coboundary shift of that one triple. Representative independence for a general cost, attainment on a real or complex repair space, weighted duality on an arbitrary complex, rational repairs, and a general coefficient field stay open. The weak direction of the duality is not imported (WDP-CH04-P07, TFQ-0348, Lean dual_certificate_lower_bound), and C01 is not shown for arbitrary coefficient spaces.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::absSum_attained`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::absSum_ge_two`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::absSum_shift`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::d0_linear`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::residual_shift`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::shifted_attained`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean::shifted_ge`](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::dual_certificate_lower_bound`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs::FenchelDualityReceipt`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::finite_quotient_l1`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::exact_quotient_l1`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:921-940`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:942-944`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:1342-1359`
