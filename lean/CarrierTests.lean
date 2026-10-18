import ExactRat
import ShadowBoundary

/-!
Three distinct carrier tests. No Mathlib, custom axioms, or native_decide.
1. The existing general report-factorization theorem, instantiated with exact
   real qubit amplitudes and an available rational orthogonal control.
2. CHSH for arbitrary finite nonnegative rational joint weights, represented
   by natural numerators and a common denominator; a positive table violates it.
3. An all-ancilla central obstruction conditional on pure composite states
   occupying one central block. This premise is NOT derived from matrix
   extremality here. No universal operational reconstruction is mechanized.
AuthorityEffect: None.
-/
namespace QuantumCarrierTests
open ExactRat

def psi (negative : Bool) : QN × QN :=
  (QN.ofPair 3 5, if negative then QN.ofPair (-4) 5 else QN.ofPair 4 5)

def populations (v : QN × QN) : QN × QN := (v.1 * v.1, v.2 * v.2)
def rotate (v : QN × QN) : QN × QN :=
  (QN.ofPair 3 5 * v.1 + QN.ofPair 4 5 * v.2,
   QN.ofPair (-4) 5 * v.1 + QN.ofPair 3 5 * v.2)
def future (v : QN × QN) : QN := (rotate v).1 * (rotate v).1

theorem states_normalized : ∀ b : Bool,
    (populations (psi b)).1 + (populations (psi b)).2 = 1 := by decide

theorem control_orthogonal :
    QN.ofPair 3 5 * QN.ofPair 3 5 + QN.ofPair 4 5 * QN.ofPair 4 5 = 1 ∧
    QN.ofPair 3 5 * QN.ofPair (-4) 5 + QN.ofPair 4 5 * QN.ofPair 3 5 = 0 := by
  decide

theorem report_collision : populations (psi false) = populations (psi true) := by decide
theorem future_answers : future (psi false) = 1 ∧ future (psi true) = QN.ofPair 49 625 := by decide
theorem future_separates : future (psi false) ≠ future (psi true) := by decide

theorem no_population_decoder :
    ¬ ∃ decode : (QN × QN) → QN, ∀ b : Bool,
      decode (populations (psi b)) = future (psi b) :=
  SnSymbolGameAndPackets.no_factor_through_shadow_of_collision
    (fun b => populations (psi b)) (fun b => future (psi b))
    false true report_collision future_separates

theorem present_question_descends :
    ∃ decode : (QN × QN) → QN, ∀ b : Bool,
      decode (populations (psi b)) = (psi b).1 * (psi b).1 :=
  ⟨Prod.fst, fun _ => rfl⟩

structure Assignment where
  a0 : Bool
  a1 : Bool
  b0 : Bool
  b1 : Bool
deriving DecidableEq

def sign (b : Bool) : Int := if b then -1 else 1
def chsh (a : Assignment) : Int :=
  sign a.a0 * sign a.b0 + sign a.a0 * sign a.b1 +
  sign a.a1 * sign a.b0 - sign a.a1 * sign a.b1

theorem vertex_bound (a : Assignment) : chsh a = 2 ∨ chsh a = -2 := by
  rcases a with ⟨a,b,c,d⟩
  cases a <;> cases b <;> cases c <;> cases d <;> decide

def mass : List (Nat × Assignment) → Int
  | [] => 0
  | (w,_) :: xs => (w : Int) + mass xs
def score : List (Nat × Assignment) → Int
  | [] => 0
  | (w,a) :: xs => (w : Int) * chsh a + score xs

/-- Clearing a common positive denominator represents every finite rational
nonnegative joint distribution in this form. No bounded weight enumeration. -/
theorem weighted_chsh_bound (xs : List (Nat × Assignment)) :
    -2 * mass xs ≤ score xs ∧ score xs ≤ 2 * mass xs := by
  induction xs with
  | nil => simp [mass, score]
  | cons x xs ih =>
    rcases x with ⟨w,a⟩
    have hw : (0 : Int) ≤ (w : Int) := Int.natCast_nonneg w
    rcases vertex_bound a with hp | hn
    · simp only [mass, score, hp]
      omega
    · simp only [mass, score, hn]
      omega

/-- Entries of our rational Bell table, with denominator 20 and context order
00,01,10,11; outcome order ++,+-,-+,--. Every entry is strictly positive. -/
def bellNumerators : List (List Nat) :=
  [[9,1,1,9],[9,1,1,9],[8,2,2,8],[2,8,8,2]]
def correlate (row : List Nat) : Int :=
  Int.ofNat (row[0]?.getD 0) - Int.ofNat (row[1]?.getD 0) -
  Int.ofNat (row[2]?.getD 0) + Int.ofNat (row[3]?.getD 0)
def bellScore : Int := correlate [9,1,1,9] + correlate [9,1,1,9] +
  correlate [8,2,2,8] - correlate [2,8,8,2]

theorem bell_table_positive_normalized :
    bellNumerators.all (fun r => r.all (fun n => n > 0) && r.foldl (· + ·) 0 == 20) = true := by decide
theorem bell_score_exact : bellScore = 56 := by decide

/-- A positive joint extension would necessarily reproduce this CHSH value.
The marginal-to-score implication is not a hidden locality assumption: the
model being tested is explicitly one positive table of all four assignments. -/
theorem bell_has_no_positive_joint_score (xs : List (Nat × Assignment))
    (positiveMass : 0 < mass xs) : 20 * score xs ≠ bellScore * mass xs := by
  have bound := (weighted_chsh_bound xs).2
  rw [bell_score_exact]
  omega

