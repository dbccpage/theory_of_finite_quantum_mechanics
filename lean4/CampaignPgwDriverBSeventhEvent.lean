import Imported.Genesis19l57g1.Derivation.Basic

open Derivation

/-
Narrowed boundary for PGW-DRIVER-B-SEVENTH-EVENT.
The sealed derivation Event has six constructors.
This module does not read a harness and does not add a constructor.
-/

def pgwDrvB_kindNames : List String :=
  ["Supply", "AdmitDatum", "AdmitForm", "AdmitInst", "AdmitRuleAll", "Impose"]

def pgwDrvB_kindName : Event → String
  | .supply _ => "Supply"
  | .admitDatum => "AdmitDatum"
  | .admitForm _ => "AdmitForm"
  | .admitInst _ _ => "AdmitInst"
  | .admitRuleAll _ => "AdmitRuleAll"
  | .impose _ _ => "Impose"

theorem pgwDrvB_kind_count : pgwDrvB_kindNames.length = 6 := by
  decide

theorem pgwDrvB_kind_nodup : pgwDrvB_kindNames.Nodup := by
  decide

theorem pgwDrvB_kindName_mem (e : Event) : pgwDrvB_kindName e ∈ pgwDrvB_kindNames := by
  cases e with
  | supply _ =>
    show "Supply" ∈ pgwDrvB_kindNames
    decide
  | admitDatum =>
    show "AdmitDatum" ∈ pgwDrvB_kindNames
    decide
  | admitForm _ =>
    show "AdmitForm" ∈ pgwDrvB_kindNames
    decide
  | admitInst _ _ =>
    show "AdmitInst" ∈ pgwDrvB_kindNames
    decide
  | admitRuleAll _ =>
    show "AdmitRuleAll" ∈ pgwDrvB_kindNames
    decide
  | impose _ _ =>
    show "Impose" ∈ pgwDrvB_kindNames
    decide

theorem pgwDrvB_names_realized :
    pgwDrvB_kindName (.supply 0) = "Supply" ∧
      pgwDrvB_kindName .admitDatum = "AdmitDatum" ∧
      pgwDrvB_kindName (.admitForm 1) = "AdmitForm" ∧
      pgwDrvB_kindName (.admitInst 0 []) = "AdmitInst" ∧
      pgwDrvB_kindName (.admitRuleAll 0) = "AdmitRuleAll" ∧
      pgwDrvB_kindName (.impose 0 1) = "Impose" := by
  decide

theorem pgwDrvB_seventh_outside : "Seventh" ∉ pgwDrvB_kindNames := by
  decide

theorem pgwDrvB_no_seventh_name (e : Event) : pgwDrvB_kindName e ≠ "Seventh" := by
  cases e with
  | supply _ =>
    show "Supply" ≠ "Seventh"
    decide
  | admitDatum =>
    show "AdmitDatum" ≠ "Seventh"
    decide
  | admitForm _ =>
    show "AdmitForm" ≠ "Seventh"
    decide
  | admitInst _ _ =>
    show "AdmitInst" ≠ "Seventh"
    decide
  | admitRuleAll _ =>
    show "AdmitRuleAll" ≠ "Seventh"
    decide
  | impose _ _ =>
    show "Impose" ≠ "Seventh"
    decide

#print axioms pgwDrvB_kind_count
#print axioms pgwDrvB_kind_nodup
#print axioms pgwDrvB_kindName_mem
#print axioms pgwDrvB_names_realized
#print axioms pgwDrvB_seventh_outside
#print axioms pgwDrvB_no_seventh_name
