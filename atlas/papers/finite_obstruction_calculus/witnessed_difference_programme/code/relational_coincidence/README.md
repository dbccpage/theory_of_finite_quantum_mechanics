# Relational coincidence checks

Exact finite checks for a corrected reading of the general-relativity source paper
[Relational Point Coincidence, Witnessed Difference, and Dressing Field Normal Forms](../../../../general_relativity/relational_point_coincidence_and_witnessed_difference/relational_point_coincidence_and_witnessed_difference.md)
(dated 2026-10-01). Line numbers below refer to that manuscript. Standard library only;
nothing is imported from the source paper or any other package.

## What is checked

1. **Point coincidence is the superkey property.** Postulate 2.1 (line 105) says that
   equal values on K = {phi0, phi1, phi2, phi3} identify the row. That is the superkey
   condition, as line 107 says; lines 109 and 112 then call K a candidate key on a
   dimension argument that no instance can check. On the source's own three rows
   (`test_relational_spacetime.py` lines 18–29) the instance candidate keys are
   {kretschmann}, {matter_density}, {phi0}, {phi1, phi2} and {phi1, phi3}: K is a
   superkey but not minimal. The source's own line-38 assertion has {phi1, phi2, phi3}
   determining matter_density, and on these rows that subset is a superkey. A constructed
   five-row instance with the same heading
   has K as its only candidate key. All dependency checks are about one supplied
   instance; keys of a schema depend on its declared dependencies, and implication under
   declared dependencies is not decided here.
2. **Heath decomposition on an instance.** If X→Y holds in R, then
   R = R[X∪Y] ⋈ R[X∪Z]. This is checked on the source's observer rows, on all 256 Boolean
   relations over three attributes (12 splits each), and on negative controls where the
   dependency fails and the join adds spurious rows. The dependency is sufficient, not
   necessary: some instances rejoin losslessly without it. A lossless decomposition of one
   snapshot says nothing about update anomalies, so "No update anomalies occur" (line 149)
   is unsupported. The S,J,T countermodel of the WDP
   [SQL note](../../docs/sql_normal_form_presentation.md) is replayed: each component edit
   is locally legal, and the rejoined relation violates SJ→T.
3. **Dressing-field convention.** S3 acts freely and transitively on the six orderings
   of a, b, c (g·φ moves the label at position j to position g(j); a permutation p is the
   tuple of images p[i]). With u(g·φ) = g·u(φ) and φ^u := u(φ)⁻¹·φ, all 6⁶ = 46656 maps
   are enumerated: exactly 6 are equivariant, and each is invariant, idempotent and sends
   every configuration to one representative. u(φ^u) = e follows from equivariance. No
   non-identity element fixes a dressed configuration, so "basic" means constant along
   orbits, not fixed. The source's printed conventions are encoded as written:
   - §1.2 (lines 62–66): φ^h = ρ(h⁻¹)φ, u^h = h⁻¹u, φ^u ≡ ρ(u)φ. The equivariance is the
     corrected one; the dressing lacks the inverse, and the step
     ρ(h⁻¹u)ρ(h⁻¹)φ = ρ(u)φ fails. At φ = (a,b,c), h = (1,2,0):
     (φ^h)^u = (c,a,b) but φ^u = (a,b,c). It fails on Z3 too, so commutativity is not
     the issue here.
   - Prop. 4.1 (lines 172–173): φ^g = ρ(g)φ, u(φ^g) = g⁻¹u(φ), Π(φ) = ρ(u(φ))φ. The proof
     moves ρ(g⁻¹) past ρ(u(φ)), which needs the two to commute. In S3 no map satisfies the
     stated equivariance (0 of 46656), since it forces (g₁g₂)⁻¹ = g₁⁻¹g₂⁻¹. The rewrite
     fails at g = (0,2,1), u(φ) = (1,0,2), φ = (a,b,c): (c,b,a) instead of (b,a,c).
     Taking u(g·φ) = u(φ)g⁻¹ instead repairs it; those fields are the inverses of the
     corrected ones and give the same dressed configurations.
   - Z3, as the rotation subgroup of S3: the Prop. 4.1 convention is satisfiable
     (9 maps), invariant, and agrees with the corrected one under u ↦ u⁻¹, with one
     representative in each of the two orbits.

## Command

From the WDP package root, with Python 3.12:

```sh
py -3.12 -m pytest code/relational_coincidence/tests -p no:cacheprovider -o addopts="" -q
```

The package's default `testpaths` do not include these tests. Finite FD operations are
owned natively by `omega_category_theory::finite_functional_dependencies` (SQL note,
"Ownership and evidence ceiling"); these are paper-local reference checks.

## Not carried from the source

- Gauge fixing versus dressing table (§4.2, lines 178–183): continuum claims about Gribov
  copies, BRST and path integrals; no finite check here bears on them.
- Zero boundary edge modes (lines 30, 181): this model has no boundary or field theory,
  and the source gives no derivation.
- Holonomy defect Γ₂ (line 32): the source defines no complex, connection or computation
  for it.
- Relational local green, global red (Theorem 6.1, lines 227–232): the source exhibits no
  configuration; its code checks a dual witness on a bare triangle not tied to any
  RPCNF/DFNF chart or Jacobian.
- RPCNF and DFNF (§5): RPCNF item 2 treats a four-attribute superkey as key minimality,
  and DFNF item 1 uses the Prop. 4.1 equivariance discussed above.

## Non-claims

These are finite checks on stated instances and on actions of S3 and Z3. They do not
model spacetime, fields or general relativity, they do not decide implication under
declared dependencies, and they say nothing about continuous gauge groups.
