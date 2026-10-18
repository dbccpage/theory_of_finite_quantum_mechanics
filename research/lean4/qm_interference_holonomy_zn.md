import Mathlib

/-!
# QM_026 attack — interference cross-term as holonomy (GTOC Zₙ regime)

Files the Lean obligations of `general_theory_of_obstruction_calculus/migrations/
qm026_interference_holonomy_attack_packet.md`.

**D1 (this file, first cut).** The two-amplitude interference cross term
`|a+b|² − |a|² − |b|²` is `2·Re(a · conj b)` (carrier-free), and for amplitudes
`r·e^{iα}` it is `2·rₐ·r_b·cos(αₐ − α_b)`. The holonomy `Δα = αₐ − α_b` is the loop
phase difference. The **same** identity holds for a finite root-of-unity carrier
`αₛ = 2π φₛ / n` (the GTOC `Zₙ` shadow) and for the continuum `αₛ ∈ ℝ` (`U(1)`):
the finite case is the continuum identity *sampled*. "Calculus is the limit of
discrete steps" — here the discrete steps are *samples of one continuous identity*.

No authority is minted (GTOC-5): this is a finite algebraic identity about a
declared carrier, not a derivation of the `ℂ`/`U(1)` carrier itself.
-/

namespace QM.InterferenceHolonomy

open Complex

/-- **D1 core (carrier-free).** The interference cross term of two complex amplitudes
is twice the real part of their Hermitian product:
`|a+b|² − |a|² − |b|² = 2·Re(a · conj b)`. -/
theorem cross_eq_two_re (a b : ℂ) :
    Complex.normSq (a + b) - Complex.normSq a - Complex.normSq b
      = 2 * (a * (starRingEnd ℂ) b).re := by
  rw [Complex.normSq_add]; ring

/-- The Hermitian product of two polar amplitudes `rₐ·e^{iαₐ}`, `r_b·e^{iα_b}`
(with real moduli) has real part `rₐ·r_b·cos(αₐ − α_b)`. -/
theorem polar_re (ra rb αa αb : ℝ) :
    (((ra : ℂ) * Complex.exp (αa * I)) *
      (starRingEnd ℂ) ((rb : ℂ) * Complex.exp (αb * I))).re
      = ra * rb * Real.cos (αa - αb) := by
  have ce : (starRingEnd ℂ) (Complex.exp ((αb : ℂ) * I)) = Complex.exp (-((αb : ℂ) * I)) := by
    rw [← Complex.exp_conj]; congr 1
    rw [map_mul, Complex.conj_ofReal, Complex.conj_I]; ring
  have key : ((ra : ℂ) * Complex.exp ((αa : ℂ) * I)) *
      (starRingEnd ℂ) ((rb : ℂ) * Complex.exp ((αb : ℂ) * I))
      = ((ra * rb : ℝ) : ℂ) * Complex.exp (((αa - αb : ℝ) : ℂ) * I) := by
    rw [map_mul, Complex.conj_ofReal, ce]
    have e2 : Complex.exp ((αa : ℂ) * I) * Complex.exp (-((αb : ℂ) * I))
        = Complex.exp (((αa - αb : ℝ) : ℂ) * I) := by
      rw [← Complex.exp_add]; congr 1; push_cast; ring
    calc ((ra : ℂ) * Complex.exp ((αa : ℂ) * I)) * ((rb : ℂ) * Complex.exp (-((αb : ℂ) * I)))
        = ((ra : ℂ) * (rb : ℂ)) *
            (Complex.exp ((αa : ℂ) * I) * Complex.exp (-((αb : ℂ) * I))) := by ring
      _ = ((ra * rb : ℝ) : ℂ) * Complex.exp (((αa - αb : ℝ) : ℂ) * I) := by
            rw [e2]; push_cast; ring
  rw [key, Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im,
      Complex.exp_ofReal_mul_I_re]
  ring

