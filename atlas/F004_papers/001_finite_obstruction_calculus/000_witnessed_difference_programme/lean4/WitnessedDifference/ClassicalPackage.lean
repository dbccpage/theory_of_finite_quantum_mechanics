import Mathlib
import WitnessedDifference.ClassicalCorner
import WitnessedDifference.EmpiricalModel

/-!
# The strengthened package S: stochastic updates and classical instruments

`ClassicalCorner` proves outcome (a) of `WDP-CH18-O01` for updates that are
reversible within the states. This module removes the reversibility and adds
the measurement layer. The package S consists of W1, W2, W3⁺ (pointwise
nonnegative weights), W4′ (linear updates that send states to states, with no
reversibility required), W6′ (classical instruments) and W7 (joint runs: the
empirical model has a nonnegative global section). S is not a strengthening of
W1–W6: it omits W5, replaces W6 by W6′ and drops the reversibility of W4.

* `WDP-CH18-P07`. State-preserving updates are the column-stochastic
  matrices; they are closed under composition and contain the identity. The
  deterministic ones, whose entries are `0` or `1`, are exactly the updates
  `funMatrix f` induced by a function `f`, and every presentation map is one.
  Every stochastic update is a mixture of function updates with weights
  `∏ j, T (f j) j`, which are nonnegative and sum to one. The units are the
  permutations (`ClassicalCorner`).
* `WDP-CH18-P08`. For a classical instrument, a family of nonnegative matrices
  whose sum is column-stochastic, the law of an outcome word is nonnegative,
  sums to the mass over all words of a given length, and is consistent under
  dropping the last outcome. On a cover, W7 gives the classical bound
  `CHSH ≤ 2`; without W7 a compatible model with `CHSH = 4` exists, and
  without W3⁺ the signed shear is mass-preserving and invertible but not a
  permutation.

No declaration here derives quantum theory. Every statement is finite and
exact over `ℚ`.
-/

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace WitnessedDifference.ClassicalPackage

open Matrix Finset

/-! ## `WDP-CH18-P07`: stochastic updates -/

section Kernels

variable {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
  [DecidableEq α] [DecidableEq β] [DecidableEq γ]

/-- A stochastic update from carrier `α` to carrier `β`: nonnegative entries,
every column summing to one. On a square carrier this is
`ClassicalCorner.IsStochastic`. -/
def IsKernel (T : Matrix β α ℚ) : Prop :=
  (∀ i j, 0 ≤ T i j) ∧ ∀ j, ∑ i, T i j = 1

theorem isKernel_iff_isStochastic {ι : Type*} [Fintype ι] [DecidableEq ι]
    (T : Matrix ι ι ℚ) : IsKernel T ↔ ClassicalCorner.IsStochastic T :=
  Iff.rfl

theorem isKernel_one : IsKernel (1 : Matrix α α ℚ) := by
  refine ⟨fun i j => ?_, fun j => ?_⟩
  · by_cases h : i = j <;> simp [one_apply, h]
  · simp [one_apply]

theorem isKernel_mul {S : Matrix γ β ℚ} {T : Matrix β α ℚ} (hS : IsKernel S)
    (hT : IsKernel T) : IsKernel (S * T) := by
  refine ⟨fun i j => ?_, fun j => ?_⟩
  · exact Finset.sum_nonneg fun k _ => mul_nonneg (hS.1 i k) (hT.1 k j)
  · simp only [mul_apply]
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, hS.2, one_mul]
    exact hT.2 j

/-- The update induced by a function `f`: the column of `j` is the basis vector
of `f j`. -/
def funMatrix (f : α → β) : Matrix β α ℚ :=
  fun i j => if i = f j then 1 else 0

theorem funMatrix_isKernel (f : α → β) : IsKernel (funMatrix f) := by
  refine ⟨fun i j => ?_, fun j => ?_⟩
  · simp only [funMatrix]
    split_ifs <;> norm_num
  · simp [funMatrix]

theorem funMatrix_mul (g : β → γ) (f : α → β) :
    funMatrix g * funMatrix f = funMatrix (g ∘ f) := by
  ext i j
  simp only [mul_apply, funMatrix, Function.comp]
  rw [Finset.sum_eq_single (f j)]
  · simp
  · intro b _ hb
    simp [hb]
  · simp

