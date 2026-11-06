# Construct outcome filters under stated closure rules and expose the tomography boundary

Base: `lean-v4-35` at `3b50a1a980fa8535590356a65ff82b1d682dac29` (PR 144).
AuthorityEffect: None. The canonical derivation DAG is unchanged.

Under the stated closure rules, selective testing followed by preparation
constructs positive, subnormalized
rank-one filters. On a generating rational positive cone, bounded globally
separating effects and available normalized preparations give an admitted
irreducible reset family. Product-test resets also have an explicit pullback
formula, but their global irreducibility is equivalent to tomography. For global
resets, product-observation descent already contains the missing tomography
claim. These results identify which parts follow from operational closure and
which part still requires an additional principle.

## Claim triple

1. **Construction under stated closure rules.** Available normalized positive
   preparations, bounded globally separating effects, a generating rational cone,
   and sequential admission construct a family with the explicit conjunction
   **admitted ∧ positive/subnormalized ∧ irreducible** (`normalized_reset_family`).
   These are supplied operational premises, not consequences of primitive difference.
2. **Product closure without irreducibility.** Product-test resets descend through
   calibrated observation, but can retain a nonzero hidden kernel. Concrete
   orthant witnesses satisfy positivity and admission while irreducibility fails.
3. **Tomography boundary.** Irreducibility of calibrated product resets, and descent
   of all globally separating resets with visible normalized output, are each
   equivalent to injectivity. They reformulate the missing separation condition.

The Lean `orthant` and `canonicalAdmission` constructions instantiate the ordered
carrier and closure rules. `orthant_reset_family` discharges their hypotheses.
`product_reset_boundary`, `global_reset_boundary`, and
`classical_product_reset_boundary` exhibit the negative and positive sides;
`product_effects_not_separating` isolates the missing effect hypothesis.

## Construction from preparation and testing

Let V be a rational vector space with a supplied positive cone C and a linear
normalization functional u, nonnegative on C. A normalized preparation p lies in
C with u(p)=1. An allowed effect e satisfies 0 <= e(x) <= u(x) on C. Define

    P_p(a) = a p,    T_(p,e)(x) = e(x) p = (P_p composed with e)(x).

`SequentialAdmission` states the operational rule that an admitted test followed
by an admitted preparation is admitted. `reset_is_sequential` and
`reset_admitted` construct the family using that rule. `reset_outcome_filter`
proves positivity and u(Tx)<=u(x); `outcome_filter_comp` proves these properties
survive sequential composition. Positive linear maps are not automatically
classified as physically available or completely positive.

## Conditional irreducibility of global resets

Assume the positive cone spans V and the admitted bounded global effects
separate V: if every e_j(x)=0, then x=0. `normalization_faithful` derives that a
positive x with u(x)=0 must vanish. It follows that each nonzero positive vector
is a positive multiple of a normalized preparation, so those preparations span
V (`normalized_preparations_span`). Faithful normalization is thus derived in
the complete family theorem, not a separate assumption there.

For any spanning family p_i and separating family e_j, the filters p_i e_j act
irreducibly. If an invariant subspace contains x!=0, some e_j(x)!=0. Applying
p_i e_j and rescaling puts every p_i in that subspace, hence the entire V.
This is `resets_irreducible`, over any field. `normalized_reset_family` combines
this argument with rational positivity and sequential admission, using all
normalized positive preparations. That canonical index set need not be finite;
the general theorem also applies to finite spanning/separating families when
those are supplied. The finite fixtures below use such families.

## Product test pullbacks and the hidden subspace

Let M:V->C_obs be product observation. For a test e=f composed with M,

    M T_(p,e)(x) = f(Mx) M(p),

so the observed action is L(c)=f(c)M(p). This proves pullback closure for arbitrary
output preparations without assuming product-test separation. Such a reset
annihilates every x in ker M. Identity, composition, addition and scalar closure
of descending generators preserve ker M (`circuits_preserve_hidden`). The
latter is algebraic closure; arbitrary sums/scalars need not remain physically
admitted or subnormalized. A repeated outcome can exceed the normalization
bound, as the exact tests demonstrate.

For a calibrated M R=id and a nonempty finite coordinate index I, define
T_ij=R E_ij M. Its k-th product test is delta_(k,i) times the j-th input test.
`product_reset_formula` identifies it as preparation R(delta_i) after test
pi_j M. `product_resets_irreducible_iff` proves

    Irreducible({R E_ij M})  <=>  M is injective.

