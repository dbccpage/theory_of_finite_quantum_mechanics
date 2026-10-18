

namespace FiniteCochain

structure Cochain0 where
  v0 : Int
  v1 : Int
  v2 : Int
  deriving DecidableEq, Repr

structure Cochain1 where
  e01 : Int
  e12 : Int
  e20 : Int
  deriving DecidableEq, Repr

structure Cochain2 where
  f0 : Int
  deriving DecidableEq, Repr

def d0 (a : Cochain0) : Cochain1 :=
  ⟨a.v1 - a.v0, a.v2 - a.v1, a.v0 - a.v2⟩

def d1 (b : Cochain1) : Cochain2 :=
  ⟨b.e01 + b.e12 + b.e20⟩

def add1 (b1 b2 : Cochain1) : Cochain1 :=
  ⟨b1.e01 + b2.e01, b1.e12 + b2.e12, b1.e20 + b2.e20⟩

theorem d1_d0_zero (a : Cochain0) : d1 (d0 a) = ⟨0⟩ := by
  dsimp [d1, d0]
  have h : (a.v1 - a.v0) + (a.v2 - a.v1) + (a.v0 - a.v2) = 0 := by omega
  rw [h]

def isCoboundary (b : Cochain1) : Prop :=
  ∃ a : Cochain0, d0 a = b

def isCocycle (b : Cochain1) : Prop :=
  d1 b = ⟨0⟩

theorem coboundary_is_cocycle (b : Cochain1) (h : isCoboundary b) : isCocycle b := by
  rcases h with ⟨a, rfl⟩
  exact d1_d0_zero a

theorem d1_add_coboundary (b : Cochain1) (a : Cochain0) :
    d1 (add1 b (d0 a)) = d1 b := by
  dsimp [d1, add1, d0]
  have h : (b.e01 + (a.v1 - a.v0)) + (b.e12 + (a.v2 - a.v1)) + (b.e20 + (a.v0 - a.v2)) = b.e01 + b.e12 + b.e20 := by omega
  rw [h]

theorem coboundary_sum_zero (b : Cochain1) (h : isCoboundary b) :
    b.e01 + b.e12 + b.e20 = 0 := by
  rcases h with ⟨a, rfl⟩
  dsimp [d0]
  omega

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

private def l5aProvenance : String :=
  "Origin: lean4/FiniteCochain.lean Claim: d1_d0_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
