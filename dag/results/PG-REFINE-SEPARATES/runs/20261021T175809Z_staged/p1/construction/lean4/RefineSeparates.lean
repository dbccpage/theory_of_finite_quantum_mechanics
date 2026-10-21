import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.Fintype.BigOperators

/-!
# Supplied-tag refinement, conflict structures and 2-colourings

AuthorityEffect: None.  Scope: a report `q : A -> O`, a supplied tag `t : A -> T`, and the refined
report `a |-> (q a, t a)`.  The tag is an INPUT of every theorem below; nothing here chooses or finds
a tag.  The conflict structure is an arbitrary relation `C` on `A` (a graph if `C` is symmetric).
The source declarations `refine_separates` / `supplied_tag_separates` are general one-pair theorems;
the source statement about many conflicts is prose only (a conflict graph and a proper colouring);
the iff, the odd-cycle obstruction, the clique/injectivity bit count and the bit-to-colour transport
below are NEW general statements proved here.  Finite counts over small graphs are in the native
certificate, not in this file, and they are not an algorithmic claim about finding tags.
-/

namespace RefineSeparates

variable {A O T : Type}

/-- Refine the old report `q` by the supplied tag `t`. -/
def refine (q : A → O) (t : A → T) (a : A) : O × T := (q a, t a)

/-- The old report is retained: it is the first projection of the refined report. -/
theorem refine_retains (q : A → O) (t : A → T) : Prod.fst ∘ refine q t = q := rfl

/-- Source theorem, general form: differing tags separate the refined reports. -/
theorem refine_separates (q : A → O) (t : A → T) (a b : A) (h : t a ≠ t b) :
    refine q t a ≠ refine q t b := fun e => h (congrArg Prod.snd e)

/-- Equality of refined reports is exactly equality of both components. -/
theorem refine_eq_iff (q : A → O) (t : A → T) (a b : A) :
    refine q t a = refine q t b ↔ q a = q b ∧ t a = t b := by
  simp [refine, Prod.ext_iff]

/-- On a collapsed pair the tag decides separation exactly (converse of the source theorem). -/
theorem refine_separates_iff (q : A → O) (t : A → T) (a b : A) (hq : q a = q b) :
    refine q t a ≠ refine q t b ↔ t a ≠ t b := by
  rw [Ne, Ne, refine_eq_iff]
  exact not_congr ⟨fun h => h.2, fun h => ⟨hq, h⟩⟩

/-- Refinement never merges what the old report separated. -/
theorem refine_keeps_old_separation (q : A → O) (t : A → T) (a b : A) (h : q a ≠ q b) :
    refine q t a ≠ refine q t b := fun e => h (congrArg Prod.fst e)

/-! ## Many conflicts at once: proper tags -/

/-- `t` is a proper tag for the conflict relation `C`: every conflicting pair gets different tags. -/
def Proper (C : A → A → Prop) (t : A → T) : Prop := ∀ a b, C a b → t a ≠ t b

/-- The refinement separates every conflict. -/
def Resolves (q : A → O) (t : A → T) (C : A → A → Prop) : Prop :=
  ∀ a b, C a b → refine q t a ≠ refine q t b

/-- If every conflict is a collapsed pair of the old report, resolving all conflicts by one tag is
exactly a proper colouring of the conflict relation by the tag values. -/
theorem resolves_iff_proper (q : A → O) (t : A → T) (C : A → A → Prop)
    (hC : ∀ a b, C a b → q a = q b) : Resolves q t C ↔ Proper C t :=
  ⟨fun h a b c => (refine_separates_iff q t a b (hC a b c)).mp (h a b c),
   fun h a b c => (refine_separates_iff q t a b (hC a b c)).mpr (h a b c)⟩

/-- Without the collapse hypothesis a proper tag still resolves every conflict (one direction only). -/
theorem resolves_of_proper (q : A → O) (t : A → T) (C : A → A → Prop) (h : Proper C t) :
    Resolves q t C := fun a b c => refine_separates q t a b (h a b c)

/-- A proper tag for `C1` and one for `C2` give a proper tag for `C1 or C2` with the pair of tags. -/
theorem proper_union {T1 T2 : Type} (C1 C2 : A → A → Prop) (t1 : A → T1) (t2 : A → T2)
    (h1 : Proper C1 t1) (h2 : Proper C2 t2) :
    Proper (fun a b => C1 a b ∨ C2 a b) (fun a => (t1 a, t2 a)) := by
  intro a b h e
  rcases h with h | h
  · exact h1 a b h (congrArg Prod.fst e)
  · exact h2 a b h (congrArg Prod.snd e)

