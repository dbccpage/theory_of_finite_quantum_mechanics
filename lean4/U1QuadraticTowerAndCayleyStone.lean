import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Data.Rat.Lemmas
import U1PythagoreanObstruction
import U1CauchyCircleCompletion
import U1ChebyshevCauchyBridge

/-!
# Iterated Quadratic Square-Root Tower $K_{m+1} = K_m(\sqrt{(1+c_m)/2})$ and Discrete Cayley Unitary Step (`FQ-GAP-U1-CIRCLE`, `FQ-GAP-STONE-CONTINUOUS-TIME`)

This module mechanizes the two structural bridges listed in the `FQ-GAP-U1-CIRCLE` next-test agenda:

1. **Section 1 — Parametric Quadratic Extension Ring `QuadExt R d` and Universal Half-Angle Step**:
   For any commutative ring $R$ and radicand $d \in R$, `QuadExt R d` represents the quadratic
   extension $R[\rho]/(\rho^2 - d)$ with a full `CommRing (QuadExt R d)` instance. Given a bundled
   unit-circle state $(c, s, w, v, \mathrm{half}) \in R^5$ satisfying
   $$c^2 + s^2 = 1, \qquad (1+c)w = 1, \qquad s v = 1, \qquad 2\,\mathrm{half} = 1,$$
   adjoining $\rho = \sqrt{d}$ with $d = \mathrm{half}\cdot(1+c)$ produces the half-angle state
   $$c' = \rho, \qquad s' = (s w)\rho, \qquad w' = 2 v^2(1+c)(1-\rho), \qquad v' = (2 v)\rho$$
   in `QuadExt R d`, which satisfies the unit-circle equation $(c')^2 + (s')^2 = 1$, the double-angle
   equations $(c')^2 - (s')^2 = c$ and $c' s' + s' c' = s$, and the invertibility invariants
   $(1+c')w' = 1$ and $s' v' = 1$ by pure polynomial ring identities.

2. **Section 2 — Inductively Defined $2^m$-Division Tower $K_m$ for $u_{345} = (3/5, 4/5)$**:
   Iterating the quadratic extension step from $K_0 = \mathbb{Q}$ and $(c_0, s_0, w_0, v_0) = (3/5, 4/5, 5/8, 5/4)$
   defines the infinite algebraic tower `TowerRing : ℕ → Type` with `CommRing (TowerRing m)` and
   `towerState (m : ℕ)` for all $m \in \mathbb{N}$. At every level $m$, `towerState m` lies on
   $S^1(K_m)$, its square in $S^1(K_{m+1})$ equals the embedded `towerState m`, and its $2^m$-th
   circle power in $S^1(K_m)$ equals the embedded Pythagorean generator $u_{345} = (3/5, 4/5)$
   (`towerState_pow_two_pow_eq_u345`).

3. **Section 3 — Discrete Cayley Unitary Step $(I - i t H)(I + i t H)^{-1}$ on `HermitianMat2Qi` (`FQ-GAP-STONE-CONTINUOUS-TIME`)**:
   Connects the 4D $\mathbb{Q}(i)$ Hermitian carrier `HermitianMat2Qi` to the rational Cayley
   unitary propagator $U_H(t) = (I - i t H)(I + i t H)^{-1}$ over $\mathbb{Q}(i)$. For every
   traceless Hermitian generator $H = z\sigma_z + x\sigma_x + y\sigma_y$ and every rational step parameter
   $t \in \mathbb{Q}$, the scalar denominator $\Delta(H, t) = 1 + t^2(z^2 + x^2 + y^2) \ge 1$ is strictly
   positive, $U_H(t)$ satisfies the exact resolvent equations $(I + i t H) U_H(t) = I - i t H$,
   is unitary ($U_H(t)^\dagger U_H(t) = U_H(t) U_H(t)^\dagger = I$) with $\det(U_H(t)) = 1$,
   satisfies the projective tangent composition law $U_H(t_1) U_H(t_2) = U_H\!\left(\frac{t_1+t_2}{1 - t_1 t_2 \|H\|^2}\right)$
   with south-pole collision $U_H(t_1) U_H(t_2) = -I$ when $t_1 t_2 \|H\|^2 = 1$, preserves the
   Born Frobenius trace on `HermitianMat2Qi`, and recovers the $(3/5, 4/5)$ Pythagorean rotation at
   $t = 1/2$ for each Pauli generator $\sigma_x, \sigma_y, \sigma_z$.

AuthorityEffect: None.
-/

namespace U1Finite.QuadraticTowerAndCayleyStone

open U1Finite.PythagoreanObstruction
open U1Finite.CauchyCircleCompletion
open U1Finite.ChebyshevCauchyBridge

/-! ## Section 1: Parametric Quadratic Extension Ring `QuadExt R d` and Universal Half-Angle Step -/

/-- Elements of the quadratic ring extension $R[\rho]/(\rho^2 - d)$, represented as $a + b\rho$. -/
@[ext]
structure QuadExt (R : Type*) (d : R) where
  a : R
  b : R
  deriving DecidableEq, Repr

namespace QuadExt

variable {R : Type*} [CommRing R] {d : R}

/-- Canonical embedding $R \hookrightarrow R[\sqrt{d}]$. -/
def ofBase (d : R) (r : R) : QuadExt R d := ⟨r, 0⟩

/-- The adjoined square-root generator $\rho = 0 + 1\cdot\rho$ satisfying $\rho^2 = d$. -/
def radGen (d : R) : QuadExt R d := ⟨0, 1⟩

/-- Galois conjugation $a + b\rho \mapsto a - b\rho$ in $R[\sqrt{d}]$. -/
def conj (x : QuadExt R d) : QuadExt R d := ⟨x.a, -x.b⟩

/-- Algebraic norm $N(a + b\rho) = a^2 - d b^2 \in R$. -/
def norm (x : QuadExt R d) : R := x.a * x.a - d * x.b * x.b

instance : Zero (QuadExt R d) := ⟨⟨0, 0⟩⟩
instance : One (QuadExt R d) := ⟨⟨1, 0⟩⟩
instance : Add (QuadExt R d) := ⟨fun x y => ⟨x.a + y.a, x.b + y.b⟩⟩
instance : Sub (QuadExt R d) := ⟨fun x y => ⟨x.a - y.a, x.b - y.b⟩⟩
instance : Neg (QuadExt R d) := ⟨fun x => ⟨-x.a, -x.b⟩⟩
instance : Mul (QuadExt R d) := ⟨fun x y => ⟨x.a * y.a + d * x.b * y.b, x.a * y.b + x.b * y.a⟩⟩
instance : NatCast (QuadExt R d) := ⟨fun n => ⟨n, 0⟩⟩
instance : IntCast (QuadExt R d) := ⟨fun z => ⟨z, 0⟩⟩

@[simp] theorem zero_a : (0 : QuadExt R d).a = 0 := rfl
@[simp] theorem zero_b : (0 : QuadExt R d).b = 0 := rfl
@[simp] theorem one_a : (1 : QuadExt R d).a = 1 := rfl
@[simp] theorem one_b : (1 : QuadExt R d).b = 0 := rfl
@[simp] theorem add_a (x y : QuadExt R d) : (x + y).a = x.a + y.a := rfl
@[simp] theorem add_b (x y : QuadExt R d) : (x + y).b = x.b + y.b := rfl
@[simp] theorem sub_a (x y : QuadExt R d) : (x - y).a = x.a - y.a := rfl
@[simp] theorem sub_b (x y : QuadExt R d) : (x - y).b = x.b - y.b := rfl
@[simp] theorem neg_a (x : QuadExt R d) : (-x).a = -x.a := rfl
@[simp] theorem neg_b (x : QuadExt R d) : (-x).b = -x.b := rfl
@[simp] theorem mul_a (x y : QuadExt R d) : (x * y).a = x.a * y.a + d * x.b * y.b := rfl
@[simp] theorem mul_b (x y : QuadExt R d) : (x * y).b = x.a * y.b + x.b * y.a := rfl
@[simp] theorem natCast_a (n : ℕ) : ((n : QuadExt R d)).a = n := rfl
@[simp] theorem natCast_b (n : ℕ) : ((n : QuadExt R d)).b = 0 := rfl
@[simp] theorem intCast_a (z : ℤ) : ((z : QuadExt R d)).a = z := rfl
@[simp] theorem intCast_b (z : ℤ) : ((z : QuadExt R d)).b = 0 := rfl
@[simp] theorem ofBase_a (r : R) : (ofBase d r).a = r := rfl
@[simp] theorem ofBase_b (r : R) : (ofBase d r).b = 0 := rfl
@[simp] theorem radGen_a : (radGen d).a = 0 := rfl
@[simp] theorem radGen_b : (radGen d).b = 1 := rfl

instance instCommRing : CommRing (QuadExt R d) where
  add := (· + ·)
  add_assoc := by intros; ext <;> simp <;> ring
  zero := 0
  zero_add := by intros; ext <;> simp
  add_zero := by intros; ext <;> simp
  nsmul := nsmulRec
  zsmul := zsmulRec
  neg := Neg.neg
  sub := Sub.sub
  sub_eq_add_neg := by intros; ext <;> simp [sub_eq_add_neg]
  neg_add_cancel := by intros; ext <;> simp
  add_comm := by intros; ext <;> simp <;> ring
  mul := (· * ·)
  left_distrib := by intros; ext <;> simp <;> ring
  right_distrib := by intros; ext <;> simp <;> ring
  zero_mul := by intros; ext <;> simp
  mul_zero := by intros; ext <;> simp
  mul_assoc := by intros; ext <;> simp <;> ring
  one := 1
  one_mul := by intros; ext <;> simp
  mul_one := by intros; ext <;> simp
  natCast := Nat.cast
  natCast_zero := by ext <;> simp
  natCast_succ := by intros; ext <;> simp
  intCast := Int.cast
  intCast_ofNat := by intros; ext <;> simp
  intCast_negSucc := by intros; ext <;> simp
  mul_comm := by intros; ext <;> simp <;> ring

/-- The adjoined generator satisfies $\rho^2 = d$. -/
theorem radGen_sq (d : R) : radGen d * radGen d = ofBase d d := by
  ext <;> simp

/-- Product with the Galois conjugate equals the embedded algebraic norm $a^2 - d b^2$. -/
theorem mul_conj_eq_norm (x : QuadExt R d) :
    x * conj x = ofBase d (norm x) := by
  ext <;> simp [conj, norm] <;> ring

/-- `ofBase` preserves addition, subtraction, and multiplication. -/
theorem ofBase_add (r s : R) : ofBase d (r + s) = ofBase d r + ofBase d s := by
  ext <;> simp

theorem ofBase_sub (r s : R) : ofBase d (r - s) = ofBase d r - ofBase d s := by
  ext <;> simp

theorem ofBase_mul (r s : R) : ofBase d (r * s) = ofBase d r * ofBase d s := by
  ext <;> simp

theorem ofBase_one : ofBase d (1 : R) = 1 := rfl

end QuadExt

/-- Bundled unit-circle half-angle state over a commutative ring $R$, carrying $(c, s) \in S^1(R)$
together with explicit multiplicative inverses $w = (1+c)^{-1}$, $v = s^{-1}$, and $\mathrm{half} = 2^{-1}$. -/
structure HalfAngleState (R : Type*) [CommRing R] where
  c : R
  s : R
  w : R
  v : R
  half : R
  h_circle : c * c + s * s = 1
  h_w : (1 + c) * w = 1
  h_v : s * v = 1
  h_half : (2 : R) * half = 1

namespace HalfAngleState

variable {R : Type*} [CommRing R]

/-- The half-angle radicand $d = \frac{1+c}{2} \in R$. -/
def radicand (st : HalfAngleState R) : R :=
  st.half * (1 + st.c)

/-- The quadratic extension carrier $R[\sqrt{(1+c)/2}]$ for the next half-angle step. -/
abbrev NextRing (st : HalfAngleState R) : Type _ :=
  QuadExt R st.radicand

/-- Half-angle cosine $c' = \rho = \sqrt{(1+c)/2}$ in $R[\sqrt{(1+c)/2}]$. -/
def nextC (st : HalfAngleState R) : st.NextRing :=
  ⟨0, 1⟩

/-- Half-angle sine $s' = (s w)\rho = \frac{s}{1+c}\sqrt{(1+c)/2}$ in $R[\sqrt{(1+c)/2}]$. -/
def nextS (st : HalfAngleState R) : st.NextRing :=
  ⟨0, st.s * st.w⟩

/-- Explicit inverse $w' = (1 + c')^{-1} = 2 v^2 (1+c)(1 - \rho)$ in $R[\sqrt{(1+c)/2}]$. -/
def nextW (st : HalfAngleState R) : st.NextRing :=
  ⟨2 * st.v * st.v * (1 + st.c), -(2 * st.v * st.v * (1 + st.c))⟩

