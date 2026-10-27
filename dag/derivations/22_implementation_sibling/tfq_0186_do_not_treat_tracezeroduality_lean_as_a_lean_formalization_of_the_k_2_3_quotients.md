# [TFQ-0186] Do not treat TraceZeroDuality.lean as a Lean formalization of the K_{2,3} quotients

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `GAP`  
> **UUID**: `27e8f02b-7475-5d49-bdb1-358ad5ea01f4`  
> **Parent Derivation**: [TFQ-0185](tfq_0185_record_the_k_2_3_finite_certificate_as_the_pair_6_and_9_2_with.md)

---

## 1. Abstract & Formal Statement

TraceZeroDuality.lean is a different object from the K_{2,3} certificate and must not be swapped in for it. Its header cites Paper 080, states a spectral reduction of a trace-zero dual ball to one half of lambda_max minus lambda_min, and lists coboundary invariance of a quotient class. It does not state the graph K_{2,3} or the values 6 and 9/2. FQ-TRACE-ZERO-DUALITY-K23 already records that the K_{2,3} certificates are exact computations and that no Lean theorem for them was found. The obligation is to leave paper 013 without a Lean stand-in. The spectral file is not that stand-in.

### Governing Obligation
Do not treat TraceZeroDuality.lean as a Lean formalization of the K_{2,3} quotients 6 and 9/2.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Hermitian trace-zero defects on a declared graph (assumption)`
- **Admitted**: `complex matrices and full CPTP class (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> GAP-F001-S000-001: Lean DualWitness is a candidate mirror, not a duality certificate for QM_080 Theorems 5-6; the K_{2,3} certificates are exact computations in Rust/Python, no Lean theorem for them. Zenodo 20550459 carries a wrong centered trace-zero dual awaiting erratum.

> [!WARNING]
> No Lean statement of the uniqueness-up-to-scale theorem found; TraceZeroDuality.lean item 3 states only that c||.||_1 is monotone for every c > 0. Rust certifies trace norms of given Hermitian matrices over Q(i), not the theorem.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.k23_uncentered_zero_duality_gap`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DualWitness.lean::dual_witness_certifies_trace_distance`](../../code/lean4/)
- [`lean4/quantum_mechanics/TraceZeroDuality.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/TraceZeroDuality.lean::trace_zero_duality_gap_zero`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`not located`](../../code/rust/src/)
- [`external:sha256:6d5d5d60c5905f79d67d8a8bc365e337b56a0ffb2270da01f2589b4c1a2620f0::PrimalCertificate`](../../code/rust/src/)
- [`external:sha256:8de9a137f60908341dba42d28fa768bf1da772772d76f839787a5fcc9b56f170::TraceNormCertificate`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`external:sha256:268cb7c97325e28274aeeb256645a51550ea6e687fa42b12343e4c63215430ad`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-TRACE-ZERO-DUALITY-K23`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-TRACE-ZERO-DUALITY-K23` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-TRACE-ZERO-DUALITY-K23`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1130, -2260, 1695]`, `chord_potential = 1695`, `holonomy_gamma2 = 2260`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-TRACE-ZERO-DUALITY-K23): 4*idx(113) + 3*stage_rank(7) + route_degree(3) == 476` ($\text{value} = 476$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-TRACE-ZERO-DUALITY-K23): R_raw(261) - G_cob(127) - S_decoy(7) == 127 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 127$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = de44fc4bd6581c92da8ddba49c422db1070b3deac57da8ff1014a69336548778`
