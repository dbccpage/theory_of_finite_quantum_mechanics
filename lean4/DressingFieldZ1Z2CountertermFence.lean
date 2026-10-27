set_option maxHeartbeats 2000000

namespace DressingFieldZ1Z2CountertermFence

structure G where
  re : Int
  im : Int
  den : Int

structure M where
  a00 : G
  a01 : G
  a02 : G
  a03 : G
  a10 : G
  a11 : G
  a12 : G
  a13 : G
  a20 : G
  a21 : G
  a22 : G
  a23 : G
  a30 : G
  a31 : G
  a32 : G
  a33 : G

def gadd (a b : G) : G where
  re := a.re * b.den + b.re * a.den
  im := a.im * b.den + b.im * a.den
  den := a.den * b.den

def gsub (a b : G) : G where
  re := a.re * b.den - b.re * a.den
  im := a.im * b.den - b.im * a.den
  den := a.den * b.den

def gmul (a b : G) : G where
  re := a.re * b.re - a.im * b.im
  im := a.re * b.im + a.im * b.re
  den := a.den * b.den

def gsum4 (a b c d : G) : G where
  re := a.re + b.re + c.re + d.re
  im := a.im + b.im + c.im + d.im
  den := a.den

def gscale (k : Int) (a : G) : G where
  re := a.re * k
  im := a.im * k
  den := a.den

def gdiv (a : G) (k : Int) : G where
  re := a.re
  im := a.im
  den := a.den * k

def z : G := { re := 0, im := 0, den := 1 }
def r (n : Int) : G := { re := n, im := 0, den := 1 }
def j (n : Int) : G := { re := 0, im := n, den := 1 }

def madd (A B : M) : M where
  a00 := gadd A.a00 B.a00
  a01 := gadd A.a01 B.a01
  a02 := gadd A.a02 B.a02
  a03 := gadd A.a03 B.a03
  a10 := gadd A.a10 B.a10
  a11 := gadd A.a11 B.a11
  a12 := gadd A.a12 B.a12
  a13 := gadd A.a13 B.a13
  a20 := gadd A.a20 B.a20
  a21 := gadd A.a21 B.a21
  a22 := gadd A.a22 B.a22
  a23 := gadd A.a23 B.a23
  a30 := gadd A.a30 B.a30
  a31 := gadd A.a31 B.a31
  a32 := gadd A.a32 B.a32
  a33 := gadd A.a33 B.a33

def msub (A B : M) : M where
  a00 := gsub A.a00 B.a00
  a01 := gsub A.a01 B.a01
  a02 := gsub A.a02 B.a02
  a03 := gsub A.a03 B.a03
  a10 := gsub A.a10 B.a10
  a11 := gsub A.a11 B.a11
  a12 := gsub A.a12 B.a12
  a13 := gsub A.a13 B.a13
  a20 := gsub A.a20 B.a20
  a21 := gsub A.a21 B.a21
  a22 := gsub A.a22 B.a22
  a23 := gsub A.a23 B.a23
  a30 := gsub A.a30 B.a30
  a31 := gsub A.a31 B.a31
  a32 := gsub A.a32 B.a32
  a33 := gsub A.a33 B.a33

def mscale (k : Int) (A : M) : M where
  a00 := gscale k A.a00
  a01 := gscale k A.a01
  a02 := gscale k A.a02
  a03 := gscale k A.a03
  a10 := gscale k A.a10
  a11 := gscale k A.a11
  a12 := gscale k A.a12
  a13 := gscale k A.a13
  a20 := gscale k A.a20
  a21 := gscale k A.a21
  a22 := gscale k A.a22
  a23 := gscale k A.a23
  a30 := gscale k A.a30
  a31 := gscale k A.a31
  a32 := gscale k A.a32
  a33 := gscale k A.a33

def mdiv (A : M) (k : Int) : M where
  a00 := gdiv A.a00 k
  a01 := gdiv A.a01 k
  a02 := gdiv A.a02 k
  a03 := gdiv A.a03 k
  a10 := gdiv A.a10 k
  a11 := gdiv A.a11 k
  a12 := gdiv A.a12 k
  a13 := gdiv A.a13 k
  a20 := gdiv A.a20 k
  a21 := gdiv A.a21 k
  a22 := gdiv A.a22 k
  a23 := gdiv A.a23 k
  a30 := gdiv A.a30 k
  a31 := gdiv A.a31 k
  a32 := gdiv A.a32 k
  a33 := gdiv A.a33 k