/-- Explicit inverse $v' = (s')^{-1} = (2 v)\rho$ in $R[\sqrt{(1+c)/2}]$. -/
def nextV (st : HalfAngleState R) : st.NextRing :=
  ⟨0, 2 * st.v⟩

/-- Embedded half-unit $2^{-1}$ in $R[\sqrt{(1+c)/2}]$. -/
def nextHalf (st : HalfAngleState R) : st.NextRing :=
  QuadExt.ofBase st.radicand st.half

/-- The constructed half-angle pair $(c', s')$ lies on the unit circle $(c')^2 + (s')^2 = 1$
in $R[\sqrt{(1+c)/2}]$. -/
theorem next_on_circle (st : HalfAngleState R) :
    st.nextC * st.nextC + st.nextS * st.nextS = 1 := by
  ext
  · change (0 * 0 + st.radicand * 1 * 1) +
        (0 * 0 + st.radicand * (st.s * st.w) * (st.s * st.w)) = 1
    unfold radicand
    linear_combination
      (st.half * (1 + st.c) * st.w * st.w) * st.h_circle +
      (st.half * (1 - st.c) * ((1 + st.c) * st.w + 1)) * st.h_w +
      st.h_half
  · change (0 * 1 + 1 * 0) + (0 * (st.s * st.w) + (st.s * st.w) * 0) = 0
    ring

