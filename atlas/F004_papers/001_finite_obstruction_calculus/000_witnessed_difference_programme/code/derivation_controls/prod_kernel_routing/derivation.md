# PROD-KERNEL-ROUTING

This is a selected finite routing control, not a completed eight-stage runtime
integration. The previous standalone Rust example accepted a caller-supplied
`cert_valid` Boolean and compared two invariant fields. It did not implement the
cochain lift, closure-damage or stabilization conditions tested by Python. That
stand-in has been deleted.

The Rust owner is `omega_wdp::prime_algos::finite_routing`, exercised by
`omega_wdp/tests/test_finite_routing.rs`. Python uses the canonical process seam
for exact Phi1/Gamma2 evaluation and receipt verification. Its finite policy
checks are independent of the Rust routing code.

For zero d0 and d1=(0,1), changing omega=(3,0) to (1,1) lowers Phi1 from 3 to 2
but raises Gamma2 from 0 to 1. A zero closure-damage allowance must refuse that
edit; allowance 1 admits it. An unchanged packet has no strict descent. In the
one-dimensional zero-differential windows the cochain map f1=2 transports omega=2
to 4, not to 2. A fixed point in the declared dynamics is required for the
selected `StabilizedSurvivor` terminal: equal packets on a two-cycle do not
establish one.

These checks do not prove that all engine transitions pass through this route,
choose a terminal policy, or confer action authority. Historical receipts are
unchanged. AuthorityEffect: None.
