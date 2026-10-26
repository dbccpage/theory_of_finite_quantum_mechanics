"""Offline source-bound records; replay never invokes the proposal producer."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import stat
from pathlib import Path

from .checker import check_certificate
from .fixtures import cheaper_route
from .model import digest, fields, graph_model

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = Path(__file__).resolve().parent / "evidence"


EXPECTED_CASES = {'two_step_optimum': True, 'dead_end_loss': True, 'winning_losing_detour': True, 'terminal_success': True, 'guard_retains_route': True, 'guard_destroys_route': True, 'classification_with_loop': True, 'identification_blind_loop': True, 'forged_live_stall': False, 'forged_terminal_shift': False, 'forged_omitted_initial': False, 'forged_successful_stall': False, 'forged_omitted_model_target': False, 'forged_wrong_task': False, 'forged_float_witness': False}

def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError(f"nonfinite JSON literal: {value}")


def strict_json(raw: bytes):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_object, parse_constant=_nonfinite)


def regular(path: Path) -> bytes:
    for parent in path.parents:
        info = parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular replay parent: {parent}")
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"non-regular replay input: {path}")
    return path.read_bytes()


def sources():
    names = sorted(f"code/certified_progress/{p.name}" for p in Path(__file__).parent.glob("*.py"))
    names += ["lean4/WitnessedDifference/CertifiedProgress.lean",
              "lean4/WitnessedDifference/BeliefGameQuotient.lean"]
    return {name: hashlib.sha256(regular(ROOT / name)).hexdigest() for name in names}


def _write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        regular(path)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8", newline="\n")


def write_evidence(directory: Path = EVIDENCE):
    # The producer belongs only to evidence generation, never replay.
    from .producer import solve_progress

    snapshot = sources()
    models = {
        "two_step_optimum": cheaper_route(),
        "dead_end_loss": graph_model({"s": [("go", "1", ["d"])]}),
        "winning_losing_detour": graph_model({"s": [("finish", "2", ["t"]),
                                                     ("bad", "1", ["u"])],
                                             "u": [("go", "1", ["d"])]}),
        "terminal_success": graph_model({"s": []}, targets=("s", "t")),
        "guard_retains_route": graph_model({"s": [("repair", "1", ["u"])],
                                            "u": [("emit", "1", ["t"])]}),
        "guard_destroys_route": graph_model({"s": [("guard", "1", ["s"])]}),
        "classification_with_loop": graph_model({"s": [("emit", "1/2", ["t"]),
                                                       ("unhelpful", "1", ["s"])]}),
        "identification_blind_loop": graph_model({"s": [("blind", "1", ["s"])]}),
    }
    records = []
    certificates = {}

    def retain(name, model, certificate, expected):
        receipt = check_certificate(model, certificate)
        if receipt["accepted"] is not expected:
            raise ValueError(f"unexpected outcome for {name}: {receipt}")
        records.append({"name": name, "model": model, "certificate": certificate,
                        "receipt": receipt, "expected_acceptance": expected})

    for name, model in models.items():
        cert = solve_progress(model)["certificate"]
        certificates[name] = cert
        retain(name, model, cert, True)
    cert = copy.deepcopy(certificates["two_step_optimum"])
    cert.update(winning=[["s"], ["t"]], losing=[["u"]], stalled=[["u"]])
    retain("forged_live_stall", models["two_step_optimum"], cert, False)
    shifted_model = graph_model({"s": [("finish", "1", ["t"])]})
    cert = solve_progress(shifted_model)["certificate"]
    for row in cert["values"]:
        row["value"] = "101" if row["belief"] == ["s"] else "100"
    retain("forged_terminal_shift", shifted_model, cert, False)
    cert = copy.deepcopy(certificates["guard_destroys_route"])
    cert.update(kind="WIN_OPTIMAL", optimality_requested=True)
    retain("forged_omitted_initial", models["guard_destroys_route"], cert, False)
    cert = copy.deepcopy(certificates["terminal_success"])
    cert.update(kind="LOSS", optimality_requested=False, winning=[], losing=[["s"]],
                stalled=[["s"]], strategy=[], values=[], ranks=[], resolutions=[])
    retain("forged_successful_stall", models["terminal_success"], cert, False)
    extra_terminal = graph_model({"s": [("choose", "1", ["t", "u"])]}, targets=("t", "u"))
    cert = solve_progress(extra_terminal)["certificate"]
    cert.update(kind="LOSS", optimality_requested=False, winning=[], losing=[["s"], ["u"]],
                stalled=[["u"]], closure=[{"belief": ["s"], "action": "choose", "successor": ["u"]}],
                strategy=[], values=[], ranks=[], resolutions=[])
    retain("forged_omitted_model_target", extra_terminal, cert, False)
    cert = copy.deepcopy(certificates["two_step_optimum"])
    cert["task_id"] = "different-original-question"
    retain("forged_wrong_task", models["two_step_optimum"], cert, False)
    cert = copy.deepcopy(certificates["two_step_optimum"])
    cert["values"][0]["value"] = 2.0
    retain("forged_float_witness", models["two_step_optimum"], cert, False)
    payload = {"schema": "wdp-progress-offline-evidence-v1", "sources": snapshot,
               "records": records, "authority_effect": "None", "provider_calls": 0}
    if sources() != snapshot:
        raise ValueError("source changed while generating evidence")
    _write(directory / "records.json", payload)
    return replay(directory)


def replay(directory: Path = EVIDENCE):
    path = directory / "records.json"
    raw = regular(path)
    payload = fields(strict_json(raw), {"schema", "sources", "records", "authority_effect", "provider_calls"})
    if payload.get("schema") != "wdp-progress-offline-evidence-v1":
        raise ValueError("unknown replay schema")
    snapshot = sources()
    if payload["sources"] != snapshot:
        raise ValueError("replay source bindings changed")
    if type(payload["records"]) is not list or payload["authority_effect"] != "None" or type(payload["provider_calls"]) is not int or payload["provider_calls"] != 0:
        raise ValueError("malformed offline evidence metadata")
    names = set()
    accepted = rejected = 0
    for record in payload["records"]:
        fields(record, {"name", "model", "certificate", "receipt", "expected_acceptance"})
        if type(record["name"]) is not str or not record["name"]:
            raise ValueError("missing record name")
        if record["name"] in names or type(record["expected_acceptance"]) is not bool:
            raise ValueError("duplicate record or malformed expected outcome")
        if record["name"] not in EXPECTED_CASES or record["expected_acceptance"] is not EXPECTED_CASES[record["name"]]:
            raise ValueError("unexpected fixture name or acceptance expectation")
        names.add(record["name"])
        receipt = check_certificate(record["model"], record["certificate"])
        if receipt["accepted"] is not record["expected_acceptance"] or digest(receipt) != digest(record["receipt"]):
            raise ValueError(f"replay mismatch: {record['name']}")
        accepted += receipt["accepted"]
        rejected += not receipt["accepted"]
    if names != set(EXPECTED_CASES) or sources() != snapshot or regular(path) != raw:
        raise ValueError("incomplete fixture inventory or bytes changed during replay")
    return {"status": "PASS", "records": len(names), "accepted": accepted,
            "rejected": rejected, "provider_calls": 0, "authority_effect": "None"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--directory", type=Path, default=EVIDENCE)
    args = parser.parse_args()
    print(json.dumps(write_evidence(args.directory) if args.write else replay(args.directory), sort_keys=True))


if __name__ == "__main__":
    main()
