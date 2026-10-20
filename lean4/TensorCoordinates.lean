import TensorTomography

open Matrix Module
open scoped BigOperators
noncomputable section
namespace TensorTomography

variable {n m ι κ : Type*} [Fintype n] [Fintype m] [Fintype ι] [Fintype κ]
  [DecidableEq ι] [DecidableEq κ]

def dual (a : Basis ι ℝ (Herm n)) : Basis ι ℝ (Herm n) :=
  LinearMap.BilinForm.dualBasis pairing pairing_nondegenerate a

theorem dual_pair (a : Basis ι ℝ (Herm n)) (i j : ι) :
    pairing (dual a i) (a j) = if j = i then 1 else 0 :=
  LinearMap.BilinForm.apply_dualBasis_left _ _ _ _

theorem dual_coord (a : Basis ι ℝ (Herm n)) (A : Herm n) (i : ι) :
    pairing (dual a i) A = a.repr A i := by
  conv_lhs => rw [← a.sum_repr A]
  simp only [map_sum, map_smul, dual_pair, smul_eq_mul, mul_ite, mul_one, mul_zero]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true]

def frame (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m)) (i : ι × κ) :
    Herm (n × m) := product (a i.1) (b i.2)

def frameTest (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m)) (i : ι × κ) :
    Herm (n × m) →ₗ[ℝ] ℝ := pairing (product (dual a i.1) (dual b i.2))

theorem frame_delta (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m)) (i j : ι × κ) :
    frameTest a b i (frame a b j) = if j = i then 1 else 0 := by
  simp only [frameTest, frame, pairing_product, dual_pair]
  split_ifs <;> simp_all [Prod.ext_iff]

def frameProjection (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m)) :
    Herm (n × m) →ₗ[ℝ] Herm (n × m) :=
  ∑ i, (frameTest a b i).smulRight (frame a b i)

theorem frameProjection_product (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m))
    (A : Herm n) (B : Herm m) : frameProjection a b (product A B) = product A B := by
  simp only [frameProjection, LinearMap.sum_apply, LinearMap.smulRight_apply]
  change (∑ i : ι × κ, pairing (product (dual a i.1) (dual b i.2)) (product A B) •
    product (a i.1) (b i.2)) = _
  simp only [pairing_product, dual_coord, Fintype.sum_prod_type]
  conv_rhs => rw [← a.sum_repr A, ← b.sum_repr B]
  change _ = productMap (∑ i, a.repr A i • a i) (∑ j, b.repr B j • b j)
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply, mul_smul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  exact smul_comm _ _ _

theorem frame_expansion (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m))
    (H : Herm (n × m)) : ∑ i, frameTest a b i H • frame a b i = H := by
  have h : H ∈ Submodule.span ℝ (Set.range (fun p : Herm n × Herm m => product p.1 p.2)) := by
    rw [product_span]; trivial
  suffices frameProjection a b H = H by simpa [frameProjection] using this
  induction h using Submodule.span_induction with
  | mem x hx => obtain ⟨⟨A,B⟩,rfl⟩ := hx; exact frameProjection_product a b A B
  | zero => exact map_zero _
  | add x y hx hy h1 h2 => rw [map_add, h1, h2]
  | smul r x hx h => rw [map_smul, h]

section Reconstruction
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- Operational data: independent bilinear preparations and tests, product
factorization, and local tomography. No joint dimension or cone is assumed. -/
structure TomographicData (n m V : Type*) [Fintype n] [Fintype m]
    [AddCommGroup V] [Module ℝ V] where
  prepare : Herm n →ₗ[ℝ] Herm m →ₗ[ℝ] V
  test : Herm n →ₗ[ℝ] Herm m →ₗ[ℝ] V →ₗ[ℝ] ℝ
  factor : ∀ E F A B, test E F (prepare A B) = pairing E A * pairing F B
  tomography : ∀ x y, (∀ E F, test E F x = test E F y) → x = y

variable (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m)) (D : TomographicData n m V)

def coordinates : V →ₗ[ℝ] Herm (n × m) :=
  ∑ i : ι × κ, (D.test (dual a i.1) (dual b i.2)).smulRight (frame a b i)

def prepareCoordinates : Herm (n × m) →ₗ[ℝ] V :=
  ∑ i : ι × κ, (frameTest a b i).smulRight (D.prepare (a i.1) (b i.2))

theorem coordinates_test (x : V) (i : ι × κ) :
    frameTest a b i (coordinates a b D x) = D.test (dual a i.1) (dual b i.2) x := by
  simp [coordinates, map_sum, frame_delta]

