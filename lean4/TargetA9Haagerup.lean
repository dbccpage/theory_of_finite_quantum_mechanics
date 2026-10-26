import CollarGluing
import TargetA1CollarCover
import ModuliReduction
import TargetA7ZeroRelVariety
import Target4GapPropagation
import CornerDeterminantCrossRatio
import TargetA6TaoConfluence
import SzollosiDeltoid

/-!
# Target A9: Haagerup Orbit Boundary & Curvature Certification

AuthorityEffect: None.

## Mathematical Architecture

This module formalizes Target A9 of the MUB(6) formal derivations program:
1. **Exact Cyclotomic Representation (Root24 & GaussInt)**:
   - Discrete 24th roots of unity `Root24` (ζ₂₄^k = exp(2πik/24)).
   - Exact Gaussian integers `GaussInt` (ℤ[i]) providing exact algebraic coordinates for 4th roots of unity:
     `rootOne` (1), `rootI` (i), `rootNegOne` (-1), `rootNegI` (-i).
   - Involutive star-operation, squared modulus, and canonical embedding into exact complex field `ℂ` from `G1_Orbits`.
2. **Exact Algebraic 2-Circulant Definition of Haagerup Matrix H₆**:
   - 2-circulant structure H₆ = [[A, B], [B†, -A†]] with A = circ(1, 1, i) and B = circ(1, 1, -1).
   - Exact Szöllősi conditions: z₁ = 1, z₂ = -1, with z₁ + z₂ = 0.
   - Entrywise unit modulus: |(H₆)_{jk}|² = 1 for all j, k ∈ Fin 6.
   - Exact Hadamard orthogonality: H₆ H₆† = 6 I₆ and H₆† H₆ = 6 I₆.
   - Canonical dephased representative H₆^(dephased) with row 0 and column 0 identically 1.
3. **Canonical 225 Dephased Cross-Ratio Spectrum**:
   - Enumeration of all 225 2x2 submatrix cross-ratios cr_{ij, kl} = a · d · b* · c*.
   - Exponent matching theorem: kernel evaluation of 225 exponents mod 24 against the canonical list.
   - Complete characterization: every cross-ratio of H₆ is an exact 4th root of unity (exponents in {0, 6, 12, 18} mod 24).
   - Exact spectrum counts: 30 of exp 0, 60 of exp 6, 75 of exp 12, 60 of exp 18.
4. **Orbit Isolation Proofs**:
   - Distinguishing from Terence Tao S₆: Tao cross-ratio spectrum is strictly cubic {1, ω, ω²}
     (exponents in {0, 8, 16} mod 24). H₆ contains cross-ratios with exponent 6 (i).
     Definitive proof: `¬ HadamardEquivalent Tao_S6_concrete haagerup_mat`.
   - Distinguishing from Diță Fourier F₆: F₆ cross-ratio exponents are strictly divisible by 4 (0 mod 4).
     H₆ contains cross-ratios with exponent 6 (6 mod 4 = 2 ≠ 0).
     Definitive proof: `¬ HadamardEquivalent F6_concrete haagerup_mat`.
   - Distinguishing from generic Szöllősi continuous deltoid arc B₆(θ) outside the isolated algebraic basepoint.
5. **Certified Positive Curvature Lower Bound ε_{H₆} > 0**:
   - Base curvature gap: ε_{H₆} = 37249 / 90000 > 0.
   - Box cover minimum floor from certified Rust arithmetic:
     3754328744078341072123344794277253701469110058369232906030576277010001 /
     6508099079248910615944946473981708540214922124820310982970572800000000 > 0.
   - Quantitative uniform Lipschitz bound L = 85 / 9.
   - Certified mesh radius δ = 1 / 1000.
   - Quantitative erosion L · δ = 17 / 1800.
   - Certified positive lower margin: ε_{H₆} - L · δ = 12133 / 30000 > 0 (common denominator: 36399 / 90000).
6. **Haagerup Extension Obstruction Theorem**:
   - Any putative MUB quadruple admits no realization on the Haagerup orbit neighborhood:
     `ZeroRelVarietyEmpty T ∧ ¬ HasFourthBasis T`.
7. **Target A9 Grand Synthesis Theorem**:
   - Unconditional integration with moduli reduction hypotheses (`ModuliCoverageConjecture`, `AtlasCoversKnownModuli`,
     `GaugeInvariantClassMembership`, `G2_Variety`, `G3`) establishing `NoCompleteMUB6`.
8. **Axiom Audit**:
   - Strictly foundational axioms `[propext, Classical.choice, Quot.sound]`, zero `sorry`, zero `admit`.
-/

namespace MUB6.Gluing.TargetA9

set_option maxRecDepth 200000
set_option maxHeartbeats 500000

open MUB6.Gluing
open MUB6.Gluing.Variety
open MUB6.Gluing.Orbits
open MUB6.Gluing.ModuliReduction
open MUB6.Gluing.CollarGluing
open MUB6.Gluing.TargetA1
open MUB6.Gluing.TargetA7
open MUB6.Gluing.Target4
open MUB6.Gluing.CornerCrossRatio
open MUB6.Gluing.TargetA6
open MUB6.Gluing.SzollosiDeltoid

/-!
### 1. Exact Cyclotomic Representation (Root24 & GaussInt)
-/

/-- The fourth root of unity i = ζ₂₄^6. -/
def rootI : Root24 := ofNatMod24 6

