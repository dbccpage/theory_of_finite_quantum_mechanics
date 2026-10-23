import WitnessedDifference.FiniteHermitianization

/-!
# Certified pure-ray separation and rational phases

The supplied compatible form and complex structure are the preceding R9
construction. Positive definiteness is an explicit additional hypothesis.
No preserver classification, arithmetic norm criterion or implementation
correctness is postulated here. This core-only module proves its declared
algebraic statements directly and is independent of the Python checker.
-/

namespace WitnessedDifference.CertifiedPreservers

open WitnessedDifference.FiniteHermitianization

set_option linter.checkUnivs false
set_option linter.unusedSimpArgs false
set_option maxHeartbeats 800000

universe u

def PositiveDefinite {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) : Prop :=
  ∀ x, F.form x x = 0 → x = vzero

theorem form_zero_left {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x : QVec ι) : F.form vzero x = 0 := by
  have hv : vzero = vsmul (0 : Rat) x := by
    funext i
    simp [vzero, vsmul]
  rw [hv, F.smul_left]
  grind

theorem form_positive {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (x : QVec ι) (hx : x ≠ vzero) : 0 < F.form x x := by
  have hn := F.nonnegative x
  have hne : F.form x x ≠ 0 := fun h => hx (hpos x h)
  grind

theorem form_smul_self {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (z : GaussianRat) (x : QVec ι) :
    F.form (complexSmul C z x) (complexSmul C z x) = gnorm z * F.form x x := by
  have h := congrArg GaussianRat.re (hermitian_smul_left F z x (complexSmul C z x))
  rw [hermitian_smul_right F z x x, hermitian_self] at h
  simp only [hermitian, gmul, gconj, gnorm] at h ⊢
  grind

/-- An unnormalised residual avoids any hidden square root or division. -/
def separationResidual {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) : QVec ι :=
  vadd (vsmul (F.form x x) y) (vneg (complexSmul C (hermitian F x y) x))

theorem separation_residual_identity {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) :
    F.form (separationResidual F x y) (separationResidual F x y) =
      F.form x x * (F.form x x * F.form y y - gnorm (hermitian F x y)) := by
  have hsym := F.symmetric y x
  have hJ := F.symmetric y (C.J x)
  have hxx := hermitian_self_im_zero F x
  simp only [hermitian] at hxx
  simp only [separationResidual, F.add_left, form_add_right,
    F.smul_left, form_smul_right, form_neg_left, form_neg_right,
    complexSmul, hermitian, gnorm, F.add_left, form_add_right,
    F.smul_left, form_smul_right, form_J_isometry]
  have hskew := F.J_skew x x
  grind

theorem cauchy_schwarz {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (x y : QVec ι) (hx : x ≠ vzero) :
    gnorm (hermitian F x y) ≤ F.form x x * F.form y y := by
  have hr := form_positive F hpos x hx
  have hn := F.nonnegative (separationResidual F x y)
  rw [separation_residual_identity] at hn
  have hm : F.form x x * 0 ≤
      F.form x x * (F.form x x * F.form y y - gnorm (hermitian F x y)) := by
    simpa using hn
  have he := Rat.le_of_mul_le_mul_left hm hr
  grind

def transition {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) : Rat :=
  gnorm (hermitian F x y) / (F.form x x * F.form y y)

theorem transition_bounds {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (x y : QVec ι) (hx : x ≠ vzero) (hy : y ≠ vzero) :
    0 ≤ transition F x y ∧ transition F x y ≤ 1 := by
  have hd := Rat.mul_pos (form_positive F hpos x hx) (form_positive F hpos y hy)
  have hdn : F.form x x * F.form y y ≠ 0 := by grind
  have hn := gnorm_nonnegative (hermitian F x y)
  have hc := cauchy_schwarz F hpos x y hx
  have he : transition F x y * (F.form x x * F.form y y) =
      gnorm (hermitian F x y) := Rat.div_mul_cancel hdn
  constructor
  · apply Rat.le_of_mul_le_mul_right (c := F.form x x * F.form y y) _ hd
    grind
  · apply Rat.le_of_mul_le_mul_right (c := F.form x x * F.form y y) _ hd
    grind

theorem transition_self {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (x : QVec ι) (hx : x ≠ vzero) : transition F x x = 1 := by
  have hr := form_positive F hpos x hx
  have hnn : F.form x x * F.form x x ≠ 0 := by
    have := Rat.mul_pos hr hr
    grind
  unfold transition
  rw [hermitian_self]
  simp only [gnorm]
  have hcancel := Rat.div_mul_cancel (a := F.form x x * F.form x x) hnn
  grind

def SameRay {ι : Type u} (C : ComplexStructure ι) (x y : QVec ι) : Prop :=
  ∃ z : GaussianRat, z ≠ gzero ∧ y = complexSmul C z x

theorem transition_one_implies_same_ray {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (x y : QVec ι) (hx : x ≠ vzero) (hy : y ≠ vzero)
    (hone : transition F x y = 1) : SameRay C x y := by
  have hr := form_positive F hpos x hx
  have hs := form_positive F hpos y hy
  have hrn : F.form x x ≠ 0 := by grind
  have hdn : F.form x x * F.form y y ≠ 0 := by
    have := Rat.mul_pos hr hs
    grind
  have he := Rat.div_mul_cancel (a := gnorm (hermitian F x y)) hdn
  change transition F x y * (F.form x x * F.form y y) = _ at he
  rw [hone] at he
  have hz : F.form (separationResidual F x y) (separationResidual F x y) = 0 := by
    rw [separation_residual_identity]
    grind
  have hw := hpos _ hz
  let z : GaussianRat := ⟨F.form x y / F.form x x, F.form (C.J x) y / F.form x x⟩
  have hmap : y = complexSmul C z x := by
    funext j
    have hj := congrFun hw j
    have ha := Rat.div_mul_cancel (a := F.form x y) hrn
    have hb := Rat.div_mul_cancel (a := F.form (C.J x) y) hrn
    simp only [separationResidual, vadd, vsmul, vneg, complexSmul, hermitian, vzero] at hj
    simp only [complexSmul, vadd, vsmul, z]
    grind
  refine ⟨z, ?_, hmap⟩
  intro hzero
  rw [hzero] at hmap
  have hyzero : y = vzero := by
    funext j
    have hj := congrFun hmap j
    simp only [complexSmul, gzero, vadd, vsmul, vzero] at hj ⊢
    grind
  exact hy hyzero

theorem gnorm_conj (z : GaussianRat) : gnorm (gconj z) = gnorm z := by
  simp only [gnorm, gconj]
  grind

theorem transition_scale_left {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) (z : GaussianRat) (hz : z ≠ gzero) :
    transition F (complexSmul C z x) y = transition F x y := by
  have hn : gnorm z ≠ 0 := fun h => hz (gnorm_eq_zero_iff z |>.mp h)
  unfold transition
  rw [hermitian_smul_left, gnorm_mul, gnorm_conj, form_smul_self]
  simp only [Rat.div_def, Rat.inv_mul_rev]
  have hc := Rat.mul_inv_cancel (gnorm z) hn
  grind

theorem transition_symmetric {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) :
    transition F x y = transition F y x := by
  unfold transition
  rw [hermitian_conjugate_symmetry F x y, gnorm_conj]
  rw [Rat.mul_comm (F.form x x) (F.form y y)]

theorem transition_scale_right {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) (z : GaussianRat) (hz : z ≠ gzero) :
    transition F x (complexSmul C z y) = transition F x y := by
  rw [transition_symmetric F x, transition_scale_left F y x z hz,
    transition_symmetric F y x]

theorem transition_representative_independent {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (x y : QVec ι) (a b : GaussianRat)
    (ha : a ≠ gzero) (hb : b ≠ gzero) :
    transition F (complexSmul C a x) (complexSmul C b y) = transition F x y := by
  rw [transition_scale_left F x _ a ha, transition_scale_right F x y b hb]

theorem table_injective_iff_same_ray {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (x y : QVec ι) (hx : x ≠ vzero) (hy : y ≠ vzero) :
    (∀ v, v ≠ vzero → transition F x v = transition F y v) ↔ SameRay C x y := by
  constructor
  · intro h
    apply transition_one_implies_same_ray F hpos x y hx hy
    rw [h y hy, transition_self F hpos y hy]
  · rintro ⟨z, hz, rfl⟩ v _
    exact (transition_scale_left F x v z hz).symm

/-- The rational circle, not merely four roots of unity, supplies equal-multiplier phases. -/
def phase (t : Rat) : GaussianRat :=
  ⟨(1-t*t)/(1+t*t), 2*t/(1+t*t)⟩

theorem phase_has_unit_norm (t : Rat) : gnorm (phase t) = 1 := by
  have ht := rat_square_nonnegative t
  have hd : 1+t*t ≠ 0 := by grind
  have ha := Rat.div_mul_cancel (a := 1-t*t) hd
  have hb := Rat.div_mul_cancel (a := 2*t) hd
  simp only [gnorm, phase]
  grind

theorem phase_counterexample :
    gnorm (⟨3/5, 4/5⟩ : GaussianRat) = 1 ∧
      (⟨3/5, 4/5⟩ : GaussianRat) ≠ gone ∧
      (⟨3/5, 4/5⟩ : GaussianRat) ≠ gneg gone ∧
      (⟨3/5, 4/5⟩ : GaussianRat) ≠ gi ∧
      (⟨3/5, 4/5⟩ : GaussianRat) ≠ gneg gi := by
  simp only [gnorm, gone, gneg, gi, ne_eq, GaussianRat.mk.injEq]
  grind

theorem phase_inverse (t : Rat) : (phase t).im / (1 + (phase t).re) = t := by
  have ht := rat_square_nonnegative t
  have hd : 1+t*t ≠ 0 := by grind
  have ha := Rat.div_mul_cancel (a := 1-t*t) hd
  have hb := Rat.div_mul_cancel (a := 2*t) hd
  have he : 1+(phase t).re ≠ 0 := by
    simp only [phase]
    grind
  have hc := Rat.div_mul_cancel (a := (phase t).im) he
  simp only [phase] at hc ⊢
  grind

theorem phase_injective (s t : Rat) (h : phase s = phase t) : s = t := by
  have hs := phase_inverse s
  have ht := phase_inverse t
  rw [h] at hs
  exact hs.symm.trans ht

theorem phase_covers_unit_norm (z : GaussianRat) (hn : gnorm z = 1)
    (hne : z.re ≠ -1) : z = phase (z.im / (1+z.re)) := by
  have hd : 1+z.re ≠ 0 := by grind
  let t := z.im / (1+z.re)
  have ht := rat_square_nonnegative t
  have htd : 1+t*t ≠ 0 := by grind
  have hc := Rat.div_mul_cancel (a := z.im) hd
  have ha := Rat.div_mul_cancel (a := 1-t*t) htd
  have hb := Rat.div_mul_cancel (a := 2*t) htd
  change z = phase t
  apply gaussian_ext <;> simp only [phase]
  all_goals
    simp only [gnorm] at hn
    change t*(1+z.re) = z.im at hc
    grind

theorem unit_norm_phase_classification (z : GaussianRat) :
    gnorm z = 1 ↔ z = gneg gone ∨ ∃ t : Rat, z = phase t := by
  constructor
  · intro hn
    by_cases h : z.re = -1
    · left
      have hb := rat_square_nonnegative z.im
      have hzero : z.im * z.im = 0 := by
        simp only [gnorm] at hn
        grind
      have hz : z.im = 0 := (Rat.mul_eq_zero.mp hzero).elim id id
      apply gaussian_ext <;> simp only [gneg, gone] <;> grind
    · exact Or.inr ⟨_, phase_covers_unit_norm z hn h⟩
  · rintro (rfl | ⟨t, rfl⟩)
    · simp only [gnorm, gneg, gone]
      grind
    · exact phase_has_unit_norm t

theorem equal_multiplier_iff_unit_phase (a : GaussianRat) (c : Rat) (hc : c ≠ 0) :
    gnorm a * c = c ↔ gnorm a = 1 := by
  constructor <;> intro h <;> grind

/-- The rational-linearity input is explicit; no field classification is an axiom. -/
structure RationalScalarHom where
  toFun : GaussianRat → GaussianRat
  map_add : ∀ z w, toFun (gadd z w) = gadd (toFun z) (toFun w)
  map_mul : ∀ z w, toFun (gmul z w) = gmul (toFun z) (toFun w)
  fix_rational : ∀ r : Rat, toFun ⟨r, 0⟩ = ⟨r, 0⟩

theorem square_minus_one_roots (z : GaussianRat) (h : gmul z z = gneg gone) :
    z = gi ∨ z = gneg gi := by
  have hre := congrArg GaussianRat.re h
  have him := congrArg GaussianRat.im h
  have ha := rat_square_nonnegative z.re
  simp only [gmul, gneg, gone] at hre him
  have hb : z.im ≠ 0 := by
    intro hzero
    simp only [hzero, Rat.mul_zero, Rat.sub_eq_add_neg, Rat.neg_zero, Rat.add_zero] at hre
    rw [hre] at ha
    grind
  have hz : z.re = 0 := by grind
  have hp : (z.im - 1)*(z.im + 1) = 0 := by grind
  rcases Rat.mul_eq_zero.mp hp with hplus | hminus
  · left
    apply gaussian_ext <;> simp only [gi] <;> grind
  · right
    apply gaussian_ext <;> simp only [gi, gneg] <;> grind

theorem rational_scalar_hom_two_branches (φ : RationalScalarHom) :
    (∀ z, φ.toFun z = z) ∨ (∀ z, φ.toFun z = gconj z) := by
  have hs := φ.map_mul gi gi
  rw [gi_square] at hs
  have hm : φ.toFun (gneg gone) = gneg gone := φ.fix_rational (-1)
  rw [hm] at hs
  have expand (z : GaussianRat) :
      φ.toFun z = gadd ⟨z.re, 0⟩ (gmul ⟨z.im, 0⟩ (φ.toFun gi)) := by
    have hz : z = gadd ⟨z.re, 0⟩ (gmul ⟨z.im, 0⟩ gi) := by
      apply gaussian_ext <;> simp only [gadd, gmul, gi] <;> grind
    conv => lhs; rw [hz]
    rw [φ.map_add, φ.map_mul, φ.fix_rational, φ.fix_rational]
  rcases square_minus_one_roots (φ.toFun gi) hs.symm with hi | hi
  · left
    intro z
    rw [expand, hi]
    apply gaussian_ext <;> simp only [gadd, gmul, gi] <;> grind
  · right
    intro z
    rw [expand, hi]
    apply gaussian_ext <;> simp only [gadd, gmul, gi, gneg, gconj] <;> grind

def gdivideReal (z : GaussianRat) (r : Rat) : GaussianRat := ⟨z.re/r, z.im/r⟩

def rayProjection {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (g x : QVec ι) : QVec ι :=
  complexSmul C (gdivideReal (hermitian F g x) (F.form g g)) g

theorem projection_pairing {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (g x : QVec ι) (hg : F.form g g ≠ 0) :
    hermitian F g (rayProjection F g x) = hermitian F g x := by
  unfold rayProjection
  rw [hermitian_smul_right, hermitian_self]
  have ha := Rat.div_mul_cancel (a := (hermitian F g x).re) hg
  have hb := Rat.div_mul_cancel (a := (hermitian F g x).im) hg
  apply gaussian_ext <;> simp only [gdivideReal, gmul] <;> grind

theorem projection_idempotent {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (g x : QVec ι) (hg : F.form g g ≠ 0) :
    rayProjection F g (rayProjection F g x) = rayProjection F g x := by
  change complexSmul C
    (gdivideReal (hermitian F g (rayProjection F g x)) (F.form g g)) g = _
  rw [projection_pairing F g x hg]
  rfl

theorem projection_selfadjoint {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (g x y : QVec ι) :
    hermitian F (rayProjection F g x) y = hermitian F x (rayProjection F g y) := by
  unfold rayProjection
  rw [hermitian_smul_left, hermitian_smul_right,
    hermitian_conjugate_symmetry F x g]
  apply gaussian_ext <;> simp only [gdivideReal, gmul, gconj, Rat.div_def] <;> grind

theorem projection_probability {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (g x : QVec ι) (hg : F.form g g ≠ 0) :
    F.form (rayProjection F g x) (rayProjection F g x) / F.form x x =
      transition F x g := by
  unfold rayProjection
  rw [form_smul_self]
  have ha := Rat.div_mul_cancel (a := (hermitian F g x).re) hg
  have hb := Rat.div_mul_cancel (a := (hermitian F g x).im) hg
  have hn := Rat.mul_inv_cancel (F.form g g) hg
  have hs := hermitian_conjugate_symmetry F g x
  have hre := congrArg GaussianRat.re hs
  have him := congrArg GaussianRat.im hs
  simp only [transition, gnorm, gdivideReal, Rat.div_def, Rat.inv_mul_rev, gconj] at *
  grind

theorem projection_zero_iff_zero_probability {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (g x : QVec ι) (hg : g ≠ vzero) (hx : x ≠ vzero) :
    rayProjection F g x = vzero ↔ transition F x g = 0 := by
  have hgn : F.form g g ≠ 0 := by have := form_positive F hpos g hg; grind
  have hxn : F.form x x ≠ 0 := by have := form_positive F hpos x hx; grind
  have hp := projection_probability F g x hgn
  constructor
  · intro hz
    rw [hz, form_zero_left] at hp
    simp only [Rat.div_def, Rat.zero_mul] at hp
    exact hp.symm
  · intro hz
    apply hpos
    have hc := Rat.div_mul_cancel
      (a := F.form (rayProjection F g x) (rayProjection F g x)) hxn
    rw [hp, hz] at hc
    grind

theorem projection_same_ray_at_positive_probability {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (hpos : PositiveDefinite F)
    (g x : QVec ι) (hg : g ≠ vzero) (hx : x ≠ vzero)
    (hp : 0 < transition F x g) : SameRay C g (rayProjection F g x) := by
  refine ⟨gdivideReal (hermitian F g x) (F.form g g), ?_, rfl⟩
  intro hz
  have he : rayProjection F g x = vzero := by
    unfold rayProjection
    rw [hz]
    funext j
    simp only [complexSmul, gzero, vadd, vsmul, vzero]
    grind
  have hzero := (projection_zero_iff_zero_probability F hpos g x hg hx).mp he
  grind

theorem projection_complement_mass {ι : Type u} {C : ComplexStructure ι}
    (F : CompatibleForm C) (g x : QVec ι) (hg : F.form g g ≠ 0) :
    F.form (rayProjection F g x) (rayProjection F g x) +
      F.form (vadd x (vneg (rayProjection F g x)))
        (vadd x (vneg (rayProjection F g x))) = F.form x x := by
  have hs := congrArg GaussianRat.re (projection_selfadjoint F g x (rayProjection F g x))
  rw [projection_idempotent F g x hg] at hs
  have hsym := F.symmetric (rayProjection F g x) x
  simp only [hermitian] at hs
  simp only [F.add_left, form_add_right, form_neg_left, form_neg_right]
  grind

end WitnessedDifference.CertifiedPreservers

#print axioms WitnessedDifference.CertifiedPreservers.separation_residual_identity
#print axioms WitnessedDifference.CertifiedPreservers.transition_bounds
#print axioms WitnessedDifference.CertifiedPreservers.table_injective_iff_same_ray
#print axioms WitnessedDifference.CertifiedPreservers.transition_scale_left
#print axioms WitnessedDifference.CertifiedPreservers.transition_representative_independent
#print axioms WitnessedDifference.CertifiedPreservers.phase_has_unit_norm
#print axioms WitnessedDifference.CertifiedPreservers.phase_counterexample
#print axioms WitnessedDifference.CertifiedPreservers.phase_injective
#print axioms WitnessedDifference.CertifiedPreservers.unit_norm_phase_classification
#print axioms WitnessedDifference.CertifiedPreservers.equal_multiplier_iff_unit_phase
#print axioms WitnessedDifference.CertifiedPreservers.rational_scalar_hom_two_branches
#print axioms WitnessedDifference.CertifiedPreservers.projection_idempotent
#print axioms WitnessedDifference.CertifiedPreservers.projection_selfadjoint
#print axioms WitnessedDifference.CertifiedPreservers.projection_probability
#print axioms WitnessedDifference.CertifiedPreservers.projection_zero_iff_zero_probability
#print axioms WitnessedDifference.CertifiedPreservers.projection_same_ray_at_positive_probability
#print axioms WitnessedDifference.CertifiedPreservers.projection_complement_mass