def mmul (A B : M) : M where
  a00 := gsum4 (gmul A.a00 B.a00) (gmul A.a01 B.a10) (gmul A.a02 B.a20) (gmul A.a03 B.a30)
  a01 := gsum4 (gmul A.a00 B.a01) (gmul A.a01 B.a11) (gmul A.a02 B.a21) (gmul A.a03 B.a31)
  a02 := gsum4 (gmul A.a00 B.a02) (gmul A.a01 B.a12) (gmul A.a02 B.a22) (gmul A.a03 B.a32)
  a03 := gsum4 (gmul A.a00 B.a03) (gmul A.a01 B.a13) (gmul A.a02 B.a23) (gmul A.a03 B.a33)
  a10 := gsum4 (gmul A.a10 B.a00) (gmul A.a11 B.a10) (gmul A.a12 B.a20) (gmul A.a13 B.a30)
  a11 := gsum4 (gmul A.a10 B.a01) (gmul A.a11 B.a11) (gmul A.a12 B.a21) (gmul A.a13 B.a31)
  a12 := gsum4 (gmul A.a10 B.a02) (gmul A.a11 B.a12) (gmul A.a12 B.a22) (gmul A.a13 B.a32)
  a13 := gsum4 (gmul A.a10 B.a03) (gmul A.a11 B.a13) (gmul A.a12 B.a23) (gmul A.a13 B.a33)
  a20 := gsum4 (gmul A.a20 B.a00) (gmul A.a21 B.a10) (gmul A.a22 B.a20) (gmul A.a23 B.a30)
  a21 := gsum4 (gmul A.a20 B.a01) (gmul A.a21 B.a11) (gmul A.a22 B.a21) (gmul A.a23 B.a31)
  a22 := gsum4 (gmul A.a20 B.a02) (gmul A.a21 B.a12) (gmul A.a22 B.a22) (gmul A.a23 B.a32)
  a23 := gsum4 (gmul A.a20 B.a03) (gmul A.a21 B.a13) (gmul A.a22 B.a23) (gmul A.a23 B.a33)
  a30 := gsum4 (gmul A.a30 B.a00) (gmul A.a31 B.a10) (gmul A.a32 B.a20) (gmul A.a33 B.a30)
  a31 := gsum4 (gmul A.a30 B.a01) (gmul A.a31 B.a11) (gmul A.a32 B.a21) (gmul A.a33 B.a31)
  a32 := gsum4 (gmul A.a30 B.a02) (gmul A.a31 B.a12) (gmul A.a32 B.a22) (gmul A.a33 B.a32)
  a33 := gsum4 (gmul A.a30 B.a03) (gmul A.a31 B.a13) (gmul A.a32 B.a23) (gmul A.a33 B.a33)

def eye : M where
  a00 := r 1
  a01 := z
  a02 := z
  a03 := z
  a10 := z
  a11 := r 1
  a12 := z
  a13 := z
  a20 := z
  a21 := z
  a22 := r 1
  a23 := z
  a30 := z
  a31 := z
  a32 := z
  a33 := r 1

def g0 : M where
  a00 := r 1
  a01 := z
  a02 := z
  a03 := z
  a10 := z
  a11 := r 1
  a12 := z
  a13 := z
  a20 := z
  a21 := z
  a22 := r (-1)
  a23 := z
  a30 := z
  a31 := z
  a32 := z
  a33 := r (-1)

def g1 : M where
  a00 := z
  a01 := z
  a02 := z
  a03 := r 1
  a10 := z
  a11 := z
  a12 := r 1
  a13 := z
  a20 := z
  a21 := r (-1)
  a22 := z
  a23 := z
  a30 := r (-1)
  a31 := z
  a32 := z
  a33 := z

def g2 : M where
  a00 := z
  a01 := z
  a02 := z
  a03 := j (-1)
  a10 := z
  a11 := z
  a12 := j 1
  a13 := z
  a20 := z
  a21 := j 1
  a22 := z
  a23 := z
  a30 := j (-1)
  a31 := z
  a32 := z
  a33 := z

