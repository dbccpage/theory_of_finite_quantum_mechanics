/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/LggrNonFactorization.lean
   Original sha256: 583fe25ed28a387bef5a7b01a4bdffd6e536eb8179b6a3182faea4056b9440f2 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.LggrNonFactorization
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
`LGGR` is not a package root and `LGGR.olean` is not in the build library,
so this import does not load `lean4/LGGR.lean`. That file's own imports are
also absent.
-/
import Imported.SymbolGameLoose.LGGR
/-!
# Paper 043, T2: LGGR non-factorization facade

These declarations expose the exact finite PaperAE004/PaperAE006 LGGR kernels under
Paper 043 names. They are wrapper aliases only. In particular, Paper 043 does
not claim new quotient, sheaf, or cohomology results here.
-/

namespace PaperER007

/-- Wrapper alias of SnSymbolGameAndPackets.minimal_lggr_delta. -/
theorem lggr_minimal_delta :
    PaperAE004.deltaEval true true false = -1 :=
  SnSymbolGameAndPackets.minimal_lggr_delta

/-- Wrapper alias of the existing finite local-green/global-red witness. -/
theorem lggr_local_green_does_not_force_global_green :
    ∃ e1 e2 eg : Bool,
      PaperAE004.localProduct e1 e2 = 1 ∧
        PaperAE004.b2i eg = 0 ∧
        PaperAE004.deltaEval e1 e2 eg = -1 :=
  SnSymbolGameAndPackets.local_green_does_not_force_global_green

/-- Wrapper alias of the existing local-dashboard collision witness. -/
theorem lggr_local_dashboard_identifies_good_and_bad :
    PaperAE004.localDashboardPrimitiveDifference.ZeroRel
      PaperAE004.allGreenTriple PaperAE004.lggrTriple :=
  SnSymbolGameAndPackets.local_dashboard_zero_identifies_good_and_lggr

/--
Wrapper alias of the exact global-classifier non-factorization theorem.
The Quot.sound dependency is inherited from the upstream quotient proof.
-/
theorem lggr_global_green_does_not_descend :
    ¬ (∃ decode :
          OmegaCore.PrimitiveDifference.ResidualQuotient
              PaperAE004.localDashboardPrimitiveDifference → Bool,
        ∀ x : PaperAE004.EvalTriple,
          decode (OmegaCore.PrimitiveDifference.classOf
                PaperAE004.localDashboardPrimitiveDifference x) =
            PaperAE004.isGlobalGreenTriple x) :=
  SnSymbolGameAndPackets.local_dashboard_quotient_cannot_carry_global_green

/--
Wrapper alias of the exact evaluator-defect non-factorization theorem.
The Quot.sound dependency is inherited from the upstream quotient proof.
-/
theorem lggr_evaluator_defect_does_not_descend :
    ¬ (∃ decode :
          OmegaCore.PrimitiveDifference.ResidualQuotient
              PaperAE004.localDashboardPrimitiveDifference → Int,
        ∀ x : PaperAE004.EvalTriple,
          decode (OmegaCore.PrimitiveDifference.classOf
                PaperAE004.localDashboardPrimitiveDifference x) =
            PaperAE004.tripleEvaluatorDefect x) :=
  SnSymbolGameAndPackets.local_dashboard_quotient_cannot_carry_evaluator_defect

/--
Wrapper alias of the all-maps-undeclared finite comparison example. It does
not assert that the Symbol Game is a sheaf or that LGGR is a cohomology class.
-/
theorem local_consistency_without_bridge_maps_is_not_ready :
    PaperAE006.sheafEpkComparisonStatus
      { sheafCarrierMapped := false
        localStateMapDeclared := false
        evaluatorTraceMapDeclared := false
        cleanGateMapDeclared := false
        authorityFirewallMapDeclared := false
        localConsistencyObserved := true } ≠
      PaperAE006.SheafEpkComparisonStatus.epkComparisonReady :=
  SnSymbolGameAndPackets.local_sheaf_consistency_does_not_prove_epk_equivalence

#print axioms PaperER007.lggr_minimal_delta
#print axioms PaperER007.lggr_local_green_does_not_force_global_green
#print axioms PaperER007.lggr_local_dashboard_identifies_good_and_bad
#print axioms PaperER007.lggr_global_green_does_not_descend
#print axioms PaperER007.lggr_evaluator_defect_does_not_descend
#print axioms PaperER007.local_consistency_without_bridge_maps_is_not_ready

end PaperER007
