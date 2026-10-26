Status: AI-drafted, awaiting human review.

# GP-IMPORT-GLEASON

AuthorityEffect: None.

The imported target asks for uniqueness of the Born quadratic form when the dimension is at least 3 and the Gleason hypotheses are in force. This note keeps that uniqueness imported. It records only the two-label arithmetic: the dimension count fails, and two readout orders disagree on one effect while agreeing on the unit effect.

## Two labels

A host with labels `false` and `true` has two labels. The inequality `2 < 3` says this host does not meet a requirement of three labels. Equivalently, `3 ≤ 2` does not hold. There are also no three pairwise distinct values among `{false, true}`.

## Amplitudes and weights

Put amplitude `2` on `false` and amplitude `1` on `true`. The squared weights are

```
2 * 2 = 4
1 * 1 = 1
```

A pairing against an effect `(e_false, e_true)` is

```
4 * e_false + 1 * e_true
```

The unit effect is `(1, 1)` in both readout orders, because swapping a constant effect leaves it constant. Both pairings equal `4 + 1 = 5`.

The false-indicator is `(1, 0)`. Swapping it gives `(0, 1)`. The two pairings are

```
4 * 1 + 1 * 0 = 4
4 * 0 + 1 * 1 = 1
```

These values differ.

## What is proved

- `2 < 3`, and `3 ≤ 2` does not hold.
- No three pairwise distinct labels exist on a two-value host.
- The squared weights of amplitudes `2` and `1` are `4` and `1`.
- Both unit-effect readout orders pair to `5`.
- The false-indicator pairs to `4` directly and to `1` after the effect is swapped.

## What is assumed

Nothing beyond integer arithmetic and the two-label enumeration. The Gleason hypotheses are not assumed, and they are not discharged.

## What is open

Uniqueness of the Born quadratic form for dimension at least 3, under noncontextuality, sigma-additivity and continuity, stays imported. The two-label disagreements do not refute that uniqueness under those hypotheses. Quartic readout under scale-2 frame additivity stays outside this slice. Status stays IMPORTED_ASSUMPTION.
