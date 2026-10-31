


import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

namespace FoliatedFracton2Gauge

inductive FoliationPlane : Type where
  | xy : FoliationPlane
  | yz : FoliationPlane
  | zx : FoliationPlane
deriving DecidableEq, Repr

inductive Mobility : Type where
  | fracton : Mobility
  | lineon  : Mobility
  | planon  : Mobility
deriving DecidableEq, Repr

theorem planon_dipole_neutrality (q : Int) :
    q + (-q) = 0 := by
  omega

theorem planon_dipole_defect_nullification (w : Int) :
    w * 1 + w * (-1) = 0 := by
  omega

theorem subsystem_extensive_gap_positive (kappa : Nat) (R : Nat) (h_k : kappa > 0) (h_R : R > 0) :
    kappa * R > 0 := by
  exact Nat.mul_pos h_k h_R

theorem extensive_gap_separates_weights (w_plus w_minus : Int) (gap : Nat) (h_gap : gap > 0) (h_sep : w_plus - w_minus ≥ (gap : Int)) :
    w_plus ≠ w_minus := by
  omega

/-- Scalar indicator model for 2×2 commuting (`false`, trace `+2`) vs anticommuting Pauli (`true`,
    `A B = -B A`, trace `-2`) hinge holonomy. For the general 2×2 matrix identity over `ℚ(i)` and the
    non-commuting `SU(2)` counterexample with positive trace `14/25`, see
    `anticommuting_mat2x2_commutator_trace_neg_two` and
    `noncommuting_su2_positive_commutator_trace_counterexample`. -/
def hingeCommutatorTrace (is_anticommuting_pauli : Bool) : Int :=
  if is_anticommuting_pauli then -2 else 2

theorem abelian_hinge_trace_positive :
    hingeCommutatorTrace false = 2 := by
  rfl

theorem nonabelian_hinge_trace_negative :
    hingeCommutatorTrace true = -2 := by
  rfl

def fractonDefectMass (tr : Int) : Nat :=
  if tr ≥ 0 then 0 else 2

theorem abelian_hinge_defect_mass_zero :
    fractonDefectMass (hingeCommutatorTrace false) = 0 := by
  rfl

theorem nonabelian_hinge_defect_mass_two :
    fractonDefectMass (hingeCommutatorTrace true) = 2 := by
  rfl

def foliatedProjectedTrace (has_corner_lineon : Bool) (base_tr : Int) : Int :=
  if has_corner_lineon then base_tr else (base_tr.natAbs * base_tr.natAbs : Nat)

theorem decoupled_foliated_projection_nonnegative (tr : Int) :
    0 ≤ foliatedProjectedTrace false tr := by
  dsimp [foliatedProjectedTrace]
  exact Int.natCast_nonneg _

theorem corner_lineon_obstruction_persists (h : hingeCommutatorTrace true = -2) :
    foliatedProjectedTrace true (hingeCommutatorTrace true) < 0 := by
  rw [h]
  decide

/-- 1D discrete coordinate position on a hinge line. -/
structure Lineon1D where
  coord : Int
  deriving DecidableEq, Repr

/-- Configuration of two lineons on a discrete 1D hinge. -/
structure TwoLineonConfig where
  pos1 : Int
  pos2 : Int
  ordered : pos1 < pos2
  deriving DecidableEq, Repr

/-- Elementary hop on 1D hinge with collision avoidance. -/
inductive DiscreteHop1D : TwoLineonConfig → TwoLineonConfig → Type where
  | hop1_left  (c : TwoLineonConfig) (h : c.pos1 - 1 < c.pos2) :
      DiscreteHop1D c ⟨c.pos1 - 1, c.pos2, h⟩
  | hop1_right (c : TwoLineonConfig) (h : c.pos1 + 1 < c.pos2) :
      DiscreteHop1D c ⟨c.pos1 + 1, c.pos2, h⟩
  | hop2_left  (c : TwoLineonConfig) (h : c.pos1 < c.pos2 - 1) :
      DiscreteHop1D c ⟨c.pos1, c.pos2 - 1, h⟩
  | hop2_right (c : TwoLineonConfig) (h : c.pos1 < c.pos2 + 1) :
      DiscreteHop1D c ⟨c.pos1, c.pos2 + 1, h⟩

