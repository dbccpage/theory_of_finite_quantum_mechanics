# FQCD-STRONG-COUPLING-AREA-LAW

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite gauge group G, a nontrivial irreducible unitary representation R and dimension d \>= 2, there are explicit beta_0 \> 0, K and sigma \> 0 depending on G, R and d such that for 0 \<= beta \< beta_0 the Wilson-action expectation of the R-character of every rectangular Wilson loop C on a finite periodic lattice much larger than C satisfies |\<W_R(C)\>| \<= K exp(-sigma Area(C)), with Area(C) the minimal spanning area.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Prove the bound by a convergent strong-coupling (cluster) expansion in the style of Osterwalder-Seiler (1978), with explicit constants. The bound would replace the declared area-law formula of TFQ-0024 by a derived inequality at strong coupling; it says nothing about weak coupling or the continuum.

## Source status

Formally proved in Lean 4 (lean4/FQCD/StrongCouplingAreaLaw.lean) and checked across Rust and Python; conditional on non-screening/center-protection in d \>= 3 (including S_3, S_4, and A_5 cubic character invariants and d = 4 multi-plaquette boundary collar contraction bounds), unconditional for abelian and 2D decimation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FQCD/StrongCouplingAreaLaw.lean`

- file: [lean4/FQCD/StrongCouplingAreaLaw.lean](../../../lean4/FQCD/StrongCouplingAreaLaw.lean)
- sha256 (`bytes`): `bebd21ce379d3f45ae39af12735c624dc02712c64b5e20a00713b8cbbac01d26`
- cited in: node.lean, receipt dag/research/campaign_tfq-1052_lean_replay.json (FQCD.StrongCouplingAreaLaw), record TFQ-1052
- replay: `verified`
  - receipt [dag/research/campaign_tfq-1052_lean_replay.json](../../../dag/research/campaign_tfq-1052_lean_replay.json) (module `FQCD.StrongCouplingAreaLaw`): recorded sha256 `bebd21ce379d3f45ae39af12735c624dc02712c64b5e20a00713b8cbbac01d26` matches the current file; exit code 0; Lean None; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/FQCD/StrongCouplingAreaLaw.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FQCD.StrongCouplingAreaLaw.a5_cubic_invariants_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.a5_cubic_invariants_exact` |
| `FQCD.StrongCouplingAreaLaw.abelian_strong_coupling_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.abelian_strong_coupling_area_law` |
| `FQCD.StrongCouplingAreaLaw.center_protected_3d_strong_coupling_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.center_protected_3d_strong_coupling_area_law` |
| `FQCD.StrongCouplingAreaLaw.cubic_invariant_screening_perimeter_receipt` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.cubic_invariant_screening_perimeter_receipt` |
| `FQCD.StrongCouplingAreaLaw.d4_multi_plaquette_collar_contraction_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.d4_multi_plaquette_collar_contraction_bound` |
| `FQCD.StrongCouplingAreaLaw.finite_group_2d_character_decimation_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.finite_group_2d_character_decimation_area_law` |
| `FQCD.StrongCouplingAreaLaw.s4_cubic_invariants_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.s4_cubic_invariants_exact` |

- counts toward the grade: yes

### Rust: `code/rust/src/fqcd/strong_coupling_area_law.rs`

- file: [code/rust/src/fqcd/strong_coupling_area_law.rs](../../../code/rust/src/fqcd/strong_coupling_area_law.rs)
- sha256 (`bytes`): `3de9e305324d2a00d21e5abbeece41feb7c28a63502c4b652e864af303e1360d`
- cited in: node.rust, record TFQ-1052
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Python: `code/python/src/fqcd/strong_coupling_area_law.py`

- file: [code/python/src/fqcd/strong_coupling_area_law.py](../../../code/python/src/fqcd/strong_coupling_area_law.py)
- sha256 (`bytes`): `1f2d671a3cbff3d91e57d98861cac8c3bf2e61977322c083228bef997ba9651b`
- cited in: record TFQ-1052
- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md`

- file: [dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md](../../../dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md)
- sha256 (`lf-normalised`): `d09392f20bbd2361d66c9d66b646c3d7545d89e3949d8d16f553cd6eea77dbca`
- generated view: listed, not counted
- cited in: record TFQ-1052
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `8a7a3be8a63e3712d9ab4f9846017c540fad454c328a9c94b79dff8317af75d7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQCD-R-STRONG-COUPLING-AREA-LAW` `GAP_NO_DERIVATION`: [TFQ-0030](TFQ-0030.md) (COMPUTATIONALLY_CHECKED), [TFQ-0024](TFQ-0024.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

