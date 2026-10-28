# [TFQ-0012] Locate a Hopf gauge file or keep the gauge datum as the

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `09cc1865-599d-550e-9b04-b82d098ea16f`  
> **Parent Derivation**: [TFQ-0009](../14_finite_gauge/tfq_0009_finite_gauge_cochain.md)

---

## 1. Abstract & Formal Statement

quaternion_gauge_shadow.rs presents Q8 as eight matrices over Q(i), embedded by tfqm_lie_theory::su2_matrix, and treats that finite subgroup of SU(2) as a non-abelian gauge shadow. finite_group.rs can hold a Cayley table for the same shadow, but the table is not an SU(3) color connection. A file search under tfqm_lie_theory/src and quantum_physics/src found no Hopf-algebra module, so Hopf gauge data remains an open obligation next to this shadow. AuthorityEffect on the quaternion module is None. F001.S000 coordinates finite carriers and does not supply color links.

### Governing Obligation
Locate a Hopf gauge file or keep the gauge datum as the Q8 shadow plus Cayley tables.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/QuaternionQ8GaugeShadow.lean`)
- `QuaternionQ8GaugeShadow.q8_group_associativity_unit_and_inverses`: Proves associativity across all `512` triples, two-sided identity, and two-sided inverses for the `Q_8` Cayley table.
- `QuaternionQ8GaugeShadow.q8_nonabelian_hamilton_relations_and_class_equation`: Proves Hamilton's quaternion relations `i² = j² = k² = ijk = -1`, non-commutativity `ij = k ≠ -k = ji`, and the `Q_8` class equation `1 + 1 + 2 + 2 + 2 = 8` with irreducible character degree sum `1² + 1² + 1² + 1² + 2² = 8`.
- `QuaternionQ8GaugeShadow.q8_mat2gi_embedding_homomorphism`: Proves that the `su2_matrix` embedding `q8ToMat2GI : Q8Elem → Mat2GI` over `ℤ[i]` is an exact multiplicative homomorphism across all `64` pairs.
- `QuaternionQ8GaugeShadow.q8_mat2gi_embedding_injective_and_unit_det`: Proves that `q8ToMat2GI` is injective and every embedded matrix has unit Gaussian determinant `1 + 0i`.
- `QuaternionQ8GaugeShadow.q8_plaquette_holonomy_conjugation_and_trace_invariance`: Proves conjugation invariance of the embedded `SU(2)` character trace across all `64` pairs `(g, h) ∈ Q_8 × Q_8`.
- `QuaternionQ8GaugeShadow.q8_su2_vs_su3_color_dimension_and_center_fence`: Proves the `SU(2)` vs. `SU(3)` fundamental dimension (`2 ≠ 3`), Lie algebra dimension (`3 ≠ 8`), and center orders (`2 ≠ 3`) and `8 % 3 = 2 ≠ 0`.
- `QuaternionQ8GaugeShadow.q8_irrep_max_degree_two_no_color_triplet_fence`: Proves that the five `Q_8` irreducible character degrees `(1, 1, 1, 1, 2)` satisfy `1² + 1² + 1² + 1² + 2² = 8` with maximum degree `2 < 3` (and `3² > 8`).
- `QuaternionQ8GaugeShadow.group_like_coproduct_vs_hopf_linearity_fence`: Distinguishes group-like Cayley table elements from general Hopf algebra superpositions.
- `QuaternionQ8GaugeShadow.f001_s000_carrier_coordination_not_color_connection_fence`: Audits `tfq0012RepoLedger` (`hasQ8MatrixShadow = true`, `hasCayleyTable = true`, `hasHopfGaugeModule = false`, `hasSu3ColorConnection = false`).
- `QuaternionQ8GaugeShadow.q8_wilson_plaquette_character_discrete_spectrum_fence`: Proves that the `Q_8` Wilson character trace takes values exclusively in `{-2, 0, 2}`.

### Independent Python Verification (`checks/independent/tfq-0012.py`)
- Executes `1779` exact Gaussian-integer and combinatorial checks across `Q_8` Cayley table laws, `M_2(ℤ[i])` matrix embedding, 4-link plaquette holonomy conjugation, and `SU(3)` / Hopf non-equivalence fences (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0013](tfq_0013_use_cyclotomic_character_tables_only_as_labels_of_a_declared_finite_group.md)
- [TFQ-0043](../18_finite_topological/tfq_0043_keep_ribbon_charges_off_the_color_and_wilson_spine.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
