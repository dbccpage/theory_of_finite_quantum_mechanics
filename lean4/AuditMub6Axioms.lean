import Mub6
import FermionSignAll
import BfLinkedFluxBraiding
import BqnfSignPacket
import ChiralAnomalyInflow
import ChiralSuperconductorCore
import Cobordism5dAnomaly
import FermionGinCore
import FermionSignCore
import FibonacciAnyonBraiding
import FoliatedFracton2Gauge
import FqhLaughlinBraiding
import FrustratedSpectrumObstruction
import GenesisFspBridge
import HaltingQuotient
import Higher2GroupBraiding
import InstantonDyonGas
import IsingMajoranaBraiding
import KitaevHoneycombCore
import MajoranaGinCore
import MeronCharacter
import MeronClusterInvolution
import NonAbelianBfBraiding
import NonAbelianGaugeSigns
import NormalFormLaws
import ReggePachnerWdw
import regge_wdw_core
import MajoranaCore
import FiniteQM
import DerivationDagQMClosure
import FiniteQFTAndGravity
import RaveraDfmFiniteToContinuum
import ContextualityObstruction
import QuantumCorrelation
import NoSignalling
import RotationGroups
import LorentzBoost
import Superposition
import Entanglement
import BornNormalization
import UnitaryInvariance
import Lean.Util.CollectAxioms

-- Unified kernel-level #print axioms gate across MUB(6), FSP, Majorana, and QM/QFT/Gravity top-level roots
#print axioms MUB6.GrandUnifiedMasterSynthesis.grand_unified_master_synthesis_assembly
#print axioms MUB6.RouteC.no_complete_mub6_via_route_c
#print axioms FermionSignAll.package_mechanization_total
#print axioms FermionSignTower.zeroRel_equiv
#print axioms ChiralSuperconductorCore.nielsen_ninomiya_pair_cancellation
#print axioms KitaevHoneycombCore.valid_vortex_pair_routes_to_repair
#print axioms PhysicsNormalForms.schlafli_zero_variation
#print axioms MajoranaGinCore.involution_pair_cancels_sign
#print axioms trichotomy_pairwise_disjoint
#print axioms mzm_boundary_decoupling
#print axioms FiniteQM.p2_sq_eq_p4_add_two_p22
#print axioms FiniteQM.five_import_mutual_independence
#print axioms FiniteQM.weyl_heisenberg_finite_trace_obstruction
#print axioms FiniteQM.dirichlet_square_well_laplacian_and_sturm_nodes
#print axioms FiniteQM.harmonic_oscillator_truncated_fock_ladder_and_boundary_defect
#print axioms FiniteQM.potential_barrier_transfer_matrix_and_flux_conservation
#print axioms FiniteQM.stern_gerlach_three_filter_regeneration_and_rabi_cayley_step
#print axioms FiniteQM.spin_half_pair_clebsch_gordan_singlet_triplet_casimir
#print axioms FiniteQM.rayleigh_schrodinger_perturbation_and_degenerate_stark_splitting
#print axioms FiniteQM.pancharatnam_berry_discrete_holonomy_gauge_invariance
#print axioms FiniteQM.fermi_golden_rule_short_time_decay_vs_heisenberg_revival
#print axioms QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor
#print axioms FiniteQFTAndGravity.kn_textbook_form
#print axioms RaveraDfmFiniteToContinuum.sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1
#print axioms ContextualityObstruction.x1_has_no_global_section
#print axioms QuantumCorrelation.q2_tsirelson_attainment
#print axioms NoSignalling.no_signalling_under_admitted_composition
#print axioms RotationGroups.octahedral_realization_in_so3_z
#print axioms LorentzBoost.boost_hyperbolic_identity
#print axioms Superposition.sorkin_third_order_interference_vanishes
#print axioms Entanglement.bell_state_is_entangled
#print axioms BornNormalization.born_normalization_redundancy
#print axioms MUB6.Gluing.fourth_basis_unitary_invariance

open Lean Elab Command

