/-
Campaign narrow case for PGW-DECLARED-INPUT-FLOOR.
Two named inputs and four stake-only carriers.
The attempt-two search is not replayed.
AuthorityEffect: None.
-/

namespace CampaignPgwDeclaredInputFloor

inductive Input where
  | stake
  | stream
deriving DecidableEq, Repr

def vocabulary : List Input := [.stake, .stream]

def count (stake stream : Bool) : Nat :=
  (if stake then 1 else 0) + (if stream then 1 else 0)

/-- Four carriers. Each pair is (declares stake, declares stream). -/
def engines : List (Bool × Bool) :=
  [(true, false), (true, false), (true, false), (true, false)]

def rounds : Nat := 15
def guard : Nat := 250
def dataBound : Nat := 4
def itemBound : Nat := 2

def floorReading : Bool :=
  engines.all (fun p => decide (2 ≤ count p.1 p.2))

def oneInputReading : Bool :=
  engines.any (fun p => decide (count p.1 p.2 = 1))

theorem vocabulary_is_two :
    vocabulary = [.stake, .stream] ∧ vocabulary.length = 2 ∧
      Input.stake ≠ Input.stream := by
  decide

theorem four_engines : engines.length = 4 := by
  decide

theorem each_declares_stake_not_stream :
    engines.all (fun p => decide (p = (true, false))) = true := by
  decide

theorem each_count_is_one :
    engines.all (fun p => decide (count p.1 p.2 = 1)) = true := by
  decide

theorem one_below_two :
    count true false = 1 ∧ count true true = 2 ∧
      count true false < count true true := by
  decide

theorem readings_disagree :
    floorReading = false ∧ oneInputReading = true := by
  decide

theorem declared_bounds :
    rounds = 15 ∧ guard = 250 ∧ dataBound = 4 ∧ itemBound = 2 := by
  decide

theorem empty_carrier_is_not_among_the_four :
    count false false = 0 ∧
      count false false < count true false ∧
      engines.all (fun p => decide (p ≠ (false, false))) = true := by
  decide

#print axioms vocabulary_is_two
#print axioms four_engines
#print axioms each_declares_stake_not_stream
#print axioms each_count_is_one
#print axioms one_below_two
#print axioms readings_disagree
#print axioms declared_bounds
#print axioms empty_carrier_is_not_among_the_four

end CampaignPgwDeclaredInputFloor
