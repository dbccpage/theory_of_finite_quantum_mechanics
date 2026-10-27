import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic.Module
import Mathlib.Tactic.NoncommRing
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
Canonical trace form for a finite real Jordan--Lie algebra.

The algebraic identities and real spectral decompositions are premises.
No inner product or positive trace form is supplied. This file constructs
the trace form and derives its compatibility and positivity from those data.
Operational states, effects, composite systems and physical realization are
outside this result.
-/

namespace Po000JordanTrace

open LinearMap

variable {E : Type*} [AddCommGroup E] [Module ℝ E]

structure Data (E : Type*) [AddCommGroup E] [Module ℝ E] where
  j : E →ₗ[ℝ] E →ₗ[ℝ] E
  l : E →ₗ[ℝ] E →ₗ[ℝ] E
  one : E
  j_comm : ∀ a b, j a b = j b a
  j_unit : ∀ a, j one a = a
  l_anti : ∀ a b, l a b = -l b a
  derivation : ∀ a b c, l a (j b c) = j (l a b) c + j b (l a c)
  associator : ∀ a b c, j (j a b) c - j a (j b c) = l b (l c a)

namespace Data

variable (d : Data E)

noncomputable def trace : E →ₗ[ℝ] ℝ := (LinearMap.trace ℝ E).comp d.j

noncomputable def form : E →ₗ[ℝ] E →ₗ[ℝ] ℝ :=
  LinearMap.compr₂ d.j d.trace

@[simp] theorem trace_apply (a : E) : d.trace a = LinearMap.trace ℝ E (d.j a) := rfl

@[simp] theorem form_apply (a b : E) : d.form a b = d.trace (d.j a b) := rfl

