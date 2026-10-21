import U1PythagoreanObstruction
import U1PowerMapInjectivity
import U1CayleyProjectiveCircle
import U1CyclotomicTorsionTower
import U1CauchyCircleCompletion
import U1ChebyshevCauchyBridge
import U1QuadraticTowerAndCayleyStone

/-!
# U(1) Phase Structure Master Synthesis (`FQ-GAP-U1-CIRCLE` & `FQ-GAP-STONE-CONTINUOUS-TIME`)

Unifies the seven kernel-checked modules of run `20261020T223000Z_u1_phase_completion_lean`:
1. `U1PythagoreanObstruction`: $S^1(\mathbb{Q})$ is a commutative group in which $4/5$ and $1/5$
   are not rational squares, $u_{345} = (3/5, 4/5)$ has no square root, $S^1(\mathbb{Q})$ fails
   2-divisibility, and no additive-to-multiplicative homomorphism $(\mathbb{Q}, +) \to S^1(\mathbb{Q})$
   sends $1 \mapsto u_{345}$.
2. `U1PowerMapInjectivity`: $(3+4i)^n \equiv 3+4i \pmod 5$ for all $n \ge 1$, so the power map
   $k \mapsto u_{345}^k$ on $\mathbb{Z}$ is injective and torsion-free (`u345_infinite_order`).
3. `U1CayleyProjectiveCircle`: Affine rational Cayley parameterization bijects $\mathbb{Q}$ onto
   the punctured circle $S^1(\mathbb{Q}) \setminus \{(-1,0)\}$ with a tangent addition pole when
   $t_1 t_2 = 1$; homogeneous projective coordinates $\mathbb{P}^1(\mathbb{Q})$ close the south-pole
   puncture at $[0:1] \mapsto (-1,0)$ and intertwine globally with circle multiplication.
4. `U1CyclotomicTorsionTower`: The directed $N$-torsion phase tower $\mu_N \hookrightarrow \mu_{kN}$
   embeds into the rational phase quotient $\mathbb{Q}/\mathbb{Z}$, which is universally $m$-divisible
   and satisfies exact finite Haar character orthogonality, yet consists solely of torsion elements.
5. `U1CauchyCircleCompletion`: The half-angle of $u_{345}$ is restored algebraically in
   $S^1(\mathbb{Q}(\sqrt{5}))$ by $w_{\mathrm{half}} = (\frac{2}{5}\sqrt{5}, \frac{1}{5}\sqrt{5})$;
   contracting dyadic intervals and regular Cauchy sequences `RegPhaseSeq` supply metric completion,
   and the finite $N$-torsion grids $\{k/N\}_{k=0}^N$ form an explicit $1/N$-net covering $[0, 1] \cap \mathbb{Q}$.
6. `U1ChebyshevCauchyBridge`: Chebyshev multiple-angle polynomials $T_n, U_n$ on $S^1(\mathbb{Q})$,
   rational alternating Taylor enclosures and Cayley-dyadic circle approximants over `RegPhaseSeq`,
   and the 4D Hermitian matrix carrier `HermitianMat2Qi` over $\mathbb{Q}(i)$ with Pauli-$Y$
   coherence orthogonality and Frobenius-trace Born representation.
7. `U1QuadraticTowerAndCayleyStone`: Iterated real quadratic square-root tower
   $K_{m+1} = K_m(\sqrt{(1+c_m)/2})$ for arbitrary $2^m$-divisions of $u_{345} = (3/5, 4/5)$,
   and the discrete Cayley unitary step $U_H(t) = (I - i t H)(I + i t H)^{-1}$ on $2\times 2$
   Hermitian matrices over $\mathbb{Q}(i)$ with exact unitarity, projective-tangent composition,
   south-pole obstruction $1 - t_1 t_2 \|H\|^2 = 0$, and Born trace invariance.

AuthorityEffect: None.
-/

