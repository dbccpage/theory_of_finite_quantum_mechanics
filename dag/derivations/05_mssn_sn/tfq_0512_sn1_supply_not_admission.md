# [TFQ-0512] sn1-supply-not-admission

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `ff418654-f39d-58f2-819c-4d5c6fff27e7`  
> **Parent Derivation**: [TFQ-0511](tfq_0511_sn0_ground_inertia.md)

---

## 1. Abstract & Formal Statement

S(1) supplies <a>. Supply(<a>) alone leaves the admitted regime unchanged (supply_no_op), and AdmitDatum(<a>) is a separate event that may create one admitted datum. The sealed source records that whether <a> is admitted at Challenge 1 is underdetermined, and that the two sub-readings converge at Challenge 2 because admission deduplicates on presentation identity. With no admitted instances every pair of data is observationally collapsed, even with uniform rules present (collapsed_of_no_insts). The ledger value s₁ = 1 is chosen for the exercise that issues the demand obs_unconsumed_mark and is not inferred from singleton cardinality.

### Governing Obligation
Model supply and admission as different events, so that a supply of <a> admits nothing, and keep s₁ = 1 as a declared ledger entry tied to an issued demand.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Ledger value s₁ = 1 and demand label obs_unconsumed_mark, declared by the S(n) exercise (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The arrival of a mark does not issue a demand for context; S1Supply checks a declared count field, and its admit_mark returns a singleton by construction rather than by a source replay.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::collapsed_of_no_insts`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::supply_no_op`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of supply versus admission in the S(n) strand`

### Python Oracles & Numerical Evaluators
- [`omega_engine_education/documentation/002_oesn/code/sn_core.py::S1Supply`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/002_oesn/code/sn_core.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0513](tfq_0513_sn2_opaque_collapse.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:228-234`
  - `omega_engine_education/documentation/002_oesn/levels/level_01_symbol_genesis.md:19-22`
  - `omega_engine_education/documentation/002_oesn/levels/level_01_symbol_genesis.md:29-32`