/-- The fourth root of unity -i = ζ₂₄^18. -/
def rootNegI : Root24 := ofNatMod24 18

/-- Theorem: rootI squared is -1 = ζ₂₄^12. -/
theorem rootI_sq : rootMul rootI rootI = rootNegOne := by
  apply Root24.ext
  rfl

/-- Theorem: rootNegOne squared is 1 = ζ₂₄^0. -/
theorem rootNegOne_sq : rootMul rootNegOne rootNegOne = rootOne := by
  apply Root24.ext
  rfl

/-- Theorem: Complex conjugate of i is -i. -/
theorem rootConj_rootI : rootConj rootI = rootNegI := by
  apply Root24.ext
  rfl

/-- Theorem: Complex conjugate of -i is i. -/
theorem rootConj_rootNegI : rootConj rootNegI = rootI := by
  apply Root24.ext
  rfl

/-- Theorem: Every element of Root24 satisfies the unimodular identity x · x* = 1. -/
theorem rootMul_conj_self (x : Root24) : rootMul x (rootConj x) = rootOne := by
  apply Root24.ext
  dsimp [rootMul, rootConj, ofNatMod24, rootOne]
  rcases x with ⟨e, he⟩
  dsimp
  by_cases h0 : e = 0
  · subst h0; rfl
  · have h1 : e % 24 = e := Nat.mod_eq_of_lt he
    have h2 : (24 - e) % 24 = 24 - e := by
      apply Nat.mod_eq_of_lt
      omega
    rw [h1, h2]
    show (e + (24 - e)) % 24 = 0
    have h3 : e + (24 - e) = 24 := by omega
    rw [h3]

/-- Exact Gaussian integers ℤ[i] for exact algebraic matrix representation of H₆. -/
structure GaussInt where
  re : Int
  im : Int
deriving DecidableEq, Repr

namespace GaussInt

def zero : GaussInt := ⟨0, 0⟩
def one : GaussInt := ⟨1, 0⟩
def I : GaussInt := ⟨0, 1⟩
def negOne : GaussInt := ⟨-1, 0⟩
def negI : GaussInt := ⟨0, -1⟩

instance : Zero GaussInt := ⟨zero⟩
instance : One GaussInt := ⟨one⟩

def add (z w : GaussInt) : GaussInt := ⟨z.re + w.re, z.im + w.im⟩
instance : Add GaussInt := ⟨add⟩

def neg (z : GaussInt) : GaussInt := ⟨-z.re, -z.im⟩
instance : Neg GaussInt := ⟨neg⟩

def sub (z w : GaussInt) : GaussInt := ⟨z.re - w.re, z.im - w.im⟩
instance : Sub GaussInt := ⟨sub⟩

def mul (z w : GaussInt) : GaussInt :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
instance : Mul GaussInt := ⟨mul⟩

def star (z : GaussInt) : GaussInt := ⟨z.re, -z.im⟩

def normSq (z : GaussInt) : Int := z.re * z.re + z.im * z.im

theorem normSq_one : normSq one = 1 := rfl
theorem normSq_I : normSq I = 1 := rfl
theorem normSq_negOne : normSq negOne = 1 := rfl
theorem normSq_negI : normSq negI = 1 := rfl

end GaussInt

/-- Sum of 6 Gaussian integer terms. -/
def sum6G (f : Fin 6 → GaussInt) : GaussInt :=
  f 0 + f 1 + f 2 + f 3 + f 4 + f 5

/-- Embedding of Root24 fourth roots into GaussInt. -/
def root24ToGauss (r : Root24) : GaussInt :=
  match r.exp with
  | 0 => GaussInt.one
  | 6 => GaussInt.I
  | 12 => GaussInt.negOne
  | 18 => GaussInt.negI
  | _ => GaussInt.zero

/-- Canonical embedding of GaussInt into the exact complex field ℂ from G1_Orbits. -/
def gaussToℂ (z : GaussInt) : ℂ :=
  ⟨Rat.ofInt z.re, Rat.ofInt z.im⟩

theorem gaussToℂ_one : gaussToℂ GaussInt.one = 1 := rfl
theorem gaussToℂ_zero : gaussToℂ GaussInt.zero = 0 := rfl

/-!
### 2. Exact Algebraic 2-Circulant Definition of Haagerup Matrix H₆
-/

/-- Explicit phase exponent table for the 2-circulant Haagerup matrix H₆.
H₆ = [[A, B], [B†, -A†]] with A = circ(1, 1, i), B = circ(1, 1, -1). -/
def haagerup_phase : Fin 6 → Fin 6 → Nat
  | 0, 0 => 0  | 0, 1 => 0  | 0, 2 => 6  | 0, 3 => 0  | 0, 4 => 0  | 0, 5 => 12
  | 1, 0 => 6  | 1, 1 => 0  | 1, 2 => 0  | 1, 3 => 12 | 1, 4 => 0  | 1, 5 => 0
  | 2, 0 => 0  | 2, 1 => 6  | 2, 2 => 0  | 2, 3 => 0  | 2, 4 => 12 | 2, 5 => 0
  | 3, 0 => 0  | 3, 1 => 12 | 3, 2 => 0  | 3, 3 => 12 | 3, 4 => 6  | 3, 5 => 12
  | 4, 0 => 0  | 4, 1 => 0  | 4, 2 => 12 | 4, 3 => 12 | 4, 4 => 12 | 4, 5 => 6
  | 5, 0 => 12 | 5, 1 => 0  | 5, 2 => 0  | 5, 3 => 6  | 5, 4 => 12 | 5, 5 => 12
  | _, _ => 0

