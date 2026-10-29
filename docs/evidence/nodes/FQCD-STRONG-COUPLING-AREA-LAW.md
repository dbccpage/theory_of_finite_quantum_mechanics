# FQCD-STRONG-COUPLING-AREA-LAW

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite gauge group G, a nontrivial irreducible unitary representation R and dimension d \>= 2, there are explicit beta_0 \> 0, K and sigma \> 0 depending on G, R and d such that for 0 \<= beta \< beta_0 the Wilson-action expectation of the R-character of every rectangular Wilson loop C on a finite periodic lattice much larger than C satisfies |\<W_R(C)\>| \<= K exp(-sigma Area(C)), with Area(C) the minimal spanning area.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
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

Formally proved in Lean 4 (lean4/FQCD/StrongCouplingAreaLaw.lean) and checked across Rust and Python; conditional on non-screening/center-protection in d \>= 3, unconditional for abelian and 2D decimation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FQCD/StrongCouplingAreaLaw.lean`

- file: [lean4/FQCD/StrongCouplingAreaLaw.lean](../../../lean4/FQCD/StrongCouplingAreaLaw.lean)
- sha256 (`bytes`): `40efc55c0f98df963bc352276415c1ce0f51176c28894fe413a51df54043d095`
- cited in: node.lean, receipt dag/research/campaign_tfq-1052_lean_replay.json (FQCD.StrongCouplingAreaLaw), record TFQ-1052
- replay: `verified`
  - receipt [dag/research/campaign_tfq-1052_lean_replay.json](../../../dag/research/campaign_tfq-1052_lean_replay.json) (module `FQCD.StrongCouplingAreaLaw`): recorded sha256 `40efc55c0f98df963bc352276415c1ce0f51176c28894fe413a51df54043d095` matches the current file; exit code 0; Lean None; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/FQCD/StrongCouplingAreaLaw.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FQCD.StrongCouplingAreaLaw.abelian_strong_coupling_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.abelian_strong_coupling_area_law` |
| `FQCD.StrongCouplingAreaLaw.center_protected_3d_strong_coupling_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.center_protected_3d_strong_coupling_area_law` |
| `FQCD.StrongCouplingAreaLaw.cubic_invariant_screening_perimeter_receipt` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.cubic_invariant_screening_perimeter_receipt` |
| `FQCD.StrongCouplingAreaLaw.finite_group_2d_character_decimation_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.StrongCouplingAreaLaw.finite_group_2d_character_decimation_area_law` |

- counts toward the grade: yes

### Rust: `code/rust/src/fqcd/strong_coupling_area_law.rs`

- file: [code/rust/src/fqcd/strong_coupling_area_law.rs](../../../code/rust/src/fqcd/strong_coupling_area_law.rs)
- sha256 (`bytes`): `1fff3c425e6804618b2de8efa5e9eb4134fba635a323921ab7d0ef1f4a69f8ad`
- cited in: node.rust, record TFQ-1052
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Python: `code/python/src/fqcd/strong_coupling_area_law.py`

- file: [code/python/src/fqcd/strong_coupling_area_law.py](../../../code/python/src/fqcd/strong_coupling_area_law.py)
- sha256 (`bytes`): `27237e2c05fd53cac02c7359f4cb3d37c4b24e432a5164ae13efb464727583e1`
- cited in: record TFQ-1052
- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md`

- file: [dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md](../../../dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md)
- sha256 (`lf-normalised`): `ca7b8bb919e42c1040546d9d104122c7813296e5c28d0cfa10d434130d517dc6`
- generated view: listed, not counted
- cited in: record TFQ-1052
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `25c22c21f7110959ca9602da6022e7e825c59b24413d303332d4140341e7ebe0`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQCD-R-STRONG-COUPLING-AREA-LAW` `GAP_NO_DERIVATION`: [TFQ-0030](TFQ-0030.md) (COMPUTATIONALLY_CHECKED), [TFQ-0024](TFQ-0024.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

