






namespace HilbertWalk.HWKernel


structure StarRingPack (K : Type) where
  add : K → K → K
  mul : K → K → K
  neg : K → K
  zero : K
  one : K
  conj : K → K
  add_comm : ∀ a b : K, add a b = add b a
  add_assoc : ∀ a b c : K, add (add a b) c = add a (add b c)
  zero_add : ∀ a : K, add zero a = a
  add_neg : ∀ a : K, add a (neg a) = zero
  mul_comm : ∀ a b : K, mul a b = mul b a
  mul_assoc : ∀ a b c : K, mul (mul a b) c = mul a (mul b c)
  one_mul : ∀ a : K, mul one a = a
  mul_add : ∀ a b c : K, mul a (add b c) = add (mul a b) (mul a c)
  mul_zero : ∀ a : K, mul a zero = zero
  conj_add : ∀ a b : K, conj (add a b) = add (conj a) (conj b)
  conj_mul : ∀ a b : K, conj (mul a b) = mul (conj a) (conj b)
  conj_conj : ∀ a : K, conj (conj a) = a
  conj_zero : conj zero = zero
  conj_one : conj one = one

namespace StarRingPack

variable {K : Type} (P : StarRingPack K)

theorem add_zero (a : K) : P.add a P.zero = a := by
  rw [P.add_comm, P.zero_add]

theorem add_left_comm (a b c : K) :
    P.add a (P.add b c) = P.add b (P.add a c) := by
  rw [← P.add_assoc, P.add_comm a b, P.add_assoc]

theorem mul_one (a : K) : P.mul a P.one = a := by
  rw [P.mul_comm, P.one_mul]

theorem zero_mul (a : K) : P.mul P.zero a = P.zero := by
  rw [P.mul_comm, P.mul_zero]

theorem add_mul (a b c : K) :
    P.mul (P.add a b) c = P.add (P.mul a c) (P.mul b c) := by
  rw [P.mul_comm, P.mul_add, P.mul_comm c a, P.mul_comm c b]

end StarRingPack


structure Enum (X : Type) where
  elems : List X
  complete : ∀ x : X, x ∈ elems
  nodup : elems.Nodup


def rsum {K : Type} (P : StarRingPack K) : List K → K
  | [] => P.zero
  | a :: t => P.add a (rsum P t)

theorem rsum_nil {K : Type} (P : StarRingPack K) : rsum P [] = P.zero :=
  rfl

theorem rsum_cons {K : Type} (P : StarRingPack K) (a : K) (t : List K) :
    rsum P (a :: t) = P.add a (rsum P t) :=
  rfl

theorem rsum_perm {K : Type} (P : StarRingPack K) {l₁ l₂ : List K}
    (h : l₁.Perm l₂) : rsum P l₁ = rsum P l₂ := by
  induction h with
  | nil => rfl
  | cons x _ ih => simp only [rsum]; rw [ih]
  | swap x y l =>
      simp only [rsum]
      rw [← P.add_assoc, ← P.add_assoc, P.add_comm y x]
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

theorem rsum_map_add {K X : Type} (P : StarRingPack K)
    (f g : X → K) (l : List X) :
    rsum P (l.map (fun x => P.add (f x) (g x))) =
      P.add (rsum P (l.map f)) (rsum P (l.map g)) := by
  induction l with
  | nil => simp only [List.map_nil, rsum, P.zero_add]
  | cons a t ih =>
      simp only [List.map_cons, rsum]
      rw [ih, P.add_assoc, P.add_assoc,
        P.add_left_comm (g a) (rsum P (t.map f)) (rsum P (t.map g))]

theorem rsum_map_mul_left {K X : Type} (P : StarRingPack K)
    (c : K) (f : X → K) (l : List X) :
    rsum P (l.map (fun x => P.mul c (f x))) =
      P.mul c (rsum P (l.map f)) := by
  induction l with
  | nil => simp only [List.map_nil, rsum, P.mul_zero]
  | cons a t ih =>
      simp only [List.map_cons, rsum]
      rw [ih, P.mul_add]


theorem nodup_map_of_injective {X Y : Type} {f : X → Y}
    (hinj : ∀ a b : X, f a = f b → a = b) :
    ∀ {l : List X}, l.Nodup → (l.map f).Nodup := by
  intro l h
  unfold List.Nodup at *
  rw [List.pairwise_map]
  exact h.imp (fun hne heq => hne (hinj _ _ heq))

