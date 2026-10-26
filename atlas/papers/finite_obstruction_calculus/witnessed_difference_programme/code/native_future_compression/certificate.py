"""Separate producer and strict candidate checks for the admitted finite task."""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

from .model import (
    ACTIONS,
    PROFILE,
    PROFILES,
    TASK,
    State,
    balance_wire,
    clipped_report,
    decode,
    digest,
    fields,
    mark_wire,
    natural,
    require,
    same,
    state_of,
)
from .replay import file_sha, original_rows

SCHEMA = "bounded-native-future-certificate/1"
QUESTIONS = {"present": ["joint_result_mark", "literal_balance_keys_and_values"],
             "offered": ["native_guard", "carrier_admission", "enabled_native_price"],
             "executed": ["child_layer_class", "native_price", "successful_occurrences"],
             "state_order": "numeric_lexicographic_n_r_s_filled",
             "class_order": "first_occurrence_in_raw_state_order",
             "terminal_profiles": list(PROFILES)}


def binding(package):
    package = Path(package).absolute()
    repo = next((p for p in (package, *package.parents)
                 if (p/"omega_engine/crates_rs/omega_wdp/Cargo.toml").is_file()), None)
    require(repo is not None, "native owner root anchor not found")
    native = repo / "omega_engine/crates_rs"
    paths = [native / "omega_wdp/src" / name for name in
             ("genesis_source_execution.rs", "genesis_marked_result.rs", "genesis_ongoing_adapter.rs",
              "native_future_compression.rs")]
    paths.append(package / "code/causal_certificates/native/main.rs")
    # The normalization owner is part of the comparison's custody too.
    paths.append(native / "omega_linear_algebra/src/gauge_pair_table.rs")
    paths += sorted((package / "code/native_future_compression").glob("*.py"))
    paths.append(package / "scripts/check_native_future_compression.py")
    paths.append(package / "manifests/source_replay_inputs.json")
    hashes = {p.relative_to(repo).as_posix(): file_sha(p) for p in paths}
    return {"task": TASK, "profile": deepcopy(PROFILE), "questions": deepcopy(QUESTIONS),
            "actions": deepcopy(ACTIONS), "authority_effect": "None",
            "original_source": original_rows(package / "manifests/source_replay_inputs.json"),
            "source_sha256": hashes}


def check_partitions(model, partitions):
    fields(partitions, PROFILES, "terminal profiles")
    lift_edges = 0
    for profile in PROFILES:
        layers = partitions[profile]
        require(type(layers) is list and len(layers) == 3, "layer count")
        for layer, labels in enumerate(layers):
            require(type(labels) is list and len(labels) == len(model.states), "partition domain")
            signature_class = {}
            class_signature = {}
            for i, label in enumerate(labels):
                natural(label, len(model.states), "class label")
                sig = model.signature(i, profile, layers[layer-1] if layer else None)
                if sig not in signature_class:
                    signature_class[sig] = len(signature_class)
                require(label == signature_class[sig], f"coarsest class or canonical label: {profile}/{layer}/{i}")
                if label in class_signature:
                    require(class_signature[label] == sig, "merged distinct behavior")
                else:
                    class_signature[label] = sig
                if layer:
                    # Checking all members, labels, statuses, prices and child
                    # classes supplies both directions for every one-step lift.
                    lift_edges += sum(e.child is not None for e in model.edges[i])
            if layer == 2:
                require(len(class_signature) == len(model.states), "horizon two raw equality")
    return lift_edges


def representatives(labels):
    out = {}
    for i, label in enumerate(labels):
        out.setdefault(label, i)
    return out


def check_all_lifts(model, partitions):
    """Check the one-step commuting square at every member of every positive layer."""
    count = 0
    for profile in PROFILES:
        for layer in (1, 2):
            labels = partitions[profile][layer]
            lower = partitions[profile][layer-1]
            reps = representatives(labels)
            for initial, class_id in enumerate(labels):
                rep = reps[class_id]
                require(model.present[initial] == model.present[rep], "quotient present factorization")
                for concrete, quotient in zip(model.edges[initial], model.edges[rep]):
                    require((concrete.status, concrete.price, concrete.occurrences) ==
                            (quotient.status, quotient.price, quotient.occurrences), "quotient offer factorization")
                    if quotient.child is not None:
                        require(concrete.child is not None and lower[concrete.child] == lower[quotient.child],
                                "lift from member does not project to quotient child")
                        count += 1
    return count


