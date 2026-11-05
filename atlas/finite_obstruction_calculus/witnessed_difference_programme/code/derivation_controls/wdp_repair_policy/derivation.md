# WDP-REPAIR-POLICY

Goal id: WDP-REPAIR-POLICY

Selected scope for WDP-REPAIR-POLICY is recorded in this note.

## Selected scope

Degree-1 window over Q with cells (e, s): C0=0, C1=Q e, C2=Q s, d0=0, d1=id, J=absolute value. d1 d0=0. Norm hypothesis of WDP-CH04-P04 holds. Run h_n=2^(-n) for n=0,1,2,... . Acceptance requires Phi_1 to strictly decrease and R_cl to stay at most ||d1||_{J to 1}=1. The same scaling is checked on the filled triangle of WDP-CH04-P08. This refutes termination on these finite windows only. No discrete rank, additive decrement, or finite value set is assumed. The 1D values are not a higher-dimensional signature.

## Hypotheses

H1. `WDP-CH04-D01` says a degree-1 window is a declared tuple of finite-dimensional coefficient spaces and linear maps with a certificate that `d1 d0=0`. The certificate is not automatic for a hand-declared pair. `WDP-CH04-D02` sets `Q^1 = C^1 / im d0`, `kappa^1([h]) = d1 h`, `H^1 = ker kappa^1`, `Phi_1([h]) = Phi_J([h])`, `Gamma_2([h]) = ||d1 h||_1`, and `R_cl([h]) = Gamma_2([h]) / Phi_1([h])` when `Phi_1([h]) > 0`. The classes are `ExactClass` when `[h] = 0`, `ClosedResidual` when `[h]` is nonzero and `Gamma_2 = 0`, and `ActiveClosureFailure` when `Gamma_2 > 0`. Section 4.2 defines `Phi_J([h]) = inf_f J(h - d0 f)`.

H2. The norm hypothesis of sections 4.9–4.11, used by `WDP-CH04-P04`, allows `Q` when `J` is the restriction of a norm on the real extension. Absolute value on `Q` is that restriction of the real absolute value. `WDP-CH04-P04` then gives exactly one diagnostic class, `Phi_1([h]) = 0` exactly for `ExactClass`, and `Phi_1 > 0` on every `ActiveClosureFailure` class. `WDP-CH04-P05` gives `Phi_1 >= 0`, `Gamma_2 >= 0`, and `Gamma_2([h]) <= ||d1||_{J to 1} Phi_1([h])`. `WDP-CH04-P06` divides that inequality by a positive `Phi_1` and concludes `0 <= R_cl([h]) <= ||d1||_{J to 1}`.

H3. `WDP-CH04-P01` says `Phi_J` is unchanged when `h` is replaced by `h + d0 g`. `WDP-CH04-P07` certifies a weighted `L^1` value over `Q` by a repair and a circulation `y` with `d0* y = 0` and `|y_e| <= w_e` when the pairing equals the repaired mass. It does not import the existence statement `WDP-CH04-C01`. `WDP-CH04-P09` and the paragraph after it in section 4.11 say that restriction, face attachment, and equal-weight subdivision do not lower `Phi_1`. A strict drop requires deleting cells, changing declared weights, or changing existing edge values. Section 21.8 repeats that a policy with content must declare one of those changes, or an enlarged repair set.

H4. The policy under test is the one named after `WDP-CH04-P06` and in goal `WDP-REPAIR-POLICY`: accept a transition only when `Phi_1` decreases and `R_cl` stays bounded, and ask for a termination argument for such runs. This note reads the decrease gate as a strict drop, `Phi_1` at the next state strictly less than `Phi_1` at the current state, and reads the bound as the `WDP-CH04-P06` number `||d1||_{J to 1}`. No discrete rank, no uniform additive decrement, and no finite admissible value set is assumed.

H5. The same paragraph says a policy of that kind is not absorbed and points to `WDP-CH04-O01`. `WDP-CH04-O01` is conditional on a declared terminal, lift, and guarded-change policy, and it says the diagnostic does not select its policy. The change log of the primitive-axiomatics absorption says the guarded repair policy and the guarded-descent run theorem were not carried. Ledger rows E9 and E10 are `NOT_CARRIED`. Their historical status is not inherited and is not used as a proof.

## Derivation

Unqualified termination is refuted on the selected windows. The two gates accept an infinite run of nonzero classes. No positive termination theorem is admitted.

### 1. The one-cell window

Take cells `(e, s)` and spaces `C^0 = 0`, `C^1 = Q e`, `C^2 = Q s`. The only linear map `d0: C^0 -> C^1` is the zero map, and `d1` is the identity, with matrix `(1)`. Then `d1 d0 = 0`, so the `WDP-CH04-D01` certificate holds. The image of `d0` is `{0}`, and `Q^1` is isomorphic to `Q`.

