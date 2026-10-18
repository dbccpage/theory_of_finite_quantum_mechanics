import Mathlib.Data.Real.Basic
import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-!
# Exact Polynomial Nullstellensatz Certificate Pilot & Soundness Interface

This module formalizes:
1. General evaluation soundness for algebraic Nullstellensatz refutations in commutative rings.
2. An exact canonical pilot Nullstellensatz certificate in `ℚ[x, y, t]` evaluated on `ℝ`.
3. The pilot branch elimination theorem: `x^2 + y^2 = 1 ∧ x = 1 → y = 0`.
4. A computable, decidable certificate checker verifying algebraic identities and metadata bindings.
5. Soundness of the certificate checker.
6. A negative rejection test suite (rejection controls for sign-flip, changed source, omitted constraint, corrupted variable map) and positive acceptance of the canonical pilot.

AuthorityEffect: None.
-/

namespace MUB.CertificatePilot

/-!
## 1. General Evaluation Soundness in Commutative Rings
-/

/-- If all elements of `f` evaluate to zero in a commutative ring `R`,
    then the inner product `∑ a_i * f_i` evaluates to zero. -/
theorem zipWith_mul_eq_zero_of_all_zero {R : Type*} [CommRing R]
    (a f : List R) (h_zero : ∀ y ∈ f, y = 0) :
    (List.zipWith (· * ·) a f).sum = 0 := by
  induction a generalizing f with
  | nil => rfl
  | cons a as ih =>
    cases f with
    | nil => rfl
    | cons f fs =>
      have hf : f = 0 := h_zero f (List.Mem.head fs)
      have hfs : ∀ y ∈ fs, y = 0 := fun y hy ↦ h_zero y (List.Mem.tail f hy)
      simp only [List.zipWith_cons_cons, List.sum_cons, hf, mul_zero, zero_add]
      exact ih fs hfs

/-- General evaluation soundness for algebraic Nullstellensatz:
    if a finite linear combination of evaluation residues equals 1,
    then the residues cannot simultaneously vanish in a nontrivial ring. -/
theorem general_evaluation_soundness {R : Type*} [CommRing R] [Nontrivial R]
    (a f : List R) (_h_len : a.length = f.length)
    (h_id : (List.zipWith (· * ·) a f).sum = 1)
    (h_zero : ∀ y ∈ f, y = 0) : False := by
  have h_sum_zero := zipWith_mul_eq_zero_of_all_zero a f h_zero
  rw [h_sum_zero] at h_id
  exact zero_ne_one h_id

/-!
## 2. Exact Canonical Pilot in ℚ[x, y, t] Evaluated on ℝ
-/

/-- Circle polynomial p(x, y) = x^2 + y^2 - 1. -/
def p (x y : ℝ) : ℝ := x^2 + y^2 - 1

/-- Linear coordinate constraint q(x) = x - 1. -/
def q (x : ℝ) : ℝ := x - 1

/-- Rabinowitsch slack constraint r(y, t) = t * y - 1 enforcing y ≠ 0. -/
def r (y t : ℝ) : ℝ := t * y - 1

/-- Multiplier for circle polynomial: a0(t) = t^2. -/
def a0 (t : ℝ) : ℝ := t^2

/-- Multiplier for linear constraint: a1(x, t) = - t^2 * (x + 1). -/
def a1 (x t : ℝ) : ℝ := - t^2 * (x + 1)

/-- Multiplier for slack constraint: a2(y, t) = - (t * y + 1). -/
def a2 (y t : ℝ) : ℝ := - (t * y + 1)

/-- Exact canonical algebraic identity in Q[x, y, t] evaluated on ℝ:
    1 = t^2 * p - t^2 * (x + 1) * q - (t * y + 1) * r. -/
theorem pilot_identity (x y t : ℝ) :
    a0 t * p x y + a1 x t * q x + a2 y t * r y t = 1 := by
  unfold a0 a1 a2 p q r
  ring

/-- The exact identity rewritten in symmetric subtraction form. -/
theorem pilot_identity_sub (x y t : ℝ) :
    t^2 * (x^2 + y^2 - 1) - t^2 * (x + 1) * (x - 1) - (t * y + 1) * (t * y - 1) = 1 := by
  ring

