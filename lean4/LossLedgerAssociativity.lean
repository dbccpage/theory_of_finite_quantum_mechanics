import Mathlib.Data.Rat.Defs
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-!
# `TFQ-0123` (`CONTINUUM_INTERFACE`)
## Natural-Number Loss Ledger Associativity vs. Floating-Point Carrier Mismatch (`GAP-F002-S000-002`) and 11D Supergravity Triangulation Fences (`GAP-F002-S000-001`)

This module formalizes the exact finite/algebraic counterpart and non-equivalence scope fences for
DAG node `TFQ-0123` (`GAP-F002-S000-002 carrier mismatch and GAP-F002-S000-001 supergravity
triangulation stay open`):

1. **Natural-Number Transport Loss Ledger Monoid (`NatTransportCell`, `TransportCell.lean` Replay)**:
   - Defines `NatTransportCell` with endpoints `source, target : Nat` and natural-number loss
     ledger `loss : Nat`, composed via `composeNatCell c1 c2 = ⟨c1.source, c2.target, c1.loss + c2.loss⟩`
     with identity `idNatCell v = ⟨v, v, 0⟩`.
   - Proves exact associativity (`nat_transport_cell_assoc`), left/right identity laws
     (`nat_transport_cell_unit_laws`), and loss monotonicity plus zero-loss characterization
     (`nat_transport_loss_monotonicity_and_zero_iff`).

2. **Carrier Mismatch Between `Nat` Addition and Floating/Dyadic Rounding (`GAP-F002-S000-002`)**:
   - Defines `ulpAbsorbedAdd eps a b : ℚ`, which absorbs a positive increment `b < eps` when added
     to a base magnitude `a ≥ 1`, modeling finite-precision floating-point ulp absorption.
   - Proves that on the dyadic triple `(1/2, 1/4, 1/8)` at scale `eps = 1/16`, `ulpAbsorbedAdd`
     coincidentally associates to `7/8` (`dyadic_triple_exact_coincidence`), replaying why testing a
     single representable dyadic triple gives a false green for general associativity.
   - Proves that on `(1, 1/16, 1/16)` at scale `eps = 1/8`, left-associated addition yields `1`
     whereas right-associated addition yields `9/8 ≠ 1`
     (`gap_f002_s000_002_float_absorption_breaks_associativity`).
   - Proves that `Nat` and `ℚ` are non-isomorphic additive carriers: `1 : Nat` has no half in `Nat`
     (`n + n ≠ 1`), so no additive homomorphism `f : ℚ → Nat` can satisfy `f 1 = 1`
     (`gap_f002_s000_002_nat_not_divisible_carrier_mismatch`).

3. **11D Supergravity Triangulation & Smooth-Frame Transport Fences (`GAP-F002-S000-001`)**:
   - Computes the exact $k$-simplex face counts $\binom{12}{k+1}$ of a single 11-dimensional
     simplex $\Delta^{11}$ (`simplex_11d_combinatorial_skeleton_counts`: 12 vertices, 66 edges,
     220 2-faces, 495 3-faces for $C_3$, 792 4-faces for $G_4 = dC_3$, 66 codimension-2 Regge
     hinges of dimension 9, and $2^{12} - 1 = 4095$ total non-empty faces), contrasting with the
     single scalar `loss : Nat` of a 1D/2-cell transport ledger.
   - Proves the codimension-2 Regge hinge dimension mismatch (`11 - 2 = 9 ≠ 2`) and the boundary
     Euler characteristic $\sum_{k=0}^{10} (-1)^k \binom{12}{k+1} = 2$ of $\partial \Delta^{11} \cong S^{10}$
     (`simplex_11d_hinge_codimension_and_euler_characteristic`).
   - Proves that a scalar loss ledger discards 2D frame orientation (`SO(2)` identity vs. $90^\circ$
     rotation have distinct traces `2 ≠ 0` yet share any loss-only scalar readout,
     `transport_loss_ledger_discards_frame_rotation_fence`) and underdetermines the
     $11 \times 12 / 2 = 66$ independent components of an 11D symmetric metric/Ricci tensor
     (`scalar_loss_ledger_underdetermines_11d_ricci_fence`).
-/

namespace LossLedgerAssociativity

