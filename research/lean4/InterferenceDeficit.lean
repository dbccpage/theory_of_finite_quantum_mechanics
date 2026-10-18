/-
  InterferenceDeficit.lean
  Additivity defect and non-descent from L1 weights for Paper 061.
  AuthorityEffect: None
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import GaussIntKernel

namespace InterferenceNonL1Resource

/-- Diagonal L1 norm: sum of squared moduli on each sector -/
def L1_norm (v : Vec GaussInt Bool) : Int :=
  GaussInt.sqMod (v false) + GaussInt.sqMod (v true)

/-- Interfered weight: modulus squared of the coherent sum -/
def interfered_weight (v : Vec GaussInt Bool) : Int :=
  GaussInt.sqMod (GaussInt.add (v false) (v true))

/-- Interference Deficit: difference between coherent and incoherent sums -/
def interference_deficit (v : Vec GaussInt Bool) : Int :=
  interfered_weight v - L1_norm v

theorem sq_add_cross (a b c d : Int) :
    (a + c) * (a + c) + (b + d) * (b + d) - (a * a + b * b + (c * c + d * d)) = 2 * a * c + 2 * b * d := by
  have h1 : (a + c) * (a + c) = a * a + c * a + a * c + c * c := by
    calc (a + c) * (a + c) = a * (a + c) + c * (a + c) := Int.add_mul a c (a + c)
    _ = a * a + a * c + (c * a + c * c) := by rw [Int.mul_add, Int.mul_add]
    _ = a * a + c * a + a * c + c * c := by omega
  have hca : c * a = a * c := Int.mul_comm c a
  have h2 : (b + d) * (b + d) = b * b + d * b + b * d + d * d := by
    calc (b + d) * (b + d) = b * (b + d) + d * (b + d) := Int.add_mul b d (b + d)
    _ = b * b + b * d + (d * b + d * d) := by rw [Int.mul_add, Int.mul_add]
    _ = b * b + d * b + b * d + d * d := by omega
  have hdb : d * b = b * d := Int.mul_comm d b
  have h_assoc_a : 2 * a * c = 2 * (a * c) := Int.mul_assoc 2 a c
  have h_assoc_b : 2 * b * d = 2 * (b * d) := Int.mul_assoc 2 b d
  rw [h_assoc_a, h_assoc_b]
  rw [h1, h2, hca, hdb]
  omega

/-- Algebraic Cross-Term Identity: deficit equals twice real part of cross term -/
theorem deficit_eq_cross_term (v : Vec GaussInt Bool) :
    interference_deficit v = 2 * (v false).re * (v true).re + 2 * (v false).im * (v true).im := by
  dsimp [interference_deficit, interfered_weight, L1_norm, GaussInt.sqMod, GaussInt.add]
  exact sq_add_cross (v false).re (v false).im (v true).re (v true).im

/-! ### The Three Deficit Trichotomy Witnesses -/
def psi_plus : Vec GaussInt Bool := fun _ => GaussInt.one
def psi_minus : Vec GaussInt Bool := fun q => if q then GaussInt.neg GaussInt.one else GaussInt.one
def psi_ortho : Vec GaussInt Bool := fun q => if q then GaussInt.i else GaussInt.one

theorem psi_plus_deficit : interference_deficit psi_plus = 2 := by decide
theorem psi_minus_deficit : interference_deficit psi_minus = -2 := by decide
theorem psi_ortho_deficit : interference_deficit psi_ortho = 0 := by decide

/-- THEOREM A1: No function of the L1 norm determines the interfered weight -/
theorem L1_cannot_compute_interference :
    ¬ ∃ f : Int → Int, ∀ v : Vec GaussInt Bool, interfered_weight v = f (L1_norm v) := by
  intro ⟨f, hf⟩
  have h1 : interfered_weight psi_plus = f (L1_norm psi_plus) := hf psi_plus
  have h2 : interfered_weight psi_minus = f (L1_norm psi_minus) := hf psi_minus
  have h_plus : L1_norm psi_plus = 2 := by decide
  have h_minus : L1_norm psi_minus = 2 := by decide
  rw [h_plus] at h1
  rw [h_minus] at h2
  have h_eq : interfered_weight psi_plus = interfered_weight psi_minus := h1.trans h2.symm
  revert h_eq
  decide

end InterferenceNonL1Resource
