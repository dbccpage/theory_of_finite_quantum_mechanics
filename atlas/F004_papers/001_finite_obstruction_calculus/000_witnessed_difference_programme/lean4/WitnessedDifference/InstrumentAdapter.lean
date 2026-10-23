import Mathlib
import WitnessedDifference.AmplitudeBridge
import WitnessedDifference.EmpiricalModel

/-!
# One finite quantum-instrument adapter

`WDP-CH19-O04` asks for one finite quantum-instrument adapter whose
probabilities, state changes and receipts match a declared operational model,
without weakening the measurement nonclaims. This module gives it for a qubit
over the Gaussian rationals `ℚ(i)`, in the Kraus form, with the least
machinery that states the adapter.

A state is a finite rational mixture `ρ = Σⱼ wⱼ |vⱼ⟩⟨vⱼ|` with `wⱼ ≥ 0` and
`Σⱼ wⱼ ⟨vⱼ, vⱼ⟩ = 1`. No spectral theorem is used: positivity is built into
the declaration. An instrument is a family of `2 × 2` matrices `K_o` over `ℚ(i)`
with `Σ_o K_oᴴ K_o = 1`. Completeness is the trace-preserving condition. No
Stinespring dilation and no Choi matrix is used, so the finite adapter does not
need import 6 beyond its Kraus form.

* `WDP-CH19-P13`. For every state and instrument: the outcome probabilities are
  the adapter declares `p_o := Σⱼ wⱼ ⟨K_o vⱼ, K_o vⱼ⟩`, and then
  `p_o = Σⱼ wⱼ ⟨vⱼ, E_o vⱼ⟩`, the mixture trace of the POVM effect
  `E_o = K_oᴴ K_o`; they are nonnegative and add to one; for `p_o ≠ 0` the
  post-measurement state `K_o ρ K_oᴴ / p_o` is again a state of the same form,
  of trace one. The probabilities form an empirical model on the one-measurement
  cover, so `WDP-CH19-P04` applies to them: the table of declared probabilities is
  the image of a table of accepted measurement packets. Replaying the receipts
  through the measurement packet is not mechanized here.
* `WDP-CH19-P14`. The POVM does not determine the instrument. The Lüders
  instrument `K_o = |o⟩⟨o|` and the measure-and-prepare instrument
  `M_o = |w⟩⟨o|` with `w = (3/5, 4/5)` have the same effects, so the same
  outcome probabilities on every state, but the post-measurement vector of the
  first outcome on the input `(1, 0)` is `(1, 0)` for one and `(3/5, 4/5)` for
  the other, and these are not parallel.

Nothing here derives the measurement postulate, repeatability, calibration or
the uncertainty budget of an instrument, or Hilbert space itself.
-/

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace WitnessedDifference.InstrumentAdapter

open Matrix WitnessedDifference.AmplitudeBridge

attribute [local simp] QuadraticAlgebra.re_one QuadraticAlgebra.im_one
  QuadraticAlgebra.re_mul QuadraticAlgebra.im_mul QuadraticAlgebra.re_add
  QuadraticAlgebra.im_add QuadraticAlgebra.re_star QuadraticAlgebra.im_star
  QuadraticAlgebra.re_zero QuadraticAlgebra.im_zero

theorem algebraMap_inj (a b : ℚ) (h : algebraMap ℚ G a = algebraMap ℚ G b) : a = b := by
  simpa only [QuadraticAlgebra.algebraMap_re] using congrArg QuadraticAlgebra.re h

/-- A vector of the qubit over `ℚ(i)`. -/
abbrev V2 := Fin 2 → G

/-- The squared length `⟨v, v⟩`, a rational number. -/
def vnorm (v : V2) : ℚ := N (v 0) + N (v 1)

theorem vnorm_nonneg (v : V2) : 0 ≤ vnorm v := by
  unfold vnorm
  rw [N_def, N_def]
  nlinarith [mul_self_nonneg (v 0).re, mul_self_nonneg (v 0).im,
    mul_self_nonneg (v 1).re, mul_self_nonneg (v 1).im]

theorem algebraMap_vnorm (v : V2) : algebraMap ℚ G (vnorm v) = star v ⬝ᵥ v := by
  simp [vnorm, dotProduct, Fin.sum_univ_two, star_mul_self, map_add]

