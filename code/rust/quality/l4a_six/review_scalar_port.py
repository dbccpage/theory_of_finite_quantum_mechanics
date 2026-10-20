"""Install individual scalar/storage review inputs, not execution or grade evidence.

AuthorityEffect: None. records.py must still verify current metrics, baselines
and designated challenges before a completed engineering score can be emitted.
"""
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from replay import ROOT, RUST, digest, write

REVIEWED_SOURCES = {
    "linear_algebra/scalars.rs": "94345b59fd4b4968ba0c9793deb52a20fa29692ab70eba1a9a049191565aff38",
    "linear_algebra/basic_matrix.rs": "1e87357a6519498a6f28094798fa217444a93c9787035ce9a0fb14c2d74f2007",
}


def bound(relative):
    path = ROOT / relative
    return {"path": relative, "sha256": digest(path)}


def reviewed(relative, basis, gates, **details):
    source = digest(RUST / "src" / relative)
    if source != REVIEWED_SOURCES[relative]:
        raise RuntimeError("Source differs from the individual review; review again before changing its pin: " + relative)
    return {
        "status": "individual_checked_protocol_review_requires_current_integration",
        "profile": "Exact",
        "capability_assessment": {"source_sha256": source, "level": "L4", "basis": basis},
        "engineering_assessment": {"source_sha256": source,
            "gates": {name: {"grade": "A", "basis": text} for name, text in gates.items()}},
        "open_obligations": [],
        **details,
    }