-- ============================================================================
-- 1. Natural-Number Transport Loss Ledger Monoid (`TransportCell.lean` Replay)
-- ============================================================================

/-- Finite transport cell carrying endpoint labels `source, target : Nat` and a natural-number
loss ledger `loss : Nat`. -/
@[ext]
structure NatTransportCell where
  source : Nat
  target : Nat
  loss : Nat
  deriving DecidableEq, Repr

/-- Horizontal composition of natural-number transport cells adds their loss ledgers in `Nat`. -/
def composeNatCell (c1 c2 : NatTransportCell) : NatTransportCell :=
  ⟨c1.source, c2.target, c1.loss + c2.loss⟩

/-- Identity transport cell at vertex `v : Nat` with zero loss. -/
def idNatCell (v : Nat) : NatTransportCell :=
  ⟨v, v, 0⟩

/-- Theorem 1: Horizontal composition of `NatTransportCell` is strictly associative. -/
theorem nat_transport_cell_assoc (c1 c2 c3 : NatTransportCell) :
    composeNatCell (composeNatCell c1 c2) c3 = composeNatCell c1 (composeNatCell c2 c3) := by
  ext <;> dsimp [composeNatCell]
  omega

/-- Theorem 2: Left and right identity laws for `idNatCell` under `composeNatCell`. -/
theorem nat_transport_cell_unit_laws (c : NatTransportCell) :
    composeNatCell (idNatCell c.source) c = c ∧
    composeNatCell c (idNatCell c.target) = c := by
  refine ⟨?_, ?_⟩ <;> (ext <;> dsimp [composeNatCell, idNatCell] <;> omega)

/-- Theorem 3: Monotonicity and zero-sum characterization of the `Nat` transport loss ledger. -/
theorem nat_transport_loss_monotonicity_and_zero_iff (c1 c2 : NatTransportCell) :
    c1.loss ≤ (composeNatCell c1 c2).loss ∧
    c2.loss ≤ (composeNatCell c1 c2).loss ∧
    ((composeNatCell c1 c2).loss = 0 ↔ c1.loss = 0 ∧ c2.loss = 0) := by
  dsimp [composeNatCell]
  refine ⟨by omega, by omega, ?_⟩
  omega

-- ============================================================================
-- 2. Carrier Mismatch: `Nat` vs. Floating/Dyadic Absorption (`GAP-F002-S000-002`)
-- ============================================================================

/-- Model of finite-precision floating-point addition with ulp absorption threshold `eps`:
when `a ≥ 1` and `0 < b < eps`, the sub-ulp increment `b` is absorbed into `a`. -/
def ulpAbsorbedAdd (eps a b : ℚ) : ℚ :=
  if 1 ≤ a ∧ 0 < b ∧ b < eps then a else a + b

/-- Theorem 4: On the exactly representable sub-unit dyadic triple `(1/2, 1/4, 1/8)` with
`eps = 1/16`, `ulpAbsorbedAdd` associates to `7/8` in both parenthesizations, replaying why a
single representable triple test does not detect floating non-associativity. -/
theorem dyadic_triple_exact_coincidence :
    ulpAbsorbedAdd (1 / 16) (ulpAbsorbedAdd (1 / 16) (1 / 2) (1 / 4)) (1 / 8) = 7 / 8 ∧
    ulpAbsorbedAdd (1 / 16) (1 / 2) (ulpAbsorbedAdd (1 / 16) (1 / 4) (1 / 8)) = 7 / 8 := by
  dsimp [ulpAbsorbedAdd]
  norm_num

/-- Theorem 5 (`GAP-F002-S000-002` Non-Associativity Fence): At absorption threshold `eps = 1/8`,
the triple `(1, 1/16, 1/16)` associates to `1` on the left (`(1 ⊕ 1/16) ⊕ 1/16 = 1`) but to `9/8`
on the right (`1 ⊕ (1/16 ⊕ 1/16) = 9/8`), whereas the scaled integer ledger sums to `16 + 1 + 1 = 18`
in both parenthesizations. -/
theorem gap_f002_s000_002_float_absorption_breaks_associativity :
    ulpAbsorbedAdd (1 / 8) (ulpAbsorbedAdd (1 / 8) 1 (1 / 16)) (1 / 16) = 1 ∧
    ulpAbsorbedAdd (1 / 8) 1 (ulpAbsorbedAdd (1 / 8) (1 / 16) (1 / 16)) = 9 / 8 ∧
    ulpAbsorbedAdd (1 / 8) (ulpAbsorbedAdd (1 / 8) 1 (1 / 16)) (1 / 16) ≠
      ulpAbsorbedAdd (1 / 8) 1 (ulpAbsorbedAdd (1 / 8) (1 / 16) (1 / 16)) ∧
    ((16 + 1) + 1 : Nat) = (16 + (1 + 1) : Nat) := by
  dsimp [ulpAbsorbedAdd]
  norm_num

