Status: AI-drafted, awaiting human review.

# Independent Derivation & Scope Audit: `FSP-XCUBE-FRACTON-MODEL` (`TFQ-1217` / `FSP-DERIV-053`)

AuthorityEffect: None.

## 1. Audited Statement & Governing Obligation

- **Node**: `FSP-XCUBE-FRACTON-MODEL` (`TFQ-1217`, stage `FERMION_SIGN`, source record `FSP-DERIV-053` in `papers/core/fsp/theory_of_finite_fsp.jsonl`).
- **Audited Statement**:
  > Vijay-Haah-Fu (2016): the X-cube model on an Lx x Ly x Lz periodic cubic lattice has pairwise commuting vertex and cube terms and ground-state degeneracy 2^(2Lx + 2Ly + 2Lz - 3).
- **Governing Obligation**:
  > Imported literature result; the checkout has no X-cube stabilizer computation, and it has no fermion-sign consequence by itself.

---

## 2. Mathematical Derivation of the X-Cube CSS Stabilizer Code on $\mathbb{T}^3$

### 2.1 Edge Qubit Carrier and CSS Generators

On a periodic cubic lattice $\mathbb{T}^3(L_x, L_y, L_z) = \mathbb{Z}_{L_x} \times \mathbb{Z}_{L_y} \times \mathbb{Z}_{L_z}$ with $V = L_x L_y L_z$ vertices and $C = L_x L_y L_z$ elementary cubes, each vertex originates three oriented edges along the $x, y, z$ axes, giving $N_e = 3 L_x L_y L_z$ physical edge qubits. The X-cube Hamiltonian (Vijay, Haah, and Fu 2016) is a Calderbank-Shor-Steane (CSS) stabilizer model
$$H_{\text{XC}} = -\sum_{v \in V} \left(A_v^{(xy)} + A_v^{(yz)} + A_v^{(zx)}\right) - \sum_{c \in C} B_c,$$
where:
- $B_c = \prod_{e \in \partial_1 c} X_e$ acts with Pauli $X$ on the $12$ edges of elementary cube $c$ ($C = V$ generators).
- $A_v^{(\mu\nu)} = \prod_{e \in \text{star}_{\mu\nu}(v)} Z_e$ acts with Pauli $Z$ on the $4$ edges incident to vertex $v$ lying in plane $\mu\nu \in \{xy, yz, zx\}$ ($3V$ generators).

### 2.2 Pairwise Commutativity $[A_v^{(\mu\nu)}, B_c] = 0$

Two Pauli operators $A_v^{(\mu\nu)}$ ($Z$-type) and $B_c$ ($X$-type) commute if and only if their edge supports intersect in an even number of edges. If $v$ is not one of the $8$ corners of $c$, their overlap is $0$. If $v$ is a corner of $c$, the three edges of $c$ incident to $v$ have axis indicator $\mathbf{c}_v = (1, 1, 1)$, while the three planar crosses at $v$ have axis indicators
$$\mathbf{p}_{xy} = (1, 1, 0), \qquad \mathbf{p}_{yz} = (0, 1, 1), \qquad \mathbf{p}_{zx} = (1, 0, 1).$$
For every plane $\mu\nu \in \{xy, yz, zx\}$, the inner product is
$$\mathbf{c}_v \cdot \mathbf{p}_{\mu\nu} = 2 \equiv 0 \pmod 2,$$
so $|\operatorname{supp}(A_v^{(\mu\nu)}) \cap \operatorname{supp}(B_c)| \in \{0, 2\}$ is always even and $(-1)^{|\operatorname{supp}(A_v^{(\mu\nu)}) \cap \operatorname{supp}(B_c)|} = +1$.

### 2.3 Stabilizer Syzygies, $\mathbb{F}_2$ Ranks, and Ground-State Degeneracy

1. **Local Vertex Syzygy**: At every vertex $v$, each incident axis belongs to two of the three coordinate planes:
   $$\mathbf{p}_{xy} + \mathbf{p}_{yz} + \mathbf{p}_{zx} = (2, 2, 2) \equiv (0, 0, 0) \pmod 2 \implies A_v^{(xy)} A_v^{(yz)} A_v^{(zx)} = I.$$
   This gives $V$ local relations, leaving $2V$ locally independent vertex operators.