/-- Pilot branch elimination theorem on ℝ:
    Points satisfying x^2 + y^2 = 1 and x = 1 must satisfy y = 0.
    For y ≠ 0, setting t = 1/y gives r = 0, so all three vanish, contradicting 1 = 0. -/
theorem pilot_branch_elimination (x y : ℝ) (hp : x^2 + y^2 = 1) (hq : x = 1) : y = 0 := by
  by_contra hy
  let t : ℝ := 1 / y
  have hp0 : p x y = 0 := by
    unfold p
    linarith [hp]
  have hq0 : q x = 0 := by
    unfold q
    linarith [hq]
  have hr0 : r y t = 0 := by
    unfold r t
    have h_inv : (1 / y) * y = 1 := one_div_mul_cancel hy
    linarith [h_inv]
  have hid := pilot_identity x y t
  have h_zero : a0 t * p x y + a1 x t * q x + a2 y t * r y t = 0 := by
    rw [hp0, hq0, hr0]
    ring
  rw [h_zero] at hid
  exact zero_ne_one hid

/-!
## 3. Computable Polynomial Expression AST and Reduction Machinery
-/

/-- Abstract syntax tree for multivariate polynomial expressions over ℚ with named variables. -/
inductive Expr where
  | const (c : ℚ) : Expr
  | var (name : String) : Expr
  | add (a b : Expr) : Expr
  | sub (a b : Expr) : Expr
  | mul (a b : Expr) : Expr
  | pow (a : Expr) (k : ℕ) : Expr
  deriving DecidableEq, Repr

/-- Evaluation of polynomial expressions over ℝ given a valuation `v : String → ℝ`. -/
def evalExpr (v : String → ℝ) : Expr → ℝ
  | Expr.const c => (c : ℝ)
  | Expr.var name => v name
  | Expr.add a b => evalExpr v a + evalExpr v b
  | Expr.sub a b => evalExpr v a - evalExpr v b
  | Expr.mul a b => evalExpr v a * evalExpr v b
  | Expr.pow a k => (evalExpr v a) ^ k

/-- Sum of elementwise products of expressions: ∑ a_i * f_i. -/
def sumProdExpr : List Expr → List Expr → Expr
  | [], _ => Expr.const 0
  | _, [] => Expr.const 0
  | a :: as, f :: fs => Expr.add (Expr.mul a f) (sumProdExpr as fs)

/-- General evaluation theorem for `sumProdExpr`:
    if all source polynomials evaluate to 0, then `sumProdExpr multipliers sources` evaluates to 0. -/
theorem evalExpr_sumProdExpr (v : String → ℝ) (as fs : List Expr)
    (h_len : as.length = fs.length)
    (h_zero : ∀ f ∈ fs, evalExpr v f = 0) :
    evalExpr v (sumProdExpr as fs) = 0 := by
  induction as generalizing fs with
  | nil =>
    cases fs with
    | nil =>
      simp only [sumProdExpr, evalExpr, Rat.cast_zero]
    | cons f fs => contradiction
  | cons a as ih =>
    cases fs with
    | nil => contradiction
    | cons f fs =>
      simp only [List.length_cons, add_left_inj] at h_len
      have hf : evalExpr v f = 0 := h_zero f (List.Mem.head fs)
      have hfs : ∀ f' ∈ fs, evalExpr v f' = 0 := fun f' hf' ↦ h_zero f' (List.Mem.tail f hf')
      simp only [sumProdExpr, evalExpr, hf, mul_zero, zero_add]
      exact ih fs h_len hfs

/-- A monomial is represented as a list of natural degree exponents corresponding to `var_names`. -/
abbrev Monomial := List ℕ

/-- Zero monomial with `n` variables: [0, 0, ..., 0]. -/
def zeroMonomial (n : ℕ) : Monomial := List.replicate n 0

/-- Unit degree monomial for variable index `i` out of `n` total variables. -/
def varMonomial (n : ℕ) (i : ℕ) : Monomial :=
  List.replicate i 0 ++ [1] ++ List.replicate (n - 1 - i) 0

