"""Independent finite replay of the unchanged model-supplied repair witnesses."""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from antibody_transfer.checker import transfer
from finite_observation.solver import Instance, Instrument, unresolved_pairs, validate_instance
from pfp_calculus.replay import canonical, digest, strict_json

from .round import frozen_inputs, packet


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def fields(value, keys: set[str]) -> None:
    require(type(value) is dict and set(value) == keys, "unexpected or missing fields")


def price(value) -> Fraction:
    require(type(value) is str, "canonical rational string required")
    result = Fraction(value)
    require(str(result) == value and result >= 0, "canonical nonnegative cost required")
    return result


def instance(a: list[str]) -> Instance:
    source = frozen_inputs()["observation"]
    require(type(a) is list and len(a) == 8 and all(type(v) is str and v in {"0", "1"} for v in a), "A must have eight binary string readings")
    instruments = tuple(Instrument(row["name"], tuple(a if row["name"] == "A" else row["outcomes"]),
                                   Fraction(row["cost"])) for row in source["instruments"])
    result = Instance(tuple(source["states"]), tuple(source["visible"]), tuple(source["query"]), instruments)
    validate_instance(result)
    return result


def verify_observation(candidate: dict, *, original_table: bool = False) -> dict:
    fields(candidate, {"A", "fixed_suite", "fixed_cost", "cheaper_subsets", "adaptive_cost", "adaptive_tree", "adaptive_lower_bound"})
    inst = instance(frozen_inputs()["observation"]["instruments"][0]["outcomes"] if original_table else candidate["A"])
    shelf = {item.name: item for item in inst.instruments}
    state_index = {state: i for i, state in enumerate(inst.states)}
    pairs = unresolved_pairs(inst)

    def suite(value) -> frozenset[str]:
        require(type(value) is list and all(type(name) is str and name in shelf for name in value), "invalid fixed suite")
        require(len(value) == len(set(value)), "duplicate fixed instrument")
        return frozenset(value)

    def cost(names) -> Fraction:
        return sum((shelf[name].cost for name in names), Fraction(0))

    selected = suite(candidate["fixed_suite"])
    fixed_cost = price(candidate["fixed_cost"])
    require(fixed_cost == cost(selected), "fixed price differs from submitted suite")
    require(all(any(shelf[name].outcomes[x] != shelf[name].outcomes[y] for name in selected) for x, y in pairs), "fixed suite fails on original unresolved pair")
    cheaper = {frozenset(names) for k in range(len(shelf) + 1) for names in combinations(shelf, k) if cost(names) < fixed_cost}
    require(type(candidate["cheaper_subsets"]) is list, "cheaper-subset certificates required")
    witnessed = set()
    for row in candidate["cheaper_subsets"]:
        fields(row, {"suite", "uncovered_pair"})
        chosen = suite(row["suite"])
        require(chosen in cheaper and chosen not in witnessed, "missing, repeated or noncheaper branch")
        pair = row["uncovered_pair"]
        require(type(pair) is list and len(pair) == 2 and all(type(x) is str and x in state_index for x in pair), "invalid pair witness")
        x, y = map(state_index.__getitem__, pair)
        require(inst.visible[x] == inst.visible[y] and inst.query[x] != inst.query[y], "pair is not an unresolved query")
        require(all(shelf[name].outcomes[x] == shelf[name].outcomes[y] for name in chosen), "pair is resolved by submitted subset")
        witnessed.add(chosen)
    require(witnessed == cheaper, "cheaper subsets not exhausted")

    def tree_cost(node, states: tuple[int, ...], used: frozenset[str]) -> Fraction:
        require(type(node) is dict and bool(states), "invalid or empty tree node")
        if set(node) == {"query"}:
            require(type(node["query"]) is str and {inst.query[i] for i in states} == {node["query"]}, "leaf query is false or unresolved")
            return Fraction(0)
        fields(node, {"measure", "branches"})
        name = node["measure"]
        require(type(name) is str and name in shelf and name not in used, "unknown or repeated tree measurement")
        branches = node["branches"]
        groups = {outcome: tuple(i for i in states if shelf[name].outcomes[i] == outcome) for outcome in {shelf[name].outcomes[i] for i in states}}
        require(type(branches) is dict and set(branches) == set(groups) and len(groups) >= 2, "tree branches omit or invent a realized outcome")
        return shelf[name].cost + max(tree_cost(branches[outcome], group, used | {name}) for outcome, group in groups.items())

    adaptive = price(candidate["adaptive_cost"])
    # This submitted fixture has a constant already-observed report. No cost is
    # charged for obtaining it; the tree is evaluated on its one realized fiber.
    actual = tree_cost(candidate["adaptive_tree"], tuple(range(len(inst.states))), frozenset())
    require(actual == adaptive, "actual submitted tree cost differs from claim")
    lower = candidate["adaptive_lower_bound"]
    fields(lower, {"state", "forcing_pairs"})
    require(type(lower["state"]) is str and lower["state"] in state_index, "missing lower-bound state")
    x = state_index[lower["state"]]
    require(type(lower["forcing_pairs"]) is list, "forcing-pair array required")
    forced = set()
    for row in lower["forcing_pairs"]:
        fields(row, {"other", "instrument"})
        require(type(row["other"]) is str and row["other"] in state_index, "missing forcing-pair state")
        y = state_index[row["other"]]
        require(inst.visible[x] == inst.visible[y] and inst.query[x] != inst.query[y], "forcing pair does not protect an unresolved query")
        separating = {name for name, item in shelf.items() if item.outcomes[x] != item.outcomes[y]}
        require(type(row["instrument"]) is str and separating == {row["instrument"]}, "forcing instrument is not unique")
        forced.add(row["instrument"])
    require(cost(forced) >= adaptive, "adaptive lower bound too small")
    require(fixed_cost == 7 and adaptive == 4, "repair did not reach the declared 7/4 target")
    return {"accepted": True, "fixed_cost": str(fixed_cost), "fixed_cheaper_subsets_checked": len(witnessed),
            "actual_tree_worst_cost": str(actual), "adaptive_forcing_lower_bound": str(cost(forced)),
            "candidate_sha256": digest(canonical(candidate).encode()), "authority_effect": "None"}


