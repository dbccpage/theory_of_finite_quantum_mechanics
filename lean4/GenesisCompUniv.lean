import GenesisCompTM
import Mathlib.Computability.TuringMachine.ToPartrec
import Mathlib.Computability.PartrecCode
import Mathlib.Computability.Halting

/-!
# Universality and undecidability for the rewriting regimes (C6, C7)

AuthorityEffect: None.

Everything about partial recursive functions, `Nat.Partrec.Code`, the Turing machine models
`TM2`, `TM1`, `TM0` and their simulations, and the halting problem is IMPORTED from Mathlib
(`Mathlib.Computability.PartrecCode`, `Mathlib.Computability.TuringMachine.ToPartrec`,
`...StackTuringMachine`, `...PostTuringMachine`, `Mathlib.Computability.Halting`).  Nothing of
that theory is re-derived here.  What is new:

* `universal_code`  one fixed `Nat.Partrec.Code` `u` evaluates every code on every input;
* `univCode`        one fixed `Turing.ToPartrec.Code` computing the same universal function
  on a single natural number argument;
* the composite fixed `TM0` machine `M0 = TM1to0.tr (TM2to1.tr PartrecToTM2.tr)` and an explicit
  family of initial configurations `initCfg0 x`, with
  `halts_iff_eval_dom : Halts M0 (initCfg0 (pair (encode c) n)) ↔ (Code.eval c n).Dom`;
* `reach_irreducible_not_computable`, `nfReach_not_computable`  composing with
  `TMEncoding.halts_iff` and `ComputablePred.halting_problem`: the predicate "the rewriting
  regime `Rules M0` reaches an irreducible word from the represented start word of the input" is
  not a computable predicate of the input (of the code `c`, or of `x : ℕ`);