theorem coordinates_injective : Function.Injective (coordinates a b D) := by
  intro x y h
  apply D.tomography x y
  intro E F
  have hi (i : ι) (j : κ) : D.test (dual a i) (dual b j) x = D.test (dual a i) (dual b j) y := by
    have := congrArg (frameTest a b (i,j)) h
    simpa only [coordinates_test] using this
  rw [← (dual a).sum_repr E, ← (dual b).sum_repr F]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]
  simp only [hi]

theorem coordinates_prepare (A : Herm n) (B : Herm m) :
    coordinates a b D (D.prepare A B) = product A B := by
  simp only [coordinates, LinearMap.sum_apply, LinearMap.smulRight_apply]
  change (∑ i : ι × κ, D.test (dual a i.1) (dual b i.2) (D.prepare A B) • frame a b i) = _
  simp only [D.factor, ← pairing_product]
  exact frame_expansion a b (product A B)

theorem coordinates_prepareCoordinates (H : Herm (n × m)) :
    coordinates a b D (prepareCoordinates a b D H) = H := by
  simp only [prepareCoordinates, LinearMap.sum_apply, LinearMap.smulRight_apply,
    map_sum, map_smul, coordinates_prepare]
  exact frame_expansion a b H

/-- The coordinate isomorphism is constructed, rather than postulated. -/
def tomographicEquiv : V ≃ₗ[ℝ] Herm (n × m) :=
  LinearEquiv.ofBijective (coordinates a b D)
    ⟨coordinates_injective a b D,
      fun H => ⟨prepareCoordinates a b D H, coordinates_prepareCoordinates a b D H⟩⟩

theorem tomographicEquiv_prepare (A : Herm n) (B : Herm m) :
    tomographicEquiv a b D (D.prepare A B) = product A B := coordinates_prepare a b D A B

theorem tomographicEquiv_test (E : Herm n) (F : Herm m) (x : V) :
    pairing (product E F) (tomographicEquiv a b D x) = D.test E F x := by
  change pairing (product E F) (coordinates a b D x) = _
  have hx : prepareCoordinates a b D (coordinates a b D x) = x :=
    coordinates_injective a b D (coordinates_prepareCoordinates a b D _)
  conv_lhs => rw [← frame_expansion a b (coordinates a b D x)]
  conv_rhs => rw [← hx]
  simp only [prepareCoordinates, LinearMap.sum_apply, LinearMap.smulRight_apply,
    map_sum, map_smul, frame, pairing_product, D.factor]

/-- Product statistics determine the coordinate map uniquely. -/
theorem tomographicEquiv_unique (J : V →ₗ[ℝ] Herm (n × m))
    (hJ : ∀ E F x, pairing (product E F) (J x) = D.test E F x) :
    J = (tomographicEquiv a b D).toLinearMap := by
  apply LinearMap.ext
  intro x
  change J x = tomographicEquiv a b D x
  rw [← frame_expansion a b (J x), ← frame_expansion a b (tomographicEquiv a b D x)]
  congr 1
  funext i
  simp only [frameTest, hJ, tomographicEquiv_test]

end Reconstruction

/-- Tomographically complete product calibration fixes a linear process. -/
theorem product_calibration {W : Type*} [AddCommGroup W] [Module ℝ W]
    (F G : Herm (n × m) →ₗ[ℝ] W)
    (h : ∀ A B, F (product A B) = G (product A B)) : F = G := by
  apply LinearMap.ext
  intro H
  have hH : H ∈ Submodule.span ℝ (Set.range (fun p : Herm n × Herm m => product p.1 p.2)) := by
    rw [product_span]; trivial
  induction hH using Submodule.span_induction with
  | mem x hx => obtain ⟨⟨A,B⟩,rfl⟩ := hx; exact h A B
  | zero => simp
  | add x y hx hy h1 h2 => simp only [map_add, h1, h2]
  | smul r x hx h1 => simp only [map_smul, h1]

/-- A finite product preparation frame and its dual test frame determine a
process from the finite table of output probabilities. -/
theorem finite_frame_calibration (a : Basis ι ℝ (Herm n)) (b : Basis κ ℝ (Herm m))
    (F G : Herm (n × m) →ₗ[ℝ] Herm (n × m))
    (h : ∀ i j, frameTest a b i (F (frame a b j)) = frameTest a b i (G (frame a b j))) :
    F = G := by
  have hg (j : ι × κ) : F (frame a b j) = G (frame a b j) := by
    rw [← frame_expansion a b (F (frame a b j)), ← frame_expansion a b (G (frame a b j))]
    simp only [h]
  apply LinearMap.ext
  intro H
  rw [← frame_expansion a b H]
  simp only [map_sum, map_smul, hg]

#print axioms tomographicEquiv
#print axioms tomographicEquiv_test
#print axioms tomographicEquiv_unique
#print axioms product_calibration
#print axioms finite_frame_calibration
end TensorTomography
