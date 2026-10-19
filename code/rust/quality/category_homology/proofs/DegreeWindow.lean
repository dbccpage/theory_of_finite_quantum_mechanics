import Mathlib.Data.Int.Basic

/-!
AuthorityEffect: None. Degree-window arithmetic model over the exact declared
i32 range. The span is upper-lower, not the number of inclusive degree points.
Rust abs_diff and its representation correspondence remain a source/runtime
review boundary; this file does not verify Rust or a category of complexes.
-/

namespace TFQM.DegreeWindow

theorem ordered_span_fits_u32 (lower upper : Int)
    (lower_bound : -2147483648 ≤ lower) (upper_bound : upper ≤ 2147483647)
    (ordered : lower ≤ upper) :
    0 ≤ upper - lower ∧ upper - lower ≤ 4294967295 := by
  omega

theorem same_endpoint_zero (degree : Int) : degree - degree = 0 := by
  omega

theorem inverted_span_negative (lower upper : Int) (inverted : upper < lower) :
    upper - lower < 0 := by
  omega

#print axioms ordered_span_fits_u32
#print axioms same_endpoint_zero
#print axioms inverted_span_negative

end TFQM.DegreeWindow