/-- Transitive closure of discrete collision-free hops on 1D hinge line. -/
inductive HingePath : TwoLineonConfig → TwoLineonConfig → Prop where
  | refl (c : TwoLineonConfig) : HingePath c c
  | step {c1 c2 c3 : TwoLineonConfig} (h12 : HingePath c1 c2) (hop : DiscreteHop1D c2 c3) :
      HingePath c1 c3

/-- Theorem 1: Collision-free 1D hinge paths strictly preserve relative order. -/
theorem hinge_path_preserves_relative_order {c_init c_final : TwoLineonConfig}
    (path : HingePath c_init c_final) :
    c_final.pos1 < c_final.pos2 := by
  induction path with
  | refl => exact c_init.ordered
  | step _ hop _ =>
    cases hop <;> assumption

/-- Two lineons on a collision-free hinge path cannot exchange positions. -/
theorem hinge_path_exchange_impossible {c_init c_final : TwoLineonConfig}
    (path : HingePath c_init c_final)
    (h_swap : c_final.pos1 = c_init.pos2 ∧ c_final.pos2 = c_init.pos1) :
    False := by
  have h_ord := hinge_path_preserves_relative_order path
  rcases h_swap with ⟨h1, h2⟩
  have h_init := c_init.ordered
  rw [h1, h2] at h_ord
  omega

/-- Discrete Intermediate Value Theorem: integer step trajectory crossing zero. -/
theorem discrete_ivt_zero (f : Nat → Int) (N : Nat)
    (h_start : f 0 < 0) (h_end : f N > 0)
    (h_step : ∀ t < N, f (t + 1) ≤ f t + 1) :
    ∃ t ≤ N, f t = 0 := by
  induction N with
  | zero =>
    omega
  | succ n ih =>
    by_cases h_eq : f n = 0
    · exact ⟨n, by omega, h_eq⟩
    · by_cases h_pos : f n > 0
      · have h_step_n : ∀ t < n, f (t + 1) ≤ f t + 1 := fun t ht => h_step t (by omega)
        obtain ⟨t, ht_le, ht_zero⟩ := ih h_pos h_step_n
        exact ⟨t, by omega, ht_zero⟩
      · have h_neg : f n < 0 := by omega
        have h_bound : f (n + 1) ≤ f n + 1 := h_step n (by omega)
        omega

/-- Theorem 2: Exchange obstruction on 1D hinge line.
    Two lineons on a 1D hinge cannot exchange without passing through an identical site. -/
theorem hinge_lineon_exchange_collision_obstruction
    (p1 p2 : Int) (h_init : p1 < p2)
    (path_pos1 path_pos2 : Nat → Int)
    (h_start1 : path_pos1 0 = p1) (h_start2 : path_pos2 0 = p2)
    (steps : Nat)
    (h_end1 : path_pos1 steps = p2) (h_end2 : path_pos2 steps = p1)
    (h_step : ∀ t < steps, path_pos1 (t + 1) - path_pos2 (t + 1) ≤ (path_pos1 t - path_pos2 t) + 1) :
    ∃ t ≤ steps, path_pos1 t = path_pos2 t := by
  let f : Nat → Int := fun t => path_pos1 t - path_pos2 t
  have h_start : f 0 < 0 := by
    dsimp [f]
    rw [h_start1, h_start2]
    omega
  have h_end : f steps > 0 := by
    dsimp [f]
    rw [h_end1, h_end2]
    omega
  have h_step_f : ∀ t < steps, f (t + 1) ≤ f t + 1 := by
    intro t ht
    exact h_step t ht
  obtain ⟨t, ht_le, ht_zero⟩ := discrete_ivt_zero f steps h_start h_end h_step_f
  exact ⟨t, ht_le, by dsimp [f] at ht_zero; omega⟩

/-- Theorem 3: Permutation parity on non-intersecting hinge lines is trivial. -/
theorem hinge_lineon_worldline_permutation_sign_trivial
    (ordered : Bool) (h_ordered : ordered = true) :
    (if ordered then (1 : Int) else (-1 : Int)) = 1 := by
  rw [h_ordered]
  rfl

