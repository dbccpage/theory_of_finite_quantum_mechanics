/-!
Integer-pair clock and shift at dimension 6.
AuthorityEffect: None.
The module has no import.
-/

namespace CampaignMub6WeylHeisenbergD6

structure R where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def rAdd (x y : R) : R := ⟨x.re + y.re, x.im + y.im⟩
def rSub (x y : R) : R := ⟨x.re - y.re, x.im - y.im⟩
def rMul (x y : R) : R :=
  ⟨x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re + x.im * y.im⟩
def rConj (x : R) : R := ⟨x.re + x.im, -x.im⟩
def rZero : R := ⟨0, 0⟩
def rOne : R := ⟨1, 0⟩
def rNegOne : R := ⟨-1, 0⟩
def rSix : R := ⟨6, 0⟩
def w : R := ⟨0, 1⟩

def wpow : Nat → R
  | 0 => rOne
  | n + 1 => rMul w (wpow n)

theorem w_sq : rMul w w = rSub w rOne := by decide
theorem w_cube : wpow 3 = rNegOne := by decide
theorem w_six : wpow 6 = rOne := by decide
theorem conj_pair (a b : Int) : rConj ⟨a, b⟩ = ⟨a + b, -b⟩ := by rfl

@[ext]
structure Mat where

  e00 : R
  e01 : R
  e02 : R
  e03 : R
  e04 : R
  e05 : R
  e10 : R
  e11 : R
  e12 : R
  e13 : R
  e14 : R
  e15 : R
  e20 : R
  e21 : R
  e22 : R
  e23 : R
  e24 : R
  e25 : R
  e30 : R
  e31 : R
  e32 : R
  e33 : R
  e34 : R
  e35 : R
  e40 : R
  e41 : R
  e42 : R
  e43 : R
  e44 : R
  e45 : R
  e50 : R
  e51 : R
  e52 : R
  e53 : R
  e54 : R
  e55 : R
  deriving DecidableEq, Repr

def mAt (A : Mat) : Fin 6 → Fin 6 → R
  | 0, 0 => A.e00
  | 0, 1 => A.e01
  | 0, 2 => A.e02
  | 0, 3 => A.e03
  | 0, 4 => A.e04
  | 0, 5 => A.e05
  | 1, 0 => A.e10
  | 1, 1 => A.e11
  | 1, 2 => A.e12
  | 1, 3 => A.e13
  | 1, 4 => A.e14
  | 1, 5 => A.e15
  | 2, 0 => A.e20
  | 2, 1 => A.e21
  | 2, 2 => A.e22
  | 2, 3 => A.e23
  | 2, 4 => A.e24
  | 2, 5 => A.e25
  | 3, 0 => A.e30
  | 3, 1 => A.e31
  | 3, 2 => A.e32
  | 3, 3 => A.e33
  | 3, 4 => A.e34
  | 3, 5 => A.e35
  | 4, 0 => A.e40
  | 4, 1 => A.e41
  | 4, 2 => A.e42
  | 4, 3 => A.e43
  | 4, 4 => A.e44
  | 4, 5 => A.e45
  | 5, 0 => A.e50
  | 5, 1 => A.e51
  | 5, 2 => A.e52
  | 5, 3 => A.e53
  | 5, 4 => A.e54
  | 5, 5 => A.e55

def dot6 (f : Fin 6 → R) : R :=
  rAdd (f 0) (rAdd (f 1) (rAdd (f 2) (rAdd (f 3) (rAdd (f 4) (f 5)))))

def mAdj (A : Mat) : Mat where
  e00 := rConj (mAt A 0 0)
  e01 := rConj (mAt A 1 0)
  e02 := rConj (mAt A 2 0)
  e03 := rConj (mAt A 3 0)
  e04 := rConj (mAt A 4 0)
  e05 := rConj (mAt A 5 0)
  e10 := rConj (mAt A 0 1)
  e11 := rConj (mAt A 1 1)
  e12 := rConj (mAt A 2 1)
  e13 := rConj (mAt A 3 1)
  e14 := rConj (mAt A 4 1)
  e15 := rConj (mAt A 5 1)
  e20 := rConj (mAt A 0 2)
  e21 := rConj (mAt A 1 2)
  e22 := rConj (mAt A 2 2)
  e23 := rConj (mAt A 3 2)
  e24 := rConj (mAt A 4 2)
  e25 := rConj (mAt A 5 2)
  e30 := rConj (mAt A 0 3)
  e31 := rConj (mAt A 1 3)
  e32 := rConj (mAt A 2 3)
  e33 := rConj (mAt A 3 3)
  e34 := rConj (mAt A 4 3)
  e35 := rConj (mAt A 5 3)
  e40 := rConj (mAt A 0 4)
  e41 := rConj (mAt A 1 4)
  e42 := rConj (mAt A 2 4)
  e43 := rConj (mAt A 3 4)
  e44 := rConj (mAt A 4 4)
  e45 := rConj (mAt A 5 4)
  e50 := rConj (mAt A 0 5)
  e51 := rConj (mAt A 1 5)
  e52 := rConj (mAt A 2 5)
  e53 := rConj (mAt A 3 5)
  e54 := rConj (mAt A 4 5)
  e55 := rConj (mAt A 5 5)

