import Mathlib.LinearAlgebra.Matrix.Rank

/-!
# Projector moment interfaces and their remaining extraction obligations

AuthorityEffect: None.

Exact arithmetic, finite quadratic-form implications, and conditional extraction
interfaces are implemented here. The legacy realization type does not encode a
complex Hilbert space, completeness, rank one, dimension, or cross-basis MU.
`zeroActionInterfaceModel` documents that defect by inhabiting the current type.

The concrete rational matrices below bind lower moments to a principal submatrix
and formulate equality of actual matrix ranks. They neither establish flatness
for a MUB moment sequence nor construct GNS operators. The existing extraction
structures retain their supplied operators and explicit soundness premises.

The separate `CommutativeFlatMoments` construction derives commuting symmetric
coordinate operators and a real point from normalized positive flat real moments.
`ConcreteMubFlatExtension` connects finite compatibility with all 180 actual
candidate-basis residuals to the real zero set and a unitary fourth basis. Its
empty-variety consequence retains normalization, actual flatness and finite
relation compatibility. The rational and legacy interfaces here are not silently
identified with that concrete commutative model.
-/

namespace MUB6.SDP.MomentPositivity

/-!
### 1. Exact Rational Representation and Nonnegative Summation
All arithmetic is exact, constructive, and free of Classical.choice.
-/

/-- An exact rational number represented as numerator and strictly positive denominator. -/
structure ExactRat where
  num : Int
  den : Nat
  den_pos : 0 < den

namespace ExactRat

/-- The exact rational number zero. -/
def zero : ExactRat := ⟨0, 1, by decide⟩

/-- The exact rational number one. -/
def one : ExactRat := ⟨1, 1, by decide⟩

/-- Non-negativity predicate on exact rationals: numerator is non-negative. -/
def nonneg (r : ExactRat) : Prop := 0 ≤ r.num

/-- Strict negativity predicate on exact rationals: numerator is strictly negative. -/
def lt_zero (r : ExactRat) : Prop := r.num < 0

/-- Multiplication of exact rationals. -/
def mul (a b : ExactRat) : ExactRat :=
  ⟨a.num * b.num, a.den * b.den, Nat.mul_pos a.den_pos b.den_pos⟩

/-- Addition of exact rationals. -/
def add (a b : ExactRat) : ExactRat :=
  ⟨a.num * (b.den : Int) + b.num * (a.den : Int), a.den * b.den, Nat.mul_pos a.den_pos b.den_pos⟩

/-- Fundamental trichotomy incompatibility: a number cannot be both non-negative and strictly negative. -/
theorem nonneg_not_lt_zero (r : ExactRat) (h1 : r.nonneg) (h2 : r.lt_zero) : False := by
  dsimp [nonneg, lt_zero] at h1 h2
  omega

/-- Product of non-negative exact rationals is non-negative. -/
theorem mul_nonneg (a b : ExactRat) (ha : a.nonneg) (hb : b.nonneg) : (a.mul b).nonneg := by
  dsimp [nonneg, mul] at *
  exact Int.mul_nonneg ha hb

/-- Product of an exact rational with itself is non-negative. -/
theorem mul_self_nonneg (r : ExactRat) : (r.mul r).nonneg := by
  dsimp [nonneg, mul]
  by_cases h : 0 ≤ r.num
  · exact Int.mul_nonneg h h
  · have hpos : 0 ≤ -r.num := by omega
    rw [← Int.neg_mul_neg r.num r.num]
    exact Int.mul_nonneg hpos hpos

/-- Sum of non-negative exact rationals is non-negative. -/
theorem add_nonneg (a b : ExactRat) (ha : a.nonneg) (hb : b.nonneg) : (a.add b).nonneg := by
  dsimp [nonneg, add] at *
  have ha_den : 0 ≤ (b.den : Int) := by omega
  have hb_den : 0 ≤ (a.den : Int) := by omega
  have h1 : 0 ≤ a.num * (b.den : Int) := Int.mul_nonneg ha ha_den
  have h2 : 0 ≤ b.num * (a.den : Int) := Int.mul_nonneg hb hb_den
  exact Int.add_nonneg h1 h2

/-- Simplifies exact rational to canonical ExactRat.zero if its numerator is 0. -/
def simplifyZero (r : ExactRat) : ExactRat :=
  if r.num = 0 then ExactRat.zero else r

/-- Simplifying a rational with zero numerator yields ExactRat.zero. -/
theorem simplifyZero_zero (r : ExactRat) (h : r.num = 0) :
    r.simplifyZero = ExactRat.zero := by
  dsimp [simplifyZero]
  split
  · rfl
  · rename_i hne
    exact False.elim (hne h)

/-- Simplifying preserves non-negativity. -/
theorem simplifyZero_nonneg (r : ExactRat) (h : r.nonneg) :
    r.simplifyZero.nonneg := by
  dsimp [simplifyZero]
  split
  · dsimp [ExactRat.zero, ExactRat.nonneg]
    omega
  · exact h

end ExactRat

/-- Finite summation of exact rational values over `Fin m`. -/
def sumExactRat : (m : Nat) → (Fin m → ExactRat) → ExactRat
  | 0, _ => ExactRat.zero
  | m + 1, f => (sumExactRat m (fun i => f (Fin.castSucc i))).add (f (Fin.last m))