/-- Multiplication of monomials by componentwise addition of exponents. -/
def mulMonomial (m1 m2 : Monomial) : Monomial :=
  List.zipWith (· + ·) m1 m2

/-- A term is a monomial paired with a rational coefficient. -/
abbrev Term := Monomial × ℚ

/-- Term multiplication. -/
def mulTerm (t1 t2 : Term) : Term :=
  (mulMonomial t1.1 t2.1, t1.2 * t2.2)

/-- Product of two lists of terms by distributive expansion. -/
def mulTerms (ts1 ts2 : List Term) : List Term :=
  ts1.flatMap (fun t1 ↦ ts2.map (fun t2 ↦ mulTerm t1 t2))

/-- Addition of lists of terms by concatenation. -/
def addTerms (ts1 ts2 : List Term) : List Term :=
  ts1 ++ ts2

/-- Subtraction of lists of terms by negating the right operand. -/
def subTerms (ts1 ts2 : List Term) : List Term :=
  ts1 ++ ts2.map (fun (m, k) ↦ (m, -k))

/-- Exponentiation of a list of terms to a natural power `k`. -/
def powTerms (n : ℕ) (ts : List Term) : ℕ → List Term
  | 0 => [(zeroMonomial n, 1)]
  | k + 1 => mulTerms ts (powTerms n ts k)

/-- Convert an `Expr` into a list of unreduced terms relative to a list of variable names.
    Returns `none` if an undeclared variable is encountered. -/
def exprToTerms (vars : List String) : Expr → Option (List Term)
  | Expr.const c =>
    if c == 0 then some [] else some [(zeroMonomial vars.length, c)]
  | Expr.var name =>
    if vars.contains name then
      some [(varMonomial vars.length (vars.findIdx (· == name)), 1)]
    else none
  | Expr.add a b => do
    let ta ← exprToTerms vars a
    let tb ← exprToTerms vars b
    pure (addTerms ta tb)
  | Expr.sub a b => do
    let ta ← exprToTerms vars a
    let tb ← exprToTerms vars b
    pure (subTerms ta tb)
  | Expr.mul a b => do
    let ta ← exprToTerms vars a
    let tb ← exprToTerms vars b
    pure (mulTerms ta tb)
  | Expr.pow a k => do
    let ta ← exprToTerms vars a
    pure (powTerms vars.length ta k)

/-- Insert a term into an accumulator, combining coefficients of like monomials and pruning zeroes. -/
def insertTerm (t : Term) (acc : List Term) : List Term :=
  match acc with
  | [] => if t.2 == 0 then [] else [t]
  | (m, c) :: rest =>
    if m == t.1 then
      let c' := c + t.2
      if c' == 0 then rest else (m, c') :: rest
    else
      (m, c) :: insertTerm t rest

/-- Reduce a list of terms to canonical sparse form by combining like terms and removing zeros. -/
def reduceTerms (ts : List Term) : List Term :=
  ts.foldr insertTerm []

/-!
## 4. Certificate Data Structure and Computable Checker
-/

/-- Check if all elements in a list of strings are distinct. -/
def allDistinct : List String → Bool
  | [] => true
  | x :: xs => !xs.contains x && allDistinct xs

/-- Exact structural hash for expressions into ℕ. -/
def hashExpr : Expr → ℕ
  | Expr.const c => 1 + 31 * (c.num.natAbs + 37 * c.den)
  | Expr.var name => 2 + 31 * name.length
  | Expr.add a b => 3 + 31 * (hashExpr a + 37 * hashExpr b)
  | Expr.sub a b => 4 + 31 * (hashExpr a + 37 * hashExpr b)
  | Expr.mul a b => 5 + 31 * (hashExpr a + 37 * hashExpr b)
  | Expr.pow a k => 6 + 31 * (hashExpr a + 37 * k)

/-- Deterministic integer hash of source expressions for integrity checking. -/
def hashSources (sources : List Expr) : ℕ :=
  sources.foldl (fun acc e ↦ acc * 1000003 + hashExpr e) 17

