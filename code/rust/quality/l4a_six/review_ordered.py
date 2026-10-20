"""Individual ordered-algebra review input; execution gates remain independently checked.

AuthorityEffect: None. Never applies this judgement to changed source bytes.
"""
import argparse
import json
from pathlib import Path
from replay import ROOT, RUST, digest, write

REVIEWED = "7b4a42bcb7d78985463307a9474ee9cb2878afa6862380f176268589346ed4d9"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activation", required=True, type=Path)
    args = parser.parse_args()
    activation_path = args.activation.resolve()
    activation = json.loads(activation_path.read_text(encoding="utf8"))
    relative = "linear_algebra/ordered.rs"
    subject = "code/rust/src/" + relative
    assert digest(RUST / "src" / relative) == REVIEWED
    assert activation["after"][subject.replace("/", "\\")] == REVIEWED
    trial_path = ROOT / activation["trial"]
    assert digest(trial_path) == activation["trial_sha256"]
    trial = json.loads(trial_path.read_text(encoding="utf8"))
    assert trial["accounting"]["killed"] == 16 and trial["accounting"]["conservative_ratio"] == 1
    def ref(path):
        return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}
    decisions = {
        "G1": "Source-pinned contracts map every public family to ordered-field or fixed-field assumptions, typed failure, LDL recurrence, count admission and real root consumers. No theorem prover, universal field-law validation or total scalar arithmetic is advertised. Historical overflow controls remain attached to the replaced public-count representation.",
        "G2": "Canonical Q sign reads the admitted numerator. Checked sign queries enforce {-1,0,1} and sign-zero consistency. Inertia counts the congruence diagonal under Sylvester's law and explicit lawful-field assumptions. Private count construction checks the total sum, so every partial sum fits usize. LDL subtracts each completed L D L* coupling, divides only a positive pivot, and stops on negative or obstructed zero pivots. Back substitution transforms the Schur witness to the original coordinates; the zero-column coefficient gives the literal form -1. Independent principal-minor and direct quadratic-form oracles challenge these identities.",
        "G3": "Expected domain, shape, symmetry, fixed-field, inverse and resource refusals propagate typed Results without mutating borrowed inputs. Count getters cannot overflow after checked admission; internal sign counts are bounded by the finite diagonal length. Private LDL indexing follows admitted n-by-n grids, columns and rows strictly below n, and equal-length pivots/witness vectors. Work arithmetic is checked before workspace construction; reservations are fallible. Lawful custom callbacks and standard arbitrary-precision allocations remain explicit trust assumptions.",
        "G4": "Requires current untouched/restored package baselines and R>=0.95 for all OD01-OD16 plus the existing ordered admission challenges. Independent u128 triples test count overflow; all 729 ternary symmetric 3-by-3 forms use seven literal principal minors and a separate direct quadratic form. Existing Hermitian, quadratic extension, reconstruction, false-sign, invalid-rational, empty and inclusive-budget cases are retained. Privacy uses an external compile-fail target, not module-internal access.",
        "G5": "Semantic LDL phases have calibrated A complexity ceilings. The largest charged grid is n^2 scalar slots and LDL charges 2n^3+n^2 arithmetic work; inertia delegates the separately documented congruence budget. Counts and zero-size loops are bounded by admitted finite dimensions. Pivots move into the result; witness buffers have length n. Limits do not bound coefficient bit growth, validation, clones, total process memory or elapsed time. Default convenience wrappers explicitly use the unlimited policy; callers requiring admission select the with_limits APIs.",
    }
    specification = {
        "status": "individual_ordered_review_requires_current_integrated_evidence",
        "profile": "Exact",
        "purpose": "Admit finite inertia counts and compute exact symmetric/Hermitian inertia, quadratic forms and LDL factorizations with replayable negative witnesses.",
        "capability_assessment": {"source_sha256": REVIEWED, "level": "L4",
            "basis": "An intentional finite exact API with immutable admitted counts, typed field/shape/sign/resource refusals, explicit configurable work policy and structured LDL state transitions. Independent model and compiler-boundary challenges support actual production capability."},
        "engineering_assessment": {"source_sha256": REVIEWED,
            "gates": {gate: {"grade": "A", "basis": basis} for gate, basis in decisions.items()}},
        "domain_invariants": [
            "OrderedExactField and HermitianOrdered are extensible obligations. Finite law samples cannot prove closure, total ordering or positive norms for arbitrary implementations.",
            "Inertia::try_new admits representable nonnegative counts; it does not certify their relationship to an arbitrary matrix. Internal count_signs derives counts from an algorithmic diagonal.",
            "Ldlt has private storage. Successful completion represents A=L D L* with nonnegative diagonal; stopped results carry the disclosed negative witness and do not claim complete reconstruction.",
        ],
        "requirement_symbol_map": {
            "checked exact order": ["OrderedExactField", "HermitianOrdered", "checked_sign", "checked_fixed_sign", "validated_sign"],
            "representable immutable counts": ["Inertia", "Inertia::try_new", "InertiaCountError", "count_signs"],
            "exact inertia and definiteness": ["inertia_with_limits", "hermitian_inertia_with_limits", "is_positive_semidefinite", "is_positive_definite", "hermitian_is_positive_semidefinite", "hermitian_is_positive_definite"],
            "forms and factorization witnesses": ["quadratic_form", "hermitian_form", "Ldlt", "LdltOutcome", "ldlt_with_limits", "hermitian_ldl_with_limits", "LdlWorkspace", "solve_unit_lower_adjoint", "zero_pivot_coefficient"],
        },
        "symbol_contracts": {
            "Inertia::try_new/rank/dimension/getters": "Check the total with checked_add before constructing private immutable counts. Overflow is DimensionOverflow. Admitted rank and dimension are exact; zero-dimensional definiteness follows the vacuous mathematical convention.",
            "ordered/fixed-field signs": "Admit canonical coefficients; distinguish undefined or nonfixed queries from valid zero. Reject out-of-range or inconsistent signs. Implementor algebraic laws remain explicit assumptions.",
            "inertia/definiteness wrappers": "Require admitted square symmetric/Hermitian input, delegate congruence under the selected limits and count checked signs. No untrusted supplied certificate enters this path.",
            "quadratic_form/hermitian_form": "Admit matrix and vector domains and matching dimensions, then compute v^T A v or v* A v through the owned checked scalar protocol.",
            "LDL APIs/LdlWorkspace": "No pivoting. Preserve completed-column LDL* recurrences. Positive pivots update the column; a negative pivot supplies a direct negative direction; an obstructed zero pivot supplies form -1. Completion iff PSD is conditional on the declared field/order laws.",
            "Ldlt reconstruction": "Reconstruct from private L and D using fallible checked matrix operations. Equality with the input is asserted only for completed factorizations.",
        },
        "consumer_review": [
            "qm/campaigns/gleason.rs now reads negative() after the deliberate public-field API migration. The root module's scalar and matrix consumers require a fresh original-root composition receipt.",
            "Congruence constructs its own diagonal/transform using invertible swaps, shears and elimination; forged public from_certificate objects are not accepted by the inertia API. Matrix, scalar and involution failure propagation were inspected at this boundary.",
        ],
        "api_changes": ["Inertia fields are private; use try_new and read-only count getters. Overflowing external triples now return DimensionOverflow instead of reaching unchecked sums."],
        "origin_and_staged_evidence": [ref(activation_path), ref(trial_path),
            ref(ROOT / "evidence/quality/l4a_six/20261020T110958Z-inertia-control/receipt.json")],
        "verification_challenges": {},
        "scope_limits": ["No formal proof of arbitrary field implementations or compiler/allocator crash freedom.", "Operation limits count declared scalar work and grid slots, not arbitrary-precision bytes or deadlines."],
        "open_obligations": [],
    }
    from mutations import candidates
    for entry in candidates():
        if entry["source"] == subject:
            specification["verification_challenges"][entry["id"]] = {"source": subject,
                "claim": "Detect the designated " + entry["id"] + " count, sign, LDL recurrence, witness, admission or privacy fault."}
    path = Path(__file__).with_name("specs.json")
    specifications = json.loads(path.read_text(encoding="utf8"))
    specifications["files"][relative] = specification
    write(path, specifications)
    print("Installed the source-pinned ordered review; current execution and sidecar validation remain required.")


if __name__ == "__main__":
    main()
