# Independent Derivation Note: `FSP-KITAEV-HONEYCOMB-SOLUTION` (`TFQ-1207`)

> **AuthorityEffect**: `None`  
> **Node**: `FSP-KITAEV-HONEYCOMB-SOLUTION` (`TFQ-1207`, Rank 25, Stage `FERMION_SIGN`)  
> **Status**: `IMPORTED_ASSUMPTION` (`E2 -> E3`, `Narrowed`)

---

## 1. Scope and Hypothesis Explicitness

`FSP-KITAEV-HONEYCOMB-SOLUTION` records Kitaev's (2006) four-Majorana representation of the 2D honeycomb spin-$1/2$ model, in which each site spin is written $\tilde{\sigma}_j^\alpha = i b_j^\alpha c_j$ ($\alpha \in \{x, y, z\}$), the $\mathbb{Z}_2$ link operators $\hat{u}_{jk}^\alpha = i b_j^\alpha b_k^\alpha$ and hexagonal plaquette fluxes $W_p = \prod_{(j,k)\in\partial p} \hat{u}_{jk}^{\alpha_{jk}}$ commute with the Hamiltonian and with each other, and within each static gauge sector $u_{jk} \in \{+1, -1\}$ the matter Hamiltonian is quadratic in the $c_j$ Majorana fermions.

This campaign derivation replaces the missing `KitaevHoneycombCore.lean::kitaev_honeycomb_exact_majorana_solution` citation and finite bisimulation fixtures with:
- [`lean4/CampaignFspKitaevHoneycombSolution.lean`](../../../lean4/CampaignFspKitaevHoneycombSolution.lean) (`L4D`, 11 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed by `lake build`).
- [`checks/independent/fsp-kitaev-honeycomb-solution.py`](../../../checks/independent/fsp-kitaev-honeycomb-solution.py) (exact integer and `Fraction` arithmetic, normal and `-O` mode).

---

## 2. Formalized Identities (`lean4/CampaignFspKitaevHoneycombSolution.lean`)

1. **Single-site four-Majorana Clifford & Pauli algebra** (`majorana_site_clifford_relations`, `kitaev_spin_operators_pauli_algebra_and_gauge_commutation`):
   - Explicit $4 \times 4$ integer matrices `bX`, `bY`, `bZ` ($b_\alpha^2 = I_4$) and `ic` ($\tilde{c} = i c$, $\tilde{c}^2 = -I_4$) mutually anticommute.
   - The composite Kitaev spin operators $\tilde{\sigma}^\alpha = b_\alpha \tilde{c}$ satisfy $(\tilde{\sigma}^\alpha)^2 = I_4$, mutual anticommutation $\{\tilde{\sigma}^\alpha, \tilde{\sigma}^\beta\} = 0$ ($\alpha \neq \beta$), commute with the site gauge complex structure $J_D = b_x b_y b_z \tilde{c}$ ($[J_D, \tilde{\sigma}^\alpha] = 0$, whereas $\{J_D, b_\alpha\} = \{J_D, \tilde{c}\} = 0$), and satisfy the chiral identity $\tilde{\sigma}^x \tilde{\sigma}^y \tilde{\sigma}^z = J_D$.
2. **Bond spin-product factorization** (`abstract_bond_spin_product_factorization`):
   - In any associative ring $R$, if the matter Majorana $c_j$ at site $j$ anticommutes with the bond Majorana $b_k$ at site $k$ ($c_j b_k = -b_k c_j$), then $(b_j c_j)(b_k c_k) = -(b_j b_k)(c_j c_k)$, separating the link gauge bilinear $b_j b_k$ from the quadratic matter Majorana bilinear $c_j c_k$.