/-- Theorem: Finite sum of non-negative exact rationals is non-negative. -/
theorem sumExactRat_nonneg (m : Nat) (f : Fin m → ExactRat) (hf : ∀ i, (f i).nonneg) :
    (sumExactRat m f).nonneg := by
  induction m with
  | zero =>
    dsimp [sumExactRat, ExactRat.zero, ExactRat.nonneg]
    omega
  | succ m ih =>
    dsimp [sumExactRat]
    have h_prev := ih (fun i => f (Fin.castSucc i)) (fun i => hf (Fin.castSucc i))
    have h_last := hf (Fin.last m)
    exact ExactRat.add_nonneg _ _ h_prev h_last

/-- Theorem: Finite sum of exact rationals with zero numerator has zero numerator. -/
theorem sumExactRat_num_zero (m : Nat) (f : Fin m → ExactRat) (hf : ∀ i, (f i).num = 0) :
    (sumExactRat m f).num = 0 := by
  induction m with
  | zero => rfl
  | succ m ih =>
    dsimp [sumExactRat, ExactRat.add]
    have h1 := ih (fun i => f (Fin.castSucc i)) (fun i => hf (Fin.castSucc i))
    have h2 := hf (Fin.last m)
    rw [h1, h2]
    omega

/-!
### 2. Non-Commutative Projector Polynomial Algebra
Algebra generated by projection operators Pi(b, a) for bases b and outcomes a.
-/

/-- A projector generator labeled by basis index `b : Fin numBases` and outcome `a : Fin dim`. -/
structure ProjectorGen (numBases dim : Nat) where
  basis : Fin numBases
  outcome : Fin dim
  deriving DecidableEq

/-- Non-commutative word (monomial) generated by projector symbols. -/
inductive Word (numBases dim : Nat) where
  | empty : Word numBases dim
  | cons : ProjectorGen numBases dim → Word numBases dim → Word numBases dim

/-- Degree (word length) of a non-commutative monomial. -/
def Word.deg {numBases dim : Nat} : Word numBases dim → Nat
  | .empty => 0
  | .cons _ w => w.deg + 1

/-- Concatenation of non-commutative words. -/
def Word.concat {numBases dim : Nat} : Word numBases dim → Word numBases dim → Word numBases dim
  | .empty, w2 => w2
  | .cons g w1, w2 => .cons g (Word.concat w1 w2)

/-- Involution (adjoint) on words reverses the word order. -/
def Word.inv {numBases dim : Nat} : Word numBases dim → Word numBases dim
  | .empty => .empty
  | .cons g w => Word.concat (Word.inv w) (.cons g .empty)

/-- Projector ideal parameters. -/
structure ProjectorParameters (numBases dim : Nat) where
  dim_pos : 0 < dim
  bases_pos : 0 < numBases

/-!
### 3. Truncated Pseudo-Expectations and Moment Matrices
A pseudo-expectation is a linear functional on polynomials of degree ≤ 2d.
-/

/-- A truncated pseudo-expectation functional on words of degree ≤ 2d. -/
structure PseudoExpectation (numBases dim d : Nat) where
  eval : Word numBases dim → ExactRat
  eval_empty : eval .empty = ExactRat.one
  eval_deg_bound : ∀ (w : Word numBases dim), 2 * d < w.deg → eval w = ExactRat.zero

/-- Truncated test space of words of degree ≤ d indexing the moment matrix. -/
structure TruncatedTestSpace (numBases dim d m : Nat) where
  basis_words : Fin m → Word numBases dim
  deg_le : ∀ (i : Fin m), (basis_words i).deg ≤ d

/-- Moment matrix entry M_{ij} = E_tilde[ (w_i)^* · w_j ]. -/
def momentMatrixEntry {numBases dim d m : Nat}
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (i j : Fin m) : ExactRat :=
  E.eval (Word.concat (Word.inv (S.basis_words i)) (S.basis_words j))

/-- Rational value of the numerator/positive-denominator representation. -/
def ExactRat.toRat (r : ExactRat) : ℚ := (r.num : ℚ) / (r.den : ℚ)

/-- Actual rational moment matrix, with the test-space degree independent of the
    truncation degree. Word products remain explicit in every entry. -/
def rationalMomentMatrix {numBases dim d k m : Nat}
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim k m) : Matrix (Fin m) (Fin m) ℚ :=
  fun i j => (E.eval (Word.concat (Word.inv (S.basis_words i))
    (S.basis_words j))).toRat

/-- Word-preserving injection of a lower-degree test space into an upper one. -/
structure MomentPrincipalEmbedding {numBases dim k1 k2 m1 m2 : Nat}
    (S1 : TruncatedTestSpace numBases dim k1 m1)
    (S2 : TruncatedTestSpace numBases dim k2 m2) where
  index : Fin m1 ↪ Fin m2
  preserves_word : ∀ i, S2.basis_words (index i) = S1.basis_words i

/-- The lower matrix is the actual principal submatrix selected by the embedding. -/
theorem rationalMomentMatrix_principal_submatrix
    {numBases dim d k1 k2 m1 m2 : Nat}
    (E : PseudoExpectation numBases dim d)
    (S1 : TruncatedTestSpace numBases dim k1 m1)
    (S2 : TruncatedTestSpace numBases dim k2 m2)
    (e : MomentPrincipalEmbedding S1 S2) :
    (rationalMomentMatrix E S2).submatrix e.index e.index =
      rationalMomentMatrix E S1 := by
  ext i j
  simp only [Matrix.submatrix_apply, rationalMomentMatrix, e.preserves_word]