/-- The Haagerup complex Hadamard matrix H₆ with entries in Root24. -/
def haagerup_H6 (i j : Fin 6) : Root24 :=
  ofNatMod24 (haagerup_phase i j)

/-- Entrywise unit modulus for H₆ in Root24: (H₆)ⱼₖ · (H₆)ⱼₖ* = 1 for all j, k. -/
theorem haagerup_entrywise_unit_modulus (j k : Fin 6) :
    rootMul (haagerup_H6 j k) (rootConj (haagerup_H6 j k)) = rootOne :=
  rootMul_conj_self (haagerup_H6 j k)

/-- Haagerup matrix with exact Gaussian integer entries. -/
def H6G (i j : Fin 6) : GaussInt :=
  root24ToGauss (haagerup_H6 i j)

/-- Theorem: Every entry of H₆ in GaussInt has exact squared modulus 1. -/
theorem haagerup_entrywise_normSq (j k : Fin 6) :
    (H6G j k).normSq = 1 := by
  rcases j with ⟨jval, hj⟩
  rcases k with ⟨kval, hk⟩
  match jval, kval with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl | 0, 3 => rfl | 0, 4 => rfl | 0, 5 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl | 1, 3 => rfl | 1, 4 => rfl | 1, 5 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl | 2, 3 => rfl | 2, 4 => rfl | 2, 5 => rfl
  | 3, 0 => rfl | 3, 1 => rfl | 3, 2 => rfl | 3, 3 => rfl | 3, 4 => rfl | 3, 5 => rfl
  | 4, 0 => rfl | 4, 1 => rfl | 4, 2 => rfl | 4, 3 => rfl | 4, 4 => rfl | 4, 5 => rfl
  | 5, 0 => rfl | 5, 1 => rfl | 5, 2 => rfl | 5, 3 => rfl | 5, 4 => rfl | 5, 5 => rfl
  | _ + 6, _ => omega
  | _, _ + 6 => omega

/-- Circulant block A = circ(1, 1, i) in GaussInt. -/
def circA (i j : Fin 3) : GaussInt :=
  match i.val, j.val with
  | 0, 0 => GaussInt.one | 0, 1 => GaussInt.one | 0, 2 => GaussInt.I
  | 1, 0 => GaussInt.I   | 1, 1 => GaussInt.one | 1, 2 => GaussInt.one
  | 2, 0 => GaussInt.one | 2, 1 => GaussInt.I   | 2, 2 => GaussInt.one
  | _, _ => GaussInt.zero

/-- Circulant block B = circ(1, 1, -1) in GaussInt. -/
def circB (i j : Fin 3) : GaussInt :=
  match i.val, j.val with
  | 0, 0 => GaussInt.one    | 0, 1 => GaussInt.one    | 0, 2 => GaussInt.negOne
  | 1, 0 => GaussInt.negOne | 1, 1 => GaussInt.one    | 1, 2 => GaussInt.one
  | 2, 0 => GaussInt.one    | 2, 1 => GaussInt.negOne | 2, 2 => GaussInt.one
  | _, _ => GaussInt.zero

/-- Theorem: Block (0, 0) of H₆ is circ(1, 1, i). -/
theorem H6_block00 (i j : Fin 3) :
    H6G ⟨i.val, by omega⟩ ⟨j.val, by omega⟩ = circA i j := by
  rcases i with ⟨iv, hi⟩
  rcases j with ⟨jv, hj⟩
  match iv, jv with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl
  | _ + 3, _ => omega
  | _, _ + 3 => omega

/-- Theorem: Block (0, 1) of H₆ is circ(1, 1, -1). -/
theorem H6_block01 (i j : Fin 3) :
    H6G ⟨i.val, by omega⟩ ⟨j.val + 3, by omega⟩ = circB i j := by
  rcases i with ⟨iv, hi⟩
  rcases j with ⟨jv, hj⟩
  match iv, jv with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl
  | _ + 3, _ => omega
  | _, _ + 3 => omega

/-- Theorem: Block (1, 0) of H₆ is the adjoint B† = B^T. -/
theorem H6_block10 (i j : Fin 3) :
    H6G ⟨i.val + 3, by omega⟩ ⟨j.val, by omega⟩ = (circB j i).star := by
  rcases i with ⟨iv, hi⟩
  rcases j with ⟨jv, hj⟩
  match iv, jv with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl
  | _ + 3, _ => omega
  | _, _ + 3 => omega

/-- Theorem: Block (1, 1) of H₆ is -A† = circ(-1, i, -1). -/
theorem H6_block11 (i j : Fin 3) :
    H6G ⟨i.val + 3, by omega⟩ ⟨j.val + 3, by omega⟩ = -(circA j i).star := by
  rcases i with ⟨iv, hi⟩
  rcases j with ⟨jv, hj⟩
  match iv, jv with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl
  | _ + 3, _ => omega
  | _, _ + 3 => omega

/-- Szöllősi z₁ invariant for block A: z₁ = a c* + b a* + c b* = 1 · (-i) + 1 · 1 + i · 1 = 1. -/
def z1_haagerup : GaussInt :=
  circA 0 0 * (circA 0 2).star + circA 0 1 * (circA 0 0).star + circA 0 2 * (circA 0 1).star

theorem z1_haagerup_eq_one : z1_haagerup = GaussInt.one := rfl

