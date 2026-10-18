-- Finite Cochain Complex and Boundary Operators in Lean 4
-- AuthorityEffect: None

namespace FiniteCochain

/-- 0-cochains on the 3-vertex carrier: integer potentials at vertices 0, 1, 2. -/
structure Cochain0 where
  v0 : Int
  v1 : Int
  v2 : Int
  deriving DecidableEq, Repr

/-- 1-cochains on the 3-edge carrier: directed transitions (0,1), (1,2), (2,0). -/
structure Cochain1 where
  e01 : Int
  e12 : Int
  e20 : Int
  deriving DecidableEq, Repr

/-- 2-cochains on the oriented 2-cell (face bounded by edges e01, e12, e20). -/
structure Cochain2 where
  f0 : Int
  deriving DecidableEq, Repr

/-- Coboundary map d0 : C^0 -> C^1 given by (d0 α)(u, v) = α(v) - α(u). -/
def d0 (a : Cochain0) : Cochain1 :=
  ⟨a.v1 - a.v0, a.v2 - a.v1, a.v0 - a.v2⟩

/-- Coboundary map d1 : C^1 -> C^2 evaluating the oriented circulation around the 2-cell. -/
def d1 (b : Cochain1) : Cochain2 :=
  ⟨b.e01 + b.e12 + b.e20⟩

/-- Addition of 1-cochains. -/
def add1 (b1 b2 : Cochain1) : Cochain1 :=
  ⟨b1.e01 + b2.e01, b1.e12 + b2.e12, b1.e20 + b2.e20⟩

/-- Fundamental cochain complex identity: d1 ∘ d0 = 0.
    The coboundary of any 0-cochain has zero circulation around the 2-cell. -/
theorem d1_d0_zero (a : Cochain0) : d1 (d0 a) = ⟨0⟩ := by
  dsimp [d1, d0]
  have h : (a.v1 - a.v0) + (a.v2 - a.v1) + (a.v0 - a.v2) = 0 := by omega
  rw [h]

/-- Predicate for 1-coboundaries B^1 := im(d0). -/
def isCoboundary (b : Cochain1) : Prop :=
  ∃ a : Cochain0, d0 a = b

/-- Predicate for 1-cocycles Z^1 := ker(d1). -/
def isCocycle (b : Cochain1) : Prop :=
  d1 b = ⟨0⟩

/-- Every coboundary is a cocycle: B^1 ⊆ Z^1. -/
theorem coboundary_is_cocycle (b : Cochain1) (h : isCoboundary b) : isCocycle b := by
  rcases h with ⟨a, rfl⟩
  exact d1_d0_zero a

/-- Gauge invariance of the closure defect Γ_2([x]):
    Adding any coboundary d0 α to a 1-cochain leaves the 2-cell curl d1 strictly invariant. -/
theorem d1_add_coboundary (b : Cochain1) (a : Cochain0) :
    d1 (add1 b (d0 a)) = d1 b := by
  dsimp [d1, add1, d0]
  have h : (b.e01 + (a.v1 - a.v0)) + (b.e12 + (a.v2 - a.v1)) + (b.e20 + (a.v0 - a.v2)) = b.e01 + b.e12 + b.e20 := by omega
  rw [h]

/-- On the oriented triangle cycle, any coboundary has zero total circulation. -/
theorem coboundary_sum_zero (b : Cochain1) (h : isCoboundary b) :
    b.e01 + b.e12 + b.e20 = 0 := by
  rcases h with ⟨a, rfl⟩
  dsimp [d0]
  omega

/-- Obstruction to exactness: A circulation cochain with non-zero sum around the cycle
    cannot be represented as a coboundary d0 α. -/
theorem non_trivial_circulation_not_coboundary :
    ¬ isCoboundary ⟨1, 1, 1⟩ := by
  intro h
  have h_sum := coboundary_sum_zero ⟨1, 1, 1⟩ h
  dsimp at h_sum
  omega

theorem cochain1_ext (x y : Cochain1) (h1 : x.e01 = y.e01) (h2 : x.e12 = y.e12) (h3 : x.e20 = y.e20) : x = y := by
  cases x
  cases y
  dsimp at h1 h2 h3
  rw [h1, h2, h3]

/-- Exactness on the filled triangle: Every 1-cocycle on this single 2-cell complex
    is a 1-coboundary (H^1 = Z^1 / B^1 = 0). -/
theorem triangle_cocycle_is_coboundary (b : Cochain1) (h : isCocycle b) :
    isCoboundary b := by
  dsimp [isCocycle, d1] at h
  have h_eq : b.e01 + b.e12 + b.e20 = 0 := by
    have h_f0 := congrArg Cochain2.f0 h
    exact h_f0
  refine ⟨⟨0, b.e01, b.e01 + b.e12⟩, ?_⟩
  apply cochain1_ext
  · dsimp [d0]; omega
  · dsimp [d0]; omega
  · dsimp [d0]; omega

#print axioms d1_d0_zero
#print axioms coboundary_is_cocycle
#print axioms d1_add_coboundary
#print axioms coboundary_sum_zero
#print axioms non_trivial_circulation_not_coboundary
#print axioms triangle_cocycle_is_coboundary

end FiniteCochain