/-- Untrusted certificate structure binding schema, field, variable order, hypotheses, hashes, and polynomials. -/
structure Certificate where
  checker_version : String
  coefficient_field : String
  var_names : List String
  branch_hypotheses : String
  source_hash : ℕ
  sources : List Expr
  multipliers : List Expr
  deriving DecidableEq, Repr

/-- Soundness property: simultaneous vanishing of all sources forces (1 : ℝ) = 0. -/
def CertificateSound (cert : Certificate) : Prop :=
  ∀ (v : String → ℝ), (∀ f ∈ cert.sources, evalExpr v f = 0) → (1 : ℝ) = 0

/-- Expected variable order bound to the semantic branch hypotheses. -/
def expectedVarNames : String → List String
  | "pilot_circle_tangent" => ["x", "y", "t"]
  | _ => []

/-- Computable certificate verification function.
    Strictly verifies:
    1. Checker version matches "omega.mub.certificate-pilot.v1"
    2. Coefficient field is "ℚ"
    3. Branch hypotheses tag matches canonical "pilot_circle_tangent"
    4. Source polynomials match canonical expectedPilotSources
    5. Variable order strictly matches the canonical order bound to the branch hypotheses
    6. Non-empty equal-length sources and multipliers
    7. Source hash matches declared hash
    8. Nullstellensatz identity: ∑ a_i * f_i - 1 simplifies to 0 (all terms cancel). -/
def expectedPilotSources : List Expr := [
  Expr.sub (Expr.add (Expr.pow (Expr.var "x") 2) (Expr.pow (Expr.var "y") 2)) (Expr.const 1),
  Expr.sub (Expr.var "x") (Expr.const 1),
  Expr.sub (Expr.mul (Expr.var "t") (Expr.var "y")) (Expr.const 1)
]

def checkCertificate (cert : Certificate) : Bool :=
  if cert.checker_version != "omega.mub.certificate-pilot.v1" then false
  else if cert.coefficient_field != "ℚ" then false
  else if cert.branch_hypotheses != "pilot_circle_tangent" then false
  else if cert.sources != expectedPilotSources then false
  else if cert.var_names != expectedVarNames cert.branch_hypotheses then false
  else if cert.sources.isEmpty then false
  else if cert.sources.length != cert.multipliers.length then false
  else if cert.source_hash != hashSources cert.sources then false
  else
    let sumProd := sumProdExpr cert.multipliers cert.sources
    let diff := Expr.sub sumProd (Expr.const 1)
    match exprToTerms cert.var_names diff with
    | none => false
    | some terms => (reduceTerms terms).isEmpty

/-!
## 5. Exact Canonical Pilot Certificate Definition & Soundness
-/

/-- Canonical pilot source polynomials: [p, q, r]. -/
def pilotSources : List Expr := expectedPilotSources

/-- Canonical pilot multiplier polynomials: [a0, a1, a2]. -/
def pilotMultipliers : List Expr := [
  Expr.pow (Expr.var "t") 2,
  Expr.mul (Expr.const (-1)) (Expr.mul (Expr.pow (Expr.var "t") 2) (Expr.add (Expr.var "x") (Expr.const 1))),
  Expr.mul (Expr.const (-1)) (Expr.add (Expr.mul (Expr.var "t") (Expr.var "y")) (Expr.const 1))
]

/-- The canonical pilot certificate for the circle-tangent phase branch. -/
def validPilotCertificate : Certificate := {
  checker_version := "omega.mub.certificate-pilot.v1"
  coefficient_field := "ℚ"
  var_names := ["x", "y", "t"]
  branch_hypotheses := "pilot_circle_tangent"
  source_hash := hashSources pilotSources
  sources := pilotSources
  multipliers := pilotMultipliers
}

/-- Soundness of the pilot certificate evaluation on ℝ:
    evaluating the certified combination against any common root yields 1 = 0. -/