def quotient_path(model, partitions, profile, layer, initial_class, actions):
    """Compute the quotient path using only class reports, never a hidden raw start."""
    require(profile in PROFILES, "path terminal profile")
    natural(layer, 3, "path remaining horizon")
    require(type(actions) is list and len(actions) <= layer, "path horizon")
    natural(initial_class, max(partitions[profile][layer])+1, "path initial class")
    current = initial_class
    classes = [current]
    prices = []
    for step, action in enumerate(actions):
        natural(action, 42, "path literal action")
        remaining = layer-step
        state_id = representatives(partitions[profile][remaining])[current]
        edge = model.edges[state_id][action]
        require(edge.status == "admitted", "path contains a refused offer")
        current = partitions[profile][remaining-1][edge.child]
        classes.append(current)
        prices.append(list(edge.price))
    return {"profile": profile, "remaining_horizon": layer, "initial_class": initial_class,
            "actions": list(actions), "classes": classes, "prices": prices,
            "occurrences": len(actions), "total_price": [sum(p[k] for p in prices) for k in (0, 1)]}


def project_path(model, partitions, profile, layer, original, actions):
    require(type(original) is State and original in model.index, "path raw start")
    initial = model.index[original]
    qpath = quotient_path(model, partitions, profile, layer, partitions[profile][layer][initial], actions)
    raw_ids = [initial]
    for i, action in enumerate(actions):
        edge = model.edges[raw_ids[-1]][action]
        require(edge.status == "admitted", "projection refused edge")
        raw_ids.append(edge.child)
        require(partitions[profile][layer-i-1][edge.child] == qpath["classes"][i+1],
                "projection child mismatch")
    return {"original": original.wire(), "raw_ids": raw_ids, "quotient": qpath}


def check_path(model, partitions, path, expected_original, expected_layer, expected_profile):
    fields(path, ("original", "raw_ids", "quotient"), "path certificate")
    original = state_of(path["original"])
    require(original == expected_original, "substituted original start")
    q = path["quotient"]
    fields(q, ("profile", "remaining_horizon", "initial_class", "actions", "classes", "prices",
               "occurrences", "total_price"), "quotient path")
    same(q["profile"], expected_profile, "changed path terminal profile")
    same(q["remaining_horizon"], expected_layer, "reset remaining horizon")
    # The candidate's own actions are checked; the checker never finds another
    # successful word to replace an invalid supplied word.
    expected = project_path(model, partitions, expected_profile, expected_layer, original, q["actions"])
    same(path, expected, "path projection or lift mismatch")
    return model.states[path["raw_ids"][-1]]


def lift_path(model, partitions, qpath, original, expected_layer, expected_profile):
    require(type(original) is State and original in model.index, "lift original state")
    result = project_path(model, partitions, expected_profile, expected_layer, original, qpath["actions"])
    same(result["quotient"], qpath, "quotient path does not lift from supplied original")
    return result


def compose_paths(model, partitions, prefix, suffix, original, layer, profile):
    middle = check_path(model, partitions, prefix, original, layer, profile)
    left_actions = prefix["quotient"]["actions"]
    check_path(model, partitions, suffix, middle, layer-len(left_actions), profile)
    return project_path(model, partitions, profile, layer, original,
                        left_actions + suffix["quotient"]["actions"])


def make_state(n, r=(), s=(), filled=()):
    def table(pairs):
        out = [0]*(n*n)
        for x, y, count in pairs:
            out[x*n+y] = count
        return tuple(out)
    return State(n, table(r), table(s), filled)


def action_id(kind, **values):
    return ACTIONS.index({"kind": kind, **values})


def fixture_inputs():
    rm = lambda rel, x, y: action_id("remove", relation=rel, x=x, y=y)
    add = action_id("add_term")
    fill = action_id("fill", x=0, y=1, z=2)
    identify = action_id("identify", x=0, y=1)
    return {
        "delete_clip_r": (make_state(2, r=((0, 1, 1),)), make_state(2, r=((1, 0, 1),)), rm("r", 0, 1)),
        "delete_clip_s": (make_state(2, s=((0, 1, 1),)), make_state(2, s=((1, 0, 1),)), rm("s", 0, 1)),
        "delete_filled": (make_state(3, filled=((0, 1, 2),)), make_state(3, filled=((0, 2, 1),)), fill),
        "horizon_collision": (make_state(2, r=((0, 1, 1), (1, 0, 2))),
                              make_state(2, r=((0, 1, 2), (1, 0, 1))), rm("r", 0, 1)),
        "growth": (make_state(2), make_state(2, r=((0, 1, 1),), s=((1, 0, 1),)), [add, fill]),
        "identification": (make_state(3, r=((0, 1, 1),)), make_state(3, r=((0, 2, 1),)), [identify]),
    }


