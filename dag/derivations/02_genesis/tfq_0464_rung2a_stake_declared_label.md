# [TFQ-0464] rung2a-stake-declared-label

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e7617de1-d55f-5505-a807-6bd87365d463`  
> **Parent Derivation**: [TFQ-0462](tfq_0462_rung0_inheritance_replay.md)

---

## 1. Abstract & Formal Statement

Rung two track one (pull request 136) extends the reconstructed sealed grammar by a declared two-sided stake: a label apart, same or free on every ordered pair of datum indices, free on the diagonal, declared once, with a demand a held labelled pair the regime does not honour. A demand comes from a declared label only, at the level of a definition: the free stake carries no demand at any regime and a supply changes no demand. Supply, imposition and, at a well-formed regime, form admission are demand-inert, and from a well-formed base every run of inert events carries exactly the base's demands, so from a demand-free base no demand is first under such a run. Growth generates an apart demand where no instance is admitted, and a same demand only under a separability hypothesis the rung did not discharge.

### Governing Obligation
State the label-source assembly, the three demand-inert kinds and the two growth cases over the stake-extended grammar, keeping the same-demand case conditional on its separability hypothesis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondNoFirst.NoFirst.no_first_demand at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondNoFirst.Run.no_demand_is_first_under_an_inert_run at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondNoFirst.Propagate.growth_generates_apart_of_no_insts at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Declared two-sided stake: apart, same or free on each ordered datum pair (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The names no_first_demand and grammar_carries_no_stake are wider than their statements, which are definitional assemblies with no run, first-occurrence or causal-source conclusion; the represented state is not bridged to the sealed regime (L-1), and a sentence giving the first demand of every run one source was withdrawn against a two-admission counterexample.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/lean/SecondNoFirst/NoFirst.lean::grammar_carries_no_stake`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/NoFirst.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/lean/SecondNoFirst/NoFirst.lean::no_first_demand`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/NoFirst.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/lean/SecondNoFirst/Propagate.lean::growth_generates_apart_of_no_insts`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/Propagate.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/lean/SecondNoFirst/Propagate.lean::growth_generates_same`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/Propagate.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/lean/SecondNoFirst/Run.lean::no_demand_is_first_under_an_inert_run`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/Run.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/nofirst.py::first_demand`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/nofirst.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_nofirst/nofirst.py::inert_event_kinds`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/nofirst.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0465](tfq_0465_rung2b_stake_menu.md)
- [TFQ-0466](tfq_0466_rung3_first_demand_index.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:302`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:189-193`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:349-355`