/-- Double-angle cosine identity: $(c')^2 - (s')^2 = c$ in $R[\sqrt{(1+c)/2}]$. -/
theorem next_double_re (st : HalfAngleState R) :
    st.nextC * st.nextC - st.nextS * st.nextS = QuadExt.ofBase st.radicand st.c := by
  ext
  · change (0 * 0 + st.radicand * 1 * 1) -
        (0 * 0 + st.radicand * (st.s * st.w) * (st.s * st.w)) = st.c
    unfold radicand
    linear_combination
      (-st.half * (1 + st.c) * st.w * st.w) * st.h_circle -
      (st.half * (1 - st.c) * ((1 + st.c) * st.w + 1)) * st.h_w +
      st.c * st.h_half
  · change (0 * 1 + 1 * 0) - (0 * (st.s * st.w) + (st.s * st.w) * 0) = 0
    ring

/-- Double-angle sine identity: $c' s' + s' c' = s$ in $R[\sqrt{(1+c)/2}]$. -/
theorem next_double_im (st : HalfAngleState R) :
    st.nextC * st.nextS + st.nextS * st.nextC = QuadExt.ofBase st.radicand st.s := by
  ext
  · change (0 * 0 + st.radicand * 1 * (st.s * st.w)) +
        (0 * 0 + st.radicand * (st.s * st.w) * 1) = st.s
    unfold radicand
    linear_combination
      (2 * st.half * st.s) * st.h_w +
      st.s * st.h_half
  · change (0 * (st.s * st.w) + 1 * 0) + (0 * 1 + (st.s * st.w) * 0) = 0
    ring

/-- Explicit invertibility of $1 + c'$: $(1 + c') w' = 1$ in $R[\sqrt{(1+c)/2}]$. -/
theorem next_w_inv (st : HalfAngleState R) :
    (1 + st.nextC) * st.nextW = 1 := by
  ext
  · change (1 + 0) * (2 * st.v * st.v * (1 + st.c)) +
        st.radicand * (0 + 1) * -(2 * st.v * st.v * (1 + st.c)) = 1
    unfold radicand
    linear_combination
      (-st.v * st.v) * st.h_circle +
      (st.s * st.v + 1) * st.h_v -
      (st.v * st.v * (1 + st.c) * (1 + st.c)) * st.h_half
  · change (1 + 0) * -(2 * st.v * st.v * (1 + st.c)) +
        (0 + 1) * (2 * st.v * st.v * (1 + st.c)) = 0
    ring

/-- Explicit invertibility of $s'$: $s' v' = 1$ in $R[\sqrt{(1+c)/2}]$. -/
theorem next_v_inv (st : HalfAngleState R) :
    st.nextS * st.nextV = 1 := by
  ext
  · change 0 * 0 + st.radicand * (st.s * st.w) * (2 * st.v) = 1
    unfold radicand
    linear_combination
      (2 * st.half * (1 + st.c) * st.w) * st.h_v +
      (2 * st.half) * st.h_w +
      st.h_half
  · change 0 * (2 * st.v) + (st.s * st.w) * 0 = 0
    ring

/-- Explicit invertibility of $2$ in $R[\sqrt{(1+c)/2}]$. -/
theorem next_half_inv (st : HalfAngleState R) :
    (2 : st.NextRing) * st.nextHalf = 1 := by
  ext
  · change (2 : R) * st.half + st.radicand * 0 * 0 = 1
    linear_combination st.h_half
  · change (2 : R) * 0 + 0 * st.half = 0
    ring

/-- The inductive step constructor: maps a `HalfAngleState R` to a `HalfAngleState (QuadExt R d)`
where $d = \frac{1+c}{2}$. -/
def step (st : HalfAngleState R) : HalfAngleState st.NextRing where
  c := st.nextC
  s := st.nextS
  w := st.nextW
  v := st.nextV
  half := st.nextHalf
  h_circle := st.next_on_circle
  h_w := st.next_w_inv
  h_v := st.next_v_inv
  h_half := st.next_half_inv

/-- Both radical coordinates of the new half-angle state $(c', s')$ have zero base part and
invertible radical part (`c'.b = 1` and `s'.b * ((1+c) * v) = 1`). -/
theorem next_radical_components (st : HalfAngleState R) :
    st.nextC.a = 0 ∧ st.nextC.b = 1 ∧
    st.nextS.a = 0 ∧ st.nextS.b * ((1 + st.c) * st.v) = 1 := by
  refine ⟨rfl, rfl, rfl, ?_⟩
  change (st.s * st.w) * ((1 + st.c) * st.v) = 1
  linear_combination (st.s * st.v) * st.h_w + st.h_v

end HalfAngleState

/-! ## Section 2: Inductively Defined $2^m$-Division Tower $K_m$ for $u_{345} = (3/5, 4/5)$ -/

/-- Gaussian multiplication $(x_1, y_1) \cdot (x_2, y_2) = (x_1 x_2 - y_1 y_2, x_1 y_2 + y_1 x_2)$
over any commutative ring $R$. -/
def ringCircleMul {R : Type*} [CommRing R] (z w : R × R) : R × R :=
  (z.1 * w.1 - z.2 * w.2, z.1 * w.2 + z.2 * w.1)

/-- Iterated squaring map $z \mapsto z^{2^k}$ on $R \times R$:
`iterCircleSq 0 z = z` and `iterCircleSq (k+1) z = iterCircleSq k (ringCircleMul z z)`. -/
def iterCircleSq {R : Type*} [CommRing R] : ℕ → R × R → R × R
  | 0, z => z
  | k + 1, z => iterCircleSq k (ringCircleMul z z)

/-- Ring homomorphisms commute with `ringCircleMul`. -/
theorem map_ringCircleMul {R S : Type*} [CommRing R] [CommRing S]
    (f : R → S) (hf_sub : ∀ x y, f (x - y) = f x - f y)
    (hf_add : ∀ x y, f (x + y) = f x + f y)
    (hf_mul : ∀ x y, f (x * y) = f x * f y) (z w : R × R) :
    (f (ringCircleMul z w).1, f (ringCircleMul z w).2) =
      ringCircleMul (f z.1, f z.2) (f w.1, f w.2) := by
  ext <;> simp [ringCircleMul, hf_sub, hf_add, hf_mul]

/-- Ring homomorphisms commute with `iterCircleSq`. -/
theorem map_iterCircleSq {R S : Type*} [CommRing R] [CommRing S]
    (f : R → S) (hf_sub : ∀ x y, f (x - y) = f x - f y)
    (hf_add : ∀ x y, f (x + y) = f x + f y)
    (hf_mul : ∀ x y, f (x * y) = f x * f y) :
    ∀ k : ℕ, ∀ z : R × R,
      (f (iterCircleSq k z).1, f (iterCircleSq k z).2) =
        iterCircleSq k (f z.1, f z.2)
  | 0, z => rfl
  | k + 1, z => by
      simp only [iterCircleSq]
      rw [map_iterCircleSq f hf_sub hf_add hf_mul k (ringCircleMul z z)]
      rw [map_ringCircleMul f hf_sub hf_add hf_mul z z]

