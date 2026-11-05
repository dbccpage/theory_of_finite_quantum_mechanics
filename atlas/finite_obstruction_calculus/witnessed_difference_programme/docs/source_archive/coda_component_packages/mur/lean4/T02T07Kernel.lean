import D01D02D03Records

/-!
# CODA-MUR: Bicategory and 2-cell kernel

**AuthorityEffect:** None.
Status: OPEN.
-/

namespace CODA_MUR

/-- 2-cell modification structure for representation transport. -/
structure TransportTwoCell where
  source_id : String
  target_id : String
  certified : Bool

end CODA_MUR
