/-!
# Finite case for TFQ-0003

AuthorityEffect: None.

Two finite complexes only. This is not a derivation from Genesis regime events,
not a Rust witness, and not a three-language correspondence.
-/

namespace FiniteObstructionTwoComplexes

inductive V3 where
  | v0
  | v1
  | v2
  deriving DecidableEq, Repr

inductive E3 where
  | e01
  | e12
  | e02
  deriving DecidableEq, Repr

/-- Oriented edges `(0,1)`, `(1,2)`, `(0,2)`. -/
def d0 (f : V3 → Int) : E3 → Int
  | .e01 => f .v1 - f .v0
  | .e12 => f .v2 - f .v1
  | .e02 => f .v2 - f .v0

/-- Face charge of the single triangle: `w01 + w12 - w02`. -/
def d1 (w : E3 → Int) : Int :=
  w .e01 + w .e12 - w .e02

def l1 (w : E3 → Int) : Nat :=
  Int.natAbs (w .e01) + Int.natAbs (w .e12) + Int.natAbs (w .e02)

/-- Quotient residual mass on this triangle: `|d1 w|`. -/
def phi1 (w : E3 → Int) : Nat :=
  Int.natAbs (d1 w)

/-- Closure charge. On this one-face complex it equals `Phi1`. -/
def gamma2 (w : E3 → Int) : Nat :=
  Int.natAbs (d1 w)

theorem gamma2_eq_phi1 (w : E3 → Int) : gamma2 w = phi1 w := rfl

theorem d1_d0 (f : V3 → Int) : d1 (d0 f) = 0 := by
  simp only [d1, d0]
  omega

theorem natAbs_sum3 (a b c : Int) :
    Int.natAbs (a + b + c) ≤ Int.natAbs a + Int.natAbs b + Int.natAbs c := by
  calc
    Int.natAbs (a + b + c) ≤ Int.natAbs (a + b) + Int.natAbs c := Int.natAbs_add_le (a + b) c
    _ ≤ Int.natAbs a + Int.natAbs b + Int.natAbs c :=
      Nat.add_le_add_right (Int.natAbs_add_le a b) _

/-- Repair that clears edges `(0,1)` and `(1,2)`. -/
def clear01 (w : E3 → Int) : V3 → Int
  | .v0 => 0
  | .v1 => w .e01
  | .v2 => w .e01 + w .e12

theorem clear01_e01 (w : E3 → Int) : d0 (clear01 w) .e01 = w .e01 := by
  simp [d0, clear01, Int.sub_zero]

theorem clear01_e12 (w : E3 → Int) : d0 (clear01 w) .e12 = w .e12 := by
  simp only [d0, clear01]
  omega

theorem clear01_e02 (w : E3 → Int) : d0 (clear01 w) .e02 = w .e01 + w .e12 := by
  simp [d0, clear01]

theorem residual_supported_on_e02 (w : E3 → Int) :
    (w .e01 - d0 (clear01 w) .e01 = 0) ∧
      (w .e12 - d0 (clear01 w) .e12 = 0) ∧
      (w .e02 - d0 (clear01 w) .e02 = -(d1 w)) := by
  refine ⟨?_, ?_, ?_⟩
  · simp [clear01_e01]
  · simp [clear01_e12]
  · simp [d1, clear01_e02, Int.sub_eq_add_neg]
    omega

theorem phi1_attained (w : E3 → Int) :
    l1 (fun e => w e - d0 (clear01 w) e) = phi1 w := by
  have h := residual_supported_on_e02 w
  have h01 : (fun e => w e - d0 (clear01 w) e) .e01 = 0 := h.1
  have h12 : (fun e => w e - d0 (clear01 w) e) .e12 = 0 := h.2.1
  have h02 : (fun e => w e - d0 (clear01 w) e) .e02 = -(d1 w) := h.2.2
  simp [l1, phi1, h01, h12, h02, Int.natAbs_zero, Int.natAbs_neg, Nat.zero_add]

theorem phi1_lower (w : E3 → Int) (f : V3 → Int) :
    phi1 w ≤ l1 (fun e => w e - d0 f e) := by
  have hlin : d1 (fun e => w e - d0 f e) = d1 w := by
    simp only [d1, d0]
    have hz : d1 (d0 f) = 0 := d1_d0 f
    simp only [d1, d0] at hz
    omega
  let x := w .e01 - d0 f .e01
  let y := w .e12 - d0 f .e12
  let z := w .e02 - d0 f .e02
  have hcharge : x + y - z = d1 w := by
    simpa [x, y, z, d1] using hlin
  have hineq : Int.natAbs (x + y - z) ≤ Int.natAbs x + Int.natAbs y + Int.natAbs z := by
    have hsum := natAbs_sum3 x y (-z)
    simpa [Int.sub_eq_add_neg, Int.natAbs_neg] using hsum
  simpa [phi1, l1, x, y, z, hcharge] using hineq

