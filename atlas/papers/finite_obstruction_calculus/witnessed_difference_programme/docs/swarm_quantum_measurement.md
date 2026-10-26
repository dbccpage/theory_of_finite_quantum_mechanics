# CH19-O04: repeatability and complete declared measurement replay

**Scope:** finite instruments over the Gaussian rationals, exact operational
replay, and explicit documentary traceability data. **AuthorityEffect: None.**

The remaining finite adapter obligations now have an exact criterion and a
concrete native path through registration, witness, accepted observation,
calibration, numeric measurement, and a checked documentary hierarchy. The
instrument, initial state, selected event, indication map, error model,
documents, and observation context are independently supplied inputs. The
checker recomputes against those inputs; no candidate receipt is its own
problem statement.

This result does not select the Born rule, identify the apparatus realized by a
laboratory, authenticate a document or reference standard, supply evaluator
standing, prove awareness, infer a confidence level, or grant authority.

## Exact outcome-repeatability theorem

Let a finite instrument on a nonzero finite-dimensional complex carrier be

\[
\mathcal M_o(\rho)=\sum_a K_{oa}\rho K_{oa}^{\dagger},\qquad
\sum_{o,a}K_{oa}^{\dagger}K_{oa}=I.
\]

The input and output carriers are the same, and all outcome groups and Kraus
operators are declared. Empty outcome groups are permitted. Probabilities and
sequential composition are the declared trace readout and CP-map composition.
For two immediately consecutive uses of this *same* instrument, define

\[
p(o,j\mid\rho)=\operatorname{tr}\bigl(\mathcal M_j(\mathcal M_o(\rho))\bigr)
=\sum_{a,b}\operatorname{tr}\bigl(A_{ojab}\rho A_{ojab}^{\dagger}\bigr),
\quad A_{ojab}=K_{jb}K_{oa}.
\]

The instrument is outcome-repeatable on every density operator exactly when

\[
\boxed{K_{jb}K_{oa}=0\quad\text{for every }j\ne o\text{ and every }a,b.}
\]

**Sufficiency.** Every switching joint probability vanishes under the boxed
condition. Trace preservation of the second measurement gives
\(\sum_j p(o,j\mid\rho)=\operatorname{tr}\mathcal M_o(\rho)\).
Consequently \(p(o,o\mid\rho)=p(o\mid\rho)\); conditional on any first event
with \(p(o\mid\rho)>0\), the probability of repeating that outcome is one.
Impossible first events require no normalized conditional state.

**Necessity.** Take the strictly positive density \(\rho_*=I/d\). Repeatability
implies, for \(o\ne j\),

\[
0=p(o,j\mid\rho_*)
=\frac1d\sum_{a,b}\operatorname{tr}(A_{ojab}^{\dagger}A_{ojab})
=\frac1d\sum_{a,b,r,c}|A_{ojab}[r,c]|^2.
\]

Every term is nonnegative, so each entry of each cross-outcome product is zero.
This argument includes all states, including those with complex or irrational
entries: the exact Gaussian-rational computation decides the operator
criterion itself. The single full-rank density is a complete separating
certificate because of positivity, rather than a collection of sampled states.

A nonzero cross product supplies an explicit counterexample: the exact joint
probability on \(I/d\) is strictly positive, hence its first-event probability
is positive and its repeat conditional probability is smaller than one.

An equivalent range condition is
\(\operatorname{ran}K_{oa}\subseteq\ker(I-E_o)\), where
\(E_o=\sum_aK_{oa}^{\dagger}K_{oa}\).
The boxed condition gives \(E_jK_{oa}=0\) for \(j\ne o\), and completeness
then gives \(E_oK_{oa}=K_{oa}\). Conversely, that last identity makes
\(K_{oa}^{\dagger}(I-E_o)K_{oa}=0\); the positive Gram sum
\(\sum_{j\ne o,b}(K_{jb}K_{oa})^{\dagger}(K_{jb}K_{oa})\) is zero, forcing
each cross product to vanish.

