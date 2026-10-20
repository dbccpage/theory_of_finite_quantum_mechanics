import TensorCoordinates
import TensorOperationalCone

open Matrix Module
open scoped BigOperators Kronecker ComplexOrder
noncomputable section
namespace TensorComposition
open TensorTomography TensorConeReconstruction TensorOperationalCone TensorReachability

variable {V : Type*} [AddCommGroup V] [Module ℝ V]
variable {n m : ℕ}

def representation (D : TomographicData (Fin n) (Fin m) V) :
    V ≃ₗ[ℝ] Herm (Fin n × Fin m) :=
  tomographicEquiv (Module.finBasis ℝ (Herm (Fin n))) (Module.finBasis ℝ (Herm (Fin m))) D

theorem representation_prepare (D : TomographicData (Fin n) (Fin m) V)
    (A : Herm (Fin n)) (B : Herm (Fin m)) :
    representation D (D.prepare A B) = product A B := tomographicEquiv_prepare _ _ D A B

theorem representation_test (D : TomographicData (Fin n) (Fin m) V)
    (E : Herm (Fin n)) (F : Herm (Fin m)) (x : V) :
    pairing (product E F) (representation D x) = D.test E F x :=
  tomographicEquiv_test _ _ D E F x

def hermRankOne {d : Type*} (v : d → ℂ) : Herm d :=
  ⟨rankOne v, by change (rankOne v)ᴴ = _; simp [rankOne, conjTranspose_vecMulVec]⟩

theorem product_rankOne (a : Fin n → ℂ) (b : Fin m → ℂ) :
    product (hermRankOne a) (hermRankOne b) = hermRankOne (productVector a b) := by
  apply Subtype.ext
  ext i j
  simp [product, hermRankOne, rankOne, Matrix.vecMulVec_apply, productVector,
    mul_comm, mul_left_comm, mul_assoc]

theorem trace_rankOne {d : Type*} [Fintype d] (v : d → ℂ) (A : Matrix d d ℂ) :
    (rankOne v * A).trace = quadratic A v := by
  rw [rankOne, vecMulVec_mul, trace_vecMulVec, dotProduct_comm, ← dotProduct_mulVec]
  rfl

theorem quadratic_nonneg_of_pairing {d : Type*} [Fintype d] (H : Herm d) (v : d → ℂ)
    (h : 0 ≤ pairing (hermRankOne v) H) : 0 ≤ quadratic H.val v := by
  rw [Complex.nonneg_iff]
  constructor
  · simpa only [pairing_apply, hermRankOne, trace_rankOne] using h
  · have him := trace_pair_im (hermRankOne v) H
    simpa only [hermRankOne, trace_rankOne] using him.symm

/-- Preservation stated on the operational carrier. Calibration can establish
these equations by `product_calibration`; no composite cone is preselected. -/
def Preserves (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (U : Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ) : Prop :=
  ∀ x ∈ K, ∃ y ∈ K, (representation D y).val = conjugate U (representation D x).val

/-- The complete state-cone theorem combines constructed tomography coordinates,
proved Schmidt reachability, and the general cone kernel. Operational premises
are explicit; there is no reachability, joint-dimension, or PSD-cone premise. -/
theorem quantum_state_cone [NeZero m] (hnm : n ≤ m)
    (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hz : 0 ∈ K) (ha : ∀ x ∈ K, ∀ y ∈ K, x + y ∈ K)
    (hprep : ∀ a b, D.prepare (hermRankOne a) (hermRankOne b) ∈ K)
    (hprob : ∀ x ∈ K, ∀ a b, 0 ≤ D.test (hermRankOne a) (hermRankOne b) x)
    (hlocal : ∀ (U : Matrix.unitaryGroup (Fin n) ℂ) (W : Matrix.unitaryGroup (Fin m) ℂ),
      Preserves D K (U.val ⊗ₖ W.val))
    (hshift : Preserves D K (controlledShift hnm).val)
    (hunshift : Preserves D K (controlledShift hnm).valᴴ) :
    (fun x => (representation D x).val) '' K = {A | A.PosSemidef} := by
  let K' : Set (Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ) :=
    (fun x => (representation D x).val) '' K
  have hp (U : Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ) (h : Preserves D K U) :
      ∀ A ∈ K', conjugate U A ∈ K' := by
    rintro A ⟨x,hx,rfl⟩
    obtain ⟨y,hy,he⟩ := h x hx
    exact ⟨y,hy,he⟩
  apply controlled_shift_selects_positive hnm K'
  · exact ⟨0,hz,by simp⟩
  · rintro A ⟨x,hx,rfl⟩ B ⟨y,hy,rfl⟩
    exact ⟨x+y,ha x hx y hy,by simp⟩
  · rintro A ⟨x,hx,rfl⟩
    exact (representation D x).property
  · intro a b
    refine ⟨D.prepare (hermRankOne a) (hermRankOne b),hprep a b,?_⟩
    change (representation D (D.prepare (hermRankOne a) (hermRankOne b))).val = _
    rw [representation_prepare, product_rankOne]
    rfl
  · rintro A ⟨x,hx,rfl⟩ a b
    apply quadratic_nonneg_of_pairing
    rw [← product_rankOne, representation_test]
    exact hprob x hx a b
  · intro U W; exact hp _ (hlocal U W)
  · exact hp _ hshift
  · exact hp _ hunshift

/-- The deterministic product test becomes trace normalization. -/
theorem unit_test_is_trace (D : TomographicData (Fin n) (Fin m) V) (x : V) :
    D.test (1 : Herm (Fin n)) (1 : Herm (Fin m)) x = (representation D x).val.trace.re := by
  rw [← representation_test]
  simp [pairing_apply, product]

#print axioms quantum_state_cone
#print axioms unit_test_is_trace
end TensorComposition