/-- Theorem 4: Intersecting non-abelian hinge commutator yields uncancelled negative trace. -/
theorem nonabelian_hinge_commutator_curvature_obstruction :
    hingeCommutatorTrace true = -2 ∧
    fractonDefectMass (hingeCommutatorTrace true) = 2 ∧
    foliatedProjectedTrace true (hingeCommutatorTrace true) < 0 := by
  refine ⟨rfl, rfl, ?_⟩
  dsimp [foliatedProjectedTrace, hingeCommutatorTrace]
  decide

/-- Theorem 5: Decoupled foliated projection restores exact non-negative trace. -/
theorem decoupled_foliated_lineon_sign_free (tr : Int) :
    0 ≤ foliatedProjectedTrace false tr := by
  dsimp [foliatedProjectedTrace]
  exact Int.natCast_nonneg _

/-- 3-prong multi-hinge Y-junction vertex where three 1D hinge axes (X, Y, Z) meet at a corner. -/
inductive YJunctionVertex : Type where
  | center  : YJunctionVertex
  | branchX : YJunctionVertex
  | branchY : YJunctionVertex
  | branchZ : YJunctionVertex
  deriving DecidableEq, Repr

/-- Undirected adjacency on the 3-prong multi-hinge Y-junction graph. -/
def yJunctionAdj : YJunctionVertex → YJunctionVertex → Bool
  | .center, .branchX => true
  | .branchX, .center => true
  | .center, .branchY => true
  | .branchY, .center => true
  | .center, .branchZ => true
  | .branchZ, .center => true
  | _, _ => false

/-- Collision-free two-particle configuration on a multi-hinge Y-junction. -/
structure TwoParticleYJunctionConfig where
  v1 : YJunctionVertex
  v2 : YJunctionVertex
  distinct : v1 ≠ v2
  deriving DecidableEq, Repr

