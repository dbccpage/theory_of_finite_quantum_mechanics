# CQFT-CAUSAL-FACTORIZATION-IMPORT

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported property, audited and corrected against Epstein and Glaser (1973, Section 1.1 condition (C.A.) pp. 214-215, Section 2.1 condition (Caus. 1) eq. (9) p. 218, Section 2.2 eq. (30) p. 223) and Brunetti and Fredenhagen (2000, arXiv:math-ph/9903028, Section 1 eq. (2) p. 4 and Section 3 Condition P3 p. 15): the scattering operator satisfies V(g, h1+h2) = S(g)^{-1} S(g+h1+h2) = V(g, h1) V(g, h2) (and at g=0, S(g1+g2) = S(g1) S(g2)) whenever supp h1 does not intersect the causal past of supp h2, written supp h1 cap (supp h2 + V^-) = empty (which includes spacelike separation as well as causal future separation, not only supp h1 inside the causal future of supp h2). Equivalently at each order n, the time-ordered operator-valued distributions factorize as T(P union Q) = T(P) T(Q) whenever {x_i : i in P} cap ({x_j : j in Q} + V^-) = empty (eq. (30) p. 223; Condition P3 p. 15), and renormalization reduces to extending time-ordered products across the total diagonal. The repository has neither operator-valued distributions nor a continuum Minkowski causal cone. Narrowed in Lean 4 and an independent Python verifier to three exact finite/algebraic components and non-equivalence fences: (1) over any group G and additive coupling carrier A, the relative Bogoliubov operator bogoliubovV S g h = (S g)^{-1} * S(g + h) satisfies V(g, 0) = 1, the unconditional telescoping cocycle law V(g, h1) * V(g + h1, h2) = V(g, h1 + h2), and the equivalence V(g, h1 + h2) = V(g, h1) * V(g, h2) \<-\> V(g + h1, h2) = V(g, h2), while on the diamond poset C2 the Epstein-Glaser separation predicate noInCausalPast C2 holds symmetrically for spacelike (\[d1\], \[d2\]) and one-way for future-before-past (\[d1, d2, d3\], \[d0\]); (2) on the 4-element N poset (0 \< 2, 1 \< 2, 1 \< 3), all 5 linear extensions extN0..extN4 are connected by chains of adjacent spacelike swaps (SpacelikeSwapChain posetN) and have identical ordered products for every spacelike-commuting monoid assignment (discharging the finite-poset connectivity question of TFQ-2110), while anticommuting Pauli operators X, Z on (n0, n3) flip the sign between extN3 and extN4; and (3) coincident pairs (x, x) on a FiniteStrictPoset are never spacelike separated, the 4D Epstein-Glaser polynomial counterterm dimension binom(omega + 4, 4) equals (1, 5, 15, 35, 70) for omega = 0..4, and off-diagonal factorization (x != y) leaves coincident-diagonal contact counterterms c unconstrained.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- operator-valued distributions (assumption)
- time ordering on spacetime (assumption)

## Bottleneck

Audited against Epstein-Glaser (1973) eqs. (9), (30) and Brunetti-Fredenhagen (2000) eq. (2) and Condition P3. The continuum distribution extension has no counterpart in the repository's finite posets.

## Source status

Audited and corrected against the full texts of Epstein and Glaser (1973, Section 1.1 pp. 214-215, Section 2.1 eq. (9) p. 218, Section 2.2 eq. (30) p. 223) and Brunetti and Fredenhagen (2000, arXiv:math-ph/9903028, Section 1 eq. (2) p. 4, Section 3 Condition P3 p. 15) on 2026-10-22; narrowed to Bogoliubov cocycle/shift-invariance equivalence, complete posetN swap connectivity and product equality, and coincident-diagonal counterterm ambiguity fence in Lean 4 and an independent Python verifier on 2026-10-24.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignCqftCausalFactorizationImport.lean`

- file: [lean4/CampaignCqftCausalFactorizationImport.lean](../../../lean4/CampaignCqftCausalFactorizationImport.lean)
- sha256 (`bytes`): `5dd49f73d783b5d3b3f732ac46e4431428eb7054132e27bd37e111901cb0549f`
- cited in: node.lean, node.source, receipt dag/research/campaign_cqft-causal-factorization-import_lean_replay.json (CampaignCqftCausalFactorizationImport), record TFQ-2109
- replay: `verified`
  - receipt [dag/research/campaign_cqft-causal-factorization-import_lean_replay.json](../../../dag/research/campaign_cqft-causal-factorization-import_lean_replay.json) (module `CampaignCqftCausalFactorizationImport`): recorded sha256 `5dd49f73d783b5d3b3f732ac46e4431428eb7054132e27bd37e111901cb0549f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCqftCausalFactorizationImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignCqftCausalFactorizationImport.bogoliubovV_causal_factorization_at_zero_iff` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_causal_factorization_at_zero_iff` |