This is an algebraic theorem. Calibrated dual frame vectors/tests can be signed;
their physical positivity and availability require the hypotheses above and
do not follow merely from calibration.

## The global reset circularity boundary

Fix one preparation p and a coordinate functional q with q(Mp)=1. Then
`reset_descent_iff_effect_factor` proves

    exists L, M T_(p,e) = L M  <=>  exists f, e = f M.

For the forward implication, f=q composed with L. For the reverse, use
L(c)=f(c)M(p). With a calibrated observation and globally separating effects,
`global_reset_descent_iff_tomography` consequently proves

    all these global resets descend through M  <=>  M is injective.

Assuming arbitrary global measure-and-prepare operations descend would therefore
supply tomography itself. The visibly normalized output condition is essential:
a zero output preparation descends even for an effect that does not factor.
This obstruction concerns the reset route and the stated closure rules; it does
not exclude a different operation family justified by stronger primitives.

## Exact finite controls

All four examples use rational entries and the ordinary nonnegative coordinate
cone, with normalization given by the sum of coordinates. Doubled observations
are M=[I I] with R=(I,I)/2. Each filter is stored and checked as p_i e_j.

| Family | State dimension | Preparation span | Effect span | Filter span | Descent | Hidden dimension |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| Classical product resets | 4 | 4 | 4 | 16 | yes | 0 |
| Doubled calibrated resets | 8 | 4 | 4 | 16 | yes | 4 |
| Doubled resets with all basis preparations | 8 | 8 | 4 | 32 | yes | 4 |
| Doubled resets with global basis tests | 8 | 8 | 8 | 64 | no | 4 |

The third row shows that spanning preparations and positive outcome filters do
not remove hidden directions when only product tests are used. The fourth gives
an irreducible family that violates descent: a protected first-block test
separates states with identical product coordinates. Lean additionally proves
the scalar doubled reset kills a nonzero hidden vector and the protected reset
cannot descend (`doubled_reset_kills_hidden`, `doubled_protected_reset_no_descent`).
The 623 filter mutations and 277 inherited tomography mutations are
**fixture-integrity checks**, not semantic refutations of all alternative models.
Separate Python and Rust semantic tests accept valid asymmetric calibrations,
exhibit proper invariant subspaces, and distinguish non-separating from separating
effect families. Python computes exact rational ranks. Rust
checks the same certificate using nonzero orthogonal Gram witnesses for the
preparations, effects and reset operators, independently of Gaussian elimination.
Finite full operator span is a sufficient irreducibility certificate, not its
definition; reducible cases have an explicit proper nonzero invariant kernel.

## Remaining assumptions and next obligation

The construction supplies neither the field-linear carrier nor positive cone,
normalization, global effect separation, preparation availability, or sequential
admission from primitive difference. It establishes the consequences of those
explicit operational rules. Product calibration is separately supplied for the
tomography equivalences. PR 138's dimension-family and positive-parameter inputs
remain unchanged; no complex-field classification or tensor-cone closure is
claimed. Wigner reconstruction is outside this change.

The remaining task is to justify an operation family and its product-test
closure by a principle that independently rules out hidden sectors. This work
proves that freely adding global resets and assuming their descent is circular.
A successful next step must expose the additional principle or provide a
countermodel; neither quotienting away protected questions nor closing the
product-reset algebra discharges it.

## Replay and source custody

Run from the repository root, with a new output directory:

```powershell
py -3.12 -X utf8 dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/replay.py --output <new-directory>
```

`source_pins.json` binds the complete inherited source set and the new proof,
checker, construction, tests, metadata and companion records. `verified/receipt.json`
is the acceptance record. The replay builds and freshly elaborates the Lean
module, audits every listed headline's axioms, runs three Python modules and the
entire finite-probability Rust library, reconstructs the candidate byte-for-byte,
and checks the DAG, synchronization, contracts and whitespace. This is a focused
suite, not all tests in the repository. `attempts/` retains compiler repair and
temporary-directory failure evidence. No historical run or review is resealed.


Follow-up custody: current-source checks and the claim corrections are in
`../../reviews/20261021T210045Z_claim_boundary_fixes/`. Historical candidate bytes,
pin envelopes and receipts remain unchanged and can be replayed at their recorded
commits. This README and the proof/test sources now have a new validation record.