def verify_antibody(candidate: dict) -> dict:
    fields(candidate, {"repair_kind", "adapter", "D", "claimed_rejected", "soundness_reason"})
    original = frozen_inputs()["unsafe_transfer"]
    updated = copy.deepcopy(original)
    require(type(candidate["adapter"]) is dict and set(candidate["adapter"]) == {"0", "1"}, "adapter must remain total")
    require(type(candidate["D"]) is list, "D must remain a declared rejection set")
    if candidate["repair_kind"] == "adapter":
        require(candidate["D"] == original["rules"][0]["rejects"] and candidate["adapter"] != original["adapter"], "adapter repair changed the wrong data")
    elif candidate["repair_kind"] == "rule":
        require(candidate["adapter"] == original["adapter"] and candidate["D"] != original["rules"][0]["rejects"], "rule repair changed the wrong data")
    else:
        raise ValueError("repair kind must be adapter or rule")
    updated["adapter"] = candidate["adapter"]
    updated["rules"][0]["rejects"] = candidate["D"]
    result = transfer(updated)
    require(all(row["source_sound"] and row["transfer_safe"] and row["admitted"] for row in result["rules"]), "submitted rule is not admitted")
    require(result["active_rules"] == ["D"], "not every proposed rule was admitted")
    require(type(candidate["claimed_rejected"]) is list and candidate["claimed_rejected"] == result["rejected"], "claimed rejection differs from checked transfer")
    require(type(candidate["soundness_reason"]) is str, "soundness explanation required")
    return {"accepted": True, "problem": updated, "checked_receipt": result, "authority_effect": "None",
            "prose_status": "retained; finite set predicates checked independently"}


def rejected(call) -> dict:
    try:
        call()
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as error:
        return {"accepted": False, "reason": str(error)}
    return {"accepted": True, "reason": "control unexpectedly accepted"}