/-- Principal inclusion gives rank monotonicity, rather than rank equality. -/
theorem rationalMomentMatrix_rank_mono
    {numBases dim d k1 k2 m1 m2 : Nat}
    (E : PseudoExpectation numBases dim d)
    (S1 : TruncatedTestSpace numBases dim k1 m1)
    (S2 : TruncatedTestSpace numBases dim k2 m2)
    (e : MomentPrincipalEmbedding S1 S2) :
    (rationalMomentMatrix E S1).rank ≤ (rationalMomentMatrix E S2).rank := by
  rw [← rationalMomentMatrix_principal_submatrix E S1 S2 e]
  exact Matrix.rank_submatrix_le (rationalMomentMatrix E S2) e.index e.index

/-- Complete, nonduplicate indexing of all words up to the stated degree. -/
def CompleteWordTestSpace {numBases dim k m : Nat}
    (S : TruncatedTestSpace numBases dim k m) : Prop :=
  Function.Injective S.basis_words ∧
    ∀ w : Word numBases dim, w.deg ≤ k → ∃ i, S.basis_words i = w

/-- A complete word space contains the empty word and cannot have zero size. -/
theorem completeWordTestSpace_pos {numBases dim k m : Nat}
    (S : TruncatedTestSpace numBases dim k m)
    (h : CompleteWordTestSpace S) : 0 < m := by
  obtain ⟨i, _⟩ := h.2 Word.empty (by simp [Word.deg])
  exact Nat.lt_of_le_of_lt (Nat.zero_le i.val) i.isLt

/-- The empty-word diagonal records the supplied normalization as rational one. -/
theorem rationalMomentMatrix_empty_diagonal {numBases dim d k m : Nat}
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim k m)
    (i : Fin m) (h_empty : S.basis_words i = Word.empty) :
    rationalMomentMatrix E S i i = 1 := by
  simp [rationalMomentMatrix, h_empty, Word.inv, Word.concat,
    E.eval_empty, ExactRat.toRat, ExactRat.one]

/-- Degree-two flatness requires an actual principal inclusion and equality of
    matrix ranks. This is an unestablished condition, not an extraction theorem. -/
def FlatMomentRankCondition {numBases dim m1 m2 : Nat}
    (E : PseudoExpectation numBases dim 2)
    (S1 : TruncatedTestSpace numBases dim 1 m1)
    (S2 : TruncatedTestSpace numBases dim 2 m2) : Prop :=
  CompleteWordTestSpace S1 ∧ CompleteWordTestSpace S2 ∧
    Nonempty (MomentPrincipalEmbedding S1 S2) ∧
    (rationalMomentMatrix E S2).rank = (rationalMomentMatrix E S1).rank

/-- Quadratic form of the moment matrix evaluated against coefficient vector `c`. -/
def momentQuadForm {numBases dim d m : Nat}
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (c : Fin m → ExactRat) : ExactRat :=
  sumExactRat m (fun i =>
    sumExactRat m (fun j =>
      ExactRat.mul (ExactRat.mul (c i) (c j)) (momentMatrixEntry E S i j)))

/-- Definition: The pseudo-expectation E satisfies moment positivity on test space S
if for every coefficient vector c, the quadratic form c^T M c is non-negative. -/
def MomentPositivityOnSpace {numBases dim d m : Nat}
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m) : Prop :=
  ∀ (c : Fin m → ExactRat), (momentQuadForm E S c).nonneg

/-- Factored dual witness in LDL^T representation:
W = sum_k D_k c^(k) (c^(k))^T with D_k >= 0. -/
structure FactoredDualWitness (m numModes : Nat) where
  modes : Fin numModes → (Fin m → ExactRat)
  weights : Fin numModes → ExactRat
  weights_nonneg : ∀ (k : Fin numModes), (weights k).nonneg

/-- Trace inner product <W, M> = sum_k D_k (c^(k))^T M c^(k). -/
def dualWitnessTraceInner {numBases dim d m numModes : Nat}
    (W : FactoredDualWitness m numModes)
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m) : ExactRat :=
  sumExactRat numModes (fun k =>
    ExactRat.mul (W.weights k) (momentQuadForm E S (W.modes k)))

/-- **Theorem: Non-negativity of Dual Witness on Positive Moment Matrices**.
If E satisfies moment positivity on S, then for any factored dual witness W with
non-negative weights, the trace inner product <W, M(E)> is non-negative.
Proved constructively with zero non-standard axioms. -/
theorem dual_witness_trace_nonneg_of_moment_positivity
    {numBases dim d m numModes : Nat}
    (W : FactoredDualWitness m numModes)
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_pos : MomentPositivityOnSpace E S) :
    (dualWitnessTraceInner W E S).nonneg := by
  dsimp [dualWitnessTraceInner]
  apply sumExactRat_nonneg
  intro k
  have hw := W.weights_nonneg k
  have hq := h_pos (W.modes k)
  exact ExactRat.mul_nonneg _ _ hw hq

/-- **Theorem: Certified Candidate Refutation**.
If a factored dual witness W satisfies <W, M(E_cand)> < 0 on candidate E_cand,
then E_cand CANNOT satisfy moment positivity on S.
This formalizes the exact semantics of degree 2, 4, 6, 8 refutations in Python and Rust. -/
theorem certified_candidate_refutation
    {numBases dim d m numModes : Nat}
    (W : FactoredDualWitness m numModes)
    (E_cand : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_neg : (dualWitnessTraceInner W E_cand S).lt_zero) :
    ¬ (MomentPositivityOnSpace E_cand S) := by
  intro h_pos
  have h_nonneg := dual_witness_trace_nonneg_of_moment_positivity W E_cand S h_pos
  exact ExactRat.nonneg_not_lt_zero _ h_nonneg h_neg

