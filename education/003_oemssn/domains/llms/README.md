# 10_llms — Domain Research Package

**Directory:** coda_all_universe/1_the_tower/10_llms/  
**Status:** Exploratory extension, not the verified core.  
**Lean re-run:** 2026-09-25, Lean 4.34.1, exit 0 on `lean4/llms_core.lean`. Files at most 40 lines are the shared irreflexivity lemma with this folder's title: `llms_core.lean`.  
Compilation checks the declarations in those files. It does not validate this domain.
**AuthorityEffect:** None  
**Primary Formal Reference:** sealed-derivation-v1 (3100c4e)  

---

## 1. Domain Package Manifest

| Artifact | Type | Description |
| :--- | :--- | :--- |
| [genesis_domain_llms.md](genesis_domain_llms.md) | Master Scenario | Colloquium of Three (Professor, John von Neumann, Lean 4 Expert), 16-step evolution ladder, recovery & gap analysis |
| [lean4/llms_core.lean](lean4/llms_core.lean) | Formal Lean 4 Core | Base setting, distinctness theorem, cotransitivity, and typed gap obstruction |
| [code/domain_llms_kernel.py](code/domain_llms_kernel.py) | Python Kernel | Standalone discrete state transition engine and gap detector |
| [tests/test_llms.py](tests/test_llms.py) | Pytest Suite | Named pytest module. The 2026-09-25 run is the verification summary, not a domain validation. |
| [claim_ledger.md](claim_ledger.md) | Epistemic Ledger | Two-operation coverage table with explicit scope fences |
| [hypothesis_ledger.md](hypothesis_ledger.md) | Hypothesis Ledger | Formal domain hypotheses, testing methods, and invalidation criteria |

---

## 2. Verification Summary

- **Lean 4 Compilation:** Re-run 2026-09-25 with `lean` 4.34.1. 1 file(s) exited 0. This replaces the earlier Lean 4.34.0 sentence.
- **Python:** On 2026-09-25 the README-named test module was included in a 12-module pytest run, 188 passed, exit 0. The old 5/5 sentence is not this run.
- **Epistemic Hygiene:** Strictly bounds all claims; AuthorityEffect: None declared throughout.
