import AdmitCore

/-!
# Admit import records

AuthorityEffect: None.

An import record names axioms, names a cost, and records whether conservativity
was proved. `coreHolds` reads only the regime. Writing a record does not make
`AdmitCore.Holds` true.
-/

namespace AdmitImport

inductive ConsStatus where
  | proved
  | openStatus

structure ImportRecord where
  name : String
  axiomsNamed : List String
  costName : String
  conservativity : ConsStatus

structure Packed where
  regime : AdmitCore.Regime
  imports : List ImportRecord

def coreHolds (p : Packed) (J : AdmitCore.Judg) : Prop :=
  AdmitCore.Holds p.regime J

def writeImport (p : Packed) (r : ImportRecord) : Packed :=
  { p with imports := r :: p.imports }

theorem write_import_iff (p : Packed) (r : ImportRecord) (J : AdmitCore.Judg) :
    coreHolds (writeImport p r) J ↔ coreHolds p J := Iff.rfl

theorem coreHolds_eq_regime (p q : Packed) (h : p.regime = q.regime) (J : AdmitCore.Judg) :
    coreHolds p J ↔ coreHolds q J := by
  unfold coreHolds
  rw [h]

/-- The two boxed laws of TFQ-0510, as a record. Not a core rule. -/
def snImport : ImportRecord where
  name := "S(n) two boxed laws"
  axiomsNamed := [
    "S(n+1) may contain only structure forced by an unresolved obstruction at S(n)",
    "a realization R(S(n)) does not extend S(n)"
  ]
  costName := "unpriced design rule from 002_oesn, not a 19L57G1 theorem (TFQ-0510)"
  conservativity := .openStatus

/-- MSS-N is an atlas, not S(n). TFQ-0528: MSS-2 is not S(2), and licensed depth is 0. -/
def mssnImport : ImportRecord where
  name := "MSS-N atlas"
  axiomsNamed := [
    "rows MSS-0 through MSS-100 are externally designed specifications",
    "MSS-2 is not S(2)",
    "licensed depth D is 0"
  ]
  costName := "unpriced atlas assumption (TFQ-0528); row count is not depth"
  conservativity := .openStatus

/-- The two regime fields this core does not store. TFQ-0378 names them. -/
def rulesImport : ImportRecord where
  name := "regime rules and requirements"
  axiomsNamed := ["rules component", "requirements component"]
  costName := "unpriced: named in TFQ-0378, no introduction rule in AdmitCore"
  conservativity := .openStatus

structure NonDerivability where
  label : String
  regime : AdmitCore.Regime
  judgment : AdmitCore.Judg
  absent : ¬ AdmitCore.Holds regime judgment

def apartOnEmpty : NonDerivability where
  label := "empty regime does not derive apart 0 1"
  regime := .empty
  judgment := .apart 0 1
  absent := AdmitCore.empty_not_apart

theorem import_is_not_a_core_derivation (r : ImportRecord) (rs : List ImportRecord) :
    ¬ coreHolds ⟨AdmitCore.Regime.empty, r :: rs⟩ (.apart 0 1) := by
  intro h
  exact AdmitCore.empty_not_apart h

theorem sn_import_does_not_derive_apart :
    ¬ coreHolds ⟨AdmitCore.Regime.empty, [snImport, mssnImport, rulesImport]⟩ (.apart 0 1) :=
  import_is_not_a_core_derivation snImport [mssnImport, rulesImport]

theorem named_nonderivable_apart : ¬ AdmitCore.Holds apartOnEmpty.regime apartOnEmpty.judgment :=
  apartOnEmpty.absent

end AdmitImport

#print axioms AdmitImport.write_import_iff
#print axioms AdmitImport.coreHolds_eq_regime
#print axioms AdmitImport.import_is_not_a_core_derivation
#print axioms AdmitImport.sn_import_does_not_derive_apart
#print axioms AdmitImport.named_nonderivable_apart