/-- Transport of properness along an equivalence of tag types. -/
theorem proper_equiv {T T' : Type} (e : T ≃ T') (C : A → A → Prop) (t : A → T) (h : Proper C t) :
    Proper C (fun a => e (t a)) := fun a b c w => h a b c (e.injective w)

theorem card_bits (b : ℕ) : Fintype.card (Fin b → Bool) = 2 ^ b := by
  rw [Fintype.card_pi_const, Fintype.card_bool]

/-- A `b`-bit tag is a colouring with `2^b` colours, and conversely. -/
theorem bits_iff_colours (b : ℕ) (C : A → A → Prop) :
    (∃ t : A → (Fin b → Bool), Proper C t) ↔ (∃ t : A → Fin (2 ^ b), Proper C t) := by
  have hc : Fintype.card (Fin b → Bool) = Fintype.card (Fin (2 ^ b)) := by
    rw [card_bits, Fintype.card_fin]
  let e : (Fin b → Bool) ≃ Fin (2 ^ b) := Fintype.equivOfCardEq hc
  exact ⟨fun ⟨t, h⟩ => ⟨_, proper_equiv e C t h⟩, fun ⟨t, h⟩ => ⟨_, proper_equiv e.symm C t h⟩⟩

/-! ## One bit: proper 2-colouring, odd cycles -/

/-- An odd closed walk in the conflict relation admits no one-bit proper tag. -/
theorem no_one_bit_of_odd_cycle (C : A → A → Prop) (f : ℕ → A) (n : ℕ)
    (hn : n % 2 = 1) (hstep : ∀ i, i < n → C (f i) (f (i + 1))) (hclose : f n = f 0) :
    ¬ ∃ t : A → Bool, Proper C t := by
  rintro ⟨t, ht⟩
  have key : ∀ i, i ≤ n → (t (f i) = t (f 0) ↔ i % 2 = 0) := by
    intro i
    induction i with
    | zero => intro _; simp
    | succ k ih =>
      intro hk
      have h1 := ih (by omega)
      have h2 : t (f k) ≠ t (f (k + 1)) := ht _ _ (hstep k (by omega))
      constructor
      · intro h
        by_contra hne
        have hk2 : k % 2 = 0 := by omega
        have : t (f k) = t (f 0) := h1.mpr hk2
        exact h2 (this.trans h.symm)
      · intro h
        have hk2 : ¬ (k % 2 = 0) := by omega
        have h3 : t (f k) ≠ t (f 0) := fun e => hk2 (h1.mp e)
        revert h2 h3
        cases t (f k) <;> cases t (f (k + 1)) <;> cases t (f 0) <;> simp
  have := (key n le_rfl).mp (by rw [hclose])
  omega

/-- Three pairwise conflicting elements (a triangle) admit no one-bit proper tag (instance of the odd
cycle statement with n = 3). -/
theorem triangle_no_one_bit {a b c : A} (C : A → A → Prop)
    (hab : C a b) (hbc : C b c) (hca : C c a) : ¬ ∃ t : A → Bool, Proper C t := by
  refine no_one_bit_of_odd_cycle C (fun i => if i = 0 then a else if i = 1 then b else if i = 2 then c else a)
    3 (by decide) ?_ (by simp)
  intro i hi
  have : i = 0 ∨ i = 1 ∨ i = 2 := by omega
  rcases this with rfl | rfl | rfl <;> simpa

/-! ## A fibre of size m: all pairs conflict -/

/-- Separating every pair of distinct elements is injectivity of the tag. -/
theorem proper_ne_iff_injective (t : A → T) : Proper (fun x y : A => x ≠ y) t ↔ Function.Injective t :=
  ⟨fun h _ _ e => by_contra fun hne => h _ _ hne e, fun h _ _ hne e => hne (h e)⟩

/-- A `b`-bit tag separates all pairs of a fibre of size `m` iff `m <= 2^b`
(so `ceil (log2 m)` bits are necessary and sufficient). -/
theorem fibre_bits_iff [Fintype A] (b : ℕ) :
    (∃ t : A → (Fin b → Bool), Proper (fun x y : A => x ≠ y) t) ↔ Fintype.card A ≤ 2 ^ b := by
  constructor
  · rintro ⟨t, ht⟩
    have := Fintype.card_le_of_injective t ((proper_ne_iff_injective t).mp ht)
    rwa [card_bits] at this
  · intro h
    have : Fintype.card A ≤ Fintype.card (Fin b → Bool) := by rwa [card_bits]
    obtain ⟨f⟩ := Function.Embedding.nonempty_of_card_le this
    exact ⟨f, (proper_ne_iff_injective f).mpr f.injective⟩

