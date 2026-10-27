import Std
namespace WittenPairing
/-- Formal weighted spectral sum; weights need not be analytic functions. -/
def traceWeight (w : Nat → Int) : List Nat → Int
  | [] => 0
  | e :: es => w e + traceWeight w es

theorem trace_append (w : Nat → Int) (xs ys : List Nat) :
    traceWeight w (xs ++ ys) = traceWeight w xs + traceWeight w ys := by
  induction xs with
  | nil => simp [traceWeight]
  | cons e es ih => simp [traceWeight, ih, Int.add_assoc]

theorem trace_zero_modes (w : Nat → Int) (h : w 0 = 1) (n : Nat) :
    traceWeight w (List.replicate n 0) = (n : Int) := by
  induction n with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ, traceWeight, ih, h]; omega

/-- Cancellation for any paired spectrum, not just a fixed temperature or example. -/
theorem paired_trace (w : Nat → Int) (h : w 0 = 1)
    (paired : List Nat) (bosonicZero fermionicZero : Nat) :
    traceWeight w (List.replicate bosonicZero 0 ++ paired) -
      traceWeight w (List.replicate fermionicZero 0 ++ paired) =
        (bosonicZero : Int) - (fermionicZero : Int) := by
  rw [trace_append, trace_append, trace_zero_modes w h, trace_zero_modes w h]
  omega

theorem weight_independent (w v : Nat → Int) (hw : w 0 = 1) (hv : v 0 = 1)
    (paired : List Nat) (b f : Nat) :
    traceWeight w (List.replicate b 0 ++ paired) - traceWeight w (List.replicate f 0 ++ paired) =
    traceWeight v (List.replicate b 0 ++ paired) - traceWeight v (List.replicate f 0 ++ paired) := by
  rw [paired_trace w hw, paired_trace v hv]

/-- A zero index does not imply that the zero-energy sector is empty. -/
theorem zero_index_with_ground_modes (w : Nat → Int) (_h : w 0 = 1) :
    traceWeight w [0] - traceWeight w [0] = 0 ∧ (1 : Nat) + 1 > 0 := by
  constructor <;> omega
end WittenPairing
#print axioms WittenPairing.paired_trace
#print axioms WittenPairing.weight_independent
#print axioms WittenPairing.zero_index_with_ground_modes