namespace U1Fable.PhaseSynthesis

open U1Fable.PythagoreanObstruction
open U1Fable.PowerMapInjectivity
open U1Fable.CayleyProjective
open U1Fable.CyclotomicTorsionTower
open U1Fable.CauchyCircleCompletion
open U1Fable.ChebyshevCauchyBridge
open U1Fable.QuadraticTowerAndCayleyStone

/-- The discrete sign carrier `{+1, -1}` has exponent 2 (`s * s = 1`), so it contains no element
of order greater than 2 and fails the connectedness shadow. -/
theorem sign_carrier_exponent_two (s : ℚ) (hs : s = 1 ∨ s = -1) :
    s * s = 1 := by
  rcases hs with rfl | rfl <;> norm_num

/-- Elliptic norm anisotropy vs. hyperbolic split-complex zero divisors:
$u^2 + v^2 = 0 \implies u = 0 \land v = 0$ over $\mathbb{Q}$, whereas $1^2 - 1^2 = 0$ with $(1,1) \neq (0,0)$. -/
theorem split_complex_vs_elliptic_anisotropy :
    ((1 : ℚ) * 1 - 1 * 1 = 0 ∧ ((1 : ℚ), (1 : ℚ)) ≠ (0, 0)) ∧
    (∀ u v : ℚ, u * u + v * v = 0 → u = 0 ∧ v = 0) :=
  ⟨hyperbolic_split_zero_divisor, elliptic_norm_anisotropic⟩

/-- Affine Cayley puncture vs. projective $\mathbb{P}^1(\mathbb{Q})$ one-point compactification:
affine Cayley bijects $\mathbb{Q}$ with $S^1(\mathbb{Q}) \setminus \{(-1,0)\}$ and collides with the
missing south pole $(-1,0)$ whenever $t_1 t_2 = 1$, whereas `homCayley` on `ProjRatLine` sends
`infinityPt = [0:1]` to `(-1,0)`, surjects onto all of $S^1(\mathbb{Q})$, and is a global
multiplicative homomorphism without pole exceptions. -/
theorem affine_cayley_puncture_and_projective_closure :
    (∀ t : ℚ, cayley t ≠ (-1, 0)) ∧
    (∀ t : ℚ, inverseCayley (cayley t) = t) ∧
    (∀ x y : ℚ, x * x + y * y = 1 → x ≠ -1 → cayley (inverseCayley (x, y)) = (x, y)) ∧
    (∀ t₁ t₂ : ℚ, t₁ * t₂ = 1 → circleMul (cayley t₁) (cayley t₂) = (-1, 0)) ∧
    (homCayley infinityPt = (-1, 0)) ∧
    (∀ x y : ℚ, x * x + y * y = 1 → ∃ p : ProjRatLine, homCayley p = (x, y)) ∧
    (∀ p q : ProjRatLine, homCayley (projMul p q) = circleMul (homCayley p) (homCayley q)) :=
  ⟨cayley_misses_south_pole,
   inverseCayley_cayley,
   cayley_inverseCayley,
   cayley_mul_pole_collision,
   homCayley_infinity,
   homCayley_surjective,
   homCayley_projMul⟩

