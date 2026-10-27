# Publication description

Edition 6.9.18 · 2026-10-14. Author-review revision; not deposited.

Projection Obstruction for Factorized States: Nonlinear Dynamics, Conditional L1 Diagnostics, and Exact Short-Time Defect Bounds

Jeremy H. Carroll

This manuscript investigates projection obstruction for factorized states under
finite one- and two-local quantum dynamics. For factorized initial states, an
exact short-time lower-bound certificate D_e(t) >= nu_e t - 24 g^2 t^2 is
established with full incident interaction norm g, alongside all-order
derivative bounds, connected cumulant Steiner-tree bounds, and polynomial
onset-or-invariance certificates. We separate marginal product retraction from
nearest-product trace-norm distance, determine tangent-space dual certificates,
and show that orthogonal pure-state excitation sectors satisfy nu_global^2 =
sum nu_e^2. Explicit families demonstrate the breakdown of unrestricted
global/edge trace-norm equivalence. Phase-fiber minimax intervals and completed
linear observer prediction bounds are established. On an Ising ring, an explicit
local cycle-gradient repair differential yields a measured cohomology class with
size-independent conditioning where pair defects vanish while cycle obstruction
remains strictly positive.

The package contains the manuscript, selected Lean 4 formalizations, exact
finite implementations and numerical diagnostics with scoped test and replay
records. The three-module E.1/E.6 target and historical standalone sources
have separate build records; no complete Lean proof of the paper is claimed.
Sampled quadrature and tolerance-based tangent solvers are numerical
candidates, not certified enclosures. Python evidence concerns only its
encoded finite data and does not establish universal mathematical claims.

Edition 6.9.16 connects protected-history reports to quantum observer completion, distinguishes positive Bell extension from linear and support gluing, and states the remaining operational reconstruction premises. Native preparation probabilities remain supplied inputs.

Edition 6.9.18 consolidates this publication as a unified 69-page edition, corrects the complete Duhamel error budget and graph-state formulas, and separates sampled numerical estimates from certified bounds. The publication audit also corrects the tangent domain, the sharp marginal derivative norm 2 versus residual bound 3, the Appendix A image domain, and the topology and noise premises in §7.9. Cut material (former §§3.4–3.14, Appendix D, and Appendix E) is reconciled with archived revisions and sibling package 006_finite_qm (§13.8). Infinite-volume conclusions require a uniform incident interaction bound. Selected formalizations and tests retain their stated scopes.
