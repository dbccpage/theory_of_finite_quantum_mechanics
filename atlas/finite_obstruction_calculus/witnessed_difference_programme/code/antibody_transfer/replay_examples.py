"""Replay corrected examples and reject altered antibody/cost receipts."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

if __package__:
    from . import checker as c
else:
    import checker as c


def example_input() -> dict:
    return {
        "schema": "wdp-antibody-input-v1",
        "transfer": {
            "source": {"id": "zero-repairs", "carrier": ["zero", "gradient", "curved"], "valid": ["zero"],
                       "profile": {"field": "Q", "repairs": "zero-only", "tolerance": "0"}},
            "target": {"id": "all-triangle-repairs", "carrier": ["zero", "gradient", "curved"], "valid": ["zero", "gradient"],
                       "profile": {"field": "Q", "repairs": "all-potentials", "tolerance": "0"}},
            "adapter": {"zero": "zero", "gradient": "gradient", "curved": "curved"},
            "outside_domain": "not_applicable",
            "rules": [{"id": "circulation", "rejects": ["curved"]},
                      {"id": "unsafe-point", "rejects": ["gradient"]},
                      {"id": "invalid-source-rule", "rejects": ["zero"]}],
            "pool": ["zero", "gradient", "curved", "curved"],
        },
        "polynomial": [
            {"candidates": {"five-x": ["0", "5"]}, "source_integrand": ["0", "1"],
             "target_integrand": ["5"], "truncate_degree": None},
            {"candidates": {"five-x": ["0", "5"]}, "source_integrand": ["5"],
             "target_integrand": ["5"], "truncate_degree": None},
            {"candidates": {"x-cubed": ["0", "0", "0", "1"]}, "source_integrand": ["0", "0", "3"],
             "target_integrand": ["0", "0", "3"], "truncate_degree": 2},
            {"candidates": {"x-squared": ["0", "0", "1"]}, "source_integrand": ["0", "2"],
             "target_integrand": ["0", "2"], "truncate_degree": 2},
        ],
        "circulation": {"d0": [["-1", "1", "0"], ["0", "-1", "1"], ["-1", "0", "1"]],
                        "weights": ["1", "1", "1"], "dual": ["1", "1", "-1"], "tolerance": "0",
                        "queries": {"zero": ["0", "0", "0"], "gradient": ["1", "-1", "0"],
                                    "curved": ["1", "1", "0"], "projected": ["1/3", "1/3", "2/3"]}},
        "cost": {"setup": "1", "guard": "1/10", "evaluation": "1", "units": "declared evaluation units"},
        "audit_cost": [
            {"adapter": "2", "source_per_rule": "1", "combined_per_rule": "2", "rules": 2},
            {"adapter": "2", "source_per_rule": "1", "combined_per_rule": "2", "rules": 3},
            {"adapter": "2", "source_per_rule": "1", "combined_per_rule": "1", "rules": 4},
            {"adapter": "0", "source_per_rule": "1", "combined_per_rule": "1", "rules": 4},
            {"adapter": "0", "source_per_rule": "2", "combined_per_rule": "1", "rules": 4},
            {"adapter": "0", "source_per_rule": "2", "combined_per_rule": "1", "rules": 0},
        ],
    }


def unsafe_binary_input() -> dict:
    return {"source": {"id": "source", "carrier": ["0", "1"], "valid": ["0"], "profile": {}},
            "target": {"id": "target", "carrier": ["0", "1"], "valid": ["1"], "profile": {}},
            "adapter": {"0": "0", "1": "1"}, "outside_domain": "not_applicable",
            "rules": [{"id": "D", "rejects": ["1"]}], "pool": ["0", "1"]}


def replay() -> dict:
    problem = example_input()
    receipt = c.evaluate(problem)
    checked = c.verify(problem, receipt)
    assert receipt["transfer"]["adapter_safe"] is False
    assert receipt["transfer"]["active_rules"] == ["circulation"]
    assert receipt["transfer"]["accumulation_sound"] is True
    assert [p["adapter_safe"] for p in receipt["polynomial"]] == [False, True, False, True]
    assert receipt["cost"]["saving"] == "3/5"
    binary = c.transfer(unsafe_binary_input())
    assert binary["rules"][0]["source_sound"] is True
    assert binary["rules"][0]["transfer_safe"] is False
    assert binary["active_rules"] == []
    mutations = []
    for name in ("audit", "source-soundness", "transfer-safety", "accumulation", "hit-count",
                 "cost", "derivative", "commutation", "dual-score", "binding", "authority"):
        bad = copy.deepcopy(receipt)
        if name == "audit":
            bad["transfer"]["adapter_safe"] = True
        elif name == "source-soundness":
            bad["transfer"]["rules"][2]["source_sound"] = True
        elif name == "transfer-safety":
            bad["transfer"]["rules"][1]["transfer_safe"] = True
        elif name == "accumulation":
            bad["transfer"]["active_rules"].append("unsafe-point")
        elif name == "hit-count":
            bad["cost"]["h"] = 4
        elif name == "cost":
            bad["cost"]["saving"] = "5"
        elif name == "derivative":
            bad["polynomial"][0]["rows"][0]["derivative"] = ["0", "1"]
        elif name == "commutation":
            bad["polynomial"][2]["commutes_on_target_valid"] = True
        elif name == "dual-score":
            next(q for q in bad["circulation"]["queries"] if q["id"] == "curved")["score"] = "0"
        elif name == "binding":
            bad["input_sha256"] = "0" * 64
        else:
            bad["authority_effect"] = "Grant"
        before = c.encoded(bad)
        try:
            c.verify(problem, bad)
        except c.Refused:
            mutations.append({"name": name, "status": "REFUSE"})
        else:
            raise AssertionError(f"accepted mutation: {name}")
        assert c.encoded(bad) == before
    return {"schema": "wdp-antibody-replay-v1", "authority_effect": "None", "status": "PASS",
            "checked": checked, "unsafe_original": binary, "receipt": receipt, "mutations": mutations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.input is None and args.receipt is None:
        result = replay()
    else:
        c.require(args.input is not None and args.receipt is not None, "supply both input and submitted receipt")
        result = c.verify(c.read_json(args.input), c.read_json(args.receipt))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
