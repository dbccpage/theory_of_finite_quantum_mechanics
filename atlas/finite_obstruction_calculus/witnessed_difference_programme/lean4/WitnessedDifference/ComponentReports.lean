/-!
# Component reports: report/query factorization, function gluing, separation

Lean-core statements for the finite parts of the derivation proposals DP-1,
DP-6 and DP-2 (`coda_wdp_derivations_20261006`). Only `Init` is imported.

* DP-1. A query `q : X → B` has a decoder on the realized image of a report
  `p : X → A` exactly when `q` is constant on the fibres of `p`; the decoder is
  unique on that image; otherwise there is a colliding pair. Factorization
  transfers from a coarse report to a refinement, and the converse fails on a
  four-point carrier. Codomain membership is part of the type of `p`, so no
  countermodel to its necessity is stated.
* DP-6. Total functions on a family of subsets that agree on every overlap
  glue to exactly one function on the union; failure of agreement is witnessed
  by one point and two contexts. Two finite presheaves on the cover
  `{a}, {b}` of `{a, b}` have zero and two global extensions of a matching
  family.
* DP-2. The zero-distance relation of a rational pseudometric is an
  equivalence; the inherited distance on a quotient by `E` is well defined iff
  `E` is contained in the zero relation, and separated iff `E` equals it. The
  indiscrete pseudometric has a quotient with at most one point (exactly one
  when the source is nonempty). A decoder with error at
  most `ε` bounds fibre diameters by `2ε`; `2ε < Δ` forces equivalence, and
  the equality case `2ε = Δ` has a countermodel.

Scope: types are arbitrary; finiteness is used only in the `decide` fixtures.
Rational arithmetic is Lean core `Rat`. AuthorityEffect: None.
-/
namespace WitnessedDifference.ComponentReports

universe u v w

/-! ## DP-1: report/query factorization on the realized image -/

section Factorization

variable {X : Type u} {A : Type v} {B : Type w}

