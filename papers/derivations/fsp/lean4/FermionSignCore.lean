

namespace FermionSignTower

universe u v

structure Setting where
  X : Type u
  r : X → X → Prop
  irrefl : ∀ x, ¬ r x x

theorem irrefl_distinct {X : Type u} {r : X → X → Prop} (hirr : ∀ x, ¬ r x x) {a b : X} (hwit : r a b) : a ≠ b :=
  fun heq => hirr a (heq ▸ hwit)

def D2 : Bool → Bool → Prop
  | false, true => True
  | _, _ => False

instance (x y : Bool) : Decidable (D2 x y) := by
  cases x <;> cases y <;> (dsimp [D2]; infer_instance)

theorem D2_irrefl : ∀ x : Bool, ¬ D2 x x := by
  intro x
  cases x <;> (intro h; exact h)

theorem D2_witness : D2 false true :=
  trivial

theorem D2_endpoints_distinct : (false : Bool) ≠ true := by
  intro h
  nomatch h

def swap (b : Bool) : Bool := !b

theorem swap_involutive (b : Bool) : swap (swap b) = b := by
  cases b <;> rfl

def D2_rev (x y : Bool) : Prop := D2 (swap x) (swap y)

instance (x y : Bool) : Decidable (D2_rev x y) := by
  dsimp [D2_rev]
  infer_instance

theorem D2_rev_spec : D2_rev true false :=
  trivial

def IsSwapInvariant (P : (Bool → Bool → Prop) → Prop) : Prop :=
  ∀ R : Bool → Bool → Prop, P R ↔ P (fun x y => R (swap x) (swap y))

theorem swap_invariant_blind
    (P : (Bool → Bool → Prop) → Prop)
    (hinv : IsSwapInvariant P) :
    P D2 ↔ P D2_rev := by
  have h := hinv D2
  exact h

def S2 (x y : Bool) : Prop := D2 x y ∨ D2 y x

instance (x y : Bool) : Decidable (S2 x y) := by
  dsimp [S2]
  infer_instance

theorem S2_symmetric (x y : Bool) : S2 x y ↔ S2 y x := by
  dsimp [S2]
  exact Or.comm

theorem S2_swap_invariant (x y : Bool) : S2 (swap x) (swap y) ↔ S2 x y := by
  cases x <;> cases y <;> decide

structure SignGapPacket where
  num_paths : Nat
  gross_l1_weight : Nat
  net_signed_sum : Int
  involution_paired : Bool
  cancellation_sound : involution_paired = true → net_signed_sum = 0

def exactMeronCancellationPacket : SignGapPacket where
  num_paths := 2
  gross_l1_weight := 2
  net_signed_sum := 0
  involution_paired := true
  cancellation_sound := fun _ => rfl

def ZeroRel (X : Type u) (δ : X → X → Int) (x y : X) : Prop :=
  δ x y = 0

theorem zeroRel_equiv (X : Type u) (δ : X → X → Int)
    (hrefl : ∀ x, δ x x = 0)
    (hsymm : ∀ x y, δ x y = 0 → δ y x = 0)
    (htrans : ∀ x y z, δ x y = 0 → δ y z = 0 → δ x z = 0) :
    Equivalence (ZeroRel X δ) where
  refl := hrefl
  symm := hsymm _ _
  trans := htrans _ _ _

end FermionSignTower