theorem nodup_not_mem_erase {X : Type} [DecidableEq X] {a : X} :
    ∀ {l : List X}, l.Nodup → a ∉ l.erase a := by
  intro l
  induction l with
  | nil => intro _ h; cases h
  | cons b t ih =>
      intro hnd hmem
      rcases List.nodup_cons.mp hnd with ⟨hbt, hnt⟩
      rw [List.erase_cons] at hmem
      by_cases hba : b = a
      · subst hba
        rw [if_pos (beq_self_eq_true b)] at hmem
        exact hbt hmem
      · rw [if_neg (fun h => hba (beq_iff_eq.mp h))] at hmem
        rcases List.mem_cons.mp hmem with rfl | hin
        · exact hba rfl
        · exact ih hnt hin

theorem nodup_erase {X : Type} [DecidableEq X] {a : X} :
    ∀ {l : List X}, l.Nodup → (l.erase a).Nodup := by
  intro l
  induction l with
  | nil => intro _; exact List.Pairwise.nil
  | cons b t ih =>
      intro hnd
      rcases List.nodup_cons.mp hnd with ⟨hbt, hnt⟩
      rw [List.erase_cons]
      by_cases hba : b = a
      · rw [if_pos (by rw [hba]; exact beq_self_eq_true a)]
        exact hnt
      · rw [if_neg (fun h => hba (beq_iff_eq.mp h))]
        exact List.nodup_cons.mpr
          ⟨fun h => hbt (List.mem_of_mem_erase h), ih hnt⟩

theorem mem_erase_of_ne_of_mem {X : Type} [DecidableEq X] {x a : X} :
    ∀ {l : List X}, x ≠ a → x ∈ l → x ∈ l.erase a := by
  intro l
  induction l with
  | nil => intro _ h; cases h
  | cons b t ih =>
      intro hxa hx
      rw [List.erase_cons]
      by_cases hba : b = a
      · subst hba
        rw [if_pos (beq_self_eq_true b)]
        rcases List.mem_cons.mp hx with rfl | hxt
        · exact absurd rfl hxa
        · exact hxt
      · rw [if_neg (fun h => hba (beq_iff_eq.mp h))]
        rcases List.mem_cons.mp hx with rfl | hxt
        · exact List.mem_cons_self
        · exact List.mem_cons_of_mem b (ih hxa hxt)

theorem rsum_map_erase {K X : Type} (P : StarRingPack K) [DecidableEq X]
    (f : X → K) :
    ∀ {l : List X} {a : X}, a ∈ l → l.Nodup →
      rsum P (l.map f) = P.add (f a) (rsum P ((l.erase a).map f)) := by
  intro l
  induction l with
  | nil => intro a ha; cases ha
  | cons b t ih =>
      intro a ha hnd
      rcases List.nodup_cons.mp hnd with ⟨hbt, hnt⟩
      rw [List.erase_cons]
      by_cases hba : b = a
      · subst hba
        rw [if_pos (beq_self_eq_true b)]
        rfl
      · rw [if_neg (fun h => hba (beq_iff_eq.mp h))]
        rcases List.mem_cons.mp ha with rfl | hat
        · exact absurd rfl hba
        · simp only [List.map_cons, rsum_cons]
          rw [ih hat hnt, P.add_left_comm]

theorem rsum_eq_of_nodup_mem_iff {K X : Type} (P : StarRingPack K)
    [DecidableEq X] (f : X → K) :
    ∀ {l₁ l₂ : List X}, l₁.Nodup → l₂.Nodup →
      (∀ x : X, x ∈ l₁ ↔ x ∈ l₂) →
      rsum P (l₁.map f) = rsum P (l₂.map f) := by
  intro l₁
  induction l₁ with
  | nil =>
      intro l₂ _ _ hm
      cases l₂ with
      | nil => rfl
      | cons c t => exact absurd ((hm c).mpr List.mem_cons_self) List.not_mem_nil
  | cons a t ih =>
      intro l₂ h₁ h₂ hm
      rcases List.nodup_cons.mp h₁ with ⟨hat, hnt⟩
      have ha2 : a ∈ l₂ := (hm a).mp List.mem_cons_self
      rw [List.map_cons, rsum_cons, rsum_map_erase P f ha2 h₂]
      have hmem : ∀ x : X, x ∈ t ↔ x ∈ l₂.erase a := by
        intro x
        constructor
        · intro hx
          have hxa : x ≠ a := fun h => hat (h ▸ hx)
          exact mem_erase_of_ne_of_mem hxa
            ((hm x).mp (List.mem_cons_of_mem a hx))
        · intro hx
          rcases List.mem_cons.mp ((hm x).mpr (List.mem_of_mem_erase hx))
            with rfl | hxt
          · exact absurd hx (nodup_not_mem_erase h₂)
          · exact hxt
      rw [ih hnt (nodup_erase h₂) hmem]

