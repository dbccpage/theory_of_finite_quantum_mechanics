# Statement-Match Review: TFQ-0012 (`FINITE_QCD`)

- **Reviewed node**: `TFQ-0012`
- **Verdict**: `QUALIFIES`
- **Review date**: `2026-10-24`
- **Reviewer**: Campaign automated & human-guided pre-commit audit

## 1. Statement-to-Evidence Alignment

| Statement Clause | Formal / Computational Anchor | Match Assessment |
|---|---|---|
| `Q8` presented as eight matrices over `Q(i)` / `Z[i]` embedded by `su2_matrix` as a finite subgroup of `SU(2)` | `CampaignTfq0012FiniteQcd.q8_mat2gi_embedding_homomorphism`, `CampaignTfq0012FiniteQcd.q8_mat2gi_embedding_injective_and_unit_det`, `CampaignTfq0012FiniteQcd.q8_plaquette_holonomy_conjugation_and_trace_invariance` | Exact match: faithful 8-element `M_2(Z[i])` homomorphism with unit determinant `1 + 0i` and conjugation-invariant trace. |
| `finite_group.rs` can hold a Cayley table for the same shadow, but the table is not an `SU(3)` color connection | `CampaignTfq0012FiniteQcd.q8_group_associativity_unit_and_inverses`, `CampaignTfq0012FiniteQcd.q8_nonabelian_hamilton_relations_and_class_equation`, `CampaignTfq0012FiniteQcd.q8_su2_vs_su3_color_dimension_and_center_fence`, `CampaignTfq0012FiniteQcd.q8_irrep_max_degree_two_no_color_triplet_fence` | Exact match: `Q_8` Cayley table verified alongside the `2 != 3` fundamental dimension, `3 != 8` Lie algebra dimension, `8 % 3 != 0` center obstruction, and max irrep degree `2 < 3`. |
| No Hopf-algebra module found; Hopf gauge data remains an open obligation; `F001.S000` coordinates finite carriers and does not supply color links | `CampaignTfq0012FiniteQcd.group_like_coproduct_vs_hopf_linearity_fence`, `CampaignTfq0012FiniteQcd.f001_s000_carrier_coordination_not_color_connection_fence`, `CampaignTfq0012FiniteQcd.q8_wilson_plaquette_character_discrete_spectrum_fence`, `checks/independent/tfq-0012.py` | Explicit scope ledger and algebraic fences keeping Hopf gauge data and `SU(3)` color connections as open obligations. |

## 2. Claim Hygiene & Fence Check

- **What it supports**: `Q_8` Cayley table group laws, Hamilton relations, class equation `1 + 1 + 2 + 2 + 2 = 8`, faithful `M_2(Z[i])` `SU(2)` matrix embedding with unit determinant and conjugation-invariant character trace in `{-2, 0, 2}`, and non-equivalence fences against `SU(3)` color connections and unbuilt Hopf gauge modules.
- **What it does not support**: `SU(3)` color gauge connections, Hopf-algebra gauge modules, or continuum Yang-Mills / QCD dynamics.
- **Forbidden words scan**: Zero occurrences of banned hype terms.