`J` is absolute value, so the norm hypothesis of `WDP-CH04-P04` holds. For the unweighted `L^1` norm, `||d1||_{1 to 1}` is the largest absolute column sum of the matrix of `d1`. That sum is `1`. Equivalently, `sup{|x| : |x| <= 1} = 1`.

For `h` in `Q`,

```
Phi_1([h]) = inf_f |h - d0 f| = |h|,
```

attained at the only repair `f = 0`. Also `d1 h = h`, so `Gamma_2([h]) = |h|`. If `h` is nonzero, `Phi_1([h]) = |h| > 0` and `R_cl([h]) = 1`. `H^1 = ker id = {0}`, so there is no nonzero closed class. Every nonzero class has `Gamma_2 > 0` and is `ActiveClosureFailure`. The expansion constant `inf{R_cl([h]) : Phi_1([h]) > 0}` equals `1`. `WDP-CH04-P06` holds with equality: `0 <= R_cl <= 1`. It supplies no smaller positive value and no least positive `Phi_1`.

`WDP-CH04-P07` certifies each positive state. The adjoint `d0*` lands in the zero space, so `d0* y = 0` for every `y`. Take the unit weight and `y = 1`. Then `|y| <= 1` and the pairing equals `|h|`. With the zero repair, the repaired mass is `|h|`, so `Phi_1([h]) = |h|` without `WDP-CH04-C01`.

### 2. Licensed repairs do not strictly decrease `Phi_1`

`WDP-CH04-P01` says replacing `h` by `h + d0 g` leaves `Phi_1` unchanged. On this window the only coboundary is `0`, so every representative change is trivial. The strict-decrease gate therefore rejects every licensed repair. A strict drop has to be a declared edit of the existing value on `e`, as `WDP-CH04-P09` and section 21.8 require. `WDP-CH04-P09` also blocks growth, face attachment, and equal-weight subdivision as sources of that drop.

### 3. The dyadic run is accepted and does not stop

Set `h_n = 2^(-n)` in `Q` for `n = 0, 1, 2, ...`. Section 1 gives

```
Phi_1(h_n) = 2^(-n),
Gamma_2(h_n) = 2^(-n),
R_cl(h_n) = 1.
```

The step from `h_n` to `h_{n+1}` replaces the value `2^(-n)` by `2^(-(n+1))`. It is not addition of a coboundary. The drop is

```
2^(-n) - 2^(-(n+1)) = 2^(-n-1) > 0,
```

so `Phi_1` strictly decreases. `R_cl` stays equal to `1`, which is at most `||d1||_{J to 1} = 1`. Both gates accept the step. The same acceptance holds for any stated bound `M >= 1`; the second gate does not cut the run. Positive expansion likewise gives no uniform drop: the ratio is constantly `1`, while the drop at step `n` is `2^(-n-1)`.

By induction, `2^0 = 1 > 0`, and if `2^(-n) > 0` then `2^(-(n+1)) = (1/2) 2^(-n) > 0`. So `Phi_1(h_n) > 0` for every finite `n`. `WDP-CH04-P04` then says `[h_n]` is not `ExactClass`. Every step is accepted, and the run does not reach a zero class in finitely many steps. The accepted run is infinite.

### 4. The prefix is not the obstruction

For `n = 0, 1, 2` the values are exact rationals:

```
h = (1, 1/2, 1/4),
Phi_1 = (1, 1/2, 1/4),
Gamma_2 = (1, 1/2, 1/4),
R_cl = (1, 1, 1),
```

and `1 > 1/2 > 1/4 > 0`. No float is required. The same identities hold for every `n`, with numerator `1` and denominator `2^n`, and with `R_cl = 1/1`. The obstruction is that closed form. A finite prefix does not stop the run, and its last positive value is not a residual of a limit step. The limit value `0` is not a state of the run and not a repair.

This does not contradict `WDP-CH04-P06`. The bound holds with equality at every nonzero state.

### 5. The same scaling on the filled triangle

The zero repair space is not essential. `WDP-CH04-P08` takes the filled triangle with edges `(01, 12, 02)`, `d0 f = (f_1 - f_0, f_2 - f_1, f_2 - f_0)`, `d1 x = x_01 + x_12 - x_02`, and `delta = (1, 1, 0)` over `Q` with unit weights. It records `d1 d0 = 0`, `Phi_1([delta]) = 2`, `Gamma_2([delta]) = 2`, `||d1||_{1 to 1} = 1`, and `R_cl([delta]) = 1`.

