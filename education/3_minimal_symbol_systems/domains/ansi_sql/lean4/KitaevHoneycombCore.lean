/-! Finite scalar sign identities. No Hamiltonian or braid theorem. -/
namespace KitaevHoneycombCore
def is_valid_gauge_link (u : Int) : Prop := u = 1 ∨ u = -1
theorem gauge_link_square (u : Int) (h : is_valid_gauge_link u) : u * u = 1 := by
  rcases h with rfl | rfl <;> rfl
theorem scalar_link_values_commute (u v : Int) : u * v = v * u := Int.mul_comm u v
end KitaevHoneycombCore
