# Curriculum: 002 S(n)

**AuthorityEffect:** None.

Eight lessons, about five hours of study including the video. This strand puts
stage labels S(0) to S(6) on the Genesis challenges, keeps two registers per
stage, and then teaches a set of small exact examples. The labels are a
bookkeeping choice; the examples are mathematics you can recompute.

**Prerequisite:** [`001_oegen`](../001_oegen/curriculum.md).
**Next strand:** [`003_oemssn`](../003_oemssn/README.md).
**Read first:** the "Known divergences" section at the end of [`README.md`](README.md).

Three symbols that look alike and are different: S(n) is a Genesis stage label
here; S_n is the symmetric group; MSS-n is an entry in the 010 atlas.

---

## Lesson 1. Two Boxed Laws and the one-way arrow

**After this lesson you can** state the two laws and explain why a model of a
stage cannot create the next stage.

**Read:** [source and checking boundaries](sn.md#1-source-representation-application-and-checking).

- "S(n+1) may contain only structure forced by an unresolved Genesis
  obstruction at S(n)."
- "A mathematical realization R(S(n)) has no authority to extend S(n)."
- A property proved in a model returns to Genesis only through an explicitly
  proved faithful reflection bridge.

These are design rules. No checker enforces them; their value is that they tell
you which arguments are not allowed.

**Exercise.** Someone shows that a graph model of S(3) has a Ramanujan
eigenvalue bound and concludes S(4) must contain spectral structure. Which law
does this break? *Answer:* the second: a property of a realization does not
extend the stage.

## Lesson 2. The stages, read against the source

**After this lesson you can** describe S(0) to S(3) in 19L57G1's own terms.

| Stage | Source event | Source result |
| --- | --- | --- |
| S(0) | the seed `<>` | inertia: nothing derivable (`genesis_underivable`) |
| S(1) | supply `<a>` | supply is not admission (`supply_no_op`) |
| S(2) | reading L admits `<a>` and the opaque whole `<ab>` | collapse (`R2L_collapsed`, `R2F_collapsed`) |
| S(3) | require `<a>` and `<ab>` to be separable | cost-two floor, tied minima (`cost1_insufficient_general`) |

The folder's flat grammar parses `<ab>` as two glyphs. This is a later
interpretation; in the source, `<ab>` is one opaque datum, and glyph identity,
component count and order are unavailable inside the regime.

**Exercise.** Why does reading `<ab>` as a pair import structure? *Answer:* a
pair has two components and an order; the regime has no rule that sees inside
an inscription.

## Lesson 3. Two registers: active obstructions and history

**After this lesson you can** separate W_n, s_n and H_n, and say what kind of
claim s = (0,1,1,1,0,1,1) is.

- W_n is the set of currently unresolved obstructions, s_n = |W_n|; H_n is the
  growing history of receipts, H_n = H_{n-1} ∪ C_n.
- Birth and death: D_n⊆W_{n-1} and B_n disjoint from W_{n-1} minus D_n give W_n = (W_{n-1} \ D_n) ⊔ B_n, so s_n = s_{n-1} − |D_n| + |B_n|.
- The sequence (0,1,1,1,0,1,1) describes one prescribed challenge history
  (see [the ledger scope](source_correspondence.md#prescribed-ledgers)). It is not a theorem, and 19L57G1 says a collapsed
  pair becomes an obstruction only when a separation requirement is declared.

**Exercise.** At S(4), s_4 = 0 while |H_4| = 5. What does that mean? *Answer:*
nothing is currently unresolved, but five receipts have been issued; closing an
obstruction does not erase its history.

## Lesson 4. Endpoints, witnesses and the pointed germ D_2

**After this lesson you can** prove the endpoint lemma and separate endpoints
from witnesses.

- If R is irreflexive and R(a, b), then a ≠ b (`PrimDiff.irrefl_witness_ne`, no
  axioms). So every cut has exactly two distinct endpoints.
- One witness can be enough: `single_oriented_witness_consistent` has one
  witness from false to true and none back. Endpoints are 2; witnesses may be 1.
- D_2 is {0, 1} with one edge 0 → 1. Any related pair R(a, b) receives exactly
  one point-preserving map with f(0) = a, f(1) = b (`D2_initial_pointed`).
- Irreflexivity and orientation are declared inputs, not consequences of `<>`
  (WDP-CH01-P02). The folder's grammar does not enforce irreflexivity: `<a->a>`
  parses.

**Exercise.** Run
`py -3.12 omega_engine_education/documentation/002_oesn/code/sn_audit.py wire --profile sn-wire-v1 "<a->a>"`.
What does the result tell you? *Answer:* `syntax_accept: true`. The grammar is a
spelling check; irreflexivity must be checked separately.

## Lesson 5. Tagging, colouring and the cost of separation

**After this lesson you can** resolve observational collisions by tagging and
compute the minimum number of tag values.

- If q(a) = q(b), add a tag t with t(a) = 0, t(b) = 1 and observe q'(x) = (q(x), t(x)).
  The old observation is the first projection of the new one.
- Several demanded pairs make this graph colouring. For three mutually collapsed
  data with all three pairs demanded, three tag values are needed; with binary
  coordinates, 2^k ≥ 3 forces k ≥ 2 (`levels/level_10_spectral_epistemic_quarantine.md`).
- Compare 001: the first separation costs two items in the declare-then-assert
  grammar. Tagging is a different grammar with a different price.

**Exercise.** How many binary coordinates separate four mutually collapsed data?
*Answer:* 2, since 2² = 4.

## Lesson 6. Stage index is not Postnikov depth; lifts and partial retractions

**After this lesson you can** explain why S(n) is not a Postnikov tower and use
the typed retraction law.

- Postnikov truncations of one space keep π_0, so "empty, then a point" cannot be
  successive truncations of one space. Use two indices, P_j(ρ(S(n))).
- A section lift u_n: P_n ↪ P_{n+1} and a partial retraction
  r̂_n: P_{n+1} → P_n ⊔ {NON_DESCENT} satisfy r̂_n ∘ u_n = inl. New elements map to
  NON_DESCENT. This is the standard option-valued construction and is this
  folder's own; it does not come from 19L57G1.
- Proposal (AuthorityEffect: None): `lean4/SnOffImage.lean` adds the domain
  restriction of that law (accepted only on section images); see
  `docs/off_image_refusal_note.md`.
- Example: A = {a, b} ⊂ B ⊂ C = {a, b, c, d}; the composite retraction sends c and d
  to ⊥ and every element of A back to itself.

**Exercise.** Why is there no total function {a} → ∅ but there is a refusal-valued
one? *Answer:* the empty set has no elements to map a to; the option type adds
NON_DESCENT.

## Lesson 7. A circulation obstruction, two ways to minimise, and torsion

**After this lesson you can** compute the triangle obstruction, its ℓ1 and ℓ2
representatives, and a torsion example.

- Triangle edges (ab, bc, ca), d_0 rows (−1, 1, 0), (0, −1, 1), (1, 0, −1), edge data
  x = (1, 0, 0). The circulation I(x) = x_ab + x_bc + x_ca is 0 on every d_0 g, and
  I(x) = 1, so no potential g gives d_0 g = x. Conversely I(x) = 0 implies x is
  exact, so im(d_0) = ker(I).
- ℓ1: every residual has I(r) = 1, so ‖r‖₁ ≥ 1; attained by (1, 0, 0) and by ties
  such as (1/2, 1/2, 0); dual certificate y = (1, 1, 1).
- ℓ2: the unique minimiser is h = (1/3, 1/3, 1/3) with ‖h‖² = 1/3, from
  g = (0, 2/3, 1/3). Optimising chooses a representative; it does not remove the
  obstruction.
- Torsion: C_2 = ℤ —2→ C_1 = ℤ —0→ C_0 = ℤ has H_1 = ℤ/2 over ℤ and 0 over ℚ. The
  rational primitive 1/2 is not an integer repair.
- WDP's chapter on finite cochains, quotients and certificates is the canonical
  treatment of this kind of obstruction; read it next.

**Exercise.** Verify d_0 g + h = x for g = (0, 2/3, 1/3). *Answer:* d_0 g =
(2/3, −1/3, −1/3); adding h gives (1, 0, 0).

## Lesson 8. Observers, repair rank, and generate ≠ evaluate ≠ admit

**After this lesson you can** complete a defective observer and count real repair
progress.

- On ℚ³ with B = ker(I), the observer Q_bad(x) = x_1 hides z = (0, 1, 0). Adding I
  gives Q_complete(x) = (x_1, I(x)) with kernel {(0, t, −t)} ⊂ B. One coordinate is
  necessary and sufficient: the hidden part K/(K∩B) has dimension 1 (the kernel
  of Q_bad has dimension 2).
- Four vertices, five edges (ab, bc, ac, cd, da): cycle space dimension 2, cycles
  z_1 = (1, 1, −1, 0, 0) and z_2 = (0, 0, 1, 1, 1). Two independent faces give rank 2
  and H_1 = 0; two copies of z_1 give rank 1 and leave dim H_1 = 1. Receipt count
  is not progress; boundary rank is.
- Generating a candidate, evaluating it and admitting it are separate acts; an
  evaluator's report is not an authorization (GEN-WDP-03, 04, 10). This is the
  same separation PFP enforces between a candidate and the host's receipt.

**Exercise.** A swarm submits three repairs with boundaries z_1, z_2 and z_1 + z_2.
What is the repair rank? *Answer:* 2.

---

## What this strand does not claim

- That the S(0)-S(6) ladder or s = (0,1,1,1,0,1,1) is proved or derived.
- That S(4)-S(6), W_n, s_n, H_n or NON_DESCENT come from 19L57G1.
- That `<ab>` is a pair, or that supplying `<a>` admits it.
- That orbit closure is autonomous (it is a declared policy) or that OB-1 is proved
  (it is open).
- That S(n) is a Postnikov tower, or that the folder derives physics.
- That its tests or Lean files verify the ladder; they check syntax, codec round
  trips, model defaults and table facts.