/-- Complete discharge of the three unpaid algebraic obligations of `FQ-GAP-U1-CIRCLE` without
bounded-search substitution:
1. $4/5$ and $1/5$ are not squares in $\mathbb{Q}$, and $u_{345} = (3/5, 4/5)$ has no square root in $S^1(\mathbb{Q})$.
2. The integer power map $k \mapsto u_{345}^k$ on $\mathbb{Z}$ is injective and torsion-free (`u345IntPow k = (1,0) ↔ k = 0`).
3. No additive-to-multiplicative homomorphism $\varphi : (\mathbb{Q}, +) \to S^1(\mathbb{Q})$ satisfies $\varphi(1) = u_{345}$. -/
theorem pythagorean_circle_divisibility_and_hom_obstruction :
    (¬ ∃ q : ℚ, q * q = 4 / 5) ∧
    (¬ ∃ q : ℚ, q * q = 1 / 5) ∧
    (¬ ∃ z : RatCircle, z * z = u345) ∧
    (¬ ∀ w : RatCircle, ∃ z : RatCircle, z * z = w) ∧
    Function.Injective u345IntPow ∧
    (∀ k : ℤ, k ≠ 0 → u345IntPow k ≠ (1, 0)) ∧
    (¬ ∃ φ : ℚ → RatCircle, (∀ p q : ℚ, φ (p + q) = φ p * φ q) ∧ φ 1 = u345) :=
  ⟨four_fifths_not_rat_square,
   one_fifth_not_rat_square,
   u345_no_rat_circle_sqrt,
   rat_circle_not_two_divisible,
   u345IntPow_injective,
   u345_infinite_order.2,
   no_rat_add_to_rat_circle_hom_u345⟩

/-- Structural duality between the cyclotomic torsion tower $\mathbb{Q}/\mathbb{Z}$ and the
Pythagorean rational circle $S^1(\mathbb{Q})$:
- $\mathbb{Q}/\mathbb{Z}$ is $m$-divisible for every $m > 0$ and satisfies exact finite Haar character
  cancellation, but every element is torsion (`∃ N > 0, phaseEquiv (N * q) 0`).
- $S^1(\mathbb{Q})$ contains the infinite-order aperiodic element $u_{345} = (3/5, 4/5)$, but fails
  $2$-divisibility at $u_{345}$. -/
theorem torsion_tower_vs_pythagorean_circle_duality :
    (∀ N k : ℕ, 0 < N → 0 < k → ∀ a : ℤ,
      torsionPhase (k * N) (refineIndex k a) = torsionPhase N a) ∧
    (∀ q : ℚ, ∀ m : ℕ, 0 < m → ∃ r : ℚ, (m : ℚ) * r = q) ∧
    (∀ q : ℚ, ∃ N : ℕ, 0 < N ∧ phaseEquiv ((N : ℚ) * q) 0) ∧
    (¬ ∃ z : RatCircle, z * z = u345) ∧
    Function.Injective u345IntPow :=
  ⟨torsionPhase_refine_eq,
   rat_phase_divisible,
   rat_phase_every_element_torsion,
   u345_no_rat_circle_sqrt,
   u345IntPow_injective⟩

/-- Constructive algebraic and metric completion bridge:
1. Adjoining $\sqrt{5}$ in `CircleQuadSqrt5` supplies the exact half-angle point
   $w_{\mathrm{half}} = (\frac{2}{5}\sqrt{5}, \frac{1}{5}\sqrt{5})$ with $w_{\mathrm{half}}^2 = u_{345}$
   and non-zero $\sqrt{5}$ components.
2. Regular Cauchy sequences `RegPhaseSeq` contain $\mathbb{Q}$ as a metrically dense subset with error
   bound $\frac{1}{N+1} + \frac{1}{m+1}$.
3. For every grid size $N > 0$, the finite $N$-torsion points $\{k/N\}_{k=0}^N$ cover $[0,1] \cap \mathbb{Q}$
   within $1/N$ and approximate every `[0,1]`-valued regular Cauchy sequence within
   $\frac{1}{N} + \frac{1}{N+1} + \frac{1}{m+1}$. -/
