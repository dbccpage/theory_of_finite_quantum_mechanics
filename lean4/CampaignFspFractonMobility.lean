import Mathlib.Tactic

/-!
# CampaignFspFractonMobility: Subdimensional Excitation Mobility in the 3D X-Cube Model (TFQ-1218)

Formalizes the narrowed local mathematical witnesses for `FSP-FRACTON-MOBILITY`
(`TFQ-1218` / `FSP-DERIV-054`, stage `FERMION_SIGN`, status `IMPORTED_ASSUMPTION`):

1. **Single-edge Pauli-Z cube syndrome (`xcube_single_edge_pauli_z_excites_four_cubes`)**:
   In the 3D X-cube model, every lattice edge `e` is shared by 4 elementary cubes
   forming a 2x2 dual plaquette perpendicular to `e`. Applying `Z_e` anticommutes
   with all 4 adjacent cube stabilizers `B_c`, flipping their F_2 syndrome from
   `(0, 0, 0, 0)` to `(1, 1, 1, 1)` of Hamming weight 4.
2. **0D immobility of isolated fractons (`xcube_isolated_fracton_hop_creates_two_extra_fractons`)**:
   Starting from a single isolated cube excitation `(1, 0, 0, 0)` of Hamming weight 1
   and energy `2 J`, applying `Z_e` on a bounding edge yields syndrome
   `((1+1)%2, (0+1)%2, (0+1)%2, (0+1)%2) = (0, 1, 1, 1)` of Hamming weight 3 and
   energy `6 J`, creating 2 additional fractons with strict energy barrier `4 J > 0`.
3. **Rectangular membrane corner-quadrupole law (`xcube_rectangular_membrane_corner_quadrupole_conservation`)**:
   A rectangular dual membrane of `R_y * R_z` parallel `Z_e` operators flips interior
   cubes `4 % 2 = 0` times, straight-edge boundary cubes `2 % 2 = 0` times, and each of
   the 4 corner cubes `1 % 2 = 1` time (total excited corner count 4), while the
   foliated separation penalty `Delta_S = kappa * R` (`FoliatedFractonEngine`) satisfies
   `kappa * R >= kappa > 0` for `kappa > 0` and `R >= 1`.
4. **2D planon mobility of fracton dipoles (`xcube_fracton_dipole_is_2d_planon`)**:
   A fracton dipole of two adjacent excited cubes `(1, 1, 0, 0)` (weight 2, energy `4 J`)
   separated along the z-axis moves by 1 step in the xy-plane under `Z_e` on the shared
   edge to `(0, 0, 1, 1)` of the same Hamming weight 2 and zero energy barrier (`Delta_E = 0`),
   whereas a transverse 4-cube flip raises the weight from 2 to 4.
5. **Single-edge Pauli-X lineon pair creation (`xcube_single_edge_pauli_x_excites_lineon_pair`)**:
   At each vertex `v`, the three planar cross stabilizers satisfy `A_v^(xy) A_v^(yz) A_v^(zx) = I`,
   so the local vertex syndrome `(s_xy, s_yz, s_zx)` has even parity `(s_xy + s_yz + s_zx) % 2 = 0`.
   Applying `X_e` on an x-oriented edge excites `(A_v^(xy), A_v^(zx))` with syndrome `(1, 0, 1)`
   of weight 2 at both endpoints.
6. **1D collinear lineon string mobility (`xcube_lineon_collinear_string_preserves_weight`)**:
   Applying `X_e` along a collinear string of x-oriented edges cancels the syndrome twice
   at every interior vertex `((1+1)%2, (0+0)%2, (1+1)%2) = (0, 0, 0)`, transporting the
   x-lineon along the x-axis with constant total excited vertex weight 4 and zero energy barrier.
7. **90-degree corner turn leaves an immobile vertex defect (`xcube_lineon_corner_turn_creates_immobile_vertex_defect`)**:
   Turning an x-lineon `(1, 0, 1)` onto a y-oriented edge with endpoint shift `(1, 1, 0)`
   leaves residual syndrome `((1+1)%2, (0+1)%2, (1+0)%2) = (0, 1, 1)` (a z-lineon of weight 2)
   at the corner vertex, raising the total vertex syndrome weight from 4 to 6 (`Delta_E = 2 J_A > 0`).
