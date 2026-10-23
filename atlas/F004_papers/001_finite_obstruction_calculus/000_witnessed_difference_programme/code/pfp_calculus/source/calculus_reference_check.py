#!/usr/bin/env python3
"""Small exact reference checker for this campaign, not a PFP runner integration.

python calculus_reference_check.py self-test
python calculus_reference_check.py check PROBLEM.json CANDIDATE.json
python calculus_reference_check.py stage4 PROBLEM.json STAGE4.json

Candidate files contain the decoded JSON from Stage 4 candidate.proposal.
The expected problem is supplied separately by the host.
"""
from fractions import Fraction
import hashlib
import json
import re
import sys

REAL = "demo001_real_qpoly_v1"
COUNTING = "demo001_integer_counting_v1"


def strict_json(text):
    def object_pairs(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate JSON key: " + key)
            obj[key] = value
        return obj
    def invalid_constant(value):
        raise ValueError("non-JSON numeric constant: " + value)
    return json.loads(text, object_pairs_hook=object_pairs, parse_constant=invalid_constant)


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def rational(text):
    if not isinstance(text, str) or len(text) > 90 or not re.fullmatch(
            r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", text):
        raise ValueError("canonical rational string required")
    value = Fraction(text)
    if str(value) != text or max(value.numerator.bit_length(), value.denominator.bit_length()) > 128:
        raise ValueError("noncanonical or out-of-profile rational")
    return value


def polynomial(values):
    if not isinstance(values, list) or not 1 <= len(values) <= 9:
        raise ValueError("one to nine polynomial coefficients required")
    result = [rational(x) for x in values]
    if len(result) > 1 and result[-1] == 0:
        raise ValueError("remove trailing zero coefficients")
    return result


def trim(values):
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values


def derivative(values):
    return trim([i*values[i] for i in range(1, len(values))] or [Fraction(0)])


def evaluate(coefficients, x):
    result = Fraction(0)
    for a in reversed(coefficients):
        result = result*x + a
    return result


def check(problem, candidate):
    receipt = {"authority_effect": "None", "input_sha256": canonical_sha(problem),
               "candidate_sha256": canonical_sha(candidate),
               "scope": "reference fixture checker only"}
    def done(status, reason, **extra):
        return dict(receipt, status=status, reason=reason, **extra)
    if not isinstance(problem, dict) or not isinstance(candidate, dict):
        return done("invalid_input", "Objects required")
    profile = problem.get("profile_id", "")
    if profile not in (REAL, COUNTING):
        return done("unsupported_evaluator", "No checker for this declared profile")
    if candidate.get("profile_id") != profile:
        return done("profile_mismatch", "Candidate profile differs from host input")
    if candidate.get("input_sha256") != canonical_sha(problem):
        return done("input_mismatch", "Candidate is bound to different input")
    try:
        integrand = polynomial(problem["integrand_coefficients"])
        claimed = rational(candidate["claimed_value"])
        if profile == REAL:
            if (problem.get("domain"), problem.get("measure")) != ("real_interval", "riemann_dx"):
                return done("invalid_input", "Real domain and admitted Riemann measure required")
            if candidate.get("method") != "polynomial_antiderivative":
                return done("unsupported_evaluator", "Reference real checker needs an antiderivative")
            required = {"profile_id","input_sha256","method","antiderivative_coefficients","claimed_value"}
            if set(candidate) != required:
                return done("invalid_witness", "Unexpected or missing candidate fields")
            primitive = polynomial(candidate["antiderivative_coefficients"])
            a, b = rational(problem["lower"]), rational(problem["upper"])
            if derivative(primitive) != integrand:
                return done("invalid_witness", "Polynomial derivative differs from the original integrand")
            computed = evaluate(primitive, b)-evaluate(primitive, a)
        else:
            if (problem.get("domain"), problem.get("measure")) != ("integer_set", "counting"):
                return done("invalid_input", "Declared integer set and counting measure required")
            if candidate.get("method") != "complete_enumeration":
                return done("unsupported_evaluator", "Reference counting checker needs complete enumeration")
            required = {"profile_id","input_sha256","method","values","claimed_value"}
            if set(candidate) != required:
                return done("invalid_witness", "Unexpected or missing candidate fields")
            points = [rational(x) for x in problem["points"]]
            if len(points) > 100 or len(points) != len(set(points)) or any(x.denominator != 1 for x in points):
                return done("invalid_input", "At most 100 distinct integer points required")
            values = [rational(x) for x in candidate["values"]]
            if values != [evaluate(integrand, x) for x in points]:
                return done("invalid_witness", "Values do not enumerate the declared integrand on its full set")
            computed = sum(values, Fraction(0))
        if claimed != computed:
            return done("invalid_witness", "Claimed value differs from the checked witness",
                        computed_value=str(computed))
        return done("checked_accept", "Submitted witness replayed against the bound problem",
                    value=str(computed))
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return done("invalid_witness", str(exc))


def decode_stage4(problem, stage4):
    """Decode the supplied proposal-string contract, after host lineage validation.

    This adapter checks the extraction envelope, not the truth of source quotes or
    routing against Stage 2/3. Those remain explicit host preconditions.
    """
    base = {"authority_effect":"None", "scope":"reference Stage 4 decoding adapter only",
            "stage4_sha256":canonical_sha(stage4), "input_sha256":canonical_sha(problem)}
    required = {"derived_under_policy","demo_id","stage","authority_effect","candidate_id",
                "coefficient_profile","source_quotes","missing_fields","candidate","should_continue"}
    if not isinstance(stage4,dict) or set(stage4) != required:
        return dict(base,status="invalid_extraction",reason="Unexpected or missing extraction fields")
    if (stage4["derived_under_policy"] != "SPK-001" or type(stage4["stage"]) is not int or
            stage4["stage"] != 4 or stage4["authority_effect"] != "None" or
            type(stage4["should_continue"]) is not bool or
            not isinstance(stage4["demo_id"],str) or not isinstance(stage4["candidate_id"],str) or
            not stage4["demo_id"] or not stage4["candidate_id"] or
            not isinstance(stage4["missing_fields"],list) or
            not all(isinstance(x,str) for x in stage4["missing_fields"]) or
            not isinstance(stage4["source_quotes"],list) or
            not all(isinstance(x,str) for x in stage4["source_quotes"])):
        return dict(base,status="invalid_extraction",reason="Malformed extraction envelope")
    if stage4["missing_fields"]:
        return dict(base,status="missing_declaration",reason="Extraction declares missing fields")
    if stage4["coefficient_profile"] != problem.get("profile_id"):
        return dict(base,status="profile_mismatch",reason="Extraction profile differs from host problem")
    wrapper=stage4["candidate"]
    if not isinstance(wrapper,dict) or set(wrapper)!={"proposal"} or not isinstance(wrapper["proposal"],str):
        return dict(base,status="invalid_extraction",reason="One proposal string required")
    try:
        candidate=strict_json(wrapper["proposal"])
    except (ValueError,TypeError) as exc:
        return dict(base,status="invalid_extraction",reason=str(exc))
    return dict(base,candidate_id=stage4["candidate_id"],mathematical_receipt=check(problem,candidate),
                host_preconditions_not_checked=["demo ID matches run", "original seed/profile binding",
                                               "Stage 2 candidate identity and fidelity", "Stage 3 extract routing",
                                               "source quote provenance"])


def problems():
    return {
        "real": {"profile_id":REAL,"domain":"real_interval","measure":"riemann_dx",
                 "integrand_coefficients":["0","1"],"lower":"0","upper":"10"},
        "counting_closed": {"profile_id":COUNTING,"domain":"integer_set","measure":"counting",
                            "integrand_coefficients":["0","1"],
                            "points":[str(x) for x in range(11)]},
        "counting_half_open": {"profile_id":COUNTING,"domain":"integer_set","measure":"counting",
                               "integrand_coefficients":["0","1"],
                               "points":[str(x) for x in range(10)]},
    }


def fixtures():
    p = problems()
    def primitive(coefficients, value="50"):
        return {"profile_id":REAL,"input_sha256":canonical_sha(p["real"]),
                "method":"polynomial_antiderivative",
                "antiderivative_coefficients":coefficients,"claimed_value":value}
    cases = [
        ("correct_primitive","real",primitive(["0","0","1/2"]),"checked_accept"),
        ("shifted_correct_primitive","real",primitive(["7","0","1/2"]),"checked_accept"),
        ("wrong_report","real",primitive(["0","0","1/2"],"51"),"invalid_witness"),
        ("same_value_wrong_linear_primitive","real",primitive(["0","5"]),"invalid_witness"),
        ("same_value_wrong_quadratic_primitive","real",primitive(["0","-10","3/2"]),"invalid_witness"),
    ]
    for name in ("counting_closed","counting_half_open"):
        pp=p[name]
        c={"profile_id":COUNTING,"input_sha256":canonical_sha(pp),
           "method":"complete_enumeration","values":pp["points"],
           "claimed_value":str(sum(map(int,pp["points"])))}
        cases.append((name,name,c,"checked_accept"))
    wrong_profile=primitive(["0","0","1/2"])
    wrong_profile["profile_id"]=COUNTING
    cases.append(("profile_transplant","real",wrong_profile,"profile_mismatch"))
    changed=dict(p["real"],upper="11")
    wrong_input=primitive(["0","0","1/2"])
    wrong_input["input_sha256"]=canonical_sha(changed)
    cases.append(("changed_input_as_counterexample","real",wrong_input,"input_mismatch"))
    c=primitive(["0","0","1/2"]);c["claimed_value"]="50.0"
    cases.append(("noncanonical_rational","real",c,"invalid_witness"))
    return p,cases


def self_test():
    p, cases=fixtures()
    results=[]
    for label, name, candidate, expected in cases:
        receipt=check(p[name],candidate)
        if receipt["status"] != expected:
            raise AssertionError((label,receipt,expected))
        results.append({"fixture":label,"expected":expected,"receipt":receipt})
    left=sum(Fraction(i) for i in range(10))
    right=sum(Fraction(i) for i in range(1,11))
    mid=sum(Fraction(2*i+1,2) for i in range(10))
    if (left,right,mid)!=(45,55,50):
        raise AssertionError("rectangle controls")
    return {"model_rounds_executed":0,"reference_checks":results,
            "rectangle_controls":{"left_10":"45","right_10":"55","midpoint_10":"50"},
            "authority_effect":"None"}


if __name__ == "__main__":
    if sys.argv[1:] == ["self-test"]:
        output=self_test()
    elif len(sys.argv)==4 and sys.argv[1] in ("check","stage4"):
        with open(sys.argv[2],encoding="utf-8") as f:problem=strict_json(f.read())
        with open(sys.argv[3],encoding="utf-8") as f:candidate=strict_json(f.read())
        output=check(problem,candidate) if sys.argv[1]=="check" else decode_stage4(problem,candidate)
    else:
        raise SystemExit(__doc__)
    print(json.dumps(output,indent=2,ensure_ascii=False))