/-- Base level $m = 0$ half-angle state for $u_{345} = (3/5, 4/5)$ over $K_0 = \mathbb{Q}$. -/
def u345BaseState : HalfAngleState ℚ where
  c := 3 / 5
  s := 4 / 5
  w := 5 / 8
  v := 5 / 4
  half := 1 / 2
  h_circle := by norm_num
  h_w := by norm_num
  h_v := by norm_num
  h_half := by norm_num

/-- Bundled level-$m$ carrier and state in the iterated real quadratic square-root tower
$K_{m+1} = K_m(\sqrt{(1+c_m)/2})$ starting at $K_0 = \mathbb{Q}$ and $(c_0, s_0) = (3/5, 4/5)$. -/
structure TowerNode where
  Carrier : Type
  instRing : CommRing Carrier
  state : @HalfAngleState Carrier instRing

attribute [instance] TowerNode.instRing

/-- Recursive construction of the infinite quadratic square-root tower $K_m$ for all $m \in \mathbb{N}$. -/
@[reducible] def u345Tower : ℕ → TowerNode
  | 0 => ⟨ℚ, inferInstance, u345BaseState⟩
  | m + 1 =>
    let prev := u345Tower m
    ⟨prev.state.NextRing, inferInstance, prev.state.step⟩

/-- Carrier ring $K_m$ at level $m$ of the iterated square-root tower. -/
abbrev TowerRing (m : ℕ) : Type := (u345Tower m).Carrier

instance instCommRingTowerRing (m : ℕ) : CommRing (TowerRing m) :=
  (u345Tower m).instRing

/-- The bundled half-angle state $(c_m, s_m, w_m, v_m)$ in $K_m$. -/
@[reducible] def towerState (m : ℕ) : HalfAngleState (TowerRing m) :=
  (u345Tower m).state

/-- The unit-circle point $(c_m, s_m) \in K_m \times K_m$ at level $m$. -/
def towerCirclePoint (m : ℕ) : TowerRing m × TowerRing m :=
  ((towerState m).c, (towerState m).s)

/-- Canonical embedding $\iota_m : K_0 = \mathbb{Q} \hookrightarrow K_m$ of rationals into level $m$
of the quadratic tower. -/
def embedRatTower : ∀ m : ℕ, ℚ → TowerRing m
  | 0, q => q
  | m + 1, q => QuadExt.ofBase (towerState m).radicand (embedRatTower m q)

/-- At every level $m \in \mathbb{N}$ of the tower, $(c_m, s_m)$ lies on the unit circle
$c_m^2 + s_m^2 = 1$ in $K_m$. -/
theorem towerState_on_circle (m : ℕ) :
    (towerState m).c * (towerState m).c + (towerState m).s * (towerState m).s = 1 :=
  (towerState m).h_circle

/-- Squaring $(c_{m+1}, s_{m+1})$ in $K_{m+1} = K_m(\sqrt{(1+c_m)/2})$ recovers the embedded
level-$m$ circle point $(c_m, s_m)$. -/
theorem towerCirclePoint_sq_eq_prev (m : ℕ) :
    ringCircleMul (towerCirclePoint (m + 1)) (towerCirclePoint (m + 1)) =
      (QuadExt.ofBase (towerState m).radicand (towerState m).c,
       QuadExt.ofBase (towerState m).radicand (towerState m).s) :=
  Prod.ext (towerState m).next_double_re (towerState m).next_double_im

/-- **Main $2^m$-Division Tower Theorem (`FQ-GAP-U1-CIRCLE`)**:
For every level $m \in \mathbb{N}$, raising the level-$m$ half-angle point $(c_m, s_m) \in S^1(K_m)$
to the $2^m$-th power via `iterCircleSq m` recovers the embedded Pythagorean generator
$u_{345} = (3/5, 4/5)$ in $K_m \times K_m$. -/
theorem towerState_pow_two_pow_eq_u345 : ∀ m : ℕ,
    iterCircleSq m (towerCirclePoint m) =
      (embedRatTower m (3 / 5), embedRatTower m (4 / 5))
  | 0 => rfl
  | m + 1 => by
      change iterCircleSq m (ringCircleMul (towerCirclePoint (m + 1)) (towerCirclePoint (m + 1))) =
        (QuadExt.ofBase (towerState m).radicand (embedRatTower m (3 / 5)),
         QuadExt.ofBase (towerState m).radicand (embedRatTower m (4 / 5)))
      rw [towerCirclePoint_sq_eq_prev m]
      have hmap := map_iterCircleSq
        (QuadExt.ofBase (towerState m).radicand)
        (fun x y => QuadExt.ofBase_sub x y)
        (fun x y => QuadExt.ofBase_add x y)
        (fun x y => QuadExt.ofBase_mul x y)
        m (towerCirclePoint m)
      change (QuadExt.ofBase (towerState m).radicand (iterCircleSq m (towerCirclePoint m)).1,
              QuadExt.ofBase (towerState m).radicand (iterCircleSq m (towerCirclePoint m)).2) =
             iterCircleSq m (QuadExt.ofBase (towerState m).radicand (towerState m).c,
                             QuadExt.ofBase (towerState m).radicand (towerState m).s) at hmap
      rw [← hmap, towerState_pow_two_pow_eq_u345 m]

/-- Level $m = 1$ specialization: the first radicand is $d_0 = \frac{1 + 3/5}{2} = \frac{4}{5}$,
and $(c_1, s_1) = (\rho_0, \frac{1}{2}\rho_0)$ in $K_1 = \mathbb{Q}(\sqrt{4/5})$. -/
theorem tower_level_one_explicit :
    (u345BaseState.radicand : ℚ) = 4 / 5 ∧
    (towerState 1).c.a = (0 : ℚ) ∧ (towerState 1).c.b = (1 : ℚ) ∧
    (towerState 1).s.a = (0 : ℚ) ∧ (towerState 1).s.b = (1 / 2 : ℚ) ∧
    (towerState 1).w.a = (5 : ℚ) ∧ (towerState 1).w.b = (-5 : ℚ) ∧
    (towerState 1).v.a = (0 : ℚ) ∧ (towerState 1).v.b = (5 / 2 : ℚ) := by
  refine ⟨?_, rfl, rfl, rfl, ?_, ?_, ?_, rfl, ?_⟩
  · change (1 / 2 : ℚ) * (1 + 3 / 5) = 4 / 5; norm_num
  · change (4 / 5 : ℚ) * (5 / 8) = 1 / 2; norm_num
  · change 2 * (5 / 4 : ℚ) * (5 / 4) * (1 + 3 / 5) = 5; norm_num
  · change -(2 * (5 / 4 : ℚ) * (5 / 4) * (1 + 3 / 5)) = -5; norm_num
  · change 2 * (5 / 4 : ℚ) = 5 / 2; norm_num

