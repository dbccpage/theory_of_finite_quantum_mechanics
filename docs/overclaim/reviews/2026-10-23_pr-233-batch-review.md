Status: AI-drafted, awaiting human review.

# Independent review of PR #233

AuthorityEffect: None. Reviewed author head `edd1ad9b0d3cdb48de818dcaa8a5c756260ee3dd` against base `5c0ec72fa57e70fdd5fec72569c854b9e5114c0c`.

## Result and acceptance boundary

The stated narrow arithmetic holds. Merge is withheld: `lean4/CampaignDfmCkmPhysicsFence.lean` is L2D under SCORING.md §2, not L4D. Its substantive content is two elementary rational polynomial identities, a four-point numeral table, and two fixed Gaussian-rational products. These do not deliver an intentional general mixing-matrix or quotient API. The mathematical topic and theorem names do not raise capability. The node stays OPEN; no status is promoted.

## Statement versus theorem

| Claim | Declaration and location | Verdict |
|---|---|---|
| Rational difference and sum identities for every n | `cpCount_from_difference`, `constraintCount_sum`, Lean:20–28 | FULL for these polynomial identities |
| Four-point table and n=3 split | `count_table`, `three_generation_split`, Lean:30–51 | FULL for the declared values |
| Two quartets have imaginary parts 0 and 1 | `quartet_real_value`, `quartet_imag_value`, `quartets_differ`, `count_misses_one_quartet`, Lean:74–106 | FULL for these two declared tuples |
| Unitarity or Yukawa reconstruction, physical CP phase counting, measured CKM values | No such declaration | NOT PROVED; remains open |

No graph or unitary matrix is constructed. In particular, these arbitrary tuples are not shown to be entries of a CKM matrix; differing imaginary parts do not refute a theorem restricted to unitary matrices. The note already limits its conclusion to declared quartets.

## Repairs and independent validation

The checker previously accepted bool, float, and text through `Fraction`, and `GR.__eq__` accessed attributes of unrelated objects. Added exact scalar guards, safe equality, and type annotations; strict mypy had 35 errors before and zero after. Thirty invalid-input cases now raise TypeError, and three unrelated equality comparisons return false. Both normal and optimized Python produce the stated exact sample/table/quartet results. A real source mutation adding 1 to `cp_count` fails in both modes at the zero sample. This is one targeted source fault, not broad mutation coverage.

Fresh `lake build CampaignDfmCkmPhysicsFence` succeeds (842 jobs), and direct Lean elaboration prints all eight expected axiom reports, each limited to propext, Classical.choice, and Quot.sound. Mathlib source and manifest both match `56a005855ea17e0b0958f73ec801ae140b0a1679`; the Lean source matches the author's pinned digest. Maximum checker CCN is 17 and cognitive complexity is 20. Complete raw commands and outputs are retained in `dag/research/campaign_dfm-ckm-physics-fence_review_validation.json`.

## Numbers recomputed

The two identities hold in Lean for every rational input; the independent checker tests nine rational samples. It recomputes the cycle/CP pairs (0,0), (1,0), (4,1), (9,3), the n=3 constraint value 3 and difference 4-3=1, and the two imaginary parts 0 and 1. Generated repository-wide README counts and historical tensor descriptors are not independently certified in this focused review. No complete campaign-pipeline success is claimed.

## Scoring

Added source-bound scored YAML companions: substantive proof L2D; independent regression checker L2D under the authorized support exception; declarative Lake registration L1D under that exception. Prior Lake assessments remain append-only. Support exceptions do not cover the substantive proof module. Raising its score without new delivered capability would violate the scoring rubric.

## Scanner and remaining uncertainty

Strict scan exits zero: HIGH=0, MEDIUM=0, LOW=3. The LOW findings are pre-existing tensor receipt-discovery coverage, the date token 20261019, and historical tensor values 1/2 and 1/4. No baseline waiver is added; these tensor claims are not recertified here. The scanner cannot establish the substantive L4 threshold, the physical meaning of counting formulas, or a full campaign-pipeline replay. This PR remains a draft for the capability blocker.
