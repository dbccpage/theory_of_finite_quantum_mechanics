/- Imported so that this repository carries its own Lean evidence.
   Original sha256: b90693440dd9596e12bdd2eeb424bb4d3709bca64b7e2a560e553432cf36b092 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.SnMssn.Paper001
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
Finite proofs for WDP Paper 001.
Mathlib-free. Each theorem is one ledger row still marked proved,
or one negative boundary named in the manuscript.
-/

def removeAll (W D : List Nat) : List Nat :=
  D.foldl (fun acc a => acc.erase a) W

theorem removeAll_nil (W : List Nat) : removeAll W [] = W := rfl

theorem removeAll_cons (W : List Nat) (a : Nat) (D : List Nat) :
    removeAll W (a :: D) = removeAll (W.erase a) D := rfl

theorem length_pos_of_mem {a : Nat} {W : List Nat} (h : a ∈ W) : 0 < W.length := by
  cases W with
  | nil => cases h
  | cons _ _ => simp

theorem add_one_le_of_le_sub (n m : Nat) (h : n ≤ m - 1) (hm : 1 ≤ m) : n + 1 ≤ m := by
  have hstep : n + 1 ≤ m - 1 + 1 := Nat.add_le_add_right h 1
  rwa [Nat.sub_add_cancel hm] at hstep

theorem pred_sub_eq (n k : Nat) : (n - 1) - k = n - (k + 1) := by
  calc
    (n - 1) - k = n - (1 + k) := by simpa using (Nat.sub_sub n 1 k)
    _ = n - (k + 1) := by rw [Nat.add_comm]

theorem nodup_subset_length (D W : List Nat) (hD : D.Nodup)
    (hsub : ∀ a, a ∈ D → a ∈ W) : D.length ≤ W.length := by
  induction D generalizing W with
  | nil => simp
  | cons a ds ih =>
    rcases List.nodup_cons.mp hD with ⟨haD, hds⟩
    have ha : a ∈ W := hsub a (by simp)
    have hsub' : ∀ x, x ∈ ds → x ∈ W.erase a := by
      intro x hx
      have hxW : x ∈ W := hsub x (by simp [hx])
      have hne : x ≠ a := by
        intro hxa
        apply haD
        simpa [hxa] using hx
      exact (List.mem_erase_of_ne hne).mpr hxW
    have hlenD := ih (W.erase a) hds hsub'
    have herase : (W.erase a).length = W.length - 1 := by
      rw [List.length_erase]
      simp [ha]
    have hpos : 1 ≤ W.length := by
      have := length_pos_of_mem ha
      omega
    have hle : ds.length ≤ W.length - 1 := by simpa [herase] using hlenD
    have hstep := add_one_le_of_le_sub ds.length W.length hle hpos
    simpa [List.length] using hstep

theorem removeAll_nodup (W D : List Nat) (hW : W.Nodup) : (removeAll W D).Nodup := by
  induction D generalizing W with
  | nil => simpa [removeAll_nil] using hW
  | cons a ds ih =>
    rw [removeAll_cons]
    exact ih (W.erase a) (List.Nodup.erase a hW)

theorem removeAll_length (W D : List Nat) (hW : W.Nodup) (hD : D.Nodup)
    (hsub : ∀ a, a ∈ D → a ∈ W) :
    (removeAll W D).length = W.length - D.length := by
  induction D generalizing W with
  | nil =>
    simp [removeAll_nil]
  | cons a ds ih =>
    rcases List.nodup_cons.mp hD with ⟨haD, hds⟩
    have ha : a ∈ W := hsub a (by simp)
    have hsub' : ∀ x, x ∈ ds → x ∈ W.erase a := by
      intro x hx
      have hxW : x ∈ W := hsub x (by simp [hx])
      have hne : x ≠ a := by
        intro hxa
        apply haD
        simpa [hxa] using hx
      exact (List.mem_erase_of_ne hne).mpr hxW
    have hlen1 : (W.erase a).length = W.length - 1 := by
      rw [List.length_erase]
      simp [ha]
    have hrec := ih (W.erase a) (List.Nodup.erase a hW) hds hsub'
    rw [removeAll_cons, hrec, hlen1, List.length]
    exact pred_sub_eq W.length ds.length

