import Paper
import ParkedAudit
import Inventory

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for modName in env.header.moduleNames do
    if (`Derivation).isPrefixOf modName || (`SecondRun).isPrefixOf modName ||
        #[`Paper, `PaperCanonical, `PaperWire, `PaperOrbit, `PaperSearch,
          `Permutation, `RegimeAction, `CanonicalMinimizer].contains modName then
      match env.getModuleIdx? modName with
      | none => throwError "census module absent: {modName}"
      | some idx =>
        let data := env.header.moduleData[idx.toNat]!
        let names := data.constNames.filter fun name =>
          !name.isInternalDetail && (env.find? name).any (·.isTheorem)
        for name in names.qsort (fun a b => a.toString < b.toString) do
          let axioms ← liftCoreM (Lean.collectAxioms name)
          let allowed := if modName == `Paper then
            #[`propext, `Quot.sound, `Classical.choice] else #[`propext, `Quot.sound]
          for axiomName in axioms do
            if !allowed.contains axiomName then
              throwError "unauthorized axiom {axiomName} in {name}"
          logInfo (ParkedAudit.renderReport name axioms)