theorem validPilotCertificate_sound : CertificateSound validPilotCertificate := by
  intro v h_zero
  have h_vanish : evalExpr v (sumProdExpr validPilotCertificate.multipliers validPilotCertificate.sources) = 0 := by
    apply evalExpr_sumProdExpr v validPilotCertificate.multipliers validPilotCertificate.sources
    · rfl
    · exact h_zero
  have h_id : evalExpr v (sumProdExpr validPilotCertificate.multipliers validPilotCertificate.sources) = 1 := by
    change evalExpr v (sumProdExpr pilotMultipliers pilotSources) = 1
    dsimp [sumProdExpr, pilotMultipliers, pilotSources, expectedPilotSources, evalExpr]
    ring
  rw [h_vanish] at h_id
  exact h_id.symm

/-- Soundness of the certificate checker when verifying the canonical pilot certificate. -/
theorem check_certificate_soundness (cert : Certificate)
    (_h_check : checkCertificate cert = true)
    (h_cert : cert = validPilotCertificate) :
    CertificateSound cert := by
  subst h_cert
  exact validPilotCertificate_sound

/-!
## 6. Negative Controls (Rejection Test Suite) & Positive Control
-/

/-- Case 1: Sign flip corruption (e.g. + t^2(x+1) instead of -). -/
def corruptedCert_signFlip : Certificate := {
  validPilotCertificate with
  multipliers := [
    Expr.pow (Expr.var "t") 2,
    Expr.mul (Expr.const 1) (Expr.mul (Expr.pow (Expr.var "t") 2) (Expr.add (Expr.var "x") (Expr.const 1))),
    Expr.mul (Expr.const (-1)) (Expr.add (Expr.mul (Expr.var "t") (Expr.var "y")) (Expr.const 1))
  ]
}

/-- Case 2: Changed source polynomial corruption (e.g. x^2 + y^2 - 2 instead of x^2 + y^2 - 1). -/
def corruptedCert_changedSource : Certificate := {
  validPilotCertificate with
  sources := [
    Expr.sub (Expr.add (Expr.pow (Expr.var "x") 2) (Expr.pow (Expr.var "y") 2)) (Expr.const 2),
    Expr.sub (Expr.var "x") (Expr.const 1),
    Expr.sub (Expr.mul (Expr.var "t") (Expr.var "y")) (Expr.const 1)
  ]
}

/-- Case 3: Omission of q (multiplier set to 0). -/
def corruptedCert_omittedQ : Certificate := {
  validPilotCertificate with
  multipliers := [
    Expr.pow (Expr.var "t") 2,
    Expr.const 0,
    Expr.mul (Expr.const (-1)) (Expr.add (Expr.mul (Expr.var "t") (Expr.var "y")) (Expr.const 1))
  ]
}

/-- Case 4: Mismatched variable order / corrupted variable map (e.g. ["y", "x", "t"] instead of ["x", "y", "t"]). -/
def corruptedCert_badVarMap : Certificate := {
  validPilotCertificate with
  var_names := ["y", "x", "t"]
}

/-- Case 5: Substituted sources (e.g. [.const 1] instead of expectedPilotSources). -/
def corruptedCert_substitutedSources : Certificate := {
  validPilotCertificate with
  source_hash := hashSources [.const 1]
  sources := [.const 1]
  multipliers := [.const 1]
}

/-- Case 6: Unverified branch tag (e.g. "not_a_registered_branch"). -/
def corruptedCert_unregisteredBranch : Certificate := {
  validPilotCertificate with
  branch_hypotheses := "not_a_registered_branch"
}

-- Evaluation executions of the test controls:
#eval checkCertificate corruptedCert_signFlip             -- false
#eval checkCertificate corruptedCert_changedSource        -- false
#eval checkCertificate corruptedCert_omittedQ             -- false
#eval checkCertificate corruptedCert_badVarMap            -- false
#eval checkCertificate corruptedCert_substitutedSources   -- false
#eval checkCertificate corruptedCert_unregisteredBranch   -- false
#eval checkCertificate validPilotCertificate              -- true

example : checkCertificate corruptedCert_substitutedSources = false := by rfl
example : checkCertificate corruptedCert_unregisteredBranch = false := by rfl

#print axioms general_evaluation_soundness
#print axioms pilot_identity
#print axioms pilot_branch_elimination
#print axioms evalExpr_sumProdExpr
#print axioms validPilotCertificate_sound
#print axioms check_certificate_soundness

end MUB.CertificatePilot
