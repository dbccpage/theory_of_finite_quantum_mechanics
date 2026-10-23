# [TFQ-0523] sn-e12-circulation-functional

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e7d71799-b168-52a6-a3e9-d8865af6de80`  
> **Parent Derivation**: [TFQ-0522](tfq_0522_sn_e08_weighted_l1_duality.md)

---

## 1. Abstract & Formal Statement

Example E12 takes the oriented triangle a→b→c→a with C₀ = C₁ = ℤ³, coboundary d₀ and supplied edge record x = (1,0,0). On the open path a→b→c the potential g = (0,1,1) realizes the first two records but predicts −1 on ca. The circulation I(x) = x_ab + x_bc + x_ca vanishes on every d₀g and I(x) = 1, so no integer or rational potential realizes all three records; conversely I(x) = 0 gives the potential (0, x_ab, x_ab + x_bc), so im d₀ = ker I and C¹/im d₀ ≅ ℤ. The combined paper states the same criterion over ℤ, and Cochain.lean establishes it as triangle_repair_invariant and triangle_repair_exact_iff.

### Governing Obligation
Check I∘d₀ = 0, replay the local potential g = (0,1,1), establish both inclusions of im d₀ = ker I, and return I(x) = 1 as the obstruction certificate for x = (1,0,0).

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared oriented incidence of the triangle graph adapter, not the intrinsic meaning of <ab> (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean covers the criterion over ℤ; the rational case is the same written argument. With edge evidence fixed the result is a certificate, not a repair, changing one entry is a separately priced response, and the example is not a Genesis stage.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/PreGenesisToMssn/Cochain.lean::triangle_repair_exact_iff`](../../../lean4/Imported/PreGenesisToMssn/Cochain.lean)
- [`lean4/Imported/PreGenesisToMssn/Cochain.lean::triangle_repair_invariant`](../../../lean4/Imported/PreGenesisToMssn/Cochain.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the converse potential (0, x_ab, x_ab + x_bc); the MSS-N circulation audit is recorded under TFQ-0534`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of E12 in the S(n) strand`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0525](tfq_0525_sn_e19_torsion_erased_over_q.md)
- [TFQ-0526](tfq_0526_sn_e20_observer_completion.md)
- [TFQ-0527](tfq_0527_sn_e21_repair_rank.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md:797-803`
  - `omega_engine_education/documentation/002_oesn/levels/level_12_observer_stack_dda.md:48-51`
  - `omega_engine_education/documentation/002_oesn/levels/level_12_observer_stack_dda.md:52-54`
