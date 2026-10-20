# Derivation DAG from `<>` to finite quantum mechanics: reading note

**AuthorityEffect:** None.

This directory holds `derivation_dag.json`, a derivation graph that starts at the inert inscription `<>` and ends at the state of finite quantum mechanics today. It records what each step rests on and where no source derives the step. It is a map of existing records. It adds no result and promotes no status.

## Model and shape

- The format is the one in `010_mub6/research/derivation_dag_20261011.json`. The path `omega_engine_woland/tests/mub6` named in the request does not exist on main, so that file is the model.
- Nodes carry id, stage, status, source_status, statement, source (file:line or ledger row), lean, rust, imported_structure, bottleneck and tags.
- A route lists the inputs it needs together and one output. Routes with one output are alternatives. A route with status `GAP_NO_DERIVATION` carries no source: it marks a link that no record derives.
- Node statuses are ADMITTED_PRIMITIVE, DEFINITION, PROVED_PROSE, PROVED_LEAN, COMPUTATIONALLY_CHECKED, CONDITIONAL, IMPORTED_ASSUMPTION, OPEN and REFUTED. Route statuses are DERIVED_PROSE, DERIVED_LEAN, COMPUTED, CONDITIONAL_ON_IMPORT and GAP_NO_DERIVATION.
- Nodes named `GP-IMPORT-*` and `L1-IMP-*` are structure the lift or the finite carrier takes in from outside. They are assumptions, not results.
- `see_also` links nodes that two segments each describe. No node was deleted to remove an overlap.

## Segments

- PREGENESIS and GENESIS: `<>` as an inscription (Pre-Genesis paper section 1; `GenesisConstruction.lean::literalRoot`), supplied versus admitted objects, the Genesis regime events and their replay.
- MSSN_SN and WDP: the S(n) presentation carrier and the Witnessed Difference Programme window (Phi1, Gamma2).
- L1_EMERGENCE: the observer axioms, the L1 weights and the residual-sector declaration.
- L1_TO_L2: QM_020 theorems 1 to 7, the imports the lift needs (square root, complex field, U(1) phases, inner product, orthogonal additivity, phase-averaged shadows, isometric dynamics), and what QM_122 recovers.
- FINITE_QM_CORE, FINITE_QM_DYNAMICS and FINITE_QM_STRUCTURE: `006_finite_qm` and the 003 papers after QM_020 (path sums, measurement update, product defect, Bell and CHSH, trace norm, authority boundary, contextuality, the five-import cascade).
- IMPLEMENTATION: Rust and Lean artifacts in `omega_quantum_physics` and the other crates.

## Gaps on the path from `<>`

These links have no derivation in any source I read. Each is a `GAP_NO_DERIVATION` route.

- The inscription `<>` to the admitted root Difference joined with Structure. The root is defined separately (ENC-1138, GTLA rule 2).
- Genesis regime events to the obligation monoid, and from there to the WDP bridge obligations and the degree-1 window.
- The Phi1/Gamma2 residual to the declared L1 sector weights.
- The L1 weights to the square-root field, the complex field, U(1) phases, the inner product, orthogonal additivity, Haar-independent phases and linear isometric dynamics. QM_122 recovers only matrices over the Gaussian integers.
- The primitive-difference quotient to the declared quantum interface, and to the selection of quantum mechanics.
- Born and Gleason uniqueness, tensor uniqueness, the U(1) circle, Stone's theorem and the continuum Hilbert lift. These are open nodes that finite quantum mechanics takes as declared imports.
- Stochastic kernels to completely positive maps, the qubit and Bell-theorem nodes (QM_072, QM_073), and Tier-3 uniqueness (QM_093).

## Proposed work, not merged

Draft pull requests exist for five theorem nodes and one Lean file. They appear as OPEN or IMPL nodes tagged `proposed-pr-open`. None is counted as proved on main.

- #1156 Pre-Genesis listed-history constructive summary.
- #1158 Genesis supply erasure (axioms: propext).
- #1157 S(n) off-image refusal. It is marked proposed here because the merge was not confirmed when the graph was built.
- #1161 FSP switching normal form NF-002 is historical PR context. The current DAG records T1-T5 and duplicate-free enumeration of length 2^numChord, with numChord=|E|-|V|+c; the count is no longer a residual obligation. This does not refresh the historical PR merge state.
- #1155 Thymus screening soundness.
- #1160 `LggrFiniteResults.lean`.

## Validation and limits

- `validate_derivation_dag.py` checks schema, vocabulary, reference resolution, acyclicity, that every derived node has an incoming route, forbidden words, and that cited paths and symbols exist. It checks structure only. It does not check that a source says what a node says.
- Command: `python validate_derivation_dag.py` from this directory. Expected result: `failures=0`.
- Lean and Rust cells were checked by file and symbol presence, not by building them.
- Some ledgers cite Lean names that are not on disk. Those cells were dropped or left empty and are listed in `segment_notes`.
- The file `derivation_dag.json` is data. Edit it through its fragments, not by hand, if the graph grows.

## Application branches added 2026-10-20

The [application fragment](fragments/application_branches.json) connects dressing fields, MUBs and FSP to the existing DAG. Regenerate the DAG and master indices with `python dag/sync_application_branches.py`; use `--check` for a read-only synchronization check. The [master index](derivations/README.md) links all branch papers. The new graph-dressing theorem admits its group and forest; MUB dimension-six and general FSP sampling obligations remain open. Historical extraction notes above do not override current node status or the stated theorem hypotheses.
