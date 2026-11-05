import Second.Cost

/-!
# Changes commute with rewriting the terms

`rename π s` is `s` with every term `x` written `π x`.  For a one-to-one `π`
every change of the second seed becomes a change of the same kind on the
renamed state (`Step3.rename`), and so does every sequence (`Reach3.rename`);
the size is unchanged (`size_rename`).  This is the step the first derivation
left open (its O3): it carries the statements proved for the writing `a = 0`,
`b = 1` to every writing.

Derived here with it:
* `result_iff_A`, `result_iff_B`: a state is reached from some writing of what
  is given exactly when it is legal, well formed, keeps `a` and `b` two terms
  and asserts `arb` (and `bra`, if given);
* `fewest_changes3_every_writing_A`, `_B`: from some writing of what is given
  the state is reached in exactly `size − size(given)` changes, and from no
  writing in fewer.
-/

namespace Seed.Second

open Seed St

/-- The state with every term `x` written `π x`. -/
def rename (π : ℕ → ℕ) (s : St) : St :=
  ⟨s.T.image π, s.A.image (Prod.map π π), π s.a, π s.b⟩

variable {π : ℕ → ℕ}

theorem rename_addTerm (s : St) (t : ℕ) :
    rename π (s.addTerm t) = (rename π s).addTerm (π t) := by
  simp [rename, St.addTerm, Finset.image_insert]

theorem rename_addAssertion (s : St) (x y : ℕ) :
    rename π (s.addAssertion x y) = (rename π s).addAssertion (π x) (π y) := by
  simp [rename, St.addAssertion, Finset.image_insert, Prod.map]

theorem merge_rename (hπ : Function.Injective π) (u v x : ℕ) :
    π (merge u v x) = merge (π u) (π v) (π x) := by
  unfold merge
  by_cases h : x = v
  · subst h
    simp
  · rw [if_neg h, if_neg (fun e => h (hπ e))]

theorem rename_identify (hπ : Function.Injective π) (s : St) (u v : ℕ) :
    rename π (s.identify u v) = (rename π s).identify (π u) (π v) := by
  apply St.ext
  · exact Finset.image_erase hπ s.T v
  · simp only [rename, St.identify, Finset.image_image]
    congr 1
    funext p
    obtain ⟨x, y⟩ := p
    simp [Prod.map, merge_rename hπ]
  · exact merge_rename hπ u v s.a
  · exact merge_rename hπ u v s.b

theorem mem_rename_T (hπ : Function.Injective π) {s : St} {x : ℕ} :
    π x ∈ (rename π s).T ↔ x ∈ s.T := by
  simp [rename, Finset.mem_image, hπ.eq_iff]

theorem mem_rename_A (hπ : Function.Injective π) {s : St} {x y : ℕ} :
    (π x, π y) ∈ (rename π s).A ↔ (x, y) ∈ s.A := by
  constructor
  · intro h
    obtain ⟨⟨u, v⟩, hp, he⟩ := Finset.mem_image.1 h
    simp only [Prod.map, Prod.mk.injEq] at he
    obtain ⟨rfl, rfl⟩ : u = x ∧ v = y := ⟨hπ he.1, hπ he.2⟩
    exact hp
  · intro h
    exact Finset.mem_image.2 ⟨(x, y), h, rfl⟩

/-- A change of the second seed, after rewriting, is a change of the same kind. -/
theorem Step3.rename (hπ : Function.Injective π) {s t : St} (h : Step3 s t) :
    Step3 (rename π s) (rename π t) := by
  cases h with
  | addTerm t ht =>
    rw [rename_addTerm]
    exact Step3.addTerm _ _ ((mem_rename_T hπ).not.2 ht)
  | addAssertion x y hx hy hxy hnew =>
    rw [rename_addAssertion]
    exact Step3.addAssertion _ _ _ ((mem_rename_T hπ).2 hx) ((mem_rename_T hπ).2 hy)
      (hπ.ne hxy) ((mem_rename_A hπ).not.2 hnew)
  | identify u v hu hv huv h1 h2 =>
    rw [rename_identify hπ]
    exact Step3.identify _ _ _ ((mem_rename_T hπ).2 hu) ((mem_rename_T hπ).2 hv)
      (hπ.ne huv) ((mem_rename_A hπ).not.2 h1) ((mem_rename_A hπ).not.2 h2)

