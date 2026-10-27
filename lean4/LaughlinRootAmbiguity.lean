import Std
namespace LaughlinRootAmbiguity
/-- Residue k denotes the formal angle k*pi/m modulo 2*pi. -/
def monodromy (m k : Nat) : Nat := (2 * k) % (2 * m)

theorem two_distinct_exchange_roots (m : Nat) (hm : 1 < m) :
    1 < 2 * m ∧ m + 1 < 2 * m ∧ 1 ≠ m + 1 ∧
    monodromy m 1 = 2 ∧ monodromy m (m + 1) = 2 := by
  have hsmall : 2 < 2 * m := by omega
  have hform : 2 * (m + 1) = 2 + 2 * m := by omega
  simp only [monodromy, Nat.mul_one, hform, Nat.add_mod_right, Nat.mod_eq_of_lt hsmall]
  exact ⟨by omega, by omega, by omega, trivial, trivial⟩

/-- The full-braid residue does not uniquely select an exchange residue. -/
theorem monodromy_not_injective (m : Nat) (hm : 1 < m) :
    ¬ (∀ a b, a < 2*m → b < 2*m → monodromy m a = monodromy m b → a = b) := by
  intro h
  obtain ⟨h1, h2, hne, ha, hb⟩ := two_distinct_exchange_roots m hm
  exact hne (h 1 (m+1) h1 h2 (ha.trans hb.symm))

theorem roots_at_third_filling :
    monodromy 3 1 = 2 ∧ monodromy 3 4 = 2 ∧ 1 ≠ (4 : Nat) := by decide
end LaughlinRootAmbiguity
#print axioms LaughlinRootAmbiguity.two_distinct_exchange_roots
#print axioms LaughlinRootAmbiguity.monodromy_not_injective
#print axioms LaughlinRootAmbiguity.roots_at_third_filling
