import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.Finset.Card

/-!
# Collapsed observation barrier: when does a function of the quotient separate?

AuthorityEffect: None.  Source: `PreMssn.collapsed_observation_barrier` (Paper.lean line 36, a general theorem,
re-proved here), `history_report_criterion` (line 10, the `ReportImage` form), `refine_separates` (line 64).
The node statement is nearly a tautology: `s = g ∘ p` forces `s` to be constant on the fibres of `p`.
The sharp content proved here:

* `factors_iff_of_nonempty`: a factorisation `s = g ∘ p` through the whole profile codomain exists iff `s` is
  constant on the fibres of `p`, whenever `Z` is inhabited.  `factors_iff_exact` gives the exact criterion for all
  `Z`: fibre-constant and (`Z` inhabited or `Y` empty).  The plain iff fails when `Z` is empty and `Y` is not
  (`factors_iff_fails_without_nonempty`: empty `X`, `Y = Unit`, empty `Z`); the source's `ReportImage` form
  (factor through the image of `p` only) is the unconditional one (`factorsImage_iff`).
* `tag_separates`: if `s` factors through the refined profile `(p, t)` then `t` separates every
  collapsed pair that `s` separates (the added tag lives outside the quotient).
* `tag_alphabet_iff`: with `Nonempty T` and `Nonempty Z`, a tag `t : X -> T` with `s` factoring through `(p, t)` exists
  iff every profile fibre carries at most `card T` distinct task values (so the least nonempty alphabet is
  `max 1 (largest number of distinct task values in one fibre)`; the empty alphabet works exactly for empty `X`).
  All carriers are in `Type` (universe 0).

No claim is made about which tag is physically or mathematically selected: the node does not select one.
-/

namespace CollapseBarrier

variable {X Y Z T : Type}

/-- `s` is a function of the profile `p`. -/
def Factors (p : X → Y) (s : X → Z) : Prop := ∃ g : Y → Z, ∀ x, g (p x) = s x