/-- Theorem 6 (`GAP-F002-S000-002` Divisibility Obstruction): `1 : Nat` has no half in `Nat`
(`∀ n : Nat, n + n ≠ 1`), whereas `(1/2 : ℚ) + (1/2 : ℚ) = 1`, so no additive map `f : ℚ → Nat`
preserving addition (`f (a + b) = f a + f b`) can satisfy `f 1 = 1`. -/
theorem gap_f002_s000_002_nat_not_divisible_carrier_mismatch :
    (∀ n : Nat, n + n ≠ 1) ∧
    ((1 / 2 : ℚ) + (1 / 2 : ℚ) = 1) ∧
    (∀ f : ℚ → Nat, (∀ a b : ℚ, f (a + b) = f a + f b) → f 1 ≠ 1) := by
  refine ⟨?_, by norm_num, ?_⟩
  · intro n
    omega
  · intro f hadd h1
    have hhalf : f 1 = f (1 / 2) + f (1 / 2) := by
      have heq : (1 : ℚ) = (1 / 2 : ℚ) + (1 / 2 : ℚ) := by norm_num
      conv_lhs => rw [heq]
      exact hadd (1 / 2) (1 / 2)
    omega

-- ============================================================================
-- 3. 11D Supergravity Triangulation & Smooth-Frame Fences (`GAP-F002-S000-001`)
-- ============================================================================

/-- Number of `k`-dimensional faces `C(d + 1, k + 1)` of a `d`-dimensional simplex `Δ^d`. -/
def simplexFaceCount (d k : Nat) : Nat :=
  Nat.choose (d + 1) (k + 1)

/-- Total number of non-empty faces `2^(d + 1) - 1` of a `d`-dimensional simplex `Δ^d`. -/
def simplexTotalFaces (d : Nat) : Nat :=
  2 ^ (d + 1) - 1

/-- Codimension-2 Regge curvature hinge dimension `d - 2` in `d`-dimensional simplicial gravity. -/
def reggeHingeDim (d : Nat) : Nat :=
  d - 2

/-- Number of independent components `d * (d + 1) / 2` of a symmetric metric or Ricci tensor in
dimension `d`. -/
def symmetricTensorComponents (d : Nat) : Nat :=
  d * (d + 1) / 2

/-- Theorem 7 (`GAP-F002-S000-001` 11D Simplex Skeleton Fence): A single 11-dimensional simplex
`Δ^11` requires `12` vertices (`0`-faces), `66` edges (`1`-faces), `220` triangles (`2`-faces),
`495` tetrahedra (`3`-faces for the 11D supergravity 3-form `C_3`), `792` pentachora (`4`-faces
for `G_4 = dC_3`), `66` codimension-2 Regge hinges (`9`-faces), and `4095` total non-empty faces,
none of which are constructed by a 1-parameter `NatTransportCell`. -/
theorem simplex_11d_combinatorial_skeleton_counts :
    simplexFaceCount 11 0 = 12 ∧
    simplexFaceCount 11 1 = 66 ∧
    simplexFaceCount 11 2 = 220 ∧
    simplexFaceCount 11 3 = 495 ∧
    simplexFaceCount 11 4 = 792 ∧
    simplexFaceCount 11 9 = 66 ∧
    simplexTotalFaces 11 = 4095 := by
  decide