/-- Level $m = 2$ specialization (quarter-angle $u_{345}^{1/4}$): in $K_2 = K_1(\sqrt{(1+\rho_0)/2})$,
the radicand is $d_1 = \frac{1}{2} + \frac{1}{2}\rho_0$, and $s_2 = \left(-2 + \frac{5}{2}\rho_0\right)\rho_1$. -/
theorem tower_level_two_radicand_and_sine :
    ((towerState 1).radicand.a : ℚ) = 1 / 2 ∧
    ((towerState 1).radicand.b : ℚ) = 1 / 2 ∧
    ((towerState 2).c.b.a : ℚ) = 1 ∧
    ((towerState 2).s.b.a : ℚ) = -2 ∧
    ((towerState 2).s.b.b : ℚ) = 5 / 2 := by
  refine ⟨?_, ?_, rfl, ?_, ?_⟩
  · change (1 / 2 : ℚ) * (1 + 0) + (1 / 2 * (1 + 3 / 5)) * 0 * (0 + 1) = 1 / 2; norm_num
  · change (1 / 2 : ℚ) * (0 + 1) + 0 * (1 + 0) = 1 / 2; norm_num
  · change (0 : ℚ) * (2 * (5 / 4) * (5 / 4) * (1 + 3 / 5)) +
      (1 / 2 * (1 + 3 / 5)) * (4 / 5 * (5 / 8)) * -(2 * (5 / 4) * (5 / 4) * (1 + 3 / 5)) = -2
    norm_num
  · change (0 : ℚ) * -(2 * (5 / 4) * (5 / 4) * (1 + 3 / 5)) +
      (4 / 5 * (5 / 8)) * (2 * (5 / 4) * (5 / 4) * (1 + 3 / 5)) = 5 / 2
    norm_num

/-! ## Section 3: Discrete Cayley Unitary Step $(I - i t H)(I + i t H)^{-1}$ on `HermitianMat2Qi` (`FQ-GAP-STONE-CONTINUOUS-TIME`) -/

/-- Elements of the Gaussian-rational field $\mathbb{Q}(i)$, represented as `re + i im`. -/
@[ext]
structure GaussRat where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Repr

namespace GaussRat

def zero : GaussRat := ⟨0, 0⟩
def one : GaussRat := ⟨1, 0⟩
def iUnit : GaussRat := ⟨0, 1⟩
def ofRat (q : ℚ) : GaussRat := ⟨q, 0⟩
def conj (z : GaussRat) : GaussRat := ⟨z.re, -z.im⟩
def normSq (z : GaussRat) : ℚ := z.re * z.re + z.im * z.im

instance : Zero GaussRat := ⟨zero⟩
instance : One GaussRat := ⟨one⟩
instance : Add GaussRat := ⟨fun z w => ⟨z.re + w.re, z.im + w.im⟩⟩
instance : Sub GaussRat := ⟨fun z w => ⟨z.re - w.re, z.im - w.im⟩⟩
instance : Neg GaussRat := ⟨fun z => ⟨-z.re, -z.im⟩⟩
instance : Mul GaussRat := ⟨fun z w => ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩⟩

@[simp] theorem zero_re : (0 : GaussRat).re = 0 := rfl
@[simp] theorem zero_im : (0 : GaussRat).im = 0 := rfl
@[simp] theorem one_re : (1 : GaussRat).re = 1 := rfl
@[simp] theorem one_im : (1 : GaussRat).im = 0 := rfl
@[simp] theorem iUnit_re : iUnit.re = 0 := rfl
@[simp] theorem iUnit_im : iUnit.im = 1 := rfl
@[simp] theorem ofRat_re (q : ℚ) : (ofRat q).re = q := rfl
@[simp] theorem ofRat_im (q : ℚ) : (ofRat q).im = 0 := rfl
@[simp] theorem conj_re (z : GaussRat) : (conj z).re = z.re := rfl
@[simp] theorem conj_im (z : GaussRat) : (conj z).im = -z.im := rfl
@[simp] theorem add_re (z w : GaussRat) : (z + w).re = z.re + w.re := rfl
@[simp] theorem add_im (z w : GaussRat) : (z + w).im = z.im + w.im := rfl
@[simp] theorem sub_re (z w : GaussRat) : (z - w).re = z.re - w.re := rfl
@[simp] theorem sub_im (z w : GaussRat) : (z - w).im = z.im - w.im := rfl
@[simp] theorem neg_re (z : GaussRat) : (-z).re = -z.re := rfl
@[simp] theorem neg_im (z : GaussRat) : (-z).im = -z.im := rfl
@[simp] theorem mul_re (z w : GaussRat) : (z * w).re = z.re * w.re - z.im * w.im := rfl
@[simp] theorem mul_im (z w : GaussRat) : (z * w).im = z.re * w.im + z.im * w.re := rfl

end GaussRat

/-- $2 \times 2$ matrices over $\mathbb{Q}(i)$. -/
@[ext]
structure Mat2Qi where
  m11 : GaussRat
  m12 : GaussRat
  m21 : GaussRat
  m22 : GaussRat
  deriving DecidableEq, Repr

namespace Mat2Qi

/-- Identity matrix $I_2 \in M_2(\mathbb{Q}(i))$. -/
def idMat : Mat2Qi := ⟨1, 0, 0, 1⟩

/-- Negative identity matrix $-I_2 \in M_2(\mathbb{Q}(i))$. -/
def negIdMat : Mat2Qi := ⟨-1, 0, 0, -1⟩

/-- Conjugate transpose (Hermitian adjoint) $M^\dagger$. -/
def dagger (M : Mat2Qi) : Mat2Qi :=
  ⟨GaussRat.conj M.m11, GaussRat.conj M.m21, GaussRat.conj M.m12, GaussRat.conj M.m22⟩

/-- Matrix multiplication in $M_2(\mathbb{Q}(i))$. -/
def mul (A B : Mat2Qi) : Mat2Qi :=
  ⟨A.m11 * B.m11 + A.m12 * B.m21,
   A.m11 * B.m12 + A.m12 * B.m22,
   A.m21 * B.m11 + A.m22 * B.m21,
   A.m21 * B.m12 + A.m22 * B.m22⟩

/-- Scalar multiplication by $q \in \mathbb{Q}$. -/
def smulRat (q : ℚ) (M : Mat2Qi) : Mat2Qi :=
  ⟨GaussRat.ofRat q * M.m11,
   GaussRat.ofRat q * M.m12,
   GaussRat.ofRat q * M.m21,
   GaussRat.ofRat q * M.m22⟩

/-- Matrix trace $\operatorname{tr}(M) \in \mathbb{Q}(i)$. -/
def tr (M : Mat2Qi) : GaussRat := M.m11 + M.m22

/-- Matrix determinant $\det(M) \in \mathbb{Q}(i)$. -/
def det (M : Mat2Qi) : GaussRat := M.m11 * M.m22 - M.m12 * M.m21

/-- Canonical embedding of `HermitianMat2Qi` into $M_2(\mathbb{Q}(i))$. -/
def ofHermitian (H : HermitianMat2Qi) : Mat2Qi :=
  ⟨⟨H.d1, 0⟩, ⟨H.br, -H.bi⟩, ⟨H.br, H.bi⟩, ⟨H.d2, 0⟩⟩

/-- Every embedded `HermitianMat2Qi` is self-adjoint: $(ofHermitian H)^\dagger = ofHermitian H$. -/
theorem ofHermitian_dagger (H : HermitianMat2Qi) :
    dagger (ofHermitian H) = ofHermitian H := by
  ext <;> simp [dagger, ofHermitian]

