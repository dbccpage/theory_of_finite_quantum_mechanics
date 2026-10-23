/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/GenesisTrace.lean
   Original sha256: 674a931de5a10dfb746cd30ec7f72779764978433db7304af64c0edc67445a7c (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.GenesisTrace
   Reason         : genesis
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.GenesisContinuation

/-! Certified state-relative swaps generate an equivalence on words. The
quotient retains replay in the protected carrier; it does not assert literal
state equality or a context-independent independence alphabet. -/
namespace GenesisTrace
open GenesisContinuation

variable {S I A : Type}

def Answers (step : S → I → Option S) (observe : S → A) (start : S)
    (u : List I) : List I → Option A :=
  fun w => (run step (some start) (u ++ w)).map observe

inductive Equiv (step : S → I → Option S) (observe : S → A) (start : S) :
    List I → List I → Prop
  | refl (u) : Equiv step observe start u u
  | swap (p v : List I) (a b : I) (s l r : S)
      (hp : run step (some start) p = some s)
      (ab : run step (some s) [a,b] = some l)
      (ba : run step (some s) [b,a] = some r)
      (future : FutureEq step observe l r) :
      Equiv step observe start (p ++ [a,b] ++ v) (p ++ [b,a] ++ v)
  | symm {u v} : Equiv step observe start u v → Equiv step observe start v u
  | trans {u v w} : Equiv step observe start u v → Equiv step observe start v w →
      Equiv step observe start u w

variable {step : S → I → Option S} {observe : S → A} {start : S} {u v : List I}

theorem answers_invariant (h : Equiv step observe start u v) :
    Answers step observe start u = Answers step observe start v := by
  induction h with
  | refl => rfl
  | swap p v a b s l r hp ab ba future =>
    funext w
    simpa only [Answers, List.append_assoc, run_append, hp, ab, ba] using future (v ++ w)
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

def traceSetoid (step : S → I → Option S) (observe : S → A) (start : S) :
    Setoid (List I) where
  r := Equiv step observe start
  iseqv := ⟨Equiv.refl, Equiv.symm, Equiv.trans⟩

abbrev Trace (step : S → I → Option S) (observe : S → A) (start : S) :=
  Quotient (traceSetoid step observe start)

def traceAnswers (step : S → I → Option S) (observe : S → A) (start : S) :
    Trace step observe start → List I → Option A :=
  Quotient.lift (Answers step observe start) (fun _ _ h => answers_invariant h)

theorem replay_invariant (h : Equiv step observe start u v) :
    (run step (some start) u).map (Quotient.mk (futureSetoid step observe)) =
    (run step (some start) v).map (Quotient.mk (futureSetoid step observe)) := by
  have hh := answers_invariant h
  have eqw (w : List I) := congrFun hh w
  simp only [Answers, run_append] at eqw
  cases hu : run step (some start) u with
  | none =>
    cases hv : run step (some start) v with
    | none => rfl
    | some t =>
      have hx := eqw []
      simp [hu, hv, run] at hx
  | some s =>
    cases hv : run step (some start) v with
    | none =>
      have hx := eqw []
      simp [hu, hv, run] at hx
    | some t =>
      simp only [Option.map_some]
      congr 1
      apply Quotient.sound
      intro w
      simpa [hu, hv] using eqw w

def traceReplay (step : S → I → Option S) (observe : S → A) (start : S) :
    Trace step observe start → Option (Carrier step observe) :=
  Quotient.lift (fun u => (run step (some start) u).map
    (Quotient.mk (futureSetoid step observe))) (fun _ _ h => replay_invariant h)

-- Exact-state diamonds preserve literal replay under any suffix.
theorem exact_diamond (step : S → I → Option S) (s : S) (a b : I)
    (h : run step (some s) [a,b] = run step (some s) [b,a]) (v : List I) :
    run step (some s) ([a,b] ++ v) = run step (some s) ([b,a] ++ v) := by
  simp only [run_append, h]

#print axioms answers_invariant
#print axioms replay_invariant
#print axioms exact_diamond
end GenesisTrace