/-- **D1 holonomy / cosine form.** For amplitudes `a = rₐ·e^{iαₐ}`, `b = r_b·e^{iα_b}`,
the interference cross term is `2·rₐ·r_b·cos(αₐ − α_b)`. The phase difference
`Δα = αₐ − α_b` is the two-path loop holonomy. Finite carrier (`αₛ = 2πφₛ/n`,
the `Zₙ` shadow) and continuum carrier are the same identity. -/
theorem cross_eq_cos (ra rb αa αb : ℝ) :
    Complex.normSq ((ra : ℂ) * Complex.exp (αa * I) + (rb : ℂ) * Complex.exp (αb * I))
      - Complex.normSq ((ra : ℂ) * Complex.exp (αa * I))
      - Complex.normSq ((rb : ℂ) * Complex.exp (αb * I))
      = 2 * ra * rb * Real.cos (αa - αb) := by
  rw [cross_eq_two_re, polar_re]; ring

/-- **The QM_026 `(1,1) / (1,−1)` witness as the `n = 2` / `Δα ∈ {0, π}` sample.**
Equal weights `ra = rb = 1`: constructive (`Δα = 0`) gives cross `+2`,
destructive (`Δα = π`) gives cross `−2` — `cos 0 = 1`, `cos π = −1`. -/
theorem witness_constructive :
    Complex.normSq (((1:ℝ) : ℂ) * Complex.exp ((0:ℝ) * I) + ((1:ℝ) : ℂ) * Complex.exp ((0:ℝ) * I))
      - Complex.normSq (((1:ℝ) : ℂ) * Complex.exp ((0:ℝ) * I))
      - Complex.normSq (((1:ℝ) : ℂ) * Complex.exp ((0:ℝ) * I)) = 2 := by
  rw [cross_eq_cos]; simp

theorem witness_destructive :
    Complex.normSq (((1:ℝ) : ℂ) * Complex.exp ((0:ℝ) * I) + ((1:ℝ) : ℂ) * Complex.exp ((Real.pi:ℝ) * I))
      - Complex.normSq (((1:ℝ) : ℂ) * Complex.exp ((0:ℝ) * I))
      - Complex.normSq (((1:ℝ) : ℂ) * Complex.exp ((Real.pi:ℝ) * I)) = -2 := by
  rw [cross_eq_cos]; simp [Real.cos_pi]

/-! ## D2 — the continuum as the certified limit of finite shadows (A6 descent)

The `Zₙ` shadow samples the phase at `αₙ = 2π·hₙ/n`. As the discrete holonomy phase
converges to `Δθ`, the finite cross terms converge to the continuum cross term. This is
"calculus is the limit of discrete steps": the continuum cosine is *reached as a certified
limit of finite, machine-checked shadows* — not parked in Q (cf. A6). By `cross_eq_cos`,
the limand is exactly the interference cross term, so this is the cross-term's certified
descent to the continuum. -/

open Filter Topology in
/-- **D2 — convergence certificate.** If the discrete holonomy phase `α n` (e.g. `2π·hₙ/n`)
tends to `Δθ`, the finite-shadow cross terms `2·rₐ·r_b·cos(α n)` tend to the continuum cross
term `2·rₐ·r_b·cos Δθ`. The infinite is connected, by an actual proof of the limit. -/
theorem cross_Zn_to_U1_refinement (ra rb Δθ : ℝ) (α : ℕ → ℝ)
    (hα : Tendsto α atTop (𝓝 Δθ)) :
    Tendsto (fun n => 2 * ra * rb * Real.cos (α n)) atTop (𝓝 (2 * ra * rb * Real.cos Δθ)) := by
  have hcos : Tendsto (fun n => Real.cos (α n)) atTop (𝓝 (Real.cos Δθ)) :=
    (Real.continuous_cos.tendsto Δθ).comp hα
  simpa using hcos.const_mul (2 * ra * rb)

open Filter Topology in
/-- The roots-of-unity instance: with `hₙ : ℕ → ℝ` and `2π·hₙ/n → Δθ`, the `Zₙ` cross-term
samples converge to the `U(1)` continuum cross term. (Specialization of `cross_Zn_to_U1_refinement`
to `α n = 2π·hₙ/n`.) -/
theorem cross_rootsOfUnity_refinement (ra rb Δθ : ℝ) (h : ℕ → ℝ)
    (hh : Tendsto (fun n => 2 * Real.pi * h n / n) atTop (𝓝 Δθ)) :
    Tendsto (fun n => 2 * ra * rb * Real.cos (2 * Real.pi * h n / n)) atTop
      (𝓝 (2 * ra * rb * Real.cos Δθ)) :=
  cross_Zn_to_U1_refinement ra rb Δθ (fun n => 2 * Real.pi * h n / n) hh

