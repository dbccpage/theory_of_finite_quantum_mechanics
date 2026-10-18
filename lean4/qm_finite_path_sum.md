import Mathlib

/-!
QM_042 §5 — finite path-sum = matrix power, and Chapman–Kolmogorov.

Paper: `research/published/qm/QM_042_Finite Path-Sum as Graded Transport`.
Closes ledger claim **QM-042-C5** (ENC-1128, PATHSUM-MXP-001): flips the §5 theorem
from `PROVED-PROSE` + Lean-`TARGETED` (PL-QM042-1) to **MECHANIZED**.

Two clauses, both fully general (any finite index type `ι`, any `CommSemiring R`):

* §5(i) **path-sum = matrix power** — `pathSum_eq_matpow`: the length-`n` path-sum
  over a finite weighted transition matrix `M` equals the `(a,b)` entry of the
  `n`-step propagator `Mⁿ`.
* §5(ii) **Chapman–Kolmogorov** — `matpow_compose`: `M^(m+n) = M^m * M^n`
  (this is `pow_add` in the matrix monoid; channels compose), with the entrywise
  intermediate-node form `matpow_compose_apply` and the path-sum form
  `pathSum_compose`.

This is the matrix-level packaging of the already-checked list-level core
(`QM.FinitePathSumReplay.pathsum_extend_right`, the sliced composition step =
finite-sum right-distributivity) and the Feynman shadow (`QM.FiniteFeynmanShadow`,
ENC-1072). No Born rule, inner product, or phase: the ℂ/U(1) phase carrier and the
continuum path-integral limit stay imported (the paper's firewall). No authority
minted — `StructureDerived ⇏ IsAuth`.

Axioms: standard Mathlib set `[propext, Classical.choice, Quot.sound]` (this file
imports Mathlib for `Matrix`). The Mathlib-free path-sum cousins
(`FinitePathSumReplay`, `FiniteFeynmanShadow`) are `Classical.choice`-free.
-/

namespace QM

open Matrix
open scoped BigOperators

variable {ι R : Type*} [Fintype ι] [DecidableEq ι] [CommSemiring R]

/-- The finite **path-sum** of a weighted transition matrix `M`.
`pathSum M n a b` sums, over every length-`n` walk `a = v₀ → v₁ → ⋯ → vₙ = b`,
the product `M v₀ v₁ · M v₁ v₂ ⋯ M v_{n-1} vₙ` of its declared edge weights.
Defined by the one-step recursion: extend each length-`n` walk by one final edge
`M k b` and sum over the penultimate node `k`. Unfolding `n` times yields exactly
the explicit sum over the `n−1` intermediate nodes. -/
def pathSum (M : Matrix ι ι R) : ℕ → ι → ι → R
  | 0,     a, b => if a = b then 1 else 0
  | n + 1, a, b => ∑ k, pathSum M n a k * M k b

/-- **§5(i): path-sum = matrix power.** The length-`n` path-sum equals the `(a,b)`
entry of the `n`-step propagator `Mⁿ`. Induction on `n`: the base is the identity
matrix, the step is `pow_succ` + `Matrix.mul_apply` (one-step path extension). -/
theorem pathSum_eq_matpow (M : Matrix ι ι R) (n : ℕ) (a b : ι) :
    pathSum M n a b = (M ^ n) a b := by
  induction n generalizing b with
  | zero => simp [pathSum, Matrix.one_apply]
  | succ n ih =>
      rw [pow_succ]
      simp only [pathSum, Matrix.mul_apply]
      exact Finset.sum_congr rfl fun k _ => by rw [ih k]

/-- **§5(ii): Chapman–Kolmogorov (composition).** The `(m+n)`-step propagator is
the product of the `m`-step and `n`-step propagators: `M^(m+n) = M^m * M^n`.
Channels compose; the path-sum monoid. (This is `pow_add` in the matrix monoid.) -/
theorem matpow_compose (M : Matrix ι ι R) (m n : ℕ) :
    M ^ (m + n) = M ^ m * M ^ n :=
  pow_add M m n

/-- Entrywise Chapman–Kolmogorov: the `(a,b)` propagator over `m+n` steps is the
sum over the intermediate node `k` of the `m`-step `a→k` and `n`-step `k→b`
propagators — the finite "sum over histories through a midpoint". -/
theorem matpow_compose_apply (M : Matrix ι ι R) (m n : ℕ) (a b : ι) :
    (M ^ (m + n)) a b = ∑ k, (M ^ m) a k * (M ^ n) k b := by
  rw [matpow_compose, Matrix.mul_apply]

/-- Path-sum form of Chapman–Kolmogorov: the `(m+n)`-step path-sum factors as a
midpoint sum of an `m`-step and an `n`-step path-sum. -/
theorem pathSum_compose (M : Matrix ι ι R) (m n : ℕ) (a b : ι) :
    pathSum M (m + n) a b = ∑ k, pathSum M m a k * pathSum M n k b := by
  simp only [pathSum_eq_matpow]
  exact matpow_compose_apply M m n a b

/-! ### Concrete replay (QM-042-C6 worked example)

The swap kernel `M = !![0,1;1,0]` over `Fin 2` — a deterministic transposition.
`M² = 1` (two swaps return to start) and `M³ = M` (Chapman–Kolmogorov: `M³ = M²·M`). -/

/-- The swap (bit-flip) transition matrix over `Fin 2`. -/
def swap2 : Matrix (Fin 2) (Fin 2) ℕ := !![0, 1; 1, 0]

/-- `M² = 1`: two swaps return every state to itself. -/
theorem swap2_sq : swap2 ^ 2 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [swap2, pow_two, Matrix.mul_apply, Fin.sum_univ_two]

/-- `M³ = M` (Chapman–Kolmogorov `M³ = M²·M`). -/
theorem swap2_cube : swap2 ^ 3 = swap2 := by
  rw [pow_succ, swap2_sq, one_mul]

end QM

#print axioms QM.pathSum_eq_matpow
#print axioms QM.matpow_compose
#print axioms QM.matpow_compose_apply
#print axioms QM.pathSum_compose
#print axioms QM.swap2_sq
#print axioms QM.swap2_cube
