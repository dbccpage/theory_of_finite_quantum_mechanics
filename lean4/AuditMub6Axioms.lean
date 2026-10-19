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
import Lean.Util.CollectAxioms

-- Unified kernel-level #print axioms gate across MUB(6), FSP, and Majorana top-level roots
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
  for reqMod in (#[`Mub6] ++ fspRoots ++ majoranaRoots) do
    unless moduleSet.contains reqMod do
      throwError "Missing required root module in unified axiom audit: {reqMod}"

  let fspSet := fspRoots.foldl (fun (s : NameHashSet) name => s.insert name) {}
  let majoranaSet := majoranaRoots.foldl (fun (s : NameHashSet) name => s.insert name) {}
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
        if !fspSet.contains modName && !majoranaSet.contains modName then
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
  let mub6Mods := modules.filter (fun m => !fspSet.contains m && !majoranaSet.contains m) |>.size
  logInfo m!"MUB6_AXIOM_AUDIT_PASS modules={modules.size} declarations={count} violations={violations}"
  logInfo m!"UNIFIED_AXIOM_AUDIT_PASS mub6_modules={mub6Mods} fsp_modules={fspRoots.size} majorana_modules={majoranaRoots.size} total_modules={modules.size} mub6_declarations={mub6Decls} fsp_declarations={fspDecls} majorana_declarations={majoranaDecls} total_declarations={count} violations={violations}"