/-- Associativity of matrix multiplication in $M_2(\mathbb{Q}(i))$. -/
theorem mul_assoc (A B C : Mat2Qi) :
    mul (mul A B) C = mul A (mul B C) := by
  ext <;> simp [mul] <;> ring

/-- Left identity law in $M_2(\mathbb{Q}(i))$. -/
theorem mul_id_left (A : Mat2Qi) :
    mul idMat A = A := by
  ext <;> simp [mul, idMat]

/-- Cyclicity of the matrix trace: $\operatorname{tr}(A B) = \operatorname{tr}(B A)$. -/
theorem tr_mul_comm (A B : Mat2Qi) :
    tr (mul A B) = tr (mul B A) := by
  ext <;> simp [tr, mul] <;> ring

end Mat2Qi

/-- Traceless $2 \times 2$ Hermitian generator $H = z\sigma_z + x\sigma_x + y\sigma_y \in \mathfrak{su}(2)_{\mathbb{Q}}$
inside `HermitianMat2Qi`. -/
@[ext]
structure TracelessHerm2Qi where
  z : ℚ
  x : ℚ
  y : ℚ
  deriving DecidableEq, Repr

namespace TracelessHerm2Qi

/-- View a traceless Hermitian generator as an element of `HermitianMat2Qi` with $d_1 = z, d_2 = -z$. -/
def toHermitian (H : TracelessHerm2Qi) : HermitianMat2Qi :=
  ⟨H.z, -H.z, H.x, H.y⟩

/-- View a traceless Hermitian generator as a $2 \times 2$ matrix over $\mathbb{Q}(i)$. -/
def toMat (H : TracelessHerm2Qi) : Mat2Qi :=
  Mat2Qi.ofHermitian H.toHermitian

/-- Squared Frobenius/Bloch norm $\|H\|^2 = z^2 + x^2 + y^2 \in \mathbb{Q}$. -/
def normSq (H : TracelessHerm2Qi) : ℚ :=
  H.z * H.z + H.x * H.x + H.y * H.y

/-- Pauli generators $\sigma_z, \sigma_x, \sigma_y$. -/
def pauliZ : TracelessHerm2Qi := ⟨1, 0, 0⟩
def pauliX : TracelessHerm2Qi := ⟨0, 1, 0⟩
def pauliY : TracelessHerm2Qi := ⟨0, 0, 1⟩

/-- The forward Cayley factor $I + i t H \in M_2(\mathbb{Q}(i))$. -/
def plusItH (H : TracelessHerm2Qi) (t : ℚ) : Mat2Qi :=
  ⟨⟨1, t * H.z⟩, ⟨t * H.y, t * H.x⟩, ⟨-t * H.y, t * H.x⟩, ⟨1, -t * H.z⟩⟩

/-- The backward Cayley factor $I - i t H \in M_2(\mathbb{Q}(i))$. -/
def minusItH (H : TracelessHerm2Qi) (t : ℚ) : Mat2Qi :=
  ⟨⟨1, -t * H.z⟩, ⟨-t * H.y, -t * H.x⟩, ⟨t * H.y, -t * H.x⟩, ⟨1, t * H.z⟩⟩

/-- The scalar Cayley denominator $\Delta(H, t) = 1 + t^2 (z^2 + x^2 + y^2) \in \mathbb{Q}$. -/
def cayleyDenom (H : TracelessHerm2Qi) (t : ℚ) : ℚ :=
  1 + t * t * H.normSq

/-- Scalar Cayley cosine coefficient $\alpha(H, t) = \frac{1 - t^2 \|H\|^2}{\Delta(H, t)}$. -/
def cayleyAlpha (H : TracelessHerm2Qi) (t : ℚ) : ℚ :=
  (1 - t * t * H.normSq) / H.cayleyDenom t

/-- Scalar Cayley sine coefficient $\beta(H, t) = \frac{2 t}{\Delta(H, t)}$. -/
def cayleyBeta (H : TracelessHerm2Qi) (t : ℚ) : ℚ :=
  (2 * t) / H.cayleyDenom t

/-- Non-negativity of the squared generator norm: $0 \le \|H\|^2$. -/
theorem normSq_nonneg (H : TracelessHerm2Qi) :
    0 ≤ H.normSq := by
  unfold normSq
  have hz : 0 ≤ H.z ^ 2 := sq_nonneg H.z
  have hx : 0 ≤ H.x ^ 2 := sq_nonneg H.x
  have hy : 0 ≤ H.y ^ 2 := sq_nonneg H.y
  linarith

/-- Unconditional positivity of the Cayley denominator: $1 \le \Delta(H, t)$ for all $t \in \mathbb{Q}$. -/
theorem cayleyDenom_ge_one (H : TracelessHerm2Qi) (t : ℚ) :
    1 ≤ H.cayleyDenom t := by
  unfold cayleyDenom
  have h1 : 0 ≤ (t * t) * H.normSq := mul_nonneg (mul_self_nonneg t) H.normSq_nonneg
  linarith

theorem cayleyDenom_pos (H : TracelessHerm2Qi) (t : ℚ) :
    0 < H.cayleyDenom t :=
  lt_of_lt_of_le zero_lt_one (H.cayleyDenom_ge_one t)

theorem cayleyDenom_ne_zero (H : TracelessHerm2Qi) (t : ℚ) :
    H.cayleyDenom t ≠ 0 :=
  ne_of_gt (H.cayleyDenom_pos t)

/-- Linear combination of $I_2$ and $-i H$ with coefficients $(c, s) \in \mathbb{Q}^2$:
`linComb H c s = c I_2 - s i H`. -/
def linComb (H : TracelessHerm2Qi) (c s : ℚ) : Mat2Qi :=
  ⟨⟨c, -s * H.z⟩,
   ⟨-s * H.y, -s * H.x⟩,
   ⟨s * H.y, -s * H.x⟩,
   ⟨c, s * H.z⟩⟩

/-- Multiplication law in the commutative subalgebra $\mathbb{Q}[i H] \subset M_2(\mathbb{Q}(i))$:
$$(c_1 I - s_1 i H)(c_2 I - s_2 i H) = (c_1 c_2 - s_1 s_2 \|H\|^2) I - (c_1 s_2 + s_1 c_2) i H.$$ -/
theorem linComb_mul (H : TracelessHerm2Qi) (c₁ s₁ c₂ s₂ : ℚ) :
    Mat2Qi.mul (H.linComb c₁ s₁) (H.linComb c₂ s₂) =
      H.linComb (c₁ * c₂ - s₁ * s₂ * H.normSq) (c₁ * s₂ + s₁ * c₂) := by
  ext <;> simp [Mat2Qi.mul, linComb, normSq] <;> ring

/-- The discrete Cayley unitary propagator
$$U_H(t) = (I - i t H)(I + i t H)^{-1} = \frac{1 - t^2\|H\|^2}{1 + t^2\|H\|^2} I - \frac{2t}{1 + t^2\|H\|^2} i H$$
over $\mathbb{Q}(i)$. -/
def cayleyStep (H : TracelessHerm2Qi) (t : ℚ) : Mat2Qi :=
  H.linComb (H.cayleyAlpha t) (H.cayleyBeta t)