def mMul (A B : Mat) : Mat where
  e00 := dot6 (fun k => rMul (mAt A 0 k) (mAt B k 0))
  e01 := dot6 (fun k => rMul (mAt A 0 k) (mAt B k 1))
  e02 := dot6 (fun k => rMul (mAt A 0 k) (mAt B k 2))
  e03 := dot6 (fun k => rMul (mAt A 0 k) (mAt B k 3))
  e04 := dot6 (fun k => rMul (mAt A 0 k) (mAt B k 4))
  e05 := dot6 (fun k => rMul (mAt A 0 k) (mAt B k 5))
  e10 := dot6 (fun k => rMul (mAt A 1 k) (mAt B k 0))
  e11 := dot6 (fun k => rMul (mAt A 1 k) (mAt B k 1))
  e12 := dot6 (fun k => rMul (mAt A 1 k) (mAt B k 2))
  e13 := dot6 (fun k => rMul (mAt A 1 k) (mAt B k 3))
  e14 := dot6 (fun k => rMul (mAt A 1 k) (mAt B k 4))
  e15 := dot6 (fun k => rMul (mAt A 1 k) (mAt B k 5))
  e20 := dot6 (fun k => rMul (mAt A 2 k) (mAt B k 0))
  e21 := dot6 (fun k => rMul (mAt A 2 k) (mAt B k 1))
  e22 := dot6 (fun k => rMul (mAt A 2 k) (mAt B k 2))
  e23 := dot6 (fun k => rMul (mAt A 2 k) (mAt B k 3))
  e24 := dot6 (fun k => rMul (mAt A 2 k) (mAt B k 4))
  e25 := dot6 (fun k => rMul (mAt A 2 k) (mAt B k 5))
  e30 := dot6 (fun k => rMul (mAt A 3 k) (mAt B k 0))
  e31 := dot6 (fun k => rMul (mAt A 3 k) (mAt B k 1))
  e32 := dot6 (fun k => rMul (mAt A 3 k) (mAt B k 2))
  e33 := dot6 (fun k => rMul (mAt A 3 k) (mAt B k 3))
  e34 := dot6 (fun k => rMul (mAt A 3 k) (mAt B k 4))
  e35 := dot6 (fun k => rMul (mAt A 3 k) (mAt B k 5))
  e40 := dot6 (fun k => rMul (mAt A 4 k) (mAt B k 0))
  e41 := dot6 (fun k => rMul (mAt A 4 k) (mAt B k 1))
  e42 := dot6 (fun k => rMul (mAt A 4 k) (mAt B k 2))
  e43 := dot6 (fun k => rMul (mAt A 4 k) (mAt B k 3))
  e44 := dot6 (fun k => rMul (mAt A 4 k) (mAt B k 4))
  e45 := dot6 (fun k => rMul (mAt A 4 k) (mAt B k 5))
  e50 := dot6 (fun k => rMul (mAt A 5 k) (mAt B k 0))
  e51 := dot6 (fun k => rMul (mAt A 5 k) (mAt B k 1))
  e52 := dot6 (fun k => rMul (mAt A 5 k) (mAt B k 2))
  e53 := dot6 (fun k => rMul (mAt A 5 k) (mAt B k 3))
  e54 := dot6 (fun k => rMul (mAt A 5 k) (mAt B k 4))
  e55 := dot6 (fun k => rMul (mAt A 5 k) (mAt B k 5))