/-- A sequence of changes, after rewriting, is a sequence of the same length. -/
theorem Reach3.rename (hπ : Function.Injective π) {s t : St} {n : ℕ} (h : Reach3 s t n) :
    Reach3 (rename π s) (rename π t) n := by
  induction h with
  | refl => exact Reach3.refl _
  | step _ st ih => exact Reach3.step ih (st.rename hπ)

theorem size_rename (hπ : Function.Injective π) (s : St) : (rename π s).size = s.size := by
  simp only [St.size, rename]
  rw [Finset.card_image_of_injective _ hπ, Finset.card_image_of_injective _ (hπ.prodMap hπ)]

theorem rename_rename (π σ : ℕ → ℕ) (s : St) : rename σ (rename π s) = rename (σ ∘ π) s := by
  simp [rename, Finset.image_image, Prod.map_comp_map]

theorem rename_id (s : St) : rename id s = s := by
  apply St.ext <;> simp [rename]

theorem rename_symm_apply (π : Equiv.Perm ℕ) (s : St) : rename π (rename π.symm s) = s := by
  rw [rename_rename, Equiv.self_comp_symm]
  exact rename_id s

theorem legal_rename (hπ : Function.Injective π) {s : St} (hs : s.Legal) : (rename π s).Legal := by
  intro x hx
  obtain ⟨⟨y, z⟩, hp, he⟩ := Finset.mem_image.1 hx
  simp only [Prod.map, Prod.mk.injEq] at he
  have : y = z := hπ (he.1.trans he.2.symm)
  subst this
  exact hs _ hp

theorem wf_rename {s : St} (hs : s.WF) : (rename π s).WF := by
  obtain ⟨hA, ha, hb⟩ := hs
  refine ⟨fun p hp => ?_, Finset.mem_image_of_mem π ha, Finset.mem_image_of_mem π hb⟩
  obtain ⟨⟨y, z⟩, hq, rfl⟩ := Finset.mem_image.1 hp
  exact ⟨Finset.mem_image_of_mem π (hA _ hq).1, Finset.mem_image_of_mem π (hA _ hq).2⟩

theorem rename_a (s : St) : (rename π s).a = π s.a := rfl

theorem rename_b (s : St) : (rename π s).b = π s.b := rfl

