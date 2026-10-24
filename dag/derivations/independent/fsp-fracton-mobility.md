Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-FRACTON-MOBILITY` (`TFQ-1218`)

AuthorityEffect: None.

## 1. Scope and Narrowed Target

Node `FSP-FRACTON-MOBILITY` (`TFQ-1218` / `FSP-DERIV-054`, stage `FERMION_SIGN`, status `IMPORTED_ASSUMPTION`) records the subdimensional excitation mobility statement of Vijay, Haah, and Fu (2016) for the 3D X-cube stabilizer code:

$$\text{Isolated cube excitations } (B_c = -1) \text{ are immobile 0D fractons, and vertex excitations } (A_v^{(\mu\nu)} = -1) \text{ move only along 1D lines.}$$

While keeping the node status at `IMPORTED_ASSUMPTION`, this note and its local witnesses ([`lean4/CampaignFspFractonMobility.lean`](../../../lean4/CampaignFspFractonMobility.lean) and [`checks/independent/fsp-fracton-mobility.py`](../../../checks/independent/fsp-fracton-mobility.py)) replace the missing `FoliatedFracton2Gauge.lean::fracton_mobility_restriction_isomorphism` reference with local syndrome-weight and excitation-mobility proofs over $\mathbb{F}_2$ and explicit scope fences.

## 2. Cube-Sector 0D Fracton Immobility and 2D Planon Dipoles

1. **Single-edge Pauli-$Z$ quadrupole creation (`xcube_single_edge_pauli_z_excites_four_cubes`)**:
   Every edge $e$ of the 3D cubic lattice $\mathbb{T}^3(L_x, L_y, L_z)$ is shared by $4$ elementary cubes forming a $2 \times 2$ dual plaquette perpendicular to $e$. Applying $Z_e$ anticommutes with all $4$ adjacent cube stabilizers $B_c = \prod_{e' \in \partial c} X_{e'}$, mapping the vacuum syndrome $(0,0,0,0) \in \mathbb{F}_2^4$ (weight $0$) to $(1,1,1,1)$ of Hamming weight $4$ and excitation energy $8 J > 0$.
2. **Isolated fracton hop barrier (`xcube_isolated_fracton_hop_creates_two_extra_fractons`)**:
   Starting from a single excited cube $c_0$ with local 4-cube syndrome $(1, 0, 0, 0)$ (Hamming weight $1$, energy $2 J$), applying $Z_e$ on an incident edge of $c_0$ produces syndrome $((1+1) \bmod 2, 1, 1, 1) = (0, 1, 1, 1)$ of Hamming weight $3$ (energy $6 J$), creating $2$ additional fractons with strict energy barrier $\Delta E = 4 J > 0$. Exhaustive verification across $\mathbb{T}^3(L_x, L_y, L_z)$ for $(L_x, L_y, L_z) \in \{3, 4\}^3$ confirms that every 1-edge $Z_e$ yields weight $3$ or $5$ and every 2-edge $Z_{e_1} Z_{e_2}$ yields weight $\ge 3$.
3. **Rectangular membrane corner law (`xcube_rectangular_membrane_corner_quadrupole_conservation`)**:
   Applying a rectangular dual membrane $M(R_y, R_z) = \prod_{(j, k) \in [0, R_y) \times [0, R_z)} Z_{e_x(0, j, k)}$ flips interior cubes $4 \equiv 0 \pmod 2$ times, straight-edge boundary cubes $2 \equiv 0 \pmod 2$ times, and the $4$ corner cubes $1 \equiv 1 \pmod 2$ time (total syndrome weight $4$), while the foliated leaf-separation penalty $\Delta S(\kappa, R) = \kappa R$ (`FoliatedFractonEngine.evaluate_isolated_fracton_separation`) satisfies $\kappa \le \Delta S(\kappa, R_1) < \Delta S(\kappa, R_2)$ for $1 \le R_1 < R_2$ and $\kappa > 0$.
4. **2D planon mobility of fracton dipoles (`xcube_fracton_dipole_is_2d_planon`)**:
   A pair of adjacent excited cubes separated along the $z$-axis with syndrome $(1, 1, 0, 0)$ (weight $2$, energy $4 J$) translates in the $xy$-plane under $Z_e$ on the shared $x$- or $y$-edge to $(0, 0, 1, 1)$ of equal Hamming weight $2$ and zero energy barrier ($\Delta E = 0$), forming a 2D planon.

## 3. Vertex-Sector 1D Lineon Mobility and Corner-Turn Defect Creation

1. **Lineon pair creation (`xcube_single_edge_pauli_x_excites_lineon_pair`)**:
   At each vertex $v$, the three planar cross stabilizers satisfy $A_v^{(xy)} A_v^{(yz)} A_v^{(zx)} = I$, so the local vertex syndrome $(s_{xy}, s_{yz}, s_{zx}) \in \mathbb{F}_2^3$ satisfies $s_{xy} + s_{yz} + s_{zx} \equiv 0 \pmod 2$. Applying $X_e$ on an $x$-oriented edge excites $(A_v^{(xy)}, A_v^{(zx)})$ with syndrome $(1, 0, 1)$ (weight $2$) at each endpoint.
2. **1D collinear string transport (`xcube_lineon_collinear_string_preserves_weight`)**:
   Extending $X_e$ along a collinear string of $x$-oriented edges cancels the syndrome twice at every interior vertex $((1+1) \bmod 2, 0, (1+1) \bmod 2) = (0, 0, 0)$, keeping the total syndrome weight equal to $4$ ($\Delta E = 0$).
3. **90-degree corner turn leaves an immobile vertex defect (`xcube_lineon_corner_turn_creates_immobile_vertex_defect`)**:
   Attempting to turn an $x$-lineon $(1, 0, 1)$ at vertex $v$ onto a $y$-oriented edge with shift $(1, 1, 0)$ leaves residual syndrome $((1+1) \bmod 2, (0+1) \bmod 2, (1+0) \bmod 2) = (0, 1, 1)$ (a $z$-lineon of weight $2$) at the corner vertex $v$, raising total vertex syndrome weight from $4$ to $6$ with positive energy barrier $\Delta E = 2 J_A > 0$.

## 4. Scope Fences

- **2D planon dipole braiding (`planon_dipole_2d_braiding_obstruction_fence`)**: Composite fracton dipoles move freely in 2D planes ($\Delta E = 0$) and can exchange positions in 2D with odd permutation sign $\operatorname{sgn}(\tau) = -1 < 0$.
- **Intersecting hinge T-junction exchange (`lineon_tjunction_three_step_exchange_fence`)**: Particles confined to 1D segments that meet at a T-junction can swap order via the branch vertex with transposition sign $-1$.
- **No automatic fermion-sign elimination (`mobility_constraints_do_not_imply_fermion_sign_freedom_fence`)**: Subdimensional excitation mobility in a bosonic CSS code does not by itself eliminate fermionic exchange signs, and non-abelian $SU(2)_2$ 2-gauge hinge holonomy $-I_2$ has negative trace $\operatorname{Tr}(-I_2) = -2 < 0$ and defect mass $\Phi_1 = 2 > 0$.