def mScale (c : R) (A : Mat) : Mat where
  e00 := rMul c (mAt A 0 0)
  e01 := rMul c (mAt A 0 1)
  e02 := rMul c (mAt A 0 2)
  e03 := rMul c (mAt A 0 3)
  e04 := rMul c (mAt A 0 4)
  e05 := rMul c (mAt A 0 5)
  e10 := rMul c (mAt A 1 0)
  e11 := rMul c (mAt A 1 1)
  e12 := rMul c (mAt A 1 2)
  e13 := rMul c (mAt A 1 3)
  e14 := rMul c (mAt A 1 4)
  e15 := rMul c (mAt A 1 5)
  e20 := rMul c (mAt A 2 0)
  e21 := rMul c (mAt A 2 1)
  e22 := rMul c (mAt A 2 2)
  e23 := rMul c (mAt A 2 3)
  e24 := rMul c (mAt A 2 4)
  e25 := rMul c (mAt A 2 5)
  e30 := rMul c (mAt A 3 0)
  e31 := rMul c (mAt A 3 1)
  e32 := rMul c (mAt A 3 2)
  e33 := rMul c (mAt A 3 3)
  e34 := rMul c (mAt A 3 4)
  e35 := rMul c (mAt A 3 5)
  e40 := rMul c (mAt A 4 0)
  e41 := rMul c (mAt A 4 1)
  e42 := rMul c (mAt A 4 2)
  e43 := rMul c (mAt A 4 3)
  e44 := rMul c (mAt A 4 4)
  e45 := rMul c (mAt A 4 5)
  e50 := rMul c (mAt A 5 0)
  e51 := rMul c (mAt A 5 1)
  e52 := rMul c (mAt A 5 2)
  e53 := rMul c (mAt A 5 3)
  e54 := rMul c (mAt A 5 4)
  e55 := rMul c (mAt A 5 5)

def mTr (A : Mat) : R := dot6 (fun i => mAt A i i)

def mHs (A B : Mat) : R :=
  dot6 (fun i => dot6 (fun k => rMul (rConj (mAt A k i)) (mAt B k i)))

def eye : Mat where
  e00 := rOne
  e01 := rZero
  e02 := rZero
  e03 := rZero
  e04 := rZero
  e05 := rZero
  e10 := rZero
  e11 := rOne
  e12 := rZero
  e13 := rZero
  e14 := rZero
  e15 := rZero
  e20 := rZero
  e21 := rZero
  e22 := rOne
  e23 := rZero
  e24 := rZero
  e25 := rZero
  e30 := rZero
  e31 := rZero
  e32 := rZero
  e33 := rOne
  e34 := rZero
  e35 := rZero
  e40 := rZero
  e41 := rZero
  e42 := rZero
  e43 := rZero
  e44 := rOne
  e45 := rZero
  e50 := rZero
  e51 := rZero
  e52 := rZero
  e53 := rZero
  e54 := rZero
  e55 := rOne

def shiftX : Mat where
  e00 := rZero
  e01 := rZero
  e02 := rZero
  e03 := rZero
  e04 := rZero
  e05 := rOne
  e10 := rOne
  e11 := rZero
  e12 := rZero
  e13 := rZero
  e14 := rZero
  e15 := rZero
  e20 := rZero
  e21 := rOne
  e22 := rZero
  e23 := rZero
  e24 := rZero
  e25 := rZero
  e30 := rZero
  e31 := rZero
  e32 := rOne
  e33 := rZero
  e34 := rZero
  e35 := rZero
  e40 := rZero
  e41 := rZero
  e42 := rZero
  e43 := rOne
  e44 := rZero
  e45 := rZero
  e50 := rZero
  e51 := rZero
  e52 := rZero
  e53 := rZero
  e54 := rOne
  e55 := rZero

def clockZ : Mat where
  e00 := wpow 0
  e01 := rZero
  e02 := rZero
  e03 := rZero
  e04 := rZero
  e05 := rZero
  e10 := rZero
  e11 := wpow 1
  e12 := rZero
  e13 := rZero
  e14 := rZero
  e15 := rZero
  e20 := rZero
  e21 := rZero
  e22 := wpow 2
  e23 := rZero
  e24 := rZero
  e25 := rZero
  e30 := rZero
  e31 := rZero
  e32 := rZero
  e33 := wpow 3
  e34 := rZero
  e35 := rZero
  e40 := rZero
  e41 := rZero
  e42 := rZero
  e43 := rZero
  e44 := wpow 4
  e45 := rZero
  e50 := rZero
  e51 := rZero
  e52 := rZero
  e53 := rZero
  e54 := rZero
  e55 := wpow 5

def mPow (A : Mat) : Nat → Mat
  | 0 => eye
  | n + 1 => mMul A (mPow A n)

def dispEntry (p q i j : Nat) : R :=
  if i = (j + p) % 6 then wpow (q * j) else rZero

