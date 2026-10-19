import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Reversal of literal boundary records only.
This does not construct or prove an opposite category or a functor.
The Rust Vec/String representation correspondence is source reviewed.
-/
namespace TFQM.LiteralReversal

structure Triple where
  source : String
  target : String
  name : String
  deriving DecidableEq

def reverse (triple : Triple) : Triple :=
  ⟨triple.target, triple.source, triple.name⟩

theorem reverse_involution (triple : Triple) : reverse (reverse triple) = triple := by
  cases triple
  rfl

theorem list_involution (triples : List Triple) :
    (triples.map reverse).map reverse = triples := by
  induction triples with
  | nil => rfl
  | cons triple rest ih => simp [reverse_involution, ih]

theorem length_preserved (triples : List Triple) :
    (triples.map reverse).length = triples.length := by
  exact List.length_map

theorem names_and_order_preserved (triples : List Triple) :
    (triples.map reverse).map Triple.name = triples.map Triple.name := by
  induction triples with
  | nil => rfl
  | cons triple rest ih => simp [reverse, ih]

#print axioms reverse_involution
#print axioms list_involution
#print axioms length_preserved
#print axioms names_and_order_preserved

end TFQM.LiteralReversal
