import Std

/- A representation-class-specific sign obstruction for a three-cycle.
No spin bordism group, eta invariant or bulk theory is computed. -/
namespace SignedTriangleSwitching

structure Signs where
  edge01 : Bool
  edge12 : Bool
  edge20 : Bool
  deriving DecidableEq, Repr

def parity (s : Signs) : Bool := Bool.xor (Bool.xor s.edge01 s.edge12) s.edge20

def switched (g0 g1 g2 : Bool) (s : Signs) : Signs :=
  ⟨Bool.xor (Bool.xor g0 s.edge01) g1,
   Bool.xor (Bool.xor g1 s.edge12) g2,
   Bool.xor (Bool.xor g2 s.edge20) g0⟩

def positive : Signs := ⟨false, false, false⟩

def sign (b : Bool) : Int := if b then -1 else 1

theorem parity_invariant (g0 g1 g2 : Bool) (s : Signs) :
    parity (switched g0 g1 g2 s) = parity s := by
  rcases s with ⟨a, b, c⟩
  cases g0 <;> cases g1 <;> cases g2 <;> cases a <;> cases b <;> cases c <;> rfl

theorem switching_normal_form (s : Signs) :
    switched false s.edge01 (Bool.xor s.edge01 s.edge12) s =
      ⟨false, false, parity s⟩ := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> rfl

theorem positive_switching_iff (s : Signs) :
    (∃ g0 g1 g2, switched g0 g1 g2 s = positive) ↔ parity s = false := by
  constructor
  · rintro ⟨g0, g1, g2, h⟩
    have e := parity_invariant g0 g1 g2 s
    rw [h] at e
    exact e.symm
  · intro h
    refine ⟨false, s.edge01, Bool.xor s.edge01 s.edge12, ?_⟩
    rw [switching_normal_form, h]
    rfl

theorem negative_cycle_obstruction (s : Signs) (h : parity s = true) :
    ¬ ∃ g0 g1 g2, switched g0 g1 g2 s = positive := by
  intro possible
  have e := (positive_switching_iff s).mp possible
  rw [h] at e
  cases e

theorem edge_product_is_cycle_sign (s : Signs) :
    sign s.edge01 * sign s.edge12 * sign s.edge20 = sign (parity s) := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> decide

theorem explicit_negative_cycle :
    ¬ ∃ g0 g1 g2, switched g0 g1 g2 ⟨true, false, false⟩ = positive :=
  negative_cycle_obstruction _ rfl

theorem balanced_negative_edges_are_removable :
    switched false true false ⟨true, true, false⟩ = positive := by decide

#print axioms parity_invariant
#print axioms switching_normal_form
#print axioms positive_switching_iff
#print axioms negative_cycle_obstruction
#print axioms edge_product_is_cycle_sign
#print axioms explicit_negative_cycle
#print axioms balanced_negative_edges_are_removable
end SignedTriangleSwitching
