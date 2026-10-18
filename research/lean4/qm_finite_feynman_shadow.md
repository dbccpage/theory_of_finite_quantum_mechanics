import «semiring_transport_kernel»

/-!
LT-R — finite Feynman shadow replay.

Paper: `12_gtta_feynman_finite_shadow_histories.md` (Part 1).

A finite **history** from one node to another is a list of declared step weights;
its amplitude is the product of those weights, and the Feynman **shadow** `K` is the
sum (over the declared finite history set) of the per-history amplitudes. The
continuum `exp(iS/ħ)` factor is replaced by declared finite weights — there is no
continuum here. The certificate clause: `K` is a **total, deterministic, replayable**
finite function (`shadowK_total`, `shadowK_deterministic`), with a finite
composition law (`shadowK_cons`) and a concrete replay.

Continuum promotion stays out (that is LT-S `ContinuumNonPromotion`). Reuses the
checked `SemiringTransportKernel` path-sum core; Mathlib-free; no authority minted.
-/

namespace QM

open OmegaCosmology.Primitives.SemiringTransportKernel

/-- Amplitude of one finite history = product of its declared step weights. -/
def histAmp {R : Type} [FWSemiring R] : List R → R
  | []      => FWSemiring.one
  | w :: ws => FWSemiring.mul w (histAmp ws)

/-- The finite Feynman shadow: the path-sum over a declared finite history set of
each history's amplitude. -/
def shadowK {R : Type} [FWSemiring R] (histories : List (List R)) : R :=
  lsum (histories.map histAmp)

/-- **Totality / replayability.** `K` is a well-defined finite value for every
declared finite history set (it is the path-sum of the history amplitudes). -/
theorem shadowK_total {R : Type} [FWSemiring R] (histories : List (List R)) :
    shadowK histories = lsum (histories.map histAmp) := rfl

/-- **Deterministic replay.** Equal declared history sets give equal shadows. -/
theorem shadowK_deterministic {R : Type} [FWSemiring R] (h1 h2 : List (List R))
    (h : h1 = h2) : shadowK h1 = shadowK h2 := by rw [h]

/-- **Finite composition law.** Adjoining one more declared history adds its
amplitude to the shadow. -/
theorem shadowK_cons {R : Type} [FWSemiring R] (hist : List R) (rest : List (List R)) :
    shadowK (hist :: rest) = FWSemiring.add (histAmp hist) (shadowK rest) := rfl

/-- Concrete finite replay over ℕ: histories `[2,3]` (amplitude `2·3=6`) and `[5]`
(amplitude `5·1=5`) give shadow `6 + 5 = 11`. -/
theorem shadowK_replay : shadowK (R := Nat) [[2, 3], [5]] = 11 := by decide

end QM

#print axioms QM.shadowK_total
#print axioms QM.shadowK_deterministic
#print axioms QM.shadowK_cons
#print axioms QM.shadowK_replay
