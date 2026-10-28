# [TFQ-0010] Finite QED and electroweak shadow

> **Stage**: `FINITE_QED` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9efdc88c-9a3b-52e2-9b66-5ba88732563b`  
> **Parent Derivation**: [TFQ-0009](../14_finite_gauge/tfq_0009_finite_gauge_cochain.md)

---

## 1. Abstract & Formal Statement

Finite QED here means charged finite transport, a finite Dirac or Clifford shadow, interaction vertices on a finite complex, and finite maps that mirror vacuum polarization, a Lamb shift datum, and an electroweak mixing control. Files under quantum_physics and the finite-QM research notes are computational controls of those maps. The three languages must state the finite identity each control checks. F002 is an interface inventory. Naming a continuum limit on that floor does not derive continuum QED.

### Governing Obligation
Carry finite charged transport, vertices, and Ward shadows without calling the result continuum QED.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Discrete Ward Shadow & Charged Link Transport**: On a finite oriented complex, a conserved 1-chain current $J$ ($d_0^* J = 0$ at every vertex) satisfies exact coboundary gauge invariance $\langle J, A + d_0 \alpha \rangle = \langle J, A \rangle$, and unit-norm Gaussian-rational link transport $U_{ab} \in \mathbb{Q}(i)$ ($|U_{ab}|^2 = 1$) transforms the covariant edge difference $D_{ab}\psi = \psi_b - U_{ab}\psi_a$ covariantly ($D'_{ab}\psi' = g_b D_{ab}\psi$) while preserving $|D_{ab}\psi|^2$.
- **Finite Clifford/CAR & Dirac-Coulomb Fine-Structure Controls**: The 2x2 CAR algebra $c^2 = 0, (c^\dagger)^2 = 0, \{c, c^\dagger\} = I_2$ and occupation projector $N = c^\dagger c$ ($N^2 = N, \mathrm{Tr}(N) = 1$) pair with the exact rational Dirac-Coulomb $n = 2$ fine-structure control ($c_{2s,\mathrm{rel}} + c_{2s,\mathrm{Darwin}} = 13/128 - 8/128 = 5/128 = c_{2p,\mathrm{rel}} + c_{2p_{1/2},\mathrm{SO}} = 7/384 + 8/384$, $\Delta_{\mathrm{FS}} = 1/32\,mc^2 = 1/16\,\mathrm{Ry}$).
- **1-Loop QED Contact Datum & Electroweak Mixing Control**: The 1-loop QED contact coefficient $5/6 - 1/5 + 1/8 = 91/120$ (self-energy $5/6$, Uehling vacuum polarization $-1/5$, anomalous magnetic moment difference $1/8$) and Bethe-lifted rational bracket $232711/30000 > 7$ pair with the Weinberg electroweak projector decomposition ($\sin^2\theta_W + \cos^2\theta_W = 1$, $\Pi_\gamma + \Pi_Z = I_2$, $\Pi_\gamma \Pi_Z = 0$, $M_{\mathrm{neutral}}^2 \Pi_\gamma = 0$, custodial $\rho = 1$) and gauge/gravitational anomaly cancellation at $N_c = 3$.
- **F002 Interface Fence**: `F002` (`F002.S001`) is an interface inventory; naming a continuum limit on that floor does not derive continuum QED.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- `lean4/FiniteQedElectroweakShadow.lean`:
  - `FiniteQedElectroweakShadow.discrete_ward_identity_and_coboundary_gauge_coupling_invariance`
  - `FiniteQedElectroweakShadow.charged_gaussian_rational_link_transport_and_vertex_covariant_difference`
  - `FiniteQedElectroweakShadow.finite_clifford_car_nilpotency_and_occupation_number_projector`
  - `FiniteQedElectroweakShadow.dirac_coulomb_n2_fine_structure_darwin_and_spin_orbit_degeneracy`
  - `FiniteQedElectroweakShadow.qed_one_loop_vacuum_polarization_and_lamb_shift_contact_datum`
  - `FiniteQedElectroweakShadow.weinberg_electroweak_projectors_and_custodial_rho_identity`
  - `FiniteQedElectroweakShadow.gell_mann_nishijima_and_anomaly_cancellation_at_nc3_vs_nc1`
  - `FiniteQedElectroweakShadow.f002_interface_inventory_does_not_derive_continuum_qed_fence`
  - `FiniteQedElectroweakShadow.finite_qed_computational_controls_scope_separation_fence`
  - `FiniteQedElectroweakShadow.tfq0010_finite_qed_and_electroweak_shadow_ledger_fence`
- `lean4/FiniteQM.lean`:
  - `FiniteQM.weinberg_projectors_complete_orthogonal_idempotent`
  - `FiniteQM.ew_custodial_rho_eq_one`
  - `FiniteQM.sm_gell_mann_nishijima_charge_identities`
  - `FiniteQM.sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1`
  - `FiniteQM.car_clifford_nilpotency_and_occupation_projector`
  - `FiniteQM.dirac_coulomb_fine_structure_n2_and_darwin_spin_orbit_degeneracy`
  - `FiniteQM.qed_one_loop_lamb_shift_contact_and_bethe_lifting`

### Independent Python Verification
- `checks/independent/tfq-0010.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `lean4/FiniteQM.lean`
  - `lean4/FiniteQedElectroweakShadow.lean`
  - `checks/independent/tfq-0010.py`
