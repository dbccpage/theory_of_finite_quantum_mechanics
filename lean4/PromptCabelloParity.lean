import GleasonCyclotomicObstruction

/- Literal universal integer parity and the measured-ray/non-PSD countermodel.
   Normalized rational arrays are checked separately by native exact predicates.
   Origin: FQ-CABELLO-NO-INTEGER-FRAME. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptCabelloParity
open HilbertWalk.GleasonCyclotomicObstruction

theorem odd_context_total_not_twice_integer (k : Int) : (9 : Int) ≠ 2*k := by omega

theorem no_integer_frame_assignment (f : Vec4 → Int)
    (h0 : f v2 + f v9 + f v15 + f v17 = 1)
    (h1 : f v4 + f v7 + f v13 + f v17 = 1)
    (h2 : f v5 + f v6 + f v13 + f v15 = 1)
    (h3 : f v0 + f v3 + f v9 + f v16 = 1)
    (h4 : f v0 + f v6 + f v10 + f v14 = 1)
    (h5 : f v1 + f v5 + f v11 + f v14 = 1)
    (h6 : f v1 + f v7 + f v8 + f v12 = 1)
    (h7 : f v2 + f v8 + f v11 + f v16 = 1)
    (h8 : f v3 + f v4 + f v10 + f v12 = 1) : False :=
  cabello_no_integer_frame_assignment f h0 h1 h2 h3 h4 h5 h6 h7 h8

theorem all_measured_checks_do_not_force_psd :
    cabello18.all (fun v => decide (0 < norm_sq4 v ∧
      0 ≤ quad_form M_bad v ∧ quad_form M_bad v ≤ 2 * norm_sq4 v)) = true ∧
    cabello_contexts.all (fun c =>
      (c.map scaled_ratio_4).foldl (· + ·) 0 == (8 : Int)) = true ∧
    quad_form M_bad w_witness < 0 := all_cabello_checks_do_not_certify_psd

theorem scaled_readouts_have_no_integer_rounding :
    cabello18.all (fun v => decide ((4 * quad_form M_bad v) % norm_sq4 v = 0)) = true := by
  decide

def rawTrace : Int := M_bad.m00 + M_bad.m11 + M_bad.m22 + M_bad.m33

theorem positive_normalization_scale_and_negative_numerator :
    rawTrace = 2 ∧ 0 < rawTrace ∧ quad_form M_bad w_witness = -2 := by decide

end QuantumMechanics.PromptCabelloParity
#print axioms QuantumMechanics.PromptCabelloParity.odd_context_total_not_twice_integer
#print axioms QuantumMechanics.PromptCabelloParity.no_integer_frame_assignment
#print axioms QuantumMechanics.PromptCabelloParity.all_measured_checks_do_not_force_psd
#print axioms QuantumMechanics.PromptCabelloParity.scaled_readouts_have_no_integer_rounding
#print axioms QuantumMechanics.PromptCabelloParity.positive_normalization_scale_and_negative_numerator