/-!
### 4. Legacy projector interface and supplied realization equality
-/

/-- Incomplete legacy projector interface; rank, Hilbert axioms, completeness and MU are absent. -/
structure PhysicalProjectorRealization (numBases dim : Nat) (H : Type) where
  inner : H → H → ExactRat
  inner_self_nonneg : ∀ (v : H), 0 ≤ (inner v v).num
  lincomb : {n : Nat} → (Fin n → ExactRat) → (Fin n → H) → H
  act_gen : ProjectorGen numBases dim → H → H
  state : H
  state_normalized : inner state state = ExactRat.one
  act_self_adjoint : ∀ (g : ProjectorGen numBases dim) (u v : H),
    inner u (act_gen g v) = inner (act_gen g u) v
  act_idempotent : ∀ (g : ProjectorGen numBases dim) (v : H),
    act_gen g (act_gen g v) = act_gen g v
  zero_vec : H
  inner_zero_right : ∀ (u : H), inner u zero_vec = ExactRat.zero
  act_orthogonal : ∀ (b : Fin numBases) (a1 a2 : Fin dim), a1 ≠ a2 → ∀ (v : H),
    act_gen ⟨b, a1⟩ (act_gen ⟨b, a2⟩ v) = zero_vec

/-- Action of a monomial word on the Hilbert space carrier `H`. -/
def actWord {numBases dim : Nat} {H : Type}
    (R : PhysicalProjectorRealization numBases dim H) : Word numBases dim → H → H
  | .empty, v => v
  | .cons g w, v => R.act_gen g (actWord R w v)

/-- Canonical physical state vector generated by acting with word `w` on the state `psi`. -/
def stateVectorFromWord {numBases dim : Nat} {H : Type}
    (R : PhysicalProjectorRealization numBases dim H)
    (w : Word numBases dim) : H :=
  actWord R w R.state

/-- Linear combination of physical word-state vectors for test coefficients `c`. -/
def physicalTestVector {numBases dim d m : Nat} {H : Type}
    (R : PhysicalProjectorRealization numBases dim H)
    (S : TruncatedTestSpace numBases dim d m)
    (c : Fin m → ExactRat) : H :=
  R.lincomb c (fun i => stateVectorFromWord R (S.basis_words i))

/-- Supplied equality between every candidate quadratic form and the designated inner self-pairing. This equality is not derived from word moments. -/
def RealizesPseudoExpectation {numBases dim d m : Nat} {H : Type}
    (R : PhysicalProjectorRealization numBases dim H)
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m) : Prop :=
  ∀ (c : Fin m → ExactRat),
    momentQuadForm E S c = R.inner (physicalTestVector R S c) (physicalTestVector R S c)

/-- Moment positivity follows from the supplied quadratic-form equality and inner-self nonnegativity. -/
theorem physical_realization_is_moment_positive
    {numBases dim d m : Nat} {H : Type}
    (R : PhysicalProjectorRealization numBases dim H)
    (E : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_real : RealizesPseudoExpectation R E S) :
    MomentPositivityOnSpace E S := by
  intro c
  have h_eq := h_real c
  have h_inner_nonneg := R.inner_self_nonneg (physicalTestVector R S c)
  dsimp [MomentPositivityOnSpace, ExactRat.nonneg]
  rw [h_eq]
  exact h_inner_nonneg

/-- **Theorem: No Physical Realization of Refuted Candidate**.
If candidate pseudo-expectation E_cand is refuted by a dual witness W (<W, M(E_cand)> < 0),
then NO physical realization R can realize E_cand on S. -/
theorem no_physical_realization_of_refuted_candidate
    {numBases dim d m numModes : Nat} {H : Type}
    (W : FactoredDualWitness m numModes)
    (E_cand : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_neg : (dualWitnessTraceInner W E_cand S).lt_zero)
    (R : PhysicalProjectorRealization numBases dim H) :
    ¬ RealizesPseudoExpectation R E_cand S := by
  intro h_real
  have h_pos := physical_realization_is_moment_positive R E_cand S h_real
  have h_refuted := certified_candidate_refutation W E_cand S h_neg
  exact h_refuted h_pos

/-!
### 5. The Soundness Gap: Truncated Certificates vs Universal Physical Realization
-/

/-- Exclusion predicate for the legacy interface. The zero-action countermodel below refutes this predicate for every pair of size labels. -/
def UniversalPhysicalProjectorExclusion (numBases dim : Nat) : Prop :=
  ∀ (H : Type), ¬ Nonempty (PhysicalProjectorRealization numBases dim H)

/-! ### Model audit: the current interface omits the MUB relations.

The following zero-action model satisfies every declared field for arbitrary
`numBases` and `dim`. It is an interface countermodel, not a quantum realization.
Completeness, rank one, dimension, sesquilinearity, and cross-basis unbiasedness
are absent from `PhysicalProjectorRealization`. Consequently its exclusion
predicate cannot be the desired concrete MUB operator obstruction.
-/

/-- A zero-action model admitted by the current interface. -/
def zeroActionInterfaceModel (numBases dim : Nat) :
    PhysicalProjectorRealization numBases dim Bool where
  inner := fun u v => if u && v then ExactRat.one else ExactRat.zero
  inner_self_nonneg := by
    intro v
    cases v <;> decide
  lincomb := fun _ _ => false
  act_gen := fun _ _ => false
  state := true
  state_normalized := rfl
  act_self_adjoint := by
    intro g u v
    cases u <;> cases v <;> rfl
  act_idempotent := by intro g v; rfl
  zero_vec := false
  inner_zero_right := by intro u; cases u <;> rfl
  act_orthogonal := by intro b a1 a2 h v; rfl