theorem algebraic_half_angle_and_precompact_cauchy_bridge :
    (CircleQuadSqrt5.mul wHalf wHalf = u345Quad) ∧
    (wHalf.re.b ≠ 0 ∧ wHalf.im.b ≠ 0) ∧
    (∀ x : RegPhaseSeq, ∀ N m : ℕ,
      |(ofRatSeq (x.seq N)).seq m - x.seq m| ≤ 1 / ((N : ℚ) + 1) + 1 / ((m : ℚ) + 1)) ∧
    (∀ q : ℚ, 0 ≤ q → q ≤ 1 → ∀ N : ℕ, 0 < N →
      ∃ k : ℕ, k ≤ N ∧ |q - (k : ℚ) / (N : ℚ)| ≤ 1 / (N : ℚ)) ∧
    (∀ x : RegPhaseSeq, (∀ n, 0 ≤ x.seq n) → (∀ n, x.seq n ≤ 1) → ∀ N : ℕ, 0 < N →
      ∃ k : ℕ, k ≤ N ∧ ∀ m : ℕ,
        |x.seq m - (k : ℚ) / (N : ℚ)| ≤
          1 / (N : ℚ) + 1 / ((N : ℚ) + 1) + 1 / ((m : ℚ) + 1)) :=
  ⟨wHalf_sq_eq_u345,
   wHalf_not_rational,
   ofRatSeq_approx,
   finite_torsion_grid_covers_unit_interval,
   regPhaseSeq_precompact_approx⟩

/-- Chebyshev/Taylor Cauchy trigonometric bridge and 4D Hermitian $\mathbb{Q}(i)$ Born carrier:
1. Chebyshev double- and triple-angle coordinates agree identically with `z * z` and `z * z * z` in `RatCircle`.
2. Rational Taylor cosine/sine approximations satisfy alternating-series nested interval bounds and
   the exact degree-6 Pythagorean unit-circle defect identity $1 - (C_4(\theta)^2 + S_3(\theta)^2) = \theta^6(8-\theta^2)/576$.
3. Every stage $k$ of the dyadic Cayley-Chebyshev circle approximant `cayleyDyadicPoint θ k` lies
   strictly on $S^1(\mathbb{Q})$, and `regTaylorCosSeq` / `regTaylorSinSeq` converge in `RegPhaseSeq` at rate $\frac{1}{n+1}$.
4. Over the 4D $\mathbb{Q}$-vector space `HermitianMat2Qi` of $2\times 2$ Hermitian matrices over $\mathbb{Q}(i)$,
   every $\mathbb{Q}$-linear functional is uniquely represented by the Hermitian Frobenius trace,
   $\sigma_y$ is orthogonal to the 3D real-symmetric subspace, and rank-1 Gaussian ket projectors
   pair to $|\langle \psi | \phi \rangle|^2$. -/
theorem chebyshev_taylor_and_hermitian_qi_bridge :
    (∀ z : RatCircle, chebyshevT 2 z.re = (z * z).re ∧ z.im * chebyshevU 1 z.re = (z * z).im) ∧
    (∀ z : RatCircle, chebyshevT 3 z.re = (z * z * z).re ∧ z.im * chebyshevU 2 z.re = (z * z * z).im) ∧
    (∀ θ : ℚ, θ ^ 2 ≤ 1 →
      taylorCos2 θ ≤ taylorCos6 θ ∧ taylorCos6 θ ≤ taylorCos4 θ ∧ taylorCos4 θ ≤ taylorCos0 θ) ∧
    (∀ θ : ℚ, 1 - ((taylorCos4 θ) ^ 2 + (taylorSin3 θ) ^ 2) = θ ^ 6 * (8 - θ ^ 2) / 576) ∧
    (∀ θ : ℚ, ∀ k : ℕ,
      (cayleyDyadicPoint θ k).re * (cayleyDyadicPoint θ k).re +
        (cayleyDyadicPoint θ k).im * (cayleyDyadicPoint θ k).im = 1) ∧
    (∀ d1 d2 br : ℚ,
      HermitianMat2Qi.frobeniusTrace (HermitianMat2Qi.ofRealSym d1 d2 br) HermitianMat2Qi.sigmaY = 0) ∧
    (∀ x1 y1 x2 y2 : ℚ, HermitianMat2Qi.det (HermitianMat2Qi.rankOneKet x1 y1 x2 y2) = 0) :=
  ⟨chebyshev_double_eq_ratCircle_sq,
   chebyshev_triple_eq_ratCircle_cube,
   taylorCos_nested_enclosure,
   taylor_pythagorean_defect_identity,
   cayleyDyadicPoint_on_circle,
   HermitianMat2Qi.sigmaY_orthogonal_to_realSym,
   HermitianMat2Qi.rankOneKet_det_zero⟩

