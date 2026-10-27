






import HWKernel

namespace HilbertWalk.Rationals

open HilbertWalk.HWKernel


structure PreQ where
  num : Int
  den : Int
  den_pos : 0 < den

theorem PreQ.ext {x y : PreQ} (hn : x.num = y.num) (hd : x.den = y.den) :
    x = y := by
  cases x
  cases y
  cases hn
  cases hd
  rfl

theorem one_pos : (0 : Int) < 1 := by decide
theorem two_pos : (0 : Int) < 2 := by decide

def qrel (x y : PreQ) : Prop :=
  x.num * y.den = y.num * x.den

theorem qrel_refl (x : PreQ) : qrel x x := rfl

theorem qrel_symm {x y : PreQ} (h : qrel x y) : qrel y x :=
  h.symm

theorem qrel_trans {x y z : PreQ} (hxy : qrel x y) (hyz : qrel y z) :
    qrel x z := by
  unfold qrel at *
  have hyd : y.den ≠ 0 := Int.ne_of_gt y.den_pos
  apply Int.eq_of_mul_eq_mul_right hyd
  calc x.num * z.den * y.den
      = x.num * y.den * z.den := by ac_rfl
    _ = y.num * x.den * z.den := by rw [hxy]
    _ = y.num * z.den * x.den := by ac_rfl
    _ = z.num * y.den * x.den := by rw [hyz]
    _ = z.num * x.den * y.den := by ac_rfl

theorem qrel_equivalence : Equivalence qrel :=
  ⟨qrel_refl, qrel_symm, qrel_trans⟩

instance preQSetoid : Setoid PreQ where
  r := qrel
  iseqv := qrel_equivalence

def Frac : Type := Quotient preQSetoid

def mkQ (x : PreQ) : Frac := Quotient.mk preQSetoid x

theorem frac_ind {motive : Frac → Prop}
    (h : ∀ a : PreQ, motive (mkQ a)) (x : Frac) : motive x :=
  Quotient.ind h x

def ofInt (n : Int) : Frac := mkQ ⟨n, 1, one_pos⟩

def fzero : Frac := ofInt 0
def fone : Frac := ofInt 1
def half : Frac := mkQ ⟨1, 2, two_pos⟩


def padd (x y : PreQ) : PreQ :=
  ⟨x.num * y.den + y.num * x.den, x.den * y.den,
    Int.mul_pos x.den_pos y.den_pos⟩

def pmul (x y : PreQ) : PreQ :=
  ⟨x.num * y.num, x.den * y.den, Int.mul_pos x.den_pos y.den_pos⟩

def pneg (x : PreQ) : PreQ :=
  ⟨-x.num, x.den, x.den_pos⟩

def pzero : PreQ := ⟨0, 1, one_pos⟩
def pone : PreQ := ⟨1, 1, one_pos⟩
def phalf : PreQ := ⟨1, 2, two_pos⟩

theorem padd_congr {a a' b b' : PreQ}
    (ha : qrel a a') (hb : qrel b b') : qrel (padd a b) (padd a' b') := by
  unfold qrel padd
  rw [Int.add_mul, Int.add_mul]
  have h1 :
      a.num * b.den * (a'.den * b'.den) =
        a'.num * b'.den * (a.den * b.den) := by
    calc a.num * b.den * (a'.den * b'.den)
        = a.num * a'.den * (b.den * b'.den) := by ac_rfl
      _ = a'.num * a.den * (b.den * b'.den) := by rw [ha]
      _ = a'.num * b'.den * (a.den * b.den) := by ac_rfl
  have h2 :
      b.num * a.den * (a'.den * b'.den) =
        b'.num * a'.den * (a.den * b.den) := by
    calc b.num * a.den * (a'.den * b'.den)
        = b.num * b'.den * (a.den * a'.den) := by ac_rfl
      _ = b'.num * b.den * (a.den * a'.den) := by rw [hb]
      _ = b'.num * a'.den * (a.den * b.den) := by ac_rfl
  rw [h1, h2]

theorem pmul_congr {a a' b b' : PreQ}
    (ha : qrel a a') (hb : qrel b b') : qrel (pmul a b) (pmul a' b') := by
  unfold qrel pmul
  calc a.num * b.num * (a'.den * b'.den)
      = a.num * a'.den * (b.num * b'.den) := by ac_rfl
    _ = a'.num * a.den * (b.num * b'.den) := by rw [ha]
    _ = a'.num * a.den * (b'.num * b.den) := by rw [hb]
    _ = a'.num * b'.num * (a.den * b.den) := by ac_rfl