theorem demand_accounting (W D B : List Nat) (hW : W.Nodup) (hD : D.Nodup) (hB : B.Nodup)
    (hsub : ∀ a, a ∈ D → a ∈ W)
    (hdisj : ∀ a, a ∈ removeAll W D → ∀ b, b ∈ B → a ≠ b) :
    ((removeAll W D) ++ B).length = W.length - D.length + B.length ∧
      ((removeAll W D) ++ B).Nodup := by
  refine ⟨?_, ?_⟩
  · rw [List.length_append, removeAll_length W D hW hD hsub]
  · rw [List.nodup_append]
    exact ⟨removeAll_nodup W D hW, hB, hdisj⟩

theorem supplied_tag_separates {A O : Type} (q : A → O) (t : A → Fin 2)
    (a b : A) (ht : t a ≠ t b) :
    (q a, t a) ≠ (q b, t b) ∧ (q a, t a).1 = q a ∧ (q b, t b).1 = q b := by
  refine ⟨?_, rfl, rfl⟩
  intro h
  exact ht (congrArg Prod.snd h)

theorem old_image_injective {A B : Type} (u : A → B) (r : B → Sum A Unit)
    (h : ∀ a, r (u a) = Sum.inl a) {a a' : A} (hu : u a = u a') : a = a' := by
  have h1 := h a
  have h2 := h a'
  rw [hu] at h1
  rw [h1] at h2
  injection h2

theorem off_image_not_implied :
    ∃ (u : Fin 1 → Fin 2) (r : Fin 2 → Sum (Fin 1) Unit),
      (∀ a, r (u a) = Sum.inl a) ∧ ∃ b : Fin 2, (∀ a, u a ≠ b) ∧ r b ≠ Sum.inr () := by
  let u : Fin 1 → Fin 2 := fun _ => ⟨0, by decide⟩
  let r : Fin 2 → Sum (Fin 1) Unit := fun _ => Sum.inl ⟨0, by decide⟩
  refine ⟨u, r, ?_, ⟨⟨1, by decide⟩, ?_, ?_⟩⟩
  · intro a
    have ha : a = ⟨0, by decide⟩ := by
      apply Fin.ext
      have := a.isLt
      omega
    simp [u, r, ha]
  · intro a hneq
    have hval := congrArg Fin.val hneq
    simp [u] at hval
  · simp [r]

