import KernelReflectionBisection

/-!
Finite arithmetic reflection of the B1 250-interval fixture. The Python regression
`test_b1_receipt_matches_reflected_interval_fixture` binds the persisted JSON bytes
and coordinates to this data. This checks overlap, endpoints and declared margin
arithmetic; it supplies no matrix residual, derivative or classification evidence.

AuthorityEffect: None.
-/
namespace MUB.KernelReflectionB1Intervals

open MUB.KernelReflectionBisection

def receiptSha256 : String :=
  "e747e53283a73c4ce18485631fd4d5f36e0cdc4269006f53ee9458dee7aff05f"

def lower : QRat := ⟨1, 180⟩
def upper : QRat := ⟨59, 180⟩
def radius : QRat := ⟨1, 1000⟩
def epsilon : QRat := ⟨37249, 90000⟩
def lipschitz : QRat := ⟨85, 9⟩
def margin : QRat := ⟨12133, 30000⟩
-- 1/180 + k * (59/180 - 1/180) / 249, with a common denominator.
def center (k : Nat) : QRat := ⟨249 + 58 * (k : Int), 44820⟩
def centers : List QRat := (List.range 250).map center

def checkFixture : Bool :=
  centers.length == 250 &&
  radius.pos && margin.pos && epsilon.pos && lipschitz.pos &&
  margin.le (epsilon.sub (lipschitz.mul radius)) &&
  (epsilon.sub (lipschitz.mul radius)).le margin &&
  ((center 0).sub radius).le lower &&
  upper.le ((center 249).add radius) &&
  centers.all (fun t => (0 < t.den) && lower.le t && t.le upper) &&
  (List.range 249).all (fun k =>
    (center k).lt (center (k + 1)) &&
    ((center (k + 1)).sub (center k)).le (radius.add radius))

set_option maxRecDepth 8192 in
set_option maxHeartbeats 800000 in
theorem b1_interval_fixture_accepted : checkFixture = true := by rfl

#print axioms b1_interval_fixture_accepted

end MUB.KernelReflectionB1Intervals