theorem pneg_congr {a a' : PreQ} (ha : qrel a a') : qrel (pneg a) (pneg a') := by
  unfold qrel pneg
  rw [Int.neg_mul, Int.neg_mul, ha]

theorem padd_comm (a b : PreQ) : padd a b = padd b a := by
  apply PreQ.ext
  · simp only [padd]
    exact Int.add_comm _ _
  · simp only [padd]
    exact Int.mul_comm _ _

theorem padd_assoc (a b c : PreQ) :
    padd (padd a b) c = padd a (padd b c) := by
  apply PreQ.ext
  · simp only [padd]
    calc (a.num * b.den + b.num * a.den) * c.den
          + c.num * (a.den * b.den)
        = (a.num * b.den) * c.den + (b.num * a.den) * c.den
            + c.num * (a.den * b.den) := by
          rw [Int.add_mul]
      _ = a.num * (b.den * c.den) + (b.num * c.den) * a.den
            + (c.num * b.den) * a.den := by
          have h1 : (a.num * b.den) * c.den = a.num * (b.den * c.den) :=
            Int.mul_assoc _ _ _
          have h2 : (b.num * a.den) * c.den = (b.num * c.den) * a.den := by
            ac_rfl
          have h3 : c.num * (a.den * b.den) = (c.num * b.den) * a.den := by
            ac_rfl
          rw [h1, h2, h3]
      _ = a.num * (b.den * c.den)
            + ((b.num * c.den) * a.den + (c.num * b.den) * a.den) := by
          rw [Int.add_assoc]
      _ = a.num * (b.den * c.den)
            + (b.num * c.den + c.num * b.den) * a.den := by
          rw [Int.add_mul]
  · simp only [padd]
    exact Int.mul_assoc a.den b.den c.den

theorem padd_zero (a : PreQ) : padd pzero a = a := by
  apply PreQ.ext
  · simp only [padd, pzero, Int.zero_mul, Int.one_mul, Int.mul_one, Int.zero_add]
  · simp only [padd, pzero, Int.one_mul]

theorem padd_neg (a : PreQ) : qrel (padd a (pneg a)) pzero := by
  unfold qrel padd pneg pzero
  rw [Int.neg_mul, Int.add_right_neg, Int.mul_one, Int.zero_mul]

theorem pmul_comm (a b : PreQ) : pmul a b = pmul b a := by
  apply PreQ.ext
  · simp only [pmul]
    exact Int.mul_comm _ _
  · simp only [pmul]
    exact Int.mul_comm _ _

theorem pmul_assoc (a b c : PreQ) :
    pmul (pmul a b) c = pmul a (pmul b c) := by
  apply PreQ.ext
  · simp only [pmul]
    exact Int.mul_assoc _ _ _
  · simp only [pmul]
    exact Int.mul_assoc _ _ _

theorem pmul_one (a : PreQ) : pmul pone a = a := by
  apply PreQ.ext
  · simp only [pmul, pone, Int.one_mul]
  · simp only [pmul, pone, Int.one_mul]

theorem pmul_padd (a b c : PreQ) :
    qrel (pmul a (padd b c)) (padd (pmul a b) (pmul a c)) := by
  unfold qrel pmul padd
  rw [Int.mul_add, Int.add_mul, Int.add_mul]
  have h1 :
      a.num * (b.num * c.den) * ((a.den * b.den) * (a.den * c.den)) =
        a.num * b.num * (a.den * c.den) * (a.den * (b.den * c.den)) := by
    ac_rfl
  have h2 :
      a.num * (c.num * b.den) * ((a.den * b.den) * (a.den * c.den)) =
        a.num * c.num * (a.den * b.den) * (a.den * (b.den * c.den)) := by
    ac_rfl
  rw [h1, h2]

theorem pmul_zero (a : PreQ) : qrel (pmul a pzero) pzero := by
  unfold qrel pmul pzero
  rw [Int.mul_zero, Int.zero_mul, Int.zero_mul]



def addPre (a : PreQ) (y : Frac) : Frac :=
  Quot.lift
    (fun b => mkQ (padd a b))
    (fun _b _b' hb => Quotient.sound (padd_congr (qrel_refl a) hb))
    y

def mulPre (a : PreQ) (y : Frac) : Frac :=
  Quot.lift
    (fun b => mkQ (pmul a b))
    (fun _b _b' hb => Quotient.sound (pmul_congr (qrel_refl a) hb))
    y

theorem addPre_mk (a b : PreQ) : addPre a (mkQ b) = mkQ (padd a b) :=
  rfl

theorem mulPre_mk (a b : PreQ) : mulPre a (mkQ b) = mkQ (pmul a b) :=
  rfl

theorem addPre_congr {a a' : PreQ} (ha : qrel a a') (y : Frac) :
    addPre a y = addPre a' y := by
  apply frac_ind (motive := fun y => addPre a y = addPre a' y)
  intro b
  rw [addPre_mk, addPre_mk]
  exact Quotient.sound (padd_congr ha (qrel_refl b))

theorem mulPre_congr {a a' : PreQ} (ha : qrel a a') (y : Frac) :
    mulPre a y = mulPre a' y := by
  apply frac_ind (motive := fun y => mulPre a y = mulPre a' y)
  intro b
  rw [mulPre_mk, mulPre_mk]
  exact Quotient.sound (pmul_congr ha (qrel_refl b))

def fadd (x y : Frac) : Frac :=
  Quot.lift (fun a => addPre a y) (fun _a _a' ha => addPre_congr ha y) x

def fmul (x y : Frac) : Frac :=
  Quot.lift (fun a => mulPre a y) (fun _a _a' ha => mulPre_congr ha y) x

def fneg (x : Frac) : Frac :=
  Quot.lift
    (fun a => mkQ (pneg a))
    (fun _a _a' ha => Quotient.sound (pneg_congr ha))
    x

theorem fadd_mk (a b : PreQ) : fadd (mkQ a) (mkQ b) = mkQ (padd a b) :=
  rfl

theorem fmul_mk (a b : PreQ) : fmul (mkQ a) (mkQ b) = mkQ (pmul a b) :=
  rfl

theorem fneg_mk (a : PreQ) : fneg (mkQ a) = mkQ (pneg a) :=
  rfl

theorem fadd_comm (x y : Frac) : fadd x y = fadd y x := by
  apply frac_ind (motive := fun x => fadd x y = fadd y x)
  intro a
  apply frac_ind (motive := fun y => fadd (mkQ a) y = fadd y (mkQ a))
  intro b
  rw [fadd_mk, fadd_mk]
  exact congrArg mkQ (padd_comm a b)

theorem fadd_assoc (x y z : Frac) :
    fadd (fadd x y) z = fadd x (fadd y z) := by
  apply frac_ind (motive := fun x => fadd (fadd x y) z = fadd x (fadd y z))
  intro a
  apply frac_ind (motive := fun y =>
    fadd (fadd (mkQ a) y) z = fadd (mkQ a) (fadd y z))
  intro b
  apply frac_ind (motive := fun z =>
    fadd (fadd (mkQ a) (mkQ b)) z = fadd (mkQ a) (fadd (mkQ b) z))
  intro c
  rw [fadd_mk, fadd_mk, fadd_mk, fadd_mk]
  exact congrArg mkQ (padd_assoc a b c)

theorem fzero_add (x : Frac) : fadd fzero x = x := by
  apply frac_ind (motive := fun x => fadd fzero x = x)
  intro a
  rw [fzero, ofInt, fadd_mk]
  change mkQ (padd pzero a) = mkQ a
  rw [padd_zero]

theorem fadd_neg (x : Frac) : fadd x (fneg x) = fzero := by
  apply frac_ind (motive := fun x => fadd x (fneg x) = fzero)
  intro a
  rw [fneg_mk, fadd_mk, fzero, ofInt]
  exact Quotient.sound (padd_neg a)

theorem fmul_comm (x y : Frac) : fmul x y = fmul y x := by
  apply frac_ind (motive := fun x => fmul x y = fmul y x)
  intro a
  apply frac_ind (motive := fun y => fmul (mkQ a) y = fmul y (mkQ a))
  intro b
  rw [fmul_mk, fmul_mk]
  exact congrArg mkQ (pmul_comm a b)

theorem fmul_assoc (x y z : Frac) :
    fmul (fmul x y) z = fmul x (fmul y z) := by
  apply frac_ind (motive := fun x => fmul (fmul x y) z = fmul x (fmul y z))
  intro a
  apply frac_ind (motive := fun y =>
    fmul (fmul (mkQ a) y) z = fmul (mkQ a) (fmul y z))
  intro b
  apply frac_ind (motive := fun z =>
    fmul (fmul (mkQ a) (mkQ b)) z = fmul (mkQ a) (fmul (mkQ b) z))
  intro c
  rw [fmul_mk, fmul_mk, fmul_mk, fmul_mk]
  exact congrArg mkQ (pmul_assoc a b c)

theorem fone_mul (x : Frac) : fmul fone x = x := by
  apply frac_ind (motive := fun x => fmul fone x = x)
  intro a
  rw [fone, ofInt, fmul_mk]
  change mkQ (pmul pone a) = mkQ a
  rw [pmul_one]

theorem fmul_add (x y z : Frac) :
    fmul x (fadd y z) = fadd (fmul x y) (fmul x z) := by
  apply frac_ind (motive := fun x =>
    fmul x (fadd y z) = fadd (fmul x y) (fmul x z))
  intro a
  apply frac_ind (motive := fun y =>
    fmul (mkQ a) (fadd y z) = fadd (fmul (mkQ a) y) (fmul (mkQ a) z))
  intro b
  apply frac_ind (motive := fun z =>
    fmul (mkQ a) (fadd (mkQ b) z) =
      fadd (fmul (mkQ a) (mkQ b)) (fmul (mkQ a) z))
  intro c
  rw [fadd_mk, fmul_mk, fmul_mk, fmul_mk, fadd_mk]
  exact Quotient.sound (pmul_padd a b c)

theorem fmul_zero (x : Frac) : fmul x fzero = fzero := by
  apply frac_ind (motive := fun x => fmul x fzero = fzero)
  intro a
  rw [fzero, ofInt, fmul_mk]
  exact Quotient.sound (pmul_zero a)

def fracPack : StarRingPack Frac where
  add := fadd
  mul := fmul
  neg := fneg
  zero := fzero
  one := fone
  conj := id
  add_comm := fadd_comm
  add_assoc := fadd_assoc
  zero_add := fzero_add
  add_neg := fadd_neg
  mul_comm := fmul_comm
  mul_assoc := fmul_assoc
  one_mul := fone_mul
  mul_add := fmul_add
  mul_zero := fmul_zero
  conj_add := fun _ _ => rfl
  conj_mul := fun _ _ => rfl
  conj_conj := fun _ => rfl
  conj_zero := rfl
  conj_one := rfl

#print axioms fracPack


theorem half_add_half : fadd half half = fone := by
  have h : qrel (padd phalf phalf) pone := by
    unfold qrel padd phalf pone
    decide
  rw [half, fone, ofInt, fadd_mk]
  exact Quotient.sound h

theorem half_add_zero : fadd half fzero = half := by
  have h : qrel (padd phalf pzero) phalf := by
    unfold qrel padd phalf pzero
    decide
  rw [half, fzero, ofInt, fadd_mk]
  exact Quotient.sound h

theorem rsum_two_halves :
    rsum fracPack [half, half] = fone := by
  simp only [rsum, fracPack]
  rw [half_add_zero, half_add_half]

def uniformHalf (_ : Bool) : Frac := half

theorem uniform_half_mass :
    rsum fracPack (enumBool.elems.map uniformHalf) = fone := by
  simp only [enumBool, uniformHalf, List.map]
  exact rsum_two_halves

theorem half_ne_zero : half ≠ fzero := by
  intro h
  have hr : qrel phalf pzero := Quotient.exact h
  unfold qrel phalf pzero at hr
  cases hr

theorem half_ne_one : half ≠ fone := by
  intro h
  have hr : qrel phalf pone := Quotient.exact h
  unfold qrel phalf pone at hr
  cases hr

theorem half_rep_nonneg : 0 ≤ phalf.num := by decide

theorem fractional_half_simplex :
    rsum fracPack (enumBool.elems.map uniformHalf) = fone ∧
      half ≠ fzero ∧
      half ≠ fone ∧
      0 ≤ phalf.num :=
  ⟨uniform_half_mass, half_ne_zero, half_ne_one, half_rep_nonneg⟩

#print axioms fractional_half_simplex

theorem choice_free_fractional_weights :
    (∀ a b : Frac, fracPack.add a b = fracPack.add b a) ∧
      rsum fracPack [half, half] = fone ∧
      half ≠ fzero ∧
      half ≠ fone :=
  ⟨fracPack.add_comm, rsum_two_halves, half_ne_zero, half_ne_one⟩

#print axioms choice_free_fractional_weights

theorem ofInt_add (m n : Int) :
    ofInt (m + n) = fadd (ofInt m) (ofInt n) := by
  have h : padd ⟨m, 1, one_pos⟩ ⟨n, 1, one_pos⟩ = ⟨m + n, 1, one_pos⟩ := by
    apply PreQ.ext
    · simp only [padd, Int.mul_one]
    · simp only [padd, Int.one_mul]
  rw [ofInt, ofInt, ofInt, fadd_mk]
  exact congrArg mkQ h.symm

#print axioms ofInt_add

end HilbertWalk.Rationals

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkRationals.lean Claim: PreQ AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
