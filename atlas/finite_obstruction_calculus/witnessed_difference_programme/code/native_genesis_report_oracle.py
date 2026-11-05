"""Independent PAPER reference replay of original Genesis admission source.

Production mathematics lives in omega_wdp. This oracle loads the preserved
Genesis source, checks whole retained states, and checks the defining relations
of report/global/repair results rather than copying the native search policy.
It makes no passage-model or unrestricted-continuation claim.
Run this reference from the monorepo: it requires the sibling preserved Genesis
package and refuses to import if that source is absent from a standalone copy.
AuthorityEffect: None.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parents[2] / "genesis/code/derivation"
SOURCE_PATH = SOURCE_DIR / "model.py"


def _original():
    name = "_wdp_preserved_genesis_admission"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, SOURCE_DIR / "__init__.py", submodule_search_locations=[str(SOURCE_DIR)]
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("original Genesis package unavailable")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return importlib.import_module(name + ".model")


MODEL = _original()


def original_l_history():
    """The actual preserved engine.GENESIS_L input, not a replacement fixture."""
    engine = importlib.import_module(MODEL.__package__ + ".engine")
    names = {"Supply": "supply", "AdmitDatum": "admit_datum"}
    return [{"kind": names[type(e).__name__], "token": e.token} for e in engine.GENESIS_L]


def _event(event):
    constructors = {
        "supply": MODEL.Supply,
        "admit_datum": MODEL.AdmitDatum,
        "admit_form": MODEL.AdmitForm,
        "admit_inst": MODEL.AdmitInst,
        "admit_rule_all": MODEL.AdmitRuleAll,
        "impose": MODEL.Impose,
    }
    fields = {k: v for k, v in event.items() if k != "kind"}
    for key, value in fields.items():
        if key in {"form", "arity", "i", "j"} and (type(value) is not int or value < 0):
            raise ValueError("wire requires natural-number indices")
        if key == "args":
            if any(type(v) is not int or v < 0 for v in value):
                raise ValueError("wire requires natural-number arguments")
            fields[key] = tuple(value)
    return constructors[event["kind"]](**fields)


def replay(events):
    if events and events[0] != {"kind": "supply", "token": "<>"}:
        raise MODEL.AdmissionError("selected profile requires literal root")
    return MODEL.replay([_event(e) for e in events])


def state_fields(state):
    return {
        "data": list(state.data),
        "forms": list(state.forms),
        "instances": [{"form": f, "args": list(args)} for f, args in sorted(state.insts)],
        "rules": sorted(state.rules),
        "requirements": [list(p) for p in sorted(state.reqs)],
    }


def answer(state, events, question):
    kind = question["kind"]
    counts = {
        "datum_count": len(state.data),
        "form_count": len(state.forms),
        "instance_count": len(state.insts),
        "rule_count": len(state.rules),
        "requirement_count": len(state.reqs),
        "event_count": len(events),
    }
    if kind in counts:
        return {"kind": "count", "value": counts[kind]}
    value = question["value"]
    if kind == "has_datum":
        return {"kind": "boolean", "value": value in state.data}
    if kind != "derivable":
        raise ValueError("unknown question")
    form, args = value["form"], tuple(value["args"])
    if not (
        0 <= form < len(state.forms)
        and len(args) == state.forms[form]
        and all(0 <= i < len(state.data) for i in args)
    ):
        return {"kind": "unavailable"}
    observe = importlib.import_module(MODEL.__package__ + ".observe")
    return {"kind": "boolean", "value": observe.derivable(state, (form, args))}


def profile(events, request):
    row = []
    for word in request["continuations"]:
        extended = events + word["events"]
        try:
            state = replay(extended)
        except MODEL.AdmissionError:
            row.extend(
                [{"kind": "boolean", "value": False}]
                + [{"kind": "unavailable"} for _ in request["questions"]]
            )
        else:
            row.append({"kind": "boolean", "value": True})
            row.extend(answer(state, extended, q["question"]) for q in request["questions"])
    return row


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _key(answer):
    return ({"boolean": 0, "count": 1, "unavailable": 2}[answer["kind"]], answer.get("value", 0))


def check_decision(reports, answers, decision):
    if decision["kind"] == "decoder":
        entries = decision["entries"]
        _require(len({r for r, _ in entries}) == len(entries), "duplicate decoder key")
        decoder = dict(entries)
        _require(set(decoder) == set(reports), "decoder image mismatch")
        _require(
            all(decoder[r] == a for r, a in zip(reports, answers, strict=True)), "decoder equation"
        )
    else:
        i, j = decision["first"], decision["second"]
        _require(0 <= i < len(reports) and 0 <= j < len(reports), "collision indices")
        _require(reports[i] == reports[j] == decision["report"], "collision report")
        _require(
            answers[i] == decision["first_answer"]
            and answers[j] == decision["second_answer"]
            and answers[i] != answers[j],
            "collision answers",
        )


def check_global(rows, request, candidate):
    if request is None:
        _require(candidate is None, "undeclared global task")
        return
    columns = request["observed_columns"]
    full = (1 << len(columns)) - 1
    profiles = {}
    for context in request["contexts"]:
        projected = [[row[c] for i, c in enumerate(columns) if context & (1 << i)] for row in rows]
        if context == full:
            profiles[context] = projected
        else:
            distinct = {tuple(_key(a) for a in row): row for row in projected}
            profiles[context] = [distinct[k] for k in sorted(distinct)]
    _require(
        candidate["profiles"] == [[c, profiles[c]] for c in sorted(profiles)],
        "restriction profile mismatch",
    )
    fiber = []
    for i, row in enumerate(rows):
        matches = True
        for context, local in zip(request["cover"], request["locals"], strict=True):
            if context == full:
                matches &= i == local
            else:
                matches &= [
                    row[c] for j, c in enumerate(columns) if context & (1 << j)
                ] == profiles[context][local]
        if matches:
            fiber.append(i)
    _require(candidate["histories"] == fiber, "incomplete original source fiber")
    fact = candidate["fact"]
    if not fiber:
        _require(fact == {"kind": "no_global_extension"}, "vacuous fact")
        return
    values = [rows[i][request["fact_column"]] for i in fiber]
    if any(value != values[0] for value in values):
        _require(fact["kind"] == "undetermined", "ambiguous answer claimed definite")
        a, b = fact["first"], fact["second"]
        _require(
            a in fiber
            and b in fiber
            and rows[a][request["fact_column"]] != rows[b][request["fact_column"]],
            "bad ambiguity witness",
        )
    elif values[0]["kind"] == "unavailable":
        _require(fact == {"kind": "unavailable"}, "unavailable answer certified")
    else:
        _require(fact == {"kind": "certified", "answer": values[0]}, "wrong factual answer")


def check_result(request, candidate):
    """Check the actual original-source equations; no native host invocation."""
    events = [h["events"] for h in request["histories"]]
    _require(
        candidate["states"] == [state_fields(replay(h)) for h in events],
        "retained source fields differ",
    )
    rows = [profile(h, request) for h in events]
    _require(candidate["answers"] == rows, "protected answers differ")
    classes = candidate["class_of"]
    _require(len(classes) == len(rows), "quotient row count")
    _require(
        len(candidate["profiles"]) == len({tuple(_key(a) for a in row) for row in rows}),
        "unrealized or duplicate quotient profile",
    )
    _require(
        all(candidate["profiles"][c] == row for c, row in zip(classes, rows, strict=True)),
        "quotient decoder",
    )
    for i in range(len(rows)):
        for j in range(len(rows)):
            _require((classes[i] == classes[j]) == (rows[i] == rows[j]), "not the minimal quotient")
    check_decision(request["report"], rows, candidate["report"])
    _require(len(candidate["operations"]) == len(request["continuations"]), "missing operation")
    for word, operation in zip(request["continuations"], candidate["operations"], strict=True):
        targets = []
        for h in events:
            extended = h + word["events"]
            try:
                replay(extended)
            except MODEL.AdmissionError:
                targets.append(None)
            else:
                targets.append(profile(extended, request))
        _require(operation["continuation"] == word["id"], "operation identity")
        check_decision(classes, targets, operation["decision"])
    check_global(rows, request["global"], candidate["global"])
    repair = candidate["repair"]
    if request["repair"] is None:
        _require(repair is None, "undeclared repair")
        return
    partitions = repair["partitions"]
    _require(
        len(partitions)
        == len(repair["steps"]) + 1
        == len(repair["ranks"])
        == len(repair["global_rechecks"]),
        "repair trace lengths",
    )
    final_count = len(set(partitions[-1]))
    for index, part in enumerate(partitions):
        _require(len(part) == len(rows), "repair row count")
        _require(repair["ranks"][index] == final_count - len(set(part)), "wrong progress rank")
        check_global(rows, request["global"], repair["global_rechecks"][index])
        previous = request["report"] if index == 0 else partitions[index - 1]
        if index:
            a, b, q = repair["steps"][index - 1]
            _require(
                previous[a] == previous[b] and rows[a][q] != rows[b][q], "not a lost distinction"
            )
            _require(repair["ranks"][index] < repair["ranks"][index - 1], "no progress")
        for i in range(len(rows)):
            for j in range(len(rows)):
                same = previous[i] == previous[j]
                if index and previous[i] == previous[a]:
                    same &= rows[i][q] == rows[j][q]
                _require((part[i] == part[j]) == same, "not the licensed one-class split")
                if index == len(partitions) - 1:
                    expected = request["report"][i] == request["report"][j] and rows[i] == rows[j]
                    _require((part[i] == part[j]) == expected, "not least sufficient")