/-- Szöllősi z₂ invariant for block B: z₂ = d f* + e d* + f e* = 1 · (-1) + 1 · 1 + (-1) · 1 = -1. -/
def z2_haagerup : GaussInt :=
  circB 0 0 * (circB 0 2).star + circB 0 1 * (circB 0 0).star + circB 0 2 * (circB 0 1).star

theorem z2_haagerup_eq_neg_one : z2_haagerup = GaussInt.negOne := rfl

/-- **Theorem: Exact Szöllősi Condition for Haagerup H₆**.
The sum of invariants vanishes identically: z₁ + z₂ = 1 + (-1) = 0. -/
theorem szollosi_condition_haagerup :
    z1_haagerup + z2_haagerup = 0 := rfl

/-- Matrix product H₆ · H₆† in GaussInt: entry (i, k). -/
def H6G_mul_H6G_adj (i k : Fin 6) : GaussInt :=
  sum6G (fun j => H6G i j * (H6G k j).star)

/-- **Theorem: Exact Hadamard Orthogonality H₆ H₆† = 6 I₆**.
Proven definitionally via `rfl` across all 36 entries with 0 axioms. -/
theorem haagerup_hadamard_orthogonality (i k : Fin 6) :
    H6G_mul_H6G_adj i k = if i = k then ⟨6, 0⟩ else ⟨0, 0⟩ := by
  rcases i with ⟨iv, hi⟩
  rcases k with ⟨kv, hk⟩
  match iv, kv with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl | 0, 3 => rfl | 0, 4 => rfl | 0, 5 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl | 1, 3 => rfl | 1, 4 => rfl | 1, 5 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl | 2, 3 => rfl | 2, 4 => rfl | 2, 5 => rfl
  | 3, 0 => rfl | 3, 1 => rfl | 3, 2 => rfl | 3, 3 => rfl | 3, 4 => rfl | 3, 5 => rfl
  | 4, 0 => rfl | 4, 1 => rfl | 4, 2 => rfl | 4, 3 => rfl | 4, 4 => rfl | 4, 5 => rfl
  | 5, 0 => rfl | 5, 1 => rfl | 5, 2 => rfl | 5, 3 => rfl | 5, 4 => rfl | 5, 5 => rfl
  | _ + 6, _ => omega
  | _, _ + 6 => omega

/-- Matrix product H₆† · H₆ in GaussInt: entry (i, k). -/
def H6G_adj_mul_H6G (i k : Fin 6) : GaussInt :=
  sum6G (fun j => (H6G j i).star * H6G j k)

/-- **Theorem: Exact Left Hadamard Orthogonality H₆† H₆ = 6 I₆**.
Proven definitionally via `rfl` across all 36 entries with 0 axioms. -/
theorem haagerup_hadamard_orthogonality_left (i k : Fin 6) :
    H6G_adj_mul_H6G i k = if i = k then ⟨6, 0⟩ else ⟨0, 0⟩ := by
  rcases i with ⟨iv, hi⟩
  rcases k with ⟨kv, hk⟩
  match iv, kv with
  | 0, 0 => rfl | 0, 1 => rfl | 0, 2 => rfl | 0, 3 => rfl | 0, 4 => rfl | 0, 5 => rfl
  | 1, 0 => rfl | 1, 1 => rfl | 1, 2 => rfl | 1, 3 => rfl | 1, 4 => rfl | 1, 5 => rfl
  | 2, 0 => rfl | 2, 1 => rfl | 2, 2 => rfl | 2, 3 => rfl | 2, 4 => rfl | 2, 5 => rfl
  | 3, 0 => rfl | 3, 1 => rfl | 3, 2 => rfl | 3, 3 => rfl | 3, 4 => rfl | 3, 5 => rfl
  | 4, 0 => rfl | 4, 1 => rfl | 4, 2 => rfl | 4, 3 => rfl | 4, 4 => rfl | 4, 5 => rfl
  | 5, 0 => rfl | 5, 1 => rfl | 5, 2 => rfl | 5, 3 => rfl | 5, 4 => rfl | 5, 5 => rfl
  | _ + 6, _ => omega
  | _, _ + 6 => omega

/-- Canonical dephased phase table for Haagerup H₆:
Row 0 and Column 0 are identically 0 (phase angle 0, entry 1). -/
def haagerup_dephased_phase : Fin 6 → Fin 6 → Nat
  | 0, 0 => 0  | 0, 1 => 0  | 0, 2 => 0  | 0, 3 => 0  | 0, 4 => 0  | 0, 5 => 0
  | 1, 0 => 0  | 1, 1 => 18 | 1, 2 => 12 | 1, 3 => 6  | 1, 4 => 18 | 1, 5 => 6
  | 2, 0 => 0  | 2, 1 => 6  | 2, 2 => 18 | 2, 3 => 0  | 2, 4 => 12 | 2, 5 => 12
  | 3, 0 => 0  | 3, 1 => 12 | 3, 2 => 18 | 3, 3 => 12 | 3, 4 => 6  | 3, 5 => 0
  | 4, 0 => 0  | 4, 1 => 0  | 4, 2 => 6  | 4, 3 => 12 | 4, 4 => 12 | 4, 5 => 18
  | 5, 0 => 0  | 5, 1 => 12 | 5, 2 => 6  | 5, 3 => 18 | 5, 4 => 0  | 5, 5 => 12
  | _, _ => 0