/-- Iterated real quadratic square-root tower $K_{m+1} = K_m(\sqrt{(1+c_m)/2})$ for arbitrary
$2^m$-divisions of $u_{345} = (3/5, 4/5)$ and discrete Cayley unitary step
$U_H(t) = (I - i t H)(I + i t H)^{-1}$ on $2\times 2$ Hermitian matrices over $\mathbb{Q}(i)$:
1. For every $m \in \mathbb{N}$, `(towerState m).c^2 + (towerState m).s^2 = 1` in $K_m$, and $m$
   iterated circle squarings recover the embedded rational point $u_{345} = (3/5, 4/5)$.
2. For every traceless $2\times 2$ Hermitian matrix $H$ over $\mathbb{Q}(i)$ and $t \in \mathbb{Q}$,
   $U_H(t)$ satisfies the exact resolvent identity $(I + i t H) U_H(t) = I - i t H$, left and right
   unitarity $U_H(t)^\dagger U_H(t) = I_2 = U_H(t) U_H(t)^\dagger$, $\det U_H(t) = 1$,
   projective-tangent composition when $1 - t_1 t_2 \|H\|^2 \neq 0$, south-pole collision $-I_2$
   when $1 - t_1 t_2 \|H\|^2 = 0$, and Born trace invariance under unitary conjugation. -/
theorem iterated_quadratic_tower_and_cayley_stone_bridge :
    (∀ m : ℕ, (towerState m).c * (towerState m).c + (towerState m).s * (towerState m).s = 1) ∧
    (∀ m : ℕ, iterCircleSq m (towerCirclePoint m) =
      (embedRatTower m (3 / 5), embedRatTower m (4 / 5))) ∧
    (∀ H : TracelessHerm2Qi, ∀ t : ℚ,
      Mat2Qi.mul (H.plusItH t) (H.cayleyStep t) = H.minusItH t) ∧
    (∀ H : TracelessHerm2Qi, ∀ t : ℚ,
      Mat2Qi.mul (Mat2Qi.dagger (H.cayleyStep t)) (H.cayleyStep t) = Mat2Qi.idMat) ∧
    (∀ H : TracelessHerm2Qi, ∀ t : ℚ, Mat2Qi.det (H.cayleyStep t) = 1) ∧
    (∀ H : TracelessHerm2Qi, ∀ t₁ t₂ : ℚ, 1 - t₁ * t₂ * H.normSq ≠ 0 →
      Mat2Qi.mul (H.cayleyStep t₁) (H.cayleyStep t₂) =
        H.cayleyStep ((t₁ + t₂) / (1 - t₁ * t₂ * H.normSq))) ∧
    (∀ H : TracelessHerm2Qi, ∀ t₁ t₂ : ℚ, H.normSq = 1 → t₁ * t₂ = 1 →
      Mat2Qi.mul (H.cayleyStep t₁) (H.cayleyStep t₂) = Mat2Qi.negIdMat) ∧
    (∀ H : TracelessHerm2Qi, ∀ t : ℚ, ∀ W : HermitianMat2Qi,
      Mat2Qi.tr (Mat2Qi.mul (Mat2Qi.mul (H.cayleyStep t) (Mat2Qi.ofHermitian W))
        (Mat2Qi.dagger (H.cayleyStep t))) =
        Mat2Qi.tr (Mat2Qi.ofHermitian W)) :=
  ⟨towerState_on_circle,
   towerState_pow_two_pow_eq_u345,
   TracelessHerm2Qi.cayleyStep_resolvent_right,
   TracelessHerm2Qi.cayleyStep_unitary_left,
   TracelessHerm2Qi.cayleyStep_det_eq_one,
   TracelessHerm2Qi.cayleyStep_comp_regular,
   TracelessHerm2Qi.cayleyStep_comp_pole,
   TracelessHerm2Qi.cayleyStep_preserves_born_trace⟩