theorem funMatrix_id : funMatrix (id : α → α) = 1 := by
  ext i j
  simp [funMatrix, one_apply, eq_comm]

/-- A function update pushes a weight forward along the function: presentation
maps act this way on weights. -/
theorem funMatrix_mulVec (f : α → β) (p : α → ℚ) (i : β) :
    (funMatrix f *ᵥ p) i = ∑ j ∈ univ.filter (fun j => f j = i), p j := by
  simp only [mulVec, dotProduct, funMatrix]
  rw [Finset.sum_filter]
  refine Finset.sum_congr rfl fun j _ => ?_
  by_cases h : f j = i
  · simp [h]
  · simp [h, Ne.symm h]

theorem funMatrix_preserves_mass (f : α → β) (p : α → ℚ) :
    ∑ i, (funMatrix f *ᵥ p) i = ∑ j, p j := by
  simp only [funMatrix_mulVec]
  rw [← Finset.sum_fiberwise (s := univ) (g := f) (f := p)]

/-- The deterministic updates are exactly the function updates: a stochastic
update whose entries are all `0` or `1`. -/
theorem deterministic_iff (T : Matrix β α ℚ) :
    (IsKernel T ∧ ∀ i j, T i j = 0 ∨ T i j = 1) ↔ ∃ f : α → β, T = funMatrix f := by
  constructor
  · rintro ⟨⟨_, hcol⟩, h01⟩
    have hex : ∀ j, ∃ a, ∀ i, T i j = if i = a then 1 else 0 := by
      intro j
      have hcard : (univ.filter (fun i => T i j = 1)).card = 1 := by
        have h1 : ∑ i, T i j = ((univ.filter (fun i => T i j = 1)).card : ℚ) := by
          rw [Finset.card_filter]
          push_cast
          refine Finset.sum_congr rfl fun i _ => ?_
          rcases h01 i j with h | h <;> simp [h]
        have := hcol j
        rw [h1] at this
        exact_mod_cast this
      obtain ⟨a, ha⟩ := Finset.card_eq_one.mp hcard
      refine ⟨a, fun i => ?_⟩
      have hmem : ∀ i, T i j = 1 ↔ i = a := by
        intro i
        have := congrArg (i ∈ ·) ha
        simpa using this
      by_cases hia : i = a
      · rw [if_pos hia]; exact (hmem i).mpr hia
      · rcases h01 i j with h | h
        · simp [hia, h]
        · exact absurd ((hmem i).mp h) hia
    choose f hf using hex
    exact ⟨f, by ext i j; exact hf j i⟩
  · rintro ⟨f, rfl⟩
    refine ⟨funMatrix_isKernel f, fun i j => ?_⟩
    simp only [funMatrix]
    split_ifs <;> simp

/-- The weight of the function `f` in the mixture decomposition of `T`. -/
def funWeight (T : Matrix β α ℚ) (f : α → β) : ℚ :=
  ∏ j, T (f j) j

theorem funWeight_nonneg {T : Matrix β α ℚ} (hT : IsKernel T) (f : α → β) :
    0 ≤ funWeight T f :=
  Finset.prod_nonneg fun j _ => hT.1 (f j) j

theorem sum_funWeight {T : Matrix β α ℚ} (hT : IsKernel T) :
    ∑ f : α → β, funWeight T f = 1 := by
  have h := Finset.prod_univ_sum (fun _ : α => (univ : Finset β)) (fun j i => T i j)
  rw [Fintype.piFinset_univ] at h
  have h2 : ∏ j, ∑ i, T i j = 1 := by simp [hT.2]
  rw [← h2, h]
  rfl