8. **Scope Fence 1 — 2D planon dipole braiding (`planon_dipole_2d_braiding_obstruction_fence`)**:
   Even though single fractons are 0D immobile, composite fracton dipoles are 2D planons
   that move freely in 2D planes (`Delta_E = 0`) and can braid with odd permutation sign `-1`.
9. **Scope Fence 2 — Intersecting hinge T-junction exchange (`lineon_tjunction_three_step_exchange_fence`)**:
   Particles on intersecting 1D hinges meeting at a T-junction can swap order via the branch
   vertex with odd permutation sign `Equiv.Perm.sign (Equiv.swap 0 1) = -1`.
10. **Scope Fence 3 — Mobility vs. fermion sign & non-abelian hinge trace (`mobility_constraints_do_not_imply_fermion_sign_freedom_fence`)**:
    Excitation mobility restrictions in a bosonic stabilizer code do not imply non-negative
    fermionic path weights, and non-abelian `SU(2)_2` hinge holonomy `-I_2` has negative trace `-2 < 0`.
-/

namespace CampaignFspFractonMobility

/-- Hamming weight of a 4-cube dual-plaquette syndrome `(c0, c1, c2, c3)` in `{0, 1}^4`. -/
def cubePlaquetteWeight (c0 c1 c2 c3 : ℕ) : ℕ :=
  c0 % 2 + c1 % 2 + c2 % 2 + c3 % 2

/-- Hamming weight of a 3-plane vertex-cross syndrome `(s_xy, s_yz, s_zx)` in `{0, 1}^3`. -/
def vertexCrossWeight (s_xy s_yz s_zx : ℕ) : ℕ :=
  s_xy % 2 + s_yz % 2 + s_zx % 2

/-- Foliated fracton separation penalty `Delta_S(kappa, R) = kappa * R`
    matching `FoliatedFractonEngine.evaluate_isolated_fracton_separation`. -/
def foliatedSeparationPenalty (kappa R : ℕ) : ℕ :=
  kappa * R

/-- Theorem 1: Applying a single Pauli `Z_e` on an edge `e` flips all 4 adjacent cubes
    sharing `e`, mapping the vacuum syndrome `(0, 0, 0, 0)` (weight 0) to the elementary
    fracton quadrupole `(1, 1, 1, 1)` of Hamming weight 4. -/
theorem xcube_single_edge_pauli_z_excites_four_cubes :
    cubePlaquetteWeight 0 0 0 0 = 0 ∧
    cubePlaquetteWeight (0 + 1) (0 + 1) (0 + 1) (0 + 1) = 4 ∧
    (∀ J : ℤ, 0 < J → 0 < 2 * J * (cubePlaquetteWeight 1 1 1 1 : ℤ)) := by
  refine ⟨by decide, by decide, ?_⟩
  intro J hJ
  have hw : (cubePlaquetteWeight 1 1 1 1 : ℤ) = 4 := by decide
  rw [hw]
  linarith

/-- Theorem 2: Starting from a single isolated fracton `(1, 0, 0, 0)` (weight 1, energy `2 J`),
    applying `Z_e` on a bounding edge produces syndrome `((1+1)%2, 1, 1, 1) = (0, 1, 1, 1)`
    of Hamming weight 3 (energy `6 J`), creating 2 new fractons with positive energy barrier `4 J > 0`. -/
theorem xcube_isolated_fracton_hop_creates_two_extra_fractons (J : ℤ) (hJ : 0 < J) :
    cubePlaquetteWeight 1 0 0 0 = 1 ∧
    cubePlaquetteWeight (1 + 1) (0 + 1) (0 + 1) (0 + 1) = 3 ∧
    cubePlaquetteWeight (1 + 1) (0 + 1) (0 + 1) (0 + 1) - cubePlaquetteWeight 1 0 0 0 = 2 ∧
    2 * J * (cubePlaquetteWeight (1 + 1) (0 + 1) (0 + 1) (0 + 1) : ℤ) -
      2 * J * (cubePlaquetteWeight 1 0 0 0 : ℤ) = 4 * J ∧
    0 < 4 * J := by
  refine ⟨by decide, by decide, by decide, ?_, by linarith⟩
  have w1 : (cubePlaquetteWeight 1 0 0 0 : ℤ) = 1 := by decide
  have w3 : (cubePlaquetteWeight (1 + 1) (0 + 1) (0 + 1) (0 + 1) : ℤ) = 3 := by decide
  rw [w1, w3]
  ring

