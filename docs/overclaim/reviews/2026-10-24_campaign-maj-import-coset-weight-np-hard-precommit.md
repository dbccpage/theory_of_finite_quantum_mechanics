# Pre-Commit Review: `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` (`TFQ-1157`)

AuthorityEffect: None.

- **Node**: `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` (`TFQ-1157` / `MAJ-IMPORT-BMVT`)
- **Stage**: `MAJORANA`
- **Status**: `IMPORTED_ASSUMPTION` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignMajImportCosetWeightNpHard.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/maj-import-coset-weight-np-hard.py` (`PASS: checks=2436 f2_algebra=2048 equivalence=353 greedy_trap=7 scope_fences=28 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: $\mathbb{F}_2^n$ involutive vector space arithmetic, Hamming weight subadditivity $\mathrm{wt}(u \oplus v) + 2\,\mathrm{overlap}(u, v) = \mathrm{wt}(u) + \mathrm{wt}(v)$, primal coset-weight vs parity-check syndrome decoding equivalence, gauge-shift invariance, a 5-coordinate greedy single-flip local-minimum trap, and $3\times 4$ vs $6\times 6$ torus coset budget overflow arithmetic.
  2. **What it does not support**: Does not formalize the Cook-Levin / 3-Dimensional Matching NP-completeness reduction of Berlekamp, McEliece, and van Tilborg (1978) (`IMPORTED_ASSUMPTION` status preserved) and does not imply that planar or toric graph-incidence decoding is NP-hard.
  3. **Scope fences included**: `coset_search_budget_overflow_witness`, `worst_case_code_hardness_vs_planar_toric_scope`, and `bmvt_import_scope_fence`.