Unit `L^1` is homogeneous: for a positive rational `c` and a rational cochain `x`, `||c x||_1 = c ||x||_1`. For `c ≠ 0` the map `f |-> c f` is a bijection of the rational repair space. Therefore `Phi_1([c delta]) = c Phi_1([delta])` and `Gamma_2([c delta]) = c Gamma_2([delta])`. Set `delta_n = 2^(-n) (1, 1, 0)`. Then

```
Phi_1(delta_n) = 2^(1-n),
Gamma_2(delta_n) = 2^(1-n),
R_cl(delta_n) = 1.
```

`WDP-CH04-P07` still certifies the value: the circulation `y = (1, 1, -1)` from `WDP-CH04-P08` pairs with `delta_n` to `2^(1-n)`, and the scaled repair `2^(-n)(0, 1, 0)` meets that mass.

The vector `(1, 1, 0)` is not a coboundary. A coboundary has the form `(a, b, a + b)`, and `1 + 1 = 2 ≠ 0`. So `delta_{n+1}` is not `delta_n` plus a coboundary. `WDP-CH04-P01` says a coboundary edit would preserve `Phi_1` in any case. The step is an edit of the three existing edge values. Both gates accept it, `Phi_1(delta_n) = 2^(1-n) > 0` for every finite `n`, and the class never becomes `ExactClass`. This is a second finite window. It is not a higher-dimensional signature read off the one-cell values `2^(-n)`.

### 6. The historical guarded-descent statement does not give finite arrival

The extracted statement associated with ledger row E10 says that an accepted run with a strict drop in `Phi` and `R <= R_max` has strictly decreasing `Phi`, satisfies `Gamma <= R_max Phi`, and, if the run is infinite and `Phi` tends to `0`, has `Gamma` tending to `0`. It also says that no infinite accepted run can drive `Phi` to `0` while leaving `Gamma` bounded below by a positive epsilon. On the one-cell run, with `R_max = 1`, one has `Gamma_n = Phi_n = 2^(-n)`, so `Gamma_n` tends to `0` with `Phi_n`. The statement holds on this run and does not contradict `WDP-CH04-P06`. It does not say that an accepted run reaches `0` after finitely many steps.

That historical statement is not a theorem of the monograph. The absorption record says the guarded repair policy and the guarded-descent run theorem were not carried. Ledger rows E9 and E10 are `NOT_CARRIED`, with no inherited status. Appendix J.2 says that finite checked guarded sequences obey a summed damage bound, without proving an infinite limit or physical stability. `WDP-CH04-O01` keeps the router external: the diagnostic does not select its policy.

### 7. Extra hypotheses that this rule does not contain

A termination theorem for every accepted run would need an extra hypothesis. None of the following is part of the stated policy, and none is proved here.

(U) Every accepted step drops `Phi_1` by at least a fixed positive rational epsilon. From `Phi_1 >= 0` in `WDP-CH04-P05`, a run starting at `q = Phi_1(h_0)` would then have length at most `floor(q / epsilon)`.

(F) Only finitely many states are visitable. An infinite strict descent would then repeat a state and therefore a `Phi_1` value.

(D) Every `Phi_1` value lies in `(1/N)` times the nonnegative integers for one fixed positive integer `N`. The count in (U) then applies with `epsilon = 1/N`.

The dyadic run meets none of these. The drop at step `n` is `2^(-n-1)`, which is not bounded below by one epsilon. The states are pairwise distinct. The denominators are unbounded. A run that stopped under (U), (F), or (D) could still stop with `Phi_1 > 0`. `WDP-CH04-N01` says that a diagnostic class is not a routing terminal, and that `ExactClass` is not `ExactRepair`. A stall at a positive value is not `ExactClass`.

## Claims this note does not make

- It does not claim that every policy of this shape, on every carrier, fails to terminate. The refutation is the accepted infinite run on the selected windows.
- It does not admit a termination theorem. In particular, it does not admit termination under an extra discrete rank, a uniform additive drop `Phi_{t+1} <= Phi_t - delta`, or a finite admissible value set.
- It does not treat positive expansion, or the upper bound in `WDP-CH04-P06`, as a discrete rank or as a uniform drop.
- It does not claim that a coboundary edit strictly decreases `Phi_1`. `WDP-CH04-P01` says the opposite.
- It does not claim that `WDP-CH04-O01` absorbs the policy or selects it. The diagnostic does not select its policy, and the monograph says the policy is not absorbed.
- It does not inherit the historical status of ledger rows E9 and E10.
- It does not treat the limit value `0` as a step of the run or as a repair.
- It does not read the last positive value of a finite prefix as a continuum residual, a physical stability statement, or authority to route.
- It does not identify the one-cell values `2^(-n)` with a signature on the filled triangle. The triangle check is a separate finite window.
- It does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