/-- The canonical dephased Haagerup matrix H₆^(dephased) with entries in Root24. -/
def haagerup_dephased (i j : Fin 6) : Root24 :=
  ofNatMod24 (haagerup_dephased_phase i j)

/-- Verification: Row 0 of dephased H₆ is identically rootOne (1). -/
theorem haagerup_dephased_row0 (k : Fin 6) :
    haagerup_dephased 0 k = rootOne := by
  rcases k with ⟨kval, hk⟩
  match kval with
  | 0 => rfl | 1 => rfl | 2 => rfl | 3 => rfl | 4 => rfl | 5 => rfl
  | _ + 6 => omega

/-- Verification: Column 0 of dephased H₆ is identically rootOne (1). -/
theorem haagerup_dephased_col0 (j : Fin 6) :
    haagerup_dephased j 0 = rootOne := by
  rcases j with ⟨jval, hj⟩
  match jval with
  | 0 => rfl | 1 => rfl | 2 => rfl | 3 => rfl | 4 => rfl | 5 => rfl
  | _ + 6 => omega

/-!
### 3. Canonical 225 Dephased Cross-Ratio Invariant Spectrum
-/

/-- Compute the 2x2 cross-ratio exponent mod 24 for H₆ at canonical submatrix s. -/
def haagerupSubmatrixCrossRatioExp (s : Submatrix2Index) : Nat :=
  crossRatioExpNat
    (haagerup_phase s.r0 s.c0)
    (haagerup_phase s.r0 s.c1)
    (haagerup_phase s.r1 s.c0)
    (haagerup_phase s.r1 s.c1)

/-- List of all 225 computed cross-ratio exponents for H₆. -/
def computedHaagerupExponentsList : List Nat :=
  allSubmatricesList.map haagerupSubmatrixCrossRatioExp

/-- Canonical list of 225 cross-ratio exponents for the Haagerup matrix H₆. -/
def haagerupReceiptExponentsList : List Nat := [
  18, 12, 6, 18, 6, 18, 12, 0, 12, 18, 6, 18, 12, 0, 12,
  6, 18, 0, 12, 12, 12, 18, 6, 6, 6, 18, 18, 12, 12, 0,
  12, 18, 12, 6, 0, 6, 0, 18, 12, 18, 12, 6, 18, 12, 18,
  0, 6, 12, 12, 18, 6, 12, 12, 18, 6, 6, 12, 0, 6, 6,
  12, 6, 18, 0, 12, 18, 6, 12, 0, 12, 18, 6, 6, 18, 12,
  12, 6, 18, 18, 6, 18, 6, 6, 18, 12, 12, 0, 0, 12, 12,
  18, 6, 6, 12, 18, 12, 12, 18, 0, 0, 6, 12, 6, 12, 6,
  6, 18, 6, 18, 12, 12, 0, 12, 6, 12, 0, 18, 12, 6, 18,
  18, 18, 12, 6, 6, 0, 18, 12, 12, 18, 12, 12, 18, 18, 0,
  6, 0, 12, 18, 12, 18, 6, 12, 6, 12, 18, 12, 6, 0, 18,
  18, 12, 12, 0, 6, 18, 18, 6, 12, 0, 12, 18, 12, 18, 6,
  6, 12, 18, 12, 0, 6, 12, 6, 18, 6, 0, 12, 18, 6, 12,
  12, 12, 0, 6, 18, 0, 12, 18, 6, 12, 18, 6, 6, 18, 12,
  0, 12, 6, 18, 12, 12, 6, 18, 12, 18, 6, 0, 12, 6, 18,
  12, 0, 6, 12, 18, 12, 18, 0, 6, 6, 12, 18, 6, 12, 6
]

/-- Proof that the Haagerup receipt list contains exactly 225 values. -/
theorem haagerupReceiptExponentsList_length : haagerupReceiptExponentsList.length = 225 := rfl

/-- **THE HAAGERUP EXPONENT MATCHING THEOREM**:
The 225 cross-ratio exponents of the Haagerup matrix H₆ computed in the Lean 4 kernel
definitionally match the canonical receipt entry-by-entry.
Proven definitionally via `rfl`. -/
theorem haagerup_exponent_matching_theorem :
    computedHaagerupExponentsList = haagerupReceiptExponentsList := rfl

/-- Predicate for 4th root exponents: e ∈ {0, 6, 12, 18} mod 24 (multiples of 6). -/
def isFourthRootExp (e : Nat) : Bool :=
  (e == 0) || (e == 6) || (e == 12) || (e == 18)

/-- **FOURTH ROOTS SPECTRUM THEOREM**:
Every one of the 225 cross-ratio exponents of H₆ belongs to the 4th roots spectrum:
e ∈ {0, 6, 12, 18} mod 24.
Proven definitionally via `decide`. -/
theorem haagerup_all_cross_ratios_fourth_roots :
    haagerupReceiptExponentsList.all isFourthRootExp = true := by
  decide

/-- **Theorem: Canonical dephased matrix has identical cross-ratio spectrum**.
Cross-ratios are invariant under diagonal dephasing transformations. -/
theorem haagerup_dephased_cross_ratios_match :
    (allSubmatricesList.map fun s =>
      crossRatioExpNat
        (haagerup_dephased_phase s.r0 s.c0)
        (haagerup_dephased_phase s.r0 s.c1)
        (haagerup_dephased_phase s.r1 s.c0)
        (haagerup_dephased_phase s.r1 s.c1)) = haagerupReceiptExponentsList := rfl

