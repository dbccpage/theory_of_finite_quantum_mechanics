import CabelloVertexData

/- Kernel check of the actual listed integer frame/tomography/negative witnesses.
   This is not a formal proof that the list is the full real frame polytope's
   vertex set. Native exhaustive-basis completeness is checked independently.
   Origin: FQ-CABELLO-FRAME-POLYTOPE-146. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptCabelloCensus
open CabelloVertexData

def quadratic (h v : List Int) : Int :=
  ((List.range 4).map fun i =>
    ((List.range 4).map fun j => v.getD i 0 * h.getD (4*i+j) 0 * v.getD j 0).sum).sum

def normSq (v : List Int) : Int := (v.map fun x => x*x).sum

def rowPredicate (k : Nat) : Prop :=
  let h := matrixData.getD k []
  let v := vectorData.getD k []
  let w := weightsData.getD k []
  let d := denominatorData.getD k 0
  quadratic h v < 0 ∧
  h.length = 16 ∧ v.length = 4 ∧ w.length = 18 ∧ 0 < d ∧
  quadratic h v = negativeData.getD k 0 ∧
  h.getD 0 0 + h.getD 5 0 + h.getD 10 0 + h.getD 15 0 = (d : Int) ∧
  (∀ i ∈ List.range 18, 0 ≤ w.getD i 0 ∧ w.getD i 0 ≤ 2) ∧
  (∀ f ∈ contextsData, (f.map fun r => w.getD r 0).sum = 2) ∧
  (∀ i ∈ List.range 18,
    2 * quadratic h (raysData.getD i []) =
      (d : Int) * normSq (raysData.getD i []) * w.getD i 0)

instance (k : Nat) : Decidable (rowPredicate k) := by
  unfold rowPredicate
  infer_instance

def rowCheck (k : Nat) : Bool := decide (rowPredicate k)

set_option maxHeartbeats 10000000 in
set_option maxRecDepth 20000 in
theorem listed_count_and_distinct :
    weightsData.length = 146 ∧ matrixData.length = 146 ∧ denominatorData.length = 146 ∧
    vectorData.length = 146 ∧ negativeData.length = 146 ∧ weightsData.eraseDups.length = 146 := by
  decide

set_option maxHeartbeats 20000000 in
set_option maxRecDepth 20000 in
theorem all_integer_frame_and_negative_certificates :
    (List.range 146).all rowCheck = true := by
  decide

theorem each_listed_certificate (k : Fin 146) : rowPredicate k.val := by
  have h := (List.all_eq_true.mp all_integer_frame_and_negative_certificates)
    k.val (List.mem_range.mpr k.isLt)
  exact of_decide_eq_true h

theorem every_listed_negative (k : Fin 146) :
    quadratic (matrixData.getD k.val []) (vectorData.getD k.val []) < 0 :=
  (each_listed_certificate k).1

end QuantumMechanics.PromptCabelloCensus
#print axioms QuantumMechanics.PromptCabelloCensus.listed_count_and_distinct
#print axioms QuantumMechanics.PromptCabelloCensus.all_integer_frame_and_negative_certificates
#print axioms QuantumMechanics.PromptCabelloCensus.each_listed_certificate
#print axioms QuantumMechanics.PromptCabelloCensus.every_listed_negative