def original_controls() -> dict:
    inputs = frozen_inputs()
    inst = instance(inputs["observation"]["instruments"][0]["outcomes"])
    collisions = [(x, y) for x, y in unresolved_pairs(inst)
                  if all(item.outcomes[x] == item.outcomes[y] for item in inst.instruments)]
    require(bool(collisions), "original observation control lost its obstruction")
    x, y = collisions[0]
    unsafe = transfer(inputs["unsafe_transfer"])
    require(unsafe["active_rules"] != ["D"] and not unsafe["rules"][0]["admitted"], "original unsafe control was accepted")
    return {"printed_observation_table": {"input": inputs["observation"], "accepted": False,
             "reason": "full shelf has equal readings but unequal query values",
             "indistinguishable_pair": [inst.states[x], inst.states[y]], "fixed_feasible": False, "adaptive_feasible": False},
            "unsafe_original_accumulation": {"input": inputs["unsafe_transfer"], "accepted": False,
             "reason": "source soundness does not establish target soundness", "checker": unsafe}}


def replay(run_dir: Path) -> dict:
    dispatched = strict_json((run_dir / "packet.json").read_text(encoding="utf-8"))
    require(canonical(dispatched) == canonical(packet()), "dispatch packet changed")
    response_bytes = (run_dir / "provider_response.json").read_bytes()
    response = json.loads(response_bytes)
    choices = response.get("choices", [])
    base = {"authority_effect": "None", "candidate_id": "wdp-repair-space-bunny-001",
            "provider_response_sha256": digest(response_bytes), "negative_controls": original_controls(),
            "prose_evidence_status": "PROPOSED_REVISION_NOT_AUTOMATIC_THEOREM_CREDIT",
            "checker_sources": {str(path.relative_to(Path(__file__).resolve().parents[1])): digest(path.read_bytes()) for path in
                                (Path(__file__), Path(__file__).with_name("round.py"),
                                 Path(__file__).resolve().parents[1] / "finite_observation/solver.py",
                                 Path(__file__).resolve().parents[1] / "antibody_transfer/checker.py")}}
    if len(choices) != 1 or choices[0].get("finish_reason") != "stop":
        return dict(base, accepted=False, status="REFUSED_INCOMPLETE_PROVIDER_RESPONSE",
                    finish_reasons=[row.get("finish_reason") for row in choices],
                    candidate_status="NO_ACCEPTED_CANDIDATE",
                    mathematical_candidate_status="NOT_PARSED_OR_EVALUATED",
                    reason="No complete provider response; no candidate is manufactured or repaired by the host")
    raw_content = choices[0]["message"]["content"]
    candidate = strict_json(raw_content)
    fields(candidate, {"candidate_id", "authority_effect", "revised_statements", "observation_repair", "antibody_repair", "verifier_specification"})
    require(candidate["candidate_id"] == "wdp-repair-space-bunny-001" and candidate["authority_effect"] == "None", "candidate identity or authority changed")
    require(type(candidate["revised_statements"]) is list and len(candidate["revised_statements"]) == 10 and all(type(text) is str for text in candidate["revised_statements"]), "ten revised statements required")
    require(type(candidate["verifier_specification"]) is str, "verifier specification must be prose")
    original_transfer = transfer(frozen_inputs()["unsafe_transfer"])
    original_bad = rejected(lambda: require(original_transfer["active_rules"] == ["D"] and all(row["admitted"] for row in original_transfer["rules"]), "original unsafe rule was refused by target counterexample"))
    original_observation = rejected(lambda: verify_observation(candidate["observation_repair"], original_table=True))
    observation = verify_observation(candidate["observation_repair"])
    antibody = verify_antibody(candidate["antibody_repair"])
    return {**base, "status": "CHECKED_FINITE_WITNESSES", "model_content_sha256": digest(raw_content.encode()),
            "candidate": candidate, "observation": observation, "antibody": antibody,
            "negative_controls": {"printed_observation_table": {"input": frozen_inputs()["observation"], "receipt": original_observation},
                                  "unsafe_original_accumulation": {"input": frozen_inputs()["unsafe_transfer"], "receipt": original_bad, "checker": original_transfer}},
            "accepted": observation["accepted"] and antibody["accepted"] and not original_observation["accepted"] and not original_bad["accepted"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = replay(args.run_dir)
    if args.write:
        (args.run_dir / "host_receipt.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"accepted": report["accepted"], "candidate_id": report["candidate_id"],
                      "status": report["status"], "prose_evidence_status": report["prose_evidence_status"], "authority_effect": "None"}))
    raise SystemExit(0 if report["accepted"] else 1)