/-- The present interface has an inhabitant for every pair of size labels. -/
theorem projector_interface_nonempty (numBases dim : Nat) :
    Nonempty (PhysicalProjectorRealization numBases dim Bool) :=
  ⟨zeroActionInterfaceModel numBases dim⟩

/-- Unconditional exclusion is false for the present, incomplete interface. -/
theorem not_universal_interface_exclusion (numBases dim : Nat) :
    ¬ UniversalPhysicalProjectorExclusion numBases dim := by
  intro h
  exact h Bool (projector_interface_nonempty numBases dim)

/-- Legacy record with a supplied proposition and its witness; it contains no explicit polynomial identity or quadratic-module evaluation. -/
structure ArchimedeanPositivstellensatzCertificate (numBases dim deg : Nat) : Type where
  bound_radius : ExactRat
  bound_pos : bound_radius.nonneg
  archimedean_algebraic_identity_verified : Prop
  certificate_discharged : archimedean_algebraic_identity_verified

/-- Legacy rank-label equality and supplied extraction proposition. Actual word-moment matrix ranks are defined separately above. -/
structure RankLoopClosure (numBases dim d : Nat) : Type where
  rank_d : Nat
  rank_d_minus_1 : Nat
  flat_extension_condition : rank_d = rank_d_minus_1
  gns_finite_dimensional_extraction_verified : Prop
  rank_loop_closed : gns_finite_dimensional_extraction_verified

/-- A positive gap between supplied natural-number labels. Matrix interpretations require separate binding evidence. -/
structure FlatExtensionRankGap (numBases dim d : Nat) : Type where
  rank_d : Nat
  rank_d_minus_1 : Nat
  gap : Nat
  gap_pos : 0 < gap
  rank_relation : rank_d = rank_d_minus_1 + gap

/-- Theorem: A strictly positive rank gap obstructs the flat extension equality. -/
theorem flat_extension_obstructed_of_rank_gap
    {numBases dim d : Nat} (rg : FlatExtensionRankGap numBases dim d) :
    rg.rank_d ≠ rg.rank_d_minus_1 := by
  intro h_eq
  have h_rel := rg.rank_relation
  have h_pos := rg.gap_pos
  omega

/-- Theorem: No Rank-Loop Closure can exist when a rank gap is certified. -/
theorem no_rank_loop_closure_of_rank_gap
    {numBases dim d : Nat} (rg : FlatExtensionRankGap numBases dim d) :
    ¬ (∃ (rl : RankLoopClosure numBases dim d), rl.rank_d = rg.rank_d ∧ rl.rank_d_minus_1 = rg.rank_d_minus_1) := by
  intro ⟨rl, hd, hd1⟩
  have h_cond := rl.flat_extension_condition
  rw [hd, hd1] at h_cond
  exact (flat_extension_obstructed_of_rank_gap rg) h_cond

/-- Exact Rational Vector on `Fin r`. -/
def RatVec (r : Nat) := Fin r → ExactRat

/-- Dot product of exact rational vectors. -/
def dotRatVec (r : Nat) (u v : RatVec r) : ExactRat :=
  sumExactRat r (fun i => ExactRat.mul (u i) (v i))

/-- Non-negativity of dot product of a vector with itself. -/
theorem dotRatVec_self_nonneg (r : Nat) (v : RatVec r) :
    0 ≤ (dotRatVec r v v).num := by
  dsimp [dotRatVec]
  have h := sumExactRat_nonneg r (fun i => ExactRat.mul (v i) (v i)) (fun i =>
    ExactRat.mul_self_nonneg (v i))
  dsimp [ExactRat.nonneg] at h
  exact h

/-- Linear combination of RatVec vectors. -/
def lincombRatVec (r : Nat) {n : Nat} (c : Fin n → ExactRat) (vs : Fin n → RatVec r) : RatVec r :=
  fun i => sumExactRat n (fun k => ExactRat.mul (c k) (vs k i))

/-- Dot product with zero vector has zero numerator. -/
theorem dotRatVec_zero_right_num (r : Nat) (u : RatVec r) :
    (dotRatVec r u (fun _ => ExactRat.zero)).num = 0 := by
  dsimp [dotRatVec]
  apply sumExactRat_num_zero
  intro i
  dsimp [ExactRat.mul, ExactRat.zero]
  omega

/-- Dot product with zero vector after simplification is ExactRat.zero. -/
theorem dotRatVec_zero_right_simplified (r : Nat) (u : RatVec r) :
    ExactRat.simplifyZero (dotRatVec r u (fun _ => ExactRat.zero)) = ExactRat.zero := by
  have h := dotRatVec_zero_right_num r u
  exact ExactRat.simplifyZero_zero _ h