### Two necessary distinctions

Outcome-repeatability does **not** require idempotence of the state-update map.
A one-outcome unitary instrument is repeatable as an outcome rule while its
state can rotate again on every application. The native fixture uses a
Gaussian-rational real rotation with coefficients \(3/5,4/5\); its first and
second post-states differ exactly.

Nor does repeatability force every POVM effect to be a projection. In dimension
three let \(c=(1+i)/2\), \(|c|^2=1/2\), and choose the grouped operators

\[
K_{00}=|0\rangle\langle0|,\quad K_{01}=c|0\rangle\langle2|,\qquad
K_{10}=|1\rangle\langle1|,\quad K_{11}=c|1\rangle\langle2|.
\]

They are complete, and all cross-outcome products vanish. Yet
\(E_0=\operatorname{diag}(1,0,1/2)\),
\(E_1=\operatorname{diag}(0,1,1/2)\), so \(E_0^2\ne E_0\).
The transient third direction is sent into the unit-eigenvalue subspace of the
selected effect. On input \(|2\rangle\langle2|\), each event has probability
\(1/2\), and the selected event then repeats with probability one.

Conversely, the projective Lüders instrument and
\(K_o=|0\rangle\langle o|\) have the same projective effects but different
repeatability. The latter switches outcome 1 to outcome 0; on \(I/3\) the joint
switching probability is exactly \(1/3\). Thus the complete instrument, rather
than its POVM alone, is the required repeatability input.

## Native ownership and replay path

| Operation | Mathematical/data owner |
| --- | --- |
| Exact matrix products, adjoints, positive density validation, Kraus completeness, CP outcome maps | `omega_quantum_physics::exact_hermitian`, `exact_channel`, `exact_instrument` |
| Cross-outcome criterion and exact switching witness on `I/d` | `omega_quantum_physics::instrument_repeatability` |
| Ordered affine error propagation and rational enclosures | `omega_measurement::affine_calibration` and `omega_kernel::interval` |
| Explicit rooted documentary graph and additive declared contribution total | `omega_measurement::documentary_traceability` |
| Exact reported-value and unit carriers | `omega_measurement::{MeasurementValue, UnitSpec}` |
| Actual problem binding, WDP registration/witness/observation ladder, complete packet receipt replay | `omega_wdp::measurement_packet` with existing instrument/calibration adapters |

`QuantumMeasurementProblem` declares the validated instrument and state,
selected outcome, one indication per outcome, mark retention, interaction
poles/carrier, evaluator identity/status/standing, ordered calibration packet,
calibration evaluator/scale binding, affine indication map, measurand,
numeric scale/unit/resolution, correction, stated uncertainty, documentary
graph, artifact provenance, and an explicit repeatability requirement.

`register_instrument_problem` recomputes the instrument probability and
post-state binding on those actual inputs and compares the retained mark with
the exact expected record. A zero-probability event is refused. Next,
`witness_instrument_registration` compares a separately supplied re-access
artifact with retained data; `accept_instrument_observation` checks the
interaction carrier, distinct poles, Accept status, evaluator identity and
declared accepting standing. Separate typed records preserve each stage.

The calibration map must compose to the exact declared value map and raw
result. Its input center is the retained indication; calibration scale and
evaluator identities must match the measurement's declared scale and accepted
observation. A required repeatability property is checked by the quantum owner;
when repeatability is not requested, the packet makes no repeatability claim.
Rectangular carrier changes are refused by the same-instrument criterion and
would need a separately declared second instrument.

Every intermediate enclosure is replayed. If its final radius is \(r_f\), the
packet requires the stated calibration uncertainty \(u\ge r_f\). With exact
correction \(c\) and the documentary additive bound \(U\), it records

\[
\text{corrected center}=x_f+c,\qquad
\text{replayed radius}=r_f+U,\qquad
\text{advertised combined bound}=u+U.
\]

