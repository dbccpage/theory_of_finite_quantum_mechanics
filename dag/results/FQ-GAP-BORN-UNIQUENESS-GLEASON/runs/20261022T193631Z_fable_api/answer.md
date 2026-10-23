# Frame functions on Gaussian-rational rays in dimension 3

## 1. Mathematical argument (prose)

**Status.** I could not decide (A) vs (B). What is proved, in three Lean files, is the largest honest piece I can establish without tools:

1. **Over ℚ (new, strengthens the repository).** The repository's parity obstruction lives only on the rational *unit sphere* (rays with square norm). I construct an explicit frame function on **all** rational rays of ℚ³ — i.e. on all integer vectors not all of whose coordinates are even — prove frame additivity for *every* pairwise orthogonal triple of such vectors (no square‑norm hypothesis), prove it is well defined on rays (invariant under sign and odd scalings), and prove no rational symmetric form represents it.

   Construction. For `v = (a,b,c) ∈ ℤ³` not all even, let `sgn v ∈ {−1,0,1}` be `0` unless exactly two coordinates `x,y` are odd, in which case `sgn v = −1` if `x ≡ y (mod 4)` and `+1` if `x ≡ −y (mod 4)`; put `exotic v = (1 + sgn v)/3 ∈ {0, 1/3, 2/3}`.

   Additivity. Reducing mod 2, orthogonality says the two vectors share an even number of odd positions. Hence an orthogonal triple has odd‑position sets of one of the shapes `{e_i,e_j,e_k}`, `{e_i, ε_i, ε_i}`, `{τ, ε_i, ε_i}` where `ε_i` is the two‑element set avoiding `i` and `τ = {1,2,3}`; `{ε_i,ε_i,ε_i}` is excluded by the mod‑4 lemma below (pigeonhole). The only nonzero contributions come from a pair `v,w` with the same two odd positions `x,y` and the third coordinate even. Then `x x' + y y' ≡ 0 (mod 4)` (the even·even product is `0 mod 4`), and for odd `x,x'` one has `x x' ≡ 1` iff `x ≡ x' (mod 4)`, else `≡ 3`; so exactly one of `x≡x'`, `y≡y'` holds, which forces `sgn v + sgn w = 0`. Hence `sgn u + sgn v + sgn w = 0` on every frame, i.e. `exotic` sums to `1`.

   Non‑quadraticity. `exotic = 1/3` on `e₁,e₂,e₃,(1,1,1)` and `0` on `(1,1,0),(1,0,1),(0,1,1)`. A representing form would need `r_ii = 1/3`, `r_ij = −1/3`, and then takes value `−1 ≠ 1` on `(1,1,1)`.

   Consequence for the K‑question: real frames are K‑frames, so any frame function on `ℚ(i)³`‑rays restricts to a ℚ‑frame function; option (B) over `K` would therefore require that *no* exotic ℚ‑function (in particular this one) extends to all `K`‑rays.

2. **Over K = ℚ(i): the parity route suggested in the problem is closed.** Let `π = 1+i`; `π ∣ a+bi ⇔ a ≡ b (mod 2)`. Reduction of a primitive Gaussian‑integer vector mod `π` gives the same seven classes as over ℚ. But over `ℤ[i]` there is a **non‑real triangle frame all of whose members lie in the class `(1,1,0)`**:
   `(1,1,0), (1,−1,1+i), (1,−1,−1−i)` (pairwise Hermitian‑orthogonal: `1−1+(1−i)(−1−i)=2−2=0`). No such triangle exists over ℚ (proved: `no_real_triangle`). Using this triangle (and its two coordinate permutations) together with the real frames `(e₃,(1,1,0),(1,−1,0))`, `(e₁,(0,1,1),(0,1,−1))`, `(e₂,(1,0,1),(1,0,−1))`, `((1,1,1),(1,−1,0),(1,1,−2))`, the seven class values satisfy `3c₁₁₀=3c₁₀₁=3c₀₁₁=1`, `c₀₀₁+2c₁₁₀=1`, `c₁₀₀+2c₀₁₁=1`, `c₀₁₀+2c₁₀₁=1`, `c₁₁₁+2c₁₁₀=1`, so **every (1+i)-parity-class frame function is the constant 1/3** on primitive Gaussian‑integer vectors — which is the Born function of `ρ = I/3`. So the Meyer/Godsil–Zaks parity argument cannot produce a non‑quadratic frame function over `ℚ(i)`; a finer invariant (deeper `π`‑adic data, or another prime) would be needed, and my attempts to refine mod `π³`, `π⁴` collapsed to zero under the triangle relations.

3. **Ray invariance over K.** Every nonzero `v ∈ K³` completes to a frame `(v,w,u)` with `w,u` independent of rescaling `v`; hence any frame function on vectors is automatically constant on rays (`f(λv) = f(v)` for `λ ≠ 0`). This justifies working with vector‑valued frame functions in the Lean statements.

**What is missing for (A):** a function on *all* Gaussian‑rational rays, additive on *all* K‑frames and non‑quadratic. **What is missing for (B):** a Gleason‑type rigidity argument over `ℚ(i)³`, which cannot proceed via continuity; equivalently, a proof that the ℚ‑exotic function above does not extend. Neither is claimed.

## 2. Lean files

