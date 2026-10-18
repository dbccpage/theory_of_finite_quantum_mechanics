/-!
Conditional composition of abstract extension and orbit hypotheses.
This file does not construct U(6)/(T^6 x S_6), classify the CHM moduli,
or instantiate an SDP certificate on arbitrary quadruples.
The arguments of each theorem are its precise scope.
AuthorityEffect: None.
-/

namespace MUB6.Gluing.GlobalGaugeChaining
open MUB6.Gluing
open MUB6.Gluing.QuadIncompatibility

def GaugeEquivTriple (T T' : MUTriple) : Prop := UnitaryEquivTriple T T'

theorem gauge_equiv_preserves_has_fourth_basis {T T' : MUTriple}
    (h : GaugeEquivTriple T T') : HasFourthBasis T ↔ HasFourthBasis T' :=
  unitary_equiv_preserves_has_fourth_basis h

/-- A conditional finite-index lemma. All orbit restrictions are premises. -/
theorem non_dita_count_le_one
    (B : Fin 7 → Basis) (InTaoOrbit InSzollosiOrbit : Basis → Prop)
    (h_tao : ∀ i j, InTaoOrbit (B i) → InTaoOrbit (B j) → i = j)
    (h_szollosi : ∀ i j, InSzollosiOrbit (B i) → InSzollosiOrbit (B j) → i = j)
    (h_cross : ¬ ∃ i j, InTaoOrbit (B i) ∧ InSzollosiOrbit (B j)) :
    ∀ i j, (InTaoOrbit (B i) ∨ InSzollosiOrbit (B i)) →
      (InTaoOrbit (B j) ∨ InSzollosiOrbit (B j)) → i = j := by
  intro i j hi hj
  cases hi with
  | inl hi =>
    cases hj with
    | inl hj => exact h_tao i j hi hj
    | inr hj => exact False.elim (h_cross ⟨i,j,hi,hj⟩)
  | inr hi =>
    cases hj with
    | inl hj => exact False.elim (h_cross ⟨j,i,hj,hi⟩)
    | inr hj => exact h_szollosi i j hi hj

def choose : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)

/-- Arithmetic only; no existence or coverage of five bases is supplied. -/
theorem choose_five_three : choose 5 3 = 10 := by rfl

theorem global_gauge_chaining_obstruction
    (h_no_quad : ¬ MUBQuadruple) (h_comp : CompleteMUB6) : False :=
  h_no_quad (mub_quadruple_of_complete h_comp)

theorem global_gauge_chaining_obstruction_of_sdp_certificate
    {G : Matrix} (W : Matrix) (hW_psd : PSD W) (h_inner : TraceInner W G < 0)
    (h_gram_eq : ∀ B : Fin 4 → Basis, PairwiseMU B → quad_gramian B = G)
    (h_psd_prop : GenuineQuadGramianPSDProperty)
    (h_comp : CompleteMUB6) : False :=
  global_gauge_chaining_obstruction
    (no_mub_quadruple_of_sdp_certificate W hW_psd h_inner h_gram_eq h_psd_prop) h_comp

#print axioms gauge_equiv_preserves_has_fourth_basis
#print axioms non_dita_count_le_one
#print axioms choose_five_three
#print axioms global_gauge_chaining_obstruction
#print axioms global_gauge_chaining_obstruction_of_sdp_certificate
end MUB6.Gluing.GlobalGaugeChaining
