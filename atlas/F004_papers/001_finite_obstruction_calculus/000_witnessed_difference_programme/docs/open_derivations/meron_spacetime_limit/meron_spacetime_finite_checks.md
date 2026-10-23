# Finite insertion checks on one original signed chain

Status: OPEN

Revision: 8b9e7d3704723a80f4927bd24375c55f0d63632e

## Command

From the repository root:

```
py -3.12 omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py
```

Python 3.12.10. Exit status 0. Scope: that one script, exact `fractions.Fraction` arithmetic, the bond order in `meron_transfer_trace`, and the SQL signed partition inside its ceiling.

A second command checked the same file:

```
py -3.12 -m ruff check --select F401,F841,I <script path above>
```

Ruff 0.14.13. Exit status 0. Scope: F401, F841, and I on that file.

The script finds the checkout root by the `.git` file or directory and imports `meron_exact_model` from there. It does not sample a measure and does not run an infinite schedule.

## What the two summations share

`ordered_product_trace` propagates occupation basis vectors through D_j, an optional diagonal observable, and T_j. `history_numerator` sums the same matrix elements over closed occupation tuples. Both read layers from `layer_transfer`. Agreement of those two summations is the expansion of one product.

At zero source the script also requires the unscaled value to equal `meron_transfer_trace`. For L in {4, 6} and LM≤12 it requires `meron_summary` reconstruction and equality with `signed_partition`. The SQL constructor does not store the sources z_{j,x}. L=2 is compared with `meron_transfer_trace` and is outside that SQL ceiling.

## Disk certificate

The in-disk fixture is L=4, M=1, q=193/192. Then M(q-1)=1/192. For x>0, log(1+x)=∫_0^x dt/(1+t)<x, so M log q < 1/192. The declared temperature interval is 0≤theta≤1/192, so this q lies in that interval.

The positive rates are 257/256 and 256/257, together with 1. For a rate at least 1 the slack is rate-1. For a rate below 1 the slack is 1/rate-1. Both non-unit rates have slack 1/256, and 4 M slack = 1/64. The same integral bound gives 4M|log rate| < 1/64. The declared source radius is 1/64, so every |z_{j,x}| in this fixture lies inside it.

The rate 255/256 is not used. There |log(1-u)| > u, and the comparison with 1/64 would go the other way.

The scalar at L=4, M=1 is q^{-1}=192/193. The script requires that rational before the sourced comparisons.

## Outside-disk algebraic control

L=4, M=1, q=3. This q has r=2 and lies outside 0≤theta≤1/192. It is retained as an algebraic control. The removed scalar on the sourced lines is q^{-1}.

Zero source, unscaled, common value of the history sum, the ordered trace, `meron_transfer_trace`, and the SQL signed partition:

```
outside_zero_unscaled=80
```

Old rates (2, 1, 1, 1) and (1, 3, 1, 1). Changed odd-slice rates (1, 1, 1, 5), with the even slice held fixed. Printed sourced values, after multiplication by q^{-1}:

```
outside_protected=596/9
outside_changed=1588/15
outside_substitute=203/3
outside_changed_source_caught=true
outside_wrong_numerator_caught=true
```

The substitute rebuilds both layers with every hop sign replaced by +1. The two summations agree on that stripped product, and that common value is refused against 596/9.

## In-disk fixture

```
inside_q=193/192
inside_zero_unscaled=113837185/7077888
inside_scalar=192/193
inside_protected=133312146660646547597746435/8331671500411760868851712
inside_changed=7699401230309635/481200388964352
inside_substitute=399936439986514024556438281/24995014501235282606555136
inside_mixed=113689345/21856518144
inside_same_site=87426958081/21856518144
```

`inside_zero_unscaled` is the common unscaled zero-source value, including the SQL signed partition. The sourced lines use the rates (257/256, 1, 1, 256/257) and (1, 257/256, 256/257, 1), multiplied by 192/193. The changed odd slice is (1, 1, 256/257, 257/256). The script refuses the changed value against the protected value, and refuses the sign-stripped value against the protected value. On the stripped layers the two summations agree before that refusal.

`inside_mixed` inserts a_0 at half-step 0 and a_1 at half-step 1, at zero source, with the scalar 192/193. `inside_same_site` inserts a_0 at both half-steps. The two rationals differ. Both controls use two distinct time slots. They differ in the spatial site of the second insertion; this checks site dependence, not collapse of two time slots.

## Unscaled wider rings

LM/4 is 3/2 at L=6, M=1 and 1/2 at L=2, M=1. The script requires the comparison scalar to stay 1 and compares unscaled sides. The common prefactor q^{-LM/4} stays in the prose identity.

```
wide_zero_unscaled=51700893357294721/801543976648704
small_zero_unscaled=147841/36864
```

The L=6 value is also the SQL signed partition at q=193/192. The L=2 value matches `meron_transfer_trace` and is not an SQL row. The L=2 wrap interval is empty, so this row is not a sign-strip control.

## Scope of the exit status

Exit 0 means the comparisons in this file held on these fixtures. It does not supply a topology, a cumulant bound, a spacetime kernel, or a joint (L, M) schedule. This is not the static spatial limit, a partition cancellation, or an assumed continuum remainder.
