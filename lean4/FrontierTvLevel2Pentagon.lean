import DiscreteSpinfoamAmplitudes
import FourSimplexSpinfoamS4

/-!
# Quantum 6j orthogonality and Biedenharn-Elliott pentagon identity at level 2
(LQG-TV-LEVEL2-PENTAGON-TARGET)

AuthorityEffect: None.
Scope: Exact arithmetic in `Q(√2)` (scaled by 2 as `Z[√2]` / `Rat(√2)`) for the `SU(2)_2`
(`q = exp(i π / 4)`) quantum recoupling symbols (`ising_f` and `ising_six_j_radical` of
`code/rust/src/general_relativity/spin_foam.rs`) on twice-spin labels `{0, 1, 2}`
(spins `0, 1/2, 1`), together with the `Z[ζ_{12}]` tetrahedral phase cocycle of `DiscreteSpinfoamAmplitudes` and `FourSimplexSpinfoamS4`.
Proves:
1. Quantum dimensions at `q = exp(i π / 4)`: `d_0 = 1`, `d_1 = √2`, `d_2 = 1`, and `d_3 = [4]_q = 0`
   (the level-2 truncation boundary).
2. Exact table of the normalized quantum 6j / F-symbols `isingF(a, b, c, d, e, f)` in `Q(√2)` for all
   `3^6 = 729` label 6-tuples (`36` nonzero entries, taking values in `{±1, ±√2/2}`).
3. Exact orthogonality relation
   `∑_f isingF(a, b, c, d, e, f) * isingF(a, b, c, d, e', f) = δ_{e, e'}`
   (equivalently `∑_f d_e d_f {a b e; c d f}_q {a b e'; c d f}_q = δ_{e, e'}`) across all admissible
   tuples `(a, b, c, d, e, e')` in `{0, 1, 2}^6`.
4. Exact quantum Biedenharn-Elliott (pentagon) identity
   `∑_r isingF(a, b, c, q, p, r) * isingF(a, r, d, e, q, s) * isingF(b, c, d, s, r, t)`
   `= isingF(p, c, d, e, q, t) * isingF(a, b, t, e, p, s)`
   across all `3^9 = 19,683` label 9-tuples `(a, b, c, d, e, p, q, s, t) ∈ {0, 1, 2}^9` with
   admissible bipyramid boundary triangles.
-/

namespace FrontierTvLevel2Pentagon

/-- Kernel-reducible canonical reduced fraction `num / den` (`den > 0`, `gcd(|num|, den) = 1`). -/
structure Frac where
  num : Int
  den : Nat
  deriving DecidableEq, Repr

namespace Frac

def mkNorm (n : Int) (d : Nat) : Frac :=
  if d == 0 || n == 0 then ⟨0, 1⟩
  else
    let g := Nat.gcd n.natAbs d
    ⟨n / (g : Int), d / g⟩

def zero : Frac := ⟨0, 1⟩
def one : Frac := ⟨1, 1⟩
def negOne : Frac := ⟨-1, 1⟩
def half : Frac := ⟨1, 2⟩
def nhalf : Frac := ⟨-1, 2⟩
def two : Frac := ⟨2, 1⟩

def add (a b : Frac) : Frac :=
  if a == zero then b
  else if b == zero then a
  else mkNorm (a.num * (b.den : Int) + b.num * (a.den : Int)) (a.den * b.den)

def sub (a b : Frac) : Frac :=
  mkNorm (a.num * (b.den : Int) - b.num * (a.den : Int)) (a.den * b.den)

def mul (a b : Frac) : Frac :=
  if a == zero || b == zero then zero
  else mkNorm (a.num * b.num) (a.den * b.den)

def neg (a : Frac) : Frac := ⟨-a.num, a.den⟩

instance : Zero Frac := ⟨zero⟩
instance : One Frac := ⟨one⟩
instance : Add Frac := ⟨add⟩
instance : Sub Frac := ⟨sub⟩
instance : Mul Frac := ⟨mul⟩
instance : Neg Frac := ⟨neg⟩

end Frac

/-- Elements of `Q(√2)` represented by `re + rt2 * √2` with `re, rt2 : Frac`. -/
structure QSqrt2 where
  re : Frac
  rt2 : Frac
  deriving DecidableEq, Repr

namespace QSqrt2

