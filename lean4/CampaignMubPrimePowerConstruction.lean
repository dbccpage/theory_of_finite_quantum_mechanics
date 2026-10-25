/-
Narrowed boundary for MUB-PRIME-POWER-CONSTRUCTION.
Dimension 2, characteristic two, three explicit bases over the Gaussian integers.
This module does not construct a family in any larger prime power, and it does not
treat dimension six.
-/

abbrev Gauss := Int × Int

def gadd (a b : Gauss) : Gauss := (a.1 + b.1, a.2 + b.2)

def gmul (a b : Gauss) : Gauss :=
  (a.1 * b.1 - a.2 * b.2, a.1 * b.2 + a.2 * b.1)

def gconj (a : Gauss) : Gauss := (a.1, -a.2)

def gnorm (a : Gauss) : Int := a.1 * a.1 + a.2 * a.2

abbrev Vec := Gauss × Gauss

def ip (u v : Vec) : Gauss :=
  gadd (gmul (gconj u.1) v.1) (gmul (gconj u.2) v.2)

def vnorm (u : Vec) : Int := gnorm u.1 + gnorm u.2

def balanced (u v : Vec) : Prop :=
  gnorm (ip u v) * 2 = vnorm u * vnorm v

def z0 : Vec := ((1, 0), (0, 0))
def z1 : Vec := ((0, 0), (1, 0))
def x0 : Vec := ((1, 0), (1, 0))
def x1 : Vec := ((1, 0), (-1, 0))
def y0 : Vec := ((1, 0), (0, 1))
def y1 : Vec := ((1, 0), (0, -1))

def chi (b : Bool) : Int :=
  if b then -1 else 1

theorem i_squared : gmul (0, 1) (0, 1) = (-1, 0) := by
  decide

theorem squared_norms :
    vnorm z0 = 1 ∧ vnorm z1 = 1 ∧
      vnorm x0 = 2 ∧ vnorm x1 = 2 ∧
        vnorm y0 = 2 ∧ vnorm y1 = 2 := by
  decide

theorem self_inner :
    ip z0 z0 = (1, 0) ∧ ip z1 z1 = (1, 0) ∧
      ip x0 x0 = (2, 0) ∧ ip x1 x1 = (2, 0) ∧
        ip y0 y0 = (2, 0) ∧ ip y1 y1 = (2, 0) := by
  decide

theorem basis_orthogonal :
    ip z0 z1 = (0, 0) ∧ ip x0 x1 = (0, 0) ∧ ip y0 y1 = (0, 0) := by
  decide

theorem cross_unbiased :
    balanced z0 x0 ∧ balanced z0 x1 ∧ balanced z1 x0 ∧ balanced z1 x1 ∧
      balanced z0 y0 ∧ balanced z0 y1 ∧ balanced z1 y0 ∧ balanced z1 y1 ∧
        balanced x0 y0 ∧ balanced x0 y1 ∧ balanced x1 y0 ∧ balanced x1 y1 := by
  unfold balanced ip vnorm gnorm gadd gmul gconj z0 z1 x0 x1 y0 y1
  decide

theorem char_values : chi false = 1 ∧ chi true = -1 := by
  decide

theorem char_of_double :
    (false ^^ false) = false ∧ (true ^^ true) = false ∧
      chi (false ^^ false) = 1 ∧ chi (true ^^ true) = 1 := by
  decide

#print axioms i_squared
#print axioms squared_norms
#print axioms self_inner
#print axioms basis_orthogonal
#print axioms cross_unbiased
#print axioms char_values
#print axioms char_of_double