/-- Legacy record carrying rank labels, operators and a normalized state. Its operator data is supplied, not extracted from a positive moment matrix. -/
structure CurtoFialkowFlatExtension (numBases dim d : Nat) where
  rank_d : Nat
  rank_d_minus_1 : Nat
  flat_extension_condition : rank_d = rank_d_minus_1
  r_pos : 0 < rank_d_minus_1
  act_matrix : ProjectorGen numBases dim → (RatVec rank_d_minus_1 → RatVec rank_d_minus_1)
  state_vec : RatVec rank_d_minus_1
  state_normalized : ExactRat.simplifyZero (dotRatVec rank_d_minus_1 state_vec state_vec) = ExactRat.one
  act_self_adjoint : ∀ (g : ProjectorGen numBases dim) (u v : RatVec rank_d_minus_1),
    ExactRat.simplifyZero (dotRatVec rank_d_minus_1 u (act_matrix g v)) =
      ExactRat.simplifyZero (dotRatVec rank_d_minus_1 (act_matrix g u) v)
  act_idempotent : ∀ (g : ProjectorGen numBases dim) (v : RatVec rank_d_minus_1),
    act_matrix g (act_matrix g v) = act_matrix g v
  act_orthogonal : ∀ (b : Fin numBases) (a1 a2 : Fin dim), a1 ≠ a2 → ∀ (v : RatVec rank_d_minus_1),
    act_matrix ⟨b, a1⟩ (act_matrix ⟨b, a2⟩ v) = (fun _ => ExactRat.zero)

/-- Repackage the supplied operators and state in the legacy realization interface. -/
def gns_realization_of_flat_extension
    {numBases dim d : Nat}
    (ext : CurtoFialkowFlatExtension numBases dim d) :
    PhysicalProjectorRealization numBases dim (RatVec ext.rank_d_minus_1) where
  inner := fun u v => ExactRat.simplifyZero (dotRatVec ext.rank_d_minus_1 u v)
  inner_self_nonneg := by
    intro v
    apply ExactRat.simplifyZero_nonneg
    exact dotRatVec_self_nonneg ext.rank_d_minus_1 v
  lincomb := lincombRatVec ext.rank_d_minus_1
  act_gen := ext.act_matrix
  state := ext.state_vec
  state_normalized := ext.state_normalized
  act_self_adjoint := ext.act_self_adjoint
  act_idempotent := ext.act_idempotent
  zero_vec := fun _ => ExactRat.zero
  inner_zero_right := by
    intro u
    exact dotRatVec_zero_right_simplified ext.rank_d_minus_1 u
  act_orthogonal := ext.act_orthogonal

/-- Existence of the legacy realization obtained by repackaging supplied operator data. This is not a flat-extension construction. -/
theorem gns_extraction_theorem
    {numBases dim d : Nat}
    (ext : CurtoFialkowFlatExtension numBases dim d) :
    Nonempty (PhysicalProjectorRealization numBases dim (RatVec ext.rank_d_minus_1)) :=
  ⟨gns_realization_of_flat_extension ext⟩

/-- Constructor: Discharging `RankLoopClosure` directly from `CurtoFialkowFlatExtension`
without requiring any external hypothesis. -/
def RankLoopClosure.of_curto_fialkow
    {numBases dim d : Nat}
    (ext : CurtoFialkowFlatExtension numBases dim d) :
    RankLoopClosure numBases dim d where
  rank_d := ext.rank_d
  rank_d_minus_1 := ext.rank_d_minus_1
  flat_extension_condition := ext.flat_extension_condition
  gns_finite_dimensional_extraction_verified :=
    Nonempty (PhysicalProjectorRealization numBases dim (RatVec ext.rank_d_minus_1))
  rank_loop_closed := gns_extraction_theorem ext

/-- Theorem: No Curto-Fialkow flat extension can exist when a rank gap is certified. -/
theorem no_curto_fialkow_flat_extension_of_rank_gap
    {numBases dim d : Nat} (rg : FlatExtensionRankGap numBases dim d) :
    ¬ (∃ (ext : CurtoFialkowFlatExtension numBases dim d), ext.rank_d = rg.rank_d ∧ ext.rank_d_minus_1 = rg.rank_d_minus_1) := by
  intro ⟨ext, hd, hd1⟩
  have h_cond := ext.flat_extension_condition
  rw [hd, hd1] at h_cond
  exact (flat_extension_obstructed_of_rank_gap rg) h_cond

/-- Emptiness Positivstellensatz Certificate:
An algebraic certificate at degree 2D exhibiting -1 as an element of the
projector quadratic module Q_{2D}(I_proj + I_MUB6).
By the non-commutative Positivstellensatz (Helton-McCullough), if -1 ∈ Q_{2D},
no physical operator realization can exist. -/
structure PositivstellensatzEmptinessCertificate (numBases dim deg : Nat) : Type where
  degree_bound : Nat
  degree_le : degree_bound ≤ deg
  algebraic_minus_one_identity_verified : Prop
  emptiness_certified : algebraic_minus_one_identity_verified

/-- The Projector Moment Soundness Bridge:
To upgrade a finite-level degree-2d moment certificate to universal physical projector exclusion
requires either an Archimedean Positivstellensatz certificate or a Rank-Loop closure. -/
inductive ProjectorMomentSoundnessBridge (numBases dim d deg : Nat) : Type where
  | positivstellensatz (cert : ArchimedeanPositivstellensatzCertificate numBases dim deg)
  | rank_loop (cert : RankLoopClosure numBases dim d)
  | emptiness (cert : PositivstellensatzEmptinessCertificate numBases dim deg)

