import MajoranaCore
import BqnfSignPacket
import MubBalancedTable
import ExtensionCurvatureObstruction
import MasterClassification

open BqnfSignPacket
open MUB.MasterClassification
open MUB.ExtensionCurvatureObstruction
open MUB.BalancedTable

-- 1. BqnfSignPacket inhabitation of all 5 routes
def m_exact : SignPacketMetrics := ⟨true, false, 0, 0, false⟩
def m_invol : SignPacketMetrics := ⟨true, false, 0, 5, true⟩
def m_open : SignPacketMetrics := ⟨true, false, 2, 0, false⟩
def m_split : SignPacketMetrics := ⟨true, true, 0, 0, false⟩
def m_fail : SignPacketMetrics := ⟨false, false, 0, 0, false⟩

theorem bqnf_exact_witness : routePacket m_exact = TerminalRoute.ExactRepair := rfl
theorem bqnf_invol_witness : routePacket m_invol = TerminalRoute.ExactRepair := rfl
theorem bqnf_open_witness : routePacket m_open = TerminalRoute.OpenSignObstruction := rfl
theorem bqnf_split_witness : routePacket m_split = TerminalRoute.SplitBrainRefusal := rfl
theorem bqnf_fail_witness : routePacket m_fail = TerminalRoute.ClosureFailure := rfl

-- 2. MasterClassification inhabitations
def karlsson_witness : KarlssonParam := ⟨1, 1⟩
theorem karlsson_domain_witness : KarlssonDomain karlsson_witness := by
  dsimp [KarlssonDomain, karlsson_witness]
  norm_num

def fourier_witness : FourierDitaParam := ⟨1, 1, 1⟩
theorem fourier_domain_witness : FourierDitaDomain fourier_witness := by
  dsimp [FourierDitaDomain, fourier_witness]
  norm_num

-- 3. ExtensionCurvatureObstruction numerical bounds
theorem W_bound_verified : W < 1 := W_lt_one
theorem d6_floor_verified : 0 < Real.sqrt ((1 - W) * (5 / 6)) := d6_floor_pos

-- 4. MubBalancedTable checks
theorem table_rows_length : rows.length = 648 := row_count

-- 5. MajoranaCore F2CochainComplex trivial zero complex inhabitation
def zero_map (n m : Nat) : F2Map n m := {
  apply := fun _ => F2Vec.zero m
  linear_zero := rfl
  linear_add := fun _ _ => rfl
}

def zero_complex (n0 n1 n2 : Nat) : F2CochainComplex n0 n1 n2 := {
  d0 := zero_map n0 n1
  d1 := zero_map n1 n2
  nilpotent := fun _ => rfl
}

theorem zero_complex_is_exact (n0 n1 n2 : Nat) :
    is_exact (zero_complex n0 n1 n2) (F2Vec.zero n1) :=
  ⟨F2Vec.zero n0, rfl⟩
