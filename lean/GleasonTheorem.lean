-- Integer quadratic frame identities; NOT a proof of Gleason's theorem.
-- AuthorityEffect: None

namespace GleasonTheorem

/-- Integer coefficients and a declared denominator for a quadratic form:
    Q(x, y) = a * x^2 + 2 b * x * y + c * y^2
    induced by a symmetric matrix with unit trace condition a + c = denom. -/
structure QuadraticFrameFunction2 where
  a : Int
  b : Int
  c : Int
  denom : Nat
  h_denom_pos : denom > 0
  h_unit_trace : a + c = (denom : Int)

/-- Evaluation of the quadratic form on a 2D vector (x, y):
    Q(x, y) = a * x^2 + 2 b * x * y + c * y^2. -/
def eval_quad (q : QuadraticFrameFunction2) (x y : Int) : Int :=
  q.a * (x * x) + 2 * q.b * (x * y) + q.c * (y * y)

/-- Quadratic frame identity in d = 2:
    For any quadratic form Q and any orthogonal pair (ux, uy) and (-uy, ux),
    the sum Q(u) + Q(u_perp) equals (a + c) * ||u||^2. -/
theorem quad_frame_sum (q : QuadraticFrameFunction2) (ux uy : Int) :
    eval_quad q ux uy + eval_quad q (-uy) ux = (q.a + q.c) * (ux * ux + uy * uy) := by
  dsimp [eval_quad]
  have h1 : (-uy) * (-uy) = uy * uy := by simp [Int.neg_mul_neg]
  have h2 : (-uy) * ux = -(ux * uy) := by
    have hcomm : uy * ux = ux * uy := Int.mul_comm uy ux
    have hneg : -uy * ux = -(uy * ux) := (Int.neg_mul_eq_neg_mul uy ux).symm
    rw [hneg, hcomm]
  rw [h1, h2]
  have h_cross : 2 * q.b * (-(ux * uy)) = -(2 * q.b * (ux * uy)) := Int.mul_neg (2 * q.b) (ux * uy)
  rw [h_cross]
  have h_dist_a : q.a * (ux * ux) + q.a * (uy * uy) = q.a * (ux * ux + uy * uy) := by
    rw [Int.mul_add]
  have h_dist_c : q.c * (uy * uy) + q.c * (ux * ux) = q.c * (ux * ux + uy * uy) := by
    have h_factor : q.c * (uy * uy) + q.c * (ux * ux) = q.c * (uy * uy + ux * ux) := (Int.mul_add q.c (uy * uy) (ux * ux)).symm
    have hcomm_u : uy * uy + ux * ux = ux * ux + uy * uy := by omega
    rw [h_factor, hcomm_u]
  have h_lin : q.a * (ux * ux) + 2 * q.b * (ux * uy) + q.c * (uy * uy) +
               (q.a * (uy * uy) + -(2 * q.b * (ux * uy)) + q.c * (ux * ux)) =
               (q.a * (ux * ux) + q.a * (uy * uy)) + (q.c * (uy * uy) + q.c * (ux * ux)) := by omega
  rw [h_lin, h_dist_a, h_dist_c]
  exact (Int.add_mul q.a q.c (ux * ux + uy * uy)).symm

/-- Normalized Frame Sum:
    When evaluated on an orthonormal frame with ||u||^2 = denom,
    the sum Q(u) + Q(v) = denom * denom (total probability 1.0 when divided by denom^2). -/
theorem frame_sum_on_unit_frame (q : QuadraticFrameFunction2) (ux uy : Int)
    (h_norm : ux * ux + uy * uy = (q.denom : Int)) :
    eval_quad q ux uy + eval_quad q (-uy) ux = (q.denom : Int) * (q.denom : Int) := by
  rw [quad_frame_sum, q.h_unit_trace, h_norm]

/-- With INTEGER cross coefficient b, the diagonal value 1 + 2b is odd.
    This does not construct a binary frame function or rule out real/rational
    quadratic coefficients (b = 1/2 would give value 2). Historical name retained;
    neither dimension-two non-Born existence nor general Gleason follows. -/
theorem d2_binary_non_bornian_obstruction (q : QuadraticFrameFunction2)
    (_h_denom_one : q.denom = 1)
    (h_e0 : eval_quad q 1 0 = 1)
    (h_e1 : eval_quad q 0 1 = 0) :
    eval_quad q 1 1 ≠ 0 ∧ eval_quad q 1 1 ≠ 2 := by
  dsimp [eval_quad] at h_e0 h_e1 ⊢
  have ha : q.a = 1 := by omega
  have hc : q.c = 0 := by omega
  rw [ha, hc]
  constructor
  · intro hz
    omega
  · intro ht
    omega

#print axioms quad_frame_sum
#print axioms frame_sum_on_unit_frame
#print axioms d2_binary_non_bornian_obstruction

end GleasonTheorem
