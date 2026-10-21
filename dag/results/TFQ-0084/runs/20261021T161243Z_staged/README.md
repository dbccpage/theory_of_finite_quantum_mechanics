# TFQ-0084 run 20261021T161243Z_staged

P0_MINE_OPERAD only (2026-10-21). Branch base: pfp-prompts. AuthorityEffect: None.

The sharpened target (T1 arccos-free Schlafli identity, T2 Regge equations, T3 exact flat Hessian
kernel, T4 squared-area near miss) is recorded in `p0/research_target_sharpened.md`; the committed
prompt still carries the generic source statement.

Mined: no exact dihedral-sine, Schlafli, Hessian or interior-grid generator exists in Rust, Lean or
Python. Exact pieces found: the external `regge_exact` Cayley-Menger kernel (BigRational, d <= 4),
`certified_dihedral.rs` normal-Gram triple (n = 4, untested), Kuhn/Freudenthal exact charts, and
`rational_regge_proxy` (the T4 weighting; the paste name `exact_ge_proxy` does not exist).

Finite-carrier evidence produced in this turn (exact Fraction arithmetic, no roots):
`p0/relation_sign_check.py` (R_CM, R_COF, R_COS with the dimension-uniform sign c_n, R_SIN) and
`p0/schlafli_rational_form_check.py` (T1 reduces to the rational cofactor sum R_e(x) = 0; verified on
every edge of 5 tetrahedra and 3 pentatopes). These are mining evidence, not certificates.

Supported: typed generators/relations and a root-free polynomial form of T1 ready for host review.
Not supported: any theorem (Schlafli, Regge equations, Hessian kernel, near-miss inequality).
Next: host review of the sign convention, the reduction and the toolchain binding; then P1 for T1, n = 3.

No host_check.json yet: the host review has not run. No provider was dispatched.
