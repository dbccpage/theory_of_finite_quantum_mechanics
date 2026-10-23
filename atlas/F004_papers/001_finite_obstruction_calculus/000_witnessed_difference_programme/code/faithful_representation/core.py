"""Constructive finite constraint representations and independently replayed traces.

Fuel counts admitted transport steps and candidate checks, not wall-clock time.
An explicit increased total ceiling on resume is a recorded grant; re-entry
does not reset consumption. Hashes bind records, not the truth of their claims.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from copy import deepcopy
from pathlib import Path


class AdmissionError(ValueError):
    """Malformed or unbound evidence, never an unsatisfiability certificate."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


def fields(value, keys):
    require(type(value) is dict and set(value) == set(keys), "unexpected object fields")


def nat(value):
    require(type(value) is int and value >= 0, "expected natural number")
    return value


def strings(value, unique=False):
    require(type(value) is list and all(type(x) is str for x in value), "expected strings")
    if unique:
        require(len(value) == len(set(value)), "duplicate string")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def constant(value):
        raise AdmissionError(f"nonfinite JSON constant: {value}")

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=pairs, parse_constant=constant)


def admit(problem):
    fields(problem, ("schema_version", "goal", "variables", "relations",
                     "assumptions", "authorization"))
    require(type(problem["schema_version"]) is int and problem["schema_version"] == 1,
            "unsupported problem version")
    require(problem["goal"] == "exists_global_assignment", "unsupported goal")
    strings(problem["assumptions"], True)
    strings(problem["authorization"], True)
    require(type(problem["variables"]) is list and type(problem["relations"]) is list,
            "expected variable/relation lists")
    domains = {}
    for variable in problem["variables"]:
        fields(variable, ("name", "domain"))
        name = variable["name"]
        require(type(name) is str and name not in domains, "duplicate/invalid variable")
        domains[name] = strings(variable["domain"], True)
    names = set()
    for relation in problem["relations"]:
        fields(relation, ("name", "scope", "rows"))
        name = relation["name"]
        require(type(name) is str and name not in names, "duplicate/invalid relation")
        names.add(name)
        scope = strings(relation["scope"], True)
        require(set(scope) <= domains.keys(), "unknown scoped variable")
        require(type(relation["rows"]) is list, "expected rows")
        seen = set()
        for row in relation["rows"]:
            strings(row)
            require(len(row) == len(scope), "row arity")
            require(all(x in domains[v] for v, x in zip(scope, row)), "value outside domain")
            require(tuple(row) not in seen, "duplicate row")
            seen.add(tuple(row))
    return deepcopy(problem)


def solution(problem, assignment):
    """Direct original-input predicate; does not use the defect evaluator."""
    domains = {v["name"]: v["domain"] for v in problem["variables"]}
    return (type(assignment) is dict and set(assignment) == set(domains)
            and all(type(assignment[v]) is str and assignment[v] in d for v, d in domains.items())
            and all([assignment[v] for v in r["scope"]] in r["rows"]
                    for r in problem["relations"]))


def assignments(problem):
    names = [v["name"] for v in problem["variables"]]
    for values in itertools.product(*(v["domain"] for v in problem["variables"])):
        yield dict(zip(names, values))


def _join(left, right, order):
    scope = [v for v in order if v in left["scope"] or v in right["scope"]]
    rows = set()
    for a, b in itertools.product(left["rows"], right["rows"]):
        x, y = dict(zip(left["scope"], a)), dict(zip(right["scope"], b))
        if all(x[v] == y[v] for v in x.keys() & y.keys()):
            rows.add(tuple((x | y)[v] for v in scope))
    return scope, [list(row) for row in sorted(rows)]