def op (p q : Fin 6) : Mat where
  e00 := dispEntry p.val q.val 0 0
  e01 := dispEntry p.val q.val 0 1
  e02 := dispEntry p.val q.val 0 2
  e03 := dispEntry p.val q.val 0 3
  e04 := dispEntry p.val q.val 0 4
  e05 := dispEntry p.val q.val 0 5
  e10 := dispEntry p.val q.val 1 0
  e11 := dispEntry p.val q.val 1 1
  e12 := dispEntry p.val q.val 1 2
  e13 := dispEntry p.val q.val 1 3
  e14 := dispEntry p.val q.val 1 4
  e15 := dispEntry p.val q.val 1 5
  e20 := dispEntry p.val q.val 2 0
  e21 := dispEntry p.val q.val 2 1
  e22 := dispEntry p.val q.val 2 2
  e23 := dispEntry p.val q.val 2 3
  e24 := dispEntry p.val q.val 2 4
  e25 := dispEntry p.val q.val 2 5
  e30 := dispEntry p.val q.val 3 0
  e31 := dispEntry p.val q.val 3 1
  e32 := dispEntry p.val q.val 3 2
  e33 := dispEntry p.val q.val 3 3
  e34 := dispEntry p.val q.val 3 4
  e35 := dispEntry p.val q.val 3 5
  e40 := dispEntry p.val q.val 4 0
  e41 := dispEntry p.val q.val 4 1
  e42 := dispEntry p.val q.val 4 2
  e43 := dispEntry p.val q.val 4 3
  e44 := dispEntry p.val q.val 4 4
  e45 := dispEntry p.val q.val 4 5
  e50 := dispEntry p.val q.val 5 0
  e51 := dispEntry p.val q.val 5 1
  e52 := dispEntry p.val q.val 5 2
  e53 := dispEntry p.val q.val 5 3
  e54 := dispEntry p.val q.val 5 4
  e55 := dispEntry p.val q.val 5 5

def raw (p q r s : Fin 6) : R :=
  dot6 (fun i => dot6 (fun k =>
    rMul (rConj (dispEntry p.val q.val k.val i.val))
         (dispEntry r.val s.val k.val i.val)))

theorem shift_entry :
    ∀ i j : Fin 6, mAt shiftX i j = if i.val = (j.val + 1) % 6 then rOne else rZero := by
  decide

theorem clock_entry :
    ∀ i j : Fin 6, mAt clockZ i j = if i = j then wpow i.val else rZero := by
  decide

theorem zx_eq : mMul clockZ shiftX = mScale w (mMul shiftX clockZ) := by
  decide

theorem xz_ne : mMul shiftX clockZ ≠ mScale w (mMul clockZ shiftX) := by
  decide

theorem mul_at (A B : Mat) (i j : Fin 6) :
    mAt (mMul A B) i j = dot6 (fun k => rMul (mAt A i k) (mAt B k j)) := by
  match i, j with
  | 0, 0 => rfl
  | 0, 1 => rfl
  | 0, 2 => rfl
  | 0, 3 => rfl
  | 0, 4 => rfl
  | 0, 5 => rfl
  | 1, 0 => rfl
  | 1, 1 => rfl
  | 1, 2 => rfl
  | 1, 3 => rfl
  | 1, 4 => rfl
  | 1, 5 => rfl
  | 2, 0 => rfl
  | 2, 1 => rfl
  | 2, 2 => rfl
  | 2, 3 => rfl
  | 2, 4 => rfl
  | 2, 5 => rfl
  | 3, 0 => rfl
  | 3, 1 => rfl
  | 3, 2 => rfl
  | 3, 3 => rfl
  | 3, 4 => rfl
  | 3, 5 => rfl
  | 4, 0 => rfl
  | 4, 1 => rfl
  | 4, 2 => rfl
  | 4, 3 => rfl
  | 4, 4 => rfl
  | 4, 5 => rfl
  | 5, 0 => rfl
  | 5, 1 => rfl
  | 5, 2 => rfl
  | 5, 3 => rfl
  | 5, 4 => rfl
  | 5, 5 => rfl

theorem adj_at (A : Mat) (i k : Fin 6) :
    mAt (mAdj A) i k = rConj (mAt A k i) := by
  match i, k with
  | 0, 0 => rfl
  | 0, 1 => rfl
  | 0, 2 => rfl
  | 0, 3 => rfl
  | 0, 4 => rfl
  | 0, 5 => rfl
  | 1, 0 => rfl
  | 1, 1 => rfl
  | 1, 2 => rfl
  | 1, 3 => rfl
  | 1, 4 => rfl
  | 1, 5 => rfl
  | 2, 0 => rfl
  | 2, 1 => rfl
  | 2, 2 => rfl
  | 2, 3 => rfl
  | 2, 4 => rfl
  | 2, 5 => rfl
  | 3, 0 => rfl
  | 3, 1 => rfl
  | 3, 2 => rfl
  | 3, 3 => rfl
  | 3, 4 => rfl
  | 3, 5 => rfl
  | 4, 0 => rfl
  | 4, 1 => rfl
  | 4, 2 => rfl
  | 4, 3 => rfl
  | 4, 4 => rfl
  | 4, 5 => rfl
  | 5, 0 => rfl
  | 5, 1 => rfl
  | 5, 2 => rfl
  | 5, 3 => rfl
  | 5, 4 => rfl
  | 5, 5 => rfl

