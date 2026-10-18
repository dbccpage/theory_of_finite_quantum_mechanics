import Std

/-! Exact monomial pairing for all balanced row masks of the six-phase
Szöllősi block form. AuthorityEffect: None.
The lift from signed Laurent monomials to matrix entries is given in the
companion execution report and replayed by verify_symbolic.py. -/

namespace MUB.SzollosiLaurentPairing

def maskSign (m : Fin 64) (r : Fin 6) : Int :=
  if m.val / 2^r.val % 2 = 1 then 1 else -1

def positiveCount (m : Fin 64) : Nat :=
  (List.finRange 6).countP fun r => maskSign m r = 1

def entryExponent (r c k : Fin 6) : Int :=
  if r.val < 3 then
    if c.val < 3 then
      if k.val = (c.val + 3 - r.val) % 3 then 1 else 0
    else
      if k.val = 3 + (c.val + 3 - r.val) % 3 then 1 else 0
  else
    if c.val < 3 then
      if k.val = 3 + (r.val + 3 - c.val) % 3 then -1 else 0
    else
      if k.val = (r.val + 3 - c.val) % 3 then -1 else 0

def columnExponent (m : Fin 64) (c k : Fin 6) : Int :=
  ((List.finRange 6).map fun r => maskSign m r * entryExponent r c k).sum

def leftColumn (c : Fin 3) : Fin 6 := ⟨c.val, by omega⟩

def rightColumn (p : Fin 6) (c : Fin 3) : Fin 6 :=
  match p.val, c.val with
  | 0, 0 => 3
  | 0, 1 => 4
  | 0, 2 => 5
  | 1, 0 => 3
  | 1, 1 => 5
  | 1, 2 => 4
  | 2, 0 => 4
  | 2, 1 => 3
  | 2, 2 => 5
  | 3, 0 => 4
  | 3, 1 => 5
  | 3, 2 => 3
  | 4, 0 => 5
  | 4, 1 => 3
  | 4, 2 => 4
  | 5, 0 => 5
  | 5, 1 => 4
  | 5, 2 => 3
  | _, _ => 3

def pairing (m : Fin 64) : Fin 6 :=
  match m.val with
  | 7 => 0
  | 11 => 5
  | 19 => 1
  | 35 => 2
  | 13 => 2
  | 21 => 5
  | 37 => 1
  | 25 => 5
  | 41 => 2
  | 49 => 1
  | 14 => 1
  | 22 => 2
  | 38 => 5
  | 26 => 1
  | 42 => 5
  | 50 => 2
  | 28 => 2
  | 44 => 1
  | 52 => 5
  | 56 => 0
  | _ => 0

set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
theorem balanced_monomial_pairing :
    ∀ m : Fin 64, positiveCount m = 3 →
      (Function.Injective (rightColumn (pairing m))) ∧
      (∀ c : Fin 3, ∀ k : Fin 6,
        columnExponent m (leftColumn c) k =
          columnExponent m (rightColumn (pairing m) c) k) := by
  unfold Function.Injective
  decide

def bottomExponent (m : Fin 64) : Int :=
  maskSign m 3 + maskSign m 4 + maskSign m 5

theorem bottom_exponent_odd : ∀ m : Fin 64, bottomExponent m % 2 = 1 := by
  decide

theorem balanced_mask_count :
    ((List.finRange 64).filter fun m => positiveCount m = 3).length = 20 := by
  decide

/-- The zero factor is uniform when the two row permutations are independent. -/
theorem uniform_orientation {I J : Type} (P : I → Prop) (Q : J → Prop)
    (h : ∀ i j, P i ∨ Q j) : (∀ i, P i) ∨ (∀ j, Q j) := by
  classical
  by_cases hp : ∀ i, P i
  · exact Or.inl hp
  · right
    intro j
    apply Classical.byContradiction
    intro hq
    apply hp
    intro i
    exact (h i j).resolve_right hq

#print axioms balanced_monomial_pairing
#print axioms bottom_exponent_odd
#print axioms balanced_mask_count
#print axioms uniform_orientation

end MUB.SzollosiLaurentPairing
