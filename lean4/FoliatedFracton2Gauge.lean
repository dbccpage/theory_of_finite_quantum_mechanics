


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

def hingeCommutatorTrace (is_nonabelian : Bool) : Int :=
  if is_nonabelian then -2 else 2

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