/-! ## D3-floor — interference is the non-L1 resource (finite core)

The full graph-`H¹` biconditional (`H¹ = 0 ⇔ L1-computable ⇔ classically trackable`) is the
follow-on infrastructure; this is its load-bearing base case at one two-path loop. -/

/-- **D3-floor.** For fixed sector weights, the interference cross term is independent of the
holonomy phase — *determined by the L1 / diagonal data alone* — **iff** the configuration is
degenerate (`ra · rb = 0`). Hence any genuine two-path configuration (both weights nonzero) has
a holonomy-dependent cross term: interference is the **non-L1 resource** (QM_026 Part A). The
`(1,1)/(1,−1)` witnesses are the `ra = rb = 1` instance (`cos 0 = +1` vs `cos π = −1`). -/
theorem interference_l1_determined_iff_degenerate (ra rb : ℝ) :
    (∀ Δθ Δθ' : ℝ, 2 * ra * rb * Real.cos Δθ = 2 * ra * rb * Real.cos Δθ') ↔ ra * rb = 0 := by
  constructor
  · intro h
    have key := h 0 Real.pi
    rw [Real.cos_zero, Real.cos_pi] at key
    nlinarith [key]
  · intro h _ _
    have h2 : 2 * ra * rb = 0 := by rw [mul_assoc, h, mul_zero]
    rw [h2, zero_mul, zero_mul]

/-! ## D3-prize core — resource dimension = H¹-rank (the high-D-entanglement direction)

This is the *honest, mechanizable* core of "rank stratifies the resource": `k` independent
two-path loops (each a nonzero-weight `F₂` holonomy) give `2^k` distinct cross-term profiles at
the **same** L1 data, so the L1-invisible interference resource has dimension `k` = the H¹-rank.
It does **not** claim a simulability / complexity separation (that stays the open long shot,
A6-style) — it bounds the *resource dimension*, which is exactly the high-dimensional-entanglement
picture: `k` entangled loops ⇒ `2^k` L1-equivalent-but-distinct configurations. -/

/-- **D3-prize core (resource dimension ≥ rank).** For `k` loops with nonzero weight products,
the map from sign-holonomy vectors (`F₂` holonomy per loop) to cross-term profiles is injective:
the `2^k` holonomy configurations give `2^k` distinct profiles at identical L1 data. -/
theorem holonomy_resource_injective {k : ℕ} (r r' : Fin k → ℝ) (hr : ∀ i, r i * r' i ≠ 0) :
    Function.Injective
      (fun (s : Fin k → Bool) (i : Fin k) =>
        2 * r i * r' i * Real.cos (if s i then Real.pi else 0)) := by
  intro s t hst
  funext i
  have hi : 2 * r i * r' i * Real.cos (if s i then Real.pi else 0)
          = 2 * r i * r' i * Real.cos (if t i then Real.pi else 0) := congrFun hst i
  have hne : (2 : ℝ) * r i * r' i ≠ 0 := by
    have h2 : (2 : ℝ) * r i * r' i = 2 * (r i * r' i) := by ring
    rw [h2]; exact mul_ne_zero two_ne_zero (hr i)
  have hcos : Real.cos (if s i then Real.pi else 0) = Real.cos (if t i then Real.pi else 0) :=
    mul_left_cancel₀ hne hi
  clear hi hne hst
  rcases Bool.eq_false_or_eq_true (s i) with hs | hs <;>
    rcases Bool.eq_false_or_eq_true (t i) with ht | ht <;>
      rw [hs, ht] at hcos ⊢ <;>
      simp only [if_true, if_false, Real.cos_zero, Real.cos_pi] at hcos ⊢ <;>
      first | rfl | (exact absurd hcos (by norm_num))

#print axioms cross_eq_two_re
#print axioms cross_eq_cos
#print axioms witness_destructive
#print axioms cross_Zn_to_U1_refinement
#print axioms interference_l1_determined_iff_degenerate
#print axioms holonomy_resource_injective

end QM.InterferenceHolonomy