/-- Source theorem, general form: equal profiles and different task values block every factorisation. -/
theorem barrier (p : X → Y) (s : X → Z) (x x' : X) (same : p x = p x') (diff : s x ≠ s x') :
    ¬ Factors p s := by
  rintro ⟨g, hg⟩
  apply diff
  rw [← hg x, ← hg x', same]

/-- A factorisation forces `s` to be constant on fibres (always true, no hypotheses on `Z`). -/
theorem fibre_constant_of_factors {p : X → Y} {s : X → Z} (h : Factors p s) :
    ∀ x x', p x = p x' → s x = s x' := by
  intro x x' same
  by_contra diff
  exact barrier p s x x' same diff h

/-- Sharp converse: with `Z` inhabited, fibre-constancy is sufficient. -/
theorem factors_of_fibre_constant [Nonempty Z] [DecidableEq Y] (p : X → Y) (s : X → Z)
    (h : ∀ x x', p x = p x' → s x = s x') : Factors p s := by
  classical
  refine ⟨fun y => if hy : ∃ x, p x = y then s (Classical.choose hy) else Classical.arbitrary Z, ?_⟩
  intro x
  have hy : ∃ x', p x' = p x := ⟨x, rfl⟩
  show (if hy : ∃ x', p x' = p x then s (Classical.choose hy) else Classical.arbitrary Z) = s x
  simp only [hy, dite_true]
  exact h _ _ (Classical.choose_spec hy)

theorem factors_iff_of_nonempty [Nonempty Z] [DecidableEq Y] (p : X → Y) (s : X → Z) :
    Factors p s ↔ ∀ x x', p x = p x' → s x = s x' :=
  ⟨fibre_constant_of_factors, factors_of_fibre_constant p s⟩

/-- Exact criterion for all `Z`: fibre-constant, and either `Z` is inhabited or `Y` is empty. -/
theorem factors_iff_exact [DecidableEq Y] (p : X → Y) (s : X → Z) :
    Factors p s ↔ (∀ x x', p x = p x' → s x = s x') ∧ (Nonempty Z ∨ IsEmpty Y) := by
  by_cases hz : Nonempty Z
  · rw [factors_iff_of_nonempty p s]
    exact ⟨fun h => ⟨h, Or.inl hz⟩, fun h => h.1⟩
  · have hZ : IsEmpty Z := not_nonempty_iff.mp hz
    constructor
    · intro h
      refine ⟨fibre_constant_of_factors h, Or.inr ⟨fun y => ?_⟩⟩
      obtain ⟨g, _⟩ := h
      exact hZ.false (g y)
    · rintro ⟨_, h | h⟩
      · exact absurd h hz
      · exact ⟨fun y => isEmptyElim y, fun x => isEmptyElim (p x)⟩

/-- Boundary: the iff is false without `Nonempty Z`.  Empty `X`, one profile value, empty `Z`. -/
theorem factors_iff_fails_without_nonempty :
    ∃ (p : Empty → Unit) (s : Empty → Empty),
      (∀ x x', p x = p x' → s x = s x') ∧ ¬ Factors p s := by
  refine ⟨fun e => e.elim, fun e => e.elim, fun x => x.elim, ?_⟩
  rintro ⟨g, _⟩
  exact (g ()).elim

/-- Unconditional form (the source `ReportImage` form): factor through the image of `p` only. -/
def FactorsImage (p : X → Y) (s : X → Z) : Prop :=
  ∃ g : {y : Y // ∃ x, p x = y} → Z, ∀ x, g ⟨p x, ⟨x, rfl⟩⟩ = s x

theorem factorsImage_iff (p : X → Y) (s : X → Z) :
    FactorsImage p s ↔ ∀ x x', p x = p x' → s x = s x' := by
  classical
  constructor
  · rintro ⟨g, hg⟩ x x' same
    have hv : (⟨p x, ⟨x, rfl⟩⟩ : {y : Y // ∃ x, p x = y}) = ⟨p x', ⟨x', rfl⟩⟩ := Subtype.ext same
    rw [← hg x, ← hg x', hv]
  · intro h
    refine ⟨fun v => s (Classical.choose v.property), fun x => ?_⟩
    exact h _ _ (Classical.choose_spec (show ∃ x', p x' = p x from ⟨x, rfl⟩))

/-- The refined profile with an added tag. -/
def refine (p : X → Y) (t : X → T) : X → Y × T := fun x => (p x, t x)

theorem refine_fst (p : X → Y) (t : X → T) (x : X) : (refine p t x).1 = p x := rfl

/-- A tag that separates the pair separates it in the refined profile (source `refine_separates`). -/
theorem refine_separates (p : X → Y) (t : X → T) (x x' : X) (diff : t x ≠ t x') :
    refine p t x ≠ refine p t x' := by
  intro h
  exact diff (congrArg Prod.snd h)

/-- If the task factors through the refined profile, the tag separates every collapsed pair the task separates. -/
theorem tag_separates {p : X → Y} {t : X → T} {s : X → Z} (h : Factors (refine p t) s)
    (x x' : X) (same : p x = p x') (diff : s x ≠ s x') : t x ≠ t x' := by
  intro ht
  exact diff (fibre_constant_of_factors h x x' (by simp [refine, same, ht]))

/-- Lower bound on the size of the added tag alphabet: `m` task values met inside one fibre need `m` tag values. -/
theorem tag_card_lower_bound [Fintype T] {p : X → Y} {t : X → T} {s : X → Z}
    (h : Factors (refine p t) s) (S : Finset X)
    (hp : ∀ x ∈ S, ∀ x' ∈ S, p x = p x') (hs : Set.InjOn s S) :
    S.card ≤ Fintype.card T := by
  classical
  have hinj : Set.InjOn t S := by
    intro x hx x' hx' ht
    by_contra hne
    have : s x ≠ s x' := fun e => hne (hs hx hx' e)
    exact tag_separates h x x' (hp x hx x' hx') this ht
  exact Finset.card_le_card_of_injOn t (fun x _ => Finset.mem_univ _) hinj |>.trans (by simp)

/-- Sufficiency: if every fibre carries at most `card T` distinct task values, some tag works. -/
theorem tag_exists [Fintype X] [DecidableEq Y] [DecidableEq Z] [Fintype T] [Nonempty T] [Nonempty Z]
    (p : X → Y) (s : X → Z)
    (hcard : ∀ y : Y, ((Finset.univ.filter (fun x => p x = y)).image s).card ≤ Fintype.card T) :
    ∃ t : X → T, Factors (refine p t) s := by
  classical
  let V : Y → Finset Z := fun y => (Finset.univ.filter (fun x => p x = y)).image s
  let E : Y → Z → T := fun y z =>
    if h : z ∈ V y then
      (Fintype.equivFin T).symm (Fin.castLE (hcard y) ((V y).equivFin ⟨z, h⟩))
    else Classical.arbitrary T
  have Einj : ∀ y z z', z ∈ V y → z' ∈ V y → E y z = E y z' → z = z' := by
    intro y z z' hz hz' hE
    simp only [E, hz, hz', dite_true] at hE
    have h1 := (Fintype.equivFin T).symm.injective hE
    have h2 := Fin.castLE_injective (hcard y) h1
    have h3 := (V y).equivFin.injective h2
    exact congrArg Subtype.val h3
  refine ⟨fun x => E (p x) (s x), ?_⟩
  apply (factors_iff_of_nonempty (refine p (fun x => E (p x) (s x))) s).mpr
  intro x x' same
  have hp : p x = p x' := congrArg Prod.fst same
  have ht : E (p x) (s x) = E (p x) (s x') := by
    have := congrArg Prod.snd same
    simpa [refine, ← hp] using this
  have hx : s x ∈ V (p x) := Finset.mem_image.mpr ⟨x, by simp, rfl⟩
  have hx' : s x' ∈ V (p x) := Finset.mem_image.mpr ⟨x', by simp [hp], rfl⟩
  exact Einj _ _ _ hx hx' ht

/-- Exact alphabet criterion (nonempty tag alphabet, inhabited task codomain). -/
theorem tag_alphabet_iff [Fintype X] [DecidableEq Y] [DecidableEq Z] [Fintype T] [Nonempty T] [Nonempty Z]
    (p : X → Y) (s : X → Z) :
    (∃ t : X → T, Factors (refine p t) s) ↔
      ∀ y : Y, ((Finset.univ.filter (fun x => p x = y)).image s).card ≤ Fintype.card T := by
  constructor
  · rintro ⟨t, h⟩ y
    classical
    let V := (Finset.univ.filter (fun x => p x = y)).image s
    let φ : V → T := fun v => t (Classical.choose (Finset.mem_image.mp v.2))
    have hφ : Function.Injective φ := by
      intro v1 v2 hv
      have h1 := Classical.choose_spec (Finset.mem_image.mp v1.2)
      have h2 := Classical.choose_spec (Finset.mem_image.mp v2.2)
      apply Subtype.ext
      by_contra hne
      have hp1 : p (Classical.choose (Finset.mem_image.mp v1.2)) = y := by
        simpa using (Finset.mem_filter.mp h1.1).2
      have hp2 : p (Classical.choose (Finset.mem_image.mp v2.2)) = y := by
        simpa using (Finset.mem_filter.mp h2.1).2
      apply tag_separates h _ _ (hp1.trans hp2.symm) (by rw [h1.2, h2.2]; exact hne)
      exact hv
    have := Fintype.card_le_of_injective φ hφ
    simpa using this
  · exact tag_exists p s

/-- Binary instance (labelled): one added bit suffices for the pair `0 / 1` on a collapsed two-point carrier. -/
theorem two_point_one_bit :
    ∃ t : Bool → Bool, Factors (refine (fun _ : Bool => ()) t) (fun b : Bool => b) :=
  ⟨id, fun ⟨_, b⟩ => b, fun _ => rfl⟩

theorem two_point_no_factor : ¬ Factors (fun _ : Bool => ()) (fun b : Bool => b) :=
  barrier _ _ false true rfl (by decide)

end CollapseBarrier

#print axioms CollapseBarrier.barrier
#print axioms CollapseBarrier.factors_iff_of_nonempty
#print axioms CollapseBarrier.factors_iff_exact
#print axioms CollapseBarrier.factors_iff_fails_without_nonempty
#print axioms CollapseBarrier.factorsImage_iff
#print axioms CollapseBarrier.refine_separates
#print axioms CollapseBarrier.tag_separates
#print axioms CollapseBarrier.tag_card_lower_bound
#print axioms CollapseBarrier.tag_exists
#print axioms CollapseBarrier.tag_alphabet_iff
#print axioms CollapseBarrier.two_point_one_bit
#print axioms CollapseBarrier.two_point_no_factor
