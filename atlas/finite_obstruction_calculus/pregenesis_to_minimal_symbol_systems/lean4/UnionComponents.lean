import GraphExtensions

/-! A terminating component-label algorithm and its carrier-general correctness
proof. Edges are processed by merging two label fibers. Duplicate edges and loops
are retained in the graph. Labels are representatives, with no ordering assumed. -/
namespace PreMssn.UnionComponents
open GraphHomology GraphExtensions
universe u

def EdgeCarrier {A : Type u} : List (A × A) → Type u
  | [] => {_a : A // False}
  | _::es => Sum (EdgeCarrier es) PUnit

def source {A : Type u} : (es : List (A × A)) → EdgeCarrier es → A
  | [], e => False.elim e.property
  | (a,_)::_, .inr _ => a
  | _::es, .inl e => source es e

def target {A : Type u} : (es : List (A × A)) → EdgeCarrier es → A
  | [], e => False.elim e.property
  | (_,b)::_, .inr _ => b
  | _::es, .inl e => target es e

abbrev graph {A : Type u} (es : List (A × A)) : Graph where
  Vertex := A
  Edge := EdgeCarrier es
  source := source es
  target := target es

def merge {A : Type u} [DecidableEq A] (a b x : A) : A :=
  if x=a ∨ x=b then a else x

theorem merge_a {A : Type u} [DecidableEq A] (a b : A) : merge a b a=a := by simp [merge]
theorem merge_b {A : Type u} [DecidableEq A] (a b : A) : merge a b b=a := by simp [merge]

theorem merge_eq_iff {A : Type u} [DecidableEq A] (a b x y : A) :
    merge a b x = merge a b y ↔ x=y ∨ ((x=a ∨ x=b) ∧ (y=a ∨ y=b)) := by
  by_cases hx : x=a ∨ x=b <;> by_cases hy : y=a ∨ y=b
  · simp [merge, hx, hy]
  · simp only [merge, if_pos hx, if_neg hy]
    constructor
    · intro h; exact False.elim (hy (Or.inl h.symm))
    · intro h
      rcases h with h | h
      · exact False.elim (hy (h ▸ hx))
      · exact False.elim (hy h.2)
  · simp only [merge, if_neg hx, if_pos hy]
    constructor
    · intro h; exact False.elim (hx (Or.inl h))
    · intro h
      rcases h with h | h
      · exact False.elim (hx (h ▸ hy))
      · exact False.elim (hx h.1)
  · simp [merge, hx, hy]

def labels {A : Type u} [DecidableEq A] : List (A × A) → A → A
  | [] => fun x => x
  | (a,b)::es => fun x => merge (labels es a) (labels es b) (labels es x)

theorem connected_nil_iff {A : Type u} (x y : A) : Connected (graph []) x y ↔ x=y := by
  constructor
  · intro h
    induction h using Connected.rec (G := graph ([] : List (A × A))) with
    | refl => rfl
    | edge e => exact False.elim e.property
    | symm _ ih => exact ih.symm
    | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  · intro h; cases h; exact Connected.refl (G := graph []) x

theorem old_connected {A : Type u} (es : List (A × A)) (a b : A) {x y : A}
    (h : Connected (graph es) x y) : Connected (graph ((a,b)::es)) x y := by
  induction h using Connected.rec (G := graph es) with
  | refl v => exact Connected.refl (G := graph ((a,b)::es)) v
  | edge e => exact Connected.edge (G := graph ((a,b)::es)) (.inl e)
  | symm _ ih => exact .symm ih
  | trans _ _ ih hj => exact .trans ih hj

/-- Two vertices receive the same computed label exactly when an undirected
path connects them in the graph containing the supplied edge occurrences. -/
theorem labels_eq_iff_connected {A : Type u} [DecidableEq A]
    (es : List (A × A)) (x y : A) : labels es x = labels es y ↔ Connected (graph es) x y := by
  induction es generalizing x y with
  | nil => exact (connected_nil_iff x y).symm
  | cons e es ih =>
    rcases e with ⟨a,b⟩
    constructor
    · intro h
      rcases (merge_eq_iff _ _ _ _).mp h with same | both
      · exact old_connected es a b ((ih x y).mp same)
      · have hx : Connected (graph ((a,b)::es)) x a := by
          rcases both.1 with hxa | hxb
          · exact old_connected es a b ((ih x a).mp hxa)
          · exact .trans (old_connected es a b ((ih x b).mp hxb))
              (.symm (Connected.edge (G := graph ((a,b)::es)) (.inr PUnit.unit)))
        have hy : Connected (graph ((a,b)::es)) y a := by
          rcases both.2 with hya | hyb
          · exact old_connected es a b ((ih y a).mp hya)
          · exact .trans (old_connected es a b ((ih y b).mp hyb))
              (.symm (Connected.edge (G := graph ((a,b)::es)) (.inr PUnit.unit)))
        exact .trans hx (.symm hy)
    · intro h
      induction h using Connected.rec (G := graph ((a,b)::es)) with
      | refl => rfl
      | edge e =>
        cases e with
        | inr _ => exact (merge_a _ _).trans (merge_b _ _).symm
        | inl e =>
          have old := (ih ((graph es).source e) ((graph es).target e)).mpr
            (Connected.edge (G := graph es) e)
          exact congrArg (merge (labels es a) (labels es b)) old
      | symm _ hi => exact hi.symm
      | trans _ _ hi hj => exact hi.trans hj

theorem labels_eq_iff_h0 {A : Type u} [DecidableEq A]
    (es : List (A × A)) (x y : A) :
    labels es x = labels es y ↔ vertexClass (graph es) x = vertexClass (graph es) y := by
  rw [labels_eq_iff_connected, vertex_class_eq_iff_connected]

/-- Every computed label names its own component; no fictitious label is added. -/
theorem label_idempotent {A : Type u} [DecidableEq A] (es : List (A × A)) (x : A) :
    labels es (labels es x) = labels es x := by
  induction es generalizing x with
  | nil => rfl
  | cons e es ih =>
    rcases e with ⟨a,b⟩
    simp only [labels]
    by_cases h : labels es x = labels es a ∨ labels es x = labels es b
    · have hm : merge (labels es a) (labels es b) (labels es x) = labels es a := if_pos h
      rw [hm, ih, merge_a]
    · have hm : merge (labels es a) (labels es b) (labels es x) = labels es x := if_neg h
      rw [hm, ih, hm]

theorem vertex_connected_to_label {A : Type u} [DecidableEq A]
    (es : List (A × A)) (x : A) : Connected (graph es) x (labels es x) :=
  (labels_eq_iff_connected es x (labels es x)).mp (label_idempotent es x).symm

/-- Choose the first vertex in a declared enumeration with the same label.
The fallback makes this total even if the enumeration omits the queried vertex. -/
def canonical {A : Type u} [DecidableEq A] (es : List (A × A)) (vertices : List A) (x : A) : A :=
  (vertices.find? (fun v => decide (labels es v = labels es x))).getD x

theorem canonical_label {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (x : A) :
    labels es (canonical es vertices x) = labels es x := by
  unfold canonical
  cases h : vertices.find? (fun v => decide (labels es v = labels es x)) with
  | none => rfl
  | some v =>
    change labels es v = labels es x
    exact of_decide_eq_true (List.find?_some (p := fun v => decide (labels es v = labels es x)) h)

theorem canonical_mem {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (x : A) (hx : x ∈ vertices) :
    canonical es vertices x ∈ vertices := by
  unfold canonical
  cases h : vertices.find? (fun v => decide (labels es v = labels es x)) with
  | none => exact hx
  | some v => exact List.mem_of_find?_eq_some h

theorem canonical_eq_iff {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (x y : A) (hx : x ∈ vertices) :
    canonical es vertices x = canonical es vertices y ↔ labels es x = labels es y := by
  constructor
  · intro h
    exact (canonical_label es vertices x).symm.trans
      ((congrArg (labels es) h).trans (canonical_label es vertices y))
  · intro same
    have hf : (fun v => decide (labels es v = labels es x)) =
        (fun v => decide (labels es v = labels es y)) := by rw [same]
    unfold canonical
    rw [hf]
    cases h : vertices.find? (fun v => decide (labels es v = labels es y)) with
    | some v => rfl
    | none =>
      have hn := (List.find?_eq_none.mp h) x hx
      simp [same] at hn

theorem canonical_eq_iff_h0 {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (x y : A) (hx : x ∈ vertices) :
    canonical es vertices x = canonical es vertices y ↔
      vertexClass (graph es) x = vertexClass (graph es) y := by
  rw [canonical_eq_iff es vertices x y hx, labels_eq_iff_h0]

def naturalRoot (n : Nat) (es : List (Nat × Nat)) (x : Nat) : Nat :=
  canonical es (List.range n) x

theorem find_minimum (vertices : List Nat) (p : Nat → Bool)
    (ordered : vertices.Pairwise (· ≤ ·)) {a b : Nat}
    (ha : vertices.find? p = some a) (hb : b ∈ vertices) (pb : p b = true) : a ≤ b := by
  induction vertices with
  | nil => contradiction
  | cons v vs ih =>
    have hs := List.pairwise_cons.mp ordered
    by_cases hv : p v = true
    · have he : v=a := by simpa [List.find?_cons, hv] using ha
      subst a
      rcases List.mem_cons.mp hb with h | h
      · exact Nat.le_of_eq h.symm
      · exact hs.1 b h
    · have htail : vs.find? p = some a := by simpa [List.find?_cons, hv] using ha
      have hb' : b ∈ vs := by
        rcases List.mem_cons.mp hb with h | h
        · subst b; exact False.elim (hv pb)
        · exact h
      exact ih hs.2 htail hb'

theorem range_ordered (n : Nat) : (List.range n).Pairwise (· ≤ ·) := by
  induction n with
  | zero => exact .nil
  | succ n ih =>
    rw [List.range_succ, List.pairwise_append]
    refine ⟨ih, by simp, ?_⟩
    intro a ha b hb
    have he : b=n := by simpa using hb
    subst b
    exact Nat.le_of_lt (List.mem_range.mp ha)

theorem natural_root_minimum (n : Nat) (es : List (Nat × Nat))
    (x y : Nat) (hx : x<n) (hy : y<n) (hxy : Connected (graph es) x y) :
    naturalRoot n es x ≤ y := by
  have same := (labels_eq_iff_connected es x y).mpr hxy
  unfold naturalRoot canonical
  cases h : (List.range n).find? (fun v => decide (labels es v = labels es x)) with
  | none =>
    have hn := (List.find?_eq_none.mp h) x (List.mem_range.mpr hx)
    simp at hn
  | some r =>
    exact find_minimum _ _ (range_ordered n) h (List.mem_range.mpr hy)
      (decide_eq_true same.symm)

theorem canonical_idempotent {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (x : A) (hx : x ∈ vertices) :
    canonical es vertices (canonical es vertices x) = canonical es vertices x :=
  (canonical_eq_iff es vertices (canonical es vertices x) x
    (canonical_mem es vertices x hx)).mpr (canonical_label es vertices x)

abbrev Representative {A : Type u} [DecidableEq A] (es : List (A × A)) (vertices : List A) :=
  {x : A // canonical es vertices x = x}

def componentRepresentative {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (complete : ∀ x, x ∈ vertices) :
    Component (graph es) → Representative es vertices := fun q =>
  Quotient.liftOn q
    (fun x => ⟨canonical es vertices x, canonical_idempotent es vertices x (complete x)⟩)
    (fun x y h => Subtype.ext ((canonical_eq_iff es vertices x y (complete x)).mpr
      ((labels_eq_iff_connected es x y).mpr h)))

theorem representative_component_inverse {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (complete : ∀ x, x ∈ vertices)
    (q : Component (graph es)) :
    component (graph es) (componentRepresentative es vertices complete q).val = q := by
  induction q using Quotient.inductionOn with
  | _ x =>
    apply Quotient.sound
    exact (labels_eq_iff_connected es (canonical es vertices x) x).mp
      (canonical_label es vertices x)

theorem component_representative_inverse {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (complete : ∀ x, x ∈ vertices)
    (r : Representative es vertices) :
    componentRepresentative es vertices complete (component (graph es) r.val) = r :=
  Subtype.ext r.property

/-- The computed representatives form an actual basis for integral H0 when the
supplied finite enumeration covers the vertex carrier. -/
def computedH0Iso {A : Type u} [DecidableEq A]
    (es : List (A × A)) (vertices : List A) (complete : ∀ x, x ∈ vertices) :
    Homology.AddIso (H0 (graph es)) (FreeAbelian.Free (Representative es vertices)) :=
  Homology.AddIso.comp
    (h0ComponentIso (graph es))
    (FiniteCoordinates.carrierIso (componentRepresentative es vertices complete)
      (fun r => component (graph es) r.val)
      (representative_component_inverse es vertices complete)
      (component_representative_inverse es vertices complete))

theorem natural_root_eq_iff_connected (n : Nat) (es : List (Nat × Nat))
    (x y : Nat) (hx : x < n) :
    naturalRoot n es x = naturalRoot n es y ↔ Connected (graph es) x y := by
  rw [naturalRoot, naturalRoot, canonical_eq_iff es (List.range n) x y
    (List.mem_range.mpr hx), labels_eq_iff_connected]

def componentTotals (n : Nat) (es : List (Nat × Nat)) (coefficients : List Int) : List Int :=
  ((List.range n).filter (fun v => naturalRoot n es v == v)).flatMap fun (v : Nat) =>
    [(v : Int), ((List.range n).map fun w =>
      if naturalRoot n es w == v then coefficients.getD w 0 else 0).sum]

end PreMssn.UnionComponents
