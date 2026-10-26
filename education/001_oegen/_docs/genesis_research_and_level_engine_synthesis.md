# Genesis Research & Level Engine Historical Synthesis

**AuthorityEffect:** None.
**Contract:** `genesis-research-synthesis/v1`
**Date:** October 2026

This document records the design rationale, findings, and migration history of three historical research modules retired during the October 2026 clean architecture consolidation:
1. `_ooutwire/level_engine`
2. `omega_engine_education/documentation/001_oegen/adversarial_verification`
3. `omega_engine_education/documentation/001_oegen/research_extension`

---

## 1. Adversarial Verification (`001_oegen/adversarial_verification`)

### Provenance and Charter
Introduced in commit `1b42a0071a` (October 1, 2026), `adversarial_verification` was developed as an audit of the educational primitives in `omega_engine_education/documentation/001_oegen/primitives` against the living Genesis repository (`19L57G1`).

### Core Findings
- **Selected Educational Family:** The original 52 Python files and 309 symbols in `primitives/` constituted an educational selection rather than an exhaustive or complete mechanical extraction of the Genesis source.
- **Countermodels & Boundaries:**
  - *Choice from `<>`:* Demonstrated that D2/S2 provide two unpointed isomorphism classes under irreflexive binary assumptions, but are not unique forced derivations from opaque `<>`.
  - *Hamiltonians & Sampling:* Examined hopping Hamiltonians, anticommutation controls, and signed-loop obstructions, demonstrating that they do not automatically solve generic fermion sign problems without explicit physical assumptions.
  - *Logic & Computation:* Checked Boolean evaluation and Turing machine state-transition embeddings.
  - *Regge & Homology:* Audited Čech simplicial complexes and curvature deficit calculations.
- **Axiom Audit:** Established the `verify_lean.py` AST scanner to ensure that all Lean 4 theorems in `001_oegen/primitives/lean4` rely strictly on standard axioms (`propext`, `Quot.sound`) with zero `sorry` statements.

### Canonical Deletion & Asset Preservation
- `verify_lean.py` relocated to [`001_oegen/primitives/scripts/verify_lean.py`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/scripts/verify_lean.py) to support continuous testing in `test_genesis_primitives.py`.
- The adversarial research report and primitive inventory are superseded by this synthesis and the canonical primitives monograph in [`001_oegen/primitives/README.md`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/README.md).

---

## 2. Executed Research Extension (`001_oegen/research_extension`)

### Provenance and Charter
Introduced in commit `a89975da29` (October 2, 2026), `research_extension` implemented the concrete obligations defined in the adversarial verification charter.

### Core Deliverables
- **Formal Refinements:** Proved 22 Lean theorems covering `Basic` and `Erasure` refinement maps between natural-token sequences and abstract carriers.
- **Signed Transport:** Developed the general signed transport obstruction theorem under diagonal $C_2$ gauges.
- **Hamiltonian Sampling:** Built finite transfer polynomial evaluators and rational basis dynamics bridges.
- **Native Rust Delegation:** Executed real Rust owner APIs for simplicial chains, Betti numbers, and discrete 2D Regge curvature diagnostics.

### Canonical Absorption into Rust Crates
The experimental algorithms prototyped in `research_extension` were factored and migrated into sovereign Rust crates:
- `omega_wdp::genesis_geometry`: Simplicial chain analysis, Betti number computations, and metric incidence verification.
- `omega_wdp::genesis_computation`: Ordered event traces, machine step execution, and Boolean graph verification.
- `omega_wdp::genesis_primitives` & `genesis_base_seed`: Absorbed from `omega_ooutwire_primitives` into `omega_wdp`.
- `omega_holonomy::signed_transport`: General cochain transport and holonomy gates.
- `omega_quantum_physics::signed_sampling`: Matrix transfer operators and signed product ratios.
- **Fixture Preservation:** The test fixture [`domain_packets.json`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine/crates_rs/tests/omega_wdp/fixtures/domain_packets.json) was preserved in `omega_wdp/tests/fixtures/` and is validated by `omega_wdp/tests/genesis_geometry_extension.rs`.

---

## 3. Level Engine (`_ooutwire/level_engine`)

### Provenance and Charter
`_ooutwire/level_engine` was originally created as an external standalone repository implementing a Mode E harness for Round E0 of the MSS-N reach plan (design `W2-C02_level_engine.md`). It evaluated levels 000–005 (`bare_inscription`, `first_separation`, `edge_endpoints`, `cell_faces`, `cell_orientation`, `distance_form`) against pinned Genesis commit `965e9d04c5` in `19L57G1` and `research/mssn_sn_tower/atlas/stages.tsv`.

### Migration and Supersession
As recorded in `EPIC-OE-PFP-006` and [`VALIDATION.md`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_governance/contracts/level_engine/v2/_docs/VALIDATION.md):
- The full Level Engine migration had already completed earlier, relocating all 1,647 files, 716 unit tests, 93 specifications, 808 parity checks, and 837 artifacts into:
  - [`omega_engine_symbol_game/infrastructure/tower_research/level_engine/`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_symbol_game/infrastructure/tower_research/level_engine/)
  - [`omega_engine_symbol_game/infrastructure/tower_evidence/level_engine/`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_symbol_game/infrastructure/tower_evidence/level_engine/)
  - [`omega_engine_governance/contracts/level_engine/v2/`](file:///c:/Users/a343o/source/repos/the_symbol_game/omega_engine_governance/contracts/level_engine/v2/)
- `pyproject.toml` packages and exposes `level-engine` directly via `omega_engine_symbol_game.entrypoints.cli.level_engine_commands:main`.
- `EPIC-OE-PFP-006` explicitly mandated: *"Do not re-import the external repository or recreate the retired research/level_engine tree."*
- `_ooutwire/level_engine` represented an obsolete 131-file external prototype. Its full standalone Git history was archived to a Git bundle (`level_engine.bundle`) prior to removal.