/-- One bit separates a fibre iff it has at most two elements. -/
theorem fibre_one_bit_iff [Fintype A] :
    (∃ t : A → Bool, Proper (fun x y : A => x ≠ y) t) ↔ Fintype.card A ≤ 2 := by
  constructor
  · rintro ⟨t, ht⟩
    have := Fintype.card_le_of_injective t ((proper_ne_iff_injective t).mp ht)
    simpa using this
  · intro h
    have : Fintype.card A ≤ Fintype.card Bool := by simpa using h
    obtain ⟨f⟩ := Function.Embedding.nonempty_of_card_le this
    exact ⟨f, (proper_ne_iff_injective f).mpr f.injective⟩

/-- The fibre of a report: some `b`-bit tag on the whole type resolves every conflict between distinct elements of
the fibre `{a // q a = x}` iff the fibre has at most `2^b` elements. -/
theorem fibre_report_bits_iff (q : A → O) (x : O) [Fintype {a // q a = x}] (b : ℕ) :
    (∃ t : A → (Fin b → Bool), Resolves q t (fun a a' => q a = x ∧ q a' = x ∧ a ≠ a')) ↔
      Fintype.card {a // q a = x} ≤ 2 ^ b := by
  classical
  rw [← fibre_bits_iff (A := {a // q a = x}) b]
  have hC : ∀ a a' : A, (q a = x ∧ q a' = x ∧ a ≠ a') → q a = q a' := fun a a' h => h.1.trans h.2.1.symm
  constructor
  · rintro ⟨t, ht⟩
    have hp := (resolves_iff_proper q t _ hC).mp ht
    exact ⟨fun a => t a.1, fun a a' hne => hp a.1 a'.1 ⟨a.2, a'.2, fun e => hne (Subtype.ext e)⟩⟩
  · rintro ⟨s, hs⟩
    refine ⟨fun a => if h : q a = x then s ⟨a, h⟩ else fun _ => false, ?_⟩
    apply resolves_of_proper
    rintro a a' ⟨h1, h2, hne⟩
    simp only [h1, h2, dite_true]
    exact hs ⟨a, h1⟩ ⟨a', h2⟩ (fun e => hne (congrArg Subtype.val e))

/-- Headline: for a conflict relation contained in a collapse of `q`, some `b`-bit refinement resolves
all conflicts iff the conflict relation has a proper `2^b`-colouring (for `b = 1`: a proper
2-colouring, refused by any odd closed walk; for the complete conflict relation on a fibre: iff the
fibre has at most `2^b` elements, see `fibre_bits_iff`).  Existence only: no tag is constructed or
searched for. -/
theorem refine_separates_many (q : A → O) (C : A → A → Prop) (hC : ∀ a b, C a b → q a = q b) (b : ℕ) :
    ((∃ t : A → (Fin b → Bool), Resolves q t C) ↔ (∃ t : A → Fin (2 ^ b), Proper C t)) :=
  by
    rw [← bits_iff_colours]
    exact ⟨fun ⟨t, h⟩ => ⟨t, (resolves_iff_proper q t C hC).mp h⟩,
           fun ⟨t, h⟩ => ⟨t, (resolves_iff_proper q t C hC).mpr h⟩⟩

end RefineSeparates

#print axioms RefineSeparates.refine_retains
#print axioms RefineSeparates.refine_separates
#print axioms RefineSeparates.refine_separates_iff
#print axioms RefineSeparates.refine_keeps_old_separation
#print axioms RefineSeparates.resolves_iff_proper
#print axioms RefineSeparates.proper_union
#print axioms RefineSeparates.card_bits
#print axioms RefineSeparates.bits_iff_colours
#print axioms RefineSeparates.no_one_bit_of_odd_cycle
#print axioms RefineSeparates.triangle_no_one_bit
#print axioms RefineSeparates.fibre_bits_iff
#print axioms RefineSeparates.fibre_one_bit_iff
#print axioms RefineSeparates.fibre_report_bits_iff
#print axioms RefineSeparates.refine_separates_many
