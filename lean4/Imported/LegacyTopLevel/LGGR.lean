/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 75209e051175aeddab58ae007c79ec08504328821931fec3178608242865c6df (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.LGGR
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
/-
Does not elaborate. The four imported module names are not Lean sources in
this repository or its git history (`git log -S` on the import strings finds
only the commit that added these imports). Related `PaperAE004` text lives
under different module names in the atlas LGGR package and is not this
import. Declarations below were not typechecked.
-/
import core_l020_01_local_green_counterexample
import core_l020_08_primitive_difference_bridge
import core_l025_16_minimal_local_green_global_red
import core_l025_32_sheaf_analogy_not_equivalence

/-!
LGGR bridge for the S(n) packetization paper.

The main point is negative and finite: local green observations and sheaf-style
local consistency reports are not enough to carry the global evaluator through
the local-dashboard quotient.
-/

namespace SnPacketGame

theorem minimal_lggr_delta :
    PaperAE004.deltaEval true true false = -1 :=
  PaperAE004.local_green_global_red_counterexample

theorem local_green_does_not_force_global_green :
    ∃ e1 e2 eg : Bool,
      PaperAE004.localProduct e1 e2 = 1 ∧
        PaperAE004.b2i eg = 0 ∧
        PaperAE004.deltaEval e1 e2 eg = -1 :=
  PaperAE006.local_green_does_not_force_global_green

theorem local_dashboard_zero_identifies_good_and_lggr :
    PaperAE004.localDashboardPrimitiveDifference.ZeroRel
      PaperAE004.allGreenTriple PaperAE004.lggrTriple :=
  PaperAE004.local_dashboard_zero_identifies_all_green_and_lggr

theorem local_dashboard_quotient_cannot_carry_global_green :
    ¬ (∃ F :
          ObstructionCore.PrimitiveDifference.ResidualQuotient
              PaperAE004.localDashboardPrimitiveDifference → Bool,
        ∀ x : PaperAE004.EvalTriple,
          F (ObstructionCore.PrimitiveDifference.classOf
                PaperAE004.localDashboardPrimitiveDifference x) =
            PaperAE004.isGlobalGreenTriple x) :=
  PaperAE004.global_classifier_no_factor_through_local_dashboard_quotient

theorem local_dashboard_quotient_cannot_carry_evaluator_defect :
    ¬ (∃ F :
          ObstructionCore.PrimitiveDifference.ResidualQuotient
              PaperAE004.localDashboardPrimitiveDifference → Int,
        ∀ x : PaperAE004.EvalTriple,
          F (ObstructionCore.PrimitiveDifference.classOf
                PaperAE004.localDashboardPrimitiveDifference x) =
            PaperAE004.tripleEvaluatorDefect x) :=
  PaperAE004.evaluator_defect_no_factor_through_local_dashboard_quotient

theorem local_sheaf_consistency_does_not_prove_epk_equivalence :
    PaperAE006.sheafEpkComparisonStatus
      { sheafCarrierMapped := false,
        localStateMapDeclared := false,
        evaluatorTraceMapDeclared := false,
        cleanGateMapDeclared := false,
        authorityFirewallMapDeclared := false,
        localConsistencyObserved := true } ≠
      PaperAE006.SheafEpkComparisonStatus.epkComparisonReady :=
  PaperAE006.local_sheaf_consistency_alone_blocks_epk_equivalence

#print axioms SnPacketGame.minimal_lggr_delta
#print axioms SnPacketGame.local_green_does_not_force_global_green
#print axioms SnPacketGame.local_dashboard_zero_identifies_good_and_lggr
#print axioms SnPacketGame.local_dashboard_quotient_cannot_carry_global_green
#print axioms SnPacketGame.local_dashboard_quotient_cannot_carry_evaluator_defect
#print axioms SnPacketGame.local_sheaf_consistency_does_not_prove_epk_equivalence

end SnPacketGame

