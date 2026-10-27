# CT-QUBIT-NO-CLONING-FINITE-TARGET

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement over Q(i), checked in Lean 4 in the following narrowed form. Take the qubit with the six Pauli eigenstates as rays. (a) The explicit measure-and-prepare maps cloneZ, cloneX and cloneY (rho to the mixture of the two basis clones with weights Tr(P rho)) send each of |0\>,|1\>; |+\>,|-\>; |+i\>,|-i\> to its own clone rho tensor rho; cloneZ is shown trace-preserving. (b) The exact relation |0\>\<0|+|1\>\<1| = |+\>\<+|+|-\>\<-| holds in Herm(2), and the difference of the two clone sums has entry -1/2 on |00\>\<11| and |11\>\<00|, so no additive map (hence no linear map) clones all four of |0\>,|1\>,|+\>,|-\>. (c) The exact squared overlaps of the six states are 1 (equal), 0 (antipodal) or 1/2 (otherwise); for a rational x in \[0,1\], x \<= x^2 forces x in {0,1}; and an exhaustive count over the 64 subsets of the six states shows that exactly 10 subsets are pairwise equal-or-orthogonal (the empty set, 6 singletons and 3 antipodal pairs) and that the maximal such subsets are the three antipodal pairs. In Lean "cloneable subset" in (c) is defined as pairwise equal-or-orthogonal.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: complete positivity of cloneZ, cloneX and cloneY, and trace preservation of cloneX and cloneY (only cloneZ is shown trace-preserving); that completely positive trace-preserving maps cannot decrease fidelity (x \<= x^2 is a hypothesis of the arithmetic lemma, not derived); and the equivalence of the semantic notion "some CPTP map clones every state of the subset" with "pairwise equal or orthogonal" in either direction (the Lean classification takes the latter as the definition of cloneable). The link to the imported definition of a superinformation medium is a reading of definitions.

## Source status

Numeric and algebraic claims verified with exact Python fractions.Fraction arithmetic on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierNoCloning (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `cloneZ_trace_preserving`, `cloneX/Y/Z_clones_*_attribute`, `pauli_Z_X_completeness_identity`, `cloning_defect_ZX_off_diagonal_half`, `no_additive_cloner_for_Z_union_X`, `fidelity_monotonicity_forces_zero_or_one`, `pauli_overlap_idempotent_iff_equal_or_antipodal`, `exhaustive_64_subsets_clonability_classification`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Entanglement.lean`

- file: [lean4/Entanglement.lean](../../../lean4/Entanglement.lean)
- sha256 (`bytes`): `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_constructor_theory.json](../../../dag/research/lean_replay_campaign_constructor_theory.json) (module `Entanglement`): recorded sha256 `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Entanglement`
- counts toward the grade: yes

### Lean: `lean4/FrontierNoCloning.lean`

- file: [lean4/FrontierNoCloning.lean](../../../lean4/FrontierNoCloning.lean)
- sha256 (`bytes`): `90b5c936198509b785c55fd1483f2e329bc1bee48185b8a3176fba383cff80d1`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierNoCloning)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierNoCloning`): recorded sha256 `90b5c936198509b785c55fd1483f2e329bc1bee48185b8a3176fba383cff80d1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierNoCloning`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierNoCloning.cloneX_clones_X_attribute` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.cloneX_clones_X_attribute` |
| `FrontierNoCloning.cloneY_clones_Y_attribute` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.cloneY_clones_Y_attribute` |
| `FrontierNoCloning.cloneZ_clones_Z_attribute` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.cloneZ_clones_Z_attribute` |
| `FrontierNoCloning.cloneZ_trace_preserving` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.cloneZ_trace_preserving` |
| `FrontierNoCloning.cloning_defect_ZX_off_diagonal_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.cloning_defect_ZX_off_diagonal_half` |
| `FrontierNoCloning.exhaustive_64_subsets_clonability_classification` | yes | yes | yes | propext | `#print axioms FrontierNoCloning.exhaustive_64_subsets_clonability_classification` |
| `FrontierNoCloning.fidelity_monotonicity_forces_zero_or_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.fidelity_monotonicity_forces_zero_or_one` |
| `FrontierNoCloning.no_additive_cloner_for_Z_union_X` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.no_additive_cloner_for_Z_union_X` |
| `FrontierNoCloning.pauli_Z_X_completeness_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.pauli_Z_X_completeness_identity` |
| `FrontierNoCloning.pauli_overlap_idempotent_iff_equal_or_antipodal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierNoCloning.pauli_overlap_idempotent_iff_equal_or_antipodal` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2009_ct_qubit_no_cloning_finite_target.md`

- file: [dag/derivations/30_constructor_theory/tfq_2009_ct_qubit_no_cloning_finite_target.md](../../../dag/derivations/30_constructor_theory/tfq_2009_ct_qubit_no_cloning_finite_target.md)
- sha256 (`lf-normalised`): `569c53b76a34ad1da5f7b7a034404132f89bd23df34dc91bc88ef4994895dd08`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2009
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `f34cd1ed156fa81d00adb9c939a21d262964134472af8231083525a54cc7abce`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-CT-QUBIT-NO-CLONING-FINITE-TARGET` `DERIVED_LEAN`: [CT-SUPERINFORMATION-MEDIUM-DEFINITION](CT-SUPERINFORMATION-MEDIUM-DEFINITION.md) (IMPORTED_ASSUMPTION), [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