def apply_change(problem, spec):
    """Only four constructive, goal-preserving presentation operations are admitted."""
    source = admit(problem)
    require(type(spec) is dict and type(spec.get("kind")) is str, "invalid transport")
    target = deepcopy(source)
    variables = {v["name"]: v["domain"] for v in source["variables"]}
    relations = {r["name"]: r for r in source["relations"]}
    kind = spec["kind"]
    if kind == "rename":
        fields(spec, ("kind", "variables", "values"))
        fields(spec["variables"], variables)
        fields(spec["values"], variables)
        strings(list(spec["variables"].values()), True)
        for v, domain in variables.items():
            fields(spec["values"][v], domain)
            strings(list(spec["values"][v].values()), True)
        target["variables"] = [{"name": spec["variables"][v],
                                "domain": [spec["values"][v][x] for x in domain]}
                               for v, domain in variables.items()]
        for relation in target["relations"]:
            old_scope = relation["scope"]
            relation["rows"] = [[spec["values"][v][x] for v, x in zip(old_scope, row)]
                                for row in relation["rows"]]
            relation["scope"] = [spec["variables"][v] for v in old_scope]
    elif kind == "join":
        fields(spec, ("kind", "left", "right", "name"))
        require(spec["left"] in relations and spec["right"] in relations
                and spec["left"] != spec["right"], "join requires distinct relations")
        removed = {spec["left"], spec["right"]}
        require(type(spec["name"]) is str and spec["name"] not in set(relations) - removed,
                "join name collision")
        scope, rows = _join(relations[spec["left"]], relations[spec["right"]], variables)
        target["relations"] = [r for r in target["relations"] if r["name"] not in removed]
        target["relations"].append({"name": spec["name"], "scope": scope, "rows": rows})
    elif kind == "split":
        fields(spec, ("kind", "relation", "components", "names"))
        require(spec["relation"] in relations, "missing split relation")
        original = relations[spec["relation"]]
        require(type(spec["components"]) is list and len(spec["components"]) == 2,
                "binary decomposition required")
        strings(spec["names"], True)
        require(len(spec["names"]) == 2, "two component names required")
        require(not (set(spec["names"]) & (set(relations) - {spec["relation"]})),
                "split name collision")
        parts = []
        for name, scope in zip(spec["names"], spec["components"]):
            strings(scope, True)
            require(set(scope) <= set(original["scope"]), "split scope outside relation")
            positions = [original["scope"].index(v) for v in scope]
            rows = sorted({tuple(row[i] for i in positions) for row in original["rows"]})
            parts.append({"name": name, "scope": scope, "rows": [list(r) for r in rows]})
        require(set(parts[0]["scope"]) | set(parts[1]["scope"]) == set(original["scope"]),
                "split omits variables")
        _, reconstructed = _join(*parts, original["scope"])
        require({tuple(r) for r in reconstructed} == {tuple(r) for r in original["rows"]},
                "lossy decomposition creates spurious rows")
        target["relations"] = [r for r in target["relations"] if r["name"] != spec["relation"]] + parts
    elif kind == "auxiliary":
        fields(spec, ("kind", "name", "domain", "scope", "rows", "relation"))
        require(type(spec["name"]) is str and spec["name"] not in variables, "auxiliary name collision")
        require(type(spec["relation"]) is str and spec["relation"] not in relations,
                "auxiliary relation collision")
        strings(spec["domain"], True)
        strings(spec["scope"], True)
        require(set(spec["scope"]) <= variables.keys(), "auxiliary scope outside carrier")
        require(type(spec["rows"]) is list, "auxiliary rows")
        function = {}
        for row in spec["rows"]:
            strings(row)
            require(len(row) == len(spec["scope"]) + 1, "auxiliary row arity")
            key = tuple(row[:-1])
            require(key not in function and row[-1] in spec["domain"], "auxiliary not a function")
            function[key] = row[-1]
        require(set(function) == set(itertools.product(*(variables[v] for v in spec["scope"]))),
                "auxiliary function is not total on declared inputs")
        target["variables"].append({"name": spec["name"], "domain": spec["domain"]})
        target["relations"].append({"name": spec["relation"],
                                    "scope": spec["scope"] + [spec["name"]], "rows": spec["rows"]})
    else:
        raise AdmissionError("unsupported presentation change")
    return admit(target)


def forward(assignment, spec):
    if spec["kind"] == "rename":
        return {spec["variables"][v]: spec["values"][v][x] for v, x in assignment.items()}
    if spec["kind"] == "auxiliary":
        key = [assignment[v] for v in spec["scope"]]
        value = next(row[-1] for row in spec["rows"] if row[:-1] == key)
        return assignment | {spec["name"]: value}
    return dict(assignment)


def backward(assignment, spec):
    if spec["kind"] == "rename":
        return {v: next(x for x, y in spec["values"][v].items() if y == assignment[new])
                for v, new in spec["variables"].items()}
    if spec["kind"] == "auxiliary":
        return {v: x for v, x in assignment.items() if v != spec["name"]}
    return dict(assignment)


def encode(problem, changes=()):
    root = admit(problem)
    current = root
    steps = []
    parent = digest(root)
    for spec in changes:
        target = apply_change(current, spec)
        step = {"source": digest(current), "target": digest(target),
                "parent": parent, "spec": deepcopy(spec)}
        step["hash"] = digest(step)
        steps.append(step)
        parent = step["hash"]
        current = target
    local = deepcopy(current["relations"])
    covered = {v for r in local for v in r["scope"]}
    names = {r["name"] for r in local}
    for variable in current["variables"]:
        if variable["name"] not in covered:
            name = "__domain_" + variable["name"]
            while name in names:
                name = "_" + name
            names.add(name)
            local.append({"name": name, "scope": [variable["name"]],
                          "rows": [[x] for x in variable["domain"]]})
    result = {"schema_version": 1, "problem": root, "problem_hash": digest(root),
              "current": current, "changes": steps, "local_relations": local}
    result["hash"] = digest(result)
    return result


