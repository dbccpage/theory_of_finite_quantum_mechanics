import Lake
open Lake DSL
package genesisPaper where
@[default_target]
lean_lib Derivation
@[default_target]
lean_lib ParkedAudit
@[default_target]
lean_lib SecondRun
lean_lib Permutation
lean_lib RegimeAction
@[default_target]
lean_lib CanonicalMinimizer
@[default_target]
lean_lib Inventory
@[default_target]
lean_lib Paper
lean_lib PaperCanonical
lean_lib PaperWire
lean_lib PaperOrbit
lean_lib PaperSearch
@[default_target]
lean_exe wireReplay where
  root := `PaperWireReplay
@[default_target]
lean_exe searchReplay where
  root := `PaperSearchReplay

-- Retain the independent finite proofs added on main.
@[default_target]
lean_lib Paper000
