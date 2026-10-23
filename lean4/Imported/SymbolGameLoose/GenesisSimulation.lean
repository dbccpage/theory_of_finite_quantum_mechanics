/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/GenesisSimulation.lean
   Original sha256: 0c0aebc5363935b73df405a384fabd9e67f4271b9b914b91f814f658410d5366 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.GenesisSimulation
   Reason         : genesis
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.GenesisContinuation
/-! A one-step simulation with event macros extends to every finite word.
Forward-only resource extensions preserve defined runs; they need not preserve
previous unavailability. These are abstract theorems, not Rust verification or
an unbounded Genesis self-interpreter theorem. -/
namespace GenesisSimulation
open GenesisContinuation
variable {S T I J : Type}

def encode (code : I → List J) : List I → List J
  | [] => []
  | a :: w => code a ++ encode code w

theorem run_none (step : S → I → Option S) (w : List I) : run step none w = none := by
  induction w with
  | nil => rfl
  | cons a w ih => exact ih

theorem simulation_all_words (source : S → I → Option S) (target : T → J → Option T)
    (f : S → T) (code : I → List J)
    (step_law : ∀ s a, run target (some (f s)) (code a) = (source s a).map f)
    (s : Option S) (w : List I) :
    run target (s.map f) (encode code w) = (run source s w).map f := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    simp only [encode, run_append, run]
    cases s with
    | none => simp only [Option.map_none, run_none, Option.bind_none]
    | some s =>
      simp only [Option.map_some, Option.bind_some, step_law]
      exact ih (source s a)

theorem extension_preserves_defined_runs (source : S → I → Option S)
    (target : T → J → Option T) (f : S → T) (code : I → List J)
    (forward : ∀ s a t, source s a = some t →
      run target (some (f s)) (code a) = some (f t))
    (s t : S) (w : List I) (defined : run source (some s) w = some t) :
    run target (some (f s)) (encode code w) = some (f t) := by
  induction w generalizing s with
  | nil =>
    simp only [run, Option.some.injEq] at defined
    subst s
    rfl
  | cons a w ih =>
    simp only [run, Option.bind_some] at defined
    cases h : source s a with
    | none => rw [h, run_none] at defined; cases defined
    | some u =>
      rw [h] at defined
      simp only [encode, run_append]
      rw [forward s a u h]
      exact ih u defined

-- Event macros have exactly additive lengths; no uniform step price is assumed.
theorem encoded_length (code : I → List J) (w : List I) :
    (encode code w).length = (w.map (fun a => (code a).length)).sum := by
  induction w with
  | nil => rfl
  | cons a w ih => simp [encode, ih]

#print axioms simulation_all_words
#print axioms extension_preserves_defined_runs
#print axioms encoded_length
end GenesisSimulation
