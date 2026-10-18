QM_120 Mermin-Peres Cochain Obstruction Claim Ledger
====================================================

**Paper Key:** `003_quantum_foundations/120_mermin_peres_contextuality_cochain_obstruction`  

*v0.1 (Pre-Print)*

Repository note: the canonical number of this artifact is **QM_120** (its
repository directory), fixed by the 2026-06-20 corpus renumber. It is distinct
from `QM_121` (The Finite QM Ingredient Ladder) and `QM_062` (The U(1)-Selector);
this ledger neither renumbers nor replaces those papers.

Claim-ID scheme: `QM-120-C<n>`. The Lean theorem names and certificate field
names referenced below are unchanged.

Encyclopedia: secured as **ENC-1143** (`paper:qm120:MP-CONTEXT-001`, MECHANIZED, 2026-06-19) — the Mermin–Peres contextuality cochain obstruction (F2 main theorem + brute-force witness + LGGR + local satisfiability), Lean axioms verified within `{propext, Classical.choice, Quot.sound}`.

| ID | Claim | Type | Evidence |
| --- | --- | --- | --- |
| QM-120-C1 | Mermin-Peres parity instance is a finite parity-context packet. | DEFINITION | `QM.MerminPeres.packet`; `mermin_peres_parity_certificate.json` |
| QM-120-C2 | Every variable appears in exactly two contexts. | MECHANIZED / PYTHON-EXACT | `QM.MerminPeres.left_global_product_for_any_assignment`; certificate `incidence_counts` |
| QM-120-C3 | Product of all context products from any assignment is `+1`. | MECHANIZED | `QM.MerminPeres.left_global_product_for_any_assignment` |
| QM-120-C4 | Declared signs multiply to `-1`. | MECHANIZED / PYTHON-EXACT | `QM.MerminPeres.declared_sign_product_neg`; certificate `declared_sign_product` |
| QM-120-C5 | No global assignment satisfies all six signed contexts. | MECHANIZED | `QM.MerminPeres.mermin_peres_no_global_assignment` |
| QM-120-C6 | Each individual context is satisfiable. | MECHANIZED / PYTHON-EXACT | `QM.MerminPeres.local_contexts_individually_satisfiable`; certificate `all_single_contexts_satisfiable` |
| QM-120-C7 | Every five-context subset is satisfiable. | MECHANIZED / PYTHON-EXACT | `QM.MerminPeres.every_five_context_subset_satisfiable`; certificate `all_five_context_subsets_satisfiable` |
| QM-120-C8 | This is an LGGR witness: local green, global red. | INTERPRETIVE + MECHANIZED BASIS | `QM.MerminPeres.local_green_global_red` |
| QM-120-C9 | This does not derive QM, Hilbert space, interpretation truth, physical measurement, or authority. | SCOPE FENCE | Paper Sections 0 and 10 |
| QM-120-C10 | The FSP/Meron connection is methodological only: finite packet discipline and LGGR vocabulary, not a Meron or fermion sign-problem solution. | BRIDGE NOTE + SCOPE FENCE | Paper Section 8 bridge note |
| QM-120-C11 | The parity context obstruction is formalized strictly over $F_2$, where $d_0 : F_2^V \to F_2^C$ is the incidence matrix, $\ell \circ d_0 = 0$, and $\ell(s) = 1$. | MECHANIZED | `QM.MerminPeresF2.mermin_peres_f2_cochain_obstruction`; [index:index:MerminPeresF2Cochain.lean](omega_engine/research/_indexes/_master_index.yaml) |

Status Discipline
-----------------

| Status | Meaning in this artifact |
| --- | --- |
| MECHANIZED | Lean theorem builds without `sorry`, `admit`, or declared `axiom`; exported theorem receipts verify axioms are within `{propext, Classical.choice, Quot.sound}`. |
| PYTHON-EXACT | Exact finite enumeration over 512 Boolean sign assignments, no floats. |
| INTERPRETIVE | Omega/GTLA reading of the known Mermin-Peres contextuality proof. |
| SCOPE FENCE | Negative boundary preventing physics or authority overclaim. |

Boundary
--------

The theorem layer proves a finite signed parity obstruction, with the F2 cochain theorem as the main theorem and the concrete brute-force theorem as a witness. It does not prove a
new physics theorem and does not promote contextuality into a full quantum
ontology or an authority constructor.
