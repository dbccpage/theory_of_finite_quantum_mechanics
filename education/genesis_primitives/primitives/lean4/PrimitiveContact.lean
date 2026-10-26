/-!
# Genesis Primitives Category 9: Pre-Topological Contact Spaces & Replacement Kernels (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/PrimitiveContact.lean
- lean4/Derivation/ContactKernel.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.PrimitiveContact

/-- Common replacement kernel: a valued difference presentation with designated
    endpoints, a diagonal-zero law, and a refutation-grade non-zero witness. -/
structure WitnessedDiff (X R : Type) where
  delta : X → X → R
  Zero : R → Prop
  a : X
  b : X
  diag_zero : ∀ x, Zero (delta x x)
  apart_ab : ¬ Zero (delta a b)

/-- The apartness a kernel induces: non-zero difference value. -/
def kernelApart {X R : Type} (K : WitnessedDiff X R) : X → X → Prop :=
  fun x y => ¬ K.Zero (K.delta x y)

/-- Irreflexivity of the induced apartness is immediate from the diagonal-zero law. -/
theorem kernelApart_irrefl {X R : Type} (K : WitnessedDiff X R) :
    ∀ x, ¬ kernelApart K x x :=
  fun x h => h (K.diag_zero x)

/-- The designated endpoints are metatheoretically distinct. -/
theorem kernel_endpoints_ne {X R : Type} (K : WitnessedDiff X R) : K.a ≠ K.b :=
  fun he => K.apart_ab (by rw [he]; exact K.diag_zero K.b)

/-- Canonical realization: the oriented two-element kernel on Bool. -/
def boolKernel : WitnessedDiff Bool Bool where
  delta := fun x y => (!x) && y
  Zero := fun v => v = false
  a := false
  b := true
  diag_zero := by intro x; cases x <;> rfl
  apart_ab := by decide

/-- Quasi-topological proximity/contact relation on power set. -/
structure ProximitySpace (X : Type) where
  Contact : (X → Prop) → (X → Prop) → Prop
  null_empty : ∀ A B, Contact A B → (∃ x, A x) ∧ (∃ y, B y)
  union_split : ∀ A B D, Contact (fun x => A x ∨ B x) D ↔ (Contact A D ∨ Contact B D)
  overlap_touch : ∀ A B, (∃ x, A x ∧ B x) → Contact A B
  symm : ∀ A B, Contact A B ↔ Contact B A

end GenesisPrimitives.PrimitiveContact