run_elab do
  let env ← getEnv
  let moduleNames := env.header.moduleNames
  let progress ← IO.getStderr
  progress.putStrLn "MUB6_AUDIT_PHASE environment_loaded"
  progress.flush
  let sources ← (System.FilePath.mk ".").readDir
  let modules := sources.filterMap fun entry =>
    if entry.fileName.endsWith ".lean" then
      let modName := Name.mkSimple (entry.fileName.dropEnd 5).toString
      if moduleNames.contains modName then some modName else none
    else none
  let moduleSet := modules.foldl (fun (s : NameHashSet) name => s.insert name) {}

  let fspRoots : Array Name := #[
    `BfLinkedFluxBraiding, `BqnfSignPacket, `ChiralAnomalyInflow,
    `ChiralSuperconductorCore, `Cobordism5dAnomaly, `FermionGinCore,
    `FermionSignAll, `FermionSignCore, `FibonacciAnyonBraiding,
    `FoliatedFracton2Gauge, `FqhLaughlinBraiding, `FrustratedSpectrumObstruction,
    `GenesisFspBridge, `HaltingQuotient, `Higher2GroupBraiding,
    `InstantonDyonGas, `IsingMajoranaBraiding, `KitaevHoneycombCore,
    `MajoranaGinCore, `MeronCharacter, `MeronClusterInvolution,
    `NonAbelianBfBraiding, `NonAbelianGaugeSigns, `NormalFormLaws,
    `ReggePachnerWdw, `regge_wdw_core
  ]
  let majoranaRoots : Array Name := #[
    `MajoranaCore, `MajoranaGinCore
  ]
  let qmRoots : Array Name := #[
    `FiniteQM, `DerivationDagQMClosure, `FiniteQFTAndGravity,
    `RaveraDfmFiniteToContinuum, `ContextualityObstruction,
    `QuantumCorrelation, `NoSignalling, `RotationGroups,
    `LorentzBoost, `Superposition, `Entanglement,
    `BornNormalization, `UnitaryInvariance
  ]
  for reqMod in (#[`Mub6] ++ fspRoots ++ majoranaRoots ++ qmRoots) do
    unless moduleSet.contains reqMod do
      throwError "Missing required root module in unified axiom audit: {reqMod}"

  let fspSet := fspRoots.foldl (fun (s : NameHashSet) name => s.insert name) {}
  let majoranaSet := majoranaRoots.foldl (fun (s : NameHashSet) name => s.insert name) {}
  let qmSet := qmRoots.foldl (fun (s : NameHashSet) name => s.insert name) {}
  let allowed : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]
  let localDeclarations := env.constants.toList.filter fun (name, _) =>
    match env.getModuleIdxFor? name with
    | some idx => moduleSet.contains moduleNames[idx.toNat]!
    | none => false
  progress.putStrLn s!"MUB6_AUDIT_PHASE local_declarations={localDeclarations.length}"
  progress.flush
  let declarations := localDeclarations.toArray.qsort fun a b => Name.quickLt a.1 b.1
  let mut count : Nat := 0
  let mut mub6Decls : Nat := 0
  let mut fspDecls : Nat := 0
  let mut majoranaDecls : Nat := 0
  let mut qmDecls : Nat := 0
  let mut violations : Nat := 0
  for (name, _) in declarations do
    if let some idx := env.getModuleIdxFor? name then
      let modName := moduleNames[idx.toNat]!
      if moduleSet.contains modName then
        count := count + 1
        if majoranaSet.contains modName then
          majoranaDecls := majoranaDecls + 1
        if fspSet.contains modName then
          fspDecls := fspDecls + 1
        if qmSet.contains modName then
          qmDecls := qmDecls + 1
        if !fspSet.contains modName && !majoranaSet.contains modName && !qmSet.contains modName then
          mub6Decls := mub6Decls + 1
        if count % 1000 == 0 then
          progress.putStrLn s!"MUB6_AUDIT_PROGRESS declarations={count}"
          progress.flush
        let axioms ← Lean.collectAxioms name
        logInfo m!"MUB6_AXIOM_DEPENDENCIES {name}: {axioms}"
        for axiomName in axioms do
          unless allowed.contains axiomName do
            violations := violations + 1
            logError m!"Disallowed dependency: {name} -> {axiomName}"
  if count == 0 then
    throwError "Empty declaration audit"
  if violations != 0 then
    throwError "Axiom audit failed: {violations} disallowed dependencies"
  let mub6Mods := modules.filter (fun m => !fspSet.contains m && !majoranaSet.contains m && !qmSet.contains m) |>.size
  logInfo m!"MUB6_AXIOM_AUDIT_PASS modules={modules.size} declarations={count} violations={violations}"
  logInfo m!"UNIFIED_AXIOM_AUDIT_PASS mub6_modules={mub6Mods} fsp_modules={fspRoots.size} majorana_modules={majoranaRoots.size} qm_modules={qmRoots.size} total_modules={modules.size} mub6_declarations={mub6Decls} fsp_declarations={fspDecls} majorana_declarations={majoranaDecls} qm_declarations={qmDecls} total_declarations={count} violations={violations}"