theorem trace_eq_hs (A B : Mat) : mTr (mMul (mAdj A) B) = mHs A B := by
  unfold mTr mHs
  apply congrArg dot6
  funext i
  rw [mul_at (mAdj A) B i i]
  apply congrArg dot6
  funext k
  rw [adj_at A i k]

@[simp] theorem rAdd_zero_left (x : R) : rAdd rZero x = x := by
  rcases x with ⟨a, b⟩
  simp [rAdd, rZero]

@[simp] theorem rAdd_zero_right (x : R) : rAdd x rZero = x := by
  rcases x with ⟨a, b⟩
  simp [rAdd, rZero]

@[simp] theorem rMul_one_left (x : R) : rMul rOne x = x := by
  rcases x with ⟨a, b⟩
  simp [rMul, rOne]

@[simp] theorem rMul_zero_left (x : R) : rMul rZero x = rZero := by
  rcases x with ⟨a, b⟩
  simp [rMul, rZero]

@[simp] theorem rMul_zero_right (x : R) : rMul x rZero = rZero := by
  rcases x with ⟨a, b⟩
  simp [rMul, rZero]

theorem rConj_zero : rConj rZero = rZero := by
  simp [rConj, rZero]

theorem rMul_assoc (x y z : R) : rMul (rMul x y) z = rMul x (rMul y z) := by
  rcases x with ⟨a, b⟩
  rcases y with ⟨c, d⟩
  rcases z with ⟨e, f⟩
  simp [rMul]
  grind

theorem wpow_add (a b : Nat) : rMul (wpow a) (wpow b) = wpow (a + b) := by
  induction a with
  | zero => simp [wpow]
  | succ a ih =>
    rw [show wpow (a + 1) = rMul w (wpow a) from rfl]
    rw [rMul_assoc, ih]
    have hsum : a + 1 + b = a + b + 1 := by omega
    rw [hsum]
    rfl

theorem rMul_bits (c d : Prop) [Decidable c] [Decidable d] :
    rMul (if c then rOne else rZero) (if d then rOne else rZero) =
      if c ∧ d then rOne else rZero := by
  by_cases hc : c <;> by_cases hd : d <;>
    simp [hc, hd, rMul_one_left, rMul_zero_left, rMul_zero_right]

theorem dot6_zero : dot6 (fun _ : Fin 6 => rZero) = rZero := by
  unfold dot6
  simp

theorem dot6_pick (t : Fin 6) (v : R) (f : Fin 6 → R)
    (h : ∀ k : Fin 6, f k = if k = t then v else rZero) : dot6 f = v := by
  unfold dot6
  have h0 := h 0
  have h1 := h 1
  have h2 := h 2
  have h3 := h 3
  have h4 := h 4
  have h5 := h 5
  match t with
  | 0 => simp [h0, h1, h2, h3, h4, h5]
  | 1 => simp [h0, h1, h2, h3, h4, h5]
  | 2 => simp [h0, h1, h2, h3, h4, h5]
  | 3 => simp [h0, h1, h2, h3, h4, h5]
  | 4 => simp [h0, h1, h2, h3, h4, h5]
  | 5 => simp [h0, h1, h2, h3, h4, h5]

theorem eye_entry : ∀ i j : Fin 6, mAt eye i j = if i = j then rOne else rZero := by
  decide

def pred6 (i : Fin 6) : Fin 6 := ⟨(i.val + 5) % 6, Nat.mod_lt _ (by decide)⟩

theorem add_mod_right (a b : Nat) : (a + b) % 6 = (a + b % 6) % 6 := by
  have h1 := Nat.add_mod a b 6
  have h2 := Nat.add_mod a (b % 6) 6
  rw [Nat.mod_mod] at h2
  rw [h1, h2]

theorem shift_step_fin :
    ∀ i j k r : Fin 6,
      (i.val = (k.val + 1) % 6 ∧ k.val = (j.val + r.val) % 6) ↔
        (k = pred6 i ∧ i.val = (j.val + r.val + 1) % 6) := by
  decide