def g3 : M where
  a00 := z
  a01 := z
  a02 := r 1
  a03 := z
  a10 := z
  a11 := z
  a12 := z
  a13 := r (-1)
  a20 := r (-1)
  a21 := z
  a22 := z
  a23 := z
  a30 := z
  a31 := r 1
  a32 := z
  a33 := z

def slash (p0 p1 p2 p3 : Int) : M :=
  msub (msub (msub (mscale p0 g0) (mscale p1 g1)) (mscale p2 g2)) (mscale p3 g3)

def propInv (p0 p1 p2 p3 mass : Int) : M :=
  msub (slash p0 p1 p2 p3) (mscale mass eye)

def sP : M where
  a00 := { re := 3, im := 0, den := 3 }
  a01 := { re := 0, im := 0, den := 3 }
  a02 := { re := 0, im := 0, den := 3 }
  a03 := { re := 0, im := 0, den := 3 }
  a10 := { re := 0, im := 0, den := 3 }
  a11 := { re := 3, im := 0, den := 3 }
  a12 := { re := 0, im := 0, den := 3 }
  a13 := { re := 0, im := 0, den := 3 }
  a20 := { re := 0, im := 0, den := 3 }
  a21 := { re := 0, im := 0, den := 3 }
  a22 := { re := -1, im := 0, den := 3 }
  a23 := { re := 0, im := 0, den := 3 }
  a30 := { re := 0, im := 0, den := 3 }
  a31 := { re := 0, im := 0, den := 3 }
  a32 := { re := 0, im := 0, den := 3 }
  a33 := { re := -1, im := 0, den := 3 }

def sPQ : M where
  a00 := { re := 4, im := 0, den := 7 }
  a01 := { re := 0, im := 0, den := 7 }
  a02 := { re := -1, im := 0, den := 7 }
  a03 := { re := 0, im := 0, den := 7 }
  a10 := { re := 0, im := 0, den := 7 }
  a11 := { re := 4, im := 0, den := 7 }
  a12 := { re := 0, im := 0, den := 7 }
  a13 := { re := 1, im := 0, den := 7 }
  a20 := { re := 1, im := 0, den := 7 }
  a21 := { re := 0, im := 0, den := 7 }
  a22 := { re := -2, im := 0, den := 7 }
  a23 := { re := 0, im := 0, den := 7 }
  a30 := { re := 0, im := 0, den := 7 }
  a31 := { re := -1, im := 0, den := 7 }
  a32 := { re := 0, im := 0, den := 7 }
  a33 := { re := -2, im := 0, den := 7 }

def qSlash : M where
  a00 := { re := 1, im := 0, den := 1 }
  a01 := { re := 0, im := 0, den := 1 }
  a02 := { re := -1, im := 0, den := 1 }
  a03 := { re := 0, im := 0, den := 1 }
  a10 := { re := 0, im := 0, den := 1 }
  a11 := { re := 1, im := 0, den := 1 }
  a12 := { re := 0, im := 0, den := 1 }
  a13 := { re := 1, im := 0, den := 1 }
  a20 := { re := 1, im := 0, den := 1 }
  a21 := { re := 0, im := 0, den := 1 }
  a22 := { re := -1, im := 0, den := 1 }
  a23 := { re := 0, im := 0, den := 1 }
  a30 := { re := 0, im := 0, den := 1 }
  a31 := { re := -1, im := 0, den := 1 }
  a32 := { re := 0, im := 0, den := 1 }
  a33 := { re := -1, im := 0, den := 1 }

def witness : M where
  a00 := { re := 2, im := 0, den := 7 }
  a01 := { re := 0, im := 0, den := 1 }
  a02 := { re := -2, im := 0, den := 7 }
  a03 := { re := 0, im := 0, den := 1 }
  a10 := { re := 0, im := 0, den := 1 }
  a11 := { re := 2, im := 0, den := 7 }
  a12 := { re := 0, im := 0, den := 1 }
  a13 := { re := 2, im := 0, den := 7 }
  a20 := { re := 2, im := 0, den := 7 }
  a21 := { re := 0, im := 0, den := 1 }
  a22 := { re := 26, im := 0, den := 21 }
  a23 := { re := 0, im := 0, den := 1 }
  a30 := { re := 0, im := 0, den := 1 }
  a31 := { re := -2, im := 0, den := 7 }
  a32 := { re := 0, im := 0, den := 1 }
  a33 := { re := 26, im := 0, den := 21 }

