# Continuing S(n) inside WDP

This is a reusable work specification, not a record of a completed derivation.
It does not request a new blind experiment or reopening the frozen source.

Read [the source correspondence](../source_correspondence.md), [sn.md](../sn.md),
[the level index](../levels/README.md), and the actual canonical Rust primitives.
Retain `<>` literally in the event history. Keep supplied opaque tokens separate
from admissions and from their later parsed representations.

For the next construction:

1. State the admitted input, the protected question and the permitted edits.
2. Construct the candidate using the primitive owner; preserve the full history.
3. Declare any incidence, coefficients, equality, topology or probability law
   needed to interpret it mathematically.
4. Prove the preservation equations and test both a valid witness and a
   counterexample to a plausible wrong correspondence.
5. Record unresolved assumptions explicitly. Move the result to its mathematics
   crate once its operations and continuation agree with that mathematical model.

WDP is the working location for these bridges. The intended durable primitive
owner is `omega_genesis` (currently `omega_ooutwire_primitives`). A future
language should compile to these same constructors and evaluators.

Use the source cost-two theorem under its actual response grammar. Do not
replace it with a claim that a binary edge or two witnesses is universally
required. Do not infer a stage transition from the fixed ledger exercise or
mistake a parsed string for a verified homology, confluence or authority receipt.
Report executed checks with their exact scope; leave future theorems as future
obligations rather than preloading their desired conclusions.