theorem shift_step_n (i j k : Fin 6) (n : Nat) :
    (i.val = (k.val + 1) % 6 ∧ k.val = (j.val + n) % 6) ↔
      (k = pred6 i ∧ i.val = (j.val + (n + 1)) % 6) := by
  let r : Fin 6 := ⟨n % 6, Nat.mod_lt _ (by decide)⟩
  have hcol : (j.val + n) % 6 = (j.val + r.val) % 6 := by
    simp [r]
  have hrow : (j.val + (n + 1)) % 6 = (j.val + r.val + 1) % 6 := by
    have h := add_mod_right (j.val + 1) n
    have happ : j.val + (n + 1) = j.val + 1 + n := by omega
    have happ2 : j.val + r.val + 1 = j.val + 1 + r.val := by omega
    rw [happ, h, happ2]
  rw [hcol, hrow]
  simpa [r] using shift_step_fin i j k r

theorem shift_pow_entry (n : Nat) (i j : Fin 6) :
    mAt (mPow shiftX n) i j =
      if i.val = (j.val + n) % 6 then rOne else rZero := by
  induction n generalizing i j with
  | zero =>
    rw [mPow, eye_entry]
    by_cases h : i = j
    · simp [h, Nat.mod_eq_of_lt j.isLt]
    · have hv : i.val ≠ j.val := fun hv => h (Fin.ext hv)
      simp [h, hv, Nat.mod_eq_of_lt j.isLt]
  | succ n ih =>
    rw [mPow, mul_at]
    have hfun : ∀ k : Fin 6,
        rMul (mAt shiftX i k) (mAt (mPow shiftX n) k j) =
          if k = pred6 i ∧ i.val = (j.val + (n + 1)) % 6 then rOne else rZero := by
      intro k
      rw [shift_entry i k, ih k j, rMul_bits]
      by_cases hL : i.val = (k.val + 1) % 6 ∧ k.val = (j.val + n) % 6
      · have hR : k = pred6 i ∧ i.val = (j.val + (n + 1)) % 6 :=
          (shift_step_n i j k n).mp hL
        rw [ite_eq_left hL, ite_eq_left hR]
      · have hR : ¬ (k = pred6 i ∧ i.val = (j.val + (n + 1)) % 6) :=
          fun h => hL ((shift_step_n i j k n).mpr h)
        rw [ite_eq_right hL, ite_eq_right hR]
    have hd :
        dot6 (fun k => rMul (mAt shiftX i k) (mAt (mPow shiftX n) k j)) =
          if i.val = (j.val + (n + 1)) % 6 then rOne else rZero := by
      by_cases hc : i.val = (j.val + (n + 1)) % 6
      · have hf : ∀ k : Fin 6,
            rMul (mAt shiftX i k) (mAt (mPow shiftX n) k j) =
              if k = pred6 i then rOne else rZero := by
          intro k
          rw [hfun k]
          simp [hc]
        rw [dot6_pick (pred6 i) rOne _ hf]
        simp [hc]
      · have hf : ∀ k : Fin 6,
            rMul (mAt shiftX i k) (mAt (mPow shiftX n) k j) = rZero := by
          intro k
          rw [hfun k]
          simp [hc]
        have hdot : dot6 (fun k => rMul (mAt shiftX i k) (mAt (mPow shiftX n) k j)) = rZero := by
          have : (fun k => rMul (mAt shiftX i k) (mAt (mPow shiftX n) k j)) =
              (fun _ : Fin 6 => rZero) := by
            funext k
            exact hf k
          rw [this, dot6_zero]
        simp [hdot, hc]
    exact hd

