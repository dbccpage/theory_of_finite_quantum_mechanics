import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic

namespace QM.GOMC10

variable {DiagState : Type}

-- Theorem: A finite sequence of diagnostic updates (e.g., channel application, branch search)
-- cannot grant authority unless the final state explicitly passes the separate descent gate.
-- Thus, diagnostic closure is strictly firewalled from authority closure.
theorem closure_firewall_sequence
    (UpdateOp : DiagState → DiagState)
    (DescentGate : DiagState → Prop)
    (HasAuthority : DiagState → Prop)
    (update_is_firewalled : ∀ s, HasAuthority s ↔ DescentGate s)
    (s : DiagState) (n : ℕ) :
    HasAuthority ((UpdateOp^[n]) s) ↔ DescentGate ((UpdateOp^[n]) s) := by
  -- By the strict separation hypothesis, authority is identical to passing the gate
  exact update_is_firewalled ((UpdateOp^[n]) s)

-- Corollary: If the descent gate is permanently closed for a sequence of diagnostic states,
-- no amount of branch search or channel update will mint authority.
theorem permanent_firewall_blocks_authority
    (UpdateOp : DiagState → DiagState)
    (DescentGate : DiagState → Prop)
    (HasAuthority : DiagState → Prop)
    (update_is_firewalled : ∀ s, HasAuthority s ↔ DescentGate s)
    (s : DiagState) (n : ℕ)
    (h_closed : ∀ k, ¬ DescentGate ((UpdateOp^[k]) s)) :
    ¬ HasAuthority ((UpdateOp^[n]) s) := by
  intro h_auth
  have h_gate := (closure_firewall_sequence UpdateOp DescentGate HasAuthority update_is_firewalled s n).mp h_auth
  exact (h_closed n) h_gate

end QM.GOMC10