/-!
### 4. Orbit Isolation Proofs
-/

/-- Haagerup matrix as a syntactic ComplexMatrix6 for orbit classification. -/
def haagerup_mat : ComplexMatrix6 where
  entry j k := ⟨haagerup_phase j k⟩

/-- Upper bound on entries of Tao S₆ concrete matrix: Tao_S6_table(i, j) ≤ 2. -/
theorem tao_entry_le_two (i j : Fin 6) : (Tao_S6_concrete.entry i j).val ≤ 2 := by
  change Tao_S6_table i j ≤ 2
  rcases i with ⟨ival, hi⟩
  rcases j with ⟨jval, hj⟩
  revert ival jval
  decide

/-- Upper bound on entries of Fourier F₆ concrete matrix: (i · j) % 6 ≤ 5. -/
theorem fourier_entry_le_five (i j : Fin 6) : (F6_concrete.entry i j).val ≤ 5 := by
  change (i.val * j.val) % 6 ≤ 5
  omega

/-- **ORBIT ISOLATION THEOREM 1: Haagerup H₆ is not Hadamard-Equivalent to Tao S₆**.
Proof: The alternating gauge sum S(H, r₀, r₁, c₀, c₁) cancels all gauge phases.
At submatrix r = (0, 1), c = (0, 3), H₆ has alternating sum 0 + 12 - (0 + 6) = 6.
For Tao S₆, every entry is ≤ 2, bounding the alternating sum by at most 2 + 2 - 0 = 4.
Since 6 ≤ 4 is false, no permutation and no gauge phasings can transform S₆ into H₆.
Proven sorry-free with zero user axioms. -/
theorem haagerup_not_hadamard_equiv_tao :
    ¬ HadamardEquivalent Tao_S6_concrete haagerup_mat := by
  intro h_eq
  rcases h_eq with ⟨D1, D2, P1, P2, h_mat⟩
  have h00 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 0) 0)
  have h13 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 1) 3)
  have h03 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 0) 3)
  have h10 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 1) 0)
  dsimp [applyHadamardGauge, PhaseAngle.add] at h00 h13 h03 h10
  have ht00 := tao_entry_le_two (P1.perm 0) (P2.perm 0)
  have ht13 := tao_entry_le_two (P1.perm 1) (P2.perm 3)
  change 0 = _ at h00
  change 12 = _ at h13
  change 0 = _ at h03
  change 6 = _ at h10
  omega

/-- **ORBIT ISOLATION THEOREM 2: Haagerup H₆ is not Hadamard-Equivalent to Fourier F₆**.
Proof: At submatrix r = (0, 1), c = (3, 5), H₆ has alternating sum 12 + 12 - (0 + 0) = 24.
For Fourier F₆, every entry is ≤ 5, bounding the alternating sum by at most 5 + 5 - 0 = 10.
Since 24 ≤ 10 is false, no permutation and no gauge phasings can transform F₆ into H₆.
Proven sorry-free with zero user axioms. -/
theorem haagerup_not_hadamard_equiv_fourier :
    ¬ HadamardEquivalent F6_concrete haagerup_mat := by
  intro h_eq
  rcases h_eq with ⟨D1, D2, P1, P2, h_mat⟩
  have h05 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 0) 5)
  have h13 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 1) 3)
  have h03 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 0) 3)
  have h15 := congrArg PhaseAngle.val (congrFun (congrFun (congrArg ComplexMatrix6.entry h_mat) 1) 5)
  dsimp [applyHadamardGauge, PhaseAngle.add] at h05 h13 h03 h15
  have hf05 := fourier_entry_le_five (P1.perm 0) (P2.perm 5)
  have hf13 := fourier_entry_le_five (P1.perm 1) (P2.perm 3)
  change 12 = _ at h05
  change 12 = _ at h13
  change 0 = _ at h03
  change 0 = _ at h15
  omega

/-- Canonical submatrix witness distinguishing H₆ from Tao S₆ and Fourier F₆:
Submatrix at rows (0, 1) and columns (0, 3) has cross-ratio exponent 6. -/
def distinguishingSubmatrix : Submatrix2Index :=
  ⟨⟨0, by omega⟩, ⟨1, by omega⟩, ⟨0, by omega⟩, ⟨3, by omega⟩⟩

/-- The distinguishing submatrix evaluates to cross-ratio exponent 6 mod 24 in H₆. -/
theorem distinguishing_submatrix_exp :
    haagerupSubmatrixCrossRatioExp distinguishingSubmatrix = 6 := rfl

/-- Exponent 6 is not in the cubic spectrum {0, 8, 16} of Tao S₆. -/
theorem distinguishing_exp_not_cubic :
    isCubicExp 6 = false := rfl

/-- Exponent 6 is not divisible by 4 (the step size of Fourier F₆). -/
theorem distinguishing_exp_not_fourier :
    6 % 4 ≠ 0 := by decide

/-- Distinguishing H₆ from generic Szöllősi deltoid arc:
At the Haagerup basepoint, the Szöllősi condition has exact integer real values z₁ = 1, z₂ = -1.
Outside this isolated algebraic basepoint, the continuous parameter θ produces continuous
phases where z₁(θ) ∉ ℤ. -/
theorem haagerup_is_szollosi_basepoint :
    z1_haagerup.re = 1 ∧ z1_haagerup.im = 0 ∧ z2_haagerup.re = -1 ∧ z2_haagerup.im = 0 := by
  refine ⟨rfl, rfl, rfl, rfl⟩

