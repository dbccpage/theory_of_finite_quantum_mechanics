# CQFT-REEH-SCHLIEDER-THEOREM-IMPORT

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported property: in a net of local algebras on Minkowski space with a translation action whose generators have positive spectrum (spectrum condition) and a vacuum vector, the vacuum is cyclic for every local algebra, and under further hypotheses separating for the algebra of a region with spacelike complement. The proof uses analytic continuation of translations, hence a continuous translation group and its generator (Stone theorem) on an infinite-dimensional Hilbert space. Both are open nodes of the repository.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- spectrum condition and continuous translation group (assumption)
- vacuum vector (assumption)

## Bottleneck

The inputs of the property are the continuum Hilbert lift and the Stone theorem, which the repository records as open. The gap route below lists them. Checked slice, status unchanged. Narrowed in Lean 4 and an independent Python verifier to three exact finite/algebraic components and non-equivalence fences: (1) over any semiring R and for any dimensions dA, dB (even when dA \< dB), if Fin dA is inhabited then CyclicForA Omega implies SeparatingForAc Omega via matrix associativity (X * Omega) * Y = X * (Omega * Y), so any nonzero right-kernel vector or identically zero column precludes cyclicity even when dA \< dB; (2) discharging the open finite items of TFQ-2107, none of |000\>, |GHZ_3\>, or |W_3\> is cyclic on any single site (s in {0, 1, 2}), |000\> has neither a left inverse nor cyclicity on any pair of sites while |GHZ_3\> and |W_3\> are both cyclic and separating on every pair of sites, all three states have full complementary rank 1 and are cyclic on the full 3-site algebra, and across the 4-qubit 2+2 bipartition neither |0000\> nor |GHZ_4\> is cyclic whereas the 2-Bell-pair cluster state has full complementary rank 4 and is both cyclic and separating; and (3) on a finite N-site ring, cyclicShift N aliases with period N, translation-invariant constant vectors have zero discrete momentum difference, and the translation-invariant 3-qubit product vacuum |000\> fails cyclicity on every proper subsystem.

## Source status

Taken from the cited source as an assumption of this branch; narrowed to dimension-independent cyclicity-implies-separating commutant duality, complete 3-qubit and 4-qubit stabilizer subsystem cyclicity census (discharging the open finite items of TFQ-2107), and discrete cyclic translation aliasing fence in Lean 4 and an independent Python verifier on 2026-10-24.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ReehSchliederImport.lean`

- file: [lean4/ReehSchliederImport.lean](../../../lean4/ReehSchliederImport.lean)
- sha256 (`bytes`): `34c147dbf411a7fdd93b93047c5cd71071211a6b60abc2420fe3c530225dd88f`
- cited in: node.lean, node.source, receipt dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_replay.json (ReehSchliederImport), record TFQ-2106
- replay: `verified`
  - receipt [dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_replay.json](../../../dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_replay.json) (module `ReehSchliederImport`): recorded sha256 `34c147dbf411a7fdd93b93047c5cd71071211a6b60abc2420fe3c530225dd88f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ReehSchliederImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ReehSchliederImport.cyclicShift_periodic_aliasing` | yes | yes | yes | propext | `#print axioms ReehSchliederImport.cyclicShift_periodic_aliasing` |
