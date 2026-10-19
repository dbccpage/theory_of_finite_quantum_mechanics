import Std

/-!
SwitchingNormalForm.lean

AuthorityEffect: None. Proposal only.

General F2 spanning-forest switching normal form (ledger row NF-002 of
`F004_papers/008_fsp`, definitions from `docs/normal_form_audit.md` §4).
Core Lean 4 only: no Mathlib, no `sorry`, no `axiom`, no `partial`,
no `native_decide`, no `Classical.choice`.

A graph is `Fin n` vertices with `m` ordered labelled edges given as a
function `Fin m → Fin n × Fin n`; loops, parallel edges, several components
and isolated vertices are all allowed. A spanning forest is a given witness
(`Forest`), not the output of a search: each non-root vertex names its parent
edge, a depth function strictly decreases along parent edges, and a component
labelling ties the forest to the graph (every edge joins vertices of one
label; every label has exactly one root). The forest potential is the parity
of the forest path to the root, computed by fuel recursion on the depth.
-/

namespace SwitchingNormalForm

/-! ## Graphs, cochains, switching -/

structure Graph where
  n : Nat
  m : Nat
  edge : Fin m → Fin n × Fin n

abbrev Cochain (G : Graph) := Fin G.m → Bool
abbrev Potential (G : Graph) := Fin G.n → Bool

/-- The coboundary `(δa)(uv) = a u xor a v`. -/
def delta (G : Graph) (a : Potential G) (e : Fin G.m) : Bool :=
  a (G.edge e).1 ^^ a (G.edge e).2

/-- Vertex switching of a cochain by a potential. -/
def switch (G : Graph) (s : Cochain G) (a : Potential G) : Cochain G :=
  fun e => s e ^^ delta G a e

/-- `s ~ t` iff `t = s xor δa` for some vertex potential `a`. -/
def SameClass (G : Graph) (s t : Cochain G) : Prop :=
  ∃ a : Potential G, t = switch G s a

def zero (G : Graph) : Cochain G := fun _ => false

theorem switch_switch (G : Graph) (s : Cochain G) (a : Potential G) :
    switch G (switch G s a) a = s := by
  funext e
  simp only [switch]
  rw [Bool.xor_assoc, Bool.xor_self, Bool.xor_false]

theorem switch_zero_potential (G : Graph) (s : Cochain G) :
    switch G s (fun _ => false) = s := by
  funext e
  simp only [switch, delta, Bool.xor_self, Bool.xor_false]

/-- The endpoint of `e` other than `v` (for a loop at `v`, `v` itself). -/
def Graph.other (G : Graph) (v : Fin G.n) (e : Fin G.m) : Fin G.n :=
  if (G.edge e).1 = v then (G.edge e).2 else (G.edge e).1

def Graph.Incident (G : Graph) (v : Fin G.n) (e : Fin G.m) : Prop :=
  (G.edge e).1 = v ∨ (G.edge e).2 = v

instance (G : Graph) (v : Fin G.n) (e : Fin G.m) : Decidable (G.Incident v e) :=
  inferInstanceAs (Decidable ((G.edge e).1 = v ∨ (G.edge e).2 = v))

theorem delta_other (G : Graph) (b : Potential G) {v : Fin G.n} {e : Fin G.m}
    (h : G.Incident v e) : delta G b e = (b v ^^ b (G.other v e)) := by
  unfold delta Graph.other
  rcases h with h | h
  · rw [ite_eq_left_of_eq_true _ _ (eq_true h), h]
  · by_cases h1 : (G.edge e).1 = v
    · rw [ite_eq_left_of_eq_true _ _ (eq_true h1), h1, h]
    · rw [ite_eq_right_of_eq_false _ _ (eq_false h1), h, Bool.xor_comm]

/-! ## Spanning forests as witnesses -/

structure Forest (G : Graph) where
  parent : Fin G.n → Option (Fin G.m)
  depth : Fin G.n → Nat
  comp : Fin G.n → Nat
  incident : ∀ v e, parent v = some e → G.Incident v e
  descends : ∀ v e, parent v = some e → depth (G.other v e) < depth v
  edgeComp : ∀ e, comp (G.edge e).1 = comp (G.edge e).2
  rootUnique : ∀ u v, parent u = none → parent v = none → comp u = comp v → u = v

variable {G : Graph}

/-- Induction along parent edges, by strong induction on the depth. -/
theorem Forest.induction (T : Forest G) (P : Fin G.n → Prop)
    (hroot : ∀ v, T.parent v = none → P v)
    (hstep : ∀ v e, T.parent v = some e → P (G.other v e) → P v) :
    ∀ v, P v := by
  have key : ∀ k v, T.depth v ≤ k → P v := by
    intro k
    induction k with
    | zero =>
      intro v hv
      cases h : T.parent v with
      | none => exact hroot v h
      | some e =>
        have := T.descends v e h
        exact absurd (Nat.lt_of_lt_of_le this hv) (Nat.not_lt_zero _)
    | succ k ih =>
      intro v hv
      cases h : T.parent v with
      | none => exact hroot v h
      | some e =>
        have hd := T.descends v e h
        exact hstep v e h (ih _ (by omega))
  intro v
  exact key (T.depth v) v (Nat.le_refl _)

theorem Forest.comp_other (T : Forest G) {v : Fin G.n} {e : Fin G.m}
    (h : T.parent v = some e) : T.comp (G.other v e) = T.comp v := by
  have hi := T.incident v e h
  have hc := T.edgeComp e
  unfold Graph.other
  rcases hi with hi | hi
  · rw [ite_eq_left_of_eq_true _ _ (eq_true hi), ← hc, hi]
  · by_cases h1 : (G.edge e).1 = v
    · rw [ite_eq_left_of_eq_true _ _ (eq_true h1), hi]
    · rw [ite_eq_right_of_eq_false _ _ (eq_false h1), hc, hi]

/-! ### Fuel recursion on the depth -/

def potAux (T : Forest G) (s : Cochain G) : Nat → Fin G.n → Bool
  | 0, _ => false
  | k + 1, v =>
    match T.parent v with
    | none => false
    | some e => s e ^^ potAux T s k (G.other v e)

/-- The forest potential: parity of the forest path from the root to `v`. -/
def potential (T : Forest G) (s : Cochain G) (v : Fin G.n) : Bool :=
  potAux T s (T.depth v) v