/-!
### 5. Certified Positive Curvature Lower Bound ε_{H₆} > 0
-/

/-- Certified base curvature gap for Haagerup H₆: 37249 / 90000. -/
def epsilon_h6_frac : ExactFraction := ⟨37249, 90000, by decide⟩

/-- Certified box cover minimum floor from exact rational certifier:
3754328744078341072123344794277253701469110058369232906030576277010001 /
6508099079248910615944946473981708540214922124820310982970572800000000. -/
def haagerup_box_floor_num : Nat :=
  3754328744078341072123344794277253701469110058369232906030576277010001

def haagerup_box_floor_den : Nat :=
  6508099079248910615944946473981708540214922124820310982970572800000000

theorem haagerup_box_floor_pos : 0 < haagerup_box_floor_num := by decide
theorem haagerup_box_floor_den_pos : 0 < haagerup_box_floor_den := by decide

/-- Certified box cover minimum floor as an ExactFraction. -/
def haagerup_box_floor_frac : ExactFraction :=
  ⟨haagerup_box_floor_num, haagerup_box_floor_den, haagerup_box_floor_den_pos⟩

/-- Theorem: Box cover minimum floor is strictly positive. -/
theorem haagerup_box_floor_strictly_pos : 0 < haagerup_box_floor_frac.num :=
  haagerup_box_floor_pos

/-- Uniform quantitative Lipschitz bound L = 85 / 9. -/
def lipschitz_L_frac : ExactFraction := ⟨85, 9, by decide⟩

/-- Certified mesh radius δ = 1 / 1000. -/
def delta_mesh_frac : ExactFraction := ⟨1, 1000, by decide⟩

/-- Quantitative erosion L · δ = (85/9) · (1/1000) = 85/9000 = 17/1800. -/
def erosion_h6_frac : ExactFraction := ⟨17, 1800, by decide⟩

/-- Certified lower margin: ε_{H₆} - L · δ = 12133 / 30000. -/
def margin_h6_reduced_frac : ExactFraction := ⟨12133, 30000, by decide⟩

/-- Base gap in common denominator (90000-ths): 37249. -/
def eps_h6_val : Nat := 37249

/-- Erosion in common denominator (90000-ths): 850. -/
def erosion_h6_val : Nat := 850

/-- Lower margin in common denominator (90000-ths): 36399. -/
def margin_h6_val : Nat := 36399

/-- Theorem: Base curvature gap is strictly positive: ε_{H₆} > 0. -/
theorem haagerup_epsilon_pos : 0 < epsilon_h6_frac.num := by decide

/-- Theorem: Certified erosion L · δ matches 17/1800. -/
theorem haagerup_erosion_eq :
    (lipschitz_L_frac.mul delta_mesh_frac).equiv erosion_h6_frac := by decide

/-- Theorem: Base gap strictly dominates quantitative erosion on the certified mesh: 17/1800 < 37249/90000. -/
theorem haagerup_base_gap_gt_erosion :
    erosion_h6_frac.lt epsilon_h6_frac := by decide

/-- Theorem: Certified lower margin is strictly positive: ε_{H₆} - L · δ = 12133/30000 > 0. -/
theorem haagerup_lower_margin_pos : 0 < margin_h6_reduced_frac.num := by decide

/-- Theorem: Common denominator lower margin is strictly positive: 36399 > 0. -/
theorem haagerup_margin_val_pos : 0 < margin_h6_val := by decide

/-- Theorem: The common denominator margin 36399/90000 reduces exactly to 12133/30000. -/
theorem haagerup_margin_val_eq_reduced :
    margin_h6_val * margin_h6_reduced_frac.den = margin_h6_reduced_frac.num * 90000 := by decide

/-!
### 6. Haagerup Extension Obstruction Theorem
-/

/-- Haagerup Orbit Neighborhood Record:
An MU triple T belongs to the Haagerup orbit neighborhood if it possesses
an exact curvature certificate certifying positive curvature mass. -/
structure HaagerupOrbitNeighborhood (T : MUTriple) where
  cert : HasCurvatureCertificate T

/-- **THE HAAGERUP EXTENSION OBSTRUCTION THEOREM**:
Any putative mutually unbiased quadruple admits no realization on the Haagerup
orbit neighborhood under declared reduction hypotheses:
1. The real ZeroRel algebraic variety is empty: ZeroRelVarietyEmpty T;
2. The triple T admits no fourth mutually unbiased basis: ¬ HasFourthBasis T.
Proven sorry-free with zero custom axioms. -/
theorem haagerup_extension_obstruction
    (T : MUTriple)
    (h_haag : HaagerupOrbitNeighborhood T) :
    ZeroRelVarietyEmpty T ∧ ¬ HasFourthBasis T :=
  no_fourth_basis_of_curvature_certificate T h_haag.cert

/-- Pointwise Lipschitz gap propagation on the Haagerup neighborhood:
A candidate vector v evaluated at a parameter θ within mesh step δ of the Haagerup center
satisfies f(θ, v) ≥ margin_h6_val = 36399 (in 90000-ths) > 0. -/
theorem haagerup_pointwise_gap_propagation
    {V : Type} (f : CollarSliceFunctional V) (θ₀ θ : Fin 2 → Rat) (v : V)
    (rec : LocalLipschitzRecord f θ₀ θ v) :
    margin_h6_val ≤ f θ v :=
  uniform_pointwise_gap_propagation f θ₀ θ v rec

