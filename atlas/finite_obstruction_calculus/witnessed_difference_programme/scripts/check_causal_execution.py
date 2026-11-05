"""Compose P.14--P.16 admission, token frames and prices with actual Rust replay.

The bounded all-order certificate is deliberately exhaustive (at most 8 events
and 10000 schedules). A receipt is a proposal: verification reexecutes the
configured, source-bound omega_wdp owner. There is no Python execution fallback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import stat
from pathlib import Path, PurePosixPath

if __package__:
    from .check_ideal_prices import ExactPrices, analyze_prices
else:  # Direct standalone invocation from the scripts directory.
    from check_ideal_prices import ExactPrices, analyze_prices


class CertificateRefusal(ValueError):
    """Malformed, mismatched, illegal or unprotected certificate."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise CertificateRefusal(reason)


def encoded(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def same(left: object, right: object) -> bool:
    return encoded(left) == encoded(right)


def regular_path(path: Path) -> Path:
    path = path.absolute()
    for part in reversed((path, *path.parents)):
        mode = part.lstat()
        require(not stat.S_ISLNK(mode.st_mode)
                and not getattr(mode, "st_file_attributes", 0) & 0x400,
                f"linked custody path: {part}")
        require(stat.S_ISREG(mode.st_mode) if part == path else stat.S_ISDIR(mode.st_mode),
                f"nonregular custody path: {part}")
    return path


def sha(path: Path) -> str:
    return hashlib.sha256(regular_path(path).read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key: {key}")
            result[key] = value
        return result

    def bad_number(value):
        raise CertificateRefusal(f"nonintegral JSON number: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=object_pairs,
                      parse_float=bad_number, parse_constant=bad_number)


def fields(value: object, names: set[str], where: str) -> None:
    require(type(value) is dict and set(value) == names, f"{where}: field mismatch")


def natural(value: object, where: str) -> int:
    require(type(value) is int and value >= 0, f"{where}: expected natural integer")
    return value


def integer_text(value: object) -> int:
    require(type(value) is str and len(value) < 1000, "expected canonical integer string")
    try:
        result = int(value)
    except ValueError as exc:
        raise CertificateRefusal("invalid integer string") from exc
    require(str(result) == value, "noncanonical integer string")
    return result


class NativeOwner:
    """Explicit executable plus independently supplied build/source custody."""

    def __init__(self, binary: Path, build_receipt: Path, source_root: Path):
        self.binary = regular_path(binary)
        self.source_root = source_root.absolute()
        self.build = read_json(regular_path(build_receipt))
        require(self.build.get("schema") == "wdp-causal-native-build-v1", "unknown native build")
        require(self.build.get("authority_effect") == "None", "native build authority")
        sources = self.build.get("sources")
        require(type(sources) is dict and bool(sources), "native sources absent")
        required = "omega_engine/crates_rs/omega_wdp/src/genesis_source_execution.rs"
        require(required in sources, "actual Source25 native owner not bound")
        self.verify_custody()
        self.calls = 0

    def verify_custody(self) -> None:
        require(sha(self.binary) == self.build["binary_sha256"], "native executable changed")
        for name, expected in self.build["sources"].items():
            require(type(name) is str, "native source path must be text")
            pure = PurePosixPath(name)
            require(bool(pure.parts) and not pure.is_absolute()
                    and pure.as_posix() == name and ".." not in pure.parts
                    and "\\" not in name and ":" not in pure.parts[0],
                    "native source path is not canonical relative text")
            path = self.source_root / name
            require(sha(path) == expected, f"native dependency changed: {name}")
        adapter = Path(__file__).resolve().parent.parent / "code/causal_certificates/native/main.rs"
        require(sha(adapter) == self.build["adapter_sha256"], "native adapter changed")
        require(sha(adapter.with_name("build_native.py")) == self.build["adapter_builder_sha256"],
                "native builder changed")

    @property
    def binding(self) -> dict:
        return {"build_sha256": digest(self.build), "binary_sha256": self.build["binary_sha256"],
                "sources_sha256": digest(self.build["sources"])}

    def replay(self, initial: dict, changes: list[dict]) -> dict:
        self.calls += 1
        try:
            process = subprocess.run([str(self.binary)], input=encoded({"initial": initial, "changes": changes}),
                                     check=False, capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise CertificateRefusal(f"native transport unavailable: {exc}") from exc
        try:
            output = json.loads(process.stdout)
        except ValueError as exc:
            raise CertificateRefusal("native response is not JSON") from exc
        require(process.returncode == 0 and output.get("status") == "PASS",
                f"native refusal: {output.get('reason', process.stderr)}")
        require(output.get("schema") == "wdp-source25-native-v1"
                and output.get("authority_effect") == "None", "native response protocol mismatch")
        run = output["run"]
        require(same(run["changes"], changes), "native descriptor binding mismatch")
        require(len(run["states"]) == len(changes) + 1, "native states omitted")
        return run


PRICES = {"term_additions", "assertion_additions", "source_size_delta", "plain_cost_delta",
          "assertion_source_size_fee"}


def admit_problem(problem: dict) -> tuple[list[dict], list[int]]:
    fields(problem, {"schema", "initial", "initial_tokens", "events", "protected_prices"}, "problem")
    require(problem["schema"] == "wdp-causal-problem-v1", "unknown problem")
    initial = problem["initial"]
    fields(initial, {"terms", "r", "s", "filled"}, "initial state")
    require(type(initial["terms"]) is list and len(initial["terms"]) <= 32, "carrier bound")
    n = len(initial["terms"])
    require(initial["terms"] == [f"t{i}" for i in range(n)], "noncanonical initial labels")
    for name in ("r", "s"):
        require(type(initial[name]) is list and len(initial[name]) == n * n, "count-table shape")
        require(all(integer_text(x) >= 0 for x in initial[name]), "negative count")
    require(type(initial["filled"]) is list, "face array missing")
    tokens = problem["initial_tokens"]
    require(type(tokens) is list and len(tokens) == n and all(type(t) is str and t for t in tokens),
            "initial token domain mismatch")
    require(len(set(tokens)) == n, "duplicate initial token")
    events = problem["events"]
    require(type(events) is list and len(events) <= 8, "event bound: at most eight")
    tags, births = {}, {}
    for e, event in enumerate(events):
        require(type(event) is dict, "event object required")
        kind = event.get("kind")
        expected = {"tag", "kind", "predecessors"}
        if kind == "add_term":
            expected.add("birth")
        elif kind in ("identify", "fill", "remove", "add_assertion"):
            expected.add("tokens")
            if kind in ("remove", "add_assertion"):
                expected.add("relation")
        else:
            raise CertificateRefusal("unknown native edit kind")
        fields(event, expected, "event")
        tag = event["tag"]
        require(type(tag) is str and bool(tag) and tag not in tags, "duplicate/invalid occurrence tag")
        tags[tag] = e
        if kind == "add_term":
            token = event["birth"]
            require(type(token) is str and token and token not in tokens and token not in births,
                    "duplicate/invalid birth name")
            births[token] = e
    before = []
    for e, event in enumerate(events):
        pred = event["predecessors"]
        require(type(pred) is list and all(type(t) is str and t in tags for t in pred),
                "invalid precedence occurrence")
        require(len(set(pred)) == len(pred) and event["tag"] not in pred, "duplicate/self precedence")
        before.append(sum(1 << tags[t] for t in pred))
    for _ in events:
        for e in range(len(events)):
            for p in range(len(events)):
                if before[e] & (1 << p):
                    before[e] |= before[p]
    require(all(not p & (1 << e) for e, p in enumerate(before)), "cyclic precedence")
    for e, event in enumerate(events):
        if event["kind"] == "add_term":
            continue
        refs = event["tokens"]
        expected = 3 if event["kind"] == "fill" else 2
        require(type(refs) is list and len(refs) == expected
                and all(type(t) is str and (t in tokens or t in births) for t in refs), "invalid named endpoints")
        require(all(t not in births or before[e] & (1 << births[t]) for t in refs), "birth-before-use missing")
        if event["kind"] in ("remove", "add_assertion"):
            require(event["relation"] in ("r", "s"), "unknown relation")
    prices = problem["protected_prices"]
    require(type(prices) is list and bool(prices) and all(type(p) is str and p in PRICES for p in prices),
            "unknown protected price")
    require(len(set(prices)) == len(prices), "duplicate price")
    return events, before


def schedules(before: list[int]) -> list[list[int]]:
    result = []
    full = (1 << len(before)) - 1

    def visit(prefix, ideal):
        if ideal == full:
            result.append(prefix)
            require(len(result) <= 10000, "schedule enumeration bound exceeded")
            return
        for e, required in enumerate(before):
            if not ideal & (1 << e) and not required & ~ideal:
                visit(prefix + [e], ideal | (1 << e))

    visit([], 0)
    require(bool(result), "no poset schedule")
    return result


def descriptors(problem: dict, order: list[int]) -> tuple[list[dict], list[dict[str, int]]]:
    labels = dict(zip(problem["initial_tokens"], range(len(problem["initial_tokens"]))))
    maps, changes = [labels.copy()], []
    size = len(labels)
    for e in order:
        event = problem["events"][e]
        kind = event["kind"]
        change = {"kind": kind}
        if kind == "add_term":
            labels[event["birth"]] = size
            size += 1
        else:
            values = [labels[t] for t in event["tokens"]]
            if kind == "identify":
                x, y = sorted(values)
                change.update(x=x, y=y)
                # Label bookkeeping only. Native execution, including the
                # x==y refusal, occurs before any certificate is accepted.
                if x != y:
                    labels = {t: x if a == y else a - (a > y) for t, a in labels.items()}
                    size -= 1
            elif kind == "fill":
                k = values.index(min(values))
                values = values[k:] + values[:k]
                change.update(zip(("x", "y", "z"), values))
            else:
                change.update(relation=event["relation"], x=values[0], y=values[1])
        changes.append(change)
        maps.append(labels.copy())
    return changes, maps


def frame(state: dict, labels: dict[str, int], ideal: int) -> dict:
    n = len(state["terms"])
    groups = [sorted(t for t, label in labels.items() if label == i) for i in range(n)]
    require(all(groups), "native token map not surjective")
    ordered = sorted(groups, key=lambda ts: ts[0])
    alignment = [ordered.index(group) for group in groups]
    require(sorted(alignment) == list(range(n)), "token alignment not bijective")
    moved = {}
    for name in ("r", "s"):
        output = ["0"] * (n * n)
        for i in range(n):
            for j in range(n):
                output[alignment[i] * n + alignment[j]] = state[name][i * n + j]
        moved[name] = output
    faces = []
    for face in state["filled"]:
        values = [alignment[i] for i in face]
        k = values.index(min(values))
        faces.append(values[k:] + values[:k])
    return {"ideal": ideal, "token_to_native": dict(sorted(labels.items())),
            "native_to_frame": alignment,
            "boundary": {"ideal": ideal, "token_classes": ordered, **moved, "filled": sorted(faces),
                         "source_size": state["source_size"], "plain_state_cost": state["plain_state_cost"]}}


def execute_order(problem: dict, order: list[int], native: NativeOwner) -> dict:
    changes, maps = descriptors(problem, order)
    run = native.replay(problem["initial"], changes)
    frames, ideal = [], 0
    for i, (state, labels) in enumerate(zip(run["states"], maps)):
        frames.append(frame(state, labels, ideal))
        if i < len(order):
            ideal |= 1 << order[i]
    prices = []
    for i, e in enumerate(order):
        kind = problem["events"][e]["kind"]
        before, after = run["states"][i:i + 2]
        values = {"term_additions": int(kind == "add_term"),
                  "assertion_additions": int(kind == "add_assertion"),
                  "source_size_delta": integer_text(after["source_size"]) - integer_text(before["source_size"]),
                  "plain_cost_delta": integer_text(after["plain_state_cost"]) - integer_text(before["plain_state_cost"]),
                  "assertion_source_size_fee": integer_text(before["source_size"]) if kind == "add_assertion" else 0}
        prices.append([values[p] for p in problem["protected_prices"]])
    expected_additions = [str(sum(change["kind"] == name for change in changes))
                          for name in ("add_term", "add_assertion")]
    require(same(run["addition_price"], expected_additions), "native additions inconsistent")
    return {"order": order, "occurrences": [problem["events"][e]["tag"] for e in order],
            "native": run, "frames": frames, "edge_prices": prices,
            "protected_total": [sum(value[j] for value in prices) for j in range(len(problem["protected_prices"]))]}


def produce_certificate(problem: dict, native: NativeOwner) -> dict:
    events, before = admit_problem(problem)
    orders = schedules(before)
    histories, boundaries, weights = [], {}, {}
    for order in orders:
        history = execute_order(problem, order, native)
        histories.append(history)
        for framed in history["frames"]:
            j = framed["ideal"]
            boundary = framed["boundary"]
            require(j not in boundaries or same(boundaries[j], boundary), "native ideal boundaries disagree")
            boundaries[j] = boundary
        for i, e in enumerate(order):
            edge = (history["frames"][i]["ideal"], e)
            value = tuple(history["edge_prices"][i])
            require(edge not in weights or weights[edge] == value, "price is history dependent")
            weights[edge] = value
    price = analyze_prices(before, weights)
    require(isinstance(price, ExactPrices), "protected price has nonzero diamond curl")
    if not events:
        price = ExactPrices({0: (0,) * len(problem["protected_prices"])})
    native.verify_custody()
    return {"schema": "wdp-causal-execution-v1", "authority_effect": "None",
            "problem_sha256": digest(problem), "native_binding": native.binding,
            "event_tags": [event["tag"] for event in events], "predecessors": before,
            "histories": histories,
            "price_potential": {str(j): list(p) for j, p in price.potential.items()},
            "scope": "all linear extensions of this supplied finite event family"}


def verify_certificate(problem: dict, certificate: dict, native: NativeOwner) -> dict:
    """Reexecute against independent problem input; never repair submitted data."""
    expected = produce_certificate(problem, native)
    require(same(certificate, expected), "execution certificate differs from fresh native replay")
    return {"status": "PASS", "authority_effect": "None", "certificate_sha256": digest(certificate),
            "histories": len(expected["histories"]), "fresh_native_replay": True}


def arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--native-bin", type=Path, required=True)
    parser.add_argument("--native-build-receipt", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("create", "check"))
    parser.add_argument("problem", type=Path)
    parser.add_argument("certificate", type=Path)
    arguments(parser)
    args = parser.parse_args()
    owner = NativeOwner(args.native_bin, args.native_build_receipt, args.source_root)
    problem = read_json(args.problem)
    if args.command == "create":
        require(not args.certificate.exists(), "refusing to overwrite submitted certificate")
        args.certificate.write_text(json.dumps(produce_certificate(problem, owner), indent=2, sort_keys=True) + "\n",
                                    encoding="utf-8", newline="\n")
    else:
        print(encoded(verify_certificate(problem, read_json(args.certificate), owner)))


if __name__ == "__main__":
    main()
