/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/GenesisJointOperations.lean
   Original sha256: d6dcefdb073e90527081d695429287292df433f2aee4b1d33fd846e81f90c0cf (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.GenesisJointOperations
   Reason         : genesis
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.GenesisContinuation

/-! Sufficient conditions for compositional protected futures, and the integer
CHSH bound for any common nonnegative preparation mixture. This proves abstract
laws; it does not verify Rust, infer probabilities, or assert physical locality.
The product theorem uses the full product. Restricted Rust relations must also
pass the explicit closure check before their local operations are admitted. -/
namespace GenesisJointOperations
open GenesisContinuation
variable {L R I J K A B : Type}

def PairRel (r : L → L → Prop) (s : R → R → Prop) (x y : L × R) : Prop :=
  r x.1 y.1 ∧ s x.2 y.2

def jointStep (left : L → I → Option L) (right : R → J → Option R)
    (interaction : L × R → K → Option (L × R)) :
    L × R → Sum I (Sum J K) → Option (L × R)
  | (l,r), .inl a => (left l a).map (fun t => (t,r))
  | (l,r), .inr (.inl b) => (right r b).map (fun t => (l,t))
  | p, .inr (.inr k) => interaction p k

theorem product_stable (left : L → I → Option L) (right : R → J → Option R)
    (interaction : L × R → K → Option (L × R))
    (rl : L → L → Prop) (rr : R → R → Prop)
    (hl : Stable rl left) (hr : Stable rr right)
    (hi : Stable (PairRel rl rr) interaction) :
    Stable (PairRel rl rr) (jointStep left right interaction) := by
  intro x y h a
  cases a with
  | inl a =>
    have hh := hl x.1 y.1 h.1 a
    cases hx : left x.1 a <;> cases hy : left y.1 a <;>
      simp_all [jointStep, Related, PairRel]
  | inr a =>
    cases a with
    | inl b =>
      have hh := hr x.2 y.2 h.2 b
      cases hx : right x.2 b <;> cases hy : right y.2 b <;>
        simp_all [jointStep, Related, PairRel]
    | inr k => exact hi x y h k

theorem paired_local_futures_suffice
    (left : L → I → Option L) (right : R → J → Option R)
    (ol : L → A) (orr : R → B)
    (interaction : L × R → K → Option (L × R))
    (hi : Stable (PairRel (FutureEq left ol) (FutureEq right orr)) interaction)
    (x y : L × R) (h : PairRel (FutureEq left ol) (FutureEq right orr) x y) :
    FutureEq (jointStep left right interaction) (fun p => (ol p.1, orr p.2)) x y := by
  apply stable_preserves_futures _ _ (PairRel (FutureEq left ol) (FutureEq right orr))
    (product_stable left right interaction _ _ (future_eq_stable left ol)
      (future_eq_stable right orr) hi) _ x y h
  intro u v huv
  have hleft : ol u.1 = ol v.1 := future_eq_observes huv.1
  have hright : orr u.2 = orr v.2 := future_eq_observes huv.2
  rw [hleft, hright]

theorem joint_future_collision_excludes_decoder
    (step : L → I → Option L) (observe : L → A) (report : L → B)
    (x y : L) (same : report x = report y) (word : List I)
    (different : (run step (some x) word).map observe ≠
      (run step (some y) word).map observe) :
    ¬ ∃ decode : B → List I → Option A,
      ∀ s w, decode (report s) w = (run step (some s) w).map observe := by
  intro ⟨decode, law⟩
  apply different
  rw [← law x word, ← law y word, same]

def sign (b : Bool) : Int := if b then -1 else 1
def chsh (a0 a1 b0 b1 : Bool) : Int :=
  sign a0 * sign b0 + sign a0 * sign b1 + sign a1 * sign b0 - sign a1 * sign b1

theorem deterministic_chsh_bound (a0 a1 b0 b1 : Bool) : chsh a0 a1 b0 b1 ≤ 2 := by
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide

structure Preparation where
  weight : Int
  a0 : Bool
  a1 : Bool
  b0 : Bool
  b1 : Bool

def scoreSum : List Preparation → Int
  | [] => 0
  | p :: ps => p.weight * chsh p.a0 p.a1 p.b0 p.b1 + scoreSum ps
def massSum : List Preparation → Int
  | [] => 0
  | p :: ps => p.weight + massSum ps

-- Weights may be unnormalized integer masses. Dividing by a positive total
-- yields the usual S <= 2; rational scaling is outside this formal statement.
theorem shared_preparation_chsh (ps : List Preparation)
    (positive : ∀ p ∈ ps, 0 ≤ p.weight) : scoreSum ps ≤ 2 * massSum ps := by
  induction ps with
  | nil => decide
  | cons p ps ih =>
    have hp := positive p (by simp)
    have ht := ih (fun q hq => positive q (by simp [hq]))
    have hc := Int.mul_le_mul_of_nonneg_left (deterministic_chsh_bound p.a0 p.a1 p.b0 p.b1) hp
    have hh := Int.add_le_add hc ht
    simpa [scoreSum, massSum, Int.mul_add, Int.add_mul, Int.mul_comm] using hh

#print axioms product_stable
#print axioms paired_local_futures_suffice
#print axioms joint_future_collision_excludes_decoder
#print axioms deterministic_chsh_bound
#print axioms shared_preparation_chsh
end GenesisJointOperations