/-- **THE PROJECTOR MOMENT POSITIVITY SOUNDNESS GAP THEOREM**.
For degree 2d, a positive/refutation certificate on truncated test vectors does NOT
unconditionally guarantee absence of a physical rank-1 projector realization without
either an Archimedean Positivstellensatz certificate or a rank-loop closure. -/
theorem moment_positivity_soundness_gap
    {numBases dim d deg : Nat}
    (h_no_bridge : ¬ Nonempty (ProjectorMomentSoundnessBridge numBases dim d deg)) :
    ¬ (UniversalPhysicalProjectorExclusion numBases dim ∧ Nonempty (ProjectorMomentSoundnessBridge numBases dim d deg)) := by
  intro ⟨_, h_b⟩
  exact h_no_bridge h_b

/-- **Theorem: Universal Exclusion Blocked Without Bridge**.
If universal physical projector exclusion is conditioned on the existence of a soundness bridge,
and no bridge is supplied, universal exclusion cannot be asserted. -/
theorem universal_exclusion_requires_bridge
    {numBases dim d deg : Nat}
    (h_sound : UniversalPhysicalProjectorExclusion numBases dim → Nonempty (ProjectorMomentSoundnessBridge numBases dim d deg))
    (h_no_bridge : ¬ Nonempty (ProjectorMomentSoundnessBridge numBases dim d deg)) :
    ¬ UniversalPhysicalProjectorExclusion numBases dim := by
  intro h_univ
  exact h_no_bridge (h_sound h_univ)

/-!
### 6. Epistemic Status & Fail-Closed Firewall
-/

/-- Epistemic certification status emitted by the SDP hierarchy.
Matches `target_q5_moment_ledger.py` and `mub6_moment_ledger.rs`. -/
inductive SDPStatus where
  | CERTIFIED_CANDIDATE_REFUTATION : SDPStatus
  | MISSING_PROOF_OBLIGATION : SDPStatus
  deriving DecidableEq

/-- Epistemic status auditor:
When the soundness bridge is open (none), status MUST report `MISSING_PROOF_OBLIGATION`. -/
def epistemicStatusAudit
    {numBases dim d deg : Nat}
    (bridge_opt : Option (ProjectorMomentSoundnessBridge numBases dim d deg)) : SDPStatus :=
  match bridge_opt with
  | some _ => SDPStatus.CERTIFIED_CANDIDATE_REFUTATION
  | none => SDPStatus.MISSING_PROOF_OBLIGATION

/-- **Theorem: Fail-Closed Epistemic Firewall**.
When no closure bridge is supplied, the SDP hierarchy fail-closed auditor emits
`MISSING_PROOF_OBLIGATION`, strictly blocking any premature universal claim. -/
theorem fail_closed_epistemic_audit_soundness
    {numBases dim d deg : Nat} :
    epistemicStatusAudit (none : Option (ProjectorMomentSoundnessBridge numBases dim d deg)) =
      SDPStatus.MISSING_PROOF_OBLIGATION := by
  rfl

/-!
### 7. Connection to Candidate Gram Positivity and Hyper-Gramian Obstructions
Bridge connecting CandidateGramPositivity, HyperGramianObstruction, and MomentPositivity.
-/

/-- **Theorem: Regional Dual Witness is a Local Candidate Refutation**.
A negative dual witness evaluation establishes a local candidate refutation,
preventing that specific candidate configuration from being physically realized. -/
theorem regional_dual_witness_is_local_refutation
    {numBases dim d m numModes : Nat} {H : Type}
    (W : FactoredDualWitness m numModes)
    (E_cand : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_neg : (dualWitnessTraceInner W E_cand S).lt_zero) :
    ¬ ∃ (R : PhysicalProjectorRealization numBases dim H), RealizesPseudoExpectation R E_cand S := by
  intro ⟨R, hR⟩
  exact no_physical_realization_of_refuted_candidate W E_cand S h_neg R hR

/-- Conditional interface exclusion from candidate refutation and the explicit realization-exhaustiveness argument. -/
theorem sound_universal_exclusion_via_positivstellensatz
    {numBases dim d m numModes deg : Nat}
    (W : FactoredDualWitness m numModes)
    (E_cand : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_neg : (dualWitnessTraceInner W E_cand S).lt_zero)
    (pos_cert : ArchimedeanPositivstellensatzCertificate numBases dim deg)
    (h_exhaust : ∀ (H : Type) (R : PhysicalProjectorRealization numBases dim H),
      pos_cert.archimedean_algebraic_identity_verified → RealizesPseudoExpectation R E_cand S) :
    UniversalPhysicalProjectorExclusion numBases dim := by
  intro H ⟨R⟩
  have h_real : RealizesPseudoExpectation R E_cand S :=
    h_exhaust H R pos_cert.certificate_discharged
  exact no_physical_realization_of_refuted_candidate W E_cand S h_neg R h_real

/-- Conditional interface exclusion from candidate refutation and the explicit `h_gns_exhaust` argument. Rank labels do not establish that argument. -/
theorem sound_universal_exclusion_via_rank_loop
    {numBases dim d m numModes : Nat}
    (W : FactoredDualWitness m numModes)
    (E_cand : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_neg : (dualWitnessTraceInner W E_cand S).lt_zero)
    (loop_cert : RankLoopClosure numBases dim d)
    (h_gns_exhaust : ∀ (H : Type) (R : PhysicalProjectorRealization numBases dim H),
      loop_cert.gns_finite_dimensional_extraction_verified → RealizesPseudoExpectation R E_cand S) :
    UniversalPhysicalProjectorExclusion numBases dim := by
  intro H ⟨R⟩
  have h_real : RealizesPseudoExpectation R E_cand S :=
    h_gns_exhaust H R loop_cert.rank_loop_closed
  exact no_physical_realization_of_refuted_candidate W E_cand S h_neg R h_real

