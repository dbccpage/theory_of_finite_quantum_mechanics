Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-HINGE-LINEON-SIGN-CLAIM` (`TFQ-1219`)

AuthorityEffect: None.

## 1. Scope and Narrowed Target

Node `FSP-HINGE-LINEON-SIGN-CLAIM` (`TFQ-1219` / `FSP-DERIV-055`, stage `FERMION_SIGN`, status `OPEN`) records the unsupported source claim that because lineons are confined to 1D hinge lines, their worldlines cannot exchange without collision and foliated fracton models are automatically sign-free. Ledger entry `GIN-C24` withdraws the historical `rfl` fixture reading.

While preserving the node status at `OPEN`, this note and its local witnesses ([`lean4/CampaignFspHingeLineonSignClaim.lean`](../../../lean4/CampaignFspHingeLineonSignClaim.lean) and [`checks/independent/fsp-hinge-lineon-sign-claim.py`](../../../checks/independent/fsp-hinge-lineon-sign-claim.py)) formalize both the narrow 1D open-chain regime where nearest-neighbor hardcore fermion worldlines are order-preserving and sign-positive, and the four structural obstructions that invalidate the unrestricted sign-free claim on 3D foliated lattices.

## 2. Isolated 1D Open-Chain Order Preservation and Jordan-Wigner Positivity

1. **Strict order preservation (`open_chain_nearest_neighbor_order_preserved`)**:
   On an isolated 1D open chain, two hardcore particles at strictly ordered sites $x_1 < x_2$ taking nearest-neighbor steps $d_1, d_2 \in \{-1, 0, 1\}$ without site collision ($x_1 + d_1 \neq x_2 + d_2$) or bond crossing ($\neg(x_1 + d_1 = x_2 \wedge x_2 + d_2 = x_1)$) satisfy $x_1 + d_1 < x_2 + d_2$.
2. **Nearest-neighbor Jordan-Wigner string triviality (`open_chain_jordan_wigner_nearest_neighbor_pass_count_zero`)**:
   In the 1D Jordan-Wigner transformation $c_i^\dagger = (\prod_{j < i} Z_j) \sigma_i^+$, a nearest-neighbor hop between adjacent sites $i$ and $i+1$ passes over $(i + 1) - i - 1 = 0$ intermediate sites, yielding Jordan-Wigner factor $(-1)^0 = +1 > 0$.
3. **Closed worldline identity permutation (`open_chain_closed_worldline_identity_permutation_sign_one`)**:
   Any closed two-particle worldline on an open chain that preserves strict site ordering returns to its initial configuration via the identity permutation $1 \in S_2$ with $\operatorname{sgn}(1) = +1 > 0$.

## 3. Four Sign Obstructions Refuting Unrestricted Foliated Fracton Sign-Freeness (`GIN-C24`)

1. **Periodic 1D hinge ring cyclic winding (`periodic_ring_cyclic_winding_even_particle_negative_sign_fence`)**:
   On a closed 1D hinge loop with periodic boundary conditions ($\mathbb{Z}/L\mathbb{Z}$), hopping across the boundary bond $(L-1, 0)$ passes over $N - 1$ occupied interior sites. For any even fermion number $N$ (in particular $N = 2$), the cyclic winding worldline induces an $N$-cycle with odd permutation sign $(-1)^{N-1} = -1 < 0$.
2. **Intersecting 1D hinges / T-junction exchange (`tjunction_intersecting_hinge_exchange_negative_sign_fence`)**:
   In a 3D foliated cubic lattice, $x$-, $y$-, and $z$-hinge lines intersect at lattice vertices. On any 4-vertex T-junction subgraph $\{0, 1, 2, 3\}$ with center $1$, two hardcore fermions starting at $(0, 2)$ exchange positions to $(2, 0)$ via the branch vertex $3$ in $6$ non-colliding steps, inducing the transposition $(0\,1)$ with sign $-1 < 0$.
3. **Corner lineon turn scattering (`corner_lineon_turn_leaves_residual_hinge_defect_fence`)**:
   Turning a 1D lineon around a $90^\circ$ hinge corner leaves a weight-$2$ orthogonal vertex defect $(0, 1, 1)$ at the corner and drops the foliated categorical quantum-double projection trace (`FoliatedFractonEngine.evaluate_foliated_categorical_projection`) from $+4$ to $-2 < 0$ with defect mass $\Phi_1 = 2 > 0$.
4. **Non-abelian 2-gauge hinge commutator holonomy (`su2_pauli_group_commutator_is_neg_identity`, `nonabelian_2gauge_hinge_trace_and_defect_mass_fence`)**:
   For two intersecting non-abelian 2-gauge defect sheets $\Sigma_{xy}$ and $\Sigma_{yz}$ carrying $2 \times 2$ holonomy generators $J = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ and $D = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$, the group commutator along the 1D hinge is $J D J^{-1} D^{-1} = -I_2$, which has negative trace $\operatorname{Tr}(-I_2) = -2 < 0$ and uncancelled defect mass $\Phi_1 = |\operatorname{Tr}(-I_2)| = 2 > 0$.
