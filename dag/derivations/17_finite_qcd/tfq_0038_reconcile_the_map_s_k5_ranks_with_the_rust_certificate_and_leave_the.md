# [TFQ-0038] Reconcile the map's K5 ranks with the Rust certificate and leave the

> **Stage**: `FINITE_QCD` | **Status**: `GAP`  
> **UUID**: `efb4737b-2124-5b1e-9449-b43526665d89`  
> **Parent Derivation**: [TFQ-0037](tfq_0037_keep_slater_car_and_shell_capacities_on_the_identical_particle_side_of_the.md)

---

## 1. Abstract & Formal Statement

Two readings of the K5 torsion must stay apart. The opening of pauli_spin_statistics_graph_finite_map.md states rank_Q of the square boundary as 7 and the rational 2-complex Betti number as 14. The Rust test and the Lean literals use rational Betti number 6 and F2 Betti number 7, hence torsion rank 1. Lean also says whether the exchange loop represents that torsion class is not established. A Python comment in analyze_conf2_graph speaks as if the torsion forces the exchange loop to have order 2. The rank mismatch and the representative question are an open gap beside the certificate.

### Governing Obligation
Reconcile the map's K5 ranks with the Rust certificate and leave the exchange-loop representative unresolved.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Two `Conf_2(K_5)` Boundary Rank Readings Kept Apart**: On $\mathrm{Conf}_2(K_5)$ ($V = 10, E = 30, b_1^{(1)} = 21$, with $15$ disjoint-edge commuting squares), the $30 \times 15$ disjoint-edge square boundary matrix has exact rational rank $15$ (and $\mathbb{F}_2$ rank $14$), giving the Rust test and `FiniteQM.lean` certificate reading (`graph_conf2_exchange_betti_and_character_collapse`) $b_1^{(2)}(\mathbb{Q}) = 21 - 15 = 6$, $b_1^{(2)}(\mathbb{F}_2) = 21 - 14 = 7$, and torsion rank $7 - 6 = 1$. By contrast, the opening prose of `pauli_spin_statistics_graph_finite_map.md` states $\mathrm{rank}_{\mathbb{Q}} = 7$ and $b_1^{(2)}(\mathbb{Q}) = 21 - 7 = 14$. The two readings differ by $\Delta \mathrm{rank}_{\mathbb{Q}} = 8$ and must be recorded side by side without conflation.
- **Unresolved Exchange-Loop Representative**: Even when $\dim_{\mathbb{F}_2} \mathrm{Tors}(H_1) = 1$ (as in $H_1 \cong \mathbb{Z}^6 \oplus \mathbb{Z}_2$), a specific geometric exchange loop $\gamma_{\mathrm{exch}}$ is not forced by the torsion rank alone to have order $2$; the Python comment in `analyze_conf2_graph` exceeds the certificate scope, and the representative question remains an open gap.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0038FiniteQcd.lean`:
  - `CampaignTfq0038FiniteQcd.conf2_graph_1skeleton_betti_numbers_p3_y_c4_k4_k5`
  - `CampaignTfq0038FiniteQcd.conf2_c4_and_k4_2complex_rational_betti_numbers`
  - `CampaignTfq0038FiniteQcd.k5_map_prose_reading_rank7_betti14_vs_certificate_reading_rank15_betti6`
  - `CampaignTfq0038FiniteQcd.universal_coefficient_torsion_rank_identity`
  - `CampaignTfq0038FiniteQcd.abelian_1d_character_collapse_boson_fermion`
  - `CampaignTfq0038FiniteQcd.non_zero_torsion_rank_does_not_identify_specific_loop_representative`
  - `CampaignTfq0038FiniteQcd.exchange_loop_representative_question_remains_open_fence`
  - `CampaignTfq0038FiniteQcd.python_comment_order_two_claim_exceeds_certificate_fence`
  - `CampaignTfq0038FiniteQcd.k5_rank_mismatch_recorded_beside_certificate_fence`
  - `CampaignTfq0038FiniteQcd.tfq0038_k5_torsion_and_exchange_loop_scope_ledger_fence`
- `lean4/FiniteQM.lean`:
  - `FiniteQM.graph_conf2_exchange_betti_and_character_collapse`

### Independent Python Verification
- `checks/independent/tfq-0038.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `lean4/FiniteQM.lean`
  - `lean4/CampaignTfq0038FiniteQcd.lean`
  - `checks/independent/tfq-0038.py`