def marginal (left right : Assignment → Bool) (u v : Bool) :
    List (Nat × Assignment) → Int
  | [] => 0
  | (w,a) :: xs =>
      (if left a = u ∧ right a = v then (w : Int) else 0) + marginal left right u v xs

def contextScore (left right : Assignment → Bool) : List (Nat × Assignment) → Int
  | [] => 0
  | (w,a) :: xs => (w : Int) * sign (left a) * sign (right a) + contextScore left right xs

theorem context_score_from_marginals (l r : Assignment → Bool)
    (xs : List (Nat × Assignment)) :
    contextScore l r xs = marginal l r false false xs - marginal l r false true xs -
      marginal l r true false xs + marginal l r true true xs := by
  induction xs with
  | nil => simp [contextScore, marginal]
  | cons x xs ih =>
    rcases x with ⟨w,a⟩
    cases hl : l a <;> cases hr : r a <;>
      simp [contextScore, marginal, sign, hl, hr] <;> omega

theorem score_from_contexts (xs : List (Nat × Assignment)) :
    score xs = contextScore Assignment.a0 Assignment.b0 xs +
      contextScore Assignment.a0 Assignment.b1 xs +
      contextScore Assignment.a1 Assignment.b0 xs -
      contextScore Assignment.a1 Assignment.b1 xs := by
  induction xs with
  | nil => simp [score, contextScore]
  | cons x xs ih =>
    rcases x with ⟨w,a⟩
    simp only [score, contextScore, chsh, Int.mul_add, Int.mul_sub, ← Int.mul_assoc]
    omega

def alice (setting : Bool) : Assignment → Bool :=
  if setting then Assignment.a1 else Assignment.a0
def bob (setting : Bool) : Assignment → Bool :=
  if setting then Assignment.b1 else Assignment.b0
def bellNumerator (x y u v : Bool) : Int :=
  if x then (if y then (if u = v then 2 else 8) else (if u = v then 8 else 2))
  else (if u = v then 9 else 1)

/-- Actual marginal matching, after clearing the joint table's positive mass
and the fixture's denominator 20. The numerators agree with bellNumerators. -/
def ExtendsBell (xs : List (Nat × Assignment)) : Prop :=
  ∀ x y u v : Bool, 20 * marginal (alice x) (bob y) u v xs =
    bellNumerator x y u v * mass xs

theorem bell_has_no_positive_joint_extension (xs : List (Nat × Assignment))
    (hm : 0 < mass xs) : ¬ ExtendsBell xs := by
  intro h
  have context (x y : Bool) :
      20 * contextScore (alice x) (bob y) xs =
        (bellNumerator x y false false - bellNumerator x y false true -
          bellNumerator x y true false + bellNumerator x y true true) * mass xs := by
    rw [context_score_from_marginals]
    have h00 := h x y false false
    have h01 := h x y false true
    have h10 := h x y true false
    have h11 := h x y true true
    simp only [Int.sub_mul, Int.add_mul]
    omega
  have h00 := context false false
  have h01 := context false true
  have h10 := context true false
  have h11 := context true true
  simp [alice, bob, bellNumerator] at h00 h01 h10 h11
  have hs := score_from_contexts xs
  have bound := (weighted_chsh_bound xs).2
  omega

/-- A pure state in the standard direct-sum tensor model occupies one joint
block. Internal quantum data may be arbitrary and the ancilla type arbitrary.
The structure records that model premise, not a proof of matrix extremality. -/
structure PureBlock (Sector Ancilla Internal : Type) where
  sector : Sector
  ancillaSector : Ancilla
  internal : Internal

def centralMass {S A I : Type} [DecidableEq S]
    (s : PureBlock S A I) (k : S) (denominator : Nat) : Nat :=
  if s.sector = k then denominator else 0

theorem pure_marginal_central_endpoint {S A I : Type} [DecidableEq S]
    (s : PureBlock S A I) (k : S) (d : Nat) :
    centralMass s k d = 0 ∨ centralMass s k d = d := by
  unfold centralMass
  split <;> simp_all

/-- A genuinely mixed central weight excludes every ancilla sector type and
every internal pure-block payload; no finite ancilla enumeration is used. -/
theorem central_mixture_has_no_pure_extension {S A I : Type} [DecidableEq S]
    (k : S) (numerator denominator : Nat)
    (hpos : 0 < numerator) (hmix : numerator < denominator) :
    ¬ ∃ s : PureBlock S A I, centralMass s k denominator = numerator := by
  intro ⟨s,h⟩
  have endpoint := pure_marginal_central_endpoint s k denominator
  omega

theorem fair_sector_mixture_obstructed {A I : Type} :
    ¬ ∃ s : PureBlock Bool A I, centralMass s false 2 = 1 :=
  central_mixture_has_no_pure_extension false 1 2 (by decide) (by decide)

theorem pure_sector_control :
    ∃ s : PureBlock Bool Unit Unit, centralMass s false 2 = 2 :=
  ⟨⟨false,(),()⟩,rfl⟩

#print axioms states_normalized
#print axioms control_orthogonal
#print axioms report_collision
#print axioms future_answers
#print axioms future_separates
#print axioms no_population_decoder
#print axioms present_question_descends
#print axioms vertex_bound
#print axioms weighted_chsh_bound
#print axioms bell_table_positive_normalized
#print axioms bell_score_exact
#print axioms bell_has_no_positive_joint_score
#print axioms context_score_from_marginals
#print axioms score_from_contexts
#print axioms bell_has_no_positive_joint_extension
#print axioms pure_marginal_central_endpoint
#print axioms central_mixture_has_no_pure_extension
#print axioms fair_sector_mixture_obstructed
#print axioms pure_sector_control
end QuantumCarrierTests