def zero : QSqrt2 := ⟨Frac.zero, Frac.zero⟩
def one : QSqrt2 := ⟨Frac.one, Frac.zero⟩
def negOne : QSqrt2 := ⟨Frac.negOne, Frac.zero⟩
def sqrt2 : QSqrt2 := ⟨Frac.zero, Frac.one⟩
def halfSqrt2 : QSqrt2 := ⟨Frac.zero, Frac.half⟩
def negHalfSqrt2 : QSqrt2 := ⟨Frac.zero, Frac.nhalf⟩

def add (x y : QSqrt2) : QSqrt2 :=
  if x == zero then y
  else if y == zero then x
  else ⟨x.re + y.re, x.rt2 + y.rt2⟩
def sub (x y : QSqrt2) : QSqrt2 := ⟨x.re - y.re, x.rt2 - y.rt2⟩
def neg (x : QSqrt2) : QSqrt2 := ⟨-x.re, -x.rt2⟩
def mul (x y : QSqrt2) : QSqrt2 :=
  if x == zero || y == zero then zero
  else ⟨x.re * y.re + Frac.two * x.rt2 * y.rt2, x.re * y.rt2 + x.rt2 * y.re⟩

instance : Zero QSqrt2 := ⟨zero⟩
instance : One QSqrt2 := ⟨one⟩
instance : Add QSqrt2 := ⟨add⟩
instance : Sub QSqrt2 := ⟨sub⟩
instance : Neg QSqrt2 := ⟨neg⟩
instance : Mul QSqrt2 := ⟨mul⟩

end QSqrt2

open QSqrt2

/-- `SU(2)_2` fusion admissibility on twice-spins `a, b, c ∈ {0, 1, 2}` (`spin_foam.rs::ising_admissible`). -/
def isingAdmissible (a b c : Nat) : Bool :=
  (a ≤ 2) && (b ≤ 2) && (c ≤ 2) &&
  (a + b ≥ c) && (a + c ≥ b) && (b + c ≥ a) &&
  ((a + b + c) % 2 == 0) && (a + b + c ≤ 4)

/-- Quantum dimension `[2j + 1]_q` at `q = exp(i π / 4)`:
`[1]_q = 1`, `[2]_q = √2`, `[3]_q = 1`, `[4]_q = 0`. -/
def qDimLevel2 : Nat → QSqrt2
  | 0 => one
  | 1 => sqrt2
  | 2 => one
  | _ => zero

/-- Quantum factorial `[n]_q!` at `q = exp(i π / 4)` for `n ≤ 3`:
`[0]_q! = 1`, `[1]_q! = 1`, `[2]_q! = √2`, `[3]_q! = √2`. -/
def qFactorialLevel2 : Nat → QSqrt2
  | 0 => one
  | 1 => one
  | 2 => sqrt2
  | 3 => sqrt2
  | _ => zero

theorem level2_quantum_dimensions_and_truncation :
    qDimLevel2 0 = one ∧
    qDimLevel2 1 = sqrt2 ∧
    qDimLevel2 2 = one ∧
    qDimLevel2 1 * qDimLevel2 1 - qDimLevel2 0 = qDimLevel2 2 ∧
    qDimLevel2 1 * qDimLevel2 2 - qDimLevel2 1 = zero := by
  decide

/-- Exact normalized quantum recoupling symbol `isingF(a, b, c, d, e, f)` in `Q(√2)` matching
`code/rust/src/general_relativity/spin_foam.rs::ising_f`.
When `(a,b,e), (e,c,d), (b,c,f), (a,f,d)` are admissible:
- If `a = b = c = d = 1` (four spin-1/2 legs, so `e, f ∈ {0, 2}`), the 2x2 F-matrix on `{0, 2}` is
  `(1/√2) [[1, 1], [1, -1]]`, i.e. `-halfSqrt2` when `e = 2 ∧ f = 2` and `+halfSqrt2` otherwise.
- If two adjacent external legs are `1` and the other two are `2`, with intermediate `1`, the sign
  from `(-1)^((a+b+c+d)/2)` and the Racah sum `z = 2` vs `z = 3` gives `-1` when
  `(a,b,c,d,e,f)` is `(1,2,1,2,1,1)` or `(2,1,2,1,1,1)`, and `+1` on all other admissible tuples. -/