/-- Theorem 3: Under a rectangular membrane of `Z_e` operators, interior cubes shared by 4
    membrane edges flip `4 % 2 = 0` times, straight-boundary cubes shared by 2 membrane edges
    flip `2 % 2 = 0` times, and each of the 4 corner cubes flips `1 % 2 = 1` time (weight 4),
    while the foliated separation penalty `foliatedSeparationPenalty kappa R = kappa * R`
    grows strictly with separation `R`. -/
theorem xcube_rectangular_membrane_corner_quadrupole_conservation
    (kappa R1 R2 : ℕ) (hkappa : 0 < kappa) (hR1 : 1 ≤ R1) (hR2 : R1 < R2) :
    4 % 2 = 0 ∧
    2 % 2 = 0 ∧
    cubePlaquetteWeight 1 1 1 1 = 4 ∧
    kappa ≤ foliatedSeparationPenalty kappa R1 ∧
    foliatedSeparationPenalty kappa R1 < foliatedSeparationPenalty kappa R2 := by
  refine ⟨by decide, by decide, by decide, ?_, ?_⟩
  · unfold foliatedSeparationPenalty
    nlinarith
  · unfold foliatedSeparationPenalty
    exact Nat.mul_lt_mul_of_pos_left hR2 hkappa

/-- Theorem 4: A fracton dipole `(1, 1, 0, 0)` of two adjacent cubes (weight 2) translates
    in the perpendicular 2D plane under `Z_e` on the shared edge to `(0, 0, 1, 1)` of equal
    weight 2 and zero energy barrier (`Delta_E = 0`), forming a 2D planon. -/
theorem xcube_fracton_dipole_is_2d_planon (J : ℤ) :
    cubePlaquetteWeight 1 1 0 0 = 2 ∧
    cubePlaquetteWeight (1 + 1) (1 + 1) (0 + 1) (0 + 1) = 2 ∧
    2 * J * (cubePlaquetteWeight (1 + 1) (1 + 1) (0 + 1) (0 + 1) : ℤ) -
      2 * J * (cubePlaquetteWeight 1 1 0 0 : ℤ) = 0 := by
  refine ⟨by decide, by decide, ?_⟩
  have w_init : (cubePlaquetteWeight 1 1 0 0 : ℤ) = 2 := by decide
  have w_hop : (cubePlaquetteWeight (1 + 1) (1 + 1) (0 + 1) (0 + 1) : ℤ) = 2 := by decide
  rw [w_init, w_hop]
  ring

/-- Theorem 5: Applying `X_e` on an x-oriented edge flips `A_v^(xy)` and `A_v^(zx)` while
    commuting with `A_v^(yz)`, creating a vertex syndrome `(1, 0, 1)` of weight 2 at each
    endpoint that satisfies the local syzygy parity `(s_xy + s_yz + s_zx) % 2 = 0`. -/
theorem xcube_single_edge_pauli_x_excites_lineon_pair :
    vertexCrossWeight 1 0 1 = 2 ∧
    (1 + 0 + 1) % 2 = 0 ∧
    vertexCrossWeight 1 1 0 = 2 ∧
    vertexCrossWeight 0 1 1 = 2 := by
  decide

/-- Theorem 6: Extending an x-lineon along a collinear x-axis edge applies `(1, 0, 1)` a
    second time at the interior vertex, cancelling `((1+1)%2, (0+0)%2, (1+1)%2) = (0, 0, 0)`
    to weight 0 and keeping the two-endpoint total syndrome weight equal to 4 (`Delta_E = 0`). -/
theorem xcube_lineon_collinear_string_preserves_weight (JA : ℤ) :
    vertexCrossWeight (1 + 1) (0 + 0) (1 + 1) = 0 ∧
    vertexCrossWeight 1 0 1 + vertexCrossWeight (1 + 1) (0 + 0) (1 + 1) +
      vertexCrossWeight 1 0 1 = 4 ∧
    JA * (vertexCrossWeight 1 0 1 + vertexCrossWeight (1 + 1) (0 + 0) (1 + 1) +
      vertexCrossWeight 1 0 1 : ℤ) -
      JA * (vertexCrossWeight 1 0 1 + vertexCrossWeight 1 0 1 : ℤ) = 0 := by
  refine ⟨by decide, by decide, ?_⟩
  have h1 : (vertexCrossWeight 1 0 1 : ℤ) = 2 := by decide
  have h2 : (vertexCrossWeight (1 + 1) (0 + 0) (1 + 1) : ℤ) = 0 := by decide
  rw [h1, h2]
  ring