def offer_inputs():
    return {
        "term_exclusion": (make_state(3), action_id("add_term")),
        "count_exclusion": (make_state(1, r=((0, 0, 2),), s=((0, 0, 2),)),
                            action_id("add_assertion", relation="r", x=0, y=0)),
        "invalid_address": (make_state(1, r=((0, 0, 2),), s=((0, 0, 2),)),
                            action_id("add_assertion", relation="r", x=2, y=2)),
        "zero_price_remove": (make_state(1, r=((0, 0, 1),)), action_id("remove", relation="r", x=0, y=0)),
        "zero_price_identify": (make_state(2), action_id("identify", x=0, y=1)),
        "zero_price_fill": (make_state(3), action_id("fill", x=0, y=1, z=2)),
        "face_key": (make_state(3, filled=((0, 1, 2),)), action_id("fill", x=0, y=1, z=2)),
        "empty_carrier": (make_state(0), action_id("add_term")),
    }


def build_witnesses(model, partitions):
    witnesses = {}
    for name, (left, right, action) in fixture_inputs().items():
        item = {"left": model.index[left], "right": model.index[right]}
        if type(action) is int:
            item["action"] = action
        else:
            item["left_path"] = project_path(model, partitions, PROFILES[0], 2, left, action)
            item["right_path"] = project_path(model, partitions, PROFILES[0], 2, right, action)
        witnesses[name] = item
    witnesses["offers"] = {}
    for name, (state, action) in offer_inputs().items():
        i = model.index[state]
        witnesses["offers"][name] = {"state": i, "action": action, "edge": model.edges[i][action].wire(),
                                       "present": {"mark": mark_wire(model.marks[i]),
                                                   "balance": balance_wire(model.balances[i])}}
    initial = make_state(2)
    add = action_id("add_term")
    fill = action_id("fill", x=0, y=1, z=2)
    prefix = project_path(model, partitions, PROFILES[0], 2, initial, [add])
    middle = model.states[prefix["raw_ids"][-1]]
    witnesses["composition"] = {
        "prefix": prefix, "suffix": project_path(model, partitions, PROFILES[0], 1, middle, [fill]),
        "composite": project_path(model, partitions, PROFILES[0], 2, initial, [add, fill]),
        "identity": project_path(model, partitions, PROFILES[0], 2, initial, [])}
    return witnesses