```lean
-- FILE: lean4/BornRationalPlaneObstruction.lean
import BornRationalSphereObstruction
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# An exotic frame function on *all* rational rays of `ℚ³`

AuthorityEffect: None.

Scope.  `BornRationalSphereObstruction` works on the rational *unit sphere* (integer vectors with
square norm).  Here the carrier is every integer vector `v = (a, b, c)` with not all coordinates
even (`IsPrimitive`); every rational ray of `ℚ³` has such a representative, and two such
representatives of the same ray differ by a factor `p/q` with `p, q` odd.

`sgn v ∈ {-1, 0, 1}` is `0` unless exactly two coordinates `x, y` are odd, in which case it is
`-1` if `x ≡ y (mod 4)` and `1` if `x ≡ -y (mod 4)`.  `exotic v = (1 + sgn v) / 3`.

Main results:
* `exotic_frame_function`: on every pairwise orthogonal triple of primitive vectors the values of
  `exotic` sum to `1` (no square-norm hypothesis).
* `exotic_eq_of_odd_scalings`, `exotic_neg`: `exotic` is a function of the rational ray.
* `exotic_not_quadratic`: no rational symmetric `3 × 3` form represents `exotic`.
* `exotic_eq_third_of_isRay`: on the rational unit sphere `exotic` is the constant `1/3`.
* `no_real_triangle`: over `ℤ³` there is no orthogonal triple all of whose members are
  `≡ (1,1,0) (mod 2)` (contrast with the Gaussian case in `BornGaussianRationalFrameObstruction`).

Nothing here is a statement about physics.
-/

namespace BornFable.RationalPlane

open BornFable.RationalSphere

/-- `v ∈ ℤ³` is *odd-primitive*: not all coordinates are even. -/
def IsPrimitive (v : Vec3) : Prop := ¬ (v.a % 2 = 0 ∧ v.b % 2 = 0 ∧ v.c % 2 = 0)

theorem isPrimitive_of_isRay {v : Vec3} (h : v.IsRay) : IsPrimitive v := by
  intro hc
  exact h.1 ⟨Int.even_iff.mpr hc.1, Int.even_iff.mpr hc.2.1, Int.even_iff.mpr hc.2.2⟩

/-- For odd `x, y`: `-1` if `x ≡ y (mod 4)`, `1` if `x ≡ -y (mod 4)`. -/
def pairSign (x y : ℤ) : ℤ := if (x - y) % 4 = 0 then -1 else 1

/-- The sign invariant: nonzero exactly when exactly two coordinates are odd. -/
def sgn (v : Vec3) : ℤ :=
  if v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0 then pairSign v.a v.b
  else if v.a % 2 = 1 ∧ v.c % 2 = 1 ∧ v.b % 2 = 0 then pairSign v.a v.c
  else if v.b % 2 = 1 ∧ v.c % 2 = 1 ∧ v.a % 2 = 0 then pairSign v.b v.c
  else 0

/-- The exotic frame function, with values in `{0, 1/3, 2/3}`. -/
def exotic (v : Vec3) : ℚ := (1 + sgn v) / 3

/-! ### Specification of `sgn` by congruences -/

/-- Complete case description of `sgn ⟨a, b, c⟩`. -/
theorem sgn_spec (a b c : ℤ) :
    (a % 2 = 1 ∧ b % 2 = 1 ∧ c % 2 = 0 ∧
        (((a - b) % 4 = 0 ∧ sgn ⟨a, b, c⟩ = -1) ∨ ((a - b) % 4 ≠ 0 ∧ sgn ⟨a, b, c⟩ = 1))) ∨
    (a % 2 = 1 ∧ c % 2 = 1 ∧ b % 2 = 0 ∧
        (((a - c) % 4 = 0 ∧ sgn ⟨a, b, c⟩ = -1) ∨ ((a - c) % 4 ≠ 0 ∧ sgn ⟨a, b, c⟩ = 1))) ∨
    (b % 2 = 1 ∧ c % 2 = 1 ∧ a % 2 = 0 ∧
        (((b - c) % 4 = 0 ∧ sgn ⟨a, b, c⟩ = -1) ∨ ((b - c) % 4 ≠ 0 ∧ sgn ⟨a, b, c⟩ = 1))) ∨
    (((a % 2 = 0 ∧ b % 2 = 0 ∧ c % 2 = 0) ∨ (a % 2 = 1 ∧ b % 2 = 0 ∧ c % 2 = 0) ∨
        (a % 2 = 0 ∧ b % 2 = 1 ∧ c % 2 = 0) ∨ (a % 2 = 0 ∧ b % 2 = 0 ∧ c % 2 = 1) ∨
        (a % 2 = 1 ∧ b % 2 = 1 ∧ c % 2 = 1)) ∧ sgn ⟨a, b, c⟩ = 0) := by
  simp only [sgn, pairSign]
  split_ifs <;> omega

/-- `sgn_spec` for an arbitrary vector. -/
theorem sgn_spec' (v : Vec3) :
    (v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0 ∧
        (((v.a - v.b) % 4 = 0 ∧ sgn v = -1) ∨ ((v.a - v.b) % 4 ≠ 0 ∧ sgn v = 1))) ∨
    (v.a % 2 = 1 ∧ v.c % 2 = 1 ∧ v.b % 2 = 0 ∧
        (((v.a - v.c) % 4 = 0 ∧ sgn v = -1) ∨ ((v.a - v.c) % 4 ≠ 0 ∧ sgn v = 1))) ∨
    (v.b % 2 = 1 ∧ v.c % 2 = 1 ∧ v.a % 2 = 0 ∧
        (((v.b - v.c) % 4 = 0 ∧ sgn v = -1) ∨ ((v.b - v.c) % 4 ≠ 0 ∧ sgn v = 1))) ∨
    (((v.a % 2 = 0 ∧ v.b % 2 = 0 ∧ v.c % 2 = 0) ∨ (v.a % 2 = 1 ∧ v.b % 2 = 0 ∧ v.c % 2 = 0) ∨
        (v.a % 2 = 0 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0) ∨ (v.a % 2 = 0 ∧ v.b % 2 = 0 ∧ v.c % 2 = 1) ∨
        (v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 1)) ∧ sgn v = 0) := by
  obtain ⟨a, b, c⟩ := v
  exact sgn_spec a b c

theorem sgn_mem (v : Vec3) : sgn v = -1 ∨ sgn v = 0 ∨ sgn v = 1 := by
  have := sgn_spec' v
  omega

/-! ### Products modulo 4 -/

/-- The residue of a product modulo `4` in terms of the factors. -/
theorem mul_emod_four (x y : ℤ) :
    (x % 2 = 0 ∧ y % 2 = 0 ∧ x * y % 4 = 0) ∨
    (x % 2 = 1 ∧ y % 2 = 1 ∧ (x - y) % 4 = 0 ∧ x * y % 4 = 1) ∨
    (x % 2 = 1 ∧ y % 2 = 1 ∧ (x - y) % 4 ≠ 0 ∧ x * y % 4 = 3) ∨
    ((x + y) % 2 = 1 ∧ x * y % 2 = 0) := by
  have h : x * y % 4 = x % 4 * (y % 4) % 4 := Int.mul_emod x y 4
  have hx : x % 4 = 0 ∨ x % 4 = 1 ∨ x % 4 = 2 ∨ x % 4 = 3 := by omega
  have hy : y % 4 = 0 ∨ y % 4 = 1 ∨ y % 4 = 2 ∨ y % 4 = 3 := by omega
  rcases hx with hx | hx | hx | hx <;> rcases hy with hy | hy | hy | hy <;>
    rw [hx, hy] at h <;> omega

/-- Multiplication by an odd integer preserves divisibility by `4`. -/
theorem odd_mul_emod_four (k m : ℤ) (hk : k % 2 = 1) : k * m % 4 = 0 ↔ m % 4 = 0 := by
  have h : k * m % 4 = k % 4 * (m % 4) % 4 := Int.mul_emod k m 4
  have hk' : k % 4 = 1 ∨ k % 4 = 3 := by omega
  have hm : m % 4 = 0 ∨ m % 4 = 1 ∨ m % 4 = 2 ∨ m % 4 = 3 := by omega
  rcases hk' with hk' | hk' <;> rcases hm with hm | hm | hm | hm <;>
    rw [hk', hm] at h <;> omega

/-! ### Frame additivity -/

/-- On every pairwise orthogonal triple of odd-primitive integer vectors the signs sum to `0`. -/
set_option maxHeartbeats 4000000 in
theorem sgn_frame {u v w : Vec3} (hu : IsPrimitive u) (hv : IsPrimitive v) (hw : IsPrimitive w)
    (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    sgn u + sgn v + sgn w = 0 := by
  simp only [IsPrimitive, Vec3.dot] at hu hv hw huv huw hvw
  have su := sgn_spec' u
  have sv := sgn_spec' v
  have sw := sgn_spec' w
  have m₁ := mul_emod_four u.a v.a
  have m₂ := mul_emod_four u.b v.b
  have m₃ := mul_emod_four u.c v.c
  have m₄ := mul_emod_four u.a w.a
  have m₅ := mul_emod_four u.b w.b
  have m₆ := mul_emod_four u.c w.c
  have m₇ := mul_emod_four v.a w.a
  have m₈ := mul_emod_four v.b w.b
  have m₉ := mul_emod_four v.c w.c
  have p₁ : u.a % 2 = 0 ∨ u.a % 2 = 1 := by omega
  have p₂ : u.b % 2 = 0 ∨ u.b % 2 = 1 := by omega
  have p₃ : u.c % 2 = 0 ∨ u.c % 2 = 1 := by omega
  have p₄ : v.a % 2 = 0 ∨ v.a % 2 = 1 := by omega
  have p₅ : v.b % 2 = 0 ∨ v.b % 2 = 1 := by omega
  have p₆ : v.c % 2 = 0 ∨ v.c % 2 = 1 := by omega
  have p₇ : w.a % 2 = 0 ∨ w.a % 2 = 1 := by omega
  have p₈ : w.b % 2 = 0 ∨ w.b % 2 = 1 := by omega
  have p₉ : w.c % 2 = 0 ∨ w.c % 2 = 1 := by omega
  rcases p₁ with p₁ | p₁ <;> rcases p₂ with p₂ | p₂ <;> rcases p₃ with p₃ | p₃ <;>
    rcases p₄ with p₄ | p₄ <;> rcases p₅ with p₅ | p₅ <;> rcases p₆ with p₆ | p₆ <;>
    rcases p₇ with p₇ | p₇ <;> rcases p₈ with p₈ | p₈ <;> rcases p₉ with p₉ | p₉ <;>
    omega

/-- Frame additivity of `exotic` on all orthogonal triples of odd-primitive integer vectors. -/
theorem exotic_frame_function {u v w : Vec3} (hu : IsPrimitive u) (hv : IsPrimitive v)
    (hw : IsPrimitive w) (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    exotic u + exotic v + exotic w = 1 := by
  have h := sgn_frame hu hv hw huv huw hvw
  have h' : ((sgn u : ℚ) + sgn v + sgn w) = 0 := by exact_mod_cast h
  unfold exotic
  linarith

theorem exotic_three_valued (v : Vec3) :
    exotic v = 0 ∨ exotic v = 1 / 3 ∨ exotic v = 2 / 3 := by
  unfold exotic
  rcases sgn_mem v with h | h | h <;> rw [h] <;> norm_num

/-- Over `ℤ³` no orthogonal triple has all three members `≡ (1, 1, 0) (mod 2)`. -/
theorem no_real_triangle {u v w : Vec3} (hu : IsPrimitive u) (hv : IsPrimitive v)
    (hw : IsPrimitive w) (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    ¬ ((u.a % 2 = 1 ∧ u.b % 2 = 1 ∧ u.c % 2 = 0) ∧ (v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0) ∧
        (w.a % 2 = 1 ∧ w.b % 2 = 1 ∧ w.c % 2 = 0)) := by
  intro h
  have h0 := sgn_frame hu hv hw huv huw hvw
  have su := sgn_spec' u
  have sv := sgn_spec' v
  have sw := sgn_spec' w
  omega

/-! ### Ray invariance -/

theorem sgn_neg (a b c : ℤ) : sgn ⟨-a, -b, -c⟩ = sgn ⟨a, b, c⟩ := by
  have h1 := sgn_spec (-a) (-b) (-c)
  have h2 := sgn_spec a b c
  omega

theorem sgn_odd_smul {k : ℤ} (hk : k % 2 = 1) (a b c : ℤ) :
    sgn ⟨k * a, k * b, k * c⟩ = sgn ⟨a, b, c⟩ := by
  have h1 := sgn_spec (k * a) (k * b) (k * c)
  have h2 := sgn_spec a b c
  have e1 := mul_emod_two_eq_one k a
  have e2 := mul_emod_two_eq_one k b
  have e3 := mul_emod_two_eq_one k c
  have f1 := odd_mul_emod_four k (a - b) hk
  have f2 := odd_mul_emod_four k (a - c) hk
  have f3 := odd_mul_emod_four k (b - c) hk
  have r1 : k * a - k * b = k * (a - b) := by ring
  have r2 : k * a - k * c = k * (a - c) := by ring
  have r3 : k * b - k * c = k * (b - c) := by ring
  omega

/-- If `q • u = p • u'` with `p, q` odd (the only way two odd-primitive vectors can represent the
same rational ray), the signs agree. -/
theorem sgn_eq_of_odd_scalings {p q : ℤ} (hp : p % 2 = 1) (hq : q % 2 = 1) {u u' : Vec3}
    (h1 : q * u.a = p * u'.a) (h2 : q * u.b = p * u'.b) (h3 : q * u.c = p * u'.c) :
    sgn u = sgn u' := by
  have e1 : sgn ⟨q * u.a, q * u.b, q * u.c⟩ = sgn u := sgn_odd_smul hq u.a u.b u.c
  have e2 : sgn ⟨p * u'.a, p * u'.b, p * u'.c⟩ = sgn u' := sgn_odd_smul hp u'.a u'.b u'.c
  rw [h1, h2, h3] at e1
  exact e1.symm.trans e2

theorem exotic_neg (a b c : ℤ) : exotic ⟨-a, -b, -c⟩ = exotic ⟨a, b, c⟩ := by
  unfold exotic
  rw [sgn_neg]

theorem exotic_eq_of_odd_scalings {p q : ℤ} (hp : p % 2 = 1) (hq : q % 2 = 1) {u u' : Vec3}
    (h1 : q * u.a = p * u'.a) (h2 : q * u.b = p * u'.b) (h3 : q * u.c = p * u'.c) :
    exotic u = exotic u' := by
  unfold exotic
  rw [sgn_eq_of_odd_scalings hp hq h1 h2 h3]

/-! ### Comparison with the rational unit sphere -/

/-- On repository rays (square norm) exactly one coordinate is odd, so `sgn = 0`. -/
theorem sgn_eq_zero_of_isRay {v : Vec3} (hv : v.IsRay) : sgn v = 0 := by
  have h := ray_exactly_one_odd hv
  simp only [Int.odd_iff, Int.even_iff] at h
  have hs := sgn_spec' v
  omega

/-- On the rational unit sphere `exotic` is the constant `1/3` (the Born value of `ρ = I/3`). -/
theorem exotic_eq_third_of_isRay {v : Vec3} (hv : v.IsRay) : exotic v = 1 / 3 := by
  unfold exotic
  rw [sgn_eq_zero_of_isRay hv]
  norm_num

/-! ### Seven explicit primitive vectors -/

theorem prim_100 : IsPrimitive ⟨1, 0, 0⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_010 : IsPrimitive ⟨0, 1, 0⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_001 : IsPrimitive ⟨0, 0, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_110 : IsPrimitive ⟨1, 1, 0⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_101 : IsPrimitive ⟨1, 0, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_011 : IsPrimitive ⟨0, 1, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_111 : IsPrimitive ⟨1, 1, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])

theorem sgn_100 : sgn ⟨1, 0, 0⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_010 : sgn ⟨0, 1, 0⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_001 : sgn ⟨0, 0, 1⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_110 : sgn ⟨1, 1, 0⟩ = -1 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_101 : sgn ⟨1, 0, 1⟩ = -1 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_011 : sgn ⟨0, 1, 1⟩ = -1 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_111 : sgn ⟨1, 1, 1⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_1m10 : sgn ⟨1, -1, 0⟩ = 1 := by first | decide | norm_num [sgn, pairSign]

theorem exotic_100 : exotic ⟨1, 0, 0⟩ = 1 / 3 := by rw [exotic, sgn_100]; norm_num
theorem exotic_010 : exotic ⟨0, 1, 0⟩ = 1 / 3 := by rw [exotic, sgn_010]; norm_num
theorem exotic_001 : exotic ⟨0, 0, 1⟩ = 1 / 3 := by rw [exotic, sgn_001]; norm_num
theorem exotic_110 : exotic ⟨1, 1, 0⟩ = 0 := by rw [exotic, sgn_110]; norm_num
theorem exotic_101 : exotic ⟨1, 0, 1⟩ = 0 := by rw [exotic, sgn_101]; norm_num
theorem exotic_011 : exotic ⟨0, 1, 1⟩ = 0 := by rw [exotic, sgn_011]; norm_num
theorem exotic_111 : exotic ⟨1, 1, 1⟩ = 1 / 3 := by rw [exotic, sgn_111]; norm_num
theorem exotic_1m10 : exotic ⟨1, -1, 0⟩ = 2 / 3 := by rw [exotic, sgn_1m10]; norm_num

/-! ### The obstruction -/

/-- No rational symmetric `3 × 3` form `Q` satisfies `Q(v) = exotic v · (a² + b² + c²)` on all
odd-primitive integer vectors (the Born value of the ray times the norm squared). -/
theorem exotic_not_quadratic :
    ¬ ∃ r00 r11 r22 r01 r02 r12 : ℚ, ∀ v : Vec3, IsPrimitive v →
      r00 * (v.a : ℚ) ^ 2 + r11 * (v.b : ℚ) ^ 2 + r22 * (v.c : ℚ) ^ 2
        + 2 * r01 * ((v.a : ℚ) * v.b) + 2 * r02 * ((v.a : ℚ) * v.c) + 2 * r12 * ((v.b : ℚ) * v.c)
        = exotic v * ((v.a : ℚ) ^ 2 + (v.b : ℚ) ^ 2 + (v.c : ℚ) ^ 2) := by
  rintro ⟨r00, r11, r22, r01, r02, r12, h⟩
  have h1 := h _ prim_100
  have h2 := h _ prim_010
  have h3 := h _ prim_001
  have h4 := h _ prim_110
  have h5 := h _ prim_101
  have h6 := h _ prim_011
  have h7 := h _ prim_111
  norm_num [exotic_100, exotic_010, exotic_001, exotic_110, exotic_101, exotic_011, exotic_111]
    at h1 h2 h3 h4 h5 h6 h7
  linarith

end BornFable.RationalPlane

#print axioms BornFable.RationalPlane.isPrimitive_of_isRay
#print axioms BornFable.RationalPlane.sgn_spec
#print axioms BornFable.RationalPlane.sgn_spec'
#print axioms BornFable.RationalPlane.sgn_mem
#print axioms BornFable.RationalPlane.mul_emod_four
#print axioms BornFable.RationalPlane.odd_mul_emod_four
#print axioms BornFable.RationalPlane.sgn_frame
#print axioms BornFable.RationalPlane.exotic_frame_function
#print axioms BornFable.RationalPlane.exotic_three_valued
#print axioms BornFable.RationalPlane.no_real_triangle
#print axioms BornFable.RationalPlane.sgn_neg
#print axioms BornFable.RationalPlane.sgn_odd_smul
#print axioms BornFable.RationalPlane.sgn_eq_of_odd_scalings
#print axioms BornFable.RationalPlane.exotic_neg
#print axioms BornFable.RationalPlane.exotic_eq_of_odd_scalings
#print axioms BornFable.RationalPlane.sgn_eq_zero_of_isRay
#print axioms BornFable.RationalPlane.exotic_eq_third_of_isRay
#print axioms BornFable.RationalPlane.exotic_not_quadratic
```

```lean
-- FILE: lean4/BornGaussianRationalFrameObstruction.lean
import BornGaussRat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Frame functions on `ℚ(i)³`: the `(1+i)`-parity route is closed

AuthorityEffect: None.

Setting.  `GVec` is `K³` for `K = ℚ(i)` (`BornFable.GaussRat`), with the Hermitian form
`inner u v = Σ conj(uₖ) vₖ`.  A frame is a triple of nonzero pairwise orthogonal vectors; a frame
function is `f : GVec → ℚ` summing to `1` on every frame.  (`BornGaussianFrameRays` shows such an
`f` is automatically constant on rays.)

For a Gaussian integer `a + b i`, `(1+i) ∣ a + b i ⇔ a ≡ b (mod 2)`; the `(1+i)`-parity class of a
Gaussian-integer vector `gv a b c d e g = (a+bi, c+di, e+gi)` is `((a+b)%2, (c+d)%2, (e+g)%2)`.

Main results:
* `frame_tri_110` (and `frame_tri_101`, `frame_tri_011`): the non-real orthogonal frame
  `(1,1,0), (1,-1,1+i), (1,-1,-1-i)` all of whose members lie in the parity class `(1,1,0)`;
  no such frame exists over `ℤ³` (`BornRationalPlaneObstruction.no_real_triangle`).
* `parity_class_function_is_third`: a frame function on `K³` whose value on every
  `(1+i)`-primitive Gaussian-integer vector depends only on the parity class is `1/3` on all of
  them — the Born value of `ρ = I/3`.  So the parity (Meyer / Godsil–Zaks) construction cannot give
  a non-quadratic frame function over `ℚ(i)`.

This file does **not** decide whether every frame function on `ℚ(i)³` rays is quadratic.
Nothing here is a statement about physics.
-/

namespace BornFable.GaussianFrames

open BornFable

/-- A vector in `K³`, `K = ℚ(i)`. -/
structure GVec where
  x : GaussRat
  y : GaussRat
  z : GaussRat

namespace GVec

/-- The Hermitian inner product `⟨u, v⟩ = Σ conj(uₖ) vₖ` (conjugate-linear in `u`). -/
def inner (u v : GVec) : GaussRat := star u.x * v.x + star u.y * v.y + star u.z * v.z

/-- `v ≠ 0`. -/
def NonZero (v : GVec) : Prop := v.x ≠ 0 ∨ v.y ≠ 0 ∨ v.z ≠ 0

/-- Scalar multiplication. -/
def smul (l : GaussRat) (v : GVec) : GVec := ⟨l * v.x, l * v.y, l * v.z⟩

end GVec

/-- An orthogonal frame: three nonzero pairwise orthogonal vectors. -/
def IsFrame (u v w : GVec) : Prop :=
  u.NonZero ∧ v.NonZero ∧ w.NonZero ∧ u.inner v = 0 ∧ u.inner w = 0 ∧ v.inner w = 0

/-- A frame function: sums to `1` on every orthogonal frame. -/
def IsFrameFunction (f : GVec → ℚ) : Prop :=
  ∀ u v w : GVec, IsFrame u v w → f u + f v + f w = 1

/-- The Gaussian-integer vector `(a + b i, c + d i, e + g i)`. -/
def gv (a b c d e g : ℤ) : GVec :=
  ⟨⟨(a : ℚ), (b : ℚ)⟩, ⟨(c : ℚ), (d : ℚ)⟩, ⟨(e : ℚ), (g : ℚ)⟩⟩

/-- `f` is determined by the `(1+i)`-parity class on `(1+i)`-primitive Gaussian-integer
vectors: there is `col` with `f (gv a b c d e g) = col ((a+b)%2) ((c+d)%2) ((e+g)%2)` whenever
not all three components are divisible by `1 + i`. -/
def ParityDetermined (f : GVec → ℚ) (col : ℤ → ℤ → ℤ → ℚ) : Prop :=
  ∀ a b c d e g : ℤ, ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0) →
    f (gv a b c d e g) = col ((a + b) % 2) ((c + d) % 2) ((e + g) % 2)

/-! ### Nonzero-ness helpers -/

theorem nonZero_of_x {v : GVec} (h : v.x.re ≠ 0) : v.NonZero :=
  Or.inl fun e => h (by simp [e])

theorem nonZero_of_y {v : GVec} (h : v.y.re ≠ 0) : v.NonZero :=
  Or.inr (Or.inl fun e => h (by simp [e]))

theorem nonZero_of_z {v : GVec} (h : v.z.re ≠ 0) : v.NonZero :=
  Or.inr (Or.inr fun e => h (by simp [e]))

/-- Verify an explicit Gaussian-rational inner-product identity componentwise. -/
macro "gauss_arith" : tactic =>
  `(tactic| first
      | (ext <;> simp [GVec.inner, gv] <;> norm_num)
      | norm_num [GVec.inner, gv, GaussRat.ext_iff])

/-! ### Seven explicit frames -/

/-- Real frame `e₃, (1,1,0), (1,-1,0)`. -/
theorem frame_e3_110 : IsFrame (gv 0 0 0 0 1 0) (gv 1 0 1 0 0 0) (gv 1 0 (-1) 0 0 0) :=
  ⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- Real frame `e₁, (0,1,1), (0,1,-1)`. -/
theorem frame_e1_011 : IsFrame (gv 1 0 0 0 0 0) (gv 0 0 1 0 1 0) (gv 0 0 1 0 (-1) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]),
    nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- Real frame `e₂, (1,0,1), (1,0,-1)`. -/
theorem frame_e2_101 : IsFrame (gv 0 0 1 0 0 0) (gv 1 0 0 0 1 0) (gv 1 0 0 0 (-1) 0) :=
  ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- Real frame `(1,1,1), (1,-1,0), (1,1,-2)`. -/
theorem frame_111_110 : IsFrame (gv 1 0 1 0 1 0) (gv 1 0 (-1) 0 0 0) (gv 1 0 1 0 (-2) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- The non-real triangle `(1,1,0), (1,-1,1+i), (1,-1,-1-i)`: all three members have
`(1+i)`-parity class `(1,1,0)`.  Compare `BornRationalPlaneObstruction.no_real_triangle`. -/
theorem frame_tri_110 :
    IsFrame (gv 1 0 1 0 0 0) (gv 1 0 (-1) 0 1 1) (gv 1 0 (-1) 0 (-1) (-1)) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- The permuted triangle `(1,0,1), (1,1+i,-1), (1,-1-i,-1)`, class `(1,0,1)`. -/
theorem frame_tri_101 :
    IsFrame (gv 1 0 0 0 1 0) (gv 1 0 1 1 (-1) 0) (gv 1 0 (-1) (-1) (-1) 0) :=
  ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-- The permuted triangle `(0,1,1), (1+i,1,-1), (-1-i,1,-1)`, class `(0,1,1)`. -/
theorem frame_tri_011 :
    IsFrame (gv 0 0 1 0 1 0) (gv 1 1 1 0 (-1) 0) (gv (-1) (-1) 1 0 (-1) 0) :=
  ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]),
    nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩

/-! ### The parity route is closed -/

/-- Class value of an explicit Gaussian-integer vector, in normalised form. -/
theorem class_value {f : GVec → ℚ} {col : ℤ → ℤ → ℤ → ℚ} (hP : ParityDetermined f col)
    (a b c d e g p q r : ℤ)
    (hne : ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0))
    (h1 : (a + b) % 2 = p) (h2 : (c + d) % 2 = q) (h3 : (e + g) % 2 = r) :
    f (gv a b c d e g) = col p q r := by
  rw [hP a b c d e g hne, h1, h2, h3]

/-- **The `(1+i)`-parity route is closed over `ℚ(i)`.**  A frame function on `K³` whose values on
`(1+i)`-primitive Gaussian-integer vectors depend only on the `(1+i)`-parity class is the constant
`1/3` on all such vectors (the Born value of `ρ = I/3`). -/
theorem parity_class_function_is_third (f : GVec → ℚ) (col : ℤ → ℤ → ℤ → ℚ)
    (hF : IsFrameFunction f) (hP : ParityDetermined f col)
    (a b c d e g : ℤ) (hne : ¬ ((a + b) % 2 = 0 ∧ (c + d) % 2 = 0 ∧ (e + g) % 2 = 0)) :
    f (gv a b c d e g) = 1 / 3 := by
  -- class values of the seventeen explicit vectors
  have k100 := class_value hP 1 0 0 0 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide)
  have k010 := class_value hP 0 0 1 0 0 0 0 1 0 (by decide) (by decide) (by decide) (by decide)
  have k001 := class_value hP 0 0 0 0 1 0 0 0 1 (by decide) (by decide) (by decide) (by decide)
  have kP := class_value hP 1 0 1 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kM := class_value hP 1 0 (-1) 0 0 0 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kQ := class_value hP 0 0 1 0 1 0 0 1 1 (by decide) (by decide) (by decide) (by decide)
  have kQm := class_value hP 0 0 1 0 (-1) 0 0 1 1 (by decide) (by decide) (by decide) (by decide)
  have kR := class_value hP 1 0 0 0 1 0 1 0 1 (by decide) (by decide) (by decide) (by decide)
  have kRm := class_value hP 1 0 0 0 (-1) 0 1 0 1 (by decide) (by decide) (by decide) (by decide)
  have kT := class_value hP 1 0 1 0 1 0 1 1 1 (by decide) (by decide) (by decide) (by decide)
  have kS := class_value hP 1 0 1 0 (-2) 0 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kA := class_value hP 1 0 (-1) 0 1 1 1 1 0 (by decide) (by decide) (by decide) (by decide)
  have kB := class_value hP 1 0 (-1) 0 (-1) (-1) 1 1 0
    (by decide) (by decide) (by decide) (by decide)
  have kC := class_value hP 1 0 1 1 (-1) 0 1 0 1 (by decide) (by decide) (by decide) (by decide)
  have kD := class_value hP 1 0 (-1) (-1) (-1) 0 1 0 1
    (by decide) (by decide) (by decide) (by decide)
  have kF := class_value hP 1 1 1 0 (-1) 0 0 1 1 (by decide) (by decide) (by decide) (by decide)
  have kG := class_value hP (-1) (-1) 1 0 (-1) 0 0 1 1
    (by decide) (by decide) (by decide) (by decide)
  -- the seven frame equations
  have t1 := hF _ _ _ frame_e3_110
  have t2 := hF _ _ _ frame_e1_011
  have t3 := hF _ _ _ frame_e2_101
  have t4 := hF _ _ _ frame_111_110
  have t5 := hF _ _ _ frame_tri_110
  have t6 := hF _ _ _ frame_tri_101
  have t7 := hF _ _ _ frame_tri_011
  -- the class of the given vector is one of the seven nonzero ones
  have ha : (a + b) % 2 = 0 ∨ (a + b) % 2 = 1 := by omega
  have hc : (c + d) % 2 = 0 ∨ (c + d) % 2 = 1 := by omega
  have he : (e + g) % 2 = 0 ∨ (e + g) % 2 = 1 := by omega
  rcases ha with ha | ha <;> rcases hc with hc | hc <;> rcases he with he | he <;>
    first
    | exact absurd (And.intro ha (And.intro hc he)) hne
    | (have key := class_value hP a b c d e g _ _ _ hne ha hc he; linarith)

end BornFable.GaussianFrames

#print axioms BornFable.GaussianFrames.frame_e3_110
#print axioms BornFable.GaussianFrames.frame_e1_011
#print axioms BornFable.GaussianFrames.frame_e2_101
#print axioms BornFable.GaussianFrames.frame_111_110
#print axioms BornFable.GaussianFrames.frame_tri_110
#print axioms BornFable.GaussianFrames.frame_tri_101
#print axioms BornFable.GaussianFrames.frame_tri_011
#print axioms BornFable.GaussianFrames.class_value
#print axioms BornFable.GaussianFrames.parity_class_function_is_third
```

```lean
-- FILE: lean4/BornGaussianFrameRays.lean
import BornGaussianRationalFrameObstruction

/-!
# Frame functions on `ℚ(i)³` are functions of rays

AuthorityEffect: None.

Every nonzero `v ∈ K³` completes to an orthogonal frame `(v, w, u)` in which `w, u` do not depend
on rescaling `v` (`exists_frame_completion`).  Hence any frame function on vectors satisfies
`f (l • v) = f v` for `l ≠ 0` (`frameFunction_smul`): the vector-level definition
`IsFrameFunction` in `BornGaussianRationalFrameObstruction` is a function on rays.
-/

namespace BornFable.GaussianFrames

open BornFable

theorem inner_smul_left (l : GaussRat) (u v : GVec) :
    (GVec.smul l u).inner v = star l * u.inner v := by
  simp only [GVec.inner, GVec.smul, star_mul]
  ring

theorem nonZero_smul {l
: GaussRat} (hl : l ≠ 0) {v : GVec} (hv : v.NonZero) :
    (GVec.smul l v).NonZero := by
  rcases hv with h | h | h
  · exact Or.inl (mul_ne_zero hl h)
  · exact Or.inr (Or.inl (mul_ne_zero hl h))
  · exact Or.inr (Or.inr (mul_ne_zero hl h))

/-- Every nonzero vector completes to a frame `(v, w, u)`, with the same `w, u` working for every
nonzero rescaling of `v`. -/
theorem exists_frame_completion {v : GVec} (hv : v.NonZero) :
    ∃ w u : GVec, IsFrame v w u ∧ ∀ l : GaussRat, l ≠ 0 → IsFrame (GVec.smul l v) w u := by
  by_cases hxy : v.x = 0 ∧ v.y = 0
  · obtain ⟨hx, hy⟩ := hxy
    have e1 : GVec.NonZero ⟨1, 0, 0⟩ := Or.inl one_ne_zero
    have e2 : GVec.NonZero ⟨0, 1, 0⟩ := Or.inr (Or.inl one_ne_zero)
    have i1 : v.inner ⟨1, 0, 0⟩ = 0 := by simp [GVec.inner, hx]
    have i2 : v.inner ⟨0, 1, 0⟩ = 0 := by simp [GVec.inner, hy]
    have i3 : GVec.inner ⟨1, 0, 0⟩ ⟨0, 1, 0⟩ = 0 := by simp [GVec.inner]
    refine ⟨⟨1, 0, 0⟩, ⟨0, 1, 0⟩, ⟨hv, e1, e2, i1, i2, i3⟩, ?_⟩
    intro l hl
    refine ⟨nonZero_smul hl hv, e1, e2, ?_, ?_, i3⟩
    · rw [inner_smul_left, i1, mul_zero]
    · rw [inner_smul_left, i2, mul_zero]
  · have hpos : 0 < GaussRat.normSq v.x + GaussRat.normSq v.y := by
      rcases not_and_or.mp hxy with hx | hy
      · have h1 : 0 < GaussRat.normSq v.x :=
          lt_of_le_of_ne (GaussRat.normSq_nonneg _)
            (fun h => hx ((GaussRat.normSq_eq_zero_iff _).mp h.symm))
        linarith [GaussRat.normSq_nonneg v.y]
      · have h1 : 0 < GaussRat.normSq v.y :=
          lt_of_le_of_ne (GaussRat.normSq_nonneg _)
            (fun h => hy ((GaussRat.normSq_eq_zero_iff _).mp h.symm))
        linarith [GaussRat.normSq_nonneg v.x]
    have hw : GVec.NonZero ⟨-star v.y, star v.x, 0⟩ := by
      rcases not_and_or.mp hxy with hx | hy
      · exact Or.inr (Or.inl (fun h => hx (star_eq_zero.mp h)))
      · exact Or.inl (fun h => hy (star_eq_zero.mp (neg_eq_zero.mp h)))
    have hz : (star v.x * v.x + star v.y * v.y).re ≠ 0 := by
      rw [GaussRat.re_add, GaussRat.re_star_mul_self, GaussRat.re_star_mul_self]
      exact hpos.ne'
    have hu : GVec.NonZero
        ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩ :=
      nonZero_of_z hz
    have i1 : v.inner ⟨-star v.y, star v.x, 0⟩ = 0 := by
      simp only [GVec.inner]
      ring
    have i2 : v.inner
        ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩ = 0 := by
      simp only [GVec.inner]
      ring
    have i3 : GVec.inner ⟨-star v.y, star v.x, 0⟩
        ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩ = 0 := by
      simp only [GVec.inner, star_neg, star_star, star_zero]
      ring
    refine ⟨⟨-star v.y, star v.x, 0⟩,
      ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩,
      ⟨hv, hw, hu, i1, i2, i3⟩, ?_⟩
    intro l hl
    refine ⟨nonZero_smul hl hv, hw, hu, ?_, ?_, i3⟩
    · rw [inner_smul_left, i1, mul_zero]
    · rw [inner_smul_left, i2, mul_zero]

/-- A frame function on vectors is constant on rays. -/
theorem frameFunction_smul {f : GVec → ℚ} (hF : IsFrameFunction f) {v : GVec} (hv : v.NonZero)
    {l : GaussRat} (hl : l ≠ 0) : f (GVec.smul l v) = f v := by
  obtain ⟨w, u, h1, h2⟩ := exists_frame_completion hv
  have e1 := hF _ _ _ h1
  have e2 := hF _ _ _ (h2 l hl)
  linarith

end BornFable.GaussianFrames

#print axioms BornFable.GaussianFrames.inner_smul_left
#print axioms BornFable.GaussianFrames.nonZero_smul
#print axioms BornFable.GaussianFrames.exists_frame_completion
#print axioms BornFable.GaussianFrames.frameFunction_smul
```

## 3. WHAT IS PROVED

**Not proved:** neither (A) nor (B). No frame function on *all* Gaussian‑rational rays is constructed, and no uniqueness theorem over `ℚ(i)³` is proved. The question remains open; the files below give the largest honest pieces.

**File `BornRationalPlaneObstruction.lean` (over ℚ, all rational rays, new relative to the repository):**
- `exotic_frame_function`: for any three integer vectors `u, v, w ∈ ℤ³`, each with not all coordinates even (`IsPrimitive`) and pairwise orthogonal for the integer dot product, `exotic u + exotic v + exotic w = 1`. No square‑norm hypothesis.
- `exotic_not_quadratic`: there is no rational symmetric form `(r_ij)` with `Q(v) = exotic v · (a²+b²+c²)` for all odd‑primitive `v`.
- `exotic_three_valued`: `exotic v ∈ {0, 1/3, 2/3}`.
- `sgn_eq_of_odd_scalings`, `exotic_eq_of_odd_scalings`, `sgn_neg`, `exotic_neg`, `sgn_odd_smul`: if `q·u = p·u'` with `p, q` odd (in particular `u' = ±u`), then `exotic u = exotic u'`; so `exotic` is a function of the rational ray (odd‑primitive representatives of one ray differ by exactly such a factor — this last sentence is stated in prose, not in Lean).
- `exotic_eq_third_of_isRay`, `sgn_eq_zero_of_isRay`: on the repository's rays (square norm) `exotic` is the constant `1/3`; `isPrimitive_of_isRay` links the two carriers.
- `no_real_triangle`: no orthogonal triple of odd‑primitive integer vectors has all three members `≡ (1,1,0) (mod 2)`.
- Auxiliary: `sgn_spec`, `sgn_spec'`, `sgn_mem`, `mul_emod_four`, `odd_mul_emod_four`, and explicit‑vector lemmas.

**File `BornGaussianRationalFrameObstruction.lean` (over K = ℚ(i)):**
- `frame_tri_110`, `frame_tri_101`, `frame_tri_011`: explicit non‑real orthogonal frames of `K³` (e.g. `(1,1,0), (1,−1,1+i), (1,−1,−1−i)`) whose three members share the `(1+i)`‑parity class; `frame_e3_110`, `frame_e1_011`, `frame_e2_101`, `frame_111_110`: four real frames.
- `parity_class_function_is_third`: if `f : K³ → ℚ` sums to `1` on every orthogonal frame of nonzero pairwise‑orthogonal vectors (`IsFrameFunction`), and on every Gaussian‑integer vector not all of whose components are divisible by `1+i` the value `f` depends only on the triple `((a+b)%2, (c+d)%2, (e+g)%2)` (`ParityDetermined`), then `f = 1/3` on every such vector. (That `1/3` is the Born function of `ρ = I/3` is stated in prose only.)

**File `BornGaussianFrameRays.lean`:**
- `exists_frame_completion`: every nonzero `v ∈ K³` completes to a frame `(v, w, u)`, with the same `w, u` for every nonzero rescaling of `v`.
- `frameFunction_smul`: for any `IsFrameFunction f`, `f (l • v) = f v` whenever `v ≠ 0`, `l ≠ 0`; so vector‑level frame functions are functions on rays.

Left unproved: existence of a non‑quadratic frame function on all `ℚ(i)`‑rays (A); quadraticity of every frame function on `ℚ(i)`‑rays (B); whether the ℚ‑function `exotic` extends to a frame function on `K³` rays. The `(1+i)`‑divisibility criterion `(1+i) ∣ a+bi ⇔ a ≡ b (mod 2)` is used as the definition of "parity class" and is justified only in prose.