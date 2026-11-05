import WitnessedDifference.BalancePreservingEdits
import WitnessedDifference.AmplitudeBridge
import WitnessedDifference.Boundaries
import WitnessedDifference.ClassicalCorner
import WitnessedDifference.ClassicalPackage
import WitnessedDifference.Composition
import WitnessedDifference.ComplexGrowth
import WitnessedDifference.Descent
import WitnessedDifference.Difference
import WitnessedDifference.EmpiricalModel
import WitnessedDifference.History
import WitnessedDifference.InstrumentAdapter
import WitnessedDifference.Interference
import WitnessedDifference.Measurement
import WitnessedDifference.Obstruction
import WitnessedDifference.PacketAdapter
import WitnessedDifference.ObserverResolution
import WitnessedDifference.PointedRelation
import WitnessedDifference.Probability
import WitnessedDifference.Routing
import WitnessedDifference.QuantumImports
import WitnessedDifference.SemiringTransport
import WitnessedDifference.Succession
import WitnessedDifference.Symmetry
import WitnessedDifference.ToleranceAdapter
import WitnessedDifference.ComponentReports
import WitnessedDifference.ComponentRepair
import WitnessedDifference.ComponentCompletion
import WitnessedDifference.ComponentQuantum

/-!
# Witnessed Difference

This root exports the bounded finite witness/observer/measurement spine. It
does not export a reconstruction theorem for any topic listed in
`WitnessedDifference.OPEN.Topic`. The `Obstruction` module adds the degree-1
obstruction window over `ℚ` and the repair quotient, and the
`ObserverResolution` module adds the observer kernel order and the
pigeonhole resolution limit. `PointedRelation` separates relatedness from
distinctness for a pointed relation; `Descent` adds the presentation-descent
obstruction and the retraction defect; `ComplexGrowth` adds restriction and
subdivision monotonicity of the repair cost; `Interference` adds the
second- and third-order interference identities for a biadditive pairing;
`ClassicalCorner` adds the classical corner of the §18.1 package: nonnegative
weights reduce reversible stochastic updates to permutations; `ℤ[i]` unitaries are monomial matrices (permutations with unit phases),
and finite localizations of the scalars end it. `EmpiricalModel` adds the typed
map from finite run tables to empirical models on a declared cover, and
`PacketAdapter` instantiates it with the measurement packets of Chapter 13.
`ClassicalPackage` extends the classical corner to stochastic updates and
classical instruments (`WDP-CH18-P07`, `WDP-CH18-P08`); `ToleranceAdapter`
adds the tolerant adapter and the two-context repair (`WDP-CH19-P06`,
`WDP-CH19-P07`); `Composition` adds the composition principle
(`WDP-CH19-P08` to `WDP-CH19-P10`); `AmplitudeBridge` adds gauge descent of
phase-blind readouts and the exponentiation obstruction (`WDP-CH19-P11`,
`WDP-CH19-P12`); and `InstrumentAdapter` adds the finite qubit instrument
adapter (`WDP-CH19-P13`, `WDP-CH19-P14`).
These modules use Mathlib, as do `ClassicalCorner`, `EmpiricalModel` and
`PacketAdapter`; the others use only Lean core.
-/