def check_witnesses(model, partitions, witnesses):
    inputs = fixture_inputs()
    fields(witnesses, (*inputs, "offers", "composition"), "witness collection")
    for name, (bound_left, bound_right, bound_actions) in inputs.items():
        item = witnesses[name]
        fields(item, ("left", "right", "action") if type(bound_actions) is int else
                     ("left", "right", "left_path", "right_path"), f"witness {name}")
        # These witnesses have declared initial pairs. Their state identifiers
        # cannot be reinterpreted against a changed indexing or substituted pair.
        same(item["left"], model.index[bound_left], f"{name}: initial left")
        same(item["right"], model.index[bound_right], f"{name}: initial right")
        left, right = item["left"], item["right"]
        require(left != right and model.marks[left] == model.marks[right], f"{name}: same mark")
        if type(bound_actions) is int:
            same(item["action"], bound_actions, f"{name}: literal separator")
            if name.startswith("delete_"):
                a, b = clipped_report(bound_left), clipped_report(bound_right)
                key = name.removeprefix("delete_")
                del a[key], b[key]
                same(a, b, f"{name}: deletion collision")
                require(model.edges[left][bound_actions].status != model.edges[right][bound_actions].status,
                        f"{name}: guard separation")
            else:
                weak, strong = (partitions[p] for p in PROFILES)
                require(weak[1][left] == weak[1][right] and weak[2][left] != weak[2][right],
                        "present-only horizon collision")
                require(strong[0][left] == strong[0][right] and strong[1][left] != strong[1][right],
                        "terminal-probe horizon separation")
                require(sum(e.status == "admitted" for e in model.edges[left]) == 12,
                        "complete 42-offer collision")
        else:
            endpoints = []
            for side, original in (("left", bound_left), ("right", bound_right)):
                path = item[f"{side}_path"]
                same(path["quotient"]["actions"], bound_actions, f"{name}: supplied word")
                endpoints.append(check_path(model, partitions, path, original, 2, PROFILES[0]))
            if name == "growth":
                require(model.balances[model.index[endpoints[0]]] == (((0, 1, 2), True),) and
                        model.balances[model.index[endpoints[1]]] == (((0, 1, 2), False),),
                        "carrier growth balance")
                require(all(item[f"{side}_path"]["quotient"]["total_price"] == [1, 0] and
                            item[f"{side}_path"]["quotient"]["occurrences"] == 2 for side in ("left", "right")),
                        "carrier growth price or occurrences")
            else:
                require(model.marks[model.index[endpoints[0]]][1] == (0, 0, 0, 1) and
                        model.marks[model.index[endpoints[1]]][1] == (0, 1, 0, 0),
                        "identification separation")
    offers = witnesses["offers"]
    fields(offers, offer_inputs(), "offer witnesses")
    for name, (state, action) in offer_inputs().items():
        item = offers[name]
        fields(item, ("state", "action", "edge", "present"), f"offer {name}")
        i = model.index[state]
        same(item["state"], i, f"{name}: offered state")
        same(item["action"], action, f"{name}: action label")
        same(item["edge"], model.edges[i][action].wire(), f"{name}: native guard/price/child/occurrences")
        same(item["present"], {"mark": mark_wire(model.marks[i]), "balance": balance_wire(model.balances[i])},
             f"{name}: complete present record")
    comp = witnesses["composition"]
    fields(comp, ("prefix", "suffix", "composite", "identity"), "composition witnesses")
    initial = make_state(2)
    composite = compose_paths(model, partitions, comp["prefix"], comp["suffix"], initial, 2, PROFILES[0])
    same(comp["composite"], composite, "supplied composite")
    check_path(model, partitions, comp["identity"], initial, 2, PROFILES[0])
    require(comp["identity"]["quotient"]["actions"] == [], "identity is empty")
    same(compose_paths(model, partitions, comp["identity"], comp["prefix"], initial, 2, PROFILES[0]),
         comp["prefix"], "left identity")
    endpoint = model.states[comp["composite"]["raw_ids"][-1]]
    right_identity = project_path(model, partitions, PROFILES[0], 0, endpoint, [])
    same(compose_paths(model, partitions, comp["composite"], right_identity, initial, 2, PROFILES[0]),
         comp["composite"], "right identity")


def census_summary(model, partitions):
    groups = defaultdict(list)
    for i, m in enumerate(model.marks):
        groups[m].append(i)
    fibers = [{"mark": mark_wire(m), "raw_states": len(ids),
               "class_counts": {p: [len({layer[i] for i in ids}) for layer in partitions[p]] for p in PROFILES}}
              for m, ids in sorted(groups.items())]
    return {"raw_states": len(model.states), "actions": 42,
            "states_by_terms": [sum(s.n == n for s in model.states) for n in range(4)],
            "offers": len(model.states)*42,
            "status_counts": dict(sorted(Counter(e.status for row in model.edges for e in row).items())),
            "layer_counts": {p: [len(set(layer)) for layer in partitions[p]] for p in PROFILES},
            "result_mark_fibers": fibers}


def build_certificate(model, partitions, expected_binding):
    return {"schema": SCHEMA, "binding": deepcopy(expected_binding),
            "state_index_sha256": digest([s.wire() for s in model.states]),
            "partitions": deepcopy(partitions), "summary": census_summary(model, partitions),
            "witnesses": build_witnesses(model, partitions)}


def check_certificate(model, candidate, expected_binding):
    fields(candidate, ("schema", "binding", "state_index_sha256", "partitions", "summary", "witnesses"), "certificate")
    same(candidate["schema"], SCHEMA, "certificate schema")
    same(candidate["binding"], expected_binding, "changed task/profile/labels/source binding")
    same(candidate["state_index_sha256"], digest([s.wire() for s in model.states]), "raw state indexing")
    lifted = check_partitions(model, candidate["partitions"])
    require(check_all_lifts(model, candidate["partitions"]) == lifted, "complete lift coverage")
    for state in model.states:
        require(decode(clipped_report(state)) == state, "all-state decoder")
    same(candidate["summary"], census_summary(model, candidate["partitions"]), "submitted census summary")
    check_witnesses(model, candidate["partitions"], candidate["witnesses"])
    return {"states": len(model.states), "decoder_replays": len(model.states),
            "member_step_lifts": lifted,
            "layer_counts": candidate["summary"]["layer_counts"], "authority_effect": "None"}