def validate_encoding(encoded):
    fields(encoded, ("schema_version", "problem", "problem_hash", "current", "changes", "local_relations", "hash"))
    require(type(encoded["changes"]) is list, "expected transport list")
    reconstructed = encode(encoded["problem"], [s["spec"] for s in encoded["changes"]])
    require(canonical(encoded) == canonical(reconstructed), "encoding or transport binding mismatch")
    return reconstructed


def family_count(encoded):
    count = 1
    for relation in encoded["local_relations"]:
        count *= len(relation["rows"])
    return count


def family_at(encoded, index):
    require(0 <= nat(index) < family_count(encoded), "candidate index outside enumeration")
    rows = []
    for relation in reversed(encoded["local_relations"]):
        index, digit = divmod(index, len(relation["rows"]))
        rows.append(digit)
    return list(reversed(rows))


def evaluate_family(encoded, candidate):
    require(type(candidate) is list and len(candidate) == len(encoded["local_relations"]), "candidate arity")
    occurrences = {v["name"]: [] for v in encoded["current"]["variables"]}
    for relation, index in zip(encoded["local_relations"], candidate):
        require(nat(index) < len(relation["rows"]), "candidate row outside relation")
        for v, value in zip(relation["scope"], relation["rows"][index]):
            occurrences[v].append(value)
    defect = []
    decoded = {}
    for variable in encoded["current"]["variables"]:
        values = occurrences[variable["name"]]
        require(bool(values), "uncovered variable")
        decoded[variable["name"]] = values[0]
        for value in values[1:]:
            defect.extend(int(value == a) - int(values[0] == a) for a in variable["domain"])
    if any(defect):
        return {"outcome": "INCOMPATIBLE", "defect": defect, "answer": None}
    require(solution(encoded["current"], decoded), "local reconstruction failed")
    for step in reversed(encoded["changes"]):
        decoded = backward(decoded, step["spec"])
    require(solution(encoded["problem"], decoded), "decoded answer fails original problem")
    return {"outcome": "SOLUTION", "defect": defect, "answer": decoded}


def _candidate_result(encoded, candidate):
    try:
        return evaluate_family(encoded, candidate)
    except AdmissionError as error:
        return {"outcome": "INVALID_CANDIDATE", "predicate": str(error), "answer": None}


def _state(encoded):
    return {"transport": 0, "canonical": 0, "proposal": 0, "phase": "proposal", "answer": None}


def _next(encoded, proposals, state):
    if state["answer"] is not None:
        return None
    if state["transport"] < len(encoded["changes"]):
        return "transport", state["transport"], None
    if state["canonical"] == family_count(encoded):
        return None
    if state["phase"] == "proposal" and state["proposal"] < len(proposals):
        return "proposal", state["proposal"], proposals[state["proposal"]]
    return "canonical", state["canonical"], family_at(encoded, state["canonical"])


def _event(encoded, proposals, state, spent, budget, parent):
    next_step = _next(encoded, proposals, state)
    require(next_step is not None, "extra event after terminal result")
    kind, index, candidate = next_step
    result = ({"transport_hash": encoded["changes"][index]["hash"]} if kind == "transport"
              else _candidate_result(encoded, candidate))
    require(kind != "canonical" or result["outcome"] != "INVALID_CANDIDATE",
            "canonical candidate could not be evaluated; exhaustion is unproved")
    event = {"kind": kind, "index": index, "candidate": candidate, "result": result,
             "cost": 1, "spent_after": spent + 1, "budget": budget, "parent": parent}
    event["hash"] = digest(event)
    return event


def _advance(state, event):
    if event["kind"] == "transport":
        state["transport"] += 1
    elif event["kind"] == "proposal":
        state["proposal"] += 1
        state["phase"] = "canonical"
    else:
        state["canonical"] += 1
        state["phase"] = "proposal"
    if event["result"].get("outcome") == "SOLUTION":
        state["answer"] = event["result"]["answer"]


def _genesis(encoded, proposals):
    return digest({"encoding": encoded["hash"], "proposals": proposals})


def _checkpoint(encoded, proposals, state, events, grants):
    return {"encoding": encoded["hash"], "proposals_hash": digest(proposals), "state": deepcopy(state),
            "spent": len(events), "budget": grants[-1]["total"],
            "parent": events[-1]["hash"] if events else _genesis(encoded, proposals)}


def _outcome(encoded, proposals, state, spent, budget):
    if state["answer"] is not None:
        return "Proved", "CERTIFIED_SOLUTION"
    if _next(encoded, proposals, state) is None:
        return "Refuted", "EXHAUSTIVE_FAILURE"
    return "Undetermined", "BUDGET_EXHAUSTED" if spent == budget else "INTERRUPTED"