* `used_state_marks_finite`, `used_marks_finite`, `card_G1`: only finitely many marks occur in
  any word reachable from a start word (1250 tape marks, the two end markers, and the state marks
  in the finite set `S0` supplied by Mathlib's `tr_supports` chain).

What is NOT proved: that the map from an input to its start word is itself computable
(`startWord_computable`, listed OPEN; it needs a `Primcodable` structure on the mark type).  The
two undecidability statements above are about the explicit family of start words.  The reduction
of the halting problem to a single decision problem over encoded rewriting instances is
`reach_problem_not_computable`, which is CONDITIONAL on that lemma.  The size of `S0` is not
computed: it depends on the code `univCode`, chosen by `Classical.choose`.
-/

open Turing

namespace GenesisComputation
namespace Universal

open Nat.Partrec (Code)

/-! ## The universal evaluator is partial recursive (imported) and has a code -/

/-- The universal evaluator on a paired argument: `pair (encode c) n ↦ eval c n`. -/
noncomputable def univFun : ℕ →. ℕ := fun m =>
  Nat.Partrec.Code.eval (Denumerable.ofNat Code m.unpair.1) m.unpair.2

theorem univFun_partrec : Partrec univFun :=
  Nat.Partrec.Code.eval_part.comp
    ((Computable.ofNat Code).comp (Computable.fst.comp Computable.unpair))
    (Computable.snd.comp Computable.unpair)

theorem univFun_apply (c : Code) (n : ℕ) :
    univFun (Nat.pair (Encodable.encode c) n) = Nat.Partrec.Code.eval c n := by
  simp [univFun]

/-- One fixed code evaluates every code: `eval u (pair (encode c) n) = eval c n`. -/
theorem universal_code :
    ∃ u : Code, ∀ (c : Code) (n : ℕ),
      Nat.Partrec.Code.eval u (Nat.pair (Encodable.encode c) n) = Nat.Partrec.Code.eval c n := by
  obtain ⟨u, hu⟩ := Nat.Partrec.Code.exists_code.1 (Partrec.nat_iff.1 univFun_partrec)
  exact ⟨u, fun c n => by rw [hu, univFun_apply]⟩

/-- A fixed `ToPartrec` code computing the universal function on one natural number. -/
theorem univCode_exists :
    ∃ cu : ToPartrec.Code, ∀ x : ℕ, cu.eval [x] = pure <$> univFun x := by
  obtain ⟨cu, hcu⟩ := ToPartrec.Code.exists_code
    (f := fun v : List.Vector ℕ 1 => univFun v.head)
    (Nat.Partrec'.part_iff₁.2 univFun_partrec)
  exact ⟨cu, fun x => hcu ⟨[x], rfl⟩⟩


/-! ## The fixed composite machine -/

section Machine

open PartrecToTM2

instance : Fintype K' := ⟨{K'.main, K'.rev, K'.aux, K'.stack}, by intro x; cases x <;> simp⟩

/-- The fixed code of `univCode_exists`. -/
noncomputable def univCode : ToPartrec.Code := Classical.choose univCode_exists

theorem univCode_eval (x : ℕ) : univCode.eval [x] = pure <$> univFun x :=
  Classical.choose_spec univCode_exists x

/-- Stack alphabet of the TM1 emulator of the TM2 machine. -/
abbrev G1 : Type := TM2to1.Γ' K' (fun _ => Γ')

/-- Label type of the TM1 emulator. -/
abbrev L1 : Type := TM2to1.Λ' K' (fun _ => Γ') Λ' (Option Γ')

/-- The fixed TM2 machine of Mathlib's partial recursive to TM2 simulation. -/
abbrev M2 : Λ' → TM2.Stmt (fun _ : K' => Γ') Λ' (Option Γ') := PartrecToTM2.tr

/-- The TM1 machine emulating `M2`. -/
abbrev M1 : L1 → TM1.Stmt G1 L1 (Option Γ') := TM2to1.tr M2

/-- The fixed TM0 machine emulating `M1`: the composite `TM1to0.tr (TM2to1.tr tr)`. -/
abbrev M0 : TM0.Machine G1 (TM1to0.Λ' M1) := TM1to0.tr M1

/-- The tape of the TM1 emulator holding a list `l` on the main stack. -/
def initL (l : List Γ') : ListBlank (∀ _ : K', Option Γ') :=
  ListBlank.mk (l.reverse.map fun a => Function.update (fun _ : K' => (none : Option Γ')) K'.main (some a))

theorem trCfg_init_gen (q : Option Λ') (v : Option Γ') (l : List Γ') :
    TM2to1.TrCfg (⟨q, v, K'.elim l [] [] []⟩ : TM2.Cfg (fun _ : K' => Γ') Λ' (Option Γ'))
      (⟨q.map TM2to1.Λ'.normal, v, Tape.mk' ∅ (TM2to1.addBottom (initL l))⟩ : TM1.Cfg G1 L1 (Option Γ')) := by
  refine TM2to1.TrCfg.mk (initL l) fun k => ?_
  refine ListBlank.ext fun i => ?_
  rw [initL, ListBlank.map_mk, ListBlank.nth_mk, List.getI_eq_getElem?_getD, List.map_map]
  cases k
  all_goals
    simp [K'.elim, proj, List.map_reverse, ListBlank.nth_mk, List.getI_eq_getElem?_getD,
      Function.comp_def]
    try (rw [List.getElem?_replicate]; split_ifs <;> rfl)

end Machine


section Halting

open PartrecToTM2

/-- Initial TM2 configuration for the universal code on input `x`. -/
noncomputable def init2 (x : ℕ) : TM2.Cfg (fun _ : K' => Γ') Λ' (Option Γ') :=
  PartrecToTM2.init univCode [x]

/-- Initial TM1 configuration of the emulator. -/
noncomputable def init1 (x : ℕ) : TM1.Cfg G1 L1 (Option Γ') :=
  ⟨(some (trNormal univCode Cont'.halt)).map TM2to1.Λ'.normal, none,
    Tape.mk' ∅ (TM2to1.addBottom (initL (trList [x])))⟩

/-- Initial TM0 configuration: the explicit family of starting configurations of the fixed
machine `M0` for the universal computation, on the paired input `x`. -/
noncomputable def initCfg0 (x : ℕ) : TM0.Cfg G1 (TM1to0.Λ' M1) :=
  TM1to0.trCfg M1 (init1 x)

theorem tr21 (x : ℕ) : TM2to1.TrCfg (init2 x) (init1 x) :=
  trCfg_init_gen _ _ _

/-- **C6, TM2 output form** (Mathlib `tr_eval` composed with the universal code).  The fixed
TM2 machine `PartrecToTM2.tr`, started on the paired input, halts in the configuration holding
`Code.eval c n` exactly when that value is defined. -/
theorem tm2_computes_eval (c : Code) (n : ℕ) :
    StateTransition.eval (TM2.step PartrecToTM2.tr) (init2 (Nat.pair (Encodable.encode c) n)) =
      PartrecToTM2.halt <$> (pure <$> Nat.Partrec.Code.eval c n) := by
  unfold init2
  rw [PartrecToTM2.tr_eval, univCode_eval, univFun_apply]

/-- The three halting predicates agree: the fixed TM0 machine halts from `initCfg0 x` exactly
when the universal function is defined at `x`. -/
theorem dom_chain (x : ℕ) :
    (StateTransition.eval (TM0.step M0) (initCfg0 x)).Dom ↔ (univFun x).Dom := by
  have h1 := StateTransition.tr_eval_dom (TM1to0.tr_respects M1)
    (a₁ := init1 x) (a₂ := initCfg0 x) rfl
  have h2 := StateTransition.tr_eval_dom (TM2to1.tr_respects M2) (tr21 x)
  have h3 : (StateTransition.eval (TM2.step PartrecToTM2.tr) (init2 x)).Dom ↔ (univFun x).Dom := by
    have := PartrecToTM2.tr_eval univCode [x]
    unfold init2
    rw [this, univCode_eval]
    simp
  rw [h1, h2, h3]

theorem halts_iff_dom {Γ Λ : Type*} [Inhabited Γ] [Inhabited Λ] (M : TM0.Machine Γ Λ)
    (c : TM0.Cfg Γ Λ) :
    TMEncoding.Halts M c ↔ (StateTransition.eval (TM0.step M) c).Dom := by
  rw [Part.dom_iff_mem]
  constructor
  · rintro ⟨c', hc, hn⟩
    exact ⟨c', StateTransition.mem_eval.2 ⟨hc, hn⟩⟩
  · rintro ⟨c', h⟩
    obtain ⟨hc, hn⟩ := StateTransition.mem_eval.1 h
    exact ⟨c', hc, hn⟩

/-- **C6, halting form.**  The fixed machine `M0` started on `initCfg0 (pair (encode c) n)` halts
exactly when `Nat.Partrec.Code.eval c n` is defined. -/
theorem halts_iff_eval_dom (c : Code) (n : ℕ) :
    TMEncoding.Halts M0 (initCfg0 (Nat.pair (Encodable.encode c) n)) ↔
      (Nat.Partrec.Code.eval c n).Dom := by
  rw [halts_iff_dom, dom_chain, univFun_apply]

/-- **C7, machine level.**  With the machine fixed, halting from the family of initial
configurations is not a computable predicate of the code. -/
theorem halting_not_computable (n : ℕ) :
    ¬ ComputablePred (fun c : Code =>
      TMEncoding.Halts M0 (initCfg0 (Nat.pair (Encodable.encode c) n))) := by
  intro h
  exact ComputablePred.halting_problem n (h.of_eq fun c => halts_iff_eval_dom c n)

open TMEncoding in
/-- A fixed representing word of the start configuration. -/
noncomputable def startWord (x : ℕ) : List (Sym G1 (TM1to0.Λ' M1)) :=
  Classical.choose (rep_exists (initCfg0 x))

open TMEncoding in
theorem startWord_rep (x : ℕ) : Rep (initCfg0 x) (startWord x) :=
  Classical.choose_spec (rep_exists (initCfg0 x))

open TMEncoding in
/-- The rewriting regime `Rules M0` reaches an irreducible word from the start word exactly
when the universal evaluation halts. -/
theorem reach_irreducible_iff (c : Code) (n : ℕ) :
    (∃ w', Reach (Rules M0) (startWord (Nat.pair (Encodable.encode c) n)) w' ∧
        Irreducible (Rules M0) w') ↔ (Nat.Partrec.Code.eval c n).Dom := by
  rw [← halts_iff_eval_dom, halts_iff (startWord_rep _)]

open TMEncoding in
/-- **C7, rewriting level.**  Reachability of an irreducible word from the family of start words
of the fixed regime `Rules M0` is not a computable predicate of the code.  This is the
undecidability of the Reach problem for one fixed rewriting regime, with the start-word family
as the instance family.  That `c ↦ startWord (pair (encode c) n)` is itself computable is NOT
proved here (`startWord_computable`, OPEN), so this does not yet reduce the halting problem to a
single computable decision problem over encoded rewriting instances. -/
theorem reach_irreducible_not_computable (n : ℕ) :
    ¬ ComputablePred (fun c : Code =>
      ∃ w', Reach (Rules M0) (startWord (Nat.pair (Encodable.encode c) n)) w' ∧
        Irreducible (Rules M0) w') := by
  intro h
  exact ComputablePred.halting_problem n (h.of_eq fun c => reach_irreducible_iff c n)

end Halting


section Support

open PartrecToTM2

/-- The finite set of TM2 labels reachable from the universal code (Mathlib `codeSupp`). -/
noncomputable def S2 : Finset Λ' := codeSupp univCode Cont'.halt

/-- The finite set of TM1 labels of the emulator. -/
noncomputable def S1 : Finset L1 := TM2to1.trSupp M2 S2

/-- The finite set of TM0 states used by the composite fixed machine. -/
noncomputable def S0 : Finset (TM1to0.Λ' M1) := TM1to0.trStmts M1 S1

theorem state_closed {q : TM1to0.Λ' M1} {a : G1} {q' : TM1to0.Λ' M1} {s : TM0.Stmt G1}
    (h : (q', s) ∈ M0 q a) (hq : q ∈ (S0 : Set (TM1to0.Λ' M1))) :
    q' ∈ (S0 : Set (TM1to0.Λ' M1)) :=
  letI : Inhabited Λ' := ⟨trNormal univCode Cont'.halt⟩
  (TM1to0.tr_supports M1 (TM2to1.tr_supports M2 (tr_supports univCode Cont'.halt))).2 h hq

/-- Every state of the composite machine reachable from an initial configuration lies in the
finite set `S0`: only finitely many state marks are ever used. -/
theorem step_closed {c c' : TM0.Cfg G1 (TM1to0.Λ' M1)}
    (h : TM0.step M0 c = some c') (hc : c.q ∈ (S0 : Set (TM1to0.Λ' M1))) :
    c'.q ∈ (S0 : Set (TM1to0.Λ' M1)) := by
  obtain ⟨q, T⟩ := c
  rcases hM : M0 q T.1 with _ | ⟨q', s⟩
  · simp [TM0.step, hM] at h
  · simp only [TM0.step, hM, Option.map_some, Option.some.injEq] at h
    subst h
    exact state_closed (by rw [hM]; rfl) hc

theorem init_mem (x : ℕ) : (initCfg0 x).q ∈ (S0 : Set (TM1to0.Λ' M1)) := by
  let _ : Inhabited Λ' := ⟨trNormal univCode Cont'.halt⟩
  have hs := tr_supports univCode Cont'.halt
  have h1 : TM2to1.Λ'.normal (trNormal univCode Cont'.halt) ∈ S1 :=
    (TM2to1.tr_supports M2 hs).1
  show (((some (TM2to1.Λ'.normal (trNormal univCode Cont'.halt))).map M1), (none : Option Γ')) ∈
    TM1to0.trStmts M1 S1
  refine Finset.mem_product.2 ⟨?_, Finset.mem_univ _⟩
  simp only [TM1.stmts, Finset.mem_insertNone, Option.mem_def, Option.some_inj, forall_eq',
    Finset.mem_biUnion, Option.map_some]
  exact ⟨_, h1, TM1.stmts₁_self⟩

open TMEncoding in
theorem reaches_closed {c c' : TM0.Cfg G1 (TM1to0.Λ' M1)} (h : TM0.Reaches M0 c c')
    (hc : c.q ∈ (S0 : Set (TM1to0.Λ' M1))) : c'.q ∈ (S0 : Set (TM1to0.Λ' M1)) := by
  induction h with
  | refl => exact hc
  | tail _ hs ih => exact step_closed hs ih

open TMEncoding in
/-- Finitely many marks: every state mark in a word reachable from the start word lies in the
fixed finite set `S0`.  Together with the finite tape alphabet `G1 = Bool × (K' → Option Γ')`
and the two end markers, the rewriting regime uses a finite alphabet. -/
theorem used_state_marks_finite (x : ℕ) {w : List (Sym G1 (TM1to0.Λ' M1))}
    (hw : Reach (Rules M0) (startWord x) w) {q : TM1to0.Λ' M1} (hq : Sym.st q ∈ w) :
    q ∈ S0 := by
  obtain ⟨c', ⟨ul, ur, hl, hr, hw'⟩, hc⟩ := reach_bwd (startWord_rep x) hw
  have hqc : c'.q ∈ (S0 : Set (TM1to0.Λ' M1)) := reaches_closed hc (init_mem x)
  rw [hw', cfgWord_eq] at hq
  rcases List.mem_append.1 hq with hq | hq
  · exact absurd rfl (noSt_prefix ul _ hq q)
  · rcases List.mem_cons.1 hq with h | h
    · have : q = c'.q := Sym.st.inj h
      rw [this]
      exact Finset.mem_coe.1 hqc
    · exact absurd rfl (noSt_suffix ur c'.Tape.head _ h q)

end Support


section Undecidable

open TMEncoding

/-- The normal-form reachability problem of the fixed regime `Rules M0` on its start-word
family indexed by `x : ℕ`: some irreducible word is reachable from the start word of `x`. -/
def NFReach (x : ℕ) : Prop :=
  ∃ w', Reach (Rules M0) (startWord x) w' ∧ Irreducible (Rules M0) w'

theorem nfReach_iff (x : ℕ) : NFReach x ↔ (univFun x).Dom := by
  unfold NFReach
  rw [← halts_iff (startWord_rep x), halts_iff_dom, dom_chain]

/-- The set of inputs `x` whose start word reaches an irreducible word is not computable:
`NFReach x ↔ (univFun x).Dom`, and `univFun` evaluates every code. -/
theorem nfReach_not_computable : ¬ ComputablePred NFReach := by
  rintro ⟨inst, h⟩
  have hcomp : Computable (fun c : Code => @decide (NFReach (Nat.pair (Encodable.encode c) 0))
      (inst _)) :=
    h.comp (Primrec₂.natPair.to_comp.comp Computable.encode (Computable.const 0))
  have h1 : ComputablePred (fun c : Code => NFReach (Nat.pair (Encodable.encode c) 0)) :=
    ⟨fun c => inst _, hcomp⟩
  refine ComputablePred.halting_problem 0 (h1.of_eq fun c => ?_)
  rw [nfReach_iff, univFun_apply]

/-- CONDITIONAL reduction on encoded instances: if the start-word map is computable for some
`Primcodable` structure on the marks, the normal-form reachability problem on words of the
fixed regime is not a computable predicate.  The hypothesis `Computable startWord` together with
the `Primcodable` structure is the OPEN lemma `startWord_computable`. -/
theorem reach_problem_not_computable
    [Primcodable (Sym G1 (TM1to0.Λ' M1))] (hc : Computable startWord) :
    ¬ ComputablePred (fun w : List (Sym G1 (TM1to0.Λ' M1)) =>
      ∃ w', Reach (Rules M0) w w' ∧ Irreducible (Rules M0) w') := by
  rintro ⟨inst, h⟩
  exact nfReach_not_computable ⟨fun x => inst _, h.comp hc⟩

end Undecidable


section Budget

open TMEncoding PartrecToTM2

/-- The tape alphabet of the composite machine has exactly `2 * 5^4 = 1250` marks. -/
theorem card_G1 : Fintype.card G1 = 1250 := by
  show Fintype.card (Bool × (K' → Option Γ')) = 1250
  have hK : Fintype.card K' = 4 := rfl
  have hG : Fintype.card Γ' = 4 := by decide
  simp [Fintype.card_prod, Fintype.card_fun, Fintype.card_option, hK, hG]

open scoped Classical in
/-- The finite set of marks that can occur in any word reachable from a start word: the two end
markers, all tape marks, and the state marks in `S0`. -/
noncomputable def markSet : Finset (Sym G1 (TM1to0.Λ' M1)) :=
  {Sym.lend, Sym.rend} ∪ (Finset.univ : Finset G1).image Sym.sym ∪ S0.image Sym.st

open scoped Classical in
/-- **C1/C6 link.**  Every mark occurring in a word reachable from the start word of the fixed
regime lies in the finite set `markSet`: the regime uses a finite alphabet, of which the tape part
has exactly 1250 marks (`card_G1`). -/
theorem used_marks_finite (x : ℕ) {w : List (Sym G1 (TM1to0.Λ' M1))}
    (hw : Reach (Rules M0) (startWord x) w) {y : Sym G1 (TM1to0.Λ' M1)} (hy : y ∈ w) :
    y ∈ markSet := by
  obtain ⟨c', ⟨ul, ur, hl, hr, hw'⟩, hc⟩ := reach_bwd (startWord_rep x) hw
  rw [hw', cfgWord_eq] at hy
  simp only [markSet, Finset.mem_union, Finset.mem_insert, Finset.mem_singleton,
    Finset.mem_image, Finset.mem_univ, true_and]
  cases y with
  | lend => exact Or.inl (Or.inl (Or.inl rfl))
  | rend => exact Or.inl (Or.inl (Or.inr rfl))
  | sym a => exact Or.inl (Or.inr ⟨a, rfl⟩)
  | st q => exact Or.inr ⟨q, Finset.mem_coe.1 (by
      have := used_state_marks_finite x hw (q := q) (by rw [hw', cfgWord_eq]; exact hy)
      exact Finset.mem_coe.2 this), rfl⟩

end Budget

end Universal
end GenesisComputation

#print axioms GenesisComputation.Universal.univFun_partrec
#print axioms GenesisComputation.Universal.universal_code
#print axioms GenesisComputation.Universal.univCode_eval
#print axioms GenesisComputation.Universal.trCfg_init_gen
#print axioms GenesisComputation.Universal.dom_chain
#print axioms GenesisComputation.Universal.tm2_computes_eval
#print axioms GenesisComputation.Universal.halts_iff_dom
#print axioms GenesisComputation.Universal.halts_iff_eval_dom
#print axioms GenesisComputation.Universal.halting_not_computable
#print axioms GenesisComputation.Universal.startWord_rep
#print axioms GenesisComputation.Universal.reach_irreducible_iff
#print axioms GenesisComputation.Universal.reach_irreducible_not_computable
#print axioms GenesisComputation.Universal.state_closed
#print axioms GenesisComputation.Universal.step_closed
#print axioms GenesisComputation.Universal.init_mem
#print axioms GenesisComputation.Universal.reaches_closed
#print axioms GenesisComputation.Universal.used_state_marks_finite
#print axioms GenesisComputation.Universal.nfReach_iff
#print axioms GenesisComputation.Universal.nfReach_not_computable
#print axioms GenesisComputation.Universal.reach_problem_not_computable
#print axioms GenesisComputation.Universal.card_G1
#print axioms GenesisComputation.Universal.used_marks_finite