/-- Adjoint duality of the Cayley factors: $(I - i t H)^\dagger = I + i t H$. -/
theorem minusItH_dagger (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.dagger (H.minusItH t) = H.plusItH t := by
  ext <;> simp [Mat2Qi.dagger, minusItH, plusItH]

/-- Clifford-Pauli involution identity: $(I + i t H)(I - i t H) = \Delta(H, t)\,I_2$. -/
theorem plusItH_mul_minusItH (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.mul (H.plusItH t) (H.minusItH t) = Mat2Qi.smulRat (H.cayleyDenom t) Mat2Qi.idMat := by
  ext <;> simp [Mat2Qi.mul, Mat2Qi.smulRat, Mat2Qi.idMat, plusItH, minusItH, cayleyDenom, normSq] <;> ring

/-- Exact right resolvent equation: $(I + i t H)\,U_H(t) = I - i t H$. -/
theorem cayleyStep_resolvent_right (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.mul (H.plusItH t) (H.cayleyStep t) = H.minusItH t := by
  have hd : H.cayleyDenom t ≠ 0 := H.cayleyDenom_ne_zero t
  have hplus : H.plusItH t = H.linComb 1 (-t) := by
    ext <;> simp [plusItH, linComb]
  have hminus : H.minusItH t = H.linComb 1 t := by
    ext <;> simp [minusItH, linComb]
  rw [hplus, hminus, cayleyStep, linComb_mul]
  congr 1
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring

/-- Exact left resolvent equation: $U_H(t)\,(I + i t H) = I - i t H$. -/
theorem cayleyStep_resolvent_left (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.mul (H.cayleyStep t) (H.plusItH t) = H.minusItH t := by
  have hd : H.cayleyDenom t ≠ 0 := H.cayleyDenom_ne_zero t
  have hplus : H.plusItH t = H.linComb 1 (-t) := by
    ext <;> simp [plusItH, linComb]
  have hminus : H.minusItH t = H.linComb 1 t := by
    ext <;> simp [minusItH, linComb]
  rw [hplus, hminus, cayleyStep, linComb_mul]
  congr 1
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring

/-- Time-reversal symmetry: $U_H(t)^\dagger = U_H(-t)$ for all $t \in \mathbb{Q}$. -/
theorem cayleyStep_dagger_eq_neg (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.dagger (H.cayleyStep t) = H.cayleyStep (-t) := by
  ext <;> simp [Mat2Qi.dagger, cayleyStep, linComb, cayleyAlpha, cayleyBeta, cayleyDenom] <;> ring

/-- Left unitarity: $U_H(t)^\dagger\,U_H(t) = I_2$ for all $t \in \mathbb{Q}$. -/
theorem cayleyStep_unitary_left (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.mul (Mat2Qi.dagger (H.cayleyStep t)) (H.cayleyStep t) = Mat2Qi.idMat := by
  have hd : H.cayleyDenom t ≠ 0 := H.cayleyDenom_ne_zero t
  have hdag : Mat2Qi.dagger (H.cayleyStep t) = H.linComb (H.cayleyAlpha t) (-H.cayleyBeta t) := by
    ext <;> simp [Mat2Qi.dagger, cayleyStep, linComb]
  have hid : Mat2Qi.idMat = H.linComb 1 0 := by
    ext <;> simp [Mat2Qi.idMat, linComb]
  rw [hdag, cayleyStep, linComb_mul, hid]
  congr 1
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring
  · unfold cayleyAlpha cayleyBeta
    ring

/-- Right unitarity: $U_H(t)\,U_H(t)^\dagger = I_2$ for all $t \in \mathbb{Q}$. -/
theorem cayleyStep_unitary_right (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.mul (H.cayleyStep t) (Mat2Qi.dagger (H.cayleyStep t)) = Mat2Qi.idMat := by
  have hd : H.cayleyDenom t ≠ 0 := H.cayleyDenom_ne_zero t
  have hdag : Mat2Qi.dagger (H.cayleyStep t) = H.linComb (H.cayleyAlpha t) (-H.cayleyBeta t) := by
    ext <;> simp [Mat2Qi.dagger, cayleyStep, linComb]
  have hid : Mat2Qi.idMat = H.linComb 1 0 := by
    ext <;> simp [Mat2Qi.idMat, linComb]
  rw [hdag, cayleyStep, linComb_mul, hid]
  congr 1
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring
  · unfold cayleyAlpha cayleyBeta
    ring

/-- Identity at $t = 0$: $U_H(0) = I_2$. -/
theorem cayleyStep_zero (H : TracelessHerm2Qi) :
    H.cayleyStep 0 = Mat2Qi.idMat := by
  ext <;> simp [cayleyStep, linComb, cayleyAlpha, cayleyBeta, cayleyDenom, Mat2Qi.idMat]

/-- Special unitary determinant: $\det(U_H(t)) = 1$ for all $t \in \mathbb{Q}$. -/
theorem cayleyStep_det_eq_one (H : TracelessHerm2Qi) (t : ℚ) :
    Mat2Qi.det (H.cayleyStep t) = 1 := by
  have hd : H.cayleyDenom t ≠ 0 := H.cayleyDenom_ne_zero t
  have hdet : Mat2Qi.det (H.cayleyStep t) =
      ⟨H.cayleyAlpha t * H.cayleyAlpha t +
        H.cayleyBeta t * H.cayleyBeta t * H.normSq, 0⟩ := by
    ext <;> simp [Mat2Qi.det, cayleyStep, linComb, normSq] <;> ring
  rw [hdet]
  ext
  · change H.cayleyAlpha t * H.cayleyAlpha t + H.cayleyBeta t * H.cayleyBeta t * H.normSq = 1
    unfold cayleyAlpha cayleyBeta
    field_simp [hd]
    unfold cayleyDenom
    ring
  · rfl

/-- Commutativity of Cayley steps generated by the same $H$:
$U_H(t_1)\,U_H(t_2) = U_H(t_2)\,U_H(t_1)$. -/
theorem cayleyStep_comm (H : TracelessHerm2Qi) (t₁ t₂ : ℚ) :
    Mat2Qi.mul (H.cayleyStep t₁) (H.cayleyStep t₂) =
      Mat2Qi.mul (H.cayleyStep t₂) (H.cayleyStep t₁) := by
  simp only [cayleyStep, linComb_mul]
  congr 1 <;> ring

/-- Projective / tangent composition law for the discrete Cayley step (`FQ-GAP-STONE-CONTINUOUS-TIME`):
whenever $1 - t_1 t_2 \|H\|^2 \neq 0$,
$$U_H(t_1)\,U_H(t_2) = U_H\!\left(\frac{t_1 + t_2}{1 - t_1 t_2 \|H\|^2}\right).$$
Notice that the parameter composition is rational projective-tangent rather than additive $t_1 + t_2$. -/
theorem cayleyStep_comp_regular (H : TracelessHerm2Qi) (t₁ t₂ : ℚ)
    (h_reg : 1 - t₁ * t₂ * H.normSq ≠ 0) :
    Mat2Qi.mul (H.cayleyStep t₁) (H.cayleyStep t₂) =
      H.cayleyStep ((t₁ + t₂) / (1 - t₁ * t₂ * H.normSq)) := by
  have hd1 : H.cayleyDenom t₁ ≠ 0 := H.cayleyDenom_ne_zero t₁
  have hd2 : H.cayleyDenom t₂ ≠ 0 := H.cayleyDenom_ne_zero t₂
  generalize hd_eq : 1 - t₁ * t₂ * H.normSq = d at h_reg ⊢
  have hd3 : H.cayleyDenom ((t₁ + t₂) / d) ≠ 0 := H.cayleyDenom_ne_zero ((t₁ + t₂) / d)
  simp only [cayleyStep, linComb_mul]
  congr 1
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd1, hd2, hd3, h_reg]
    unfold cayleyDenom
    field_simp [h_reg]
    subst hd_eq
    ring
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd1, hd2, hd3, h_reg]
    unfold cayleyDenom
    field_simp [h_reg]
    subst hd_eq
    ring

/-- South-pole collision of the affine Cayley time parameter: when $t_1 t_2 = 1$
and $\|H\|^2 = 1$, $U_H(t_1)\,U_H(t_2) = -I_2$. -/
theorem cayleyStep_comp_pole (H : TracelessHerm2Qi) (t₁ t₂ : ℚ)
    (h_unit : H.normSq = 1) (h_pole : t₁ * t₂ = 1) :
    Mat2Qi.mul (H.cayleyStep t₁) (H.cayleyStep t₂) = Mat2Qi.negIdMat := by
  have hd1 : H.cayleyDenom t₁ ≠ 0 := H.cayleyDenom_ne_zero t₁
  have hd2 : H.cayleyDenom t₂ ≠ 0 := H.cayleyDenom_ne_zero t₂
  have hneg : Mat2Qi.negIdMat = H.linComb (-1) 0 := by
    ext <;> simp [Mat2Qi.negIdMat, linComb]
  simp only [cayleyStep, linComb_mul, hneg]
  congr 1
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd1, hd2]
    unfold cayleyDenom
    rw [h_unit]
    linear_combination (2 * (t₁ * t₂ - 1)) * h_pole
  · unfold cayleyAlpha cayleyBeta
    field_simp [hd1, hd2]
    unfold cayleyDenom
    rw [h_unit]
    linear_combination (-2 * (t₁ + t₂)) * h_pole

/-- Born trace preservation under Cayley unitary evolution:
for any `W : HermitianMat2Qi` and any traceless generator $H$,
$\operatorname{tr}(U_H(t)\,W\,U_H(t)^\dagger) = \operatorname{tr}(W)$. -/
theorem cayleyStep_preserves_born_trace (H : TracelessHerm2Qi) (t : ℚ) (W : HermitianMat2Qi) :
    Mat2Qi.tr (Mat2Qi.mul (Mat2Qi.mul (H.cayleyStep t) (Mat2Qi.ofHermitian W))
      (Mat2Qi.dagger (H.cayleyStep t))) =
      Mat2Qi.tr (Mat2Qi.ofHermitian W) := by
  rw [Mat2Qi.tr_mul_comm, ← Mat2Qi.mul_assoc, H.cayleyStep_unitary_left t, Mat2Qi.mul_id_left]

/-- Recovery of the Pythagorean $(3/5, 4/5)$ rotation from Pauli generators at $t = 1/2$:
for $H = \sigma_z$, $U_{\sigma_z}(1/2) = \operatorname{diag}(3/5 - 4/5 i,\, 3/5 + 4/5 i)$. -/
theorem cayleyStep_pauliZ_half :
    pauliZ.cayleyStep (1 / 2) =
      ⟨⟨3 / 5, -4 / 5⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨3 / 5, 4 / 5⟩⟩ := by
  ext <;> simp [pauliZ, cayleyStep, linComb, cayleyAlpha, cayleyBeta, cayleyDenom, normSq] <;> norm_num

/-- For $H = \sigma_x$ at $t = 1/2$, $U_{\sigma_x}(1/2) = \frac{3}{5} I_2 - \frac{4}{5} i \sigma_x$. -/
theorem cayleyStep_pauliX_half :
    pauliX.cayleyStep (1 / 2) =
      ⟨⟨3 / 5, 0⟩, ⟨0, -4 / 5⟩, ⟨0, -4 / 5⟩, ⟨3 / 5, 0⟩⟩ := by
  ext <;> simp [pauliX, cayleyStep, linComb, cayleyAlpha, cayleyBeta, cayleyDenom, normSq] <;> norm_num

/-- For $H = \sigma_y$ at $t = 1/2$, $U_{\sigma_y}(1/2) = \frac{3}{5} I_2 - \frac{4}{5} i \sigma_y$
(a real orthogonal rotation matrix with entries $\pm 3/5, \pm 4/5$). -/
theorem cayleyStep_pauliY_half :
    pauliY.cayleyStep (1 / 2) =
      ⟨⟨3 / 5, 0⟩, ⟨-4 / 5, 0⟩, ⟨4 / 5, 0⟩, ⟨3 / 5, 0⟩⟩ := by
  ext <;> simp [pauliY, cayleyStep, linComb, cayleyAlpha, cayleyBeta, cayleyDenom, normSq] <;> norm_num

end TracelessHerm2Qi

end U1Finite.QuadraticTowerAndCayleyStone

#print axioms U1Finite.QuadraticTowerAndCayleyStone.QuadExt.instCommRing
#print axioms U1Finite.QuadraticTowerAndCayleyStone.QuadExt.radGen_sq
#print axioms U1Finite.QuadraticTowerAndCayleyStone.QuadExt.mul_conj_eq_norm
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_on_circle
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_double_re
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_double_im
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_w_inv
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_v_inv
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_half_inv
#print axioms U1Finite.QuadraticTowerAndCayleyStone.HalfAngleState.next_radical_components
#print axioms U1Finite.QuadraticTowerAndCayleyStone.towerState_on_circle
#print axioms U1Finite.QuadraticTowerAndCayleyStone.towerCirclePoint_sq_eq_prev
#print axioms U1Finite.QuadraticTowerAndCayleyStone.towerState_pow_two_pow_eq_u345
#print axioms U1Finite.QuadraticTowerAndCayleyStone.tower_level_one_explicit
#print axioms U1Finite.QuadraticTowerAndCayleyStone.tower_level_two_radicand_and_sine
#print axioms U1Finite.QuadraticTowerAndCayleyStone.Mat2Qi.ofHermitian_dagger
#print axioms U1Finite.QuadraticTowerAndCayleyStone.Mat2Qi.mul_assoc
#print axioms U1Finite.QuadraticTowerAndCayleyStone.Mat2Qi.tr_mul_comm
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyDenom_ge_one
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyDenom_ne_zero
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.linComb_mul
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.minusItH_dagger
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.plusItH_mul_minusItH
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_resolvent_right
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_resolvent_left
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_unitary_left
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_unitary_right
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_dagger_eq_neg
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_zero
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_det_eq_one
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comm
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_regular
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_pole
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_preserves_born_trace
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_pauliZ_half
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_pauliX_half
#print axioms U1Finite.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_pauliY_half
