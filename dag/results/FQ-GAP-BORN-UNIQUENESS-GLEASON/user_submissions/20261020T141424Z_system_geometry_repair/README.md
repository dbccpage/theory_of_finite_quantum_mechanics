# Row 8: geometric System and classical-exclusion repair

Status: **compiled and ready for review**. AuthorityEffect: None.

- [Repaired System and guarded Jordan interface](ReconstructionGeometry.lean): actual compact convex real state spaces, calibrated capacity/dimension, affine reversibles and composites. The old phantom is excluded by a proved rank-one/dimension-one theorem.
- [Concrete classical-exclusion chain](ClassicalExclusion.lean): affine hull transport, marginal sections, exposed sphere witnesses, infinitely many extreme points, and no affine polytope marginal onto the three-ball.
- [Preserved arithmetic](ReconstructionArithmetic.lean): byte-identical to the previous sealed extraction; all 19 printed receipts rechecked.
- [Affine substitution laws](ConvexSubstitution.lean) and [15 typed operation records](operad_delta.json): unit, substitution and associativity are proved for the unary affine fragment.
- [Independent mathematical review and remaining inputs](review.md), [claim boundaries](claim_status.json), [kernel axiom receipts](verification/kernel_axioms.json), and [compiler/dependency custody](verification/toolchain_dependencies.json).
- [Validation](validation.json), [prior evidence custody](provenance.json), and [file manifest](manifest.json).

Four accepted modules compile with pinned Lean 4.33.1. Their **51 printed axiom receipts** contain only standard Lean logical axioms (or none): 19 preserved arithmetic receipts and 32 new receipts, including 3 reversible-map constructors. No accepted source contains a global custom axiom, sorry or admit.

The elementary classical-composite exclusion is now proved from concrete affine geometry. The combined classical-factor theorem also names its representation, dichotomy, dimension-product and rank-bound premises. **A concrete Jordan catalogue/classification proof, tensor compatibility, complex selection and full process equivalence remain open inputs.** This repair does not establish all of Row 8.

All 824 earlier sealed files were reverified. Earlier failed compilation attempts and API probes remain in [verification](verification/harness_notes.json); only the four *_final receipts certify accepted sources. `Probe.lean` is an unsuccessful exploratory API probe, not an accepted module. The old unsafe sources under [input](input/README.md) are historical context and are not imported.

The source snapshots, exact compiler commands, stdout/stderr and compiled artifact bytes are saved under verification/*_final. Transient build/ import files are excluded from the file seal; their accepted bytes are sealed as compiled.olean.bin. Dependency custody records the resolved direct imports and available sidecars, plus source-package commits; it does not claim a fresh build of Mathlib. [The compiler runner](tools/evidence.py) compiles frozen copies; replay should use a fresh copy of this bundle to preserve this seal.

Stopped for review. No provider calls or Git publication actions were performed.