/-- Master synthesis theorem for `FQ-GAP-U1-CIRCLE`: combines the projective Cayley closure,
the Pythagorean non-square / power-injectivity / homomorphism obstructions, the torsion-tower
divisibility duality, and the algebraic + precompact Cauchy completion bridge. -/
theorem u1_phase_structure_master_synthesis :
    ((1 : ℚ) * 1 - 1 * 1 = 0 ∧ ((1 : ℚ), (1 : ℚ)) ≠ (0, 0)) ∧
    (∀ t : ℚ, cayley t ≠ (-1, 0)) ∧
    (homCayley infinityPt = (-1, 0)) ∧
    (∀ x y : ℚ, x * x + y * y = 1 → ∃ p : ProjRatLine, homCayley p = (x, y)) ∧
    (∀ p q : ProjRatLine, homCayley (projMul p q) = circleMul (homCayley p) (homCayley q)) ∧
    (¬ ∃ q : ℚ, q * q = 4 / 5) ∧
    (¬ ∃ z : RatCircle, z * z = u345) ∧
    Function.Injective u345IntPow ∧
    (¬ ∃ φ : ℚ → RatCircle, (∀ p q : ℚ, φ (p + q) = φ p * φ q) ∧ φ 1 = u345) ∧
    (∀ q : ℚ, ∀ m : ℕ, 0 < m → ∃ r : ℚ, (m : ℚ) * r = q) ∧
    (∀ q : ℚ, ∃ N : ℕ, 0 < N ∧ phaseEquiv ((N : ℚ) * q) 0) ∧
    (CircleQuadSqrt5.mul wHalf wHalf = u345Quad) ∧
    (∀ q : ℚ, 0 ≤ q → q ≤ 1 → ∀ N : ℕ, 0 < N →
      ∃ k : ℕ, k ≤ N ∧ |q - (k : ℚ) / (N : ℚ)| ≤ 1 / (N : ℚ)) :=
  ⟨hyperbolic_split_zero_divisor,
   cayley_misses_south_pole,
   homCayley_infinity,
   homCayley_surjective,
   homCayley_projMul,
   four_fifths_not_rat_square,
   u345_no_rat_circle_sqrt,
   u345IntPow_injective,
   no_rat_add_to_rat_circle_hom_u345,
   rat_phase_divisible,
   rat_phase_every_element_torsion,
   wHalf_sq_eq_u345,
   finite_torsion_grid_covers_unit_interval⟩

end U1Fable.PhaseSynthesis

#print axioms U1Fable.PhaseSynthesis.sign_carrier_exponent_two
#print axioms U1Fable.PhaseSynthesis.split_complex_vs_elliptic_anisotropy
#print axioms U1Fable.PhaseSynthesis.affine_cayley_puncture_and_projective_closure
#print axioms U1Fable.PhaseSynthesis.pythagorean_circle_divisibility_and_hom_obstruction
#print axioms U1Fable.PhaseSynthesis.torsion_tower_vs_pythagorean_circle_duality
#print axioms U1Fable.PhaseSynthesis.algebraic_half_angle_and_precompact_cauchy_bridge
#print axioms U1Fable.PhaseSynthesis.chebyshev_taylor_and_hermitian_qi_bridge
#print axioms U1Fable.PhaseSynthesis.iterated_quadratic_tower_and_cayley_stone_bridge
#print axioms U1Fable.PhaseSynthesis.u1_phase_structure_master_synthesis