theorem clock_pow_entry (n : Nat) (i j : Fin 6) :
    mAt (mPow clockZ n) i j = if i = j then wpow (n * i.val) else rZero := by
  induction n generalizing i j with
  | zero =>
    rw [mPow, eye_entry]
    by_cases h : i = j
    · simp [h, wpow]
    · simp [h]
  | succ n ih =>
    rw [mPow, mul_at]
    have hfun : ∀ k : Fin 6,
        rMul (mAt clockZ i k) (mAt (mPow clockZ n) k j) =
          if k = i ∧ i = j then wpow ((n + 1) * i.val) else rZero := by
      intro k
      rw [clock_entry i k, ih k j]
      by_cases hk : i = k
      · subst hk
        rw [ite_eq_left (rfl : i = i)]
        by_cases hj : i = j
        · subst hj
          rw [ite_eq_left rfl, wpow_add, ite_eq_left (And.intro rfl rfl)]
          congr 1
          rw [Nat.succ_mul, Nat.add_comm]
        · have hn : ¬ (i = i ∧ i = j) := fun h => hj h.2
          rw [ite_eq_right hj, rMul_zero_right, ite_eq_right hn]
      · have hn : ¬ (k = i ∧ i = j) := fun h => hk h.1.symm
        rw [ite_eq_right hk, rMul_zero_left, ite_eq_right hn]
    have hd :
        dot6 (fun k => rMul (mAt clockZ i k) (mAt (mPow clockZ n) k j)) =
          if i = j then wpow ((n + 1) * i.val) else rZero := by
      by_cases hj : i = j
      · have hf : ∀ k : Fin 6,
            rMul (mAt clockZ i k) (mAt (mPow clockZ n) k j) =
              if k = i then wpow ((n + 1) * i.val) else rZero := by
          intro k
          rw [hfun k]
          simp [hj]
        rw [dot6_pick i (wpow ((n + 1) * i.val)) _ hf]
        simp [hj]
      · have hf : ∀ k : Fin 6,
            rMul (mAt clockZ i k) (mAt (mPow clockZ n) k j) = rZero := by
          intro k
          rw [hfun k]
          simp [hj]
        have : (fun k => rMul (mAt clockZ i k) (mAt (mPow clockZ n) k j)) =
            (fun _ : Fin 6 => rZero) := by
          funext k
          exact hf k
        rw [this, dot6_zero]
        simp [hj]
    exact hd

theorem pow_entry (p q : Nat) (i j : Fin 6) :
    mAt (mMul (mPow shiftX p) (mPow clockZ q)) i j = dispEntry p q i.val j.val := by
  rw [mul_at]
  have hfun : ∀ k : Fin 6,
      rMul (mAt (mPow shiftX p) i k) (mAt (mPow clockZ q) k j) =
        if k = j ∧ i.val = (j.val + p) % 6 then wpow (q * j.val) else rZero := by
    intro k
    rw [shift_pow_entry p i k, clock_pow_entry q k j]
    by_cases hk : k = j
    · rw [ite_eq_left hk]
      by_cases hi : i.val = (k.val + p) % 6
      · have hi' : i.val = (j.val + p) % 6 := by simpa [hk] using hi
        rw [ite_eq_left hi, rMul_one_left, ite_eq_left (And.intro hk hi')]
        simp [hk]
      · have hi' : ¬ i.val = (j.val + p) % 6 := by simpa [hk] using hi
        have hn : ¬ (k = j ∧ i.val = (j.val + p) % 6) := fun h => hi' h.2
        rw [ite_eq_right hi, rMul_zero_left, ite_eq_right hn]
    · have hn : ¬ (k = j ∧ i.val = (j.val + p) % 6) := fun h => hk h.1
      rw [ite_eq_right hk, rMul_zero_right, ite_eq_right hn]
  let v : R := if i.val = (j.val + p) % 6 then wpow (q * j.val) else rZero
  have hf : ∀ k : Fin 6,
      rMul (mAt (mPow shiftX p) i k) (mAt (mPow clockZ q) k j) =
        if k = j then v else rZero := by
    intro k
    rw [hfun k]
    by_cases hk : k = j
    · simp [hk, v]
    · simp [hk, v]
  have hd := dot6_pick j v (fun k => rMul (mAt (mPow shiftX p) i k) (mAt (mPow clockZ q) k j)) hf
  simpa [dispEntry, v] using hd

def slot (i : Fin 6) (p : Nat) : Fin 6 := ⟨(i.val + p) % 6, Nat.mod_lt _ (by decide)⟩

theorem slot_eq_iff : ∀ i p r : Fin 6, slot i p.val = slot i r.val ↔ p = r := by
  decide

theorem term_off (p q r s i k : Fin 6) (hp : p ≠ r) :
    rMul (rConj (dispEntry p.val q.val k.val i.val))
        (dispEntry r.val s.val k.val i.val) = rZero := by
  unfold dispEntry
  by_cases h1 : k.val = (i.val + p.val) % 6
  · by_cases h2 : k.val = (i.val + r.val) % 6
    · have hs : slot i p.val = slot i r.val := by
        apply Fin.ext
        simp only [slot]
        rw [← h1, h2]
      exact absurd ((slot_eq_iff i p r).mp hs) hp
    · rw [ite_eq_right h2]
      simp [rMul_zero_right]
  · rw [ite_eq_right h1]
    simp [rConj_zero]

theorem term_on (p q s i k : Fin 6) :
    rMul (rConj (dispEntry p.val q.val k.val i.val))
        (dispEntry p.val s.val k.val i.val) =
      if k = slot i p.val then
        rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val))
      else rZero := by
  unfold dispEntry
  by_cases hk : k.val = (i.val + p.val) % 6
  · have he : k = slot i p.val := by
      apply Fin.ext
      simpa [slot] using hk
    simp [slot, he]
  · have he : k ≠ slot i p.val := by
      intro h
      apply hk
      have hv := congrArg Fin.val h
      simpa [slot] using hv
    simp [hk, he, rConj_zero]