| `CampaignCqftCausalFactorizationImport.bogoliubovV_cocycle_telescoping` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_cocycle_telescoping` |
| `CampaignCqftCausalFactorizationImport.bogoliubovV_factorization_iff_background_shift_invariance` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_factorization_iff_background_shift_invariance` |
| `CampaignCqftCausalFactorizationImport.bogoliubovV_zero` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_zero` |
| `CampaignCqftCausalFactorizationImport.c2_epstein_glaser_separation_asymmetry` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.c2_epstein_glaser_separation_asymmetry` |
| `CampaignCqftCausalFactorizationImport.coincident_diagonal_not_spacelike_and_counterterm_dim` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.coincident_diagonal_not_spacelike_and_counterterm_dim` |
| `CampaignCqftCausalFactorizationImport.diagonal_counterterm_preserves_off_diagonal_factorization` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignCqftCausalFactorizationImport.diagonal_counterterm_preserves_off_diagonal_factorization` |
| `CampaignCqftCausalFactorizationImport.posetN_all_five_extensions_swap_connected` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.posetN_all_five_extensions_swap_connected` |
| `CampaignCqftCausalFactorizationImport.posetN_all_five_ordered_products_eq` | yes | yes | yes | propext | `#print axioms CampaignCqftCausalFactorizationImport.posetN_all_five_ordered_products_eq` |
| `CampaignCqftCausalFactorizationImport.posetN_all_spacelike_pairs` | yes | yes | yes | none | `#print axioms CampaignCqftCausalFactorizationImport.posetN_all_spacelike_pairs` |
| `CampaignCqftCausalFactorizationImport.posetN_exact_five_linear_extensions` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCqftCausalFactorizationImport.posetN_exact_five_linear_extensions` |
| `CampaignCqftCausalFactorizationImport.posetN_pauli_commuting_vs_anticommuting_witness` | yes | yes | yes | propext | `#print axioms CampaignCqftCausalFactorizationImport.posetN_pauli_commuting_vs_anticommuting_witness` |
- counts toward the grade: yes

### Python: `checks/independent/cqft-causal-factorization-import.py`

- file: [checks/independent/cqft-causal-factorization-import.py](../../../checks/independent/cqft-causal-factorization-import.py)
- sha256 (`bytes`): `2d3005b22a2c61edb854c646a946300fa29958352f49a7e8ce194a15a3899083`
- cited in: node.source, record TFQ-2109
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2109_cqft_causal_factorization_import.md`

- file: [dag/derivations/31_causal_qft/tfq_2109_cqft_causal_factorization_import.md](../../../dag/derivations/31_causal_qft/tfq_2109_cqft_causal_factorization_import.md)
- sha256 (`lf-normalised`): `161d79944f69823e27cbcbfbafa493e55ff76dd04edb34e926c25295a7ac9ca8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2109
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/cqft-causal-factorization-import.md`

- file: [dag/derivations/independent/cqft-causal-factorization-import.md](../../../dag/derivations/independent/cqft-causal-factorization-import.md)
- sha256 (`lf-normalised`): `3907ce5b0ae7dedc3a9ec8d38c697fc9e2a9dd0152cef05132b97a685faba446`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_cqft-causal-factorization-import_independent.json`

- file: [dag/research/campaign_cqft-causal-factorization-import_independent.json](../../../dag/research/campaign_cqft-causal-factorization-import_independent.json)
- sha256 (`lf-normalised`): `19c321367f561844ae66fa948beabf696dde1c3c9ab13d87d38e325d30054f64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_cqft-causal-factorization-import_lean_mutation.json`

- file: [dag/research/campaign_cqft-causal-factorization-import_lean_mutation.json](../../../dag/research/campaign_cqft-causal-factorization-import_lean_mutation.json)
- sha256 (`lf-normalised`): `8d2fc00b5589ba48628691887e7eb27cf5143aa81e72141443ff459ae2c48e07`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_cqft-causal-factorization-import_lean_replay.json`

- file: [dag/research/campaign_cqft-causal-factorization-import_lean_replay.json](../../../dag/research/campaign_cqft-causal-factorization-import_lean_replay.json)
- sha256 (`lf-normalised`): `33151041a91b005377ae8d776dda04de4f52afabc9a8cb3d84fcf3a082e826c0`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:math-ph/9903028`
- `external:numdam:AIHPA_1973__19_3_211_0`

## Routes

Incoming (1):

- `FRO-R-CQFT-CAUSAL-FACTORIZATION-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-EPSTEIN-GLASER-1973-SOURCE](CQFT-EPSTEIN-GLASER-1973-SOURCE.md) (SOURCE_RECORD)

Outgoing (1):

- `FRO-R-CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET` `DERIVED_LEAN`: [CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET](CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET.md) (PROVED_LEAN)