def conjGamma (g : M) (eta : Int) (A : M) : M :=
  mmul g (mmul A (mscale eta g))

def dirac (A : M) : M :=
  let c0 := conjGamma g0 1 A
  let c1 := conjGamma g1 (-1) A
  let c2 := conjGamma g2 (-1) A
  let c3 := conjGamma g3 (-1) A
  { a00 := gsum4 c0.a00 c1.a00 c2.a00 c3.a00
    a01 := gsum4 c0.a01 c1.a01 c2.a01 c3.a01
    a02 := gsum4 c0.a02 c1.a02 c2.a02 c3.a02
    a03 := gsum4 c0.a03 c1.a03 c2.a03 c3.a03
    a10 := gsum4 c0.a10 c1.a10 c2.a10 c3.a10
    a11 := gsum4 c0.a11 c1.a11 c2.a11 c3.a11
    a12 := gsum4 c0.a12 c1.a12 c2.a12 c3.a12
    a13 := gsum4 c0.a13 c1.a13 c2.a13 c3.a13
    a20 := gsum4 c0.a20 c1.a20 c2.a20 c3.a20
    a21 := gsum4 c0.a21 c1.a21 c2.a21 c3.a21
    a22 := gsum4 c0.a22 c1.a22 c2.a22 c3.a22
    a23 := gsum4 c0.a23 c1.a23 c2.a23 c3.a23
    a30 := gsum4 c0.a30 c1.a30 c2.a30 c3.a30
    a31 := gsum4 c0.a31 c1.a31 c2.a31 c3.a31
    a32 := gsum4 c0.a32 c1.a32 c2.a32 c3.a32
    a33 := gsum4 c0.a33 c1.a33 c2.a33 c3.a33
  }

def embed (mu : M) : M :=
  let t0 := mmul g0 (mmul sPQ (mmul mu (mmul sP (mscale 1 g0))))
  let t1 := mmul g1 (mmul sPQ (mmul mu (mmul sP (mscale (-1) g1))))
  let t2 := mmul g2 (mmul sPQ (mmul mu (mmul sP (mscale (-1) g2))))
  let t3 := mmul g3 (mmul sPQ (mmul mu (mmul sP (mscale (-1) g3))))
  { a00 := gsum4 t0.a00 t1.a00 t2.a00 t3.a00
    a01 := gsum4 t0.a01 t1.a01 t2.a01 t3.a01
    a02 := gsum4 t0.a02 t1.a02 t2.a02 t3.a02
    a03 := gsum4 t0.a03 t1.a03 t2.a03 t3.a03
    a10 := gsum4 t0.a10 t1.a10 t2.a10 t3.a10
    a11 := gsum4 t0.a11 t1.a11 t2.a11 t3.a11
    a12 := gsum4 t0.a12 t1.a12 t2.a12 t3.a12
    a13 := gsum4 t0.a13 t1.a13 t2.a13 t3.a13
    a20 := gsum4 t0.a20 t1.a20 t2.a20 t3.a20
    a21 := gsum4 t0.a21 t1.a21 t2.a21 t3.a21
    a22 := gsum4 t0.a22 t1.a22 t2.a22 t3.a22
    a23 := gsum4 t0.a23 t1.a23 t2.a23 t3.a23
    a30 := gsum4 t0.a30 t1.a30 t2.a30 t3.a30
    a31 := gsum4 t0.a31 t1.a31 t2.a31 t3.a31
    a32 := gsum4 t0.a32 t1.a32 t2.a32 t3.a32
    a33 := gsum4 t0.a33 t1.a33 t2.a33 t3.a33
  }