/-- `WDP-CH18-P07`. Every stochastic update is a mixture of function updates,
with weights `∏ j, T (f j) j`. -/
theorem mixture_of_functions {T : Matrix β α ℚ} (hT : IsKernel T) :
    T = ∑ f : α → β, funWeight T f • funMatrix f := by
  ext i k
  simp only [Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul, funMatrix, funWeight]
  have hterm : ∀ f : α → β,
      (∏ j, T (f j) j) * (if i = f k then (1 : ℚ) else 0) =
        ∏ j, (T (f j) j * (if j = k then (if i = f j then (1 : ℚ) else 0) else 1)) := by
    intro f
    rw [Finset.prod_mul_distrib]
    congr 1
    rw [Finset.prod_ite_eq' ]
    simp
  simp_rw [hterm]
  have h := Finset.prod_univ_sum (fun _ : α => (univ : Finset β))
    (fun j i' => T i' j * (if j = k then (if i = i' then (1 : ℚ) else 0) else 1))
  rw [Fintype.piFinset_univ] at h
  rw [← h]
  rw [Finset.prod_eq_single k]
  · simp
  · intro j _ hj
    simp only [hj, if_false, mul_one]
    exact hT.2 j
  · simp

/-- `WDP-CH18-P07`, bundled. State-preserving updates of a square carrier are
closed under composition and contain the identity; the deterministic ones are
the function updates; and every stochastic update is a mixture of function
updates whose weights are nonnegative and sum to one. -/
theorem stochastic_updates_are_mixtures_of_functions :
    (IsKernel (1 : Matrix α α ℚ)) ∧
      (∀ (S T : Matrix α α ℚ), IsKernel S → IsKernel T → IsKernel (S * T)) ∧
      (∀ T : Matrix β α ℚ, (IsKernel T ∧ ∀ i j, T i j = 0 ∨ T i j = 1) ↔
        ∃ f : α → β, T = funMatrix f) ∧
      (∀ T : Matrix β α ℚ, IsKernel T →
        T = ∑ f : α → β, funWeight T f • funMatrix f ∧
          (∀ f, 0 ≤ funWeight T f) ∧ ∑ f : α → β, funWeight T f = 1) :=
  ⟨isKernel_one, fun _ _ hS hT => isKernel_mul hS hT, deterministic_iff,
    fun _ hT => ⟨mixture_of_functions hT, funWeight_nonneg hT, sum_funWeight hT⟩⟩

end Kernels

/-! ## `WDP-CH18-P08`: classical instruments -/

section Instruments

variable {ι O : Type*} [Fintype ι] [DecidableEq ι] [Fintype O]

/-- A classical instrument (W6′): one nonnegative update per outcome, whose sum
is column-stochastic. -/
structure Instrument (ι O : Type*) [Fintype ι] [DecidableEq ι] [Fintype O] where
  T : O → Matrix ι ι ℚ
  nonneg : ∀ o i j, 0 ≤ T o i j
  complete : IsKernel (∑ o, T o)

/-- The unnormalized state after the outcome word, applied first outcome first. -/
def Instrument.run (I : Instrument ι O) : List O → (ι → ℚ) → (ι → ℚ)
  | [], p => p
  | o :: l, p => I.run l (I.T o *ᵥ p)

/-- The law of an outcome word on the state `p`: the mass left after the run. -/
def Instrument.law (I : Instrument ι O) (l : List O) (p : ι → ℚ) : ℚ :=
  ∑ i, I.run l p i

theorem Instrument.run_nonneg (I : Instrument ι O) (l : List O) :
    ∀ p : ι → ℚ, (∀ i, 0 ≤ p i) → ∀ i, 0 ≤ I.run l p i := by
  induction l with
  | nil => intro p hp; exact hp
  | cons o l ih =>
    intro p hp
    refine ih _ (fun i => ?_)
    exact Finset.sum_nonneg fun j _ => mul_nonneg (I.nonneg o i j) (hp j)

theorem Instrument.law_nonneg (I : Instrument ι O) (l : List O) {p : ι → ℚ}
    (hp : ∀ i, 0 ≤ p i) : 0 ≤ I.law l p :=
  Finset.sum_nonneg fun i _ => I.run_nonneg l p hp i

theorem Instrument.run_append (I : Instrument ι O) (l : List O) (o : O) :
    ∀ p : ι → ℚ, I.run (l ++ [o]) p = I.T o *ᵥ I.run l p := by
  induction l with
  | nil => intro p; rfl
  | cons o' l ih => intro p; exact ih _

/-- The outcomes of one step exhaust the mass: `∑ o, mass (T o p) = mass p`. -/
theorem Instrument.sum_step (I : Instrument ι O) (q : ι → ℚ) :
    ∑ o, ∑ i, (I.T o *ᵥ q) i = ∑ i, q i := by
  have h : ∀ j, ∑ o, ∑ i, I.T o i j = 1 := by
    intro j
    rw [Finset.sum_comm]
    simpa [Matrix.sum_apply] using I.complete.2 j
  calc ∑ o, ∑ i, (I.T o *ᵥ q) i
      = ∑ o, ∑ i, ∑ j, I.T o i j * q j := by
        simp [mulVec, dotProduct]
    _ = ∑ j, (∑ o, ∑ i, I.T o i j) * q j := by
        simp_rw [Finset.sum_mul]
        calc _ = ∑ o, ∑ j, ∑ i, I.T o i j * q j :=
              Finset.sum_congr rfl fun o _ => Finset.sum_comm
          _ = _ := Finset.sum_comm
    _ = ∑ j, q j := by simp [h]

/-- Consistency: dropping the last outcome recovers the law of the prefix. -/
theorem Instrument.law_consistent (I : Instrument ι O) (l : List O) (p : ι → ℚ) :
    ∑ o, I.law (l ++ [o]) p = I.law l p := by
  simp only [Instrument.law, I.run_append]
  exact I.sum_step _

/-- Normalization: over all outcome words of length `n` the laws add up to the
mass of the initial state. -/
theorem Instrument.law_total (I : Instrument ι O) (n : ℕ) :
    ∀ p : ι → ℚ, ∑ w : Fin n → O, I.law (List.ofFn w) p = ∑ i, p i := by
  induction n with
  | zero =>
    intro p
    simp [Instrument.law, Instrument.run]
  | succ n ih =>
    intro p
    rw [← (Fin.consEquiv (fun _ : Fin (n + 1) => O)).sum_comp, Fintype.sum_prod_type]
    simp only [Fin.consEquiv_apply, List.ofFn_succ, Fin.cons_zero, Fin.cons_succ]
    have : ∀ (o : O) (w : Fin n → O),
        I.law (o :: List.ofFn w) p = I.law (List.ofFn w) (I.T o *ᵥ p) := fun _ _ => rfl
    simp_rw [this]
    simp_rw [ih]
    exact I.sum_step p

end Instruments

/-! ## `WDP-CH18-P08`: the package and its sharpness -/

open WitnessedDifference.Empirical in
/-- `WDP-CH18-P08`. Under the strengthened package S the observer and
measurement layers are classical: the outcome law of every classical instrument
is a probability law (nonnegative, consistent, normalized), and every
noncontextual model on the CHSH cover has `CHSH ≤ 2`. The hypotheses are
needed. Without W7 the PR box is a compatible model with `CHSH = 4` and no
nonnegative global section; without W3⁺ the signed shear preserves mass, has a
mass-preserving inverse, and is not a permutation. -/
theorem classical_package_and_sharpness :
    (∀ {ι O : Type} [Fintype ι] [DecidableEq ι] [Fintype O] (I : Instrument ι O)
        (p : ι → ℚ), (∀ i, 0 ≤ p i) →
        (∀ l, 0 ≤ I.law l p) ∧ (∀ l, ∑ o, I.law (l ++ [o]) p = I.law l p) ∧
          ∀ n, ∑ w : Fin n → O, I.law (List.ofFn w) p = ∑ i, p i) ∧
      (∀ weight : ∀ xy, (chshContext xy → Bool) → ℚ,
        IsNoncontextual chshContext weight → chsh weight ≤ 2) ∧
      (IsGlobalSection chshContext prWeight prSigned ∧
        ¬ IsNoncontextual chshContext prWeight ∧ chsh prWeight = 4) ∧
      ((∀ w : Fin 2 → ℚ, ∑ i, (ClassicalCorner.signedShear *ᵥ w) i = ∑ i, w i) ∧
        ClassicalCorner.signedShearInv * ClassicalCorner.signedShear = 1 ∧
        (∀ σ : Equiv.Perm (Fin 2), ClassicalCorner.signedShear ≠ σ.permMatrix ℚ)) := by
  refine ⟨fun I p hp => ⟨fun l => I.law_nonneg l hp, fun l => I.law_consistent l p,
      fun n => I.law_total n p⟩, fun _ h => chsh_le_two_of_noncontextual h, ?_, ?_⟩
  · exact ⟨prBox_signed_not_nonneg.1, prBox_signed_not_nonneg.2.2, chsh_prBox⟩
  · obtain ⟨h1, _, h3, h4, _⟩ := ClassicalCorner.signed_weights_break_the_corner
    exact ⟨h1, h3, h4⟩

end WitnessedDifference.ClassicalPackage