/-- The realized image `P = p(X)` of a report. -/
def Image (p : X → A) : Type v := {a : A // ∃ x, p x = a}

/-- The point `p x` of the realized image. -/
def Image.of (p : X → A) (x : X) : Image p := ⟨p x, x, rfl⟩

/-- `D` is a decoder on the realized image: `D (p x) = q x` for every `x`. -/
def IsDecoder (p : X → A) (q : X → B) (D : Image p → B) : Prop :=
  ∀ x, D (Image.of p x) = q x

/-- `q` is constant on every fibre of `p`. -/
def FiberConstant (p : X → A) (q : X → B) : Prop :=
  ∀ x y, p x = p y → q x = q y

/-- A colliding pair: equal reports and unequal query values. -/
def Collision (p : X → A) (q : X → B) : Prop :=
  ∃ x y, p x = p y ∧ q x ≠ q y

/-- DP-1: a decoder on the realized image exists iff `q` is fibre-constant. -/
theorem decoder_exists_iff_fiber_constant (p : X → A) (q : X → B) :
    (∃ D, IsDecoder p q D) ↔ FiberConstant p q := by
  constructor
  · rintro ⟨D, hD⟩ x y hxy
    have hpt : Image.of p x = Image.of p y := Subtype.ext hxy
    rw [← hD x, ← hD y, hpt]
  · intro hconst
    refine ⟨fun a => q (Classical.choose a.2), ?_⟩
    intro x
    have hspec : p (Classical.choose (Image.of p x).2) = p x :=
      Classical.choose_spec (Image.of p x).2
    exact hconst _ _ hspec

/-- DP-1: the decoder on the realized image is unique. -/
theorem decoder_unique (p : X → A) (q : X → B) (D E : Image p → B)
    (hD : IsDecoder p q D) (hE : IsDecoder p q E) : D = E := by
  funext a
  obtain ⟨a, x, rfl⟩ := a
  exact (hD x).trans (hE x).symm

/-- DP-1: failure of fibre-constancy is exactly a colliding pair. -/
theorem not_fiber_constant_iff_collision (p : X → A) (q : X → B) :
    ¬ FiberConstant p q ↔ Collision p q := by
  constructor
  · intro h
    apply Classical.byContradiction
    intro hno
    apply h
    intro x y hxy
    apply Classical.byContradiction
    intro hne
    exact hno ⟨x, y, hxy, hne⟩
  · rintro ⟨x, y, hxy, hne⟩ hconst
    exact hne (hconst x y hxy)

/-- DP-1: exactly one of the two outcomes holds (decoder or collision). -/
theorem decoder_xor_collision (p : X → A) (q : X → B) :
    ((∃ D, IsDecoder p q D) ∨ Collision p q) ∧
      ¬ ((∃ D, IsDecoder p q D) ∧ Collision p q) := by
  rw [decoder_exists_iff_fiber_constant, ← not_fiber_constant_iff_collision]
  constructor
  · exact Classical.em _
  · rintro ⟨h, hn⟩
    exact hn h

/-- DP-1: the empty source has a decoder, even into an empty output type. -/
theorem empty_source_has_decoder (p : Empty → A) (q : Empty → B) :
    ∃ D, IsDecoder p q D := by
  refine ⟨fun a => (Classical.choose a.2).elim, ?_⟩
  intro x
  exact x.elim

/-- DP-1: factorization transfers from a coarse report `p` to a refinement
`pf` with `p = h ∘ pf`. -/
theorem refinement_transfers {Af : Type v} (pf : X → Af) (h : Af → A)
    (p : X → A) (q : X → B) (hcomm : ∀ x, p x = h (pf x))
    (hcoarse : FiberConstant p q) : FiberConstant pf q := by
  intro x y hxy
  apply hcoarse
  rw [hcomm x, hcomm y, hxy]

/-- The four-point converse countermodel: fine report `id`, coarse report the
first coordinate, query the second coordinate. -/
def fineReport (x : Bool × Bool) : Bool × Bool := x
def coarseReport (x : Bool × Bool) : Bool := x.1
def secondQuery (x : Bool × Bool) : Bool := x.2

/-- DP-1: the converse of refinement transfer fails. -/
theorem refinement_converse_fails :
    FiberConstant fineReport secondQuery ∧
      (∀ x, coarseReport x = Prod.fst (fineReport x)) ∧
      Collision coarseReport secondQuery := by
  refine ⟨?_, fun _ => rfl, ⟨(false, false), (false, true), rfl, ?_⟩⟩
  · intro x y hxy
    simp only [fineReport] at hxy
    rw [hxy]
  · decide

/-- The positive DP-1 fixture `X = {x0,x1,x2}`, `p = (0,0,1)`, with query
values coded `0 ↦ 1/3`, `1 ↦ 2/3`. -/
def fixtureReport : Fin 3 → Nat
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 0
  | ⟨_, _⟩ => 1

/-- Query codes: `1` stands for `1/3`, `2` for `2/3`. -/
def fixtureQueryCode : Fin 3 → Nat
  | ⟨0, _⟩ => 1
  | ⟨1, _⟩ => 1
  | ⟨_, _⟩ => 2

/-- The rational query values `(1/3, 1/3, 2/3)`. -/
def fixtureQuery (x : Fin 3) : Rat := (fixtureQueryCode x : Rat) / 3

/-- DP-1: the positive fixture's code query is fibre-constant (by `decide`). -/
theorem fixture_code_fiber_constant :
    FiberConstant fixtureReport fixtureQueryCode := by
  unfold FiberConstant; decide

/-- DP-1: the positive fixture is factorable with rational values. -/
theorem fixture_factorable : ∃ D, IsDecoder fixtureReport fixtureQuery D := by
  rw [decoder_exists_iff_fiber_constant]
  intro x y hxy
  unfold fixtureQuery
  rw [fixture_code_fiber_constant x y hxy]

/-- DP-1 "not sufficient" fixture: constant report, identity query on `{0,1}`;
profile metadata passing does not prevent the collision `(0,1)`. -/
theorem constant_report_collides :
    Collision (fun _ : Bool => (0 : Nat)) (fun b : Bool => b) :=
  ⟨false, true, rfl, by decide⟩

/-- DP-1: a decoder required on all of `A` is not unique outside the image. -/
theorem decoder_off_image_not_unique :
    ∃ D E : Bool → Bool, D ≠ E ∧
      D ((fun _ : Unit => false) ()) = (fun _ : Unit => false) () ∧
      E ((fun _ : Unit => false) ()) = (fun _ : Unit => false) () :=
  ⟨fun _ => false, fun b => b, fun h => by
    have := congrFun h true
    exact Bool.noConfusion this, rfl, rfl⟩

end Factorization

/-! ## DP-6: gluing of total functions on a cover -/

section Gluing

variable {X : Type u} {I : Type v} {B : Type w}

/-- The union of a family of subsets. -/
def Union (U : I → X → Prop) : Type u := {x : X // ∃ i, U i x}

/-- Local sections agree on every pairwise overlap. -/
def Compatible (U : I → X → Prop) (s : (i : I) → {x // U i x} → B) : Prop :=
  ∀ i j x (hi : U i x) (hj : U j x), s i ⟨x, hi⟩ = s j ⟨x, hj⟩

/-- A global function on the union restricting to every local section. -/
def Restricts (U : I → X → Prop) (s : (i : I) → {x // U i x} → B)
    (g : Union U → B) : Prop :=
  ∀ i x (hi : U i x), g ⟨x, i, hi⟩ = s i ⟨x, hi⟩

/-- DP-6: compatible sections glue to exactly one function on the union. -/
theorem glue_exists_unique (U : I → X → Prop) (s : (i : I) → {x // U i x} → B)
    (hc : Compatible U s) : ∃ g, Restricts U s g ∧
      ∀ g', Restricts U s g' → g' = g := by
  refine ⟨fun y => s (Classical.choose y.2) ⟨y.1, Classical.choose_spec y.2⟩,
    ?_, ?_⟩
  · intro i x hi
    exact hc _ _ _ _ _
  · intro g' hg'
    funext y
    obtain ⟨x, hx⟩ := y
    have := hg' (Classical.choose hx) x (Classical.choose_spec hx)
    exact this

/-- DP-6: existence of a restricting global function forces compatibility. -/
theorem compatible_of_restricts (U : I → X → Prop)
    (s : (i : I) → {x // U i x} → B) (g : Union U → B)
    (hg : Restricts U s g) : Compatible U s := by
  intro i j x hi hj
  rw [← hg i x hi, ← hg j x hj]

/-- DP-6: incompatibility is witnessed by one point and two contexts. -/
theorem not_compatible_iff_witness (U : I → X → Prop)
    (s : (i : I) → {x // U i x} → B) :
    ¬ Compatible U s ↔
      ∃ i j x, ∃ (hi : U i x) (hj : U j x), s i ⟨x, hi⟩ ≠ s j ⟨x, hj⟩ := by
  constructor
  · intro h
    apply Classical.byContradiction
    intro hno
    apply h
    intro i j x hi hj
    apply Classical.byContradiction
    intro hne
    exact hno ⟨i, j, x, hi, hj, hne⟩
  · rintro ⟨i, j, x, hi, hj, hne⟩ hc
    exact hne (hc i j x hi hj)

/-- DP-6: the empty cover glues uniquely (the empty function). -/
theorem empty_cover_glues (U : Empty → X → Prop)
    (s : (i : Empty) → {x // U i x} → B) :
    ∃ g, Restricts U s g ∧ ∀ g', Restricts U s g' → g' = g :=
  glue_exists_unique U s (fun i => nomatch i)

/-- A finite presheaf on the cover `{a}, {b}` of `{a,b}`: global sections,
the two local section sets, the overlap (`∅`) set, restrictions, and the two
composite laws (restricting a global section to `∅` through either side
agrees). -/
structure CoverPresheaf where
  G : Type
  LA : Type
  LB : Type
  L0 : Type
  resA : G → LA
  resB : G → LB
  ovA : LA → L0
  ovB : LB → L0
  glob0 : G → L0
  lawA : ∀ g, ovA (resA g) = glob0 g
  lawB : ∀ g, ovB (resB g) = glob0 g

/-- A matching family on the cover. -/
def CoverPresheaf.Matching (F : CoverPresheaf) (la : F.LA) (lb : F.LB) : Prop :=
  F.ovA la = F.ovB lb

/-- A global section extends the family `(la, lb)`. -/
def CoverPresheaf.Extends (F : CoverPresheaf) (la : F.LA) (lb : F.LB)
    (g : F.G) : Prop :=
  F.resA g = la ∧ F.resB g = lb

/-- DP-6: restrictions of a global section always form a matching family. -/
theorem CoverPresheaf.restriction_matches (F : CoverPresheaf) (g : F.G) :
    F.Matching (F.resA g) (F.resB g) := by
  unfold CoverPresheaf.Matching
  rw [F.lawA, F.lawB]

/-- Existence failure: `F(∅) = Unit`, every nonempty context `Bool`,
restrictions between nonempty contexts are identities. -/
def existenceFailure : CoverPresheaf where
  G := Bool
  LA := Bool
  LB := Bool
  L0 := Unit
  resA := id
  resB := id
  ovA := fun _ => ()
  ovB := fun _ => ()
  glob0 := fun _ => ()
  lawA := fun _ => rfl
  lawB := fun _ => rfl

/-- DP-6: the matching family `(false, true)` has no global extension. -/
theorem existence_failure_zero_extensions :
    existenceFailure.Matching (false : Bool) (true : Bool) ∧
      ∀ g, ¬ existenceFailure.Extends (false : Bool) (true : Bool) g := by
  refine ⟨rfl, ?_⟩
  intro g h
  have h1 : g = false := h.1
  have h2 : g = true := h.2
  rw [h1] at h2
  exact Bool.noConfusion h2

/-- Uniqueness failure: `F(X) = Bool`, every proper subset `Unit`. -/
def uniquenessFailure : CoverPresheaf where
  G := Bool
  LA := Unit
  LB := Unit
  L0 := Unit
  resA := fun _ => ()
  resB := fun _ => ()
  ovA := id
  ovB := id
  glob0 := fun _ => ()
  lawA := fun _ => rfl
  lawB := fun _ => rfl

/-- DP-6: the unique matching family has two distinct global extensions. -/
theorem uniqueness_failure_two_extensions :
    uniquenessFailure.Matching () () ∧
      uniquenessFailure.Extends () () (false : Bool) ∧
      uniquenessFailure.Extends () () (true : Bool) ∧ (false ≠ true) :=
  ⟨rfl, ⟨rfl, rfl⟩, ⟨rfl, rfl⟩, Bool.noConfusion⟩

/-- DP-6: existence for every matching family is surjectivity of the
restriction map onto matching families. -/
theorem CoverPresheaf.every_matching_extends_iff (F : CoverPresheaf) :
    (∀ la lb, F.Matching la lb → ∃ g, F.Extends la lb g) ↔
      ∀ m : {p : F.LA × F.LB // F.Matching p.1 p.2},
        ∃ g, (F.resA g, F.resB g) = m.1 := by
  constructor
  · rintro h ⟨⟨la, lb⟩, hm⟩
    obtain ⟨g, h1, h2⟩ := h la lb hm
    exact ⟨g, by rw [h1, h2]⟩
  · intro h la lb hm
    obtain ⟨g, hg⟩ := h ⟨(la, lb), hm⟩
    exact ⟨g, congrArg Prod.fst hg, congrArg Prod.snd hg⟩

end Gluing

/-! ## DP-2: zero-distance quotient and separation -/

section Separation

/-- A rational pseudometric on a carrier. -/
structure Pseudometric (S : Type u) where
  d : S → S → Rat
  nonneg : ∀ x y, 0 ≤ d x y
  self : ∀ x, d x x = 0
  symm : ∀ x y, d x y = d y x
  triangle : ∀ x y z, d x z ≤ d x y + d y z

variable {S : Type u}

/-- The zero-distance relation `Z`. -/
def Pseudometric.Zero (m : Pseudometric S) (x y : S) : Prop := m.d x y = 0

/-- DP-2: the zero-distance relation is an equivalence relation. -/
theorem Pseudometric.zero_equivalence (m : Pseudometric S) :
    Equivalence m.Zero := by
  constructor
  · exact m.self
  · intro x y h
    unfold Pseudometric.Zero at *
    rw [m.symm]; exact h
  · intro x y z hxy hyz
    unfold Pseudometric.Zero at *
    have ht := m.triangle x y z
    have hn := m.nonneg x z
    rw [hxy, hyz] at ht
    grind

/-- DP-2: the distance is constant on `Z`-classes. -/
theorem Pseudometric.descends_of_zero (m : Pseudometric S) {s s' t t' : S}
    (hs : m.Zero s s') (ht : m.Zero t t') : m.d s t = m.d s' t' := by
  unfold Pseudometric.Zero at hs ht
  have h1 := m.triangle s s' t
  have h2 := m.triangle s' t' t
  have h3 := m.triangle s' s t'
  have h4 := m.triangle s t t'
  have hs' : m.d s' s = 0 := by rw [m.symm]; exact hs
  have ht' : m.d t' t = 0 := by rw [m.symm]; exact ht
  grind

/-- DP-2: for an equivalence `E`, the inherited formula is well defined iff
`E ⊆ Z`. -/
theorem Pseudometric.well_defined_iff (m : Pseudometric S) (E : S → S → Prop)
    (hE : Equivalence E) :
    (∀ s s' t t', E s s' → E t t' → m.d s t = m.d s' t') ↔
      ∀ s t, E s t → m.Zero s t := by
  constructor
  · intro h s t hst
    have := h s t t t hst (hE.refl t)
    unfold Pseudometric.Zero
    rw [this, m.self]
  · intro h s s' t t' hs ht
    exact m.descends_of_zero (h _ _ hs) (h _ _ ht)

/-- The setoid generated by an equivalence. -/
def setoidOf (E : S → S → Prop) (hE : Equivalence E) : Setoid S := ⟨E, hE⟩

/-- The inherited distance on `S / E` when `E ⊆ Z`. -/
def Pseudometric.quotDist (m : Pseudometric S) (E : S → S → Prop)
    (hE : Equivalence E) (hsub : ∀ s t, E s t → m.Zero s t) :
    Quotient (setoidOf E hE) → Quotient (setoidOf E hE) → Rat :=
  @Quotient.lift₂ S S Rat (setoidOf E hE) (setoidOf E hE) m.d
    (fun _ _ _ _ hs ht => m.descends_of_zero (hsub _ _ hs) (hsub _ _ ht))

/-- The inherited distance computes on representatives. -/
theorem Pseudometric.quotDist_mk (m : Pseudometric S) (E : S → S → Prop)
    (hE : Equivalence E) (hsub : ∀ s t, E s t → m.Zero s t) (s t : S) :
    m.quotDist E hE hsub (Quotient.mk (setoidOf E hE) s)
      (Quotient.mk (setoidOf E hE) t) = m.d s t := rfl

/-- DP-2: the inherited distance is separated iff `Z ⊆ E` (with `E ⊆ Z`,
iff `E = Z`). -/
theorem Pseudometric.separated_iff (m : Pseudometric S) (E : S → S → Prop)
    (hE : Equivalence E) (hsub : ∀ s t, E s t → m.Zero s t) :
    (∀ a b, m.quotDist E hE hsub a b = 0 → a = b) ↔
      ∀ s t, m.Zero s t → E s t := by
  constructor
  · intro h s t hz
    have := h (Quotient.mk (setoidOf E hE) s) (Quotient.mk (setoidOf E hE) t)
      (by rw [m.quotDist_mk]; exact hz)
    exact Quotient.exact this
  · intro h a b
    induction a using Quotient.inductionOn
    induction b using Quotient.inductionOn
    intro hz
    rw [m.quotDist_mk] at hz
    exact Quotient.sound (h _ _ hz)

/-- The indiscrete pseudometric. -/
def indiscrete (S : Type u) : Pseudometric S where
  d := fun _ _ => 0
  nonneg := fun _ _ => Rat.le_refl
  self := fun _ => rfl
  symm := fun _ _ => rfl
  triangle := fun _ _ _ => by grind

/-- DP-2: the quotient by the zero relation of the indiscrete pseudometric is
a subsingleton (it can be empty when S is empty). -/
theorem indiscrete_quotient_singleton :
    ∀ a b : Quotient (setoidOf (indiscrete S).Zero
      (indiscrete S).zero_equivalence), a = b := by
  intro a b
  induction a using Quotient.inductionOn
  induction b using Quotient.inductionOn
  exact Quotient.sound rfl

/-- DP-2: a decoder value within `ε` of two outputs bounds their distance by
`2ε`. -/
theorem fiber_diameter_le (m : Pseudometric S) (u v c : S) (ε : Rat)
    (hu : m.d u c ≤ ε) (hv : m.d v c ≤ ε) : m.d u v ≤ 2 * ε := by
  have ht := m.triangle u c v
  have hs : m.d c v = m.d v c := m.symm c v
  grind

/-- DP-2: with gap `Δ` between inequivalent outputs and `2ε < Δ`, a common
decoder value forces equivalence. -/
theorem strict_gap_forces_equivalence (m : Pseudometric S) (E : S → S → Prop)
    (Δ ε : Rat) (hgap : ∀ s t, ¬ E s t → Δ ≤ m.d s t) (hstrict : 2 * ε < Δ)
    (u v c : S) (hu : m.d u c ≤ ε) (hv : m.d v c ≤ ε) : E u v := by
  apply Classical.byContradiction
  intro hne
  have h1 := hgap u v hne
  have h2 := fiber_diameter_le m u v c ε hu hv
  grind

/-- Absolute value on `Rat` (Lean core has none). -/
def qabs (x : Rat) : Rat := if x < 0 then -x else x

/-- The ambient distance `|x - y|` on `Rat`. -/
def absMetric : Pseudometric Rat where
  d := fun x y => qabs (x - y)
  nonneg := fun x y => by unfold qabs; split <;> grind
  self := fun x => by unfold qabs; grind
  symm := fun x y => by unfold qabs; split <;> split <;> grind
  triangle := fun x y z => by
    unfold qabs; split <;> split <;> split <;> grind

/-- DP-2: the strict threshold is needed. Outputs `0, 1` (gap `1`), decoder
`1/2`, error `1/2`: `2ε = Δ`, both errors within `ε`, outputs unequal. -/
theorem equality_threshold_countermodel :
    absMetric.d 0 (1 / 2) ≤ 1 / 2 ∧ absMetric.d 1 (1 / 2) ≤ 1 / 2 ∧
      2 * (1 / 2 : Rat) = absMetric.d 0 1 ∧ (0 : Rat) ≠ 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · show qabs (0 - 1 / 2) ≤ 1 / 2
    unfold qabs; grind
  · show qabs (1 - 1 / 2) ≤ 1 / 2
    unfold qabs; grind
  · show 2 * (1 / 2 : Rat) = qabs (0 - 1)
    unfold qabs; grind
  · grind

/-- DP-2 worked example, weights `(1,2)`: `d(a,b) = 4/3`, `d(a,c) = 1`,
`d(b,c) = 5/3`, for `a = (0,0)`, `b = (1/3,1/2)`, `c = (1,0)`. -/
def weightedDist (x y : Rat × Rat) : Rat := qabs (x.1 - y.1) + 2 * qabs (x.2 - y.2)

theorem worked_example_distances :
    weightedDist (0, 0) (1 / 3, 1 / 2) = 4 / 3 ∧
      weightedDist (0, 0) (1, 0) = 1 ∧
      weightedDist (1 / 3, 1 / 2) (1, 0) = 5 / 3 := by
  unfold weightedDist qabs
  refine ⟨?_, ?_, ?_⟩ <;> grind

end Separation

end WitnessedDifference.ComponentReports
