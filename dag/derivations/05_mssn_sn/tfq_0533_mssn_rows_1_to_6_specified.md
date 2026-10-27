# [TFQ-0533] mssn-rows-1-to-6-specified

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9310dc27-3279-55f3-b0dc-baf703ad5681`  
> **Parent Derivation**: [TFQ-0532](tfq_0532_mssn_syntax_not_decoding.md)

---

## 1. Abstract & Formal Statement

Atlas rows MSS-1 to MSS-6 are specified targets whose lift status is unlicensed. MSS-1 introduces a single mark ⟨a⟩; MSS-2 specifies irreflexive pairings ⟨ab⟩ and obstructed cuts ⟨⟨ab⟩⟨⟩⟩ and refuses ⟨aa⟩; MSS-3 specifies abstract k-simplices for 0 ≤ k ≤ 3 with ∂² = 0; MSS-4 specifies 1-skeleton graph projections, a k-simplex decomposing into K_{k+1}; MSS-6 specifies stage packets with up-maps u_N and down-maps r_N satisfying r_N(u_N(x)) = x, with typed NON_DESCENT for new terms. MSS-0 is recorded in TFQ-0377, and MSS-5 is not part of this record.

### Governing Obligation
Treat MSS-1, MSS-2, MSS-3, MSS-4 and MSS-6 as specified targets, verify each submitted packet against its row's obligation, and grant no lift between rows.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `External MSS atlas row specifications MSS-1 to MSS-6 (assumption)`

### Further Prerequisites
- [TFQ-0377](../02_genesis/tfq_0377_mss0_only_inscription.md) mss0-only-inscription
- [TFQ-0337](tfq_0337_record_homology_injectivity_under_a_chain_map_retraction_and_record_that_the_two_point.md) Record homology injectivity under a chain-map retraction, and record that the two-point

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> MSS-2 ≠ S(2): the levels README crosswalks MSS-2 post hoc to Genesis S(3) while the level_02 frontmatter names S(2), and either crosswalk is post hoc; each successor rationale is a declared obligation, and evaluator names and error labels are proposed interface labels, not running software.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of rows MSS-1 to MSS-6 as specifications; the homology facts behind MSS-2 and MSS-3 are recorded under TFQ-0337`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust evaluator implements the MSS-1 to MSS-6 row obligations`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python evaluator implements the MSS-1 to MSS-6 row obligations`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0534](tfq_0534_mssn_circulation_obstruction.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `external:sha256:6313c51659873eb093e3ef4171a13eac33217dd96e168a97416623d6248005b9:49-75`
  - `external:sha256:4e709507bd351074c9318b8454b2a4418ffc758a4f28222081607ad0fb3a4628:60`
  - `external:sha256:c11eaf69b4acba8ce20f9899f30478cbafcf397f28894555048836e167a121b2:40`