/-- Elementary collision-free single-particle hop on a multi-hinge Y-junction. -/
inductive YJunctionHop : TwoParticleYJunctionConfig → TwoParticleYJunctionConfig → Type where
  | hop1 (c : TwoParticleYJunctionConfig) (v1' : YJunctionVertex)
      (h_adj : yJunctionAdj c.v1 v1' = true) (h_dist : v1' ≠ c.v2) :
      YJunctionHop c ⟨v1', c.v2, h_dist⟩
  | hop2 (c : TwoParticleYJunctionConfig) (v2' : YJunctionVertex)
      (h_adj : yJunctionAdj c.v2 v2' = true) (h_dist : c.v1 ≠ v2') :
      YJunctionHop c ⟨c.v1, v2', h_dist⟩

/-- Reflexive-transitive closure of collision-free hops on the multi-hinge Y-junction. -/
inductive YJunctionPath : TwoParticleYJunctionConfig → TwoParticleYJunctionConfig → Prop where
  | refl (c : TwoParticleYJunctionConfig) : YJunctionPath c c
  | step {c1 c2 c3 : TwoParticleYJunctionConfig}
      (h12 : YJunctionPath c1 c2) (hop : YJunctionHop c2 c3) :
      YJunctionPath c1 c3

def yConfigXY : TwoParticleYJunctionConfig := ⟨.branchX, .branchY, by decide⟩
def yConfig0Y : TwoParticleYJunctionConfig := ⟨.center, .branchY, by decide⟩
def yConfigZY : TwoParticleYJunctionConfig := ⟨.branchZ, .branchY, by decide⟩
def yConfigZ0 : TwoParticleYJunctionConfig := ⟨.branchZ, .center, by decide⟩
def yConfigZX : TwoParticleYJunctionConfig := ⟨.branchZ, .branchX, by decide⟩
def yConfig0X : TwoParticleYJunctionConfig := ⟨.center, .branchX, by decide⟩
def yConfigYX : TwoParticleYJunctionConfig := ⟨.branchY, .branchX, by decide⟩

/-- Theorem 6: On a 3-prong multi-hinge Y-junction where corner branch-hopping is permitted,
    two particles starting at `(branchX, branchY)` admit an explicit 6-step collision-free
    exchange trajectory to `(branchY, branchX)` via the third hinge branch `branchZ`. -/
theorem y_junction_collision_free_exchange_exists :
    YJunctionPath yConfigXY yConfigYX ∧
    yConfigYX.v1 = yConfigXY.v2 ∧
    yConfigYX.v2 = yConfigXY.v1 := by
  refine ⟨?_, rfl, rfl⟩
  have s0 : YJunctionPath yConfigXY yConfigXY := YJunctionPath.refl yConfigXY
  have s1 : YJunctionPath yConfigXY yConfig0Y :=
    YJunctionPath.step s0 (YJunctionHop.hop1 yConfigXY .center rfl (by decide))
  have s2 : YJunctionPath yConfigXY yConfigZY :=
    YJunctionPath.step s1 (YJunctionHop.hop1 yConfig0Y .branchZ rfl (by decide))
  have s3 : YJunctionPath yConfigXY yConfigZ0 :=
    YJunctionPath.step s2 (YJunctionHop.hop2 yConfigZY .center rfl (by decide))
  have s4 : YJunctionPath yConfigXY yConfigZX :=
    YJunctionPath.step s3 (YJunctionHop.hop2 yConfigZ0 .branchX rfl (by decide))
  have s5 : YJunctionPath yConfigXY yConfig0X :=
    YJunctionPath.step s4 (YJunctionHop.hop1 yConfigZX .center rfl (by decide))
  exact YJunctionPath.step s5 (YJunctionHop.hop1 yConfig0X .branchY rfl (by decide))

/-- Worldline exchange permutation sign on a two-particle Y-junction trajectory (`-1` if exchanged, `+1` otherwise). -/
def yJunctionExchangeSign (c_init c_final : TwoParticleYJunctionConfig) : Int :=
  if c_final.v1 = c_init.v2 ∧ c_final.v2 = c_init.v1 then -1 else 1

/-- Theorem 7: Unconstrained multi-hinge Y-junction exchange induces a negative worldline
    permutation sign (`-1 < 0`), and when combined with abelian (`+2`) or non-abelian (`-2`)
    hinge commutator holonomy yields non-trivial signed amplitudes (`-2` vs `+2`). -/
theorem y_junction_exchange_induces_negative_sign :
    yJunctionExchangeSign yConfigXY yConfigYX = -1 ∧
    yJunctionExchangeSign yConfigXY yConfigXY = 1 ∧
    yJunctionExchangeSign yConfigXY yConfigYX * hingeCommutatorTrace false = -2 ∧
    yJunctionExchangeSign yConfigXY yConfigYX * hingeCommutatorTrace true = 2 ∧
    yJunctionExchangeSign yConfigXY yConfigXY * hingeCommutatorTrace true = -2 := by
  decide

/-- Two-lineon state with conserved 1D hinge-axis sector labels `(axis1, axis2)`. -/
structure AxisConservedTwoLineonState where
  axis1 : FoliationPlane
  axis2 : FoliationPlane
  coord1 : Int
  coord2 : Int
  deriving DecidableEq, Repr

/-- Hinge-sector-conserving transition: lineons hop only along their own 1D hinge axis. -/
inductive AxisConservingPath : AxisConservedTwoLineonState → AxisConservedTwoLineonState → Prop where
  | refl (s : AxisConservedTwoLineonState) : AxisConservingPath s s
  | step {s1 s2 s3 : AxisConservedTwoLineonState}
      (h12 : AxisConservingPath s1 s2)
      (h_ax1 : s3.axis1 = s2.axis1)
      (h_ax2 : s3.axis2 = s2.axis2) :
      AxisConservingPath s1 s3

theorem axis_conserving_path_preserves_axes {s_init s_final : AxisConservedTwoLineonState}
    (path : AxisConservingPath s_init s_final) :
    s_final.axis1 = s_init.axis1 ∧ s_final.axis2 = s_init.axis2 := by
  induction path with
  | refl => exact ⟨rfl, rfl⟩
  | step _ h_ax1 h_ax2 ih =>
    exact ⟨Eq.trans h_ax1 ih.1, Eq.trans h_ax2 ih.2⟩

/-- Theorem 8: Strict foliated dipole conservation preserves each lineon's 1D hinge sector,
    forbidding cross-branch Y-junction exchange between distinct hinge axes (`axis1 ≠ axis2`). -/
theorem foliated_lineon_axis_conservation_forbids_branch_exchange
    {s_init s_final : AxisConservedTwoLineonState}
    (h_distinct : s_init.axis1 ≠ s_init.axis2)
    (path : AxisConservingPath s_init s_final)
    (h_swap : s_final.axis1 = s_init.axis2 ∧ s_final.axis2 = s_init.axis1) :
    False := by
  have h_pres := axis_conserving_path_preserves_axes path
  exact h_distinct (Eq.trans h_pres.1.symm h_swap.1)

/-- Gaussian rationals `ℚ(i)` for exact 2×2 gauge holonomy matrices. -/
@[ext]
structure GaussRat where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Repr

namespace GaussRat

def zero : GaussRat := ⟨0, 0⟩
def one : GaussRat := ⟨1, 0⟩
def iUnit : GaussRat := ⟨0, 1⟩
def negIUnit : GaussRat := ⟨0, -1⟩

def add (z w : GaussRat) : GaussRat := ⟨z.re + w.re, z.im + w.im⟩
def sub (z w : GaussRat) : GaussRat := ⟨z.re - w.re, z.im - w.im⟩
def neg (z : GaussRat) : GaussRat := ⟨-z.re, -z.im⟩
def mul (z w : GaussRat) : GaussRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

end GaussRat

/-- Exact 2×2 matrix over `ℚ(i)`. -/
@[ext]
structure Mat2x2Q where
  m00 : GaussRat
  m01 : GaussRat
  m10 : GaussRat
  m11 : GaussRat
  deriving DecidableEq, Repr

namespace Mat2x2Q

def identity : Mat2x2Q :=
  ⟨GaussRat.one, GaussRat.zero, GaussRat.zero, GaussRat.one⟩

def negIdentity : Mat2x2Q :=
  ⟨⟨-1, 0⟩, GaussRat.zero, GaussRat.zero, ⟨-1, 0⟩⟩

def neg (A : Mat2x2Q) : Mat2x2Q :=
  ⟨GaussRat.neg A.m00, GaussRat.neg A.m01, GaussRat.neg A.m10, GaussRat.neg A.m11⟩

def mul (A B : Mat2x2Q) : Mat2x2Q :=
  ⟨GaussRat.add (GaussRat.mul A.m00 B.m00) (GaussRat.mul A.m01 B.m10),
   GaussRat.add (GaussRat.mul A.m00 B.m01) (GaussRat.mul A.m01 B.m11),
   GaussRat.add (GaussRat.mul A.m10 B.m00) (GaussRat.mul A.m11 B.m10),
   GaussRat.add (GaussRat.mul A.m10 B.m01) (GaussRat.mul A.m11 B.m11)⟩

def trace (A : Mat2x2Q) : GaussRat :=
  GaussRat.add A.m00 A.m11

def det (A : Mat2x2Q) : GaussRat :=
  GaussRat.sub (GaussRat.mul A.m00 A.m11) (GaussRat.mul A.m01 A.m10)

/-- Multiplicative commutator `A B A⁻¹ B⁻¹` given explicit inverses `A_inv, B_inv`. -/
def commutatorHolonomy (A B A_inv B_inv : Mat2x2Q) : Mat2x2Q :=
  mul (mul A B) (mul A_inv B_inv)

theorem mul_assoc (X Y Z : Mat2x2Q) :
    mul (mul X Y) Z = mul X (mul Y Z) := by
  ext <;> dsimp [mul, GaussRat.add, GaussRat.mul] <;> ring

theorem neg_mul (X Y : Mat2x2Q) :
    mul (neg X) Y = neg (mul X Y) := by
  ext <;> dsimp [mul, neg, GaussRat.add, GaussRat.mul, GaussRat.neg] <;> ring

theorem identity_mul (X : Mat2x2Q) :
    mul identity X = X := by
  ext <;> dsimp [mul, identity, GaussRat.add, GaussRat.mul, GaussRat.one, GaussRat.zero] <;> ring

theorem neg_identity_eq :
    neg identity = negIdentity := by
  rfl

end Mat2x2Q

/-- Theorem 9: For any invertible 2×2 matrices `A, B` over `ℚ(i)` satisfying `A B = -B A`,
    the multiplicative commutator `A B A⁻¹ B⁻¹` equals `-I₂` and has trace `-2 < 0`. -/
theorem anticommuting_mat2x2_commutator_trace_neg_two
    (A B A_inv B_inv : Mat2x2Q)
    (h_anticomm : Mat2x2Q.mul A B = Mat2x2Q.neg (Mat2x2Q.mul B A))
    (h_invA : Mat2x2Q.mul A A_inv = Mat2x2Q.identity)
    (h_invB : Mat2x2Q.mul B B_inv = Mat2x2Q.identity) :
    Mat2x2Q.commutatorHolonomy A B A_inv B_inv = Mat2x2Q.negIdentity ∧
    (Mat2x2Q.trace (Mat2x2Q.commutatorHolonomy A B A_inv B_inv)).re = -2 ∧
    (Mat2x2Q.trace (Mat2x2Q.commutatorHolonomy A B A_inv B_inv)).im = 0 := by
  have h_comm : Mat2x2Q.commutatorHolonomy A B A_inv B_inv = Mat2x2Q.negIdentity := by
    dsimp [Mat2x2Q.commutatorHolonomy]
    rw [h_anticomm, Mat2x2Q.neg_mul, Mat2x2Q.mul_assoc]
    rw [← Mat2x2Q.mul_assoc A A_inv B_inv, h_invA, Mat2x2Q.identity_mul, h_invB]
    exact Mat2x2Q.neg_identity_eq
  refine ⟨h_comm, ?_, ?_⟩
  · rw [h_comm]
    dsimp [Mat2x2Q.trace, Mat2x2Q.negIdentity, GaussRat.add]
    norm_num
  · rw [h_comm]
    dsimp [Mat2x2Q.trace, Mat2x2Q.negIdentity, GaussRat.add]
    norm_num

/-- Non-commuting `SU(2)` counterexample matrix `A = diag(i, -i)`. -/
def su2CounterexampleA : Mat2x2Q :=
  ⟨GaussRat.iUnit, GaussRat.zero, GaussRat.zero, GaussRat.negIUnit⟩

/-- Inverse `A⁻¹ = diag(-i, i)` of `su2CounterexampleA`. -/
def su2CounterexampleAInv : Mat2x2Q :=
  ⟨GaussRat.negIUnit, GaussRat.zero, GaussRat.zero, GaussRat.iUnit⟩

/-- Non-commuting `SU(2)` Pythagorean rotator `B = [[4/5, -3/5], [3/5, 4/5]]`. -/
def su2CounterexampleB : Mat2x2Q :=
  ⟨⟨4 / 5, 0⟩, ⟨-3 / 5, 0⟩, ⟨3 / 5, 0⟩, ⟨4 / 5, 0⟩⟩

/-- Inverse `B⁻¹ = [[4/5, 3/5], [-3/5, 4/5]]` of `su2CounterexampleB`. -/
def su2CounterexampleBInv : Mat2x2Q :=
  ⟨⟨4 / 5, 0⟩, ⟨3 / 5, 0⟩, ⟨-3 / 5, 0⟩, ⟨4 / 5, 0⟩⟩

/-- Theorem 10: Non-commuting `SU(2)` holonomies do not generally give negative commutator trace:
    for `A = diag(i, -i) ∈ SU(2)` and `B = [[4/5, -3/5], [3/5, 4/5]] ∈ SU(2)`,
    `A B ≠ B A` yet `Tr(A B A⁻¹ B⁻¹) = 14/25 > 0`. -/
theorem noncommuting_su2_positive_commutator_trace_counterexample :
    Mat2x2Q.det su2CounterexampleA = GaussRat.one ∧
    Mat2x2Q.det su2CounterexampleB = GaussRat.one ∧
    Mat2x2Q.mul su2CounterexampleA su2CounterexampleAInv = Mat2x2Q.identity ∧
    Mat2x2Q.mul su2CounterexampleB su2CounterexampleBInv = Mat2x2Q.identity ∧
    Mat2x2Q.mul su2CounterexampleA su2CounterexampleB ≠
      Mat2x2Q.mul su2CounterexampleB su2CounterexampleA ∧
    (Mat2x2Q.trace
      (Mat2x2Q.commutatorHolonomy
        su2CounterexampleA su2CounterexampleB
        su2CounterexampleAInv su2CounterexampleBInv)).re = 14 / 25 ∧
    (Mat2x2Q.trace
      (Mat2x2Q.commutatorHolonomy
        su2CounterexampleA su2CounterexampleB
        su2CounterexampleAInv su2CounterexampleBInv)).im = 0 ∧
    (14 / 25 : ℚ) > 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, by norm_num⟩
  · ext <;> dsimp [Mat2x2Q.det, su2CounterexampleA, GaussRat.sub, GaussRat.mul,
      GaussRat.iUnit, GaussRat.negIUnit, GaussRat.zero, GaussRat.one] <;> norm_num
  · ext <;> dsimp [Mat2x2Q.det, su2CounterexampleB, GaussRat.sub, GaussRat.mul,
      GaussRat.one] <;> norm_num
  · ext <;> dsimp [Mat2x2Q.mul, su2CounterexampleA, su2CounterexampleAInv, Mat2x2Q.identity,
      GaussRat.add, GaussRat.mul, GaussRat.iUnit, GaussRat.negIUnit,
      GaussRat.zero, GaussRat.one] <;> norm_num
  · ext <;> dsimp [Mat2x2Q.mul, su2CounterexampleB, su2CounterexampleBInv, Mat2x2Q.identity,
      GaussRat.add, GaussRat.mul, GaussRat.zero, GaussRat.one] <;> norm_num
  · intro h_eq
    have h01 : (Mat2x2Q.mul su2CounterexampleA su2CounterexampleB).m01.im =
        (Mat2x2Q.mul su2CounterexampleB su2CounterexampleA).m01.im :=
      congrArg GaussRat.im (congrArg Mat2x2Q.m01 h_eq)
    dsimp [Mat2x2Q.mul, su2CounterexampleA, su2CounterexampleB,
      GaussRat.add, GaussRat.mul, GaussRat.iUnit, GaussRat.negIUnit, GaussRat.zero] at h01
    norm_num at h01
  · dsimp [Mat2x2Q.trace, Mat2x2Q.commutatorHolonomy, Mat2x2Q.mul,
      su2CounterexampleA, su2CounterexampleB, su2CounterexampleAInv, su2CounterexampleBInv,
      GaussRat.add, GaussRat.mul, GaussRat.iUnit, GaussRat.negIUnit, GaussRat.zero]
    norm_num
  · dsimp [Mat2x2Q.trace, Mat2x2Q.commutatorHolonomy, Mat2x2Q.mul,
      su2CounterexampleA, su2CounterexampleB, su2CounterexampleAInv, su2CounterexampleBInv,
      GaussRat.add, GaussRat.mul, GaussRat.iUnit, GaussRat.negIUnit, GaussRat.zero]
    norm_num

end FoliatedFracton2Gauge

#print axioms FoliatedFracton2Gauge.hinge_path_preserves_relative_order
#print axioms FoliatedFracton2Gauge.hinge_path_exchange_impossible
#print axioms FoliatedFracton2Gauge.discrete_ivt_zero
#print axioms FoliatedFracton2Gauge.hinge_lineon_exchange_collision_obstruction
#print axioms FoliatedFracton2Gauge.hinge_lineon_worldline_permutation_sign_trivial
#print axioms FoliatedFracton2Gauge.nonabelian_hinge_commutator_curvature_obstruction
#print axioms FoliatedFracton2Gauge.decoupled_foliated_lineon_sign_free
#print axioms FoliatedFracton2Gauge.y_junction_collision_free_exchange_exists
#print axioms FoliatedFracton2Gauge.y_junction_exchange_induces_negative_sign
#print axioms FoliatedFracton2Gauge.foliated_lineon_axis_conservation_forbids_branch_exchange
#print axioms FoliatedFracton2Gauge.anticommuting_mat2x2_commutator_trace_neg_two
#print axioms FoliatedFracton2Gauge.noncommuting_su2_positive_commutator_trace_counterexample