3. **Plaquette $\mathbb{Z}_2$ gauge invariance, link-flip duality, and closed-surface vortex parity** (`plaquette_flux_local_z2_gauge_invariance`, `hexPlaquetteFlux_sq_eq_one`, `single_link_flip_inverts_two_incident_plaquettes`, `closed_surface_total_plaquette_flux_eq_one`):
   - Under any local vertex $\mathbb{Z}_2$ gauge transformation $u_{ab} \mapsto \eta_a u_{ab} \eta_b$ with $\eta_v^2 = 1$, the hexagonal plaquette flux $W_p = u_{01} u_{12} u_{23} u_{34} u_{45} u_{50}$ is invariant and satisfies $W_p^2 = 1$ when $u_e^2 = 1$.
   - Flipping a shared link $u_{\mathrm{shared}} \mapsto -u_{\mathrm{shared}}$ inverts both incident plaquettes $(W_p, W_q) \mapsto (-W_p, -W_q)$ and preserves $W_p W_q$.
   - On any closed surface where each link $u_e$ ($u_e^2 = 1$) occurs twice across plaquette boundaries, $\prod_p W_p = 1$.
4. **Quadratic matter Majorana skew-symmetry and Pfaffian-squared determinant** (`quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det`):
   - For any $4 \times 4$ skew-symmetric quadratic matter matrix $A(a_{01}, \dots, a_{23})$ over a commutative ring $R$, $A^T = -A$ and $\det(A) = (\mathrm{Pf}_4(A))^2$.
5. **Scope fences on gauge projection and flux-sector sign structure** (`unprojected_majorana_fock_overcounts_physical_spin_space_fence`, `link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence`, `physical_parity_projection_excludes_mismatched_sector_states_fence`):
   - The unprojected $N$-site four-Majorana space has dimension $4^N = 2^N \cdot 2^N$, overcounting the $2^N$-dimensional physical spin space by $2^N$ local $\mathbb{Z}_2$ gauge transformations.
   - Flipping a single link $u_{01} = 1 \mapsto -1$ reverses $\mathrm{Pf}_4(A(u))$ from $+1$ to $-1$ while $\det(A(u)) = +1$ in both sectors ($\mathrm{Pf}(+1) + \mathrm{Pf}(-1) = 0$).
   - The physical parity projector weight $1 + P_{\mathrm{matter}} P_{\mathrm{gauge}}$ vanishes on mismatched parity states $P_{\mathrm{matter}} = -P_{\mathrm{gauge}}$.

---

## 3. Claim Hygiene Summary

1. **What it supports**: On finite honeycomb clusters and closed tori, the four-Majorana representation maps bond spin interactions to products of static $\mathbb{Z}_2$ link bilinears and quadratic $c$-Majorana bilinears, hexagonal plaquette fluxes are invariant under local vertex $\mathbb{Z}_2$ gauge transformations and obey $\prod_p W_p = 1$ on closed surfaces, and each fixed sector's quadratic matter matrix satisfies $\det(A(u)) = \mathrm{Pf}(A(u))^2$, while explicit gauge-projection and Pfaffian sign-flip fences separate fixed-sector quadratic solvability from an unprojected sign-free partition-function claim.
2. **What it does not support**: It does not establish sign-free Monte Carlo sampling of the full thermal spin partition function across all $2^{N_p - 1}$ flux sectors with non-Kitaev perturbations or without explicit physical gauge projection, nor does it establish dynamic adiabatic Berry-phase integration of Ising anyons.
3. **Narrowest defensible claim**: Within the declared finite four-Majorana algebra and static $\mathbb{Z}_2$ link model, bond spin products factor into commuting link variables and quadratic matter Majoranas with $\mathbb{Z}_2$-gauge-invariant plaquette fluxes and $\det(A(u)) = \mathrm{Pf}(A(u))^2$, subject to the $4^N = 2^N \cdot 2^N$ gauge projection and link-flip Pfaffian sign fences.
4. **Next test needed**: Narrow `FSP-LAUGHLIN-EXCHANGE-PHASE` (`TFQ-1208`, Rank 27, `IMPORTED_ASSUMPTION`) by formalizing the finite Vandermonde polynomial exchange algebra and separating it from uncomputed continuum torus Berry-phase integrals.
