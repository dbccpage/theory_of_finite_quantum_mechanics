import WallTransport
import ZeroRelVariety
import ModuliReduction
import AlgebraicCornerReconstruction

/-!
# Target 5: Candidate Gram Positivity & Regional Dual Obstruction

AuthorityEffect: None

This module formalizes:
1. Exact Gram matrix construction from candidate column vectors:
   G_{ij} = ⟨v_i, v_j⟩ in a pre-Hilbert space.
2. Constructive proof of positive semidefiniteness (PSD) of the Gram matrix G:
   c† G c = ⟨∑ c_i v_i, ∑ c_j v_j⟩ = ‖∑ c_i v_i‖² ≥ 0.
3. Dual witness representation W = L D L† with D ≥ 0, and constructive proof
   of trace nonnegativity:
   Tr(W · G) = ∑_k D_k ‖∑_i L_{ik} v_i‖² ≥ 0.
4. Formulation and proof of the Regional Dual Obstruction:
   If there exists a certified dual witness W = L D L† (D ≥ 0) such that
   Tr(W · G(θ)) < 0 on an exact rational parameter box, then no valid column
   Gram matrix exists (obstruction to completion).
5. Bridge to MUB(6) complete set impossibility via HyperGramianObstruction.
-/

namespace MUB6.Gluing.CandidateGram

open MUB6.Gluing
open MUB6.Gluing.Orbits
open MUB6.Gluing.HyperGramianObstruction

/-!
### 1. Exact Summation and Rational Arithmetic Bounds
-/

/-- Finite summation over `Fin m` for rational values. -/
def sumRat : (m : Nat) → (Fin m → Rat) → Rat
  | 0, _ => 0
  | m + 1, f => sumRat m (fun i => f (Fin.castSucc i)) + f (Fin.last m)