/-- Two different terms can be written `0` and `1` by a rewriting. -/
theorem exists_perm_of_ne {a b : ℕ} (hab : a ≠ b) : ∃ π : Equiv.Perm ℕ, π 0 = a ∧ π 1 = b := by
  set b' := Equiv.swap 0 a b with hb'
  have hb0 : b' ≠ 0 := by
    intro h
    rw [hb', Equiv.swap_apply_eq_iff, Equiv.swap_apply_left] at h
    exact hab h.symm
  refine ⟨Equiv.swap 0 a * Equiv.swap 1 b', ?_, ?_⟩
  · rw [Equiv.Perm.mul_apply, Equiv.swap_apply_of_ne_of_ne (by omega) (Ne.symm hb0),
      Equiv.swap_apply_left]
  · rw [Equiv.Perm.mul_apply, Equiv.swap_apply_left, hb', Equiv.swap_apply_self]

/-- What is given, rewritten by `π`, still asserts `arb` between its named terms. -/
theorem rename_givenA_arb (π : Equiv.Perm ℕ) :
    ((rename π givenA).a, (rename π givenA).b) ∈ (rename π givenA).A :=
  (mem_rename_A π.injective).2 givenA_arb

theorem rename_givenB_arb (π : Equiv.Perm ℕ) :
    ((rename π givenB).a, (rename π givenB).b) ∈ (rename π givenB).A :=
  (mem_rename_A π.injective).2 givenB_arb

theorem rename_givenB_bra (π : Equiv.Perm ℕ) :
    ((rename π givenB).b, (rename π givenB).a) ∈ (rename π givenB).A :=
  (mem_rename_A π.injective).2 givenB_bra

/-- **The results, `bra` not asserted to begin with.**  A state is reached from some
writing of what is given exactly when it is legal, well formed, keeps `a` and `b` two
terms, and asserts `arb`. -/
theorem result_iff_A (g : St) :
    (∃ (π : Equiv.Perm ℕ) (n : ℕ), Reach3 (rename π givenA) g n) ↔
      (g.Legal ∧ g.WF ∧ g.a ≠ g.b ∧ (g.a, g.b) ∈ g.A) := by
  constructor
  · rintro ⟨π, n, h⟩
    have hl := legal_rename π.injective givenA_legal
    have hw := wf_rename (π := π) givenA_wf
    exact ⟨h.legal hl, h.wf hw, h.names_apart hl (rename_givenA_arb π),
      h.arb_persists (rename_givenA_arb π)⟩
  · rintro ⟨hg, hgw, hne, hab⟩
    obtain ⟨π, h0, h1⟩ := exists_perm_of_ne hne
    have ha' : (rename π.symm g).a = 0 := by
      rw [rename_a, Equiv.symm_apply_eq, h0]
    have hb' : (rename π.symm g).b = 1 := by
      rw [rename_b, Equiv.symm_apply_eq, h1]
    have hab' : (0, 1) ∈ (rename π.symm g).A := by
      have := (mem_rename_A π.symm.injective (s := g)).2 hab
      rwa [show π.symm g.a = 0 from ha', show π.symm g.b = 1 from hb'] at this
    obtain ⟨n, hn, _⟩ := fewest_changes3_upper_A (legal_rename π.symm.injective hg)
      (wf_rename hgw) ha' hb' hab'
    refine ⟨π, n, ?_⟩
    have := hn.rename π.injective
    rwa [rename_symm_apply] at this

/-- **The results, `bra` asserted to begin with.** -/
theorem result_iff_B (g : St) :
    (∃ (π : Equiv.Perm ℕ) (n : ℕ), Reach3 (rename π givenB) g n) ↔
      (g.Legal ∧ g.WF ∧ g.a ≠ g.b ∧ (g.a, g.b) ∈ g.A ∧ (g.b, g.a) ∈ g.A) := by
  constructor
  · rintro ⟨π, n, h⟩
    have hl := legal_rename π.injective givenB_legal
    have hw := wf_rename (π := π) givenB_wf
    exact ⟨h.legal hl, h.wf hw, h.names_apart hl (rename_givenB_arb π),
      h.arb_persists (rename_givenB_arb π), h.bra_persists (rename_givenB_bra π)⟩
  · rintro ⟨hg, hgw, hne, hab, hba⟩
    obtain ⟨π, h0, h1⟩ := exists_perm_of_ne hne
    have ha' : (rename π.symm g).a = 0 := by
      rw [rename_a, Equiv.symm_apply_eq, h0]
    have hb' : (rename π.symm g).b = 1 := by
      rw [rename_b, Equiv.symm_apply_eq, h1]
    have hab' : (0, 1) ∈ (rename π.symm g).A := by
      have := (mem_rename_A π.symm.injective (s := g)).2 hab
      rwa [show π.symm g.a = 0 from ha', show π.symm g.b = 1 from hb'] at this
    have hba' : (1, 0) ∈ (rename π.symm g).A := by
      have := (mem_rename_A π.symm.injective (s := g)).2 hba
      rwa [show π.symm g.a = 0 from ha', show π.symm g.b = 1 from hb'] at this
    obtain ⟨n, hn, _⟩ := fewest_changes3_upper_B (legal_rename π.symm.injective hg)
      (wf_rename hgw) ha' hb' hab' hba'
    refine ⟨π, n, ?_⟩
    have := hn.rename π.injective
    rwa [rename_symm_apply] at this

/-- **Fewest changes for every writing, `bra` not asserted to begin with.**  From some
writing of what is given the state is reached in exactly `size − 3` changes, and from
no writing in fewer. -/
theorem fewest_changes3_every_writing_A {g : St} (hg : g.Legal) (hgw : g.WF) (hne : g.a ≠ g.b)
    (hab : (g.a, g.b) ∈ g.A) :
    (∃ (π : Equiv.Perm ℕ) (n : ℕ), Reach3 (rename π givenA) g n ∧ n + 3 = g.size) ∧
      ∀ (π : Equiv.Perm ℕ) (n : ℕ), Reach3 (rename π givenA) g n → g.size ≤ n + 3 := by
  constructor
  · obtain ⟨π, h0, h1⟩ := exists_perm_of_ne hne
    have ha' : (rename π.symm g).a = 0 := by
      rw [rename_a, Equiv.symm_apply_eq, h0]
    have hb' : (rename π.symm g).b = 1 := by
      rw [rename_b, Equiv.symm_apply_eq, h1]
    have hab' : (0, 1) ∈ (rename π.symm g).A := by
      have := (mem_rename_A π.symm.injective (s := g)).2 hab
      rwa [show π.symm g.a = 0 from ha', show π.symm g.b = 1 from hb'] at this
    obtain ⟨n, hn, hc⟩ := fewest_changes3_upper_A (legal_rename π.symm.injective hg)
      (wf_rename hgw) ha' hb' hab'
    refine ⟨π, n, ?_, ?_⟩
    · have := hn.rename π.injective
      rwa [rename_symm_apply] at this
    · rwa [size_rename π.symm.injective] at hc
  · intro π n h
    have := h.size_le
    rw [size_rename π.injective, size_givenA] at this
    omega

/-- **Fewest changes for every writing, `bra` asserted to begin with.** -/
theorem fewest_changes3_every_writing_B {g : St} (hg : g.Legal) (hgw : g.WF) (hne : g.a ≠ g.b)
    (hab : (g.a, g.b) ∈ g.A) (hba : (g.b, g.a) ∈ g.A) :
    (∃ (π : Equiv.Perm ℕ) (n : ℕ), Reach3 (rename π givenB) g n ∧ n + 4 = g.size) ∧
      ∀ (π : Equiv.Perm ℕ) (n : ℕ), Reach3 (rename π givenB) g n → g.size ≤ n + 4 := by
  constructor
  · obtain ⟨π, h0, h1⟩ := exists_perm_of_ne hne
    have ha' : (rename π.symm g).a = 0 := by
      rw [rename_a, Equiv.symm_apply_eq, h0]
    have hb' : (rename π.symm g).b = 1 := by
      rw [rename_b, Equiv.symm_apply_eq, h1]
    have hab' : (0, 1) ∈ (rename π.symm g).A := by
      have := (mem_rename_A π.symm.injective (s := g)).2 hab
      rwa [show π.symm g.a = 0 from ha', show π.symm g.b = 1 from hb'] at this
    have hba' : (1, 0) ∈ (rename π.symm g).A := by
      have := (mem_rename_A π.symm.injective (s := g)).2 hba
      rwa [show π.symm g.a = 0 from ha', show π.symm g.b = 1 from hb'] at this
    obtain ⟨n, hn, hc⟩ := fewest_changes3_upper_B (legal_rename π.symm.injective hg)
      (wf_rename hgw) ha' hb' hab' hba'
    refine ⟨π, n, ?_, ?_⟩
    · have := hn.rename π.injective
      rwa [rename_symm_apply] at this
    · rwa [size_rename π.symm.injective] at hc
  · intro π n h
    have := h.size_le
    rw [size_rename π.injective, size_givenB] at this
    omega

/-! ## O3: First-seed rewriting commutation (`Step.rename`, `Reach.rename`, `fewest_changes_every_writing_A/B`) -/

theorem rename_remove (hπ : Function.Injective π) (s : St) (p : ℕ × ℕ) :
    rename π (s.remove p) = (rename π s).remove (Prod.map π π p) := by
  apply St.ext
  · rfl
  · exact Finset.image_erase (hπ.prodMap hπ) s.A p
  · rfl
  · rfl

/-- A change of the first seed, after rewriting, is a change of the same kind (`O3`). -/
theorem Step.rename (hπ : Function.Injective π) {s t : St} (h : Step s t) :
    Step (rename π s) (rename π t) := by
  cases h with
  | addTerm t ht =>
    rw [rename_addTerm]
    exact Step.addTerm _ _ ((mem_rename_T hπ).not.2 ht)
  | addAssertion x y hx hy hxy hnew =>
    rw [rename_addAssertion]
    exact Step.addAssertion _ _ _ ((mem_rename_T hπ).2 hx) ((mem_rename_T hπ).2 hy)
      (hπ.ne hxy) ((mem_rename_A hπ).not.2 hnew)
  | remove p hp =>
    rcases p with ⟨x, y⟩
    rw [rename_remove hπ]
    exact Step.remove _ (π x, π y) ((mem_rename_A hπ).2 hp)
  | identify u v hu hv huv h1 h2 =>
    rw [rename_identify hπ]
    exact Step.identify _ _ _ ((mem_rename_T hπ).2 hu) ((mem_rename_T hπ).2 hv)
      (hπ.ne huv) ((mem_rename_A hπ).not.2 h1) ((mem_rename_A hπ).not.2 h2)

/-- A sequence of first-seed changes, after rewriting, is a sequence of the same length (`O3`). -/
theorem Reach.rename (hπ : Function.Injective π) {s t : St} {n : ℕ} (h : Reach s t n) :
    Reach (rename π s) (rename π t) n := by
  induction h with
  | refl => exact Reach.refl _
  | step _ st ih => exact Reach.step ih (Step.rename hπ st)

theorem miss_rename (hπ : Function.Injective π) (s : St) (x y : ℕ) :
    miss (rename π s) (π x) (π y) = miss s x y := by
  unfold miss
  by_cases h : (x, y) ∈ s.A
  · have h' : (π x, π y) ∈ (rename π s).A := (mem_rename_A hπ).2 h
    simp [h, h']
  · have h' : (π x, π y) ∉ (rename π s).A := (mem_rename_A hπ).not.2 h
    simp [h, h']

theorem lostA_rename (hπ : Function.Injective π) (s : St) :
    lostA (rename π s) = lostA s := by
  unfold lostA
  simp only [rename_a, rename_b, hπ.eq_iff, miss_rename hπ]

theorem lostB_rename (hπ : Function.Injective π) (s : St) :
    lostB (rename π s) = lostB s := by
  unfold lostB
  simp only [rename_a, rename_b, hπ.eq_iff, miss_rename hπ]

theorem costA_rename (hπ : Function.Injective π) (s : St) :
    costA (rename π s) = costA s := by
  simp [costA, size_rename hπ, lostA_rename hπ]

theorem costB_rename (hπ : Function.Injective π) (s : St) :
    costB (rename π s) = costB s := by
  simp [costB, size_rename hπ, lostB_rename hπ]

/-- **O3: Fewest changes for every writing of the first seed, `bra` not asserted to begin with.**
From some writing of what is given, any legal well-formed state `g` is reached in
`costA g - 3` changes, and from no writing in fewer. -/
theorem fewest_changes_every_writing_A {g : St} (hg : g.Legal) (hgw : g.WF) :
    (∃ (π : Equiv.Perm ℕ) (n : ℕ), Reach (rename π givenA) g n ∧ n + 3 = costA g) ∧
      ∀ (π : Equiv.Perm ℕ) (n : ℕ), Reach (rename π givenA) g n → costA g ≤ n + 3 := by
  constructor
  · by_cases hne : g.a = g.b
    · let π : Equiv.Perm ℕ := Equiv.swap 0 g.a
      have ha' : (rename π.symm g).a = 0 := by
        simp [π, rename_a]
      have hb' : (rename π.symm g).b = 0 := by
        simp [π, rename_b, ← hne]
      obtain ⟨n, hn, hc⟩ := fewest_changes_upper_A_merged
        (legal_rename π.symm.injective hg) (wf_rename hgw) ha' hb'
      refine ⟨π, n, ?_, ?_⟩
      · have := Reach.rename π.injective hn
        rwa [rename_symm_apply] at this
      · rwa [costA_rename π.symm.injective] at hc
    · obtain ⟨π, h0, h1⟩ := exists_perm_of_ne hne
      have ha' : (rename π.symm g).a = 0 := by
        rw [rename_a, Equiv.symm_apply_eq, h0]
      have hb' : (rename π.symm g).b = 1 := by
        rw [rename_b, Equiv.symm_apply_eq, h1]
      obtain ⟨n, hn, hc⟩ := fewest_changes_upper_A_apart
        (legal_rename π.symm.injective hg) (wf_rename hgw) ha' hb'
      refine ⟨π, n, ?_, ?_⟩
      · have := Reach.rename π.injective hn
        rwa [rename_symm_apply] at this
      · rwa [costA_rename π.symm.injective] at hc
  · intro π n h
    have h' := Reach.rename π.symm.injective h
    rw [ ← rename_rename, Equiv.symm_comp_self, rename_id] at h'
    have hlow := fewest_changes_lower_A h'
    rwa [costA_rename π.symm.injective] at hlow

/-- **O3: Fewest changes for every writing of the first seed, `bra` asserted to begin with.** -/
theorem fewest_changes_every_writing_B {g : St} (hg : g.Legal) (hgw : g.WF) :
    (∃ (π : Equiv.Perm ℕ) (n : ℕ), Reach (rename π givenB) g n ∧ n + 4 = costB g) ∧
      ∀ (π : Equiv.Perm ℕ) (n : ℕ), Reach (rename π givenB) g n → costB g ≤ n + 4 := by
  constructor
  · by_cases hne : g.a = g.b
    · let π : Equiv.Perm ℕ := Equiv.swap 0 g.a
      have ha' : (rename π.symm g).a = 0 := by
        simp [π, rename_a]
      have hb' : (rename π.symm g).b = 0 := by
        simp [π, rename_b, ← hne]
      obtain ⟨n, hn, hc⟩ := fewest_changes_upper_B_merged
        (legal_rename π.symm.injective hg) (wf_rename hgw) ha' hb'
      refine ⟨π, n, ?_, ?_⟩
      · have := Reach.rename π.injective hn
        rwa [rename_symm_apply] at this
      · rwa [costB_rename π.symm.injective] at hc
    · obtain ⟨π, h0, h1⟩ := exists_perm_of_ne hne
      have ha' : (rename π.symm g).a = 0 := by
        rw [rename_a, Equiv.symm_apply_eq, h0]
      have hb' : (rename π.symm g).b = 1 := by
        rw [rename_b, Equiv.symm_apply_eq, h1]
      obtain ⟨n, hn, hc⟩ := fewest_changes_upper_B_apart
        (legal_rename π.symm.injective hg) (wf_rename hgw) ha' hb'
      refine ⟨π, n, ?_, ?_⟩
      · have := Reach.rename π.injective hn
        rwa [rename_symm_apply] at this
      · rwa [costB_rename π.symm.injective] at hc
  · intro π n h
    have h' := Reach.rename π.symm.injective h
    rw [← rename_rename, Equiv.symm_comp_self, rename_id] at h'
    have hlow := fewest_changes_lower_B h'
    rwa [costB_rename π.symm.injective] at hlow

/-! ## O6: Multi-step obstruction persistence (`D5` for a sequence of changes) -/

/-- A sequence of `n` performed changes from `s` to `t` that tracks an asserted pair `(u₀, v₀)`
    to `(u, v)` without removing the tracked pair at any step (`O6` / multi-step `D5`). -/
inductive ReachNoRemove : St → ℕ → ℕ → St → ℕ → ℕ → ℕ → Prop
  | refl (s : St) (u v : ℕ) : ReachNoRemove s u v s u v 0
  | addTerm {s t : St} {u₀ v₀ u v w n : ℕ}
      (r : ReachNoRemove s u₀ v₀ t u v n) (hw : w ∉ t.T) :
      ReachNoRemove s u₀ v₀ (t.addTerm w) u v (n + 1)
  | addAssertion {s t : St} {u₀ v₀ u v x y n : ℕ}
      (r : ReachNoRemove s u₀ v₀ t u v n) (hx : x ∈ t.T) (hy : y ∈ t.T)
      (hxy : x ≠ y) (hnew : (x, y) ∉ t.A) :
      ReachNoRemove s u₀ v₀ (t.addAssertion x y) u v (n + 1)
  | removeOther {s t : St} {u₀ v₀ u v n : ℕ} {p : ℕ × ℕ}
      (r : ReachNoRemove s u₀ v₀ t u v n) (hp : p ∈ t.A) (hne : p ≠ (u, v)) :
      ReachNoRemove s u₀ v₀ (t.remove p) u v (n + 1)
  | identify {s t : St} {u₀ v₀ u v p q n : ℕ}
      (r : ReachNoRemove s u₀ v₀ t u v n) (hp : p ∈ t.T) (hq : q ∈ t.T)
      (hpq : p ≠ q) (h1 : (p, q) ∉ t.A) (h2 : (q, p) ∉ t.A) :
      ReachNoRemove s u₀ v₀ (t.identify p q) (merge p q u) (merge p q v) (n + 1)

theorem ReachNoRemove.toReach {s t : St} {u₀ v₀ u v n : ℕ}
    (h : ReachNoRemove s u₀ v₀ t u v n) : Reach s t n := by
  induction h with
  | refl s u v => exact Reach.refl s
  | addTerm _ hw ih => exact Reach.step ih (Step.addTerm _ _ hw)
  | addAssertion _ hx hy hxy hnew ih => exact Reach.step ih (Step.addAssertion _ _ _ hx hy hxy hnew)
  | removeOther _ hp _ ih => exact Reach.step ih (Step.remove _ _ hp)
  | identify _ hp hq hpq h1 h2 ih => exact Reach.step ih (Step.identify _ _ _ hp hq hpq h1 h2)

/-- **O6 (Multi-step `D5`, tracked form):** Along any sequence of changes that never removes
the tracked pair, the pair remains asserted between two distinct terms and identifying them
remains obstructed. -/
theorem ReachNoRemove.obstruction_persists {s t : St} {u₀ v₀ u v n : ℕ}
    (h : ReachNoRemove s u₀ v₀ t u v n) (hs : s.Legal) (huv₀ : (u₀, v₀) ∈ s.A) :
    (u, v) ∈ t.A ∧ u ≠ v ∧ ¬ (t.identify u v).Legal := by
  induction h with
  | refl s u v =>
    have hne : u ≠ v := by rintro rfl; exact hs u huv₀
    have hobs : ¬ (s.identify u v).Legal := by
      rw [identify_legal_iff hs]
      intro h12
      exact h12.1 huv₀
    exact ⟨huv₀, hne, hobs⟩
  | addTerm r hw ih =>
    obtain ⟨hmem, hne, _⟩ := ih
    have ht_leg : ( _ ).Legal := (r.toReach.step (Step.addTerm _ _ hw)).legal hs
    refine ⟨hmem, hne, ?_⟩
    rw [identify_legal_iff ht_leg]
    intro h12
    exact h12.1 hmem
  | addAssertion r hx hy hxy hnew ih =>
    obtain ⟨hmem, hne, _⟩ := ih
    have hmem' : (u, v) ∈ ( _ ).A := Finset.mem_insert_of_mem hmem
    have ht_leg := (r.toReach.step (Step.addAssertion _ _ _ hx hy hxy hnew)).legal hs
    refine ⟨hmem', hne, ?_⟩
    rw [identify_legal_iff ht_leg]
    intro h12
    exact h12.1 hmem'
  | removeOther r hp hne_p ih =>
    obtain ⟨hmem, hne, _⟩ := ih
    have hmem' : (u, v) ∈ ( _ ).A := Finset.mem_erase.2 ⟨fun e => hne_p e.symm, hmem⟩
    have ht_leg := (r.toReach.step (Step.remove _ _ hp)).legal hs
    refine ⟨hmem', hne, ?_⟩
    rw [identify_legal_iff ht_leg]
    intro h12
    exact h12.1 hmem'
  | identify r hp hq hpq h1 h2 ih =>
    obtain ⟨hmem, _, _⟩ := ih
    have hprev_leg := r.toReach.legal hs
    have hmem' := mem_identify.2 ⟨(u, v), hmem, rfl⟩
    have hne' := identify_keeps_apart hprev_leg h1 h2 hmem
    have ht_leg := (r.toReach.step (Step.identify _ _ _ hp hq hpq h1 h2)).legal hs
    refine ⟨hmem', hne', ?_⟩
    rw [identify_legal_iff ht_leg]
    intro h12
    exact h12.1 hmem'

/-- **O6 (Multi-step `D5`, general `Reach` decomposition):** For any sequence of `n` performed
changes `Reach s t n` from a legal state `s` with `(u₀, v₀) ∈ s.A`, either the tracked assertion
survives the entire sequence as `(u, v) ∈ t.A` (with `u ≠ v` and `identify u v` obstructed), or
the sequence explicitly removes the tracked assertion at some intermediate step. -/
theorem obstruction_persists_reach {s t : St} {n : ℕ} (h : Reach s t n)
    (hs : s.Legal) {u₀ v₀ : ℕ} (huv₀ : (u₀, v₀) ∈ s.A) :
    (∃ u v, ReachNoRemove s u₀ v₀ t u v n ∧ (u, v) ∈ t.A ∧ u ≠ v ∧ ¬ (t.identify u v).Legal) ∨
      ∃ (m k : ℕ) (mid : St) (u v : ℕ),
        m + 1 + k = n ∧ ReachNoRemove s u₀ v₀ mid u v m ∧ (u, v) ∈ mid.A ∧
          Reach (mid.remove (u, v)) t k := by
  induction h with
  | refl =>
    left
    have hnr := ReachNoRemove.refl s u₀ v₀
    obtain ⟨h1, h2, h3⟩ := hnr.obstruction_persists hs huv₀
    exact ⟨u₀, v₀, hnr, h1, h2, h3⟩
  | step r st ih =>
    rcases ih with ⟨u, v, hnr, hmem, hne, hobs⟩ | ⟨m, k, mid, u, v, hlen, hnr, hmem, htail⟩
    · cases st with
      | addTerm _ w hw =>
        left
        have hnr' := ReachNoRemove.addTerm hnr hw
        obtain ⟨h1, h2, h3⟩ := hnr'.obstruction_persists hs huv₀
        exact ⟨u, v, hnr', h1, h2, h3⟩
      | addAssertion _ x y hx hy hxy hnew =>
        left
        have hnr' := ReachNoRemove.addAssertion hnr hx hy hxy hnew
        obtain ⟨h1, h2, h3⟩ := hnr'.obstruction_persists hs huv₀
        exact ⟨u, v, hnr', h1, h2, h3⟩
      | remove _ p hp =>
        by_cases hpe : p = (u, v)
        · subst hpe
          right
          exact ⟨_, 0, _, u, v, by omega, hnr, hmem, Reach.refl _⟩
        · left
          have hnr' := ReachNoRemove.removeOther hnr hp hpe
          obtain ⟨h1, h2, h3⟩ := hnr'.obstruction_persists hs huv₀
          exact ⟨u, v, hnr', h1, h2, h3⟩
      | identify _ p q hp hq hpq h1 h2 =>
        left
        have hnr' := ReachNoRemove.identify hnr hp hq hpq h1 h2
        obtain ⟨hb1, hb2, hb3⟩ := hnr'.obstruction_persists hs huv₀
        exact ⟨merge p q u, merge p q v, hnr', hb1, hb2, hb3⟩
    · right
      exact ⟨m, k + 1, mid, u, v, by omega, hnr, hmem, Reach.step htail st⟩

end Seed.Second
