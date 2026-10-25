Status: AI-drafted, awaiting human review.

# QCV-CONDITIONAL-VIABILITY-CERTIFICATE nonnegative backlog

The repair backlog of rates `lam`, `g`, and `mu = kappa * r`, from a rational initial value `q0`, is the sequence that adds `lam + g * mu - mu` each round and then replaces a negative value by zero. `BacklogBounded` means some constant bounds every round.

## The certificate

Assume `0 <= q0`, `g < 1`, `kappa > 0`, and `r` at least `lam / ((1 - g) * kappa)`. Assume an overhead function with `c(k) <= C` for every natural number `k`, and level errors `p(k) >= 0` with `max(C, 1) * p(0) < 1`. Assume that whenever that backlog predicate holds, `p(k + 1) <= c(k) * p(k)^2`.

The supply hypothesis is the fresh-supply threshold for a nonnegative initial backlog, so the backlog predicate holds. The recurrence is then available at every level. The level errors stay at most the constant-overhead closed form, and that closed form becomes smaller than any positive rational. For every rational `L >= 0` and every `epsilon > 0`, some level therefore satisfies `L * p(k) <= epsilon`.

If also `max(C, 1) * p(0) <= 1/2`, the same hypotheses give an explicit level: every natural number `k` with `L <= epsilon * max(C, 1) * 2^(2^k)` satisfies `L * p(k) <= epsilon`.

`viability_nonneg_initial` in `lean4/CampaignQcvConditionalViabilityCertificate.lean` has the first conclusion as its type. `viability_explicit_level` has the explicit level bound as its type. Both use `conditional_viability` and `conditional_viability_explicit` in `lean4/QcSelfObstruction.lean`. The printed axiom list of each is `propext`, `Classical.choice`, and `Quot.sound`.

The Python script checks one rational instance: threshold `2`, `D * p0 = 2/5 <= 1/2`, `p1 = 1/25`, and `16 * p1 = 16/25 <= 1`. That instance is not the general implication.

## What is proved

- Under the hypotheses above, including a nonnegative initial backlog, the backlog predicate holds and the level-error union bound can be made at most any positive rational epsilon.
- Under the stronger threshold `max(C, 1) * p(0) <= 1/2`, the explicit level inequality implies `L * p(k) <= epsilon`.

## What is assumed

- The kernel axioms `propext`, `Classical.choice`, and `Quot.sound`.
- The backlog and concatenation developments cited by the parent nodes.
- The rates and the error sequence are rational inputs of the implication.

## What is open

- A negative initial backlog.
- A construction of the recurrence from a noise process.
- A device, a fresh-ancilla apparatus, or a classical decoder.