def qContract : M :=
  let left := embed g0
  let right := mscale (-1) (embed g3)
  { a00 := gsum4 left.a00 right.a00 z z
    a01 := gsum4 left.a01 right.a01 z z
    a02 := gsum4 left.a02 right.a02 z z
    a03 := gsum4 left.a03 right.a03 z z
    a10 := gsum4 left.a10 right.a10 z z
    a11 := gsum4 left.a11 right.a11 z z
    a12 := gsum4 left.a12 right.a12 z z
    a13 := gsum4 left.a13 right.a13 z z
    a20 := gsum4 left.a20 right.a20 z z
    a21 := gsum4 left.a21 right.a21 z z
    a22 := gsum4 left.a22 right.a22 z z
    a23 := gsum4 left.a23 right.a23 z z
    a30 := gsum4 left.a30 right.a30 z z
    a31 := gsum4 left.a31 right.a31 z z
    a32 := gsum4 left.a32 right.a32 z z
    a33 := gsum4 left.a33 right.a33 z z
  }

def sigmaDiff : M := msub (dirac sP) (dirac sPQ)

abbrev eqG (a b : G) : Prop :=
  a.re * b.den = b.re * a.den ∧ a.im * b.den = b.im * a.den ∧ a.den ≠ 0 ∧ b.den ≠ 0

abbrev eqM (A B : M) : Prop :=
  eqG A.a00 B.a00 ∧ eqG A.a01 B.a01 ∧ eqG A.a02 B.a02 ∧ eqG A.a03 B.a03 ∧ eqG A.a10 B.a10 ∧ eqG A.a11 B.a11 ∧ eqG A.a12 B.a12 ∧ eqG A.a13 B.a13 ∧ eqG A.a20 B.a20 ∧ eqG A.a21 B.a21 ∧ eqG A.a22 B.a22 ∧ eqG A.a23 B.a23 ∧ eqG A.a30 B.a30 ∧ eqG A.a31 B.a31 ∧ eqG A.a32 B.a32 ∧ eqG A.a33 B.a33

theorem inverse_difference (p0 p1 p2 p3 q0 q1 q2 q3 mass : Int) :
    eqM (msub (propInv (p0 + q0) (p1 + q1) (p2 + q2) (p3 + q3) mass) (propInv p0 p1 p2 p3 mass))
      (slash q0 q1 q2 q3) := by
  simp only [eqM, eqG, msub, propInv, slash, mscale, gsub, gscale, eye, g0, g1, g2, g3, z, r, j]
  omega

theorem propagator_values :
    eqM sP (mdiv (madd (slash 2 0 0 0) (mscale 1 eye)) 3) ∧
    eqM sPQ (mdiv (madd (slash 3 0 0 1) (mscale 1 eye)) 7) ∧
    eqM qSlash (slash 1 0 0 1) := by
  repeat (any_goals constructor)
  all_goals simp only [sP, sPQ, qSlash, mdiv, madd, slash, mscale, msub, gadd, gsub, gdiv, gscale, eye, g0, g1, g2, g3, z, r, j]
  repeat (any_goals constructor)
  all_goals decide

theorem sandwich : eqM (mmul sPQ (mmul qSlash sP)) (msub sP sPQ) := by
  simp only [eqM, eqG, sP, sPQ, qSlash, mmul, msub, gsum4, gmul, gsub]
  repeat (any_goals constructor)
  all_goals decide

theorem contraction : eqM qContract sigmaDiff := by
  simp only [eqM, eqG, qContract, sigmaDiff, embed, dirac, conjGamma, sP, sPQ, mmul, msub, mscale, gsum4, gmul, gsub, gscale, g0, g1, g2, g3, z]
  repeat (any_goals constructor)
  all_goals decide

theorem contraction_entries : eqM qContract witness := by
  simp only [eqM, eqG, qContract, witness, embed, sP, sPQ, mmul, mscale, gsum4, gmul, gscale, g0, g1, g2, g3, z]
  repeat (any_goals constructor)
  all_goals decide

#print axioms DressingFieldZ1Z2CountertermFence.inverse_difference
#print axioms DressingFieldZ1Z2CountertermFence.propagator_values
#print axioms DressingFieldZ1Z2CountertermFence.sandwich
#print axioms DressingFieldZ1Z2CountertermFence.contraction
#print axioms DressingFieldZ1Z2CountertermFence.contraction_entries

end DressingFieldZ1Z2CountertermFence
