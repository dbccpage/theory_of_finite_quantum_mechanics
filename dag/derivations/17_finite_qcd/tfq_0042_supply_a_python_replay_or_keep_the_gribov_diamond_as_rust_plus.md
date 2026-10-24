# [TFQ-0042] Supply a Python replay or keep the Gribov diamond as Rust plus

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `6181a140-4d12-5202-a730-119fbe654fd4`  
> **Parent Derivation**: [TFQ-0023](tfq_0023_keep_the_3_by_3_betti_count_separate_from_a_link_ensemble.md)

---

## 1. Abstract & Formal Statement

ravera_dfm_finite_to_continuum.rs evaluates evaluate_su3_spanning_tree_vs_landau_gribov_control on CarrierGraph::diamond with five explicit block links over Q(i), checks a non-abelian commutator, and dresses every spanning tree, and it counts diagonal Klein-four copies. Lean su3_diagonal_klein_four_landau_gribov_copies and spanning_tree_dfm_eliminates_gribov_copies treat the copy count 4^3=64 and a tree identity for rational, not matrix, link variables. No Python twin of this function was found under 006_finite_qm/python. The module title uses continuum language; that title is not a bridge theorem.

### Governing Obligation
Supply a Python replay or keep the Gribov diamond as Rust plus a Lean rational shadow.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Exact Python Replay of the 5-Link `Q(i)` Diamond Control**: `checks/independent/tfq-0042.py` replays the 4-vertex, 5-edge diamond graph (`b_1 = 2`, $8$ spanning trees) with five $3 \times 3$ unitary block links over $\mathbb{Q}(i)$, verifying exact unitarity $U^\dagger U = I_3$, $\det(U) = 1$, non-abelian commutator $[U_{01}, U_{12}] \ne 0$, tree-link neutralization across all $8$ spanning trees, and all $4^3 = 64$ diagonal Klein-four copies.
- **Matrix vs Scalar Tree Identity & Title Fence**: `lean4/CampaignTfq0042FiniteQcd.lean` formalizes both non-abelian matrix tree dressing (`matrix_spanning_tree_dressing_neutralizes_tree_links`) and `3x3` color-block non-commutativity (`su3_block_links_nonabelian_commutator_witness`), explicitly separates the 1D rational scalar identity in `FiniteQM.lean` from `3x3` matrix links, and establishes that the continuum-sounding title `ravera_dfm_finite_to_continuum.rs` is not a bridge theorem.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0042FiniteQcd.lean`:
  - `CampaignTfq0042FiniteQcd.diamond_graph_betti_and_spanning_tree_count`
  - `CampaignTfq0042FiniteQcd.su3_block_links_nonabelian_commutator_witness`
  - `CampaignTfq0042FiniteQcd.pythagorean_qi_block_unitarity_and_det_one`
  - `CampaignTfq0042FiniteQcd.matrix_spanning_tree_dressing_neutralizes_tree_links`
  - `CampaignTfq0042FiniteQcd.su3_diagonal_klein_four_landau_gribov_64_copies`
  - `CampaignTfq0042FiniteQcd.lean_finite_qm_rational_shadow_vs_matrix_link_scope_separation`
  - `CampaignTfq0042FiniteQcd.continuum_module_title_is_not_bridge_theorem_fence`
  - `CampaignTfq0042FiniteQcd.missing_006_finite_qm_python_twin_and_independent_replay_fence`
  - `CampaignTfq0042FiniteQcd.gribov_diamond_control_does_not_derive_continuum_qcd_fence`
  - `CampaignTfq0042FiniteQcd.tfq0042_gribov_diamond_and_title_scope_ledger_fence`
- `lean4/FiniteQM.lean`:
  - `FiniteQM.su3_diagonal_klein_four_landau_gribov_copies`
  - `FiniteQM.spanning_tree_dfm_eliminates_gribov_copies`

### Independent Python Verification
- `checks/independent/tfq-0042.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F002.S001`
- **Primary Source Paths**:
  - `lean4/FiniteQM.lean`
  - `lean4/CampaignTfq0042FiniteQcd.lean`
  - `checks/independent/tfq-0042.py`