theorem inner_at (p q r s i : Fin 6) :
    dot6 (fun k => rMul (rConj (dispEntry p.val q.val k.val i.val))
        (dispEntry r.val s.val k.val i.val)) =
      if p = r then rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val)) else rZero := by
  by_cases hp : p = r
  · subst hp
    have hf : ∀ k : Fin 6,
        rMul (rConj (dispEntry p.val q.val k.val i.val))
            (dispEntry p.val s.val k.val i.val) =
          if k = slot i p.val then
            rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val))
          else rZero := by
      intro k
      exact term_on p q s i k
    simpa using
      dot6_pick (slot i p.val)
        (rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val))) _ hf
  · have hf : ∀ k : Fin 6,
        rMul (rConj (dispEntry p.val q.val k.val i.val))
            (dispEntry r.val s.val k.val i.val) = rZero :=
      fun k => term_off p q r s i k hp
    have : (fun k => rMul (rConj (dispEntry p.val q.val k.val i.val))
        (dispEntry r.val s.val k.val i.val)) = fun _ : Fin 6 => rZero := by
      funext k
      exact hf k
    rw [this, dot6_zero]
    simp [hp]

theorem sum_phase_diag : ∀ q : Fin 6,
    dot6 (fun i => rMul (rConj (wpow (q.val * i.val))) (wpow (q.val * i.val))) = rSix := by
  decide

theorem sum_phase_off : ∀ q s : Fin 6, q ≠ s →
    dot6 (fun i => rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val))) = rZero := by
  decide

theorem mHs_raw (p q r s : Fin 6) : mHs (op p q) (op r s) = raw p q r s := by
  rfl

theorem raw_eval (p q r s : Fin 6) :
    raw p q r s = if p = r ∧ q = s then rSix else rZero := by
  unfold raw
  have hstep :
      dot6 (fun i => dot6 (fun k =>
        rMul (rConj (dispEntry p.val q.val k.val i.val))
            (dispEntry r.val s.val k.val i.val))) =
        dot6 (fun i => if p = r then
          rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val)) else rZero) := by
    apply congrArg dot6
    funext i
    exact inner_at p q r s i
  rw [hstep]
  by_cases hp : p = r
  · by_cases hq : q = s
    · have hfun :
          (fun i : Fin 6 => if p = r then
            rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val)) else rZero) =
            fun i : Fin 6 =>
              rMul (rConj (wpow (s.val * i.val))) (wpow (s.val * i.val)) := by
        funext i
        simp [hp, hq]
      rw [hfun]
      simpa [hp, hq] using sum_phase_diag s
    · simp only [hp, hq]
      exact sum_phase_off q s hq
  · have : (fun i : Fin 6 => if p = r then
        rMul (rConj (wpow (q.val * i.val))) (wpow (s.val * i.val)) else rZero) =
        fun _ : Fin 6 => rZero := by
      funext i
      simp [hp]
    rw [this, dot6_zero]
    simp [hp]

theorem trace_raw (p q r s : Fin 6) :
    mHs (mMul (mPow shiftX p.val) (mPow clockZ q.val))
        (mMul (mPow shiftX r.val) (mPow clockZ s.val)) = raw p q r s := by
  unfold mHs raw
  apply congrArg dot6
  funext i
  apply congrArg dot6
  funext k
  rw [pow_entry p.val q.val k i, pow_entry r.val s.val k i]

theorem hs_orth (p q r s : Fin 6) :
    mTr (mMul (mAdj (mMul (mPow shiftX p.val) (mPow clockZ q.val)))
             (mMul (mPow shiftX r.val) (mPow clockZ s.val)))
      = if p = r ∧ q = s then rSix else rZero := by
  rw [trace_eq_hs, trace_raw p q r s, raw_eval p q r s]

#print axioms w_sq
#print axioms w_cube
#print axioms w_six
#print axioms conj_pair
#print axioms shift_entry
#print axioms clock_entry
#print axioms zx_eq
#print axioms xz_ne
#print axioms hs_orth

end CampaignMub6WeylHeisenbergD6
