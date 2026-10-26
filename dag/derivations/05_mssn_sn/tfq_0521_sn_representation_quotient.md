# [TFQ-0521] sn-representation-quotient

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `86d3e34c-bb92-59da-91da-f8cdebd6d204`  
> **Parent Derivation**: [TFQ-0518](tfq_0518_sn_off_image_refusal_proposal.md)

---

## 1. Abstract & Formal Statement

In a supplied complex model with one coordinate at each of two sites, the balance map T sends the ordinary tensor coefficients (rr, ri, ir, ii) to (rr − ii, ri + ir), so for m = n = 1 its rows are (1,0,0,−1) and (0,1,1,0). With u = Tᵗ/2 and r = T, r u = I₂ while u r = P = TᵗT/2 is a rank-2 idempotent, and the vector (1,0,0,1) lies in ker T, so P ≠ I₄. The exact kernel of T is the complex balancing relation. The reading guide uses this as a representation quotient: it names the declared questions that survive and the information quotiented away, and it supplies no native S(n) obstruction.

### Governing Obligation
Check r u = I₂ and u r = P ≠ I₄ for the balance map, exhibit (1,0,0,1) in ker T, and record the quotient as a declared representation with its preserved questions.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared complex scalars and tensor coordinates of the WDP realification supplement (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean states integer coefficient laws (balance after section is doubling, and the kernel test rr = ii, ri = −ir); division by 2 and positivity are written separately. A lawful representation of the selected quantum composite gives neither a new native S(n) obstruction nor permission to advance beyond S(6).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean::balance_kernel_iff`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean::balance_section`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean::twice_project_square`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ComplexTensorBalancing.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs::balance_map_with_limits` (private upstream source, not in this repository)
- `omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs::balance_projector_with_limits` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of the balance map in the S(n) strand`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/complex_tensor_balancing.md:16-21`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/complex_tensor_balancing.md:28-31`
  - `omega_engine_education/documentation/002_oesn/reading_guide.md:69-74`