| `ReehSchliederImport.cyclic_implies_separating` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.cyclic_implies_separating` |
| `ReehSchliederImport.four_qubit_half_system_cyclicity_dichotomy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.four_qubit_half_system_cyclicity_dichotomy` |
| `ReehSchliederImport.full_three_site_cyclic_all_three_states` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.full_three_site_cyclic_all_three_states` |
| `ReehSchliederImport.ghz3_and_w3_pair_cyclic_and_separating` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.ghz3_and_w3_pair_cyclic_and_separating` |
| `ReehSchliederImport.no_left_inverse_of_zero_column` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.no_left_inverse_of_zero_column` |
| `ReehSchliederImport.not_cyclic_of_right_kernel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.not_cyclic_of_right_kernel` |
| `ReehSchliederImport.not_cyclic_of_zero_column` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.not_cyclic_of_zero_column` |
| `ReehSchliederImport.prod3_pair_not_cyclic_and_no_left_inverse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.prod3_pair_not_cyclic_and_no_left_inverse` |
| `ReehSchliederImport.single_site_not_cyclic_all_three_states` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.single_site_not_cyclic_all_three_states` |
| `ReehSchliederImport.translation_invariant_product_vacuum_not_cyclic_for_proper_subsystems` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReehSchliederImport.translation_invariant_product_vacuum_not_cyclic_for_proper_subsystems` |
| `ReehSchliederImport.translation_invariant_zero_momentum_diff` | yes | yes | yes | Quot.sound, propext | `#print axioms ReehSchliederImport.translation_invariant_zero_momentum_diff` |

- counts toward the grade: yes

### Python: `checks/independent/cqft-reeh-schlieder-theorem-import.py`

- file: [checks/independent/cqft-reeh-schlieder-theorem-import.py](../../../checks/independent/cqft-reeh-schlieder-theorem-import.py)
- sha256 (`bytes`): `817557dd378e4df7b3e2c47be62d16b2e6380b04bef27ce317c3d2800b494088`
- cited in: node.source, record TFQ-2106
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2106_cqft_reeh_schlieder_theorem_import.md`

- file: [dag/derivations/31_causal_qft/tfq_2106_cqft_reeh_schlieder_theorem_import.md](../../../dag/derivations/31_causal_qft/tfq_2106_cqft_reeh_schlieder_theorem_import.md)
- sha256 (`lf-normalised`): `df7638df283e1eaa5547c41981e19599a2d58c1d4b4291dc5cd4b2eeb666f1b6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2106
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/cqft-reeh-schlieder-theorem-import.md`

- file: [dag/derivations/independent/cqft-reeh-schlieder-theorem-import.md](../../../dag/derivations/independent/cqft-reeh-schlieder-theorem-import.md)
- sha256 (`lf-normalised`): `1ebb16f910a83489c43ce6324ed272d35c0d80ecd5272ed1ec0af494fd2cf2a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_cqft-reeh-schlieder-theorem-import_independent.json`

- file: [dag/research/campaign_cqft-reeh-schlieder-theorem-import_independent.json](../../../dag/research/campaign_cqft-reeh-schlieder-theorem-import_independent.json)
- sha256 (`lf-normalised`): `afab229e73d3892bb2c875a852ebed18bda42ab4cd48108ad8ba88ef166e9c86`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_mutation.json`

- file: [dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_mutation.json](../../../dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_mutation.json)
- sha256 (`lf-normalised`): `fc9d28ae684cdb451a94d82aaccfb298f1befe01fb6f1ecdd169bdf692376b82`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_replay.json`

- file: [dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_replay.json](../../../dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_replay.json)
- sha256 (`lf-normalised`): `430c102bde184d5dc036c96df5b61bf7a7b02ad832aff51e17d9784a7f7c29fa`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:Nuovo-Cimento-22-1051-1961`
- `external:doi:10.1063/1.1704187`

## Routes

Incoming (2):

- `FRO-R-CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-REEH-SCHLIEDER-1961-SOURCE](CQFT-REEH-SCHLIEDER-1961-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CQFT-REEH-SCHLIEDER-THEOREM-IMPORT-X1` `GAP_NO_DERIVATION`: [FQ-GAP-STONE-CONTINUOUS-TIME](FQ-GAP-STONE-CONTINUOUS-TIME.md) (CONDITIONAL), [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)

Outgoing (1):

- `FRO-R-CQFT-RS-FINITE-CYCLICITY-TARGET` `DERIVED_LEAN`: [CQFT-RS-FINITE-CYCLICITY-TARGET](CQFT-RS-FINITE-CYCLICITY-TARGET.md) (PROVED_LEAN)
