# Admitted primitive-to-witness floor

**Status.** Explicit admission for `GEN-WDP-O01`. The register row stays
`OPEN FOUNDATIONAL OBLIGATION`. This note admits the carrier, signature,
irreflexivity law, and no-form challenge-generation floor named by that row.
It does not retag the row, and it does not prove a stronger floor.

**Witness.** `gen-wdp-o01-admission-floor`,
`problem_sha256` `5317764cd6eace9c04d85bdc68109402c64d7ae5b3d3f4704791a594e7674d86`,
receipt
[`evidence/gen_wdp_o01_admission_floor_receipt.json`](../../evidence/gen_wdp_o01_admission_floor_receipt.json).
The checker is
[`code/witnessed_difference/gen_wdp_o01_admission_floor.py`](../../code/witnessed_difference/gen_wdp_o01_admission_floor.py).

## 1. The admitted object

The source anchor is the `GEN-WDP-O01` row of
[`genesis_bridge_register.md`](../genesis_bridge_register.md), together with
[the primitive floor](../primitive_admission_and_transport.md). An exhibited
cut supplies four inputs:

- a carrier;
- a binary signature `R`;
- designated endpoints and the instance `R(a,b)`;
- the law `forall x, not R(x,x)`.

These are admissions. The opaque glyph `<>` supplies none of them. Supply
leaves the admitted components unchanged. Admitting that same token twice
under dedup still yields one datum, no form, no orientation, and no law.

## 2. Finite checks of the cut

On the carrier `{0,1}` both the forward instance `R(0,1)` and the reverse
instance `R(1,0)` are irreflexive. The law retains both orientations and
selects neither.

On a singleton the full relation has an instance and breaks the law. The
empty relation keeps the law and has no instance. Neither relation is a cut,
so a subsingleton carrier does not support one.

Sending both endpoints of the forward cut to one image point forces the
instance onto a diagonal. No image relation can preserve that instance and
obey the law. The identity transport keeps the endpoints apart.

The declared unary and binary separation responses each have item cost 2.
Their declared arity costs are 1 and 2, so the arity comparison retains the
unary response. Those are declared prices. They are not the Genesis
cost-floor theorem, and these two responses are not an exhaustive language.

## 3. The admitted challenge-generation floor

The source anchors are
[the initial challenge floor](../source_replay_and_remaining_derivations.md)
and the all-arity section of
[`primitive_execution_refinement.md`](../primitive_execution_refinement.md).
This observational floor is not the irreflexive cut.

For two data and one separation requirement, with form arity at most 2, the
form-plus-instance responses whose mentioned data cover the edge are six:
the unary instances `(0)` and `(1)`, and the four binary instances, including
both diagonals. Each has item cost 2. The lexicographic item-then-arity
comparison retains the two unary responses. Because the diagonals remain
among the six, this floor does not choose irreflexivity.

A datum with no form does not separate the profiles. A form with no instance
does not separate them. A form with a uniform rule gives both data the same
profile.

On the named complete requirement graphs the minimum cover sizes are 1, 2,
and 3. The three-datum graph has six ordered binary minimum responses. The
four-datum graph has no covering instance of arity at most 2, and twenty-four
ordered ternary minimum responses at arity 3. The checker enumerates those
three graphs. It does not replace the written all-arity argument.

## 4. What stays unproved

A stronger floor still needs a theorem and a falsifier. Complete
source-specific challenge-generation refinement across all declared regimes
stays open. The observational floor does not choose the irreflexivity law.
The declared prices are not the Genesis cost-floor theorem and do not exhaust
every language. This note does not prove a machine-checked refinement of the
concrete Python or Rust programs, and it does not prove generated-token
freshness. No topology, kernel, or schedule is introduced.
