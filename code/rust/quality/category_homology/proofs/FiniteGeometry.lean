import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-! AuthorityEffect: None. Exact affine-line existence/uniqueness over a field,
the concrete Fano table, equal-width integer dot products, and admission/index
facts. Source correspondence, all refusal cases and checked-i64 prefixes are
separate review obligations. No extracted Rust or allocator theorem. -/
namespace TFQM.FiniteGeometry

variable {K : Type*} [Field K]

theorem slope_exists (x1 x2 y1 y2 : K) (hx : x2 ≠ x1) :
    ∃ m c : K, m*x1+c=y1 ∧ m*x2+c=y2 := by
  refine ⟨(y2-y1)/(x2-x1), y1-((y2-y1)/(x2-x1))*x1, ?_, ?_⟩
  · ring
  · have hm := div_mul_cancel₀ (y2-y1) (sub_ne_zero.mpr hx)
    calc
      (y2-y1)/(x2-x1)*x2+(y1-(y2-y1)/(x2-x1)*x1) =
          ((y2-y1)/(x2-x1))*(x2-x1)+y1 := by ring
      _ = y2 := by rw [hm]; ring

theorem slope_unique (x1 x2 m c m' c' : K) (hx : x2 ≠ x1)
    (h1 : m*x1+c=m'*x1+c') (h2 : m*x2+c=m'*x2+c') : m=m' ∧ c=c' := by
  have h : m*(x2-x1)=m'*(x2-x1) := by
    calc
      m*(x2-x1) = (m*x2+c)-(m*x1+c) := by ring
      _ = (m'*x2+c')-(m'*x1+c') := by rw [h1, h2]
      _ = m'*(x2-x1) := by ring
  have hm : m=m' := mul_right_cancel₀ (sub_ne_zero.mpr hx) h
  constructor
  · exact hm
  · rw [hm] at h1
    exact add_left_cancel h1

theorem same_x_excludes_slope (x y1 y2 m c : K) (hy : y1 ≠ y2)
    (h1 : m*x+c=y1) : m*x+c ≠ y2 := by
  intro h2
  exact hy (h1.symm.trans h2)

def fanoLines : List (List Nat) :=
  [[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]]

theorem fano_unique : ∀ p q : Fin 7, p ≠ q →
    (fanoLines.filter (fun l => decide (p.val ∈ l ∧ q.val ∈ l))).length = 1 := by
  decide

def dot : List Int → List Int → Int
  | [], _ => 0
  | _, [] => 0
  | a::as, b::bs => a*b + dot as bs

theorem dot_symmetric (a b : List Int) : dot a b = dot b a := by
  induction a generalizing b with
  | nil => cases b <;> rfl
  | cons a as ih =>
    cases b with
    | nil => rfl
    | cons b bs => simp [dot, ih, Int.mul_comm]

theorem equal_width_tails (a b : Int) (as bs : List Int)
    (h : (a::as).length = (b::bs).length) : as.length = bs.length := by simpa using h

theorem dot_cons (a b : Int) (as bs : List Int) : dot (a::as) (b::bs) = a*b+dot as bs := rfl

def edge (rows : Nat → List Int) (i j : Nat) : Prop := i ≠ j ∧ dot (rows i) (rows j)=0

theorem adjacency_symmetric (rows : Nat → List Int) (i j : Nat) : edge rows i j ↔ edge rows j i := by
  simp only [edge, dot_symmetric (rows i) (rows j), ne_comm]

theorem diagonal_false (rows : Nat → List Int) (i : Nat) : ¬edge rows i i := by simp [edge]

def admitProduct (a b maximum : Nat) : Bool := decide (a*b ≤ maximum)

theorem product_admission (a b maximum : Nat) : admitProduct a b maximum = true ↔ a*b ≤ maximum := by simp [admitProduct]

theorem ray_pair_bound (n : Nat) : n*(n-1)/2 ≤ n*n := by
  exact Nat.le_trans (Nat.div_le_self _ _) (Nat.mul_le_mul_left n (Nat.sub_le n 1))

theorem point_successor_safe (p n : Nat) (h : p < n) : p+1 ≤ n := by omega

theorem affine_encoding_bound (p x y : Nat) (hx : x<p) (hy : y<p) : x*p+y < p*p := by
  calc
    x*p+y < x*p+p := Nat.add_lt_add_left hy _
    _ = (x+1)*p := by ring
    _ ≤ p*p := Nat.mul_le_mul_right p (by omega)

#print axioms slope_exists
#print axioms slope_unique
#print axioms same_x_excludes_slope
#print axioms fano_unique
#print axioms dot_symmetric
#print axioms equal_width_tails
#print axioms dot_cons
#print axioms adjacency_symmetric
#print axioms diagonal_false
#print axioms product_admission
#print axioms ray_pair_bound
#print axioms point_successor_safe
#print axioms affine_encoding_bound
end TFQM.FiniteGeometry
