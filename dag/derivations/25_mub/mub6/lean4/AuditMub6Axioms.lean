import Mub6
import Lean.Util.CollectAxioms

open Lean Elab Command

/-! Audit every declaration owned by a local source module, not only selected
published theorem names. Fails when a local module is omitted or any dependency
lies outside the explicitly allowed foundational axiom set. -/
run_elab do
  let env ← getEnv
  -- Cache this projection: EnvironmentHeader.moduleNames maps the entire import array.
  let moduleNames := env.header.moduleNames
  let progress ← IO.getStderr
  progress.putStrLn "MUB6_AUDIT_PHASE environment_loaded"
  progress.flush
  let sources ← (System.FilePath.mk ".").readDir
  let modules := sources.filterMap fun entry =>
    if entry.fileName.endsWith ".lean" then
      some (Name.mkSimple (entry.fileName.dropEnd 5).toString)
    else none
  for moduleName in modules do
    unless moduleNames.contains moduleName do
      throwError "Local source module not imported: {moduleName}"
  let moduleSet := modules.foldl (fun (s : NameHashSet) name => s.insert name) {}
  let allowed : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]
  -- Select owned declarations before sorting, so imported mathlib declarations
  -- do not dominate this local audit's time and memory.
  let localDeclarations := env.constants.toList.filter fun (name, _) =>
    match env.getModuleIdxFor? name with
    | some idx => moduleSet.contains moduleNames[idx.toNat]!
    | none => false
  progress.putStrLn s!"MUB6_AUDIT_PHASE local_declarations={localDeclarations.length}"
  progress.flush
  let declarations := localDeclarations.toArray.qsort fun a b => Name.quickLt a.1 b.1
  let mut count : Nat := 0
  let mut violations : Nat := 0
  for (name, _) in declarations do
    if let some idx := env.getModuleIdxFor? name then
      if moduleSet.contains moduleNames[idx.toNat]! then
        count := count + 1
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
  logInfo m!"MUB6_AXIOM_AUDIT_PASS modules={modules.size} declarations={count} violations={violations}"
