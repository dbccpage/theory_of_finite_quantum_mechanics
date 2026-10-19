import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.Field.Rat

/-! AuthorityEffect: None. Finite directed incidence and triangle cancellation.
The Rust map from distinct admitted edge pairs to matrix columns and checked
storage operations requires separate source review. This is no Rust extraction,
allocator totality, graph connectivity/rank or arbitrary triangulation theorem.
-/
namespace TFQM.GraphIncidence

open scoped BigOperators

def point {α : Type*} [DecidableEq α] (v label : α) : ℚ :=
  if v = label then 1 else 0

def incidence {α : Type*} [DecidableEq α] (a b v : α) : ℚ :=
  point v b - point v a

theorem incidence_loop_zero {α : Type*} [DecidableEq α] (a v : α) :
    incidence a a v = 0 := sub_self _

theorem incidence_reverse {α : Type*} [DecidableEq α] (a b v : α) :
    incidence b a v = -incidence a b v := by
  exact (neg_sub (point v b) (point v a)).symm

theorem triangle_cancellation {α : Type*} [DecidableEq α] (a b c v : α) :
    incidence a b v + incidence b c v - incidence a c v = 0 := by
  unfold incidence
  rw [add_comm (point v b - point v a) (point v c - point v b),
    sub_add_sub_cancel, sub_self]

theorem distinct_edge_pairs {α : Type*} (a b c : α) (hab : a ≠ b) (hbc : b ≠ c) :
    (a,b) ≠ (b,c) ∧ (a,b) ≠ (a,c) ∧ (b,c) ≠ (a,c) := by
  exact ⟨fun h => hab (congrArg Prod.fst h),
    fun h => hbc (congrArg Prod.snd h),
    fun h => hab (congrArg Prod.fst h).symm⟩

def triangleRow {E : Type*} [DecidableEq E] (ab bc ac e : E) : ℚ :=
  point e ab + point e bc - point e ac

theorem triangle_at_ab {E : Type*} [DecidableEq E] (ab bc ac : E)
    (hbc : ab ≠ bc) (hac : ab ≠ ac) : triangleRow ab bc ac ab = 1 := by
  simp [triangleRow, point, hbc, hac]

theorem triangle_at_bc {E : Type*} [DecidableEq E] (ab bc ac : E)
    (hab : bc ≠ ab) (hac : bc ≠ ac) : triangleRow ab bc ac bc = 1 := by
  simp [triangleRow, point, hab, hac]

theorem triangle_at_ac {E : Type*} [DecidableEq E] (ab bc ac : E)
    (hab : ac ≠ ab) (hbc : ac ≠ bc) : triangleRow ab bc ac ac = -1 := by
  simp [triangleRow, point, hab, hbc]

theorem row_action {E : Type*} [Fintype E] [DecidableEq E]
    (ab bc ac : E) (f : E → ℚ) :
    ∑ e, triangleRow ab bc ac e * f e = f ab + f bc - f ac := by
  classical
  simp [triangleRow, point, add_mul, sub_mul, ite_mul,
    Finset.sum_add_distrib, Finset.sum_sub_distrib]

theorem row_product_zero {E V : Type*} [Fintype E] [DecidableEq E] [DecidableEq V]
    (ab bc ac : E) (a b c v : V) (d0 : E → V → ℚ)
    (hab : d0 ab v = incidence a b v) (hbc : d0 bc v = incidence b c v)
    (hac : d0 ac v = incidence a c v) :
    ∑ e, triangleRow ab bc ac e * d0 e v = 0 := by
  rw [row_action, hab, hbc, hac, triangle_cancellation]

end TFQM.GraphIncidence

#print axioms TFQM.GraphIncidence.incidence_loop_zero
#print axioms TFQM.GraphIncidence.incidence_reverse
#print axioms TFQM.GraphIncidence.triangle_cancellation
#print axioms TFQM.GraphIncidence.distinct_edge_pairs
#print axioms TFQM.GraphIncidence.triangle_at_ab
#print axioms TFQM.GraphIncidence.triangle_at_bc
#print axioms TFQM.GraphIncidence.triangle_at_ac
#print axioms TFQM.GraphIncidence.row_action
#print axioms TFQM.GraphIncidence.row_product_zero
