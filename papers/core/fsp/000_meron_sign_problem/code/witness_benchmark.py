"""Finite, answer-free orbit tasks backed by the package's existing exact model.

The task supplies complete signs, weights and graph edges. It measures recovery
of finite witnesses from those inputs, not discovery of a physical mechanism.
Historical prompt builders and pilot evidence are left intact.
"""
from __future__ import annotations

import hashlib
import json

from meron_exact_model import meron_database, rational

GRAPH_IDS = (63, 3, 255, 15)
ATOM_NAMES = "abcdefghijklmnop"


def canonical_digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def build_tasks(q: str = "5/2") -> tuple[dict, dict]:
    """Read four complete orbits; keep computed answers out of public inputs."""
    q_value = rational(q)
    if q_value <= 1:
        raise ValueError("these tasks require positive breakup weights: q > 1")
    con = meron_database(4, 2, str(q_value))
    tasks = []
    answers = {}
    try:
        for task_id, gid in zip("abcd", GRAPH_IDS, strict=True):
            rows = con.execute(
                "SELECT mask,sign,weight FROM meron_configuration WHERE gid=? ORDER BY mask",
                (gid,),
            ).fetchall()
            components = []
            for cluster, in con.execute(
                "SELECT DISTINCT cluster FROM meron_component WHERE gid=? ORDER BY cluster",
                (gid,),
            ):
                components.append([
                    ATOM_NAMES[node] for node, in con.execute(
                        "SELECT node FROM meron_component WHERE gid=? AND cluster=? ORDER BY node",
                        (gid, cluster),
                    )
                ])
            edges = [
                ATOM_NAMES[u] + ">" + ATOM_NAMES[v]
                for u, v in con.execute(
                    "SELECT DISTINCT source,target FROM meron_edge WHERE gid=? ORDER BY source,target",
                    (gid,),
                )
            ]
            signs = [sign for _, sign, _ in rows]
            weights = {weight for _, _, weight in rows}
            if len(weights) != 1:
                raise ValueError("unequal orbit weights")
            weight = weights.pop()
            reversing = [
                bit for bit in range(len(components))
                if all(signs[mask ^ (1 << bit)] == -signs[mask] for mask in range(len(signs)))
            ]
            pairs = (
                [[mask, mask ^ (1 << reversing[0])] for mask in range(len(signs))
                 if mask < (mask ^ (1 << reversing[0]))]
                if reversing else []
            )
            tasks.append({
                "id": task_id, "nodes": ATOM_NAMES, "edges": edges,
                "weight": weight, "signs": signs,
            })
            answers[task_id] = {
                "id": task_id, "components": components, "reversing": reversing,
                "pairs": pairs, "total": str(sum(signs) * rational(weight)),
            }
    finally:
        con.close()
    return {"protocol": "finite-orbit-witness-v1", "tasks": tasks}, answers


def make_prompt(packet: dict) -> str:
    """Give full inputs and a response contract; omit computed target quantities."""
    return (
        "Recover witnesses for four finite graph inputs. Each a>b is an edge; "
        "connected components are ordered by their least node, and their members "
        "are in node order. Bits of mask m select components in that order. "
        "signs[m] is the complete supplied sign table, indexed from zero; every "
        "orientation has the supplied exact rational weight.\n"
        "For each input return its components, every bit whose flip reverses the "
        "sign for every mask, a disjoint partition of all masks into equal-weight "
        "opposite-sign pairs if any such bit exists (otherwise []), and the exact "
        "signed sum total. Compute these from the supplied inputs.\n"
        'Return only {"answers":[{"id":"a","components":[["node",...],...],'
        '"reversing":[integer,...],"pairs":[[integer,integer],...],'
        '"total":"reduced integer or fraction string"},...]} with no extra keys.\n'
        + json.dumps(packet, separators=(",", ":"), sort_keys=True)
    )


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate response key")
        result[key] = value
    return result


def parse_response(raw: str) -> object:
    if len(raw.encode("utf-8")) > 262144:
        raise ValueError("response exceeds finite input bound")
    return json.loads(raw, object_pairs_hook=_no_duplicates)


def score_response(packet: dict, expected: dict, raw: str) -> dict:
    """Check complete finite pair witnesses; prose and truthy flags earn no credit."""
    try:
        response = parse_response(raw)
    except (ValueError, TypeError, RecursionError):
        return {"valid": False, "errors": ["invalid_json"], "cases": []}
    if type(response) is not dict or set(response) != {"answers"}:
        return {"valid": False, "errors": ["response_shape"], "cases": []}
    answers = response["answers"]
    if type(answers) is not list or len(answers) != len(packet["tasks"]):
        return {"valid": False, "errors": ["case_coverage"], "cases": []}
    reported = {}
    for answer in answers:
        if type(answer) is not dict or type(answer.get("id")) is not str:
            return {"valid": False, "errors": ["case_shape"], "cases": []}
        if answer["id"] in reported:
            return {"valid": False, "errors": ["duplicate_case"], "cases": []}
        reported[answer["id"]] = answer
    if set(reported) != set(expected):
        return {"valid": False, "errors": ["case_identity"], "cases": []}
    results = []
    for task in packet["tasks"]:
        task_id = task["id"]
        answer = reported[task_id]
        truth = expected[task_id]
        errors = []
        if set(answer) != {"id", "components", "reversing", "pairs", "total"}:
            errors.append("case_shape")
        if answer.get("components") != truth["components"]:
            errors.append("components")
        reversing = answer.get("reversing")
        if (type(reversing) is not list or any(type(bit) is not int for bit in reversing)
                or reversing != truth["reversing"]):
            errors.append("reversing_bits")
        total = answer.get("total")
        try:
            total_valid = type(total) is str and total == str(rational(total))
            total_valid = total_valid and rational(total) == rational(truth["total"])
        except (ValueError, TypeError, ZeroDivisionError):
            total_valid = False
        if not total_valid:
            errors.append("total")
        pairs = answer.get("pairs")
        seen = set()
        pair_valid = type(pairs) is list
        if pair_valid:
            for pair in pairs:
                if (type(pair) is not list or len(pair) != 2
                        or any(type(mask) is not int for mask in pair)):
                    pair_valid = False
                    break
                left, right = pair
                if (left in seen or right in seen or left == right
                        or not 0 <= left < len(task["signs"])
                        or not 0 <= right < len(task["signs"])):
                    pair_valid = False
                    break
                if task["signs"][left] != -task["signs"][right]:
                    pair_valid = False
                    break
                seen.update(pair)
            required = set(range(len(task["signs"]))) if truth["reversing"] else set()
            pair_valid = pair_valid and seen == required
        if not pair_valid:
            errors.append("pair_witness")
        results.append({"id": task_id, "valid": not errors, "errors": errors})
    return {"valid": all(case["valid"] for case in results), "errors": [], "cases": results}


def positive_control(expected: dict) -> str:
    return json.dumps({"answers": list(expected.values())}, separators=(",", ":"))
