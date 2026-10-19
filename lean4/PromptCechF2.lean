import ContextualityObstruction
import DualWitness

/- Exact native overlap ranks and the global incidence ranks are distinct.
   This module does not turn a native rank output into a kernel rank theorem.
   Origin: FQ-CONTEXTUALITY-CECH-F2. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptCechF2
theorem differential_squares_zero {n m : Nat}
    (s : ContextualityObstruction.Cochain0 n m) (i j k : Fin m) (r : Fin n) :
    ContextualityObstruction.d1 (ContextualityObstruction.d0 s) i j k r = 0 :=
  ContextualityObstruction.differential_squares_to_zero s i j k r
theorem cabello_no_global_section :
    ¬ (∃ g, ContextualityObstruction.IsGlobalSection ContextualityObstruction.X1 g) :=
  ContextualityObstruction.x1_has_no_global_section
theorem mermin_parity (s : DualWitness.MagicSquareAssignment) :
    DualWitness.row1_prod s = .Pos → DualWitness.row2_prod s = .Pos →
    DualWitness.row3_prod s = .Pos → DualWitness.col1_prod s = .Pos →
    DualWitness.col2_prod s = .Pos → DualWitness.col3_prod s = .Neg → False :=
  DualWitness.mermin_peres_parity_obstruction s
theorem valid_global_control :
    ContextualityObstruction.IsGlobalSection ContextualityObstruction.X2
      ContextualityObstruction.g_X2 := ContextualityObstruction.x2_global_section_valid
theorem character_blocks_preimage {A B : Type} (d : A → B) (chi : B → Fin 2)
    (b : B) (annihilates : ∀ a, chi (d a) = 0) (nonzero : chi b ≠ 0) :
    ¬ ∃ a, d a = b := by
  rintro ⟨a, ha⟩
  exact nonzero (ha ▸ annihilates a)
end QuantumMechanics.PromptCechF2
#print axioms QuantumMechanics.PromptCechF2.differential_squares_zero
#print axioms QuantumMechanics.PromptCechF2.cabello_no_global_section
#print axioms QuantumMechanics.PromptCechF2.mermin_parity
#print axioms QuantumMechanics.PromptCechF2.valid_global_control
#print axioms QuantumMechanics.PromptCechF2.character_blocks_preimage