/-- The Gram identity behind the POVM formula: `⟨K v, K v⟩ = ⟨v, Kᴴ K v⟩`. -/
theorem gram (K : Matrix (Fin 2) (Fin 2) G) (v : V2) :
    star (K *ᵥ v) ⬝ᵥ (K *ᵥ v) = star v ⬝ᵥ ((Kᴴ * K) *ᵥ v) := by
  simp [dotProduct, mulVec, Fin.sum_univ_two, Matrix.mul_apply, Matrix.conjTranspose_apply,
    star_add, star_mul']
  ring

/-! ## `WDP-CH19-P13`: probabilities and state change -/

section Adapter

variable {O : Type*} [Fintype O]

/-- The completeness (trace-preserving) condition `Σ_o K_oᴴ K_o = 1`. -/
def IsComplete (K : O → Matrix (Fin 2) (Fin 2) G) : Prop :=
  ∑ o, (K o)ᴴ * K o = 1

theorem sum_vnorm {K : O → Matrix (Fin 2) (Fin 2) G} (hK : IsComplete K) (v : V2) :
    ∑ o, vnorm (K o *ᵥ v) = vnorm v := by
  have h : algebraMap ℚ G (∑ o, vnorm (K o *ᵥ v)) = algebraMap ℚ G (vnorm v) := by
    rw [map_sum]
    simp_rw [algebraMap_vnorm, gram]
    rw [← dotProduct_sum, ← Matrix.sum_mulVec, hK, Matrix.one_mulVec]
  exact algebraMap_inj _ _ h

/-- A state: a finite list of weights and vectors, with nonnegative weights and
total mass one. -/
structure State where
  parts : List (ℚ × V2)
  weight_nonneg : ∀ x ∈ parts, 0 ≤ x.1
  mass : (parts.map fun x => x.1 * vnorm x.2).sum = 1

/-- The probability of the outcome `o`: `Σⱼ wⱼ ⟨K_o vⱼ, K_o vⱼ⟩`. -/
def prob (K : O → Matrix (Fin 2) (Fin 2) G) (s : State) (o : O) : ℚ :=
  (s.parts.map fun x => x.1 * vnorm (K o *ᵥ x.2)).sum

/-- The POVM effect `E_o = K_oᴴ K_o`. -/
def effect (K : O → Matrix (Fin 2) (Fin 2) G) (o : O) : Matrix (Fin 2) (Fin 2) G :=
  (K o)ᴴ * K o

/-- The same probability read through the POVM effect: `Σⱼ wⱼ ⟨vⱼ, E_o vⱼ⟩`. -/
def probViaEffect (E : O → Matrix (Fin 2) (Fin 2) G) (s : State) (o : O) : G :=
  (s.parts.map fun x => algebraMap ℚ G x.1 * (star x.2 ⬝ᵥ (E o *ᵥ x.2))).sum

theorem prob_nonneg (K : O → Matrix (Fin 2) (Fin 2) G) (s : State) (o : O) :
    0 ≤ prob K s o := by
  unfold prob
  refine List.sum_nonneg fun y hy => ?_
  obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hy
  exact mul_nonneg (s.weight_nonneg x hx) (vnorm_nonneg _)

theorem sum_map_sum {ι α : Type*} [Fintype ι] (l : List α) (f : α → ι → ℚ) :
    ∑ i, (l.map fun x => f x i).sum = (l.map fun x => ∑ i, f x i).sum := by
  induction l with
  | nil => simp
  | cons x l ih => simp [Finset.sum_add_distrib, ih]

/-- `WDP-CH19-P13`. The outcome probabilities add up to one. -/
theorem sum_prob {K : O → Matrix (Fin 2) (Fin 2) G} (hK : IsComplete K) (s : State) :
    ∑ o, prob K s o = 1 := by
  unfold prob
  rw [sum_map_sum]
  simp_rw [← Finset.mul_sum, sum_vnorm hK]
  exact s.mass

/-- `WDP-CH19-P13`. The probability is the trace formula `tr(E_o ρ)`: the
Gaussian-rational image of `p_o` is `Σⱼ wⱼ ⟨vⱼ, E_o vⱼ⟩`. -/
theorem prob_eq_effect (K : O → Matrix (Fin 2) (Fin 2) G) (s : State) (o : O) :
    algebraMap ℚ G (prob K s o) = probViaEffect (effect K) s o := by
  unfold prob probViaEffect effect
  induction s.parts with
  | nil => simp
  | cons x l ih =>
    simp only [List.map_cons, List.sum_cons, map_add, map_mul, algebraMap_vnorm, gram] at ih ⊢
    rw [ih]

theorem list_sum_map_div {α : Type*} (l : List α) (f : α → ℚ) (p : ℚ) :
    (l.map fun x => f x / p).sum = (l.map f).sum / p := by
  induction l with
  | nil => simp
  | cons x l ih => simp [ih, add_div]

/-- The post-measurement state for an outcome of positive probability. -/
noncomputable def post (K : O → Matrix (Fin 2) (Fin 2) G) (s : State) (o : O)
    (hp : prob K s o ≠ 0) : State where
  parts := s.parts.map fun x => (x.1 / prob K s o, K o *ᵥ x.2)
  weight_nonneg := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hy
    exact div_nonneg (s.weight_nonneg x hx) (prob_nonneg K s o)
  mass := by
    have h1 : (s.parts.map fun x => (x.1 / prob K s o, K o *ᵥ x.2)).map
        (fun y => y.1 * vnorm y.2) =
        s.parts.map (fun x => (x.1 * vnorm (K o *ᵥ x.2)) / prob K s o) := by
      rw [List.map_map]
      exact List.map_congr_left fun x _ => by
        simp [div_mul_eq_mul_div]
    rw [h1, list_sum_map_div]
    exact div_self hp

/-- Sections over the one-measurement context are the outcomes. -/
def secEquiv (O : Type*) : (↥(Finset.univ : Finset Unit) → O) ≃ O where
  toFun t := t ⟨(), Finset.mem_univ _⟩
  invFun o := fun _ => o
  left_inv t := by
    funext x
    obtain ⟨u, hx⟩ := x
    cases u
    rfl
  right_inv _ := rfl

/-- `WDP-CH19-P13`. The probabilities `p_o` form an empirical model on the
one-measurement cover: the model that `WDP-CH19-P04` shows to be the image of a
finite table of accepted measurement packets. -/
noncomputable def instrumentModel [DecidableEq O] {K : O → Matrix (Fin 2) (Fin 2) G}
    (hK : IsComplete K) (s : State) :
    Empirical.EmpiricalModel (fun _ : Unit => (Finset.univ : Finset Unit)) O where
  weight := fun _ t => prob K s (secEquiv O t)
  nonneg := fun _ t => prob_nonneg K s _
  normalized := fun _ =>
    (Equiv.sum_comp (secEquiv O) (fun o => prob K s o)).trans (sum_prob hK s)
  compatible := fun _ _ _ => rfl

end Adapter

/-! ## `WDP-CH19-P14`: the POVM does not determine the instrument -/

/-- The Lüders instrument in the standard basis. -/
def ludersK : Bool → Matrix (Fin 2) (Fin 2) G
  | false => !![1, 0; 0, 0]
  | true => !![0, 0; 0, 1]

/-- The measure-and-prepare instrument that prepares `w = (3/5, 4/5)` whatever
the outcome. -/
def prepareK : Bool → Matrix (Fin 2) (Fin 2) G
  | false => !![⟨3 / 5, 0⟩, 0; ⟨4 / 5, 0⟩, 0]
  | true => !![0, ⟨3 / 5, 0⟩; 0, ⟨4 / 5, 0⟩]

theorem ludersK_complete : IsComplete ludersK := by
  unfold IsComplete
  rw [Fintype.sum_bool]
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [ludersK, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_two]

theorem prepareK_complete : IsComplete prepareK := by
  unfold IsComplete
  rw [Fintype.sum_bool]
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [prepareK, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_two] <;>
    norm_num

theorem same_effects : ∀ o, effect ludersK o = effect prepareK o := by
  intro o
  cases o <;>
    (ext i j <;> fin_cases i <;> fin_cases j <;>
       simp [effect, ludersK, prepareK, Matrix.mul_apply, Matrix.conjTranspose_apply,
         Fin.sum_univ_two] <;> norm_num)

/-- The outcome `false` on the input `(1, 0)` leaves `(1, 0)` under the Lüders
instrument and `(3/5, 4/5)` under measure-and-prepare. -/
theorem post_vectors_differ :
    (ludersK false *ᵥ ![1, 0] : V2) = ![1, 0] ∧
      (prepareK false *ᵥ ![1, 0] : V2) = ![⟨3 / 5, 0⟩, ⟨4 / 5, 0⟩] ∧
      ∀ c : G, (ludersK false *ᵥ ![1, 0] : V2) ≠ c • (prepareK false *ᵥ ![1, 0] : V2) := by
  refine ⟨?_, ?_, ?_⟩
  · ext i <;> fin_cases i <;> simp [ludersK, mulVec, dotProduct, Fin.sum_univ_two]
  · ext i <;> fin_cases i <;> simp [prepareK, mulVec, dotProduct, Fin.sum_univ_two]
  · intro c h
    have h1 := congrFun h 1
    have h0 := congrFun h 0
    simp [ludersK, prepareK, mulVec, dotProduct, Fin.sum_univ_two] at h0 h1
    have h0r := congrArg QuadraticAlgebra.re h0
    have h1r := congrArg QuadraticAlgebra.re h1
    simp at h0r h1r
    linarith

/-- `WDP-CH19-P14`. The two instruments are complete, have the same POVM, hence
the same outcome probabilities on every state, and different post-measurement
vectors. -/
theorem povm_does_not_determine_the_instrument :
    IsComplete ludersK ∧ IsComplete prepareK ∧ (∀ o, effect ludersK o = effect prepareK o) ∧
      (∀ (s : State) (o : Bool), algebraMap ℚ G (prob ludersK s o) =
        algebraMap ℚ G (prob prepareK s o)) ∧
      ((ludersK false *ᵥ ![1, 0] : V2) = ![1, 0] ∧
        (prepareK false *ᵥ ![1, 0] : V2) = ![⟨3 / 5, 0⟩, ⟨4 / 5, 0⟩] ∧
        ∀ c : G, (ludersK false *ᵥ ![1, 0] : V2) ≠ c • (prepareK false *ᵥ ![1, 0] : V2)) := by
  refine ⟨ludersK_complete, prepareK_complete, same_effects, fun s o => ?_, post_vectors_differ⟩
  rw [prob_eq_effect, prob_eq_effect, funext same_effects]

end WitnessedDifference.InstrumentAdapter
