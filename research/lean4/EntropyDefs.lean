-- Definitions.lean — Finite Quantum Rational Spectra & Logarithmic Forms
-- Campaign: C750 Block 01 (Target C750-T568)
-- AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

namespace FiniteQm.C750.B01

/-- Exact rational number represented as integer numerator and positive natural denominator.
    Purposely avoids Lean core's stock `Rat`, which depends on `Classical.choice`.
    All operations are constructive and choice-free. -/
structure RatFrac where
  num : Int
  den : Nat
  den_pos : 0 < den
deriving Repr

namespace RatFrac

/-- Zero rational 0/1. -/
def zero : RatFrac := ⟨0, 1, Nat.zero_lt_one⟩

/-- Unit rational 1/1. -/
def one : RatFrac := ⟨1, 1, Nat.zero_lt_one⟩

/-- Exact rational addition: a/b + c/d = (a*d + c*b)/(b*d). -/
def add (x y : RatFrac) : RatFrac :=
  ⟨x.num * (y.den : Int) + y.num * (x.den : Int), x.den * y.den, Nat.mul_pos x.den_pos y.den_pos⟩

/-- Exact rational negation: -(a/b) = (-a)/b. -/
def neg (x : RatFrac) : RatFrac :=
  ⟨-x.num, x.den, x.den_pos⟩

/-- Exact rational subtraction. -/
def sub (x y : RatFrac) : RatFrac :=
  add x (neg y)

/-- Exact rational multiplication: (a/b) * (c/d) = (a*c)/(b*d). -/
def mul (x y : RatFrac) : RatFrac :=
  ⟨x.num * y.num, x.den * y.den, Nat.mul_pos x.den_pos y.den_pos⟩

/-- Exact scalar multiplication by integer: c * (a/b) = (c*a)/b. -/
def smul (c : Int) (x : RatFrac) : RatFrac :=
  ⟨c * x.num, x.den, x.den_pos⟩

/-- Predicate for vanishing rational: a/b = 0 iff a = 0. -/
def isZero (x : RatFrac) : Prop := x.num = 0

end RatFrac

/-- An exact rational density operator spectrum in arbitrary finite dimension `d ≥ 1`.
    The spectrum consists of `d` non-negative integer eigenvalue weights normalized
    by a common strictly positive integer denominator `denom`.
    This satisfies `lean_general_d: true`. -/
structure RationalDensity (d : Nat) where
  dim_pos : 0 < d
  weights : List Nat
  length_eq : weights.length = d
  denom : Nat
  denom_pos : 0 < denom
  trace_eq : weights.sum = denom

namespace RationalDensity

/-- The unnormalized purity moment: Tr(rho^2) * denom^2 = sum_j w_j^2. -/
def purity_num (rho : RationalDensity d) : Nat :=
  (rho.weights.map (fun w => w * w)).sum

/-- A density operator is pure iff Tr(rho^2) = 1, i.e., sum_j w_j^2 = denom^2. -/
def is_pure (rho : RationalDensity d) : Prop :=
  purity_num rho = rho.denom * rho.denom

/-- A density operator is mixed iff it is not pure, i.e., Tr(rho^2) < 1. -/
def is_mixed (rho : RationalDensity d) : Prop :=
  ¬ is_pure rho

end RationalDensity

/-- A linear form in logarithms of prime bases: sum_{i=1}^m c_i * log(p_i),
    with rational coefficients c_i in Q. -/
structure LinearFormInLogarithms where
  basis : List Nat
  coeffs : List RatFrac
  len_eq : basis.length = coeffs.length

namespace LinearFormInLogarithms

/-- The linear form is non-vanishing if at least one rational coefficient has non-zero numerator. -/
def is_nonvanishing (form : LinearFormInLogarithms) : Prop :=
  ∃ c ∈ form.coeffs, c.num ≠ 0

/-- The linear form vanishes identically iff all rational coefficients are zero. -/
def is_zero (form : LinearFormInLogarithms) : Prop :=
  ∀ c ∈ form.coeffs, c.num = 0

end LinearFormInLogarithms

/-- Removable singularity convention for the entropy term:
    0 * log(0) := lim_{x -> 0^+} x * log(x) = 0.
    A zero eigenvalue weight contributes exactly 0 to the linear form in logarithms. -/
def removable_singularity_term (w : Nat) (log_val : RatFrac) : RatFrac :=
  if w = 0 then RatFrac.zero else RatFrac.mul ⟨(w : Int), 1, Nat.zero_lt_one⟩ log_val

theorem removable_singularity_zero (log_val : RatFrac) :
    removable_singularity_term 0 log_val = RatFrac.zero := by
  rfl

end FiniteQm.C750.B01