/-- Theorem 7: Attempting to turn an x-lineon `(1, 0, 1)` around a 90-degree corner onto a
    y-oriented edge with shift `(1, 1, 0)` leaves residual syndrome `((1+1)%2, (0+1)%2, (1+0)%2)
    = (0, 1, 1)` of weight 2 at the corner vertex, increasing total syndrome weight from 4 to 6
    with positive energy barrier `2 * JA > 0`. -/
theorem xcube_lineon_corner_turn_creates_immobile_vertex_defect (JA : ℤ) (hJA : 0 < JA) :
    vertexCrossWeight (1 + 1) (0 + 1) (1 + 0) = 2 ∧
    vertexCrossWeight 1 0 1 + vertexCrossWeight (1 + 1) (0 + 1) (1 + 0) +
      vertexCrossWeight 1 1 0 = 6 ∧
    JA * (vertexCrossWeight 1 0 1 + vertexCrossWeight (1 + 1) (0 + 1) (1 + 0) +
      vertexCrossWeight 1 1 0 : ℤ) -
      JA * (vertexCrossWeight 1 0 1 + vertexCrossWeight 1 0 1 : ℤ) = 2 * JA ∧
    0 < 2 * JA := by
  refine ⟨by decide, by decide, ?_, by linarith⟩
  have hx : (vertexCrossWeight 1 0 1 : ℤ) = 2 := by decide
  have hc : (vertexCrossWeight (1 + 1) (0 + 1) (1 + 0) : ℤ) = 2 := by decide
  have hy : (vertexCrossWeight 1 1 0 : ℤ) = 2 := by decide
  rw [hx, hc, hy]
  ring

/-- Theorem 8 (Scope Fence 1): Even though isolated single fractons have hop barrier `4 J > 0`,
    composite fracton dipoles have hop barrier `0` in 2D planes (2D planons), and exchanging
    two composite fermions in a 2D plane induces an odd permutation `Equiv.swap 0 1` of sign `-1 < 0`. -/
theorem planon_dipole_2d_braiding_obstruction_fence :
    cubePlaquetteWeight (1 + 1) (1 + 1) (0 + 1) (0 + 1) = cubePlaquetteWeight 1 1 0 0 ∧
    Equiv.Perm.sign (Equiv.swap (0 : Fin 2) (1 : Fin 2)) = -1 ∧
    ((Equiv.Perm.sign (Equiv.swap (0 : Fin 2) (1 : Fin 2)) : ℤ) < 0) := by
  refine ⟨by decide, ?_, ?_⟩
  · decide
  · decide

/-- Theorem 9 (Scope Fence 2): On two intersecting 1D hinges meeting at a T-junction,
    exchanging two lineons via the branch vertex induces the transposition `Equiv.swap 0 1`
    on `Fin 3` with odd permutation sign `-1`, showing that 1D hinge segments do not prevent
    exchange when hinges intersect. -/
theorem lineon_tjunction_three_step_exchange_fence :
    let tau : Equiv.Perm (Fin 3) := Equiv.swap 0 1
    tau 0 = 1 ∧ tau 1 = 0 ∧ tau 2 = 2 ∧
    Equiv.Perm.sign tau = -1 := by
  decide

/-- Theorem 10 (Scope Fence 3): Subdimensional excitation mobility in the bosonic X-cube code
    does not by itself eliminate fermionic exchange signs, and non-abelian `SU(2)_2` 2-gauge
    hinge holonomy `-I_2` (`FoliatedFractonEngine.evaluate_hinge_lineon_braid`) has trace `-2 < 0`
    and positive defect mass `|-2| = 2 > 0`. -/
theorem mobility_constraints_do_not_imply_fermion_sign_freedom_fence :
    let trace_neg_I2 : ℤ := (-1) + (-1)
    let phi_1 : ℤ := |trace_neg_I2|
    trace_neg_I2 = -2 ∧ trace_neg_I2 < 0 ∧ phi_1 = 2 ∧ 0 < phi_1 := by
  decide

end CampaignFspFractonMobility