def isingF (a b c d e f : Nat) : QSqrt2 :=
  if !(isingAdmissible a b e && isingAdmissible e c d &&
       isingAdmissible b c f && isingAdmissible a f d) then
    zero
  else if a == 1 && b == 1 && c == 1 && d == 1 then
    if e == 2 && f == 2 then negHalfSqrt2 else halfSqrt2
  else if (a == 1 && b == 2 && c == 1 && d == 2 && e == 1 && f == 1) ||
          (a == 2 && b == 1 && c == 2 && d == 1 && e == 1 && f == 1) then
    negOne
  else
    one

def labels3 : List Nat := [0, 1, 2]

/-- Count of nonzero `isingF` symbols across all `3^6 = 729` label 6-tuples is 36. -/
def nonzeroIsingFCount : Nat :=
  (labels3.flatMap fun a =>
   labels3.flatMap fun b =>
   labels3.flatMap fun c =>
   labels3.flatMap fun d =>
   labels3.flatMap fun e =>
   labels3.filter fun f => decide (isingF a b c d e f ≠ zero)).length

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
theorem isingF_nonzero_count_36 : nonzeroIsingFCount = 36 := by
  decide

/-- Exact orthogonality relation: for all `a, b, c, d, e, ep ∈ {0, 1, 2}` with admissible channels
`(a,b,e), (e,c,d), (a,b,ep), (ep,c,d)`,
`∑_{f ∈ {0,1,2}} isingF(a,b,c,d,e,f) * isingF(a,b,c,d,ep,f) = δ_{e, ep}`. -/
def checkOrthogonalityAt (a b c d e ep : Nat) : Bool :=
  if isingAdmissible a b e && isingAdmissible e c d &&
     isingAdmissible a b ep && isingAdmissible ep c d then
    let lhs := labels3.foldl (fun acc f => acc + isingF a b c d e f * isingF a b c d ep f) zero
    let rhs := if e == ep then one else zero
    decide (lhs = rhs)
  else
    true

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
theorem level2_orthogonality_all_admissible :
    (labels3.all fun a =>
     labels3.all fun b =>
     labels3.all fun c =>
     labels3.all fun d =>
     labels3.all fun e =>
     labels3.all fun ep =>
       checkOrthogonalityAt a b c d e ep) = true := by
  decide

/-- Exact quantum Biedenharn-Elliott (pentagon) identity across all `3^9 = 19,683` label 9-tuples
`(a, b, c, d, e, p, q, s, t) ∈ {0, 1, 2}^9`:
whenever the 6 boundary fusion triangles of the 2-3 Pachner bipyramid are admissible,
`∑_{r ∈ {0,1,2}} isingF(a,b,c,q,p,r) * isingF(a,r,d,e,q,s) * isingF(b,c,d,s,r,t)`
`= isingF(p,c,d,e,q,t) * isingF(a,b,t,e,p,s)`. -/
def checkPentagonAt (a b c d e p q s t : Nat) : Bool :=
  let bdy :=
    isingAdmissible a b p && isingAdmissible p c q && isingAdmissible q d e &&
    isingAdmissible c d t && isingAdmissible b t s && isingAdmissible a s e
  let lhs :=
    labels3.foldl
      (fun acc r => acc + isingF a b c q p r * isingF a r d e q s * isingF b c d s r t)
      zero
  let rhs := if bdy then isingF p c d e q t * isingF a b t e p s else zero
  decide (lhs = rhs)

set_option maxRecDepth 20000 in
set_option maxHeartbeats 1600000 in
theorem level2_quantum_pentagon_identity_all_19683 :
    (labels3.all fun a =>
     labels3.all fun b =>
     labels3.all fun c =>
     labels3.all fun d =>
     labels3.all fun e =>
     labels3.all fun p =>
     labels3.all fun q =>
     labels3.all fun s =>
     labels3.all fun t =>
       checkPentagonAt a b c d e p q s t) = true := by
  decide

end FrontierTvLevel2Pentagon

#print axioms FrontierTvLevel2Pentagon.level2_quantum_dimensions_and_truncation
#print axioms FrontierTvLevel2Pentagon.isingF_nonzero_count_36
#print axioms FrontierTvLevel2Pentagon.level2_orthogonality_all_admissible
#print axioms FrontierTvLevel2Pentagon.level2_quantum_pentagon_identity_all_19683

private def l5aProvenance : String :=
  "Origin: lean4/FrontierTvLevel2Pentagon.lean Claim: level2_quantum_pentagon_identity_all_19683 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
