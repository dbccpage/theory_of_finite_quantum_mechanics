import Core
import Derivation.Basic

/-!
AuthorityEffect: None. Certified map from the sealed Genesis interpreter to
the actual local finite-obstruction PrimitiveDifference carrier. Its zero
relation is contextual collapse, not syntactic inequality of datum indices.
The source-pin receipt binds Basic.lean to the sealed tag 3100c4e.
-/

namespace CampaignGenesisCarrierBridge

abbrev Datum (r : Derivation.Regime) := Fin r.data

def sourceRelation (r : Derivation.Regime) (i j : Datum r) : Prop :=
  Derivation.collapsed r i.val j.val

theorem source_relation_refl (r : Derivation.Regime) (i : Datum r) :
    sourceRelation r i i := fun _ _ => Iff.rfl

theorem source_relation_symm (r : Derivation.Regime) {i j : Datum r}
    (h : sourceRelation r i j) : sourceRelation r j i := fun c hc => (h c hc).symm

theorem source_relation_trans (r : Derivation.Regime) {i j k : Datum r}
    (h : sourceRelation r i j) (g : sourceRelation r j k) : sourceRelation r i k :=
  fun c hc => (h c hc).trans (g c hc)

/-- A term of the book's candidate structure, with its actual three zero laws. -/
def certifiedDifference (r : Derivation.Regime) :
    GrokPdNight20260814.Core.PrimitiveDifference (Datum r) Prop where
  δ := sourceRelation r
  Zero := id
  zero_refl := source_relation_refl r
  zero_symm := fun _ _ => source_relation_symm r
  zero_trans := fun _ _ _ => source_relation_trans r

def certifiedSetoid (r : Derivation.Regime) : Setoid (Datum r) where
  r := GrokPdNight20260814.Core.ZeroRel (certifiedDifference r)
  iseqv := ⟨source_relation_refl r, source_relation_symm r, source_relation_trans r⟩

abbrev CertifiedCarrier (r : Derivation.Regime) := Quotient (certifiedSetoid r)

def termMap (r : Derivation.Regime) (d : Datum r) : CertifiedCarrier r :=
  Quotient.mk _ d

theorem certified_zero_iff (r : Derivation.Regime) (i j : Datum r) :
    GrokPdNight20260814.Core.ZeroRel (certifiedDifference r) i j ↔
      Derivation.collapsed r i.val j.val := Iff.rfl

theorem termMap_eq_iff (r : Derivation.Regime) (i j : Datum r) :
    termMap r i = termMap r j ↔ Derivation.collapsed r i.val j.val :=
  ⟨fun h => Quotient.exact h, fun h => Quotient.sound h⟩

theorem termMap_surjective (r : Derivation.Regime) : Function.Surjective (termMap r) := by
  intro q
  induction q using Quotient.inductionOn with
  | h d => exact ⟨d, rfl⟩

theorem separation_gives_raw_distinction (r : Derivation.Regime) (i j : Datum r)
    (h : Derivation.separable r i.val j.val) :
    termMap r i ≠ termMap r j :=
  fun he => Derivation.separable_not_collapsed h ((termMap_eq_iff r i j).mp he)

/-- The exact factorization criterion; no arbitrary source event is presumed faithful. -/
theorem factorization_iff (r s : Derivation.Regime) (f : Datum r → Datum s) :
    (∃ F : CertifiedCarrier r → CertifiedCarrier s,
      ∀ d, F (termMap r d) = termMap s (f d)) ↔
    (∀ i j, Derivation.collapsed r i.val j.val →
      Derivation.collapsed s (f i).val (f j).val) := by
  constructor
  · rintro ⟨F, hF⟩ i j hij
    apply (termMap_eq_iff s (f i) (f j)).mp
    rw [← hF i, ← hF j]
    exact congrArg F ((termMap_eq_iff r i j).mpr hij)
  · intro hf
    refine ⟨Quotient.lift (fun d => termMap s (f d)) ?_, fun _ => rfl⟩
    intro i j hij
    exact (termMap_eq_iff s (f i) (f j)).mpr (hf i j hij)

def separated : Derivation.Regime := ⟨2, [1], [(0, [0])], [], [(0, 1)]⟩
def ruled : Derivation.Regime := { separated with rules := [0] }
def empty : Derivation.Regime := ⟨0, [], [], [], []⟩

theorem sealed_response_reaches_separated :
    Derivation.applyDelta Derivation.R2L [.newForm 1, .newInst 0 [0]] = some separated := by
  decide

theorem separated_witness : Derivation.separable separated 0 1 := by
  refine ⟨⟨0, [none]⟩, ?_, ?_⟩
  · decide
  · decide

theorem sealed_image_has_raw_distinction :
    ∃ x y : CertifiedCarrier separated, x ≠ y :=
  ⟨termMap separated ⟨0, by decide⟩, termMap separated ⟨1, by decide⟩,
    separation_gives_raw_distinction separated _ _ separated_witness⟩

theorem undeclared_marks_collapse (i j : Datum Derivation.R2L) :
    termMap Derivation.R2L i = termMap Derivation.R2L j := by
  apply (termMap_eq_iff _ _ _).mpr
  intro c hc
  have hf := hc.1
  simp [Derivation.R2L] at hf

theorem uniform_rule_erases_distinction (i j : Datum ruled) :
    termMap ruled i = termMap ruled j := by
  apply (termMap_eq_iff _ _ _).mpr
  intro c hc
  have hf : c.form = 0 := by
    have h := hc.1
    simp only [ruled, separated, List.length_cons, List.length_nil] at h
    omega
  have hi : Derivation.derivable ruled (Derivation.plug c i.val) := by
    exact Or.inr (by simp [Derivation.plug, hf, ruled])
  have hj : Derivation.derivable ruled (Derivation.plug c j.val) := by
    exact Or.inr (by simp [Derivation.plug, hf, ruled])
  exact iff_of_true hi hj

theorem inert_inscription_has_no_distinction :
    ¬ ∃ x y : CertifiedCarrier empty, x ≠ y := by
  rintro ⟨x, y, _⟩
  induction x using Quotient.inductionOn with
  | h d => exact Fin.elim0 d

end CampaignGenesisCarrierBridge

#print axioms CampaignGenesisCarrierBridge.source_relation_refl
#print axioms CampaignGenesisCarrierBridge.source_relation_symm
#print axioms CampaignGenesisCarrierBridge.source_relation_trans
#print axioms CampaignGenesisCarrierBridge.certified_zero_iff
#print axioms CampaignGenesisCarrierBridge.termMap_eq_iff
#print axioms CampaignGenesisCarrierBridge.termMap_surjective
#print axioms CampaignGenesisCarrierBridge.separation_gives_raw_distinction
#print axioms CampaignGenesisCarrierBridge.factorization_iff
#print axioms CampaignGenesisCarrierBridge.sealed_response_reaches_separated
#print axioms CampaignGenesisCarrierBridge.separated_witness
#print axioms CampaignGenesisCarrierBridge.sealed_image_has_raw_distinction
#print axioms CampaignGenesisCarrierBridge.undeclared_marks_collapse
#print axioms CampaignGenesisCarrierBridge.uniform_rule_erases_distinction
#print axioms CampaignGenesisCarrierBridge.inert_inscription_has_no_distinction