The corrected nominal value must lie on the declared resolution grid. The
native adapter also requires its entire replayed enclosure to fit in the
declared scale. It performs no rounding. These are deterministic conditional
enclosures; neither independence nor a distribution of stage errors is assumed.

The complete receipt binds every actual input. `verify_quantum_measurement`
recomputes the entire ladder and compares all records, calibration states,
graph data, reported values, enclosures, and digests. `refresh_digest` performs
content hashing only, so freshly rehashed false probabilities, missing
post-state bindings, false re-access/evaluator fields, altered intermediate
enclosures, and false final native values remain rejected.

## Documentary graph contract

A supplied graph is a finite directed graph from this calibration packet to a
named terminal reference. Every edge explicitly names source, target,
document, result unit, and a nonnegative exact uncertainty contribution. The
measurement owner checks:

1. nonempty graph, nonempty identities/documents and well-defined rational terms;
2. no duplicate documentary edge, no directed cycle and no disconnected component;
3. every branch is reachable from the calibration origin and ends at the one
   declared terminal reference;
4. every contribution is already expressed in the measurement's declared unit.

The exact additive total sums the declared edge contributions. If a caller
asserts an error decomposition into terms bounded by those contributions, the
triangle inequality gives that total as an upper bound. Without that extra
model assumption, it is only documentary arithmetic. Diamond-shaped support
graphs are permitted; summing every declared edge is the explicit conservative
convention, rather than an inferred stochastic combination rule.

The graph validates the *shape and declared content* of a hierarchy. It does
not check a laboratory's standards, a document's authenticity, certificates,
signatures, or real apparatus realization. Artifact provenance is a separate
field and cannot stand in for this graph.

## Paper Python and Lean evidence

`code/witnessed_difference/quantum_measurement_replay.py` independently mirrors
the square grouped Gaussian-rational instrument algebra on finite nonnegative
mixtures. It binds the exact instrument outcome/post-state record into a
retained mark and reuses the paper's actual `Registration`, witness,
`AcceptedObservation`, `Measurement`, and `measurement_replay` APIs. Thus their
existing scale, calibration-evaluator, uncertainty, and documentary-chain
validation executes directly. It rejects a mathematically false instrument
record even when the retained mark, witness, observation and ordinary
measurement have all been consistently rebuilt around that false record.
Python uses the existing chain-shaped documentary hierarchy; the native owner
also supports checked finite DAGs.

`lean4/WitnessedDifference/InstrumentRepeatability.lean` compiles six standalone
theorems without admitted proofs. It formalizes finite Gaussian-rational norm
zero detection (positive common denominators), finite nonnegative zero sums,
matrix-entry zero separation, and the requirement that every required
cross-outcome product appear in the encoding. It does not claim to formalize
matrix products, positive trace identities, or the entire all-state theorem.
The latter has the explicit mathematical proof above and native finite evidence.

## Executed validation

- Quantum owner: **4 passed** (`instrument_repeatability` integration target).
- Measurement owner: **3 passed** (documentary graph native tests).
- WDP complete packet: **7 passed** (`quantum_measurement_packet` target).
- Paper Python mirror: **5 passed** (`test_quantum_measurement_replay.py`);
  **9 passed** when the existing composed measurement replay regression is included.
- Lean: **6 compiled theorems**, no `sorry`, `admit` or new axioms. Printed
  dependencies are the existing Lean foundations (`propext`, `Classical.choice`,
  `Quot.sound`).

The common end-to-end fixture produces event probability \(1/2\), raw value
\(-6\), corrected value \(-11/2\), final calibration radius \(351/1000\),
documentary sum \(3/10\), replayed corrected radius \(651/1000\), and advertised
combined bound \(4/5\). Rust and the independent paper Python agree exactly.

The finite declared-model adapter is now implemented. Actual physical
apparatus realization, external document authenticity, and a selected physical
measurement law remain additional evidence or premises, not stalled algebraic
derivations and not consequences of the receipt checker.