theorem rsum_reindex {K X : Type} (P : StarRingPack K) [DecidableEq X]
    (E : Enum X) {π σ : X → X}
    (hσπ : ∀ x, σ (π x) = x) (hπσ : ∀ x, π (σ x) = x) (f : X → K) :
    rsum P (E.elems.map (fun x => f (π x))) = rsum P (E.elems.map f) := by
  have h1 : E.elems.map (fun x => f (π x)) = (E.elems.map π).map f := by
    rw [List.map_map]
    rfl
  rw [h1]
  exact rsum_eq_of_nodup_mem_iff P f
    (nodup_map_of_injective
      (fun a b hab => by
        have h := congrArg σ hab
        rwa [hσπ, hσπ] at h)
      E.nodup)
    E.nodup
    (fun y => ⟨fun _ => E.complete y,
      fun _ => List.mem_map.mpr ⟨σ y, E.complete (σ y), hπσ y⟩⟩)


theorem rsum_map_zero {K X : Type} (P : StarRingPack K) (l : List X) :
    rsum P (l.map (fun _ => P.zero)) = P.zero := by
  induction l with
  | nil => rfl
  | cons a t ih =>
      simp only [List.map_cons, rsum_cons]
      rw [ih, P.zero_add]

theorem map_congr_mem {X Y : Type} {f g : X → Y} :
    ∀ {l : List X}, (∀ a ∈ l, f a = g a) → l.map f = l.map g := by
  intro l
  induction l with
  | nil => intro _; rfl
  | cons b t ih =>
      intro h
      simp only [List.map_cons]
      rw [h b List.mem_cons_self,
        ih (fun a ha => h a (List.mem_cons_of_mem b ha))]

theorem filter_congr_mem {X : Type} {p q : X → Bool} :
    ∀ {l : List X}, (∀ a ∈ l, p a = q a) → l.filter p = l.filter q := by
  intro l
  induction l with
  | nil => intro _; rfl
  | cons b t ih =>
      intro h
      rw [List.filter_cons, List.filter_cons,
        h b List.mem_cons_self,
        ih (fun a ha => h a (List.mem_cons_of_mem b ha))]

theorem filter_none {X : Type} {p : X → Bool} :
    ∀ {l : List X}, (∀ x ∈ l, ¬(p x = true)) → l.filter p = [] := by
  intro l
  induction l with
  | nil => intro _; rfl
  | cons b t ih =>
      intro h
      rw [List.filter_cons, if_neg (h b List.mem_cons_self)]
      exact ih (fun x hx => h x (List.mem_cons_of_mem b hx))

theorem map_if_of_not_mem {K Q : Type} [DecidableEq Q] {a : Q}
    (g f : Q → K) :
    ∀ {t : List Q}, a ∉ t →
      t.map (fun q => if (a == q) = true then g q else f q) = t.map f := by
  intro t
  induction t with
  | nil => intro _; rfl
  | cons b s ih =>
      intro hnt
      have hab : ¬((a == b) = true) := by
        intro h
        exact hnt (by rw [beq_iff_eq.mp h]; exact List.mem_cons_self)
      simp only [List.map_cons]
      rw [if_neg hab, ih (fun h => hnt (List.mem_cons_of_mem b h))]