theorem bracket_self (a : E) : d.l a a = 0 := by
  have h := d.l_anti a a
  have h' : (2 : ℝ) • d.l a a = 0 := by
    calc
      _ = d.l a a + d.l a a := by module
      _ = 0 := (congrArg (fun x => x + d.l a a) h).trans (neg_add_cancel _)
  exact (smul_eq_zero.mp h').resolve_left (by norm_num)

theorem bracket_unit (a : E) : d.l a d.one = 0 := by
  have h := d.derivation a d.one d.one
  rw [d.j_unit, d.j_unit, d.j_comm (d.l a d.one) d.one, d.j_unit] at h
  exact (add_eq_left.mp h.symm)

theorem derivation_commutator (a b : E) :
    d.j (d.l a b) = d.l a * d.j b - d.j b * d.l a := by
  ext c
  simp only [LinearMap.sub_apply, Module.End.mul_apply]
  rw [d.derivation]
  module

theorem trace_bracket (a b : E) : d.trace (d.l a b) = 0 := by
  rw [trace_apply, d.derivation_commutator, map_sub, LinearMap.trace_mul_comm]
  exact sub_self _

theorem form_comm (a b : E) : d.form a b = d.form b a := by
  simp only [form_apply, d.j_comm a b]

theorem form_associative (a b c : E) :
    d.form (d.j a b) c = d.form b (d.j a c) := by
  have h := congrArg d.trace (d.associator b a c)
  rw [map_sub, d.trace_bracket, d.j_comm b a] at h
  exact sub_eq_zero.mp h

theorem form_bracket_skew (a b c : E) :
    d.form (d.l a b) c = -d.form b (d.l a c) := by
  have h := congrArg d.trace (d.derivation a b c)
  rw [d.trace_bracket, map_add] at h
  exact eq_neg_of_add_eq_zero_left h.symm

theorem idempotent_bracket_half (e x : E) (he : d.j e e = e) :
    (2 : ℝ) • d.j e (d.l e x) = d.l e x := by
  have h := d.derivation x e e
  rw [he, d.l_anti x e, d.j_comm (-d.l e x) e] at h
  simp only [map_neg] at h
  simpa only [neg_neg, neg_add_rev, two_smul] using (congrArg Neg.neg h).symm

theorem idempotent_square_relation (e x : E) (he : d.j e e = e) :
    d.j e (d.j e x) - d.j e x = d.l e (d.l e x) := by
  have h := d.associator e e x
  rw [he, d.l_anti x e, map_neg] at h
  calc
    _ = -(d.j e x - d.j e (d.j e x)) := by module
    _ = d.l e (d.l e x) := by rw [h, neg_neg]

theorem idempotent_peirce (e : E) (he : d.j e e = e) :
    2 * (d.j e) ^ 3 - 3 * (d.j e) ^ 2 + d.j e = 0 := by
  ext x
  have h := d.idempotent_bracket_half e (d.l e x) he
  have h₁ := d.idempotent_square_relation e x he
  have h₂ := congrArg (d.j e) h₁
  simp only [map_sub] at h₂
  rw [← h₂, ← h₁] at h
  simp only [LinearMap.add_apply, LinearMap.sub_apply, Module.End.mul_apply,
    pow_succ, pow_zero, Module.End.one_apply, LinearMap.zero_apply,
    Module.End.ofNat_apply]
  convert sub_eq_zero.mpr h using 1
  module

theorem peirce_projection_one (T : E →ₗ[ℝ] E)
    (h : 2 * T ^ 3 - 3 * T ^ 2 + T = 0) :
    IsIdempotentElem (2 * T ^ 2 - T) := by
  apply sub_eq_zero.mp
  calc
    _ = (2 * T + 1) * (2 * T ^ 3 - 3 * T ^ 2 + T) := by noncomm_ring
    _ = 0 := by rw [h, mul_zero]

theorem peirce_projection_half (T : E →ₗ[ℝ] E)
    (h : 2 * T ^ 3 - 3 * T ^ 2 + T = 0) :
    IsIdempotentElem (4 * (T - T ^ 2)) := by
  apply sub_eq_zero.mp
  calc
    _ = (8 * T - 4) * (2 * T ^ 3 - 3 * T ^ 2 + T) := by noncomm_ring
    _ = 0 := by rw [h, mul_zero]

variable [FiniteDimensional ℝ E]

theorem trace_idempotent_nonneg (P : E →ₗ[ℝ] E) (hP : IsIdempotentElem P) :
    0 ≤ LinearMap.trace ℝ E P := by
  rw [hP.isProj_range.trace]
  exact Nat.cast_nonneg _

theorem trace_idempotent_pos (e : E) (he : d.j e e = e) (hne : e ≠ 0) :
    0 < d.trace e := by
  let P := 2 * (d.j e) ^ 2 - d.j e
  let Q := 4 * (d.j e - (d.j e) ^ 2)
  have hP : IsIdempotentElem P := peirce_projection_one _ (d.idempotent_peirce e he)
  have hQ : IsIdempotentElem Q := peirce_projection_half _ (d.idempotent_peirce e he)
  have hPe : P e = e := by
    simp [P, pow_two, Module.End.mul_apply, Module.End.ofNat_apply, he]
    module
  have hPne : P ≠ 0 := by
    intro h
    apply hne
    simpa [h] using hPe.symm
  have htP : 0 < LinearMap.trace ℝ E P := by
    have hn := trace_idempotent_nonneg P hP
    have hz : LinearMap.trace ℝ E P ≠ 0 := by
      intro h
      exact hPne (hP.eq_zero_of_trace_eq_zero h)
    exact lt_of_le_of_ne hn (Ne.symm hz)
  have htQ := trace_idempotent_nonneg Q hQ
  have hid : (2 : ℝ) • d.j e = (2 : ℝ) • P + Q := by
    ext x
    simp only [P, Q, LinearMap.smul_apply, LinearMap.add_apply, LinearMap.sub_apply,
      Module.End.mul_apply, Module.End.ofNat_apply]
    module
  have ht := congrArg (LinearMap.trace ℝ E) hid
  simp only [map_smul, map_add, smul_eq_mul] at ht
  change 0 < LinearMap.trace ℝ E (d.j e)
  linarith

/-- A supplied real spectral decomposition. Its idempotents are not
assumed to have positive trace; that property was proved above. -/
structure SpectralWitness (a : E) where
  count : ℕ
  coefficient : Fin count → ℝ
  vector : Fin count → E
  decomposition : a = ∑ i, coefficient i • vector i
  nonzero : ∀ i, vector i ≠ 0
  idempotent : ∀ i, d.j (vector i) (vector i) = vector i
  orthogonal : ∀ i j, i ≠ j → d.j (vector i) (vector j) = 0

omit [FiniteDimensional ℝ E] in
theorem spectral_square (a : E) (s : d.SpectralWitness a) :
    d.j a a = ∑ i, (s.coefficient i) ^ 2 • s.vector i := by
  classical
  have hv (i : Fin s.count) : d.j (s.vector i) a = s.coefficient i • s.vector i := by
    calc
      _ = d.j (s.vector i) (∑ j, s.coefficient j • s.vector j) :=
        congrArg (d.j (s.vector i)) s.decomposition
      _ = s.coefficient i • s.vector i := ?_
    rw [map_sum]
    simp only [map_smul]
    rw [Finset.sum_eq_single i]
    · rw [s.idempotent]
    · intro j _ hji
      rw [s.orthogonal i j (Ne.symm hji), smul_zero]
    · simp
  have h : d.j a a = ∑ i, s.coefficient i • d.j (s.vector i) a := by
    calc
      _ = d.j (∑ i, s.coefficient i • s.vector i) a :=
        congrArg (fun x => d.j x a) s.decomposition
      _ = _ := by simp
  rw [h]
  simp only [hv, smul_smul, pow_two]

omit [FiniteDimensional ℝ E] in
theorem form_self_spectral (a : E) (s : d.SpectralWitness a) :
    d.form a a = ∑ i, (s.coefficient i) ^ 2 * d.trace (s.vector i) := by
  rw [form_apply, d.spectral_square a s, map_sum]
  simp only [map_smul, smul_eq_mul]

theorem form_self_pos (a : E) (s : d.SpectralWitness a) (ha : a ≠ 0) :
    0 < d.form a a := by
  classical
  have hc : ∃ i, s.coefficient i ≠ 0 := by
    by_contra! h
    apply ha
    rw [s.decomposition]
    simp [h]
  rw [d.form_self_spectral a s]
  apply Finset.sum_pos'
  · intro i _
    exact mul_nonneg (sq_nonneg _) (le_of_lt
      (d.trace_idempotent_pos _ (s.idempotent i) (s.nonzero i)))
  · obtain ⟨i, hi⟩ := hc
    exact ⟨i, Finset.mem_univ _, mul_pos (sq_pos_of_ne_zero hi)
      (d.trace_idempotent_pos _ (s.idempotent i) (s.nonzero i))⟩

theorem form_self_nonneg (a : E) (s : d.SpectralWitness a) : 0 ≤ d.form a a := by
  by_cases ha : a = 0
  · simp [ha]
  · exact le_of_lt (d.form_self_pos a s ha)

theorem form_self_eq_zero_iff (a : E) (s : d.SpectralWitness a) :
    d.form a a = 0 ↔ a = 0 := by
  constructor
  · intro h
    by_contra ha
    have hp := d.form_self_pos a s ha
    linarith
  · intro h
    simp [h]

end Data

/-- The real scalar algebra supplies an inhabitant of the identity package. -/
noncomputable def scalarData : Data ℝ where
  j := LinearMap.mul ℝ ℝ
  l := 0
  one := 1
  j_comm := mul_comm
  j_unit := one_mul
  l_anti := by intros; simp
  derivation := by intros; simp
  associator := by intros; simp [mul_assoc]

/-- Every real scalar has an explicit spectral witness in the same model. -/
noncomputable def scalarSpectrum (a : ℝ) : scalarData.SpectralWitness a where
  count := 1
  coefficient := fun _ => a
  vector := fun _ => 1
  decomposition := by simp
  nonzero := by intros; exact one_ne_zero
  idempotent := by intros; simp [scalarData]
  orthogonal := by intro i j h; exact False.elim (h (Subsingleton.elim i j))

#print axioms Data.trace_bracket
#print axioms Data.form_associative
#print axioms Data.form_bracket_skew
#print axioms Data.idempotent_peirce
#print axioms Data.trace_idempotent_pos
#print axioms Data.form_self_pos
#print axioms Data.form_self_nonneg
#print axioms Data.form_self_eq_zero_iff
#print axioms scalarSpectrum

end Po000JordanTrace