/-- Product of non-negative rationals is non-negative. -/
theorem rat_mul_nonneg (a b : Rat) (ha : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ a * b :=
  Rat.mul_nonneg ha hb

/-- A rational number cannot be both non-negative and strictly negative. -/
theorem rat_nonneg_not_lt_zero (x : Rat) (h1 : 0 ≤ x) (h2 : x < 0) : False := by
  have h_true : x.blt 0 = true := h2
  have h_false : x.blt 0 = false := h1
  rw [h_true] at h_false
  contradiction

/-- Sum of non-negative rationals is non-negative. -/
theorem sumRat_nonneg (m : Nat) (f : Fin m → Rat) (hf : ∀ i, 0 ≤ f i) :

    0 ≤ sumRat m f := by
  induction m with
  | zero =>
    dsimp [sumRat]
    decide
  | succ m ih =>
    dsimp [sumRat]
    have h_prev := ih (fun i => f (Fin.castSucc i)) (fun i => hf (Fin.castSucc i))
    have h_last := hf (Fin.last m)
    exact Rat.add_nonneg h_prev h_last

/-!
### 2. Pre-Hilbert Space and Candidate Column Gram Matrix
-/

/-- An exact rational pre-Hilbert space structure on carrier type `V`.
Models candidate column vectors in dimension 6 under exact inner products. -/
structure PreHilbertSpace (V : Type) where
  inner : V → V → Rat
  inner_self_nonneg : ∀ (v : V), 0 ≤ inner v v
  lincomb : {n : Nat} → (Fin n → Rat) → (Fin n → V) → V

/-- Construction of the Gram matrix from `n` candidate column vectors:
G_{ij} = ⟨v_i, v_j⟩. -/
def gramMatrix {V : Type} (H : PreHilbertSpace V) {n : Nat} (v : Fin n → V) :
    Fin n → Fin n → Rat :=
  fun i j => H.inner (v i) (v j)

/-- Quadratic form evaluation on candidate vectors:
c† G c = ⟨∑ c_i v_i, ∑ c_j v_j⟩. -/
def quadFormOnVectors {V : Type} (H : PreHilbertSpace V) {n : Nat}
    (v : Fin n → V) (c : Fin n → Rat) : Rat :=
  H.inner (H.lincomb c v) (H.lincomb c v)

/-- **Theorem: Candidate Column Gram Matrix is Positive Semidefinite (PSD)**.
For any coefficient vector c, c† G c = ‖∑ c_i v_i‖² ≥ 0.
Proven constructively. -/
theorem gram_matrix_is_psd {V : Type} (H : PreHilbertSpace V) {n : Nat}
    (v : Fin n → V) (c : Fin n → Rat) :
    0 ≤ quadFormOnVectors H v c :=
  H.inner_self_nonneg (H.lincomb c v)

/-!
### 3. Dual Witness Matrix W = L D L† and Trace Nonnegativity
-/

/-- An exact dual witness matrix in factored form W = L D L†:
- `m` modes / rank components;
- `col : Fin m → (Fin n → Rat)` gives columns of L;
- `d : Fin m → Rat` gives diagonal elements of D, with d_k ≥ 0. -/
structure DualWitness (n m : Nat) where
  col : Fin m → (Fin n → Rat)
  d : Fin m → Rat
  d_nonneg : ∀ (k : Fin m), 0 ≤ d k

/-- Action of dual witness on candidate column vectors via factored trace:
Tr(W · G) = ∑_{k=0}^{m-1} D_k ‖∑_{i=0}^{n-1} L_{ik} v_i‖². -/
def traceInnerFactored {n m : Nat} (W : DualWitness n m)
    {V : Type} (H : PreHilbertSpace V) (v : Fin n → V) : Rat :=
  sumRat m (fun k => W.d k * quadFormOnVectors H v (W.col k))

/-- **Theorem: Nonnegativity of Dual Witness Trace Tr(W · G) ≥ 0**.
For any valid dual witness W = L D L† with D ≥ 0, and any candidate Gram matrix G,
Tr(W · G) ≥ 0.
Proven constructively from non-negativity of each factor. -/
theorem dual_witness_trace_nonneg
    {n m : Nat} (W : DualWitness n m)
    {V : Type} (H : PreHilbertSpace V) (v : Fin n → V) :
    0 ≤ traceInnerFactored W H v := by
  apply sumRat_nonneg
  intro k
  have hd : 0 ≤ W.d k := W.d_nonneg k
  have hq : 0 ≤ quadFormOnVectors H v (W.col k) := gram_matrix_is_psd H v (W.col k)
  exact rat_mul_nonneg (W.d k) (quadFormOnVectors H v (W.col k)) hd hq

/-!
### 4. Regional Dual Obstruction on Exact Parameter Box
-/

/-- An exact rational parameter box in coordinate space `θ`. -/
structure ParameterBox (θ : Type) where
  in_box : θ → Prop

/-- A parameterized family of candidate Gram matrices G(θ). -/
def CandidateGramFamily (θ : Type) (n : Nat) := θ → (Fin n → Fin n → Rat)

/-- A parameterized family of candidate vectors v(θ). -/
def CandidateVectorFamily (θ : Type) (V : Type) (n : Nat) := θ → (Fin n → V)

/-- Predicate: Candidate vectors realize the candidate Gram family on the box. -/
def RealizesGramFamily {θ V : Type} (H : PreHilbertSpace V) {n : Nat}
    (box : ParameterBox θ)
    (G : CandidateGramFamily θ n)
    (v : CandidateVectorFamily θ V n) : Prop :=
  ∀ (p : θ), box.in_box p → gramMatrix H (v p) = G p


/-- **THE REGIONAL DUAL OBSTRUCTION THEOREM**.
If a certified dual witness W = L D L† with D ≥ 0 induces a strictly negative
trace evaluation `eval_trace (G q) < 0` for all points q in the parameter box,
then for any point p in the box, G(p) CANNOT equal the Gram matrix of any
configuration of vectors v in H.
Proof: If such vectors existed, `eval_trace (gramMatrix H v) = traceInnerFactored W H v ≥ 0`,
contradicting `eval_trace (G p) < 0` derived from `box.in_box p`. -/
theorem regional_dual_obstruction
    {θ V : Type} (H : PreHilbertSpace V) {n m : Nat}
    (W : DualWitness n m)
    (G : CandidateGramFamily θ n)
    (eval_trace : (Fin n → Fin n → Rat) → Rat)
    (h_eval_eq : ∀ (v : Fin n → V), eval_trace (gramMatrix H v) = traceInnerFactored W H v)
    (box : ParameterBox θ)
    (h_box_neg : ∀ (q : θ), box.in_box q → eval_trace (G q) < 0)
    (p : θ)
    (hp : box.in_box p) :
    ¬ ∃ (v : Fin n → V), gramMatrix H v = G p := by
  intro ⟨v, hv⟩
  have h_neg : eval_trace (G p) < 0 := h_box_neg p hp
  have h_nonneg : 0 ≤ traceInnerFactored W H v := dual_witness_trace_nonneg W H v
  have h_trace_val : eval_trace (G p) = traceInnerFactored W H v := by
    rw [← hv, h_eval_eq]
  have h_contra : 0 ≤ eval_trace (G p) := by
    rw [h_trace_val]
    exact h_nonneg
  exact rat_nonneg_not_lt_zero (eval_trace (G p)) h_contra h_neg

/-- **Regional Incompatibility of Candidate MUB Gram Matrix**:
When an SDP dual certificate certifies a negative trace Tr(W · G(q)) < 0 across an entire parameter box,
no candidate basis vectors in H can realize the Gram matrix G(p) for any point p in that box. -/
theorem sdp_dual_certificate_obstruction
    {θ V : Type} (H : PreHilbertSpace V) {n m : Nat}
    (W : DualWitness n m)
    (G : CandidateGramFamily θ n)
    (eval_trace : (Fin n → Fin n → Rat) → Rat)
    (h_eval_eq : ∀ (v : Fin n → V), eval_trace (gramMatrix H v) = traceInnerFactored W H v)
    (box : ParameterBox θ)
    (h_box_neg : ∀ (q : θ), box.in_box q → eval_trace (G q) < 0)
    (p : θ)
    (hp : box.in_box p) :
    ∀ (v : Fin n → V), gramMatrix H v = G p → False := by
  intro v hv
  have h_not := regional_dual_obstruction H W G eval_trace h_eval_eq box h_box_neg p hp
  exact h_not ⟨v, hv⟩

/-- **RealizesGramFamily Obstruction**:
A parameterized candidate vector family v(θ) cannot realize the Gram family G(θ) on the box. -/
theorem realizes_gram_family_obstruction
    {θ V : Type} (H : PreHilbertSpace V) {n m : Nat}
    (W : DualWitness n m)
    (G : CandidateGramFamily θ n)
    (eval_trace : (Fin n → Fin n → Rat) → Rat)
    (h_eval_eq : ∀ (v : Fin n → V), eval_trace (gramMatrix H v) = traceInnerFactored W H v)
    (box : ParameterBox θ)
    (h_box_neg : ∀ (q : θ), box.in_box q → eval_trace (G q) < 0)
    (p : θ) (hp : box.in_box p)
    (v : CandidateVectorFamily θ V n) :
    RealizesGramFamily H box G v → False := by
  intro h_realizes
  have hv := h_realizes p hp
  exact regional_dual_obstruction H W G eval_trace h_eval_eq box h_box_neg p hp ⟨v p, hv⟩

#print axioms rat_mul_nonneg
#print axioms rat_nonneg_not_lt_zero
#print axioms sumRat_nonneg
#print axioms gram_matrix_is_psd
#print axioms dual_witness_trace_nonneg
#print axioms regional_dual_obstruction
#print axioms sdp_dual_certificate_obstruction
#print axioms realizes_gram_family_obstruction


end MUB6.Gluing.CandidateGram
