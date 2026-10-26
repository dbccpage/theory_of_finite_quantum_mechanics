import Foundations

namespace Coda

theorem transport_factor {X Y P Q V : Type}
    (p : X → P) (p' : Y → Q) (move : X → Y) (display : P → Q)
    (query : Y → V) (factor : Q → V)
    (square : ∀ x, p' (move x) = display (p x))
    (spec : ∀ y, factor (p' y) = query y) (x : X) :
    factor (display (p x)) = query (move x) := by
  rw [← square x]
  exact spec (move x)

theorem triangle_no_global_section :
    ¬ ∃ a b c : Bool, a = b ∧ b = c ∧ c ≠ a := by
  rintro ⟨a, b, c, hab, hbc, hca⟩
  exact hca (hab.trans hbc).symm

theorem triangle_each_edge_satisfiable :
    (∃ a b : Bool, a = b) ∧ (∃ b c : Bool, b = c) ∧
    (∃ c a : Bool, c ≠ a) := by
  exact ⟨⟨false, false, rfl⟩, ⟨false, false, rfl⟩, ⟨false, true, by decide⟩⟩

def Standing (evidence grant : Prop) : Prop := evidence ∧ grant

theorem standing_requires_grant {evidence grant : Prop}
    (h : Standing evidence grant) : grant := h.2

theorem evidence_does_not_supply_grant : ¬ Standing True False := by
  intro h
  exact h.2

theorem constant_map_not_injective :
    ¬ (∀ a b : Bool, (fun _ : Bool => ()) a = (fun _ : Bool => ()) b → a = b) := by
  intro h
  have impossible := h false true rfl
  cases impossible

end Coda
