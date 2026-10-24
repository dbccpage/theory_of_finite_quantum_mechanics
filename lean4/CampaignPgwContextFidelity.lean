/-
Narrowed boundary for PGW-CONTEXT-FIDELITY.
Code 0 is the stale declared context and code 1 is the replayed context.
The empty-claim step and the equality binding are this two-code model only.
This module does not define ValidTrace and does not read a trial record.
-/

def pgwContextStale : Nat := 0

def pgwContextReplay : Nat := 1

def pgwContextEmptyClaim (ctx : Nat) : Bool :=
  ctx = 0

def pgwContextAcceptBinding (declared replayed : Nat) : Bool :=
  declared = replayed

def pgwContextAcceptCount : Nat :=
  (if pgwContextAcceptBinding 0 0 then 1 else 0) +
    (if pgwContextAcceptBinding 0 1 then 1 else 0) +
    (if pgwContextAcceptBinding 1 0 then 1 else 0) +
    (if pgwContextAcceptBinding 1 1 then 1 else 0)

theorem pgwContext_codes_differ : pgwContextStale ≠ pgwContextReplay := by
  decide

theorem pgwContext_empty_claim_on_stale : pgwContextEmptyClaim pgwContextStale = true := by
  decide

theorem pgwContext_empty_claim_on_replay : pgwContextEmptyClaim pgwContextReplay = false := by
  decide

theorem pgwContext_binding_refuses_stale :
    pgwContextAcceptBinding pgwContextStale pgwContextReplay = false := by
  decide

theorem pgwContext_binding_accepts_match :
    pgwContextAcceptBinding pgwContextReplay pgwContextReplay = true := by
  decide

theorem pgwContext_accept_count : pgwContextAcceptCount = 2 := by
  decide

#print axioms pgwContext_codes_differ
#print axioms pgwContext_empty_claim_on_stale
#print axioms pgwContext_empty_claim_on_replay
#print axioms pgwContext_binding_refuses_stale
#print axioms pgwContext_binding_accepts_match
#print axioms pgwContext_accept_count
