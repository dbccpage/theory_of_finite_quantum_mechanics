# [TFQ-0014] Do not cite the M_2 packet complex or the groupoid algebra as

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `2e607b2e-8fd5-5ae9-9e08-799f459a4a81`  
> **Parent Derivation**: [TFQ-0013](tfq_0013_use_cyclotomic_character_tables_only_as_labels_of_a_declared_finite_group.md)

---

## 1. Abstract & Formal Statement

finite_groupoid_algebra.rs linearizes a ValidatedFiniteGroupoid as convolution over Q(i). The module states that the associated complex C*-algebra is a mathematical extension, not a native finite computation. gauge_cochain_complex.rs is a different object: an exact complex on packets in M_2(Q(i)), with d0 sending anti-Hermitian generators to commutators on effects and states. Neither file is a Hopf gauge theory, and neither file stores SU(3) link variables. The obligation is to keep the groupoid convolution and the qubit packet complex from being cited as the color connection used later in the QCD control.

### Governing Obligation
Do not cite the M_2 packet complex or the groupoid algebra as the color connection.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/CampaignTfq0014FiniteQcd.lean`)
- `CampaignTfq0014FiniteQcd.pair_groupoid_convolution_associative`: Proves associativity of convolution multiplication on the 2-object pair groupoid over `ℤ[i]`.
- `CampaignTfq0014FiniteQcd.pair_groupoid_unit_and_orthogonal_object_idempotents`: Proves that `e₀₀ + e₁₁` is the two-sided convolution unit and `e₀₀ * e₁₁ = 0`.
- `CampaignTfq0014FiniteQcd.groupoid_cstar_norm_requires_sqrt_extension_fence`: Proves the `(2p + 1)² ≠ 2q²` parity obstruction showing that the `C*`-norm `√2` of `e₀₀ + e₀₁` is an analytic extension outside `ℚ`.
- `CampaignTfq0014FiniteQcd.packet_d0_commutator_trace_zero`: Proves that the `M_2(ℤ[i])` packet commutator differential `packetD0 Ω X = [Ω, X]` has zero trace.
- `CampaignTfq0014FiniteQcd.packet_d0_scalar_kernel_and_leibniz_derivation`: Proves that scalar matrices lie in `ker(packetD0 Ω)` and that `packetD0 Ω` satisfies the Leibniz derivation rule.
- `CampaignTfq0014FiniteQcd.packet_d0_jacobi_identity`: Proves the Jacobi identity for `packetD0` on `M_2(ℤ[i])`.
- `CampaignTfq0014FiniteQcd.groupoid_convolution_vs_packet_d0_distinct_objects_fence`: Proves that `groupoidId` is idempotent under convolution (`I₂ * I₂ = I₂`) and annihilated by `packetD0` (`[I₂, I₂] = 0`).
- `CampaignTfq0014FiniteQcd.m2_packet_vs_su3_color_dimension_and_casimir_fence`: Proves the matrix entry (`4 ≠ 9`), Lie generator dimension (`3 ≠ 8`), and fundamental Casimir (`3/4 ≠ 4/3`) fences separating `M_2` packets from `SU(3)` color links.
- `CampaignTfq0014FiniteQcd.neither_module_is_hopf_or_su3_scope_ledger_fence`: Audits `tfq0014RepoLedger` (`hasGroupoidConvolution = true`, `hasM2PacketComplex = true`, `isCStarCompletionNative = false`, `hasHopfGaugeTheory = false`, `hasSu3ColorLinks = false`).
- `CampaignTfq0014FiniteQcd.commutator_derivation_breaks_grouplike_multiplicativity_fence`: Proves that `packetD0` is a Lie derivation (`d₀(σ_z)(σ_x²) = 0`) and not a multiplicative link homomorphism (`(d₀(σ_z)(σ_x))² ≠ 0`).

### Independent Python Verification (`checks/independent/tfq-0014.py`)
- Executes `1185` exact Gaussian-integer and rational checks across 2-object groupoid convolution, `M_2(ℤ[i])` packet commutator derivations, and `SU(3)` / Hopf non-equivalence fences (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0015](tfq_0015_do_not_promote_the_weighted_gell_mann_norms_to_a_closed_su_3_c_lie.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