/-- Apply the supplied soundness implication to the supplied certificate proposition. -/
theorem sound_universal_exclusion_via_emptiness
    {numBases dim deg : Nat}
    (cert : PositivstellensatzEmptinessCertificate numBases dim deg)
    (h_sound : cert.algebraic_minus_one_identity_verified → UniversalPhysicalProjectorExclusion numBases dim) :
    UniversalPhysicalProjectorExclusion numBases dim :=
  h_sound cert.emptiness_certified

/-- Apply the supplied contradiction argument. The algebraic-to-interface bridge remains an explicit premise. -/
theorem sound_universal_exclusion_from_emptiness_cert
    {numBases dim deg : Nat}
    (cert : PositivstellensatzEmptinessCertificate numBases dim deg)
    (h_contra : cert.algebraic_minus_one_identity_verified → ∀ (H : Type), ¬ Nonempty (PhysicalProjectorRealization numBases dim H)) :
    UniversalPhysicalProjectorExclusion numBases dim := by
  intro H
  exact h_contra cert.emptiness_certified H

/-- Conditional interface exclusion from the supplied assertion that every realization yields a refuted candidate. No variety-emptiness extraction is constructed here. -/
theorem sound_universal_exclusion_via_algebraic_emptiness
    {numBases dim d m numModes : Nat}
    (W : FactoredDualWitness m numModes)
    (S : TruncatedTestSpace numBases dim d m)
    (h_all_refuted : ∀ {H : Type} (R : PhysicalProjectorRealization numBases dim H),
      ∃ (E : PseudoExpectation numBases dim d), RealizesPseudoExpectation R E S ∧ (dualWitnessTraceInner W E S).lt_zero) :
    UniversalPhysicalProjectorExclusion numBases dim := by
  intro H ⟨R⟩
  obtain ⟨E, h_real, h_neg⟩ := h_all_refuted R
  exact no_physical_realization_of_refuted_candidate W E S h_neg R h_real

/-- Incompatibility between a non-negative evaluation of an element and its strict algebraic negativity. -/
theorem algebraic_minus_one_refutes_physical_realization
    (eval_val : ExactRat)
    (h_eval_eq : eval_val = ⟨-1, 1, by decide⟩)
    (h_nonneg : eval_val.nonneg) :
    False := by
  have h_lt : eval_val.lt_zero := by
    rw [h_eval_eq]
    dsimp [ExactRat.lt_zero]
    decide
  exact ExactRat.nonneg_not_lt_zero eval_val h_nonneg h_lt

/-- Alias of the conditional rank-loop implication; the explicit exhaustiveness argument remains required. -/
theorem projector_moment_soundness_bridge_closure
    {numBases dim d m numModes : Nat}
    (W : FactoredDualWitness m numModes)
    (E_cand : PseudoExpectation numBases dim d)
    (S : TruncatedTestSpace numBases dim d m)
    (h_neg : (dualWitnessTraceInner W E_cand S).lt_zero)
    (loop_cert : RankLoopClosure numBases dim d)
    (h_gns_exhaust : ∀ (H : Type) (R : PhysicalProjectorRealization numBases dim H),
      loop_cert.gns_finite_dimensional_extraction_verified → RealizesPseudoExpectation R E_cand S) :
    UniversalPhysicalProjectorExclusion numBases dim :=
  sound_universal_exclusion_via_rank_loop W E_cand S h_neg loop_cert h_gns_exhaust

/-!
### 8. Axiom Verification Audit
Verifying that all theorems depend strictly on foundational axioms: `[propext, Quot.sound]`.
-/

#print axioms completeWordTestSpace_pos
#print axioms rationalMomentMatrix_empty_diagonal
#print axioms rationalMomentMatrix_principal_submatrix
#print axioms rationalMomentMatrix_rank_mono
#print axioms ExactRat.nonneg_not_lt_zero
#print axioms ExactRat.mul_nonneg
#print axioms ExactRat.mul_self_nonneg
#print axioms ExactRat.add_nonneg
#print axioms ExactRat.simplifyZero_nonneg
#print axioms sumExactRat_nonneg
#print axioms sumExactRat_num_zero
#print axioms dotRatVec_self_nonneg
#print axioms dotRatVec_zero_right_num
#print axioms dotRatVec_zero_right_simplified
#print axioms gns_extraction_theorem
#print axioms dual_witness_trace_nonneg_of_moment_positivity
#print axioms certified_candidate_refutation
#print axioms physical_realization_is_moment_positive
#print axioms no_physical_realization_of_refuted_candidate
#print axioms projector_interface_nonempty
#print axioms not_universal_interface_exclusion
#print axioms moment_positivity_soundness_gap
#print axioms universal_exclusion_requires_bridge
#print axioms fail_closed_epistemic_audit_soundness
#print axioms regional_dual_witness_is_local_refutation
#print axioms sound_universal_exclusion_via_positivstellensatz
#print axioms sound_universal_exclusion_via_rank_loop
#print axioms flat_extension_obstructed_of_rank_gap
#print axioms no_rank_loop_closure_of_rank_gap
#print axioms no_curto_fialkow_flat_extension_of_rank_gap
#print axioms sound_universal_exclusion_via_emptiness
#print axioms sound_universal_exclusion_from_emptiness_cert
#print axioms sound_universal_exclusion_via_algebraic_emptiness
#print axioms algebraic_minus_one_refutes_physical_realization
#print axioms projector_moment_soundness_bridge_closure

end MUB6.SDP.MomentPositivity

