# WDP-21-16-FSP

Goal id: WDP-21-16-FSP

Selected scope for WDP-21-16-FSP is recorded in this note.

## Selected scope

Two labelled finite carriers already fixed in the monograph, not a yes or a no to the unbound section 21.16 question.

The opened goal row is `open`, with empty `depends_on` and no fence field. Its note says the bullet is a research question, not a register obligation. Its sources are the section 21.16 heading and the FSP bullet. Those lines name neither a fermionic representation, a configuration carrier, nor an observable list.

1. Carrier A. Sites `{0, 1, 2, 3}`, star centered at 0. Two-particle masks `(6, 5, 12, 9, 10, 3, 6)`, with site `x` as bit `x`, and hops `1→0`, `0→3`, `2→0`, `0→1`, `3→0`, `0→2`. The hop sign is `(-1)` to the sum of occupied counts before annihilation and before creation in the ascending occupation order. A diagonal configuration gauge adds `g_u + g_v` in `F_2`.
2. Carrier B. One complete orientation orbit, pinned at `k=1`, `A=1`, `s=+1`, and `O(u)=(-1)^u`. This is an instance of Appendix M.1, not a reuse of the holonomy integer `-1`, and not the four-site meron fixture.

No Python, Rust, SQL, or Lean kernel was run for this note. No continuum, sampling, mixing, or all-model claim is in scope.

## Hypotheses

H1. Section 21.16 asks whether the chosen fermionic representation removes sign holonomy on configuration space while preserving the requested physical observables. The section states that question and does not bind the representation or the observable list. The goal note says this is not a register obligation. The arithmetic below does not close the question.

H2. The representation checked on carrier A is the ascending CAR occupation representation declared for the star exchange and written in `exchange_cycle`. Appendix W states that `c_x` removes site `x` with sign `(-1)` to the number of occupied sites preceding `x`. The function also counts occupied sites preceding the creation target after that removal. A configuration-vertex sign gauge changes an edge parity by `g_head + g_tail` over `F_2`, so every cycle sum is invariant. This note inspects that formula and the stored integers. It does not multiply the `16×16` matrices.

H3. Appendix M.1 assumes a complete orientation orbit `U=(Z/2Z)^k`, a constant nonnegative weight `A`, a baseline sign `s` in `{+1,-1}`, and a sign character `chi_m(u)=(-1)^(m·u)`. The quantities on that orbit are the signed partition contribution `Z_U` and the numerator `N_U = A s 2^k hat{O}(m)`. The `k=1` line is an instance of those formulas, not a continuum ensemble.

H4. Section O.5 records a raw squared numerator `36864` and partition `912` for one canonical fixture, with time-average square `48/19` and equal-time square `149/57`. That pair is not selected. Section 21.16 does not call it the requested observable, and O.4 says the partition-density closure does not establish all observable numerators.

## Derivation

The two carriers stay separate. Neither integer answers the unbound conjunction for every fermionic representation and every requested observable.

### 1. Star holonomy on the configuration graph

The masks are the occupation sets `{1,2}`, `{0,2}`, `{2,3}`, `{0,3}`, `{1,3}`, `{0,1}`, and back to `{1,2}`. Each hop meets the occupation predicate: the source bit is set, the target bit is clear, and the next mask is the mask after removal and creation.

| mask | hop | counts before removal and before creation | sign | next |
| --- | --- | --- | --- | --- |
| `6 = 0b0110` | `1→0` | `0+0` | `+1` | `5` |
| `5 = 0b0101` | `0→3` | `0+1` | `-1` | `12` |
| `12 = 0b1100` | `2→0` | `0+0` | `+1` | `9` |
| `9 = 0b1001` | `0→1` | `0+0` | `+1` | `10` |
| `10 = 0b1010` | `3→0` | `1+0` | `-1` | `3` |
| `3 = 0b0011` | `0→2` | `0+1` | `-1` | `6` |

The six signs are `1, -1, 1, 1, -1, -1`. Their product is

```
1·(-1)·1·1·(-1)·(-1) = -1.
```

The same integer is the Lean statement `actual_exchange_product` and the stored replay field `exchange.product` in `examples.json`, whose `signs` array is the same six integers. The checker in `replay.py` that recomputes `exchange_cycle()` was not run. The parity bits `(0, 1, 0, 0, 1, 1)` sum to `3`, hence to `1` in `F_2`.