theorem observation_not_implied :
    ∃ (u : Fin 2 → Fin 2) (r : Fin 2 → Sum (Fin 2) Unit) (q q' : Fin 2 → Nat),
      (∀ a, r (u a) = Sum.inl a) ∧ ¬ (∀ a, q' (u a) = q a) := by
  refine ⟨id, fun a => Sum.inl a, fun _ => 0, fun a => a.val, ?_, ?_⟩
  · intro a
    rfl
  · intro h
    have := h ⟨1, by decide⟩
    simp at this

theorem repair_not_implied :
    ∃ (u : Fin 1 → Fin 1) (r : Fin 1 → Sum (Fin 1) Unit) (obstruction : Fin 1 → Bool),
      (∀ a, r (u a) = Sum.inl a) ∧
        obstruction ⟨0, by decide⟩ = true ∧
        obstruction (u ⟨0, by decide⟩) = true := by
  refine ⟨id, fun a => Sum.inl a, fun _ => true, ?_, rfl, rfl⟩
  intro a
  rfl

def Indecomposable {α : Type} (w : List α) : Prop :=
  w ≠ [] ∧ ∀ x y : List α, x ≠ [] → y ≠ [] → x ++ y ≠ w

theorem indecomposable_singleton {α : Type} (a : α) : Indecomposable [a] := by
  refine ⟨by simp, ?_⟩
  intro x y hx hy happ
  have hlen := congrArg List.length happ
  rw [List.length_append, List.length_singleton] at hlen
  cases x with
  | nil => exact hx rfl
  | cons _ xt =>
    cases y with
    | nil => exact hy rfl
    | cons _ _ =>
      simp [List.length] at hlen
      omega

theorem not_indecomposable_long {α : Type} {w : List α} (hw : 2 ≤ w.length) :
    ¬ Indecomposable w := by
  intro h
  match w with
  | [] => simp at hw
  | a :: t =>
    have ht : t ≠ [] := by
      intro ht
      simp [ht, List.length] at hw
    exact h.2 [a] t (by simp) ht (by simp)

theorem indecomposable_iff {α : Type} (w : List α) :
    Indecomposable w ↔ ∃ a, w = [a] := by
  constructor
  · intro h
    match w with
    | [] => exact absurd rfl h.1
    | a :: t =>
      match t with
      | [] => exact ⟨a, rfl⟩
      | b :: t =>
        exfalso
        have hwlen : 2 ≤ (a :: b :: t).length := by
          change 2 ≤ t.length + 1 + 1
          omega
        exact not_indecomposable_long hwlen h
  · rintro ⟨a, rfl⟩
    exact indecomposable_singleton a

structure MonoidIso (α β : Type) where
  toFun : List α → List β
  invFun : List β → List α
  map_nil : toFun [] = []
  map_append : ∀ x y, toFun (x ++ y) = toFun x ++ toFun y
  inv_nil : invFun [] = []
  inv_append : ∀ x y, invFun (x ++ y) = invFun x ++ invFun y
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

def MonoidIso.symm {α β : Type} (e : MonoidIso α β) : MonoidIso β α where
  toFun := e.invFun
  invFun := e.toFun
  map_nil := e.inv_nil
  map_append := e.inv_append
  inv_nil := e.map_nil
  inv_append := e.map_append
  left_inv := e.right_inv
  right_inv := e.left_inv

theorem iso_preserves_indecomp {α β : Type} (e : MonoidIso α β) {w : List α}
    (h : Indecomposable w) : Indecomposable (e.toFun w) := by
  refine ⟨?_, ?_⟩
  · intro hnil
    have := congrArg e.invFun hnil
    rw [e.left_inv, e.inv_nil] at this
    exact h.1 this
  · intro x y hx hy happ
    have hxy := congrArg e.invFun happ
    rw [e.inv_append, e.left_inv] at hxy
    have hx' : e.invFun x ≠ [] := by
      intro hz
      have := congrArg e.toFun hz
      rw [e.right_inv, e.map_nil] at this
      exact hx this
    have hy' : e.invFun y ≠ [] := by
      intro hz
      have := congrArg e.toFun hz
      rw [e.right_inv, e.map_nil] at this
      exact hy this
    exact h.2 _ _ hx' hy' hxy

theorem iso_letters {α β : Type} (e : MonoidIso α β) (a : α) :
    ∃ b : β, e.toFun [a] = [b] := by
  have h := iso_preserves_indecomp e (indecomposable_singleton a)
  rcases (indecomposable_iff _).mp h with ⟨b, hb⟩
  exact ⟨b, hb⟩

theorem singleton_inj {α : Type} {a b : α} (h : [a] = [b]) : a = b := by
  injection h

def punch {m : Nat} (k x : Fin (m + 1)) (hne : x ≠ k) : Fin m :=
  if h : x.val < k.val then
    ⟨x.val, by omega⟩
  else
    ⟨x.val - 1, by
      have hne' : x.val ≠ k.val := by
        intro hv
        exact hne (Fin.ext hv)
      have hxlt : x.val < m + 1 := x.isLt
      omega⟩

theorem punch_injective {m : Nat} (k x y : Fin (m + 1)) (hx : x ≠ k) (hy : y ≠ k)
    (h : punch k x hx = punch k y hy) : x = y := by
  by_cases hxlt : x.val < k.val <;> by_cases hylt : y.val < k.val
  · have hval := congrArg Fin.val h
    simp [punch, hxlt, hylt] at hval
    exact Fin.ext hval
  · have hval := congrArg Fin.val h
    simp [punch, hxlt, hylt] at hval
    have hne' : y.val ≠ k.val := by
      intro hv
      exact hy (Fin.ext hv)
    omega
  · have hval := congrArg Fin.val h
    simp [punch, hxlt, hylt] at hval
    have hne' : x.val ≠ k.val := by
      intro hv
      exact hx (Fin.ext hv)
    omega
  · have hval := congrArg Fin.val h
    simp [punch, hxlt, hylt] at hval
    have hne' : x.val ≠ k.val := by
      intro hv
      exact hx (Fin.ext hv)
    have hney : y.val ≠ k.val := by
      intro hv
      exact hy (Fin.ext hv)
    have : x.val = y.val := by omega
    exact Fin.ext this

theorem no_inj_fin_succ (n : Nat) :
    ¬ ∃ f : Fin (n + 1) → Fin n, ∀ x y, f x = f y → x = y := by
  induction n with
  | zero =>
    intro ⟨f, _⟩
    exact Fin.elim0 (f ⟨0, by omega⟩)
  | succ n ih =>
    intro ⟨f, hf⟩
    let last : Fin (n + 2) := ⟨n + 1, by omega⟩
    let k : Fin (n + 1) := f last
    let f' : Fin (n + 1) → Fin n := fun i =>
      punch k (f ⟨i.val, by omega⟩) (by
        intro h
        have heq := hf ⟨i.val, by omega⟩ last h
        have hval := congrArg Fin.val heq
        simp [last] at hval
        omega)
    have hf' : ∀ x y, f' x = f' y → x = y := by
      intro x y hxy
      have hxk : f ⟨x.val, by omega⟩ ≠ k := by
        intro h
        have heq := hf ⟨x.val, by omega⟩ last h
        have hval := congrArg Fin.val heq
        simp [last] at hval
        omega
      have hyk : f ⟨y.val, by omega⟩ ≠ k := by
        intro h
        have heq := hf ⟨y.val, by omega⟩ last h
        have hval := congrArg Fin.val heq
        simp [last] at hval
        omega
      have hpunch := punch_injective k (f ⟨x.val, by omega⟩) (f ⟨y.val, by omega⟩) hxk hyk hxy
      have heq := hf ⟨x.val, by omega⟩ ⟨y.val, by omega⟩ hpunch
      have hvals : x.val = y.val := by
        have := congrArg Fin.val heq
        simpa using this
      exact Fin.ext hvals
    exact ih ⟨f', hf'⟩

theorem inj_fin_le {n m : Nat} (f : Fin n → Fin m)
    (hf : ∀ x y, f x = f y → x = y) : n ≤ m := by
  if h : n ≤ m then
    exact h
  else
    have hlt : m < n := by omega
    let incl : Fin (m + 1) → Fin n := fun i => ⟨i.val, by omega⟩
    have hcomp : ∀ x y, f (incl x) = f (incl y) → x = y := by
      intro x y hxy
      have heq := hf (incl x) (incl y) hxy
      have hvals : x.val = y.val := by
        have := congrArg Fin.val heq
        simpa [incl] using this
      exact Fin.ext hvals
    exact False.elim (no_inj_fin_succ m ⟨fun x => f (incl x), hcomp⟩)

theorem fin_card_eq {n m : Nat} (f : Fin n → Fin m) (g : Fin m → Fin n)
    (hgf : ∀ x, g (f x) = x) (hfg : ∀ y, f (g y) = y) : n = m := by
  have hinj : ∀ x y, f x = f y → x = y := by
    intro x y h
    have := congrArg g h
    simpa [hgf x, hgf y] using this
  have hinj' : ∀ x y, g x = g y → x = y := by
    intro x y h
    have := congrArg f h
    simpa [hfg x, hfg y] using this
  have h1 := inj_fin_le f hinj
  have h2 := inj_fin_le g hinj'
  omega

theorem no_free_monoid_iso {n m : Nat} (h : n ≠ m) : MonoidIso (Fin n) (Fin m) → False := by
  intro e
  let f : Fin n → Fin m := fun a => (iso_letters e a).choose
  have hf : ∀ a, e.toFun [a] = [f a] := fun a => (iso_letters e a).choose_spec
  let g : Fin m → Fin n := fun b => (iso_letters e.symm b).choose
  have hg : ∀ b, e.invFun [b] = [g b] := fun b => (iso_letters e.symm b).choose_spec
  have hgf : ∀ a, g (f a) = a := by
    intro a
    have h1 : e.invFun (e.toFun [a]) = e.invFun [f a] := congrArg e.invFun (hf a)
    rw [e.left_inv] at h1
    rw [hg (f a)] at h1
    exact (singleton_inj h1).symm
  have hfg : ∀ b, f (g b) = b := by
    intro b
    have h1 : e.toFun (e.invFun [b]) = e.toFun [g b] := congrArg e.toFun (hg b)
    rw [e.right_inv] at h1
    rw [hf (g b)] at h1
    exact (singleton_inj h1).symm
  exact h (fin_card_eq f g hgf hfg)

structure DiscreteEquiv (n m : Nat) where
  toObj : Fin n → Fin m
  invObj : Fin m → Fin n
  left_inv : ∀ x, invObj (toObj x) = x
  right_inv : ∀ y, toObj (invObj y) = y

theorem no_discrete_equivalence {n m : Nat} (h : n ≠ m) : DiscreteEquiv n m → False := by
  intro e
  exact h (fin_card_eq e.toObj e.invObj e.left_inv e.right_inv)

theorem discrete_two_and_twenty_six_inequivalent : DiscreteEquiv 2 26 → False :=
  no_discrete_equivalence (by decide)

inductive ToyWord where
  | old
  | fresh
  deriving DecidableEq, Repr

def restrictSet (M : List ToyWord) : List ToyWord :=
  M.filter fun w => w == ToyWord.old

def refuseWord (w : List ToyWord) : Option (List ToyWord) :=
  if w.all (fun a => a == ToyWord.old) then some w else none

def eraseWord (w : List ToyWord) : List ToyWord :=
  w.filter fun a => a == ToyWord.old

theorem set_retraction_on_old_word :
    restrictSet [ToyWord.old] = [ToyWord.old] := by
  decide

theorem three_contracts_differ_on_a_new_letter :
    refuseWord [ToyWord.old, ToyWord.fresh] = none ∧
      eraseWord [ToyWord.old, ToyWord.fresh] = [ToyWord.old] ∧
      restrictSet [ToyWord.old, ToyWord.fresh] = [ToyWord.old] ∧
      refuseWord [ToyWord.old] = some [ToyWord.old] ∧
      eraseWord [ToyWord.old] = [ToyWord.old] := by
  decide

def joinsDistinct (edges : List (Fin 2 × Fin 2)) : Bool :=
  edges.any fun e => e.1 != e.2

def componentsOnTwo (edges : List (Fin 2 × Fin 2)) : Nat :=
  if joinsDistinct edges then 1 else 2

theorem empty_graph_two_components : componentsOnTwo [] = 2 := by
  decide

theorem loop_does_not_lower_component_count :
    componentsOnTwo [(⟨0, by decide⟩, ⟨0, by decide⟩)] = 2 := by
  decide

theorem connecting_edge_lowers_component_count :
    componentsOnTwo [(⟨0, by decide⟩, ⟨1, by decide⟩)] = 1 := by
  decide

theorem reduced_h0_of_nonempty (c : Nat) (hc : 0 < c) : c - 1 + 1 = c :=
  Nat.sub_add_cancel hc

theorem two_point_reduced_h0 : 2 - 1 = 1 := rfl

theorem list_any_false {α : Type} (p : α → Bool) (l : List α)
    (h : ∀ a, a ∈ l → p a = false) : l.any p = false := by
  induction l with
  | nil => rfl
  | cons a as ih =>
    rw [List.any_cons]
    rw [h a (by simp)]
    exact ih (fun a' ha' => h a' (List.mem_cons_of_mem a ha'))

theorem loops_do_not_lower (edges : List (Fin 2 × Fin 2))
    (h : ∀ e, e ∈ edges → e.1 = e.2) : componentsOnTwo edges = 2 := by
  unfold componentsOnTwo joinsDistinct
  have hany : edges.any (fun e => e.1 != e.2) = false :=
    list_any_false (fun e => e.1 != e.2) edges fun e he => by
      have heq : e.1 = e.2 := h e he
      rw [heq]
      simp [bne]
  simp [hany]

structure ChainRetraction (Cnext Cj Dnext Dj : Type) where
  boundaryC : Cnext → Cj
  boundaryD : Dnext → Dj
  embed : Cj → Dj
  retract : Dj → Cj
  retractUp : Dnext → Cnext
  sectionLaw : ∀ c, retract (embed c) = c
  retractChain : ∀ d, retract (boundaryD d) = boundaryC (retractUp d)

theorem homology_kernel_trivial {Cnext Cj Dnext Dj : Type}
    (X : ChainRetraction Cnext Cj Dnext Dj) (z : Cj) (b : Dnext)
    (hkilled : X.embed z = X.boundaryD b) :
    z = X.boundaryC (X.retractUp b) := by
  rw [← X.sectionLaw z, hkilled, X.retractChain]

theorem homology_injective_of_chain_retraction {Cnext Cj Cprev Dnext Dj : Type}
    (X : ChainRetraction Cnext Cj Dnext Dj) (cycleBoundary : Cj → Cprev) (zeroPrev : Cprev)
    (z : Cj) (b : Dnext) (hz : cycleBoundary z = zeroPrev)
    (hkilled : X.embed z = X.boundaryD b) :
    z = X.boundaryC (X.retractUp b) ∧ cycleBoundary z = zeroPrev :=
  ⟨homology_kernel_trivial X z b hkilled, hz⟩

def twoPointBoundary (k : Int) : Int × Int := (-k, k)

theorem two_point_retraction_impossible (r0 : Int × Int → Int × Int)
    (hfix : r0 (-1, 1) = (-1, 1)) (hchain : r0 (-1, 1) = (0, 0)) : False := by
  have h : (-1, 1) = ((0, 0) : Int × Int) := by rw [← hfix, hchain]
  have h1 := congrArg Prod.fst h
  omega

def triangleBoundary (x y w : Int) : Int × Int × Int := (-x + w, x - y, y - w)

theorem triangle_cycle_is_cycle : triangleBoundary 1 1 1 = (0, 0, 0) := by
  decide

theorem triangle_cycle_nonzero : ((1, 1, 1) : Int × Int × Int) ≠ (0, 0, 0) := by
  decide

theorem triangle_retraction_impossible {C2 : Type} (boundaryC : C2 → Int × Int × Int)
    (r1 : Int × Int × Int → Int × Int × Int) (r2 : Int → C2)
    (hsec : r1 (1, 1, 1) = (1, 1, 1))
    (hchain : r1 (1, 1, 1) = boundaryC (r2 1))
    (hzero : boundaryC (r2 1) = (0, 0, 0)) : False := by
  have h : ((1, 1, 1) : Int × Int × Int) = (0, 0, 0) := by
    rw [← hsec, hchain, hzero]
  exact triangle_cycle_nonzero h

def encodeCollapse (w : List Bool) : List Bool :=
  w.flatMap fun bit => if bit then [false, false] else [false]

theorem code_collapses_aa_and_b :
    encodeCollapse [false, false] = [false, false] ∧
      encodeCollapse [true] = [false, false] := by
  decide

def chshSelected (e00 e01 e10 e11 : Int) : Int := e00 + e01 + e10 - e11

def chshOther (e00 e01 e10 e11 : Int) : Int := e00 + e01 - e10 + e11

def assignProduct (a0 a1 b0 b1 : Int) : Int :=
  (a0 * b0) * (a0 * b1) * (a1 * b0) * (a1 * b1)

def pmSign (b : Bool) : Int := if b then 1 else -1

def allAssignments (check : Bool → Bool → Bool → Bool → Bool) : Bool :=
  [false, true].all fun a0 =>
    [false, true].all fun a1 =>
      [false, true].all fun b0 =>
        [false, true].all fun b1 => check a0 a1 b0 b1

theorem chsh_missed_orientation :
    chshSelected 1 1 (-1) 1 = 0 ∧
      chshOther 1 1 (-1) 1 = 4 ∧
      (1 * 1 * (-1) * 1 : Int) = -1 ∧
      allAssignments (fun a0 a1 b0 b1 =>
        assignProduct (pmSign a0) (pmSign a1) (pmSign b0) (pmSign b1) == 1) = true := by
  decide

theorem exists_descent_of_constant {X Y Z : Type} (q : X → Y) (f : X → Z)
    (h : ∀ x x', q x = q x' → f x = f x') :
    ∃ g : { y : Y // ∃ x, q x = y } → Z, ∀ x, g ⟨q x, ⟨x, rfl⟩⟩ = f x := by
  refine ⟨fun ys => f (Classical.choose ys.2), ?_⟩
  intro x
  apply h
  have hspec :=
    Classical.choose_spec (show ∃ x', q x' = q x from ⟨x, rfl⟩)
  have hsamespec :
      Classical.choose (show ∃ x', q x' = q x from ⟨x, rfl⟩) =
        Classical.choose (⟨q x, ⟨x, rfl⟩⟩ : { y : Y // ∃ x', q x' = y }).2 := by
    rfl
  simpa [hsamespec] using hspec

theorem descent_unique {X Y Z : Type} (q : X → Y) (f : X → Z)
    (g₁ g₂ : { y : Y // ∃ x, q x = y } → Z)
    (h₁ : ∀ x, g₁ ⟨q x, ⟨x, rfl⟩⟩ = f x)
    (h₂ : ∀ x, g₂ ⟨q x, ⟨x, rfl⟩⟩ = f x)
    (y : { y : Y // ∃ x, q x = y }) : g₁ y = g₂ y := by
  rcases y with ⟨y, hy⟩
  rcases hy with ⟨x, hx⟩
  cases hx
  rw [h₁ x, h₂ x]