2. **Global Planar Subsystem Syzygies**:
   - On $\mathbb{T}^3(L_x, L_y, L_z)$ ($L_x, L_y, L_z \ge 2$), the product of $B_c$ over any dual layer $x = x_0$, $y = y_0$, or $z = z_0$ cancels every edge twice, with $2$ global redundancies among the $L_x + L_y + L_z$ layer products, giving $L_x + L_y + L_z - 2$ independent $X$-relations and
     $$\operatorname{rank}_{\mathbb{F}_2}(H_X) = V - (L_x + L_y + L_z - 2).$$
   - The product of $A_v^{(\mu\nu)}$ over each of the $L_x + L_y + L_z$ coordinate planes equals $I$, with $1$ global redundancy modulo the local vertex relations, giving $L_x + L_y + L_z - 1$ independent global $Z$-relations and
     $$\operatorname{rank}_{\mathbb{F}_2}(H_Z) = 2V - (L_x + L_y + L_z - 1).$$
3. **Logical Qubit Dimension and Ground-State Degeneracy**:
   $$k(L_x, L_y, L_z) = N_e - \big(\operatorname{rank}_{\mathbb{F}_2}(H_X) + \operatorname{rank}_{\mathbb{F}_2}(H_Z)\big) = 3V - \big(3V - (2L_x + 2L_y + 2L_z - 3)\big) = 2L_x + 2L_y + 2L_z - 3,$$
   and
   $$\text{GSD}(L_x, L_y, L_z) = 2^{k(L_x, L_y, L_z)} = 2^{2L_x + 2L_y + 2L_z - 3}.$$
   Exact $\mathbb{F}_2$ Gaussian elimination in `checks/independent/fsp-xcube-fracton-model.py` verifies $\operatorname{rank}_{\mathbb{F}_2}(H_X)$, $\operatorname{rank}_{\mathbb{F}_2}(H_Z)$, and $k(L_x, L_y, L_z)$ across all $27$ periodic cubic lattices $(L_x, L_y, L_z) \in \{2, 3, 4\}^3$ (e.g., $k = 9, \text{GSD} = 512$ at $L = 2$; $k = 15, \text{GSD} = 32768$ at $L = 3$; $k = 21, \text{GSD} = 2097152$ at $L = 4$).

---

## 3. Explicit Scope Fences

1. **6-Edge 3D Star Anti-Commutation (`six_edge_3d_star_anticommutes_with_cube_fence`)**:
   Replacing the 4-edge planar vertex cross $A_v^{(\mu\nu)}$ by the 6-edge 3D vertex star $A_v^{(xyz)}$ gives overlap $\mathbf{c}_v \cdot \mathbf{c}_v = 3 \equiv 1 \pmod 2$ at every corner of an adjacent cube, so the 6-edge $Z$-star and 12-edge $X$-cube anti-commute ($(-1)^3 = -1 \ne 1$).
2. **Bosonic CSS Stoquasticity (`xcube_css_bosonic_stoquasticity_fence`)**:
   The X-cube model is a bosonic qubit CSS stabilizer code with non-positive off-diagonal cube matrix entries ($-1 \le 0$) in the computational $Z$-basis, and carries no fermionic exchange sign consequence by itself.
3. **Non-Abelian Hinge Holonomy Negative Trace (`nonabelian_hinge_holonomy_negative_trace_fence`)**:
   While abelian X-cube stabilizers commute with positive trace $+2$, non-abelian $SU(2)_2$ 2-gauge defect sheets intersecting along a 1D hinge line have commutator holonomy $-I_2$ with negative trace $\operatorname{Tr}(-I_2) = -2 < 0$.

---

## 4. Verification Summary

- **Lean 4 Module**: [`lean4/CampaignFspXcubeFractonModel.lean`](../../../lean4/CampaignFspXcubeFractonModel.lean) — 10 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed.
- **Independent Python Check**: [`checks/independent/fsp-xcube-fracton-model.py`](../../../checks/independent/fsp-xcube-fracton-model.py) — `checks=74061 f2_css_lattices=74004 scaling_fences=57 failures=0`.