theorem rsum_map_if_single {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (c : K) (f : Q → K) :
    ∀ {l : List Q} {a : Q}, a ∈ l → l.Nodup →
      rsum P (l.map (fun q =>
        if (a == q) = true then P.add c (f q) else f q)) =
      P.add c (rsum P (l.map f)) := by
  intro l
  induction l with
  | nil => intro a ha; cases ha
  | cons b t ih =>
      intro a ha hnd
      rcases List.nodup_cons.mp hnd with ⟨hbt, hnt⟩
      simp only [List.map_cons, rsum_cons]
      by_cases hab : a = b
      · subst hab
        rw [if_pos (beq_self_eq_true a),
          map_if_of_not_mem (fun q => P.add c (f q)) f hbt, P.add_assoc]
      · rw [if_neg (fun h => hab (beq_iff_eq.mp h))]
        rcases List.mem_cons.mp ha with rfl | hat
        · exact absurd rfl hab
        · rw [ih hat hnt, P.add_left_comm]

theorem rsum_fiber_partition {K X Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (EQ : Enum Q) (τ : X → Q) (w : X → K) :
    ∀ l : List X,
      rsum P (EQ.elems.map (fun q =>
        rsum P ((l.filter (fun x => τ x == q)).map w))) =
      rsum P (l.map w) := by
  intro l
  induction l with
  | nil =>
      have h : EQ.elems.map (fun q =>
          rsum P ((List.filter (fun x => τ x == q) []).map w)) =
          EQ.elems.map (fun _ => P.zero) :=
        map_congr_mem (fun _ _ => rfl)
      rw [h, rsum_map_zero]
      rfl
  | cons x t ih =>
      have hstep : EQ.elems.map (fun q =>
          rsum P (((x :: t).filter (fun y => τ y == q)).map w)) =
          EQ.elems.map (fun q =>
            if (τ x == q) = true
            then P.add (w x)
              (rsum P ((t.filter (fun y => τ y == q)).map w))
            else rsum P ((t.filter (fun y => τ y == q)).map w)) := by
        apply map_congr_mem
        intro q _
        rw [List.filter_cons]
        by_cases h : (τ x == q) = true
        · rw [if_pos h, if_pos h]
          rfl
        · rw [if_neg h, if_neg h]
      rw [hstep,
        rsum_map_if_single P (w x)
          (fun q => rsum P ((t.filter (fun y => τ y == q)).map w))
          (EQ.complete (τ x)) EQ.nodup,
        ih]
      rfl

theorem rsum_map_delta {K Q : Type} (P : StarRingPack K) [DecidableEq Q]
    (c : K) {l : List Q} {a : Q} (ha : a ∈ l) (hnd : l.Nodup) :
    rsum P (l.map (fun q => if (a == q) = true then c else P.zero)) = c := by
  have h : l.map (fun q => if (a == q) = true then c else P.zero) =
      l.map (fun q =>
        if (a == q) = true then P.add c P.zero else P.zero) :=
    map_congr_mem (fun q _ => by
      by_cases hq : (a == q) = true
      · rw [if_pos hq, if_pos hq, P.add_zero]
      · rw [if_neg hq, if_neg hq])
  rw [h, rsum_map_if_single P c (fun _ => P.zero) ha hnd,
    rsum_map_zero, P.add_zero]

theorem rsum_filter_key {K X : Type} (P : StarRingPack K)
    [DecidableEq X] (w : X → K) :
    ∀ {l : List X} {a : X}, a ∈ l → l.Nodup →
      rsum P ((l.filter (fun x => x == a)).map w) = P.add (w a) P.zero := by
  intro l
  induction l with
  | nil => intro a ha; cases ha
  | cons b t ih =>
      intro a ha hnd
      rcases List.nodup_cons.mp hnd with ⟨hbt, hnt⟩
      rw [List.filter_cons]
      by_cases hba : b = a
      · subst hba
        rw [if_pos (beq_self_eq_true b),
          filter_none (fun x hx h => hbt (by rw [← beq_iff_eq.mp h]; exact hx))]
        rfl
      · rw [if_neg (fun h => hba (beq_iff_eq.mp h))]
        rcases List.mem_cons.mp ha with rfl | hat
        · exact absurd rfl hba
        · exact ih hat hnt


def intPack : StarRingPack Int where
  add := (· + ·)
  mul := (· * ·)
  neg := (- ·)
  zero := 0
  one := 1
  conj := id
  add_comm := Int.add_comm
  add_assoc := Int.add_assoc
  zero_add := Int.zero_add
  add_neg := Int.add_right_neg
  mul_comm := Int.mul_comm
  mul_assoc := Int.mul_assoc
  one_mul := Int.one_mul
  mul_add := Int.mul_add
  mul_zero := Int.mul_zero
  conj_add := fun _ _ => rfl
  conj_mul := fun _ _ => rfl
  conj_conj := fun _ => rfl
  conj_zero := rfl
  conj_one := rfl


def ratPack : StarRingPack Rat where
  add := (· + ·)
  mul := (· * ·)
  neg := (- ·)
  zero := 0
  one := 1
  conj := id
  add_comm := Rat.add_comm
  add_assoc := Rat.add_assoc
  zero_add := Rat.zero_add
  add_neg := Rat.add_neg_cancel
  mul_comm := Rat.mul_comm
  mul_assoc := Rat.mul_assoc
  one_mul := Rat.one_mul
  mul_add := Rat.mul_add
  mul_zero := Rat.mul_zero
  conj_add := fun _ _ => rfl
  conj_mul := fun _ _ => rfl
  conj_conj := fun _ => rfl
  conj_zero := rfl
  conj_one := rfl


structure GaussInt where
  re : Int
  im : Int
deriving DecidableEq, Repr

namespace GaussInt

def gadd (x y : GaussInt) : GaussInt :=
  ⟨x.re + y.re, x.im + y.im⟩

def gmul (x y : GaussInt) : GaussInt :=
  ⟨x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re⟩

def gneg (x : GaussInt) : GaussInt :=
  ⟨-x.re, -x.im⟩

def gconj (x : GaussInt) : GaussInt :=
  ⟨x.re, -x.im⟩

def gzero : GaussInt := ⟨0, 0⟩

def gone : GaussInt := ⟨1, 0⟩

def gi : GaussInt := ⟨0, 1⟩

theorem gi_sq : gmul gi gi = gneg gone := by decide

theorem gadd_comm (a b : GaussInt) : gadd a b = gadd b a := by
  cases a; cases b
  simp [gadd, Int.add_comm]

theorem gadd_assoc (a b c : GaussInt) :
    gadd (gadd a b) c = gadd a (gadd b c) := by
  cases a; cases b; cases c
  simp [gadd, Int.add_assoc]

theorem gzero_add (a : GaussInt) : gadd gzero a = a := by
  cases a
  simp [gadd, gzero]

theorem gadd_neg (a : GaussInt) : gadd a (gneg a) = gzero := by
  cases a
  simp [gadd, gneg, gzero, Int.add_right_neg]

theorem gmul_comm (a b : GaussInt) : gmul a b = gmul b a := by
  cases a; cases b
  simp [gmul, Int.mul_comm, Int.add_comm]

theorem gmul_assoc (a b c : GaussInt) :
    gmul (gmul a b) c = gmul a (gmul b c) := by
  cases a; cases b; cases c
  simp [gmul, Int.sub_eq_add_neg, Int.neg_mul, Int.mul_neg,
    Int.neg_add, Int.neg_neg, Int.mul_add, Int.add_mul,
    Int.mul_assoc, Int.mul_comm, Int.mul_left_comm,
    Int.add_assoc, Int.add_comm, Int.add_left_comm]

theorem gone_mul (a : GaussInt) : gmul gone a = a := by
  cases a
  simp [gmul, gone]

theorem gmul_gone (a : GaussInt) : gmul a gone = a := by
  cases a
  simp [gmul, gone]

theorem gmul_add (a b c : GaussInt) :
    gmul a (gadd b c) = gadd (gmul a b) (gmul a c) := by
  cases a; cases b; cases c
  simp [gmul, gadd, Int.mul_add, Int.sub_eq_add_neg, Int.neg_add,
    Int.add_assoc, Int.add_comm, Int.add_left_comm]

theorem gmul_zero (a : GaussInt) : gmul a gzero = gzero := by
  cases a
  simp [gmul, gzero]

theorem gconj_add (a b : GaussInt) :
    gconj (gadd a b) = gadd (gconj a) (gconj b) := by
  cases a; cases b
  simp [gconj, gadd, Int.neg_add]

theorem gconj_mul (a b : GaussInt) :
    gconj (gmul a b) = gmul (gconj a) (gconj b) := by
  cases a; cases b
  simp [gconj, gmul, Int.sub_eq_add_neg, Int.neg_add, Int.neg_mul,
    Int.mul_neg, Int.neg_neg]

theorem gconj_conj (a : GaussInt) : gconj (gconj a) = a := by
  cases a
  simp [gconj]

theorem gconj_gi_mul (a b : GaussInt) :
    gmul (gconj (gmul gi a)) (gmul gi b) = gmul (gconj a) b := by
  cases a with
  | mk ar ai =>
      cases b with
      | mk br bi =>
          simp only [gmul, gconj, gi, Int.neg_mul, Int.mul_neg,
            Int.neg_neg, Int.sub_eq_add_neg, Int.neg_add,
            Int.zero_mul, Int.mul_zero, Int.zero_add, Int.add_zero,
            Int.mul_comm, Int.one_mul, Int.mul_one, mk.injEq]
          exact ⟨Int.add_comm _ _, Int.add_comm _ _⟩

end GaussInt

def gaussPack : StarRingPack GaussInt where
  add := GaussInt.gadd
  mul := GaussInt.gmul
  neg := GaussInt.gneg
  zero := GaussInt.gzero
  one := GaussInt.gone
  conj := GaussInt.gconj
  add_comm := GaussInt.gadd_comm
  add_assoc := GaussInt.gadd_assoc
  zero_add := GaussInt.gzero_add
  add_neg := GaussInt.gadd_neg
  mul_comm := GaussInt.gmul_comm
  mul_assoc := GaussInt.gmul_assoc
  one_mul := GaussInt.gone_mul
  mul_add := GaussInt.gmul_add
  mul_zero := GaussInt.gmul_zero
  conj_add := GaussInt.gconj_add
  conj_mul := GaussInt.gconj_mul
  conj_conj := GaussInt.gconj_conj
  conj_zero := by decide
  conj_one := by decide

def f2Pack : StarRingPack Bool where
  add := xor
  mul := and
  neg := id
  zero := false
  one := true
  conj := id
  add_comm := by decide
  add_assoc := by decide
  zero_add := by decide
  add_neg := by decide
  mul_comm := by decide
  mul_assoc := by decide
  one_mul := by decide
  mul_add := by decide
  mul_zero := by decide
  conj_add := fun _ _ => rfl
  conj_mul := fun _ _ => rfl
  conj_conj := fun _ => rfl
  conj_zero := rfl
  conj_one := rfl


def enumBool : Enum Bool where
  elems := [false, true]
  complete := fun x => by
    cases x
    · exact List.mem_cons_self
    · exact List.mem_cons_of_mem false List.mem_cons_self
  nodup := by decide

def enumBoolProd : Enum (Bool × Bool) where
  elems := [(false, false), (false, true), (true, false), (true, true)]
  complete := fun x => by
    rcases x with ⟨a, b⟩
    cases a <;> cases b
    · exact List.mem_cons_self
    · exact List.mem_cons_of_mem _ List.mem_cons_self
    · exact List.mem_cons_of_mem _
        (List.mem_cons_of_mem _ List.mem_cons_self)
    · exact List.mem_cons_of_mem _
        (List.mem_cons_of_mem _
          (List.mem_cons_of_mem _ List.mem_cons_self))
  nodup := by decide


theorem rsum_int_fixture : rsum intPack [1, 2, 3] = 6 := by decide

theorem f2_one_plus_one :
    f2Pack.add f2Pack.one f2Pack.one = f2Pack.zero := by decide

#print axioms rsum_reindex
#print axioms rsum_eq_of_nodup_mem_iff
#print axioms rsum_perm
#print axioms rsum_fiber_partition
#print axioms rsum_filter_key
#print axioms gaussPack
#print axioms f2Pack
#print axioms intPack
#print axioms rsum_int_fixture
#print axioms ratPack
#print axioms Rat.add_comm
#print axioms Rat.add_assoc
#print axioms Rat.zero_add
#print axioms Rat.add_neg_cancel
#print axioms Rat.mul_comm
#print axioms Rat.mul_assoc
#print axioms Rat.one_mul
#print axioms Rat.mul_add
#print axioms Rat.mul_zero

end HilbertWalk.HWKernel

private def l5aProvenance : String :=
  "Origin: lean4/HWKernel.lean Claim: add_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