def main():
    path = Path(__file__).with_name("specs.json")
    specs = json.loads(path.read_text(encoding="utf8"))
    activation = "evidence/quality/l4a_six/20261020T104119Z-scalar-activation"
    old_specs = ROOT / activation / "previous_assessment/code/rust/quality/l4a_six/specs.json"
    previous_scalar = json.loads(old_specs.read_text(encoding="utf8"))["files"]["linear_algebra/scalars.rs"]
    history = [bound(activation + "/activation.json"),
               bound("evidence/quality/l4a_six/20261020T102150Z-scalar-port-faults/receipt.json"),
               bound("evidence/quality/l4a_six/20261020T103621Z-scalar-composition/receipt.json"),
               bound("evidence/quality/l4a_six/20261020T104923Z-mutations/INTERRUPTION.json"),
               bound("evidence/quality/l4a_six/20261020T105520Z-scalar-regression-restoration/restoration.json"),
               bound("evidence/quality/l4a_six/20261020T105539Z-mutations/receipt.json")]
    specs["files"]["linear_algebra/scalars.rs"] = reviewed(
        "linear_algebra/scalars.rs",
        "Individual source review: an owned extensible fallible scalar protocol replaces provider trait reexports. Native operations return range refusals, rational queries admit canonical domains, bounded fractions widen before arithmetic, and private Gaussian storage preserves Q(i). Typed errors, independent edge models, compile-fail boundaries and adapted real consumers supply actual L4 capability.",
        {
            "G1": "SHA-bound requirement/symbol and actual-consumer maps describe the owned protocol and deliberately distinct rational hash policy. Current receipts pin source, dependencies and commands. Archived source/sidecars retain the old overflow findings; no provider-wide repair or formal theorem is advertised.",
            "G2": "i64 uses checked intrinsics and has no Field/ExactRing marker. Q admission requires denominator>0 and gcd(n,d)=1 before arithmetic or zero/conjugate queries. Rational64 widens raw operands first, executes in Q and narrows canonical results with checked conversion. Private admitted Gaussian components close under Q(i) formulas; a^2+b^2=0 iff both coordinates vanish, so inversion rejects exactly zero before division. Generic implementations retain explicitly stated algebra/domain obligations.",
            "G3": "Every expected native range, raw rational domain and zero divisor failure is a typed Result. Borrowed operands are unchanged. Gaussian construction/decoding prevents forged components; native signed division is never used for field operations. q/qr widen first. Hash refusal precedes hasher mutation. num exact arithmetic, serde, blake3, Rust/std allocation and lawful custom scalar callbacks are explicit assumptions; process OOM and arbitrary downstream callback panics are outside this claim.",
            "G4": "Conditional on fresh untouched/restored package baselines and R>=0.95 for designated SC and nonduplicate CP scalar faults. Wide native oracles, independent Gaussian coordinates, literal byte frames, malformed operand/query cases, bounded rational refusals and compiler privacy/trait controls challenge declared failure classes. A distinct F5 implementation checks preservation of generic field support. Earlier survivors and incomplete runs retain their original outcomes.",
            "G5": "All 66 explicit production bodies meet calibrated A ceilings. Rational-domain GCD borrows components instead of cloning/reducing them. Q/Gaussian formulas borrow operands; Rational64 promotion has fixed-size inputs, and output-owned conjugates necessarily copy retained coordinates. Hash buffers are necessary byte encodings. There is no recursive local algorithm, arbitrary-precision bit bound, deadline or process-memory promise.",
        },
        purpose="Provide partial exact scalar operations with canonical domain admission, typed representation refusal, immutable Q(i), and stable normalized rational digest frames.",
        domain_invariants=[
            "Q is still a raw-capable BigRational alias. Successful local operations admit operands; alias membership alone proves no domain invariant.",
            "i64 supports a partial checked ring representation but is neither ExactRing nor Field. Rational64 models partial representable rational-field operations, with a positive canonical denominator on success.",
            "The public traits are intentionally extensible. Their identities, closure, algebraic laws, validation completeness, determinism and expected typed failures are obligations for external implementations; finite law samples cannot establish them universally.",
            "GaussianRational has private canonical Q components. Its constructors, admitted serde decoder, identities and closed arithmetic preserve the domain; validate can consequently return Ok without rechecking private coordinates.",
        ],
        symbol_contracts={
            "q/qr": previous_scalar["symbol_contracts"]["qr"] | {"scope_limit": "q is an integer embedding. qr has no bounded signed normalization and rejects d=0 before Q construction."},
            "Semiring/Ring/Field/ExactRing/CheckedExactField/Involution": "Partial exact protocol with valid zero/one and validation even for queries. Default subtraction/division admit both roles first. Bounded intermediates may refuse despite a representable final expression; success always has the declared mathematical value. No totality claim is made.",
            "ScalarError/ScalarResult/Operation": "ZeroDenominator, NegativeDenominator, NonReduced, DivisionByZero, operation-tagged OutOfRange, InvalidDomain and neutral nonzero InversionRefused are distinct typed refusals. InversionRefused does not assert mathematical noninvertibility.",
            "validate_rational/validate_pair": "Reject denominator zero, then negative, then gcd(n,d)!=1, without normalization arithmetic on malformed fractions. Admit left before right. Canonical zero is 0/1.",
            "i64/BigInt implementations": "Native add/subtract/multiply/negate return checked intrinsic results or their Operation-tagged OutOfRange. BigInt arithmetic is unbounded exact ring arithmetic subject to allocator resources; no field implementation for either integer representation.",
            "wide/narrow/Rational64 implementations": "Build raw Q from widened numerator and denominator, admit through Q operations, and convert both resulting canonical components to i64. This avoids native MIN negation or MIN/-1 division. Reject an unrepresentable positive denominator, including inverse(MIN). Zero queries and conjugation also validate.",
            "Q implementations": "Admit every used operand before exact num-rational operations. Inverse/division reject admitted zero divisors explicitly. Canonical rational arithmetic preserves normalization and positivity; exact intermediates are not a bit or memory budget.",
            "GaussianRational/GaussianWire": "new validates real then imaginary canonical Q. Decoder denies unknown fields and admits its decoded components. Immutable accessors and closed operations preserve Q(i); inverse returns Result and rejects zero. No mutable component escape or larger extension is admitted.",
            "hash_bigint": previous_scalar["symbol_contracts"]["hash_bigint"],
            "hash_rational": previous_scalar["symbol_contracts"]["hash_rational"],
        },
        requirement_symbol_map={
            "typed representation/domain refusal": ["ScalarError", "ScalarResult", "Operation", "validate_rational", "validate_pair", "wide", "narrow"],
            "extensible partial exact models": ["Semiring", "Ring", "Field", "ExactRing", "CheckedExactField", "Involution"],
            "admitted closed Gaussian field": ["GaussianRational::new", "GaussianWire", "GaussianRational::norm_sq", "Field::try_inv", "Involution::try_conj"],
            "stable finite rational hash frames": ["hash_bigint", "hash_rational"],
        },
        consumer_review=[
            "Local elimination, matrix, polynomial, involution, ordered, tensor and law callers propagate ScalarResult. Homology conversions handle new matrix errors. The staged full original-root module/test composition compiles with all QM adaptations; an actual-root consumer receipt is additionally required for current composition evidence.",
            "QM bridge explicitly admits foreign storage before local arithmetic, translates exhaustive error variants, and admits outgoing storage. Receiving provider algorithms and independent provider scalar traits remain separately scoped.",
        ],
        api_changes=["Provider scalar trait reexports are replaced by owned fallible traits. Existing custom implementations and consumers must implement/handle validate and try_* Results; this is an intentional source API migration.", "Involution and ordered-field methods now return typed Results. All in-repository root-module consumers were compiled in the staged full composition check."],
        repaired_historical_findings={
            "controls": [bound("evidence/quality/l4a_six/20261020T074614Z-native-scalar-control/receipt.json")],
            "witness": "Previously the exported i64 provider Semiring add panicked on MAX+1. That trait reexport is removed; the owned implementation returns OutOfRange(Add), and the old ExactRing claim for i64 is absent.",
            "scope": "Old E remains bound to its original source. Current classification requires fresh integrated checks; no stale defect receipt is passed as current-source evidence.",
        },
        origin_and_staged_evidence=history,
        scope_limits=["Exact successful arithmetic, not universal algebraic proof, generic callback panic freedom or allocator crash freedom.", "Arbitrary-precision bit growth, input parsing/serde allocation, hashing allocation and elapsed time have no global bound."])
    specs["files"]["linear_algebra/basic_matrix.rs"] = reviewed(
        "linear_algebra/basic_matrix.rs",
        "Individual source review: the former provider facade is now an owned private storage abstraction with complete numeric operand admission, typed scalar failures, configurable element/work preflight, borrowed arithmetic and explicit private interoperability. This is actual L4 API/resource design rather than a reexport label.",
        {
            "G1": "SHA-bound storage/arithmetic/interoperability maps and current execution receipts separate raw coefficient transport from admitted numeric operations. Inspected pinned provider primitives supply shape storage only. The old MAX*2 panic is archived with its original source and the replacement API is explicitly documented.",
            "G2": "Private storage guarantees checked rows*cols equals length. Numeric entry points check compatible dimensions, inclusive element/work counters and every coefficient before output allocation, even for unused empty-product inputs. Each output dot is the exact ordered multiply/add sequence under the declared partial scalar protocol; zip operations preserve shape. A returned scalar refusal is propagated without inventing a value.",
            "G3": "Output counts and arithmetic charges use checked usize operations. Admission/reservation precede buffers; division by output column count occurs only in a nonempty flat range. Product indices are bounded by admitted input shapes. Errors drop local partial outputs without input mutation. Provider storage field and outgoing conversion are private; no Numeric/Deref escape is public. Lawful scalar/callback/Clone/Drop behavior and allocator internals remain explicit environment assumptions.",
            "G4": "Conditional on fresh untouched/restored integrated baselines and R>=0.95 for MB/PV storage faults, with compiler field/outgoing privacy controls. 6561 independent small matrix pairs, i128 dot/sum/difference models, every native overflow class, malformed coefficient roles, empty metadata, inclusive boundaries, serde shape and thread-local output-layout positive controls exercise declared failure classes.",
            "G5": "All 39 explicit production bodies meet calibrated A ceilings. Products borrow coefficients and reserve the final flat buffer once. Full admission scans precede allocation; no per-entry operand clones or row buffers occur. Internal provider import copies once to establish separately owned storage, and export moves storage. Work counts exactly 2*m*n*k scalar calls, excluding validation/scalar internals; element counts are not byte/RSS/time bounds.",
        },
        purpose="Preserve private shape-checked coefficient transport while providing owned partial exact matrix arithmetic with typed refusals and pre-allocation domain/resource admission.",
        symbol_contracts={
            "BasicMatrix/from_row_major/from_row_major_with_limit/serde": "Private transparent provider storage. Checked dimensions and exact vector length are maintained. Raw coefficient transport, mutation, serialization and layout conversion do not assert numeric domain admission. Numeric operations always revalidate inputs.",
            "try_from_fn*/try_map/try_transpose/try_*nalgebra/get*/set/as_slice/shape/rows/cols": "Use inspected provider shape/index/fallible storage primitives only. Callbacks, coefficient Clone/Drop and nalgebra internals retain their stated behavior. A failing set leaves storage unchanged. Shape-only constructors default to usize::MAX, with explicit limits where offered; this differs from numeric defaults.",
            "DEFAULT_LIMITS/OperationLimits/preflight": "Numeric defaults: 4096 output slots and 1000000 multiply/accumulate calls. Check dimensions, rows*cols, cell charge, 2*elements*inner with checked arithmetic, then work charge, all coefficients, then reserve. Limits are inclusive; huge zero-area metadata runs no output iterations.",
            "mul/checked_mul*/product_entry/mul_vec/checked_mul_vec*": "Admit both complete inputs, including unused coefficients. Reserve once; enumerate row-major outputs and accumulate each exact product through typed scalar calls. Any scalar failure drops partial output. Work limit counts multiplication plus addition, not queries/validation or scalar bit cost.",
            "add/checked_add*/sub/checked_sub*/zip": "Require identical shapes and output slot admission, validate both full coefficient slices, reserve once and apply scalar add/subtract in storage order. No input is mutated; error returns no partial matrix.",
            "try_from_provider/into_provider": "Crate-only interoperability. Import charges default input slots and admits all values before one fallible storage copy. Export re-admits every value then moves the provider storage. This does not approve arithmetic performed later by a receiving foreign API.",
            "zero": "Construct valid additive identities through the declared Semiring provider, with default numeric slot limit and fallible buffer reservation. Identity validity is part of the custom Semiring obligation.",
        },
        requirement_symbol_map={
            "private shape storage and transport": ["BasicMatrix", "from_row_major", "get_ref", "set", "try_transpose", "try_map"],
            "complete pre-allocation admission": ["preflight", "admit", "DEFAULT_LIMITS", "checked_mul_with_limits", "checked_mul_vec_with_limits", "zip"],
            "partial exact borrowed arithmetic": ["product_entry", "checked_add_with_limit", "checked_sub_with_limit"],
            "audited private interoperability": ["try_from_provider", "into_provider"],
        },
        consumer_review=["Core matrix/elimination and homology callers use this owned storage. QM consumers needing foreign nominal matrix records go through a private explicit bridge; no public conversion backdoor exposes provider Numeric multiplication.", "Pinned provider shape, access, serde, fallible callback/map/transpose and nalgebra storage bodies were inspected. Its legacy Numeric arithmetic is never invoked by the local numeric methods."],
        verification_challenges={
            "CP21-unaccounted-polynomial-product": {"source": "code/rust/src/linear_algebra/char_poly.rs", "claim": "The allocation fixture positive control also detects a discarded output product. This is an observed redundant-buffer fault, not proof of a formerly invalid conservative arithmetic budget."}},
        repaired_historical_findings={
            "controls": [bound("evidence/quality/l4a_six/20261020T082506Z-native-matrix-control/receipt.json")],
            "witness": "Previously the unchanged exported provider matrix mul panicked for valid 1x1 i64 MAX times 2. The owned numeric method now propagates ScalarError::OutOfRange(Multiply); private storage blocks bypass through the local type.",
        },
        origin_and_staged_evidence=history,
        scope_limits=["Raw transport is intentionally distinct from admitted numeric values. Custom scalar implementations must uphold their own protocol.", "No bit-length, byte-allocation, process-memory, timeout or foreign algorithm certification is implied."])
    specs["files"]["linear_algebra/provider_scalars.rs"] = {
        "status": "checked_adapters_with_provider_algorithm_review_pending",
        "profile": "Exact",
        "purpose": "Admit canonical coefficients of existing provider Gaussian and cyclotomic representations before invoking their arithmetic through the owned protocol.",
        "symbol_contracts": {"GaussianRat/Cyc12/Cyc24/Cyclotomic<N>": "Validate all rational coefficients before operations and queries, reject zero inversion, and preserve nonzero provider refusal as InversionRefused. Provider arithmetic, modulus, conductor, nonzero invertibility and allocation properties still require a whole-file review."},
        "open_obligations": ["Complete pinned provider inverse/domain/control-flow and scalar closure review for every exported trait implementation, including generic conductors. Finite product grids and a compiling adapter do not certify those algorithms.", "Complete individual capability and all five engineering gates before promoting this new subject to L4A."],
        "origin_and_staged_evidence": history,
    }
    # Each documented critical fault is mandatory. A passing partial prefix
    # replay cannot discharge the whole protocol/storage G4 judgement.
    from mutations import candidates
    critical = candidates()
    for relative in ("linear_algebra/scalars.rs", "linear_algebra/basic_matrix.rs"):
        links = specs["files"][relative].setdefault("verification_challenges", {})
        for entry in critical:
            if entry["source"] == "code/rust/src/" + relative:
                links[entry["id"]] = {"source": entry["source"],
                    "claim": "Detect the designated " + entry["id"]
                    + " fault at the specified exact domain, arithmetic, representation or privacy boundary."}
    write(path, specs)
    print("Installed two source-pinned individual reviews and one explicitly incomplete adapter contract.")


if __name__ == "__main__":
    main()
