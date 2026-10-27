/- Imported so that this repository carries its own Lean evidence.
   Original sha256: b0f6365df8b146d3b8e798b7f2c21dd59ca5f60a37cde258942f6ace9d3ff8e7 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.Paper
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-! Preservation statements for the consolidated manuscript.
No Mathlib, proof oracle, source-level axiom or omitted proof is used.
Classical choice is used for arbitrary report images and the alphabet bijection.
-/
namespace PreMssn

def ReportImage {H V : Type} (report : H → V) :=
  {v : V // ∃ h, report h = v}

theorem history_report_criterion {H V S : Type}
    (report : H → V) (answer : H → S) :
    (∃ factor : ReportImage report → S,
      ∀ h, factor ⟨report h, ⟨h, rfl⟩⟩ = answer h) ↔
    (∀ h h', report h = report h' → answer h = answer h') := by
  constructor
  · rintro ⟨factor, hf⟩ h h' heq
    have hv : (⟨report h, ⟨h, rfl⟩⟩ : ReportImage report) =
        ⟨report h', ⟨h', rfl⟩⟩ := Subtype.ext heq
    rw [← hf h, ← hf h', hv]
  · intro hc
    classical
    refine ⟨fun v => answer (Classical.choose v.property), ?_⟩
    intro h
    exact hc _ _ (Classical.choose_spec (show ∃ h', report h' = report h from ⟨h, rfl⟩))

theorem history_factor_unique {H V S : Type}
    (report : H → V) (answer : H → S)
    (a b : ReportImage report → S)
    (ha : ∀ h, a ⟨report h, ⟨h, rfl⟩⟩ = answer h)
    (hb : ∀ h, b ⟨report h, ⟨h, rfl⟩⟩ = answer h) : a = b := by
  funext v
  obtain ⟨h, hh⟩ := v.property
  have hv : (⟨report h, ⟨h, rfl⟩⟩ : ReportImage report) = v := Subtype.ext hh
  rw [← hv, ha, hb]

theorem collapsed_observation_barrier {A V S : Type}
    (report : A → V) (task : A → S) (x y : A)
    (same : report x = report y) (different : task x ≠ task y) :
    ¬ ∃ factor : V → S, ∀ a, factor (report a) = task a := by
  rintro ⟨factor, hf⟩
  apply different
  rw [← hf x, ← hf y, same]

theorem empty_observations {A : Type} (x y : A) :
    ∀ o : Empty, (Empty.elim o : A → Unit) x = (Empty.elim o : A → Unit) y := by
  intro o
  exact Empty.elim o

theorem irreflexive_endpoints {A : Type} (R : A → A → Prop)
    (hirr : ∀ a, ¬ R a a) {a b : A} (h : R a b) : a ≠ b := by
  intro eq
  exact hirr a (eq ▸ h)

theorem old_image_injective {A B E : Type} (u : A → B) (r : B → Sum A E)
    (old : ∀ a, r (u a) = Sum.inl a) {a b : A} (h : u a = u b) : a = b := by
  have heq : Sum.inl (β := E) a = Sum.inl b := by rw [← old a, h, old b]
  exact Sum.inl.inj heq

def refineReport {A O T : Type} (q : A → O) (t : A → T) (a : A) := (q a, t a)

theorem refine_preserves {A O T : Type} (q : A → O) (t : A → T) (a : A) :
    (refineReport q t a).1 = q a := rfl

theorem refine_separates {A O T : Type} (q : A → O) (t : A → T)
    (a b : A) (different : t a ≠ t b) : refineReport q t a ≠ refineReport q t b := by
  intro eq
  exact different (congrArg Prod.snd eq)

theorem triangle_not_two_colored (a b c : Bool) :
    ¬ (a ≠ b ∧ b ≠ c ∧ c ≠ a) := by
  cases a <;> cases b <;> cases c <;> simp

theorem filter_partition {A : Type} (xs : List A) (p : A → Bool) :
    (xs.filter p).length + (xs.filter (fun a => !(p a))).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
      cases hp : p a <;> simp [List.filter, hp] at * <;> omega

/-- Finite sets are represented by distinct-element lists. The predicate marks
exactly the discharged subset; births must be disjoint from the residual. -/
theorem demand_accounting {A : Type} (active births : List A) (discharged : A → Bool) :
    ((active.filter (fun a => !(discharged a))) ++ births).length =
      active.length - (active.filter discharged).length + births.length := by
  have hp := filter_partition active discharged
  simp only [List.length_append]
  omega

theorem demand_register_nodup {A : Type} (active births : List A)
    (discharged : A → Bool) (ha : active.Nodup) (hb : births.Nodup)
    (disjoint : ∀ x, x ∈ active → discharged x = false → x ∉ births) :
    ((active.filter (fun a => !(discharged a))) ++ births).Nodup := by
  apply List.nodup_append.mpr
  refine ⟨ha.filter _, hb, ?_⟩
  intro a ha' b hb' eq
  obtain ⟨hm, hd⟩ := List.mem_filter.mp ha'
  have hf : discharged a = false := by cases h : discharged a <;> simp_all
  exact disjoint a hm hf (eq ▸ hb')

/-- Fixed-degree fragment of a chain complex. Subtraction is supplied by the
chain group; the theorem uses only the displayed map laws and retraction. -/
structure ChainFragment where
  upper : Type
  middle : Type
  lower : Type
  zero : lower
  sub : middle → middle → middle
  boundary : upper → middle
  differential : middle → lower
  square_zero : ∀ b, differential (boundary b) = zero

structure ChainMap (C D : ChainFragment) where
  upper : C.upper → D.upper
  middle : C.middle → D.middle
  lower : C.lower → D.lower
  boundary_commutes : ∀ b, middle (C.boundary b) = D.boundary (upper b)
  differential_commutes : ∀ z, lower (C.differential z) = D.differential (middle z)
  zero_preserved : lower C.zero = D.zero
  sub_preserved : ∀ x y, middle (C.sub x y) = D.sub (middle x) (middle y)

def IsCycle (C : ChainFragment) (z : C.middle) := C.differential z = C.zero
def IsBoundary (C : ChainFragment) (z : C.middle) := ∃ b, C.boundary b = z
def Homologous (C : ChainFragment) (x y : C.middle) := IsBoundary C (C.sub x y)

theorem chain_map_cycles {C D : ChainFragment} (i : ChainMap C D)
    (z : C.middle) (hz : IsCycle C z) : IsCycle D (i.middle z) := by
  unfold IsCycle at *
  rw [← i.differential_commutes, hz, i.zero_preserved]

theorem chain_retraction_reflects_boundaries {C D : ChainFragment}
    (i : ChainMap C D) (r : ChainMap D C)
    (fixes : ∀ z, r.middle (i.middle z) = z)
    (z : C.middle) (h : IsBoundary D (i.middle z)) : IsBoundary C z := by
  obtain ⟨b, hb⟩ := h
  refine ⟨r.upper b, ?_⟩
  rw [← r.boundary_commutes, hb, fixes]

theorem chain_retraction_reflects_homology {C D : ChainFragment}
    (i : ChainMap C D) (r : ChainMap D C)
    (fixes : ∀ z, r.middle (i.middle z) = z)
    (x y : C.middle) (h : Homologous D (i.middle x) (i.middle y)) :
    Homologous C x y := by
  unfold Homologous at *
  rw [← i.sub_preserved] at h
  exact chain_retraction_reflects_boundaries i r fixes _ h

theorem chain_retraction_cannot_kill {C D : ChainFragment}
    (i : ChainMap C D) (r : ChainMap D C)
    (fixes : ∀ z, r.middle (i.middle z) = z)
    (z : C.middle) (nonboundary : ¬ IsBoundary C z) :
    ¬ IsBoundary D (i.middle z) := by
  intro h
  exact nonboundary (chain_retraction_reflects_boundaries i r fixes z h)

/-- The two-vertex boundary has coordinates (-1,1), hence is nonzero. -/
theorem bridge_boundary_nonzero : ((-1 : Int), (1 : Int)) ≠ (0, 0) := by decide

def triangleBoundary (x y z : Int) := (z - x, x - y, y - z)

theorem triangle_cycle : triangleBoundary 1 1 1 = (0, 0, 0) := by decide
theorem triangle_face_square_zero (k : Int) : triangleBoundary k k k = (0, 0, 0) := by
  simp [triangleBoundary]
theorem triangle_cycle_nonzero : ((1 : Int), (1 : Int), (1 : Int)) ≠ (0, 0, 0) := by decide

def binaryCode : List Bool → List Bool
  | [] => []
  | false :: xs => false :: binaryCode xs
  | true :: xs => false :: false :: binaryCode xs

theorem code_aa_b_collision : binaryCode [false, false] = binaryCode [true] := rfl
theorem code_ab_ba_collision : binaryCode [false, true] = binaryCode [true, false] := rfl
theorem code_not_injective : ¬ ∀ x y, binaryCode x = binaryCode y → x = y := by
  intro h
  have bad := h [false, false] [true] code_aa_b_collision
  contradiction

def unitAtom {A : Type} (w : List A) :=
  w ≠ [] ∧ ∀ u v, w = u ++ v → u = [] ∨ v = []

theorem word_atom_iff_singleton {A : Type} (w : List A) :
    unitAtom w ↔ ∃ a, w = [a] := by
  constructor
  · rintro ⟨hne, hp⟩
    cases w with
    | nil => exact False.elim (hne rfl)
    | cons a xs =>
        have h := hp [a] xs rfl
        cases h with
        | inl h => contradiction
        | inr h => exact ⟨a, h ▸ rfl⟩
  · rintro ⟨a, rfl⟩
    refine ⟨by simp, ?_⟩
    intro u v eq
    cases u with
    | nil => exact Or.inl rfl
    | cons b xs =>
        have tail : xs ++ v = [] := (List.cons.inj eq).2.symm
        exact Or.inr (List.append_eq_nil_iff.mp tail).2

structure WordIso (A B : Type) where
  forward : List A → List B
  backward : List B → List A
  forward_empty : forward [] = []
  backward_empty : backward [] = []
  forward_append : ∀ u v, forward (u ++ v) = forward u ++ forward v
  backward_append : ∀ u v, backward (u ++ v) = backward u ++ backward v
  left_inverse : ∀ w, backward (forward w) = w
  right_inverse : ∀ w, forward (backward w) = w

def WordIso.symm {A B : Type} (e : WordIso A B) : WordIso B A :=
  ⟨e.backward, e.forward, e.backward_empty, e.forward_empty, e.backward_append,
    e.forward_append, e.right_inverse, e.left_inverse⟩

theorem word_iso_preserves_atoms {A B : Type} (e : WordIso A B)
    (w : List A) (h : unitAtom w) : unitAtom (e.forward w) := by
  refine ⟨?_, ?_⟩
  · intro eq
    have old := congrArg e.backward eq
    rw [e.left_inverse, e.backward_empty] at old
    exact h.1 old
  · intro u v eq
    have old := congrArg e.backward eq
    rw [e.left_inverse, e.backward_append] at old
    cases h.2 _ _ old with
    | inl hu =>
        left
        have back := congrArg e.forward hu
        rw [e.right_inverse, e.forward_empty] at back
        exact back
    | inr hv =>
        right
        have back := congrArg e.forward hv
        rw [e.right_inverse, e.forward_empty] at back
        exact back

/-- Explicit bijection between alphabet carriers induced by a free-monoid iso.
Equality of finite alphabet cardinalities follows from this carrier bijection. -/
theorem word_iso_alphabet_bijection {A B : Type} (e : WordIso A B) :
    ∃ f : A → B, ∃ g : B → A, (∀ a, g (f a) = a) ∧ (∀ b, f (g b) = b) := by
  classical
  have hf : ∀ a, ∃ b, e.forward [a] = [b] := by
    intro a
    obtain ⟨b, hb⟩ := (word_atom_iff_singleton _).mp
      (word_iso_preserves_atoms e [a] ((word_atom_iff_singleton _).mpr ⟨a, rfl⟩))
    exact ⟨b, hb⟩
  have hg : ∀ b, ∃ a, e.backward [b] = [a] := by
    intro b
    exact (word_atom_iff_singleton _).mp
      (word_iso_preserves_atoms e.symm [b] ((word_atom_iff_singleton _).mpr ⟨b, rfl⟩))
  let f := fun a => Classical.choose (hf a)
  let g := fun b => Classical.choose (hg b)
  have hforward : ∀ a, e.forward [a] = [f a] := fun a => Classical.choose_spec (hf a)
  have hbackward : ∀ b, e.backward [b] = [g b] := fun b => Classical.choose_spec (hg b)
  refine ⟨f, g, ?_, ?_⟩
  · intro a
    have eq := congrArg e.backward (hforward a)
    rw [e.left_inverse, hbackward] at eq
    exact (List.cons.inj eq).1.symm
  · intro b
    have eq := congrArg e.forward (hbackward b)
    rw [e.right_inverse, hforward] at eq
    exact (List.cons.inj eq).1.symm

theorem finite_injection_card_le {n m : Nat} (f : Fin n → Fin m)
    (injective : ∀ a b, f a = f b → a = b) : n ≤ m := by
  have nodup : ((List.finRange n).map f).Nodup := by
    apply List.pairwise_map.mpr
    exact (List.nodup_finRange n).imp (fun hne heq => hne (injective _ _ heq))
  have bound := nodup.length_le_of_subset (l₂ := List.finRange m)
    (fun _ _ => List.mem_finRange _)
  simpa using bound

theorem finite_word_iso_card_eq {n m : Nat} (e : WordIso (Fin n) (Fin m)) : n = m := by
  obtain ⟨f, g, hf, hg⟩ := word_iso_alphabet_bijection e
  have left := finite_injection_card_le f (fun a b eq => by rw [← hf a, eq, hf b])
  have right := finite_injection_card_le g (fun a b eq => by rw [← hg a, eq, hg b])
  omega

theorem unequal_finite_alphabets_not_iso {n m : Nat} (different : n ≠ m) :
    ¬ Nonempty (WordIso (Fin n) (Fin m)) := by
  rintro ⟨e⟩
  exact different (finite_word_iso_card_eq e)

theorem alphabet_filter_retraction {A : Type} (xs : List A) (p : A → Bool)
    (h : ∀ x, x ∈ xs → p x = true) : xs.filter p = xs := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simp [List.filter, h a (by simp), ih (fun x hx => h x (by simp [hx]))]

def chsh (a b c d : Int) := (a + b + c - d, a + b - c + d)
theorem missed_chsh_orientation : chsh 1 1 (-1) 1 = (0, 4) := by decide

theorem deterministic_sign_product (a0 a1 b0 b1 : Bool) :
    Bool.xor (Bool.xor (Bool.xor a0 b0) (Bool.xor a0 b1))
      (Bool.xor (Bool.xor a1 b0) (Bool.xor a1 b1)) = false := by
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide

end PreMssn