theorem potAux_fuel (T : Forest G) (s : Cochain G) :
    ∀ k₁ k₂ v, T.depth v ≤ k₁ → T.depth v ≤ k₂ → potAux T s k₁ v = potAux T s k₂ v := by
  intro k₁
  induction k₁ with
  | zero =>
    intro k₂ v h1 h2
    cases k₂ with
    | zero => rfl
    | succ k₂ =>
      simp only [potAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have := T.descends v e h
        omega
  | succ k₁ ih =>
    intro k₂ v h1 h2
    cases k₂ with
    | zero =>
      simp only [potAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have := T.descends v e h
        omega
    | succ k₂ =>
      simp only [potAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have hd := T.descends v e h
        dsimp only
        rw [ih k₂ (G.other v e) (by omega) (by omega)]

theorem potential_root (T : Forest G) (s : Cochain G) {v : Fin G.n}
    (h : T.parent v = none) : potential T s v = false := by
  unfold potential
  rw [potAux_fuel T s (T.depth v) (T.depth v + 1) v (Nat.le_refl _) (Nat.le_succ _)]
  simp only [potAux, h]

theorem potential_step (T : Forest G) (s : Cochain G) {v : Fin G.n} {e : Fin G.m}
    (h : T.parent v = some e) :
    potential T s v = (s e ^^ potential T s (G.other v e)) := by
  unfold potential
  rw [potAux_fuel T s (T.depth v) (T.depth v + 1) v (Nat.le_refl _) (Nat.le_succ _)]
  simp only [potAux, h]
  have hd := T.descends v e h
  rw [potAux_fuel T s (T.depth v) (T.depth (G.other v e)) (G.other v e) (by omega) (Nat.le_refl _)]

/-! ### Roots -/

def rootAux (T : Forest G) : Nat → Fin G.n → Fin G.n
  | 0, v => v
  | k + 1, v =>
    match T.parent v with
    | none => v
    | some e => rootAux T k (G.other v e)

def root (T : Forest G) (v : Fin G.n) : Fin G.n :=
  rootAux T (T.depth v) v

theorem rootAux_fuel (T : Forest G) :
    ∀ k₁ k₂ v, T.depth v ≤ k₁ → T.depth v ≤ k₂ → rootAux T k₁ v = rootAux T k₂ v := by
  intro k₁
  induction k₁ with
  | zero =>
    intro k₂ v h1 h2
    cases k₂ with
    | zero => rfl
    | succ k₂ =>
      simp only [rootAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have := T.descends v e h
        omega
  | succ k₁ ih =>
    intro k₂ v h1 h2
    cases k₂ with
    | zero =>
      simp only [rootAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have := T.descends v e h
        omega
    | succ k₂ =>
      simp only [rootAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have hd := T.descends v e h
        dsimp only
        rw [ih k₂ (G.other v e) (by omega) (by omega)]

theorem root_of_none (T : Forest G) {v : Fin G.n} (h : T.parent v = none) :
    root T v = v := by
  unfold root
  rw [rootAux_fuel T (T.depth v) (T.depth v + 1) v (Nat.le_refl _) (Nat.le_succ _)]
  simp only [rootAux, h]

theorem root_step (T : Forest G) {v : Fin G.n} {e : Fin G.m} (h : T.parent v = some e) :
    root T v = root T (G.other v e) := by
  unfold root
  rw [rootAux_fuel T (T.depth v) (T.depth v + 1) v (Nat.le_refl _) (Nat.le_succ _)]
  simp only [rootAux, h]
  have hd := T.descends v e h
  rw [rootAux_fuel T (T.depth v) (T.depth (G.other v e)) (G.other v e) (by omega) (Nat.le_refl _)]

theorem root_isRoot (T : Forest G) (v : Fin G.n) : T.parent (root T v) = none := by
  refine T.induction (fun v => T.parent (root T v) = none) ?_ ?_ v
  · intro v h
    rw [root_of_none T h]
    exact h
  · intro v e h ih
    rw [root_step T h]
    exact ih

theorem comp_root (T : Forest G) (v : Fin G.n) : T.comp (root T v) = T.comp v := by
  refine T.induction (fun v => T.comp (root T v) = T.comp v) ?_ ?_ v
  · intro v h
    rw [root_of_none T h]
  · intro v e h ih
    rw [root_step T h, ih, T.comp_other h]

theorem root_eq_of_comp (T : Forest G) {u v : Fin G.n} (h : T.comp u = T.comp v) :
    root T u = root T v := by
  apply T.rootUnique _ _ (root_isRoot T u) (root_isRoot T v)
  rw [comp_root, comp_root, h]

theorem root_edge (T : Forest G) (e : Fin G.m) :
    root T (G.edge e).1 = root T (G.edge e).2 :=
  root_eq_of_comp T (T.edgeComp e)

/-! ## The normal form -/

/-- `N_T(s)(uv) = s(uv) xor a(u) xor a(v)` with `a` the forest potential. -/
def normal (T : Forest G) (s : Cochain G) : Cochain G :=
  switch G s (potential T s)

/-! ### Boolean telescoping identities (closed by case analysis) -/

theorem xor_tele (p q x y z : Bool) :
    ((p ^^ (x ^^ y)) ^^ ((q ^^ y) ^^ z)) = (((p ^^ q) ^^ x) ^^ z) := by
  cases p <;> cases q <;> cases x <;> cases y <;> cases z <;> rfl

theorem xor_forest (p y : Bool) : (p ^^ ((p ^^ y) ^^ y)) = false := by
  cases p <;> cases y <;> rfl

theorem xor_gauge (p q r x y z : Bool) :
    ((p ^^ (x ^^ y)) ^^ (((q ^^ x) ^^ z) ^^ ((r ^^ y) ^^ z))) = (p ^^ (q ^^ r)) := by
  cases p <;> cases q <;> cases r <;> cases x <;> cases y <;> cases z <;> rfl

/-- Telescoping: switching by `b` shifts the potential by `b v xor b (root v)`. -/
theorem potential_switch (T : Forest G) (s : Cochain G) (b : Potential G) (v : Fin G.n) :
    potential T (switch G s b) v = ((potential T s v ^^ b v) ^^ b (root T v)) := by
  refine T.induction
    (fun v => potential T (switch G s b) v = ((potential T s v ^^ b v) ^^ b (root T v))) ?_ ?_ v
  · intro v h
    rw [potential_root T _ h, potential_root T _ h, root_of_none T h, Bool.false_xor, Bool.xor_self]
  · intro v e h ih
    rw [potential_step T _ h, potential_step T _ h, ih, root_step T h]
    simp only [switch]
    rw [delta_other G b (T.incident v e h)]
    exact xor_tele _ _ _ _ _

/-! ## T1: soundness -/

theorem normal_sound (T : Forest G) (s : Cochain G) : SameClass G s (normal T s) :=
  ⟨potential T s, rfl⟩

theorem switch_normal (T : Forest G) (s : Cochain G) :
    switch G (normal T s) (potential T s) = s :=
  switch_switch G s (potential T s)

theorem normal_forest_zero (T : Forest G) (s : Cochain G) {v : Fin G.n} {e : Fin G.m}
    (h : T.parent v = some e) : normal T s e = false := by
  simp only [normal, switch]
  rw [delta_other G _ (T.incident v e h), potential_step T s h]
  exact xor_forest _ _

/-! ## Gauge invariance and T2: idempotence -/

theorem normal_switch (T : Forest G) (s : Cochain G) (b : Potential G) :
    normal T (switch G s b) = normal T s := by
  funext e
  simp only [normal, switch, delta]
  rw [potential_switch, potential_switch, root_edge T e]
  exact xor_gauge _ _ _ _ _ _

theorem normal_idem (T : Forest G) (s : Cochain G) :
    normal T (normal T s) = normal T s := by
  have hz : potential T (normal T s) = fun _ => false := by
    funext v
    unfold normal
    rw [potential_switch, Bool.xor_self, Bool.false_xor]
    exact potential_root T s (root_isRoot T v)
  show switch G (normal T s) (potential T (normal T s)) = normal T s
  rw [hz, switch_zero_potential]

/-! ## T3: completeness -/

theorem same_class_iff (T : Forest G) (s t : Cochain G) :
    SameClass G s t ↔ normal T s = normal T t := by
  constructor
  · rintro ⟨b, rfl⟩
    exact (normal_switch T s b).symm
  · intro h
    refine ⟨fun v => potential T s v ^^ potential T t v, ?_⟩
    funext e
    have he := congrFun h e
    simp only [normal, switch, delta] at he ⊢
    revert he
    generalize s e = p
    generalize t e = q
    generalize potential T s (G.edge e).1 = a1
    generalize potential T s (G.edge e).2 = a2
    generalize potential T t (G.edge e).1 = b1
    generalize potential T t (G.edge e).2 = b2
    cases p <;> cases q <;> cases a1 <;> cases a2 <;> cases b1 <;> cases b2 <;> decide

theorem same_class_refl (G : Graph) (s : Cochain G) : SameClass G s s :=
  ⟨fun _ => false, (switch_zero_potential G s).symm⟩

theorem same_class_symm (T : Forest G) {s t : Cochain G} (h : SameClass G s t) :
    SameClass G t s :=
  (same_class_iff T t s).2 ((same_class_iff T s t).1 h).symm

theorem same_class_trans (T : Forest G) {s t u : Cochain G}
    (h1 : SameClass G s t) (h2 : SameClass G t u) : SameClass G s u :=
  (same_class_iff T s u).2 (((same_class_iff T s t).1 h1).trans ((same_class_iff T t u).1 h2))

/-! ## T5 (gauge form): the obstruction criterion -/

theorem normal_zero (T : Forest G) : normal T (zero G) = zero G := by
  have hz : potential T (zero G) = fun _ => false := by
    funext v
    refine T.induction (fun v => potential T (zero G) v = false) ?_ ?_ v
    · intro v h
      exact potential_root T _ h
    · intro v e h ih
      rw [potential_step T _ h, ih]
      rfl
  show switch G (zero G) (potential T (zero G)) = zero G
  rw [hz, switch_zero_potential]

theorem normal_eq_zero_iff (T : Forest G) (s : Cochain G) :
    normal T s = zero G ↔ ∃ a : Potential G, switch G s a = zero G := by
  constructor
  · intro h
    exact ⟨potential T s, h⟩
  · rintro ⟨a, h⟩
    have hs : s = switch G (zero G) a := by
      rw [← h, switch_switch]
    rw [hs, normal_switch, normal_zero]

/-! ## T5 (cycle form): closed edge walks and fundamental cycles -/

/-- `e` has endpoints `u` and `w` (in either orientation). -/
def Graph.Ends (G : Graph) (e : Fin G.m) (u w : Fin G.n) : Prop :=
  G.edge e = (u, w) ∨ G.edge e = (w, u)

theorem Graph.Ends.symm {e : Fin G.m} {u w : Fin G.n} (h : G.Ends e u w) : G.Ends e w u :=
  Or.symm h

theorem ends_other {v : Fin G.n} {e : Fin G.m} (h : G.Incident v e) :
    G.Ends e v (G.other v e) := by
  unfold Graph.Ends Graph.other
  rcases h with h | h
  · left
    rw [ite_eq_left_of_eq_true _ _ (eq_true h), ← h]
  · by_cases h1 : (G.edge e).1 = v
    · left
      rw [ite_eq_left_of_eq_true _ _ (eq_true h1), ← h1]
    · right
      rw [ite_eq_right_of_eq_false _ _ (eq_false h1), ← h]

/-- An edge walk from `u` to `v` along the listed edges. -/
inductive Walk (G : Graph) : Fin G.n → Fin G.n → List (Fin G.m) → Prop
  | nil (v : Fin G.n) : Walk G v v []
  | cons {u w v : Fin G.n} {e : Fin G.m} {es : List (Fin G.m)} :
      G.Ends e u w → Walk G w v es → Walk G u v (e :: es)

/-- Sign parity of a cochain along a list of edges. -/
def parity (s : Cochain G) : List (Fin G.m) → Bool
  | [] => false
  | e :: es => s e ^^ parity s es

theorem delta_ends (b : Potential G) {e : Fin G.m} {u w : Fin G.n} (h : G.Ends e u w) :
    delta G b e = (b u ^^ b w) := by
  unfold delta
  rcases h with h | h
  · rw [h]
  · rw [h]
    exact Bool.xor_comm _ _

theorem parity_switch (s : Cochain G) (b : Potential G) {u v : Fin G.n}
    {es : List (Fin G.m)} (w : Walk G u v es) :
    parity (switch G s b) es = ((parity s es ^^ b u) ^^ b v) := by
  induction w with
  | nil v =>
    simp only [parity]
    rw [Bool.false_xor, Bool.xor_self]
  | cons he _ ih =>
    simp only [parity, switch]
    rw [ih, delta_ends b he]
    exact xor_tele _ _ _ _ _

theorem closed_walk_invariant (s : Cochain G) (b : Potential G) {u : Fin G.n}
    {es : List (Fin G.m)} (w : Walk G u u es) :
    parity (switch G s b) es = parity s es := by
  rw [parity_switch s b w, Bool.xor_assoc, Bool.xor_self, Bool.xor_false]

theorem parity_zero : ∀ es : List (Fin G.m), parity (zero G) es = false
  | [] => rfl
  | e :: es => by
    simp only [parity, zero]
    rw [Bool.false_xor]
    exact parity_zero es

theorem parity_append (s : Cochain G) : ∀ l l' : List (Fin G.m),
    parity s (l ++ l') = (parity s l ^^ parity s l')
  | [], l' => by
    simp only [List.nil_append, parity]
    rw [Bool.false_xor]
  | e :: l, l' => by
    simp only [List.cons_append, parity]
    rw [parity_append s l l', Bool.xor_assoc]

theorem parity_reverse (s : Cochain G) : ∀ l : List (Fin G.m),
    parity s l.reverse = parity s l
  | [] => rfl
  | e :: l => by
    rw [List.reverse_cons, parity_append, parity_reverse s l]
    simp only [parity]
    rw [Bool.xor_false, Bool.xor_comm]

theorem Walk.append {u v w : Fin G.n} {es es' : List (Fin G.m)}
    (h1 : Walk G u v es) (h2 : Walk G v w es') : Walk G u w (es ++ es') := by
  induction h1 with
  | nil => exact h2
  | cons he _ ih => exact Walk.cons he (ih h2)

theorem Walk.symm {u v : Fin G.n} {es : List (Fin G.m)} (h : Walk G u v es) :
    Walk G v u es.reverse := by
  induction h with
  | nil v => exact Walk.nil v
  | cons he _ ih =>
    rw [List.reverse_cons]
    exact Walk.append ih (Walk.cons he.symm (Walk.nil _))

/-- Every cycle (closed edge walk) of a cochain in the zero class is even. -/
theorem cycle_even_of_normal_zero (T : Forest G) {s : Cochain G} (h : normal T s = zero G)
    {u : Fin G.n} {es : List (Fin G.m)} (w : Walk G u u es) : parity s es = false := by
  obtain ⟨a, ha⟩ := (normal_eq_zero_iff T s).1 h
  have hs : s = switch G (zero G) a := by
    rw [← ha, switch_switch]
  rw [hs, closed_walk_invariant _ _ w, parity_zero]

/-! ### The forest path to the root, and fundamental cycles -/

def pathAux (T : Forest G) : Nat → Fin G.n → List (Fin G.m)
  | 0, _ => []
  | k + 1, v =>
    match T.parent v with
    | none => []
    | some e => e :: pathAux T k (G.other v e)

/-- The forest path from `v` up to its root, as a list of edges. -/
def pathTo (T : Forest G) (v : Fin G.n) : List (Fin G.m) :=
  pathAux T (T.depth v) v

theorem pathAux_fuel (T : Forest G) :
    ∀ k₁ k₂ v, T.depth v ≤ k₁ → T.depth v ≤ k₂ → pathAux T k₁ v = pathAux T k₂ v := by
  intro k₁
  induction k₁ with
  | zero =>
    intro k₂ v h1 h2
    cases k₂ with
    | zero => rfl
    | succ k₂ =>
      simp only [pathAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have := T.descends v e h
        omega
  | succ k₁ ih =>
    intro k₂ v h1 h2
    cases k₂ with
    | zero =>
      simp only [pathAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have := T.descends v e h
        omega
    | succ k₂ =>
      simp only [pathAux]
      cases h : T.parent v with
      | none => rfl
      | some e =>
        have hd := T.descends v e h
        dsimp only
        rw [ih k₂ (G.other v e) (by omega) (by omega)]

theorem pathTo_root (T : Forest G) {v : Fin G.n} (h : T.parent v = none) :
    pathTo T v = [] := by
  unfold pathTo
  rw [pathAux_fuel T (T.depth v) (T.depth v + 1) v (Nat.le_refl _) (Nat.le_succ _)]
  simp only [pathAux, h]

theorem pathTo_step (T : Forest G) {v : Fin G.n} {e : Fin G.m} (h : T.parent v = some e) :
    pathTo T v = e :: pathTo T (G.other v e) := by
  unfold pathTo
  rw [pathAux_fuel T (T.depth v) (T.depth v + 1) v (Nat.le_refl _) (Nat.le_succ _)]
  simp only [pathAux, h]
  have hd := T.descends v e h
  rw [pathAux_fuel T (T.depth v) (T.depth (G.other v e)) (G.other v e) (by omega) (Nat.le_refl _)]

theorem walk_pathTo (T : Forest G) (v : Fin G.n) : Walk G v (root T v) (pathTo T v) := by
  refine T.induction (fun v => Walk G v (root T v) (pathTo T v)) ?_ ?_ v
  · intro v h
    rw [pathTo_root T h, root_of_none T h]
    exact Walk.nil v
  · intro v e h ih
    rw [pathTo_step T h, root_step T h]
    exact Walk.cons (ends_other (T.incident v e h)) ih

theorem parity_pathTo (T : Forest G) (s : Cochain G) (v : Fin G.n) :
    parity s (pathTo T v) = potential T s v := by
  refine T.induction (fun v => parity s (pathTo T v) = potential T s v) ?_ ?_ v
  · intro v h
    rw [pathTo_root T h, potential_root T s h]
    rfl
  · intro v e h ih
    rw [pathTo_step T h, potential_step T s h]
    simp only [parity]
    rw [ih]

/-- The fundamental closed walk of an edge `e = uv`: root-to-`u` path, `e`, `v`-to-root path. -/
def fundamental (T : Forest G) (e : Fin G.m) : List (Fin G.m) :=
  (pathTo T (G.edge e).1).reverse ++ e :: pathTo T (G.edge e).2

theorem walk_fundamental (T : Forest G) (e : Fin G.m) :
    Walk G (root T (G.edge e).1) (root T (G.edge e).1) (fundamental T e) := by
  unfold fundamental
  refine Walk.append (walk_pathTo T (G.edge e).1).symm ?_
  refine Walk.cons (Or.inl rfl) ?_
  rw [root_edge T e]
  exact walk_pathTo T (G.edge e).2

theorem xor_fund (p a b : Bool) : (a ^^ (p ^^ b)) = (p ^^ (a ^^ b)) := by
  cases p <;> cases a <;> cases b <;> rfl

/-- The parity of the fundamental walk of `e` is the normal-form coordinate at `e`. -/
theorem parity_fundamental (T : Forest G) (s : Cochain G) (e : Fin G.m) :
    parity s (fundamental T e) = normal T s e := by
  unfold fundamental
  rw [parity_append, parity_reverse]
  simp only [parity, normal, switch, delta]
  rw [parity_pathTo, parity_pathTo]
  exact xor_fund _ _ _

/-- A forest edge is one that some vertex names as its parent edge. -/
def IsForestEdge (T : Forest G) (e : Fin G.m) : Prop :=
  ∃ v : Fin G.n, T.parent v = some e

instance (T : Forest G) : DecidablePred (IsForestEdge T) :=
  fun e => inferInstanceAs (Decidable (∃ v : Fin G.n, T.parent v = some e))

/-- Evenness of the fundamental walks of the chords alone forces the zero normal form. -/
theorem normal_zero_of_fundamental_even (T : Forest G) (s : Cochain G)
    (h : ∀ e, ¬ IsForestEdge T e → parity s (fundamental T e) = false) :
    normal T s = zero G := by
  funext e
  show normal T s e = false
  refine Decidable.byCases (p := IsForestEdge T e) ?_ ?_
  · rintro ⟨v, hv⟩
    exact normal_forest_zero T s hv
  · intro hf
    rw [← parity_fundamental T s e]
    exact h e hf

/-- T5, cycle form, with cycles read as closed edge walks. -/
theorem normal_eq_zero_iff_cycles (T : Forest G) (s : Cochain G) :
    normal T s = zero G ↔ ∀ (u : Fin G.n) (es : List (Fin G.m)), Walk G u u es → parity s es = false := by
  constructor
  · intro h u es w
    exact cycle_even_of_normal_zero T h w
  · intro h
    apply normal_zero_of_fundamental_even
    intro e _
    exact h _ _ (walk_fundamental T e)

/-- The three readings of the obstruction criterion, chained. -/
theorem obstruction_criterion (T : Forest G) (s : Cochain G) :
    (normal T s = zero G ↔ ∃ a : Potential G, switch G s a = zero G) ∧
    (normal T s = zero G ↔ ∀ (u : Fin G.n) (es : List (Fin G.m)), Walk G u u es → parity s es = false) :=
  ⟨normal_eq_zero_iff T s, normal_eq_zero_iff_cycles T s⟩

/-! ### Roots are representatives of the connected components -/

theorem comp_of_ends (T : Forest G) {e : Fin G.m} {u w : Fin G.n} (h : G.Ends e u w) :
    T.comp u = T.comp w := by
  have hc := T.edgeComp e
  rcases h with h | h
  · rw [h] at hc
    exact hc
  · rw [h] at hc
    exact hc.symm

theorem comp_of_walk (T : Forest G) {u v : Fin G.n} {es : List (Fin G.m)} (w : Walk G u v es) :
    T.comp u = T.comp v := by
  induction w with
  | nil => rfl
  | cons he _ ih => exact (comp_of_ends T he).trans ih

theorem walk_of_comp (T : Forest G) {u v : Fin G.n} (h : T.comp u = T.comp v) :
    Walk G u v (pathTo T u ++ (pathTo T v).reverse) := by
  refine Walk.append (walk_pathTo T u) ?_
  rw [root_eq_of_comp T h]
  exact (walk_pathTo T v).symm

/-- Two vertices are joined by a walk exactly when they carry the same component label. -/
theorem walk_iff_comp (T : Forest G) (u v : Fin G.n) :
    (∃ es, Walk G u v es) ↔ T.comp u = T.comp v :=
  ⟨fun ⟨_, w⟩ => comp_of_walk T w, fun h => ⟨_, walk_of_comp T h⟩⟩

/-! ## T4: the class count -/

/-- The chords: edges outside the forest. Loops are always chords. -/
abbrev Chord (T : Forest G) := {e : Fin G.m // ¬ IsForestEdge T e}

def restrict (T : Forest G) (s : Cochain G) : Chord T → Bool := fun e => s e.1

def extend (T : Forest G) (c : Chord T → Bool) : Cochain G :=
  fun e => if h : IsForestEdge T e then false else c ⟨e, h⟩

theorem extend_forest (T : Forest G) (c : Chord T → Bool) {v : Fin G.n} {e : Fin G.m}
    (h : T.parent v = some e) : extend T c e = false := by
  unfold extend
  rw [dite_eq_left_of_eq_true (eq_true ⟨v, h⟩)]

theorem extend_chord (T : Forest G) (c : Chord T → Bool) (e : Chord T) :
    extend T c e.1 = c e := by
  unfold extend
  rw [dite_eq_right_of_eq_false (eq_false e.2)]

theorem potential_of_forest_zero (T : Forest G) {s : Cochain G}
    (hs : ∀ v e, T.parent v = some e → s e = false) (v : Fin G.n) :
    potential T s v = false := by
  refine T.induction (fun v => potential T s v = false) ?_ ?_ v
  · intro v h
    exact potential_root T s h
  · intro v e h ih
    rw [potential_step T s h, hs v e h, ih]
    rfl

theorem normal_of_forest_zero (T : Forest G) {s : Cochain G}
    (hs : ∀ v e, T.parent v = some e → s e = false) : normal T s = s := by
  show switch G s (potential T s) = s
  have : potential T s = fun _ => false := funext (potential_of_forest_zero T hs)
  rw [this, switch_zero_potential]

theorem normal_extend (T : Forest G) (c : Chord T → Bool) :
    normal T (extend T c) = extend T c :=
  normal_of_forest_zero T (fun _ _ h => extend_forest T c h)

theorem restrict_extend (T : Forest G) (c : Chord T → Bool) :
    restrict T (extend T c) = c := by
  funext e
  exact extend_chord T c e

/-- A normal form is determined by its chord coordinates. -/
theorem normal_eq_extend_restrict (T : Forest G) (s : Cochain G) :
    normal T s = extend T (restrict T (normal T s)) := by
  funext e
  refine Decidable.byCases (p := IsForestEdge T e) ?_ ?_
  · rintro ⟨v, hv⟩
    rw [normal_forest_zero T s hv, extend_forest T _ hv]
  · intro hf
    rw [extend_chord T _ ⟨e, hf⟩]
    rfl

/-- Switching classes correspond to chord cochains: the map `s ↦ restrict (normal s)`
    identifies exactly the switching-equivalent cochains ... -/
theorem class_iff_chord (T : Forest G) (s t : Cochain G) :
    SameClass G s t ↔ restrict T (normal T s) = restrict T (normal T t) := by
  rw [same_class_iff T]
  constructor
  · intro h
    rw [h]
  · intro h
    rw [normal_eq_extend_restrict T s, normal_eq_extend_restrict T t, h]

/-- ... and reaches every chord cochain. -/
theorem chord_surj (T : Forest G) (c : Chord T → Bool) :
    ∃ s : Cochain G, restrict T (normal T s) = c :=
  ⟨extend T c, by rw [normal_extend, restrict_extend]⟩

/-! ### Counting chords: `|chords| + |V| = |E| + |roots|` -/

theorem length_filter_add_length_filter_not {α : Type} (p : α → Bool) :
    ∀ l : List α, (l.filter p).length + (l.filter (fun x => !p x)).length = l.length
  | [] => rfl
  | x :: l => by
    have ih := length_filter_add_length_filter_not p l
    cases hp : p x
    · rw [List.filter_cons_of_neg (by rw [hp]; exact Bool.false_ne_true),
        List.filter_cons_of_pos (by rw [hp]; rfl)]
      simp only [List.length_cons]
      omega
    · rw [List.filter_cons_of_pos hp, List.filter_cons_of_neg (by rw [hp]; exact Bool.false_ne_true)]
      simp only [List.length_cons]
      omega

def numForest (T : Forest G) : Nat :=
  ((List.finRange G.m).filter (fun e => decide (IsForestEdge T e))).length

def numChord (T : Forest G) : Nat :=
  ((List.finRange G.m).filter (fun e => !decide (IsForestEdge T e))).length

def numRoot (T : Forest G) : Nat :=
  ((List.finRange G.n).filter (fun v => decide (T.parent v = none))).length

def numNonRoot (T : Forest G) : Nat :=
  ((List.finRange G.n).filter (fun v => !decide (T.parent v = none))).length

theorem numForest_add_numChord (T : Forest G) : numForest T + numChord T = G.m := by
  unfold numForest numChord
  rw [length_filter_add_length_filter_not, List.length_finRange]

theorem numRoot_add_numNonRoot (T : Forest G) : numRoot T + numNonRoot T = G.n := by
  unfold numRoot numNonRoot
  rw [length_filter_add_length_filter_not, List.length_finRange]

/-- Each forest edge is the parent edge of exactly one vertex. -/
theorem parent_inj (T : Forest G) {u v : Fin G.n} {e : Fin G.m}
    (hu : T.parent u = some e) (hv : T.parent v = some e) : u = v := by
  have du := T.descends u e hu
  have dv := T.descends v e hv
  have iu := T.incident u e hu
  have iv := T.incident v e hv
  unfold Graph.other at du dv
  rcases iu with iu | iu <;> rcases iv with iv | iv
  · exact iu.symm.trans iv
  · rw [ite_eq_left_of_eq_true _ _ (eq_true iu), iv] at du
    refine Decidable.byCases (p := (G.edge e).1 = v) ?_ ?_
    · intro h1
      exact iu.symm.trans h1
    · intro h1
      rw [ite_eq_right_of_eq_false _ _ (eq_false h1), iu] at dv
      exact absurd (Nat.lt_trans du dv) (Nat.lt_irrefl _)
  · rw [ite_eq_left_of_eq_true _ _ (eq_true iv), iu] at dv
    refine Decidable.byCases (p := (G.edge e).1 = u) ?_ ?_
    · intro h1
      exact h1.symm.trans iv
    · intro h1
      rw [ite_eq_right_of_eq_false _ _ (eq_false h1), iv] at du
      exact absurd (Nat.lt_trans du dv) (Nat.lt_irrefl _)
  · exact iu.symm.trans iv

theorem nodup_map_of_inj_on {α β : Type} (f : α → β) :
    ∀ l : List α, l.Nodup → (∀ a, a ∈ l → ∀ b, b ∈ l → f a = f b → a = b) → (l.map f).Nodup
  | [], _, _ => List.Pairwise.nil
  | x :: l, hl, hf => by
    rw [List.map_cons, List.nodup_cons]
    rw [List.nodup_cons] at hl
    constructor
    · intro hmem
      rw [List.mem_map] at hmem
      obtain ⟨a, ha, hfa⟩ := hmem
      have := hf a (List.mem_cons_of_mem x ha) x (List.mem_cons_self) hfa
      exact hl.1 (this ▸ ha)
    · exact nodup_map_of_inj_on f l hl.2
        (fun a ha b hb h => hf a (List.mem_cons_of_mem x ha) b (List.mem_cons_of_mem x hb) h)

theorem nonRootList_nodup (T : Forest G) :
    (((List.finRange G.n).filter (fun v => !decide (T.parent v = none))).map T.parent).Nodup := by
  apply nodup_map_of_inj_on
  · exact List.Nodup.sublist List.filter_sublist (List.nodup_finRange _)
  · intro a ha b _ hab
    rw [List.mem_filter] at ha
    have ha2 := ha.2
    cases h : T.parent a with
    | none =>
      rw [h, decide_eq_true rfl] at ha2
      exact absurd ha2 Bool.false_ne_true
    | some e =>
      rw [h] at hab
      exact parent_inj T h hab.symm

theorem forestList_nodup (T : Forest G) :
    (((List.finRange G.m).filter (fun e => decide (IsForestEdge T e))).map some).Nodup := by
  apply nodup_map_of_inj_on
  · exact List.Nodup.sublist List.filter_sublist (List.nodup_finRange _)
  · intro a _ b _ hab
    exact Option.some.inj hab

theorem mem_nonRootList_iff (T : Forest G) (x : Option (Fin G.m)) :
    x ∈ ((List.finRange G.n).filter (fun v => !decide (T.parent v = none))).map T.parent ↔
    x ∈ ((List.finRange G.m).filter (fun e => decide (IsForestEdge T e))).map some := by
  rw [List.mem_map, List.mem_map]
  constructor
  · rintro ⟨v, hv, rfl⟩
    rw [List.mem_filter] at hv
    have hv2 := hv.2
    cases h : T.parent v with
    | none =>
      rw [h, decide_eq_true rfl] at hv2
      exact absurd hv2 Bool.false_ne_true
    | some e =>
      refine ⟨e, ?_, rfl⟩
      rw [List.mem_filter]
      exact ⟨List.mem_finRange e, decide_eq_true ⟨v, h⟩⟩
  · rintro ⟨e, he, rfl⟩
    rw [List.mem_filter] at he
    obtain ⟨v, hv⟩ := of_decide_eq_true he.2
    refine ⟨v, ?_, hv⟩
    rw [List.mem_filter]
    refine ⟨List.mem_finRange v, ?_⟩
    rw [hv]
    rfl

/-- A duplicate-free list is no longer than any list containing its members
    (proved here to stay inside `{propext, Quot.sound}`). -/
theorem nodup_subset_length_le {α : Type} :
    ∀ (l₁ l₂ : List α), l₁.Nodup → (∀ x, x ∈ l₁ → x ∈ l₂) → l₁.length ≤ l₂.length
  | [], _, _, _ => Nat.zero_le _
  | x :: l₁, l₂, hn, hsub => by
    rw [List.nodup_cons] at hn
    obtain ⟨s, t, rfl⟩ := List.append_of_mem (hsub x List.mem_cons_self)
    have hsub' : ∀ y, y ∈ l₁ → y ∈ s ++ t := by
      intro y hy
      have hy2 := hsub y (List.mem_cons_of_mem x hy)
      rw [List.mem_append, List.mem_cons] at hy2
      rw [List.mem_append]
      rcases hy2 with h | h | h
      · exact Or.inl h
      · exact absurd (h ▸ hy) hn.1
      · exact Or.inr h
    have ih := nodup_subset_length_le l₁ (s ++ t) hn.2 hsub'
    rw [List.length_append] at ih
    rw [List.length_append, List.length_cons, List.length_cons]
    omega

theorem numNonRoot_eq_numForest (T : Forest G) : numNonRoot T = numForest T := by
  have h1 := nodup_subset_length_le _ _ (nonRootList_nodup T)
    (fun x hx => (mem_nonRootList_iff T x).1 hx)
  have h2 := nodup_subset_length_le _ _ (forestList_nodup T)
    (fun x hx => (mem_nonRootList_iff T x).2 hx)
  rw [List.length_map, List.length_map] at h1 h2
  exact Nat.le_antisymm h1 h2

/-- `|chords| = |E| - |V| + c` with `c` the number of roots, as a Nat identity. -/
theorem numChord_identity (T : Forest G) : numChord T + G.n = G.m + numRoot T := by
  have h1 := numForest_add_numChord T
  have h2 := numRoot_add_numNonRoot T
  have h3 := numNonRoot_eq_numForest T
  omega

/-! ### Counting switching classes: `2 ^ numChord T` normal forms -/

/-- Set the value of a cochain at edge `e` to `b`, leaving other edges unchanged. -/
def setAt (G : Graph) (e : Fin G.m) (b : Bool) (s : Cochain G) : Cochain G :=
  fun i => if i = e then b else s i

/-- Cochains supported on a list `L` of edges (`false` outside `L`). -/
def supportedOn (G : Graph) (L : List (Fin G.m)) (s : Cochain G) : Prop :=
  ∀ i : Fin G.m, i ∉ L → s i = false

/-- Enumerate all `2 ^ L.length` cochains supported on `L`. -/
def chordNormalForms (G : Graph) : List (Fin G.m) → List (Cochain G)
  | [] => [zero G]
  | e :: es =>
    (chordNormalForms G es).map (setAt G e false) ++
    (chordNormalForms G es).map (setAt G e true)

theorem chordNormalForms_length (G : Graph) :
    ∀ L : List (Fin G.m), (chordNormalForms G L).length = 2 ^ L.length
  | [] => rfl
  | e :: es => by
    simp only [chordNormalForms, List.length_append, List.length_map, List.length_cons,
      chordNormalForms_length G es, Nat.pow_succ]
    omega

theorem supportedOn_of_mem_chordNormalForms (G : Graph) :
    ∀ (L : List (Fin G.m)) (s : Cochain G),
      s ∈ chordNormalForms G L → supportedOn G L s
  | [], s, hs => by
    rw [chordNormalForms, List.mem_singleton] at hs
    subst hs
    intro _ _
    rfl
  | e :: es, s, hs => by
    rw [chordNormalForms, List.mem_append, List.mem_map, List.mem_map] at hs
    intro i hi
    have hie : i ≠ e := fun h => hi (h ▸ List.mem_cons_self)
    have hies : i ∉ es := fun h => hi (List.mem_cons_of_mem e h)
    rcases hs with ⟨t, ht, rfl⟩ | ⟨t, ht, rfl⟩
    · simp only [setAt, ite_eq_right_of_eq_false _ _ (eq_false hie)]
      exact supportedOn_of_mem_chordNormalForms G es t ht i hies
    · simp only [setAt, ite_eq_right_of_eq_false _ _ (eq_false hie)]
      exact supportedOn_of_mem_chordNormalForms G es t ht i hies

theorem mem_chordNormalForms_of_supportedOn (G : Graph) :
    ∀ (L : List (Fin G.m)) (s : Cochain G),
      supportedOn G L s → s ∈ chordNormalForms G L
  | [], s, hs => by
    rw [chordNormalForms, List.mem_singleton]
    funext i
    exact hs i (by intro h; cases h)
  | e :: es, s, hs => by
    rw [chordNormalForms, List.mem_append, List.mem_map, List.mem_map]
    let s₀ : Cochain G := setAt G e false s
    have hs₀ : supportedOn G es s₀ := by
      intro i hi
      unfold s₀ setAt
      by_cases hie : i = e
      · rw [ite_eq_left_of_eq_true _ _ (eq_true hie)]
      · rw [ite_eq_right_of_eq_false _ _ (eq_false hie)]
        exact hs i (by intro hm; rcases List.mem_cons.1 hm with h1 | h2; exact hie h1; exact hi h2)
    have hmem₀ := mem_chordNormalForms_of_supportedOn G es s₀ hs₀
    cases hse : s e
    · left
      refine ⟨s₀, hmem₀, ?_⟩
      funext i
      unfold s₀ setAt
      by_cases hie : i = e
      · subst hie
        simp [hse]
      · simp [hie]
    · right
      refine ⟨s₀, hmem₀, ?_⟩
      funext i
      unfold s₀ setAt
      by_cases hie : i = e
      · subst hie
        simp [hse]
      · simp [hie]

theorem mem_chordNormalForms_iff (G : Graph) (L : List (Fin G.m)) (s : Cochain G) :
    s ∈ chordNormalForms G L ↔ supportedOn G L s :=
  ⟨supportedOn_of_mem_chordNormalForms G L s, mem_chordNormalForms_of_supportedOn G L s⟩

theorem nodup_append_of_disjoint {α : Type} :
    ∀ (l₁ l₂ : List α), l₁.Nodup → l₂.Nodup → (∀ x, x ∈ l₁ → x ∉ l₂) → (l₁ ++ l₂).Nodup
  | [], l₂, _, h2, _ => h2
  | x :: l₁, l₂, h1, h2, hdis => by
    rw [List.cons_append, List.nodup_cons]
    rw [List.nodup_cons] at h1
    refine ⟨?_, nodup_append_of_disjoint l₁ l₂ h1.2 h2 (fun y hy => hdis y (List.mem_cons_of_mem x hy))⟩
    intro hmem
    rw [List.mem_append] at hmem
    rcases hmem with hm1 | hm2
    · exact h1.1 hm1
    · exact hdis x List.mem_cons_self hm2

theorem setAt_inj_on_chordNormalForms (G : Graph) (e : Fin G.m) (es : List (Fin G.m))
    (he : e ∉ es) (b : Bool) :
    ∀ a, a ∈ chordNormalForms G es → ∀ c, c ∈ chordNormalForms G es →
      setAt G e b a = setAt G e b c → a = c := by
  intro a ha c hc h
  have ha0 := supportedOn_of_mem_chordNormalForms G es a ha e he
  have hc0 := supportedOn_of_mem_chordNormalForms G es c hc e he
  funext i
  by_cases hie : i = e
  · subst hie
    exact ha0.trans hc0.symm
  · have hi := congrFun h i
    simpa [setAt, hie] using hi

theorem chordNormalForms_nodup (G : Graph) :
    ∀ (L : List (Fin G.m)), L.Nodup → (chordNormalForms G L).Nodup
  | [], _ => List.Pairwise.cons (by intro _ h; cases h) List.Pairwise.nil
  | e :: es, hl => by
    rw [List.nodup_cons] at hl
    have ih := chordNormalForms_nodup G es hl.2
    simp only [chordNormalForms]
    apply nodup_append_of_disjoint
    · exact nodup_map_of_inj_on (setAt G e false) _ ih
        (setAt_inj_on_chordNormalForms G e es hl.1 false)
    · exact nodup_map_of_inj_on (setAt G e true) _ ih
        (setAt_inj_on_chordNormalForms G e es hl.1 true)
    · intro s hs1 hs2
      rw [List.mem_map] at hs1 hs2
      obtain ⟨a, _, rfl⟩ := hs1
      obtain ⟨c, _, heq⟩ := hs2
      have hval := congrFun heq e
      simp [setAt] at hval

def chordList (T : Forest G) : List (Fin G.m) :=
  (List.finRange G.m).filter (fun e => !decide (IsForestEdge T e))

/-- The duplicate-free list of all `2 ^ numChord T` switching normal forms on `(G, T)`. -/
def normalForms (T : Forest G) : List (Cochain G) :=
  chordNormalForms G (chordList T)

/-- There are `2 ^ numChord T` normal forms on `(G, T)`. -/
theorem normalForms_length (T : Forest G) :
    (normalForms T).length = 2 ^ numChord T := by
  unfold normalForms numChord chordList
  exact chordNormalForms_length G _

/-- The normal-form enumeration is duplicate-free. -/
theorem normalForms_nodup (T : Forest G) :
    (normalForms T).Nodup := by
  apply chordNormalForms_nodup
  exact List.Nodup.sublist List.filter_sublist (List.nodup_finRange G.m)

/-- A cochain is in `normalForms T` iff it is the normal form of some cochain on `G`. -/
theorem mem_normalForms_iff (T : Forest G) (c : Cochain G) :
    c ∈ normalForms T ↔ ∃ s : Cochain G, normal T s = c := by
  unfold normalForms
  rw [mem_chordNormalForms_iff]
  constructor
  · intro hsupp
    refine ⟨c, ?_⟩
    apply normal_of_forest_zero T
    intro v e hv
    apply hsupp e
    unfold chordList
    rw [List.mem_filter]
    intro ⟨_, hnot⟩
    have hf : decide (IsForestEdge T e) = true := decide_eq_true ⟨v, hv⟩
    rw [hf] at hnot
    exact Bool.noConfusion hnot
  · rintro ⟨s, rfl⟩
    intro e he
    refine Decidable.byCases (p := IsForestEdge T e) ?_ ?_
    · rintro ⟨v, hv⟩
      exact normal_forest_zero T s hv
    · intro hf
      exfalso
      apply he
      unfold chordList
      rw [List.mem_filter]
      refine ⟨List.mem_finRange e, ?_⟩
      cases h : decide (IsForestEdge T e)
      · rfl
      · exact absurd (of_decide_eq_true h) hf

/-! ## Instances (checked by `decide`) -/

/-- A graph on `k + 1` vertices from a list of endpoint pairs (read modulo `k + 1`). -/
def Graph.ofList (k : Nat) (es : List (Nat × Nat)) : Graph where
  n := k + 1
  m := es.length
  edge := fun i =>
    (⟨(es[i]).1 % (k + 1), Nat.mod_lt _ (Nat.succ_pos k)⟩,
     ⟨(es[i]).2 % (k + 1), Nat.mod_lt _ (Nat.succ_pos k)⟩)

/-- A forest witness from per-vertex lists: parent edge index, depth, component label. -/
def Forest.ofLists (G : Graph) (par : List (Option Nat)) (dep comp : List Nat)
    (h1 : ∀ v e, (fun v : Fin G.n =>
        match par.getD v.1 none with
        | none => none
        | some j => if h : j < G.m then some (⟨j, h⟩ : Fin G.m) else none) v = some e →
        G.Incident v e)
    (h2 : ∀ v e, (fun v : Fin G.n =>
        match par.getD v.1 none with
        | none => none
        | some j => if h : j < G.m then some (⟨j, h⟩ : Fin G.m) else none) v = some e →
        (fun v : Fin G.n => dep.getD v.1 0) (G.other v e) < (fun v : Fin G.n => dep.getD v.1 0) v)
    (h3 : ∀ e, (fun v : Fin G.n => comp.getD v.1 0) (G.edge e).1 =
        (fun v : Fin G.n => comp.getD v.1 0) (G.edge e).2)
    (h4 : ∀ u v, (fun v : Fin G.n =>
        match par.getD v.1 none with
        | none => none
        | some j => if h : j < G.m then some (⟨j, h⟩ : Fin G.m) else none) u = none →
        (fun v : Fin G.n =>
        match par.getD v.1 none with
        | none => none
        | some j => if h : j < G.m then some (⟨j, h⟩ : Fin G.m) else none) v = none →
        (fun v : Fin G.n => comp.getD v.1 0) u = (fun v : Fin G.n => comp.getD v.1 0) v → u = v) :
    Forest G where
  parent := fun v =>
    match par.getD v.1 none with
    | none => none
    | some j => if h : j < G.m then some (⟨j, h⟩ : Fin G.m) else none
  depth := fun v => dep.getD v.1 0
  comp := fun v => comp.getD v.1 0
  incident := h1
  descends := h2
  edgeComp := h3
  rootUnique := h4

/-- Read a cochain off the bits of a natural number. -/
def ofBits (G : Graph) (x : Nat) : Cochain G := fun i => x.testBit i.1

/-- Pack a cochain into a natural number. -/
def toBits (G : Graph) (s : Cochain G) : Nat :=
  (List.finRange G.m).foldr (fun i acc => 2 * acc + (if s i then 1 else 0)) 0

/-- The number of distinct normal forms over all `2^m` cochains: a finite census of the
    switching classes, to be compared with `2^(m - n + c)`. -/
def numClasses (G : Graph) (T : Forest G) : Nat :=
  ((List.range (2 ^ G.m)).map (fun x => toBits G (normal T (ofBits G x)))).eraseDups.length

/-! ### Instance 1: the triangle (3 vertices, edges 01, 12, 20) -/

def tri : Graph := Graph.ofList 2 [(0, 1), (1, 2), (2, 0)]

def triT : Forest tri :=
  Forest.ofLists tri [none, some 0, some 1] [0, 1, 2] [0, 0, 0]
    (by decide) (by decide) (by decide) (by decide)

example : numClasses tri triT = 2 := by decide
example : numChord triT = 1 ∧ numRoot triT = 1 := by decide

/-! ### Instance 2: one loop (1 vertex, edge 00) -/

def loopG : Graph := Graph.ofList 0 [(0, 0)]

def loopT : Forest loopG :=
  Forest.ofLists loopG [none] [0] [0] (by decide) (by decide) (by decide) (by decide)

example : numClasses loopG loopT = 2 := by decide
example : numChord loopT = 1 ∧ numRoot loopT = 1 := by decide
/-- The loop is a chord, and its sign is a switching invariant. -/
example : ¬ IsForestEdge loopT ⟨0, by decide⟩ := by decide

/-! ### Instance 3: a pair of parallel edges (2 vertices, edges 01, 01) -/

def parG : Graph := Graph.ofList 1 [(0, 1), (0, 1)]

def parT : Forest parG :=
  Forest.ofLists parG [none, some 0] [0, 1] [0, 0] (by decide) (by decide) (by decide) (by decide)

example : numClasses parG parT = 2 := by decide
example : numChord parT = 1 ∧ numRoot parT = 1 := by decide

/-! ### Instance 4: a triangle plus an isolated vertex (two components) -/

def isoG : Graph := Graph.ofList 3 [(0, 1), (1, 2), (2, 0)]

def isoT : Forest isoG :=
  Forest.ofLists isoG [none, some 0, some 1, none] [0, 1, 2, 0] [0, 0, 0, 1]
    (by decide) (by decide) (by decide) (by decide)

example : numClasses isoG isoT = 2 := by decide
example : numChord isoT = 1 ∧ numRoot isoT = 2 := by decide

/-! ### Instance 5: a square with one diagonal (4 vertices, 5 edges) -/

def sqG : Graph := Graph.ofList 3 [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]

def sqT : Forest sqG :=
  Forest.ofLists sqG [none, some 0, some 1, some 2] [0, 1, 2, 3] [0, 0, 0, 0]
    (by decide) (by decide) (by decide) (by decide)

example : numClasses sqG sqT = 4 := by decide
example : numChord sqT = 2 ∧ numRoot sqT = 1 := by decide

/-! ## Re-deriving the deposit's triangle theorems from the general ones

The four definitions below are copied verbatim from
`F004_papers/008_fsp/lean4/NormalFormLaws.lean` lines 56 to 71 (`TriangleSigns`,
`triangleCycle`, `triangleNormal`, `triangleGauge`, `triangleEquivalent`). -/

namespace DepositTriangle

structure TriangleSigns where
  s01 : Bool
  s12 : Bool
  s20 : Bool
deriving DecidableEq, Repr

def triangleCycle (s : TriangleSigns) : Bool :=
  (s.s01.xor s.s12).xor s.s20

def triangleNormal (s : TriangleSigns) : TriangleSigns :=
  ⟨false, false, triangleCycle s⟩

def triangleGauge (a0 a1 a2 : Bool) (s : TriangleSigns) : TriangleSigns :=
  ⟨(s.s01.xor a0).xor a1, (s.s12.xor a1).xor a2, (s.s20.xor a2).xor a0⟩

def triangleEquivalent (s t : TriangleSigns) : Prop :=
  ∃ a0 a1 a2 : Bool, triangleGauge a0 a1 a2 s = t

end DepositTriangle

open DepositTriangle

def e0 : Fin tri.m := ⟨0, by decide⟩
def e1 : Fin tri.m := ⟨1, by decide⟩
def e2 : Fin tri.m := ⟨2, by decide⟩
def v0 : Fin tri.n := ⟨0, by decide⟩
def v1 : Fin tri.n := ⟨1, by decide⟩
def v2 : Fin tri.n := ⟨2, by decide⟩

def toCochain (s : TriangleSigns) : Cochain tri :=
  fun i => if i.1 = 0 then s.s01 else if i.1 = 1 then s.s12 else s.s20

def ofCochain (c : Cochain tri) : TriangleSigns := ⟨c e0, c e1, c e2⟩

def toPotential (a0 a1 a2 : Bool) : Potential tri :=
  fun v => if v.1 = 0 then a0 else if v.1 = 1 then a1 else a2

theorem cochain_ext3 (c d : Cochain tri) (h0 : c e0 = d e0) (h1 : c e1 = d e1)
    (h2 : c e2 = d e2) : c = d := by
  funext i
  rcases i with ⟨i, hi⟩
  have hm : i < 3 := hi
  match i, hm with
  | 0, _ => exact h0
  | 1, _ => exact h1
  | 2, _ => exact h2

theorem ofCochain_toCochain (s : TriangleSigns) : ofCochain (toCochain s) = s := by
  rcases s with ⟨a, b, c⟩
  rfl

/-- The general normal form on the triangle graph is the deposit's `triangleNormal`. -/
theorem normal_tri (s : TriangleSigns) :
    normal triT (toCochain s) = toCochain (triangleNormal s) := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> exact cochain_ext3 _ _ rfl rfl rfl

theorem gauge_tri (a0 a1 a2 : Bool) (s : TriangleSigns) :
    toCochain (triangleGauge a0 a1 a2 s) = switch tri (toCochain s) (toPotential a0 a1 a2) := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;> cases a0 <;> cases a1 <;> cases a2 <;>
    exact cochain_ext3 _ _ rfl rfl rfl

theorem equivalent_iff_sameClass (s t : TriangleSigns) :
    triangleEquivalent s t ↔ SameClass tri (toCochain s) (toCochain t) := by
  constructor
  · rintro ⟨a0, a1, a2, h⟩
    exact ⟨toPotential a0 a1 a2, by rw [← h, gauge_tri]⟩
  · rintro ⟨a, ha⟩
    refine ⟨a v0, a v1, a v2, ?_⟩
    have h0 : t.s01 = (s.s01 ^^ (a v0 ^^ a v1)) := congrFun ha e0
    have h1 : t.s12 = (s.s12 ^^ (a v1 ^^ a v2)) := congrFun ha e1
    have h2 : t.s20 = (s.s20 ^^ (a v2 ^^ a v0)) := congrFun ha e2
    rcases t with ⟨t0, t1, t2⟩
    simp only at h0 h1 h2
    rw [h0, h1, h2]
    show TriangleSigns.mk _ _ _ = TriangleSigns.mk _ _ _
    rw [Bool.xor_assoc, Bool.xor_assoc, Bool.xor_assoc]

/-- The deposit's `triangle_complete`, derived from `same_class_iff` on the triangle graph. -/
theorem triangle_complete' (s t : TriangleSigns) :
    triangleNormal s = triangleNormal t ↔ triangleEquivalent s t := by
  rw [equivalent_iff_sameClass, same_class_iff triT, normal_tri, normal_tri]
  constructor
  · intro h
    rw [h]
  · intro h
    rw [← ofCochain_toCochain (triangleNormal s), ← ofCochain_toCochain (triangleNormal t), h]

/-- The deposit's `odd_triangle_cannot_be_switched_positive`, derived from `normal_eq_zero_iff`. -/
theorem odd_triangle_cannot_be_switched_positive' (s : TriangleSigns)
    (h : triangleCycle s = true) (a0 a1 a2 : Bool) :
    triangleGauge a0 a1 a2 s ≠ ⟨false, false, false⟩ := by
  intro hz
  have hsw : switch tri (toCochain s) (toPotential a0 a1 a2) = zero tri := by
    rw [← gauge_tri, hz]
    exact cochain_ext3 _ _ rfl rfl rfl
  have hn := (normal_eq_zero_iff triT (toCochain s)).2 ⟨_, hsw⟩
  rw [normal_tri] at hn
  have h2 := congrFun hn e2
  simp only [toCochain, triangleNormal, zero] at h2
  rw [h] at h2
  exact absurd h2 (by decide)

#print axioms normal_sound
#print axioms normal_forest_zero
#print axioms normal_idem
#print axioms normal_switch
#print axioms same_class_iff
#print axioms normal_eq_zero_iff
#print axioms cycle_even_of_normal_zero
#print axioms normal_zero_of_fundamental_even
#print axioms normal_eq_zero_iff_cycles
#print axioms obstruction_criterion
#print axioms walk_iff_comp
#print axioms class_iff_chord
#print axioms chord_surj
#print axioms numChord_identity
#print axioms normalForms_length
#print axioms normalForms_nodup
#print axioms mem_normalForms_iff
#print axioms triangle_complete'
#print axioms odd_triangle_cannot_be_switched_positive'

end SwitchingNormalForm