def equiv (w w' : E3 → Int) : Prop :=
  ∃ f : V3 → Int, ∀ e, w e = w' e + d0 f e

theorem equiv_of_d1 (w w' : E3 → Int) (h : d1 w = d1 w') : equiv w w' := by
  let u : E3 → Int := fun e => w e - w' e
  have hu : d1 u = 0 := by
    simp only [u, d1] at *
    omega
  refine ⟨clear01 u, ?_⟩
  intro e
  have he : u e = d0 (clear01 u) e := by
    cases e with
    | e01 => simp [u, clear01_e01]
    | e12 => simp [u, clear01_e12]
    | e02 =>
        have h02 : u .e01 + u .e12 = u .e02 := by
          have hz : u .e01 + u .e12 - u .e02 = 0 := by simpa [d1] using hu
          exact (Int.sub_eq_zero).mp hz
        simp [d0, clear01, h02]
  have he' : w e - w' e = d0 (clear01 u) e := by simpa [u] using he
  omega

theorem d1_of_equiv {w w' : E3 → Int} (h : equiv w w') : d1 w = d1 w' := by
  rcases h with ⟨f, hf⟩
  have h01 := hf .e01
  have h12 := hf .e12
  have h02 := hf .e02
  simp only [d0] at h01 h12 h02
  simp only [d1]
  omega

theorem equiv_iff_d1 (w w' : E3 → Int) : equiv w w' ↔ d1 w = d1 w' :=
  ⟨d1_of_equiv, equiv_of_d1 w w'⟩

/-- `some (num, den)` is the rational `num / den`. `none` refuses the ratio. -/
def rcl (phi gamma : Nat) : Option (Nat × Nat) :=
  if phi ≠ 0 then some (gamma, phi) else if gamma = 0 then some (0, 1) else none

theorem rcl_refuses_zero_over_one : rcl 0 1 = none := rfl

theorem triangle_rcl_defined (w : E3 → Int) : rcl (phi1 w) (gamma2 w) ≠ none := by
  unfold rcl phi1 gamma2
  by_cases h : Int.natAbs (d1 w) = 0
  · simp [h]
  · simp [h]

def sample : E3 → Int
  | .e01 => 1
  | .e12 => 1
  | .e02 => 0

def recordedRepair : V3 → Int
  | .v0 => 0
  | .v1 => 1
  | .v2 => 0

theorem sample_d1 : d1 sample = 2 := rfl

theorem sample_phi1 : phi1 sample = 2 := rfl

theorem sample_gamma2 : gamma2 sample = 2 := rfl

theorem sample_rcl : rcl (phi1 sample) (gamma2 sample) = some (2, 2) := rfl

theorem sample_ratio_one : phi1 sample = gamma2 sample := rfl

theorem recorded_residual_values :
    (sample .e01 - d0 recordedRepair .e01 = 0) ∧
      (sample .e12 - d0 recordedRepair .e12 = 2) ∧
      (sample .e02 - d0 recordedRepair .e02 = 0) := by
  decide

theorem recorded_residual_l1 :
    l1 (fun e => sample e - d0 recordedRepair e) = 2 := by
  decide

def zeroCochain : E3 → Int := fun _ => 0

theorem zero_signature :
    phi1 zeroCochain = 0 ∧ gamma2 zeroCochain = 0 ∧
      rcl (phi1 zeroCochain) (gamma2 zeroCochain) = some (0, 1) ∧
      equiv zeroCochain zeroCochain := by
  refine ⟨rfl, rfl, rfl, ?_⟩
  exact ⟨fun _ => 0, by intro e; cases e <;> rfl⟩

/-- Raw vertex comparison. It is not the cochain quotient. -/
def edge02 : E3 → Int
  | .e02 => 1
  | .e01 => 0
  | .e12 => 0

theorem vertex_comparison : V3.v0 ≠ V3.v2 := by
  intro h
  cases h

theorem edge02_not_exact : ¬ equiv edge02 zeroCochain := by
  intro h
  have hd : d1 edge02 = d1 zeroCochain := d1_of_equiv h
  simp [d1, edge02, zeroCochain] at hd

theorem comparison_is_not_the_quotient :
    V3.v0 ≠ V3.v2 ∧ ¬ equiv edge02 zeroCochain :=
  ⟨vertex_comparison, edge02_not_exact⟩

inductive V4 where
  | v0
  | v1
  | v2
  | v3
  deriving DecidableEq, Repr

inductive E4 where
  | e01
  | e12
  | e23
  | e30
  deriving DecidableEq, Repr

def d0Cycle (f : V4 → Int) : E4 → Int
  | .e01 => f .v1 - f .v0
  | .e12 => f .v2 - f .v1
  | .e23 => f .v3 - f .v2
  | .e30 => f .v0 - f .v3

def holonomy (w : E4 → Int) : Int :=
  w .e01 + w .e12 + w .e23 + w .e30

def l1Cycle (w : E4 → Int) : Nat :=
  Int.natAbs (w .e01) + Int.natAbs (w .e12) + Int.natAbs (w .e23) + Int.natAbs (w .e30)

/-- No 2-cell is declared, so the closure charge is the constant 0. -/
def gamma2Cycle (_w : E4 → Int) : Nat :=
  0

def phi1Cycle (w : E4 → Int) : Nat :=
  Int.natAbs (holonomy w)

theorem holonomy_d0 (f : V4 → Int) : holonomy (d0Cycle f) = 0 := by
  simp only [holonomy, d0Cycle]
  omega

theorem natAbs_sum4 (a b c d : Int) :
    Int.natAbs (a + b + c + d) ≤
      Int.natAbs a + Int.natAbs b + Int.natAbs c + Int.natAbs d := by
  calc
    Int.natAbs (a + b + c + d) ≤ Int.natAbs (a + b + c) + Int.natAbs d :=
      Int.natAbs_add_le (a + b + c) d
    _ ≤ Int.natAbs (a + b) + Int.natAbs c + Int.natAbs d :=
      Nat.add_le_add_right (Int.natAbs_add_le (a + b) c) _
    _ ≤ Int.natAbs a + Int.natAbs b + Int.natAbs c + Int.natAbs d :=
      Nat.add_le_add_right (Nat.add_le_add_right (Int.natAbs_add_le a b) _) _

def concentrate (w : E4 → Int) : V4 → Int
  | .v0 => 0
  | .v1 => w .e01 - holonomy w
  | .v2 => w .e01 - holonomy w + w .e12
  | .v3 => w .e01 - holonomy w + w .e12 + w .e23

theorem phi1Cycle_attained (w : E4 → Int) :
    l1Cycle (fun e => w e - d0Cycle (concentrate w) e) = phi1Cycle w := by
  have h01 : w .e01 - d0Cycle (concentrate w) .e01 = holonomy w := by
    simp [d0Cycle, concentrate, Int.sub_zero]
    omega
  have h12 : w .e12 - d0Cycle (concentrate w) .e12 = 0 := by
    simp [d0Cycle, concentrate]
    omega
  have h23 : w .e23 - d0Cycle (concentrate w) .e23 = 0 := by
    simp [d0Cycle, concentrate]
    omega
  have h30 : w .e30 - d0Cycle (concentrate w) .e30 = 0 := by
    simp [d0Cycle, concentrate, holonomy]
    omega
  simp [l1Cycle, phi1Cycle, h01, h12, h23, h30, Int.natAbs_zero, Nat.add_zero]

theorem phi1Cycle_lower (w : E4 → Int) (f : V4 → Int) :
    phi1Cycle w ≤ l1Cycle (fun e => w e - d0Cycle f e) := by
  have hlin : holonomy (fun e => w e - d0Cycle f e) = holonomy w := by
    simp only [holonomy, d0Cycle]
    have hz : holonomy (d0Cycle f) = 0 := holonomy_d0 f
    simp only [holonomy, d0Cycle] at hz
    omega
  have hsum :
      Int.natAbs (holonomy (fun e => w e - d0Cycle f e)) ≤
        l1Cycle (fun e => w e - d0Cycle f e) := by
    simpa [holonomy, l1Cycle] using
      natAbs_sum4 (w .e01 - d0Cycle f .e01) (w .e12 - d0Cycle f .e12)
        (w .e23 - d0Cycle f .e23) (w .e30 - d0Cycle f .e30)
  simpa [phi1Cycle, hlin] using hsum

def equivCycle (w w' : E4 → Int) : Prop :=
  ∃ f : V4 → Int, ∀ e, w e = w' e + d0Cycle f e

def cycleSample : E4 → Int
  | .e01 => 1
  | .e12 => 0
  | .e23 => 0
  | .e30 => 0

def zeroCycle : E4 → Int := fun _ => 0

theorem cycle_not_exact : ¬ equivCycle cycleSample zeroCycle := by
  intro h
  rcases h with ⟨f, hf⟩
  have h01 := hf .e01
  have h12 := hf .e12
  have h23 := hf .e23
  have h30 := hf .e30
  simp only [cycleSample, zeroCycle, d0Cycle] at h01 h12 h23 h30
  have hhol : holonomy cycleSample = 1 := by simp [holonomy, cycleSample]
  have hcob : holonomy (d0Cycle f) = 0 := holonomy_d0 f
  have hsum : holonomy cycleSample = holonomy (d0Cycle f) := by
    simp only [holonomy, d0Cycle] at hcob ⊢
    omega
  omega

theorem cycle_rcl_defined (w : E4 → Int) : rcl (phi1Cycle w) (gamma2Cycle w) ≠ none := by
  unfold rcl gamma2Cycle
  by_cases h : phi1Cycle w = 0
  · simp [h]
  · simp [h]

theorem cycle_signature :
    phi1Cycle cycleSample = 1 ∧ gamma2Cycle cycleSample = 0 ∧
      rcl (phi1Cycle cycleSample) (gamma2Cycle cycleSample) = some (0, 1) ∧
      ¬ equivCycle cycleSample zeroCycle := by
  refine ⟨rfl, rfl, rfl, cycle_not_exact⟩

def triangleVertices : List V3 := [.v0, .v1, .v2]
def triangleEdges : List E3 := [.e01, .e12, .e02]
def cycleEdges : List E4 := [.e01, .e12, .e23, .e30]

theorem vertex_count : triangleVertices.length = 3 ∧ triangleVertices.Nodup := by decide
theorem edge_count_triangle : triangleEdges.length = 3 ∧ triangleEdges.Nodup := by decide
theorem edge_count_cycle : cycleEdges.length = 4 ∧ cycleEdges.Nodup := by decide

theorem triangle_vertices_complete (v : V3) : v ∈ triangleVertices := by
  cases v <;> decide
theorem triangle_edges_complete (e : E3) : e ∈ triangleEdges := by
  cases e <;> decide
theorem cycle_edges_complete (e : E4) : e ∈ cycleEdges := by
  cases e <;> decide

end FiniteObstructionTwoComplexes

#print axioms FiniteObstructionTwoComplexes.d1_d0
#print axioms FiniteObstructionTwoComplexes.phi1_attained
#print axioms FiniteObstructionTwoComplexes.phi1_lower
#print axioms FiniteObstructionTwoComplexes.equiv_iff_d1
#print axioms FiniteObstructionTwoComplexes.sample_phi1
#print axioms FiniteObstructionTwoComplexes.sample_gamma2
#print axioms FiniteObstructionTwoComplexes.sample_rcl
#print axioms FiniteObstructionTwoComplexes.sample_ratio_one
#print axioms FiniteObstructionTwoComplexes.recorded_residual_l1
#print axioms FiniteObstructionTwoComplexes.zero_signature
#print axioms FiniteObstructionTwoComplexes.comparison_is_not_the_quotient
#print axioms FiniteObstructionTwoComplexes.rcl_refuses_zero_over_one
#print axioms FiniteObstructionTwoComplexes.triangle_rcl_defined
#print axioms FiniteObstructionTwoComplexes.phi1Cycle_attained
#print axioms FiniteObstructionTwoComplexes.phi1Cycle_lower
#print axioms FiniteObstructionTwoComplexes.cycle_rcl_defined
#print axioms FiniteObstructionTwoComplexes.cycle_signature
#print axioms FiniteObstructionTwoComplexes.holonomy_d0

#print axioms FiniteObstructionTwoComplexes.vertex_count

#print axioms FiniteObstructionTwoComplexes.edge_count_triangle

#print axioms FiniteObstructionTwoComplexes.edge_count_cycle

#print axioms FiniteObstructionTwoComplexes.triangle_vertices_complete

#print axioms FiniteObstructionTwoComplexes.triangle_edges_complete

#print axioms FiniteObstructionTwoComplexes.cycle_edges_complete