On this loop the three odd hops are `0→3`, `3→0`, and `0→2`. That is the between-mode occupancy named for this star in the Hamiltonian-origin note and the parity bits named for this loop in the finite-QM descent note. The agreement is on these six hops. It is not a general identification of the two counting rules beyond this carrier.

The six configuration vertices are distinct, and the loop returns to `{1,2}`. Each vertex is entered once and left once, so every gauge term `g_v` appears twice and cancels in `F_2`. The gauged cycle sum remains `1`. No diagonal sign gauge of this form makes the holonomy `+1`.

The identity `(-1)^6 = 1` is a different assignment: six signs each equal to `-1`. Lean states it as `six_negative_hops_do_not_exchange`, and the star-exchange paragraph says that assignment would multiply to `+1`. It is not this cycle.

The physical site graph has edges `{0,1}`, `{0,2}`, `{0,3}`. Its cycle rank is `3 - 4 + 1 = 0`, so it is a tree. The odd holonomy is on the configuration graph. These hop signs are the off-diagonal CAR matrix elements of the declared removal-then-creation rule, so replacing their product by `+1` changes at least one of those six elements.

This declared ordering therefore does not remove the sign holonomy of this cycle.

### 2. Observable numerator on a different orbit

For nonzero `m`, Appendix M.1 gives `Z_U = 0`. Take `k=1`, `U={0,1}`, `m=1`, `A=1`, `s=1`, `O(0)=1`, and `O(1)=-1`. Then `chi(0)=1` and `chi(1)=-1`, so

```
Z_U = 1·1·(1 + (-1)) = 0.
```

The same character against the observable is `chi(0)O(0)=1` and `chi(1)O(1)=(-1)·(-1)=1`. The sum is `2`, and

```
hat{O}(1) = 2^(-1)·(1+1) = 1,
N_U = 1·1·2^1·1 = 2.
```

Deleting this nonzero-meron orbit keeps the zero partition contribution and drops the numerator `2`. M.1 states the cut: for `A>0`, deletion preserves the numerator if and only if the coefficient at `m` vanishes. An orbit-constant observable is sufficient, not necessary. A normalized expectation still needs a nonzero total `Z`. Cancellation does not preserve this observable.

The same split is the cancelling pair in the finite-QM descent note: weights `+1, -1` contribute `0` to a partition sum and, for observable values `+1, -1`, contribute `2` to a numerator. That sentence is the same two-point arithmetic. It is not a second carrier.

### 3. The two failures do not close the question

Inside these carriers the conjunction fails: the declared ascending CAR occupation representation does not remove the sign holonomy, and meron deletion of this odd character does not preserve the numerator. Those are two labelled witnesses. Section 21.16 does not select this representation or this observable, so the witnesses do not answer the joint question for every requested observable.

The neighbouring fixture integers are not that test. Section O.5 records raw squared numerator `36864` and partition `912`. Their ratio is `768/19`, because `912·40 = 36480` and `384/912 = 8/19`. O.5 separately states a time-average square `48/19` and an equal-time square `149/57`. The FSP monograph, read only as the integration target named by section 21.16, states the same star product `-1` and states that the raw and zero-or-two-meron numerators both equal `36864` on one four-site, two-repetition, `q=3` fixture. That reconstruction was not replayed, and those scalars are not adopted as the section 21.16 calculation. One preserved numerator on that fixture is not removal of configuration-space holonomy.

No continuum limit, physical law, sampling bound, or representation outside these carriers follows. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not answer section 21.16 yes. The representation and the requested observables stay unbound there. Section 21.16 stays open for every other fermionic representation, continuum limit, and sampling claim.
- It does not claim that the ascending CAR occupation representation removes the star holonomy. The inspected product is `-1`, and the `F_2` gauge sum on this cycle remains `1`.
- It does not claim that a physical site tree has positive configuration-space holonomy, or that Lieb–Robinson locality on the site graph supplies that holonomy.
- It does not claim that meron deletion, or any equal-weight sign-reversing involution, preserves every observable. The `k=1` numerator is `2` against a partition contribution of `0`.
- It does not treat `36864`, `912`, `768/19`, `48/19`, or `149/57` as one holonomy-removal theorem, and it does not replay the SQL, Lean, or transfer-matrix checks. The stored exchange field was read; `exchange_cycle()` was not executed.
- It does not solve a generic or NP-hard fermion sign problem, a sampling or mixing bound, or a thermodynamic limit.
- It does not select the complex field, `U(1)`, or a physical CAR law from an inscription. Chapter 22 refuses that Tier-4 selection.
- It does not close section 21.16 or turn the research question into a register obligation. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside these two carriers.