def _validate_trace(original, certificate):
    fields(certificate, ("schema_version", "encoding", "proposals", "grants", "events",
                         "checkpoint", "status", "reason", "answer", "authority_effect"))
    require(type(certificate["schema_version"]) is int and certificate["schema_version"] == 1,
            "unsupported certificate version")
    require(certificate["authority_effect"] == "None", "authority escalation")
    encoded = validate_encoding(certificate["encoding"])
    require(canonical(admit(original)) == canonical(encoded["problem"]), "wrong original problem/assumptions")
    proposals, events, grants = certificate["proposals"], certificate["events"], certificate["grants"]
    require(type(proposals) is list and type(events) is list and type(grants) is list and grants,
            "invalid trace lists")
    previous_at, previous_total = -1, -1
    for grant in grants:
        fields(grant, ("at", "total"))
        at, total = nat(grant["at"]), nat(grant["total"])
        require(previous_at <= at <= len(events) and total > previous_total and total >= at,
                "fuel reset or invalid grant")
        previous_at, previous_total = at, total
    require(grants[0]["at"] == 0, "missing initial grant")
    state = _state(encoded)
    parent = _genesis(encoded, proposals)
    for i, event in enumerate(events):
        budget = max(g["total"] for g in grants if g["at"] <= i)
        require(i < budget, "operation without fuel")
        expected = _event(encoded, proposals, state, i, budget, parent)
        require(canonical(event) == canonical(expected), "event witness, scheduling, parent or fuel mismatch")
        _advance(state, expected)
        parent = expected["hash"]
    expected_checkpoint = _checkpoint(encoded, proposals, state, events, grants)
    require(canonical(certificate["checkpoint"]) == canonical(expected_checkpoint), "stale/reset checkpoint")
    status, reason = _outcome(encoded, proposals, state, len(events), grants[-1]["total"])
    require(certificate["status"] == status and certificate["reason"] == reason,
            "unsupported terminal claim")
    require(canonical(certificate["answer"]) == canonical(state["answer"]), "substituted answer")
    return state


def check(original_problem, certificate):
    """Replay the supplied witness; never search for a replacement."""
    try:
        state = _validate_trace(original_problem, certificate)
        return {"accepted": True, "status": certificate["status"], "reason": certificate["reason"],
                "answer": state["answer"], "certificate_sha256": digest(certificate),
                "authority_effect": "None"}
    except (AdmissionError, KeyError, TypeError, ValueError, IndexError, StopIteration) as error:
        return {"accepted": False, "status": None, "reason": str(error), "authority_effect": "None"}


def search(encoded, fuel, checkpoint=None, *, proposals=None, max_steps=None):
    """Fuel is a cumulative ceiling. A checkpoint is the entire prior certificate."""
    encoded = validate_encoding(encoded)
    nat(fuel)
    if max_steps is not None:
        nat(max_steps)
    if checkpoint is None:
        proposals = [] if proposals is None else deepcopy(proposals)
        require(type(proposals) is list, "proposals must be a finite replayable list")
        canonical(proposals)
        events, grants, state = [], [{"at": 0, "total": fuel}], _state(encoded)
    else:
        state = _validate_trace(encoded["problem"], checkpoint)
        require(encoded["hash"] == checkpoint["encoding"]["hash"], "checkpoint belongs to another encoding")
        require(checkpoint["status"] == "Undetermined", "terminal traces cannot resume")
        if proposals is not None:
            require(canonical(proposals) == canonical(checkpoint["proposals"]), "changed proposal queue")
        proposals = deepcopy(checkpoint["proposals"])
        events, grants = deepcopy(checkpoint["events"]), deepcopy(checkpoint["grants"])
        require(fuel >= grants[-1]["total"], "fuel reset")
        if fuel > grants[-1]["total"]:
            grants.append({"at": len(events), "total": fuel})
    start = len(events)
    while len(events) < fuel and (max_steps is None or len(events) - start < max_steps):
        if _next(encoded, proposals, state) is None:
            break
        parent = events[-1]["hash"] if events else _genesis(encoded, proposals)
        event = _event(encoded, proposals, state, len(events), fuel, parent)
        events.append(event)
        _advance(state, event)
    status, reason = _outcome(encoded, proposals, state, len(events), fuel)
    return {"schema_version": 1, "encoding": encoded, "proposals": proposals, "grants": grants,
            "events": events, "checkpoint": _checkpoint(encoded, proposals, state, events, grants),
            "status": status, "reason": reason, "answer": state["answer"], "authority_effect": "None"}


def replay(run_directory):
    directory = Path(run_directory)
    return check(load(directory / "problem.json"), load(directory / "certificate.json"))
