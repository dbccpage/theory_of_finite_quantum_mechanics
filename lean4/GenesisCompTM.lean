import GenesisComputation
import Mathlib.Computability.TuringMachine.PostTuringMachine

/-!
# Turing machines as rewriting regimes (C5)

AuthorityEffect: None.

A Mathlib `Turing.TM0` machine over a tape alphabet `Γ` and a state type `Λ` is encoded as a
semi-Thue system on configuration words
`lend · (left cells, far to near) · q · a · (right cells, near to far) · rend`
over the mark type `Sym Γ Λ` of tape symbols, state symbols and two end markers.  The rule
set `Rules M` has five rule shapes; the end rules supply a fresh blank mark exactly when the
head moves past the written part of the tape, which is the only place where words grow.

Headline statements (all kernel-checked, no unproved goals):

* `step_fwd`   one machine step is one rewrite step, on every representation;
* `step_bwd`   one rewrite step of a represented word is the machine step (so the rewriting is
  deterministic on represented words, and a halted configuration has no rewrite);
* `reaches_fwd`, `reach_bwd`  the same for the closures;
* `halts_iff`  the machine halts from `c` iff a represented word reaches an irreducible word;
* `runner_unbounded`  the right-running machine reaches words of every length, so no finite
  bound closes its regime (it needs an unbounded supply of fresh blanks);
* `card_sym`   the mark budget `|Γ| + |Λ| + 2`.

Mathlib's `Turing.TM0`, `Turing.Tape` and `ListBlank` are imported infrastructure.
-/

open Turing

namespace GenesisComputation
namespace TMEncoding

/-- Marks of the encoding: end markers, state marks and tape-symbol marks. -/
inductive Sym (Γ Λ : Type*)
  | lend
  | rend
  | st (q : Λ)
  | sym (a : Γ)
  deriving DecidableEq

variable {Γ Λ : Type*}

/-- The mark type is a finite sum: `Sym Γ Λ ≃ (Unit ⊕ Unit) ⊕ (Λ ⊕ Γ)`. -/
def Sym.equivSum : Sym Γ Λ ≃ (Unit ⊕ Unit) ⊕ (Λ ⊕ Γ) where
  toFun
    | .lend => .inl (.inl ())
    | .rend => .inl (.inr ())
    | .st q => .inr (.inl q)
    | .sym a => .inr (.inr a)
  invFun
    | .inl (.inl _) => .lend
    | .inl (.inr _) => .rend
    | .inr (.inl q) => .st q
    | .inr (.inr a) => .sym a
  left_inv x := by cases x <;> rfl
  right_inv x := by rcases x with (⟨⟩ | ⟨⟩) | (_ | _) <;> rfl

instance [Fintype Γ] [Fintype Λ] : Fintype (Sym Γ Λ) := Fintype.ofEquiv _ Sym.equivSum.symm

/-- The mark budget of a machine: `|Γ|` tape marks, `|Λ|` state marks, two end markers. -/
theorem card_sym [Fintype Γ] [Fintype Λ] :
    Fintype.card (Sym Γ Λ) = Fintype.card Γ + Fintype.card Λ + 2 := by
  rw [Fintype.card_congr Sym.equivSum]
  simp [Fintype.card_sum]
  omega

variable [Inhabited Γ] [Inhabited Λ]

/-- The word of a configuration with left cells `ul` (nearest first), state `q`, scanned
symbol `a` and right cells `ur` (nearest first). -/
def cfgWord (ul : List Γ) (q : Λ) (a : Γ) (ur : List Γ) : List (Sym Γ Λ) :=
  .lend :: (ul.reverse.map Sym.sym ++ (.st q :: .sym a :: (ur.map Sym.sym ++ [.rend])))

/-- `w` represents the configuration `c`: it is the configuration word for some lists
presenting the two blank-padded tape halves.  Extra blanks at the far ends are allowed. -/
def Rep (c : TM0.Cfg Γ Λ) (w : List (Sym Γ Λ)) : Prop :=
  ∃ ul ur : List Γ, c.Tape.left = ListBlank.mk ul ∧ c.Tape.right = ListBlank.mk ur ∧
    w = cfgWord ul c.q c.Tape.head ur