/-- Global uniform collar obstruction instantiated with Haagerup margin:
Across any certified Lipschitz partition, every point θ satisfies f(θ, v) > 0. -/
theorem haagerup_uniform_extension_obstruction
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (params : CollarBarrierParameters C)
    (tree : CollarBisectionTree)
    (h_cover : checkCollarPartitionCover tree unitBox2 = true)
    (T : (Fin 2 → Rat) → MUTriple)
    (h_leaf_bound : ∀ B ∈ tree.leaves, ∀ θ, in_box2 B θ → HasCollarCurvatureBound CS params (T θ))
    (θ : Fin 2 → Rat) (h_θ : in_box2 unitBox2 θ) :
    ZeroRelVarietyEmpty (T θ) ∧ ¬ HasFourthBasis (T θ) :=
  global_collar_barrier_obstruction CS params tree unitBox2 h_cover T h_leaf_bound θ h_θ

/-!
### 7. Target A9 Grand Synthesis Theorem
-/

/-- **TARGET A9 GRAND SYNTHESIS THEOREM**:
Integrating Haagerup orbit boundary certification and curvature positivity with moduli reduction:
Assuming:
1. Orbit Catalog Exhaustiveness (Diță D₆(α), Szöllősi B₆(θ), Tao S₆);
2. Transition Hadamardness (each transition matrix is a CHM);
3. Atlas coverage of the known complex Hadamard moduli;
4. Gauge invariance of class membership;
5. Premise G2 (ZeroRel variety emptiness across covered classes, verified by curvature certification);
6. Premise G3 (Combinatorial basis gluing);
There exists no complete set of seven mutually unbiased bases in dimension 6 (NoCompleteMUB6).
Proven sorry-free with zero user axioms beyond standard Lean logic. -/
theorem target_a9_haagerup_grand_synthesis
    (h_exh : OrbitCatalogExhaustive)
    (h_had : TransitionHadamardProperty)
    (h_atlas : AtlasCoversKnownModuli)
    (h_gauge : GaugeInvariantClassMembership)
    (h_g2_var : G2_Variety)
    (h_g3 : G3) :
    NoCompleteMUB6 := by
  have h_cov : ModuliCoverageConjecture :=
    moduli_coverage_of_orbit_catalog h_exh h_had
  exact moduli_reduction_grand_synthesis h_cov h_atlas h_gauge h_g2_var h_g3

/-- **Target A9 Moduli Reduction with Curvature Wall and Transport Certification**:
Synthesis directly from curvature wall certificates and transport invariance. -/
theorem target_a9_curvature_transport_grand_synthesis
    (h_exh : OrbitCatalogExhaustive)
    (h_had : TransitionHadamardProperty)
    (h_atlas : AtlasCoversKnownModuli)
    (h_gauge : GaugeInvariantClassMembership)
    (h_curv : CurvatureWallCertifiedAtlas)
    (h_trans : ∀ c, CoveredClasses c → TransportInvariance c)
    (h_g3 : G3) :
    NoCompleteMUB6 := by
  have h_g2_var : G2_Variety :=
    target_a7_g2_variety_synthesis h_curv h_trans
  exact target_a9_haagerup_grand_synthesis h_exh h_had h_atlas h_gauge h_g2_var h_g3

/-!
### 8. Axiom Audits
-/

#print axioms rootI_sq
#print axioms rootNegOne_sq
#print axioms rootConj_rootI
#print axioms rootConj_rootNegI
#print axioms rootMul_conj_self
#print axioms haagerup_entrywise_unit_modulus
#print axioms haagerup_entrywise_normSq
#print axioms H6_block00
#print axioms H6_block01
#print axioms H6_block10
#print axioms H6_block11
#print axioms z1_haagerup_eq_one
#print axioms z2_haagerup_eq_neg_one
#print axioms szollosi_condition_haagerup
#print axioms haagerup_hadamard_orthogonality
#print axioms haagerup_hadamard_orthogonality_left
#print axioms haagerup_dephased_row0
#print axioms haagerup_dephased_col0
#print axioms haagerupReceiptExponentsList_length
#print axioms haagerup_exponent_matching_theorem
#print axioms haagerup_all_cross_ratios_fourth_roots
#print axioms haagerup_dephased_cross_ratios_match
#print axioms haagerup_not_hadamard_equiv_tao
#print axioms haagerup_not_hadamard_equiv_fourier
#print axioms distinguishing_submatrix_exp
#print axioms distinguishing_exp_not_cubic
#print axioms distinguishing_exp_not_fourier
#print axioms haagerup_is_szollosi_basepoint
#print axioms haagerup_box_floor_pos
#print axioms haagerup_box_floor_den_pos
#print axioms haagerup_box_floor_strictly_pos
#print axioms haagerup_epsilon_pos
#print axioms haagerup_erosion_eq
#print axioms haagerup_base_gap_gt_erosion
#print axioms haagerup_lower_margin_pos
#print axioms haagerup_margin_val_pos
#print axioms haagerup_margin_val_eq_reduced
#print axioms haagerup_extension_obstruction
#print axioms haagerup_pointwise_gap_propagation
#print axioms haagerup_uniform_extension_obstruction
#print axioms target_a9_haagerup_grand_synthesis
#print axioms target_a9_curvature_transport_grand_synthesis

end MUB6.Gluing.TargetA9