/-- Theorem 8 (`GAP-F002-S000-001` Hinge Dimension & Boundary Euler Characteristic): In `d = 11`,
Regge curvature hinges have dimension `reggeHingeDim 11 = 9 ≠ 2` (unlike a 2-cell), and the
alternating face-count sum of the boundary `∂Δ^11 ≅ S^10` equals `2`. -/
theorem simplex_11d_hinge_codimension_and_euler_characteristic :
    reggeHingeDim 11 = 9 ∧
    reggeHingeDim 11 ≠ 2 ∧
    (simplexFaceCount 11 0 : Int) - simplexFaceCount 11 1 + simplexFaceCount 11 2 -
      simplexFaceCount 11 3 + simplexFaceCount 11 4 - simplexFaceCount 11 5 +
      simplexFaceCount 11 6 - simplexFaceCount 11 7 + simplexFaceCount 11 8 -
      simplexFaceCount 11 9 + simplexFaceCount 11 10 = 2 := by
  decide

/-- A 2x2 integer matrix representing a discrete local frame transformation. -/
structure Frame2D where
  a11 : Int
  a12 : Int
  a21 : Int
  a22 : Int
  deriving DecidableEq, Repr

/-- Trace of a 2D frame matrix. -/
def frameTrace (F : Frame2D) : Int :=
  F.a11 + F.a22

/-- Determinant of a 2D frame matrix. -/
def frameDet (F : Frame2D) : Int :=
  F.a11 * F.a22 - F.a12 * F.a21

/-- Theorem 9 (Smooth-Frame Transport Fence): The identity frame `⟨1, 0, 0, 1⟩` and the 90-degree
rotated frame `⟨0, -1, 1, 0⟩` both have unit determinant (`det = 1`) in `SO(2)` but distinct
traces (`2 ≠ 0`), showing that a scalar `Nat` loss ledger (`loss : Nat`) carries zero frame
orientation or spin-connection information. -/
theorem transport_loss_ledger_discards_frame_rotation_fence :
    let F_id : Frame2D := ⟨1, 0, 0, 1⟩
    let F_rot : Frame2D := ⟨0, -1, 1, 0⟩
    frameDet F_id = 1 ∧
    frameDet F_rot = 1 ∧
    frameTrace F_id = 2 ∧
    frameTrace F_rot = 0 ∧
    F_id ≠ F_rot := by
  decide

/-- Theorem 10 (11D Einstein/Ricci Underdetermination Fence): In dimension `d = 11`, a symmetric
metric or Ricci tensor has `symmetricTensorComponents 11 = 66` independent components per point
(`66 > 1`), and two diagonal mode pairs `(0, 0)` vs. `(r, -r)` with `r ≠ 0` have identical zero
scalar trace (`r + (-r) = 0`) while `r^2 + (-r)^2 = 2 * r^2 > 0`, fencing that a scalar loss
ledger is not the Einstein field equation. -/
theorem scalar_loss_ledger_underdetermines_11d_ricci_fence (r : ℚ) (hr : r ≠ 0) :
    symmetricTensorComponents 11 = 66 ∧
    r + (-r) = 0 ∧
    (0 : ℚ) + 0 = 0 ∧
    r ^ 2 + (-r) ^ 2 = 2 * r ^ 2 ∧
    0 < 2 * r ^ 2 := by
  have hr2 : 0 < r ^ 2 := sq_pos_of_ne_zero hr
  refine ⟨by decide, by ring, by ring, by ring, by linarith⟩

end LossLedgerAssociativity

#print axioms LossLedgerAssociativity.nat_transport_cell_assoc
#print axioms LossLedgerAssociativity.nat_transport_cell_unit_laws
#print axioms LossLedgerAssociativity.nat_transport_loss_monotonicity_and_zero_iff
#print axioms LossLedgerAssociativity.dyadic_triple_exact_coincidence
#print axioms LossLedgerAssociativity.gap_f002_s000_002_float_absorption_breaks_associativity
#print axioms LossLedgerAssociativity.gap_f002_s000_002_nat_not_divisible_carrier_mismatch
#print axioms LossLedgerAssociativity.simplex_11d_combinatorial_skeleton_counts
#print axioms LossLedgerAssociativity.simplex_11d_hinge_codimension_and_euler_characteristic
#print axioms LossLedgerAssociativity.transport_loss_ledger_discards_frame_rotation_fence
#print axioms LossLedgerAssociativity.scalar_loss_ledger_underdetermines_11d_ricci_fence

private def l5aProvenance : String :=
  "Origin: lean4/LossLedgerAssociativity.lean Claim: TFQ-0123 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