/-- The rewriting rules of a machine. -/
inductive Rules (M : TM0.Machine Γ Λ) : List (Sym Γ Λ) → List (Sym Γ Λ) → Prop
  | write {q a q' b} (h : M q a = some (q', TM0.Stmt.write b)) :
      Rules M [.st q, .sym a] [.st q', .sym b]
  | right {q a q' c} (h : M q a = some (q', TM0.Stmt.move Dir.right)) :
      Rules M [.st q, .sym a, .sym c] [.sym a, .st q', .sym c]
  | rightEnd {q a q'} (h : M q a = some (q', TM0.Stmt.move Dir.right)) :
      Rules M [.st q, .sym a, .rend] [.sym a, .st q', .sym default, .rend]
  | left {q a q' c} (h : M q a = some (q', TM0.Stmt.move Dir.left)) :
      Rules M [.sym c, .st q, .sym a] [.st q', .sym c, .sym a]
  | leftEnd {q a q'} (h : M q a = some (q', TM0.Stmt.move Dir.left)) :
      Rules M [.lend, .st q, .sym a] [.lend, .st q', .sym default, .sym a]

/-- A list contains no state mark. -/
def NoSt (l : List (Sym Γ Λ)) : Prop := ∀ x ∈ l, ∀ q, x ≠ Sym.st q

theorem noSt_map_sym (l : List Γ) : NoSt (l.map (Sym.sym : Γ → Sym Γ Λ)) := by
  intro x hx q
  obtain ⟨a, _, rfl⟩ := List.mem_map.1 hx
  simp

theorem NoSt.cons_iff {x : Sym Γ Λ} {l : List (Sym Γ Λ)} :
    NoSt (x :: l) ↔ (∀ q, x ≠ Sym.st q) ∧ NoSt l := by
  constructor
  · intro h; exact ⟨h x (by simp), fun y hy => h y (by simp [hy])⟩
  · rintro ⟨h1, h2⟩ y hy q
    rcases List.mem_cons.1 hy with rfl | hy
    · exact h1 q
    · exact h2 y hy q

theorem NoSt.append {l l' : List (Sym Γ Λ)} (h : NoSt l) (h' : NoSt l') : NoSt (l ++ l') := by
  intro x hx q
  rcases List.mem_append.1 hx with hx | hx
  · exact h x hx q
  · exact h' x hx q

/-- The state mark is located uniquely in a word with exactly one. -/
theorem split_st {A B P S : List (Sym Γ Λ)} {q0 q : Λ} (hP : NoSt P) (hS : NoSt S)
    (h : A ++ Sym.st q0 :: B = P ++ Sym.st q :: S) : A = P ∧ q0 = q ∧ B = S := by
  induction A generalizing P with
  | nil =>
      cases P with
      | nil => simp at h; exact ⟨rfl, h.1, h.2⟩
      | cons x P' =>
          simp only [List.nil_append, List.cons_append, List.cons.injEq] at h
          exact absurd h.1.symm (((NoSt.cons_iff.1 hP).1) q0)
  | cons a A ih =>
      cases P with
      | nil =>
          simp only [List.cons_append, List.nil_append, List.cons.injEq] at h
          obtain ⟨rfl, h2⟩ := h
          exact absurd (by rw [← h2]; simp) (fun hm => hS _ hm q0 rfl)
      | cons x P' =>
          simp only [List.cons_append, List.cons.injEq] at h
          obtain ⟨rfl, h2⟩ := h
          obtain ⟨h3, h4, h5⟩ := ih (NoSt.cons_iff.1 hP).2 h2
          exact ⟨by rw [h3], h4, h5⟩

theorem noSt_prefix (ul : List Γ) : NoSt (Sym.lend :: ul.reverse.map (Sym.sym : Γ → Sym Γ Λ)) := by
  rw [NoSt.cons_iff]
  exact ⟨fun q => by simp, noSt_map_sym _⟩

theorem noSt_suffix (ur : List Γ) (a : Γ) :
    NoSt (Sym.sym a :: (ur.map (Sym.sym : Γ → Sym Γ Λ) ++ [Sym.rend])) := by
  rw [NoSt.cons_iff]
  refine ⟨fun q => by simp, (noSt_map_sym _).append ?_⟩
  intro x hx q
  simp at hx
  subst hx
  simp

theorem cfgWord_eq (ul : List Γ) (q : Λ) (a : Γ) (ur : List Γ) :
    cfgWord ul q a ur =
      (Sym.lend :: ul.reverse.map Sym.sym) ++ Sym.st q :: (Sym.sym a :: (ur.map Sym.sym ++ [Sym.rend])) := by
  simp [cfgWord]

/-- Every configuration has a representing word. -/
theorem rep_exists (c : TM0.Cfg Γ Λ) : ∃ w, Rep c w := by
  obtain ⟨ul, hl⟩ := Quotient.exists_rep c.Tape.left
  obtain ⟨ur, hr⟩ := Quotient.exists_rep c.Tape.right
  exact ⟨_, ul, ur, hl.symm, hr.symm, rfl⟩

/-- A word represents at most one configuration (the decoding is unique). -/
theorem rep_unique {c c' : TM0.Cfg Γ Λ} {w : List (Sym Γ Λ)} (h : Rep c w) (h' : Rep c' w) :
    c = c' := by
  obtain ⟨q, ⟨a, L, R⟩⟩ := c
  obtain ⟨q', ⟨a', L', R'⟩⟩ := c'
  obtain ⟨ul, ur, hl, hr, hw⟩ := h
  obtain ⟨ul', ur', hl', hr', hw'⟩ := h'
  dsimp only at hl hr hw hl' hr' hw'
  rw [cfgWord_eq] at hw hw'
  have key := split_st (noSt_prefix ul') (noSt_suffix ur' a')
    (show (Sym.lend :: ul.reverse.map Sym.sym) ++ Sym.st q ::
        (Sym.sym a :: (ur.map Sym.sym ++ [Sym.rend])) =
      (Sym.lend :: ul'.reverse.map Sym.sym) ++ Sym.st q' ::
        (Sym.sym a' :: (ur'.map Sym.sym ++ [Sym.rend])) from hw.symm.trans hw')
  obtain ⟨h1, h2, h3⟩ := key
  simp only [List.cons.injEq, true_and] at h1 h3
  have hul : ul = ul' := by
    have := List.map_injective_iff.2 (fun x y (h : (Sym.sym x : Sym Γ Λ) = Sym.sym y) =>
      Sym.sym.inj h) h1
    simpa using this
  obtain ⟨h4, h5⟩ := h3
  have hur : ur = ur' := by
    have := List.append_cancel_right h5
    exact List.map_injective_iff.2 (fun x y (h : (Sym.sym x : Sym Γ Λ) = Sym.sym y) =>
      Sym.sym.inj h) this
  have h4' : a = a' := Sym.sym.inj h4
  subst h2; subst hul; subst hur; subst h4'
  subst hl hr hl' hr'
  rfl

/-! ### One machine step is one rewrite step -/

theorem step_write {M : TM0.Machine Γ Λ} {q a q' b} (h : M q a = some (q', TM0.Stmt.write b))
    (L R : ListBlank Γ) :
    TM0.step M ⟨q, ⟨a, L, R⟩⟩ = some ⟨q', ⟨b, L, R⟩⟩ := by
  simp [TM0.step, h, Tape.write]

theorem step_right {M : TM0.Machine Γ Λ} {q a q'} (h : M q a = some (q', TM0.Stmt.move Dir.right))
    (L R : ListBlank Γ) :
    TM0.step M ⟨q, ⟨a, L, R⟩⟩ = some ⟨q', ⟨R.head, L.cons a, R.tail⟩⟩ := by
  simp [TM0.step, h, Tape.move]

theorem step_left {M : TM0.Machine Γ Λ} {q a q'} (h : M q a = some (q', TM0.Stmt.move Dir.left))
    (L R : ListBlank Γ) :
    TM0.step M ⟨q, ⟨a, L, R⟩⟩ = some ⟨q', ⟨L.head, L.tail, R.cons a⟩⟩ := by
  simp [TM0.step, h, Tape.move]

/-- Forward simulation: a machine step is matched by a rewrite step, from every word that
represents the configuration, landing on a word that represents the next configuration. -/
theorem step_fwd {M : TM0.Machine Γ Λ} {c c' : TM0.Cfg Γ Λ} {w : List (Sym Γ Λ)}
    (hs : TM0.step M c = some c') (hr : Rep c w) :
    ∃ w', Rep c' w' ∧ Step (Rules M) w w' := by
  obtain ⟨q, ⟨a, L, R⟩⟩ := c
  obtain ⟨ul, ur, hL, hR, hw⟩ := hr
  dsimp only at hL hR hw
  subst hL hR hw
  rcases hM : M q a with _ | ⟨q', st⟩
  · simp [TM0.step, hM] at hs
  · cases st with
    | write b =>
        rw [step_write hM] at hs
        cases hs
        refine ⟨cfgWord ul q' b ur, ⟨ul, ur, rfl, rfl, rfl⟩, ?_⟩
        exact ⟨_, _, Sym.lend :: ul.reverse.map Sym.sym, ur.map Sym.sym ++ [Sym.rend],
          Rules.write hM, by simp [cfgWord], by simp [cfgWord]⟩
    | move d =>
        cases d with
        | right =>
            rw [step_right hM] at hs
            cases hs
            cases ur with
            | nil =>
                refine ⟨cfgWord (a :: ul) q' default [], ⟨a :: ul, [], ?_, ?_, ?_⟩, ?_⟩
                · simp [ListBlank.cons_mk]
                · simp
                · simp [ListBlank.head_mk]
                · exact ⟨_, _, Sym.lend :: ul.reverse.map Sym.sym, [],
                    Rules.rightEnd hM, by simp [cfgWord], by simp [cfgWord]⟩
            | cons c ur' =>
                refine ⟨cfgWord (a :: ul) q' c ur', ⟨a :: ul, ur', ?_, ?_, ?_⟩, ?_⟩
                · simp [ListBlank.cons_mk]
                · simp [ListBlank.tail_mk]
                · simp [ListBlank.head_mk]
                · exact ⟨_, _, Sym.lend :: ul.reverse.map Sym.sym,
                    ur'.map Sym.sym ++ [Sym.rend], Rules.right (c := c) hM,
                    by simp [cfgWord], by simp [cfgWord]⟩
        | left =>
            rw [step_left hM] at hs
            cases hs
            cases ul with
            | nil =>
                refine ⟨cfgWord [] q' default (a :: ur), ⟨[], a :: ur, ?_, ?_, ?_⟩, ?_⟩
                · simp [ListBlank.tail_mk]
                · simp [ListBlank.cons_mk]
                · simp [ListBlank.head_mk]
                · exact ⟨_, _, [], ur.map Sym.sym ++ [Sym.rend], Rules.leftEnd hM,
                    by simp [cfgWord], by simp [cfgWord]⟩
            | cons c ul' =>
                refine ⟨cfgWord ul' q' c (a :: ur), ⟨ul', a :: ur, ?_, ?_, ?_⟩, ?_⟩
                · simp [ListBlank.tail_mk]
                · simp [ListBlank.cons_mk]
                · simp [ListBlank.head_mk]
                · exact ⟨_, _, Sym.lend :: ul'.reverse.map Sym.sym,
                    ur.map Sym.sym ++ [Sym.rend], Rules.left (c := c) hM,
                    by simp [cfgWord], by simp [cfgWord]⟩

/-- Backward simulation: every rewrite step of a represented word is the machine step. -/
theorem step_bwd {M : TM0.Machine Γ Λ} {c : TM0.Cfg Γ Λ} {w w' : List (Sym Γ Λ)}
    (hr : Rep c w) (hs : Step (Rules M) w w') :
    ∃ c', TM0.step M c = some c' ∧ Rep c' w' := by
  obtain ⟨q, ⟨a, L, R⟩⟩ := c
  obtain ⟨ul, ur, hL, hR, hw⟩ := hr
  dsimp only at hL hR hw
  subst hL hR
  obtain ⟨l, r, u, v, hrule, hwl, hwr⟩ := hs
  rw [cfgWord_eq] at hw
  subst hw
  cases hrule with
  | write hM =>
      rename_i q0 a0 q' b
      obtain ⟨h1, h2, h3⟩ := split_st (noSt_prefix ul) (noSt_suffix ur a)
        (show u ++ Sym.st q0 :: (Sym.sym a0 :: v) = _ by simpa using hwl.symm)
      subst h2
      simp only [List.cons.injEq, Sym.sym.injEq, true_and] at h3
      obtain ⟨rfl, rfl⟩ := h3
      refine ⟨_, step_write hM _ _, ul, ur, rfl, rfl, ?_⟩
      rw [hwr, h1]; simp [cfgWord]
  | right hM =>
      rename_i q0 a0 q' c0
      obtain ⟨h1, h2, h3⟩ := split_st (noSt_prefix ul) (noSt_suffix ur a)
        (show u ++ Sym.st q0 :: (Sym.sym a0 :: Sym.sym c0 :: v) = _ by simpa using hwl.symm)
      subst h2
      simp only [List.cons.injEq, Sym.sym.injEq, true_and] at h3
      obtain ⟨rfl, h3⟩ := h3
      cases ur with
      | nil => simp at h3
      | cons c' ur' =>
          simp only [List.map_cons, List.cons_append, List.cons.injEq, Sym.sym.injEq] at h3
          obtain ⟨rfl, rfl⟩ := h3
          refine ⟨_, step_right hM _ _, a0 :: ul, ur', ?_, ?_, ?_⟩
          · simp [ListBlank.cons_mk]
          · simp [ListBlank.tail_mk]
          · simp [ListBlank.head_mk]
            rw [hwr, h1]; simp [cfgWord]
  | rightEnd hM =>
      rename_i q0 a0 q'
      obtain ⟨h1, h2, h3⟩ := split_st (noSt_prefix ul) (noSt_suffix ur a)
        (show u ++ Sym.st q0 :: (Sym.sym a0 :: Sym.rend :: v) = _ by simpa using hwl.symm)
      subst h2
      simp only [List.cons.injEq, Sym.sym.injEq, true_and] at h3
      obtain ⟨rfl, h3⟩ := h3
      cases ur with
      | nil =>
          simp only [List.map_nil, List.nil_append, List.cons.injEq, true_and] at h3
          subst h3
          refine ⟨_, step_right hM _ _, a0 :: ul, [], ?_, ?_, ?_⟩
          · simp [ListBlank.cons_mk]
          · simp
          · simp [ListBlank.head_mk]
            rw [hwr, h1]; simp [cfgWord]
      | cons c' ur' => simp at h3
  | left hM =>
      rename_i q0 a0 q' c0
      have hwl' : (u ++ [Sym.sym c0]) ++ Sym.st q0 :: (Sym.sym a0 :: v) =
          (Sym.lend :: ul.reverse.map Sym.sym) ++ Sym.st q ::
            (Sym.sym a :: (ur.map Sym.sym ++ [Sym.rend])) := by simpa using hwl.symm
      obtain ⟨h1, h2, h3⟩ := split_st (noSt_prefix ul) (noSt_suffix ur a) hwl'
      subst h2
      simp only [List.cons.injEq, Sym.sym.injEq, true_and] at h3
      obtain ⟨rfl, rfl⟩ := h3
      cases ul with
      | nil =>
          have := congrArg List.getLast? h1
          simp at this
      | cons c' ul' =>
          have h1' : u ++ [Sym.sym c0] =
              (Sym.lend :: ul'.reverse.map Sym.sym) ++ [Sym.sym c'] := by
            simpa using h1
          obtain ⟨hu, hc⟩ := List.append_inj' h1' (by simp)
          have hc0 : c0 = c' := by simpa using hc
          subst hc0
          refine ⟨_, step_left hM _ _, ul', a0 :: ur, ?_, ?_, ?_⟩
          · simp [ListBlank.tail_mk]
          · simp [ListBlank.cons_mk]
          · simp [ListBlank.head_mk]
            rw [hwr, hu]; simp [cfgWord]
  | leftEnd hM =>
      rename_i q0 a0 q'
      have hwl' : (u ++ [Sym.lend]) ++ Sym.st q0 :: (Sym.sym a0 :: v) =
          (Sym.lend :: ul.reverse.map Sym.sym) ++ Sym.st q ::
            (Sym.sym a :: (ur.map Sym.sym ++ [Sym.rend])) := by simpa using hwl.symm
      obtain ⟨h1, h2, h3⟩ := split_st (noSt_prefix ul) (noSt_suffix ur a) hwl'
      subst h2
      simp only [List.cons.injEq, Sym.sym.injEq, true_and] at h3
      obtain ⟨rfl, rfl⟩ := h3
      cases hul : ul.reverse with
      | cons c' t =>
          rw [hul] at h1
          have hlen := congrArg List.length h1
          simp only [List.length_append, List.length_cons, List.length_map,
            List.length_singleton] at hlen
          cases u with
          | nil => simp at hlen
          | cons x u' =>
              simp only [List.cons_append, List.cons.injEq] at h1
              have hm : Sym.lend ∈ List.map (Sym.sym : Γ → Sym Γ Λ) (c' :: t) := by
                rw [← h1.2]; simp
              simp at hm
      | nil =>
          have hul' : ul = [] := List.reverse_eq_nil_iff.1 hul
          subst hul'
          simp only [List.reverse_nil, List.map_nil] at h1
          have hu : u = [] := by
            have := congrArg List.length h1
            simp at this
            exact this
          subst hu
          refine ⟨_, step_left hM _ _, [], a0 :: ur, ?_, ?_, ?_⟩
          · simp [ListBlank.tail_mk]
          · simp [ListBlank.cons_mk]
          · simp [ListBlank.head_mk]
            rw [hwr]; simp [cfgWord]

/-! ### Closures, halting, and the unbounded supply -/

/-- Forward simulation of sequences of steps. -/
theorem reaches_fwd {M : TM0.Machine Γ Λ} {c c' : TM0.Cfg Γ Λ} (h : TM0.Reaches M c c')
    {w : List (Sym Γ Λ)} (hr : Rep c w) : ∃ w', Rep c' w' ∧ Reach (Rules M) w w' := by
  induction h with
  | refl => exact ⟨w, hr, Relation.ReflTransGen.refl⟩
  | tail _ hs ih =>
      obtain ⟨w1, hr1, hR1⟩ := ih
      obtain ⟨w2, hr2, hs2⟩ := step_fwd hs hr1
      exact ⟨w2, hr2, hR1.tail hs2⟩

/-- Backward simulation of sequences of rewrite steps. -/
theorem reach_bwd {M : TM0.Machine Γ Λ} {c : TM0.Cfg Γ Λ} {w w' : List (Sym Γ Λ)}
    (hr : Rep c w) (h : Reach (Rules M) w w') : ∃ c', Rep c' w' ∧ TM0.Reaches M c c' := by
  induction h with
  | refl => exact ⟨c, hr, Relation.ReflTransGen.refl⟩
  | tail _ hs ih =>
      obtain ⟨c1, hr1, hR1⟩ := ih
      obtain ⟨c2, hstep, hr2⟩ := step_bwd hr1 hs
      exact ⟨c2, hr2, hR1.tail hstep⟩

/-- The machine halts from `c`: some reachable configuration has no transition. -/
def Halts (M : TM0.Machine Γ Λ) (c : TM0.Cfg Γ Λ) : Prop :=
  ∃ c', TM0.Reaches M c c' ∧ TM0.step M c' = none

/-- A word with no rewrite step. -/
def Irreducible (R : List (Sym Γ Λ) → List (Sym Γ Λ) → Prop) (w : List (Sym Γ Λ)) : Prop :=
  ∀ w', ¬ Step R w w'

/-- The halting of the machine is the reachability of an irreducible word. -/
theorem halts_iff {M : TM0.Machine Γ Λ} {c : TM0.Cfg Γ Λ} {w : List (Sym Γ Λ)}
    (hr : Rep c w) :
    Halts M c ↔ ∃ w', Reach (Rules M) w w' ∧ Irreducible (Rules M) w' := by
  constructor
  · rintro ⟨c', hc, hnone⟩
    obtain ⟨w', hr', hR⟩ := reaches_fwd hc hr
    refine ⟨w', hR, fun w'' hs => ?_⟩
    obtain ⟨c'', hstep, _⟩ := step_bwd hr' hs
    rw [hnone] at hstep
    cases hstep
  · rintro ⟨w', hR, hirr⟩
    obtain ⟨c', hr', hc⟩ := reach_bwd hr hR
    refine ⟨c', hc, ?_⟩
    rcases hs : TM0.step M c' with _ | c''
    · rfl
    · obtain ⟨w'', _, hstep⟩ := step_fwd hs hr'
      exact absurd hstep (hirr w'')

/-! ### The right-running machine needs unbounded blanks -/

/-- A machine on one state and the tape alphabet `Bool` that moves right forever. -/
def runner : TM0.Machine Bool Unit := fun _ _ => some ((), TM0.Stmt.move Dir.right)

/-- The configuration word of the runner after `n` steps from the blank tape. -/
def runnerWord (n : ℕ) : List (Sym Bool Unit) :=
  Sym.lend :: (List.replicate n (Sym.sym false) ++ [Sym.st (), Sym.sym false, Sym.rend])

theorem runnerWord_length (n : ℕ) : (runnerWord n).length = n + 4 := by
  simp [runnerWord]

theorem runner_step (n : ℕ) : Step (Rules runner) (runnerWord n) (runnerWord (n + 1)) := by
  refine ⟨[Sym.st (), Sym.sym false, Sym.rend],
    [Sym.sym false, Sym.st (), Sym.sym (default : Bool), Sym.rend],
    Sym.lend :: List.replicate n (Sym.sym false), [],
    Rules.rightEnd (q := ()) (a := false) (q' := ()) rfl, ?_, ?_⟩
  · simp [runnerWord]
  · simp [runnerWord, List.replicate_succ']

theorem runner_reach (n : ℕ) : Reach (Rules runner) (runnerWord 0) (runnerWord n) := by
  induction n with
  | zero => exact Relation.ReflTransGen.refl
  | succ n ih => exact ih.tail (runner_step n)

/-- Words of every length are reachable: no finite length bound closes the runner's regime, so
simulating it needs an unbounded supply of fresh blank marks. -/
theorem runner_unbounded (L : ℕ) :
    ∃ w, Reach (Rules runner) (runnerWord 0) w ∧ L < w.length :=
  ⟨runnerWord L, runner_reach L, by rw [runnerWord_length]; omega⟩

/-! ### A finite rule list for finite machines -/

section Finite

variable [Fintype Γ] [Fintype Λ] [DecidableEq Γ] [DecidableEq Λ]

/-- The rule list of a finite machine: one entry per transition shape. -/
noncomputable def ruleList (M : TM0.Machine Γ Λ) : RuleList (Sym Γ Λ) :=
  (Finset.univ : Finset Λ).toList.flatMap fun q =>
    (Finset.univ : Finset Γ).toList.flatMap fun a =>
      match M q a with
      | none => []
      | some (q', TM0.Stmt.write b) => [([Sym.st q, Sym.sym a], [Sym.st q', Sym.sym b])]
      | some (q', TM0.Stmt.move Dir.right) =>
          ([Sym.st q, Sym.sym a, Sym.rend], [Sym.sym a, Sym.st q', Sym.sym default, Sym.rend]) ::
            (Finset.univ : Finset Γ).toList.map fun c =>
              ([Sym.st q, Sym.sym a, Sym.sym c], [Sym.sym a, Sym.st q', Sym.sym c])
      | some (q', TM0.Stmt.move Dir.left) =>
          ([Sym.lend, Sym.st q, Sym.sym a], [Sym.lend, Sym.st q', Sym.sym default, Sym.sym a]) ::
            (Finset.univ : Finset Γ).toList.map fun c =>
              ([Sym.sym c, Sym.st q, Sym.sym a], [Sym.st q', Sym.sym c, Sym.sym a])

theorem mem_ruleList {M : TM0.Machine Γ Λ} {l r : List (Sym Γ Λ)} :
    (l, r) ∈ ruleList M ↔ Rules M l r := by
  constructor
  · intro h
    simp only [ruleList, List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and] at h
    obtain ⟨q, a, h⟩ := h
    rcases hM : M q a with _ | ⟨q', st⟩
    · rw [hM] at h; simp at h
    · rw [hM] at h
      cases st with
      | write b =>
          simp at h
          obtain ⟨rfl, rfl⟩ := h
          exact Rules.write hM
      | move d =>
          cases d with
          | right =>
              simp at h
              rcases h with ⟨rfl, rfl⟩ | ⟨c, rfl, rfl⟩
              · exact Rules.rightEnd hM
              · exact Rules.right hM
          | left =>
              simp at h
              rcases h with ⟨rfl, rfl⟩ | ⟨c, rfl, rfl⟩
              · exact Rules.leftEnd hM
              · exact Rules.left hM
  · intro h
    simp only [ruleList, List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and]
    cases h with
    | write hM => exact ⟨_, _, by rw [hM]; simp⟩
    | right hM => exact ⟨_, _, by rw [hM]; simp⟩
    | rightEnd hM => exact ⟨_, _, by rw [hM]; simp⟩
    | left hM => exact ⟨_, _, by rw [hM]; simp⟩
    | leftEnd hM => exact ⟨_, _, by rw [hM]; simp⟩

theorem reach_ruleList_iff {M : TM0.Machine Γ Λ} {w w' : List (Sym Γ Λ)} :
    Reach (inRules (ruleList M)) w w' ↔ Reach (Rules M) w w' := by
  constructor
  · exact Reach.mono (fun l r h => mem_ruleList.1 h)
  · exact Reach.mono (fun l r h => mem_ruleList.2 h)

end Finite

/-- The runner regime, as a finite rule list, is an unbounded-supply regime. -/
theorem runner_unboundedSupply :
    UnboundedSupply (ruleList runner) (runnerWord 0) := by
  intro L
  obtain ⟨w, hw, hl⟩ := runner_unbounded L
  exact ⟨w, reach_ruleList_iff.2 hw, hl⟩

/-- Hence no bound `L` at or above the start length closes the runner's bounded search: the
bounded decider never returns `unreachable` for it; it returns `boundExceeded`. -/
theorem runner_not_closed {L : ℕ} (hL : 4 ≤ L) : ¬ Closed (ruleList runner) L (runnerWord 0) :=
  not_closed_of_unbounded runner_unboundedSupply (by rw [runnerWord_length]; omega)

/-! ### A halting instance -/

/-- Writes a one on a blank cell in state `false`, then halts in state `true`. -/
def writeOne : TM0.Machine Bool Bool := fun q _ =>
  if q = false then some (true, TM0.Stmt.write true) else none

theorem writeOne_halts : Halts writeOne (TM0.init []) := by
  refine ⟨⟨true, Tape.mk₁ [true]⟩, ?_, rfl⟩
  refine Relation.ReflTransGen.single ?_
  show TM0.step writeOne (TM0.init []) = some _
  simp [TM0.step, TM0.init, writeOne, Tape.mk₁, Tape.mk₂, Tape.mk', Tape.write]

end TMEncoding
end GenesisComputation

#print axioms GenesisComputation.TMEncoding.card_sym
#print axioms GenesisComputation.TMEncoding.rep_exists
#print axioms GenesisComputation.TMEncoding.rep_unique
#print axioms GenesisComputation.TMEncoding.step_fwd
#print axioms GenesisComputation.TMEncoding.step_bwd
#print axioms GenesisComputation.TMEncoding.reaches_fwd
#print axioms GenesisComputation.TMEncoding.reach_bwd
#print axioms GenesisComputation.TMEncoding.halts_iff
#print axioms GenesisComputation.TMEncoding.runnerWord_length
#print axioms GenesisComputation.TMEncoding.runner_step
#print axioms GenesisComputation.TMEncoding.runner_unbounded
#print axioms GenesisComputation.TMEncoding.mem_ruleList
#print axioms GenesisComputation.TMEncoding.reach_ruleList_iff
#print axioms GenesisComputation.TMEncoding.runner_unboundedSupply
#print axioms GenesisComputation.TMEncoding.runner_not_closed
#print axioms GenesisComputation.TMEncoding.writeOne_halts
