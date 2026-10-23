#!/usr/bin/env python3
"""Construct source graph operators; generate or independently replay receipts.

python replay_examples.py generate observer_completion_certificates.json
python replay_examples.py check observer_completion_certificates.json
python replay_examples.py adversarial observer_completion_certificates.json
"""
import json
import sys
from copy import deepcopy
from pathlib import Path

if __package__:
    from .observer_completion import (
        F,
        M,
        basis,
        check_completion,
        check_distance,
        check_failure,
        check_receipt,
        construct,
        distance_certificate,
        eye,
        facets_l1,
        facets_linf,
        failure,
        guarantees,
        hc,
        inverse,
        l1,
        op1,
        rank,
        rational,
        read_json,
        require,
        run_input,
        solve,
        spaces,
        vc,
        zero,
    )
else:
    from observer_completion import (
        F,
        M,
        basis,
        check_completion,
        check_distance,
        check_failure,
        check_receipt,
        construct,
        distance_certificate,
        eye,
        facets_l1,
        facets_linf,
        failure,
        guarantees,
        hc,
        inverse,
        l1,
        op1,
        rank,
        rational,
        read_json,
        require,
        run_input,
        solve,
        spaces,
        vc,
        zero,
    )

SOURCE_COMMIT = "39aacbe33bc7e6fabb94323b14e1ddeebe15e86e"
NORM_DESCRIPTION = "entrywise l1 on V and stacked reports unless explicitly overridden"


def select(n, ids):
    return eye(n).rows(ids)


def incidence(site_count, fiber, edges, zero_translations=False):
    """Edge convention: (lower, upper), D_e s = r_e s_upper - s_lower."""
    rows = []
    for lower, upper in edges:
        for j in range(fiber):
            row = [0]*(site_count*fiber)
            row[lower*fiber+j] = -1
            if not zero_translations:
                row[upper*fiber+j] += 1
            rows.append(row)
    return M(rows)


def source_instances():
    edges = [(3,0),(3,1),(4,1),(4,2),(5,2),(5,0)]
    d = incidence(6, 3, edges)
    hidden = [0,4,7,11,14,15]
    q = select(18, [j for j in range(18) if j not in hidden])
    ell = M([[int(j % 3 == i)*(1 if (j//3) % 2 == 0 else -1)
              for j in range(18)] for i in range(3)])
    t = eye(18).cols([0,1,2])
    three = {"name": "three_patch", "d0": d, "Q": q, "L": ell, "T": t,
             "completions": {"raw": select(18,[0,7,14]), "quotient": ell,
                             "both": select(18,hidden)}}
    d = incidence(3,2,[(0,1),(0,2)],True)
    ell = M([[1,0,-1,0],[0,1,0,-1]])
    t = eye(4).cols([0,1])
    coupled = []
    for name, ids in (("coupled_lggr_v",[0,3]), ("coupled_projection",[1,2])):
        coupled.append({"name": name, "d0": d, "Q": select(4,ids), "L": ell, "T": t,
                        "completions": {"raw": zero(0,4), "quotient": ell,
                                        "both": select(4,[j for j in range(4) if j not in ids])}})
    # Source scalar quotient example has no Q. Zero Q is a declared NEW extension.
    d = incidence(3,1,[(0,1),(0,2)],True)
    ell = M([[1,-1]])
    scalar = {"name": "scalar_quotient_with_new_zero_observer",
              "d0": d, "Q": zero(0,2), "L": ell, "T": eye(2).cols([0]),
              "completions": {"raw": select(2,[0]), "quotient": ell, "both": eye(2)}}
    return [three]+coupled+[scalar]


def check_l1_quotient_geometry(d, ell, t):
    require(ell @ d == zero(ell.r,d.c), "quotient map annihilation")
    require(rank(ell) == d.r-rank(d), "quotient map kernel")
    require(ell @ t == eye(ell.r), "quotient right inverse")
    require(op1(ell) <= 1 and op1(t) <= 1, "quotient contractions")


def raw_certificate(d, a):
    s = basis(d)
    g = inverse(a) if a.r == a.c and rank(a) == a.c else solve((a @ s).T,s.T).T
    c = op1(g)
    for j in range(s.c):
        b = s.cols([j])
        if l1(b) == c*l1(a @ b) and l1(a @ b) > 0:
            return {"constant": str(c), "decoder": g.encode(),
                    "site_preimage": solve(d,b).encode(), "saturating_defect": b.encode()}
    raise ValueError("supply a better decoder or a sharpness witness")


def check_raw(d, a, receipt):
    require(set(receipt) == {"constant", "decoder", "saturating_defect", "site_preimage"}, "raw fields")
    c = rational(receipt["constant"], wire=True)
    g = M.decode(receipt["decoder"])
    b = M.decode(receipt["saturating_defect"])
    require(g @ a @ d == d, "raw decoder on realizable carrier")
    require(op1(g) <= c, "raw upper bound")
    require(d @ M.decode(receipt["site_preimage"]) == b, "raw witness site realization")
    require(l1(a @ b) > 0 and l1(b) == c*l1(a @ b), "raw sharpness")


def quotient_certificate(instance, a, target):
    q, ell, t = instance["Q"], instance["L"], instance["T"]
    if target == "quotient":
        lo = hc(zero(ell.r,q.r),eye(ell.r))
        to = vc(zero(q.r,ell.r),eye(ell.r))
    else:
        lo, to = ell @ inverse(a), a @ t
    return {"constant": "1", "observed_L": lo.encode(), "observed_T": to.encode(),
            "saturating_cochain": t.cols([0]).encode()}


def check_quotient(d, a, ell, t, receipt):
    require(set(receipt) == {"constant", "observed_L", "observed_T", "saturating_cochain"}, "quotient fields")
    lo, to = M.decode(receipt["observed_L"]), M.decode(receipt["observed_T"])
    check_l1_quotient_geometry(d,ell,t)
    check_l1_quotient_geometry(a @ d,lo,to)
    require(lo @ a == ell, "quotient diagnostic equality")
    require(rational(receipt["constant"], wire=True) == 1, "quotient upper constant")
    v = M.decode(receipt["saturating_cochain"])
    require(l1(ell @ v) == l1(lo @ a @ v) > 0, "quotient sharpness")


def generic_trials():
    d = M([[1],[0],[0]])
    q = M([[1,0,0]])
    # Minimal completion happens to be the last two coordinate rows.
    inp = {"d0": d.encode(), "Q": q.encode(), "target": "both",
           "V_facets": facets_l1(3).encode(),
           "augmented_facets": facets_linf(3).encode()}
    out = run_input(inp)
    require([x["constant"] for x in out["recovery"]] == ["1","2"], "generic constants")
    # Direct distance: nontrivial weights, rational input, a mixed repair line.
    h = M([[2,3],[2,-3],[-2,3],[-2,-3]])
    s = M([[1],[1]])
    v = M([["1/2"],["-3/2"]])
    distance = distance_certificate(h,s,v)
    require(check_distance(h,s,distance) == 4, "weighted rational distance")
    return {"recovery": out, "distance": {"H": h.encode(), "S": s.encode(),
                                         "certificate": distance}}


def generate():
    result = {"source_commit": SOURCE_COMMIT,
              "norms": NORM_DESCRIPTION,
              "authority_effect": "None", "cases": []}
    for instance in source_instances():
        d, q = instance["d0"], instance["Q"]
        ell, t = instance["L"], instance["T"]
        s,n,h = spaces(d,q)
        item = {"name": instance["name"], "d0": d.encode(), "Q": q.encode(),
                "L": ell.encode(), "T": t.encode(),
                "dimensions": {"V": d.r, "B": s.c, "K": n.c, "intersection": h.c},
                "initial": {}, "completions": []}
        for target in ("raw","quotient"):
            witness = failure(d,q,target)
            item["initial"][target] = ({"failure": witness} if witness else
                                       {"recovery": raw_certificate(d,q)})
        for target, rr in instance["completions"].items():
            certificate = construct(d,q,target)
            certificate["R"] = rr.encode()
            a = vc(q,rr)
            record = {"completion": certificate, "guarantees": guarantees(d,a)}
            if record["guarantees"]["raw"]:
                record["raw_recovery"] = raw_certificate(d,a)
            if record["guarantees"]["quotient"]:
                record["quotient_recovery"] = quotient_certificate(instance,a,target)
            item["completions"].append(record)
        result["cases"].append(item)
    result["generic"] = generic_trials()
    return result


def check(data):
    require(set(data) == {"source_commit", "norms", "authority_effect", "cases", "generic"}, "source fields")
    require(data["source_commit"] == SOURCE_COMMIT and data["authority_effect"] == "None",
            "scope binding")
    require(data["norms"] == NORM_DESCRIPTION, "source norm binding")
    instances = source_instances()
    require(len(data["cases"]) == len(instances), "case count")
    for source, item in zip(instances,data["cases"]):
        require(set(item) == {"name", "d0", "Q", "L", "T", "dimensions", "initial", "completions"}, "case fields")
        require(item["name"] == source["name"], "case name")
        for key in ("d0","Q","L","T"):
            require(M.decode(item[key]) == source[key], "source reconstruction " + key)
        d,q,ell,t = (source[x] for x in ("d0","Q","L","T"))
        s,n,h = spaces(d,q)
        require(all(type(x) is int for x in item["dimensions"].values()), "source integer dimensions")
        require(item["dimensions"] == {"V": d.r, "B": s.c, "K": n.c, "intersection": h.c},
                "source dimensions")
        check_l1_quotient_geometry(d,ell,t)
        require(set(item["initial"]) == {"raw", "quotient"}, "initial target fields")
        for target in ("raw","quotient"):
            initial = item["initial"][target]
            require(set(initial) in ({"failure"}, {"recovery"}), "initial evidence fields")
            if "failure" in initial:
                require(initial["failure"]["kind"] == target, "failure target binding")
                check_failure(d,q,initial["failure"])
            else:
                require(target == "raw", "unexpected source quotient success")
                check_raw(d,q,initial["recovery"])
        require(len(item["completions"]) == 3, "completion count")
        for expected, record in zip(("raw","quotient","both"),item["completions"]):
            cc = record["completion"]
            require(cc["target"] == expected, "completion target binding")
            check_completion(d,q,cc)
            a = vc(q,M.decode(cc["R"]))
            gg = guarantees(d,a)
            fields = {"completion", "guarantees"}
            fields.update(name + "_recovery" for name in gg if gg[name])
            require(set(record) == fields, "completion evidence fields")
            require(set(record["guarantees"]) == set(gg) and
                    all(type(x) is bool for x in record["guarantees"].values()),
                    "boolean guarantee labels")
            require(gg == record["guarantees"], "guarantee labels")
            if gg["raw"]:
                check_raw(d,a,record["raw_recovery"])
            if gg["quotient"]:
                check_quotient(d,a,ell,t,record["quotient_recovery"])
    # Source section family reconstructed from SITE states, not asserted edge arrays.
    three = instances[0]
    for amplitude in (F(0), F(1), F(-3,2), F(17,11)):
        sites = M([[amplitude if i in (0,4,8) else 0] for i in range(18)])
        defect = three["d0"] @ sites
        require(l1(defect) == 6*abs(amplitude), "source section mass")
        require(three["Q"] @ defect == zero(12,1), "source section observation")
        require(three["L"] @ defect == zero(3,1), "source section exactness")
    # Scalar source witness has exact primal and dual certificates.
    scalar = instances[-1]
    omega = M([[1],[-1]])
    require(l1(scalar["L"] @ omega) == 2, "source scalar quotient value")
    require(M([[1,-1]]) @ scalar["d0"] == zero(1,3), "source scalar dual")
    require(l1(omega) == 2, "source scalar repair zero attains bound")
    # The coupled source's original maximum-observer norm gives C_raw=4.
    for source in instances[1:3]:
        b = M([[1],[1],[1],[1]])
        require(l1(b) == 4 and max(abs(x[0]) for x in (source["Q"] @ b).a) == 1,
                "maximum-observer sharpness")
    generic = data["generic"]
    require(set(generic) == {"recovery", "distance"}, "generic fields")
    expected = {"d0": M([[1],[0],[0]]).encode(), "Q": M([[1,0,0]]).encode(),
                "target": "both", "V_facets": facets_l1(3).encode(),
                "augmented_facets": facets_linf(3).encode()}
    check_receipt(generic["recovery"], expected)
    dd = generic["distance"]
    require(set(dd) == {"H", "S", "certificate"}, "weighted distance fields")
    require(M.decode(dd["H"]) == M([[2,3],[2,-3],[-2,3],[-2,-3]]) and
            M.decode(dd["S"]) == M([[1],[1]]) and
            M.decode(dd["certificate"]["v"]) == M([["1/2"],["-3/2"]]),
            "weighted distance query binding")
    require(check_distance(M.decode(dd["H"]),M.decode(dd["S"]),dd["certificate"]) == 4,
            "weighted LP check")
    return True


def adversarial(data):
    mutations = [
        ("too few measurements", lambda z: z["cases"][0]["completions"][0]["completion"].update(minimum=2)),
        ("wrong raw constant", lambda z: z["cases"][0]["completions"][0]["raw_recovery"].update(constant="1")),
        ("wrong quotient constant", lambda z: z["cases"][0]["completions"][1]["quotient_recovery"].update(constant="0")),
        ("wrong graph sign", lambda z: z["cases"][0]["d0"]["data"][0].__setitem__(0,"-1")),
        ("forged raw realization", lambda z: z["cases"][0]["initial"]["raw"]["failure"]["preimage"]["data"].__setitem__(0,["99"])),
        ("wrong target", lambda z: z["cases"][0]["completions"][0]["completion"].update(target="quotient")),
        ("missing recovery vertex", lambda z: z["generic"]["recovery"]["recovery"][1]["vertices"].pop()),
        ("forged LP dual", lambda z: z["generic"]["distance"]["certificate"]["mu"]["data"].__setitem__(0,["-1"])),
        ("authority escalation", lambda z: z.update(authority_effect="Grant")),
        ("nested authority escalation", lambda z: z["generic"]["recovery"].update(authority_effect="Grant")),
        ("false norm label", lambda z: z.update(norms="l-infinity on all spaces")),
        ("unverified active rows", lambda z: z["generic"]["recovery"]["recovery"][0]["vertices"][0].update(active_rows=[999])),
        ("omitted initial failure", lambda z: z["generic"]["recovery"].update(initial_failure=None)),
        ("wrong weighted input", lambda z: z["generic"]["distance"]["certificate"]["v"].update(data=[["-1/2"],["3/2"]])),
        ("wrong adapted basis", lambda z: z["generic"]["recovery"]["completion"].update(
            adapted_basis=eye(3).encode(), adapted_inverse=eye(3).encode())),
    ]
    rejected = []
    for name, mutate in mutations:
        altered = deepcopy(data)
        mutate(altered)
        try:
            check(altered)
        except (ValueError, KeyError, IndexError):
            rejected.append(name)
        else:
            raise ValueError("mutation accepted: " + name)
    # Necessary-hypothesis counterexamples checked as exact matrix statements.
    b = M([[1],[1]])
    q = zero(0,2)
    require(construct(b,q,"quotient")["minimum"] == 1, "unrestricted minimum")
    require(not guarantees(b,select(2,[0]))["quotient"] and
            not guarantees(b,select(2,[1]))["quotient"], "coordinate-menu counterexample")
    require(guarantees(b,M([[1,-1]]))["quotient"], "allowed difference observer")
    for d in (zero(2,0),eye(2)):
        for qq in (zero(0,2),eye(2)):
            for target in ("raw","quotient","both"):
                check_completion(d,qq,construct(d,qq,target))
    for target in ("raw","quotient","both"):
        check_completion(zero(0,0),zero(0,0),construct(zero(0,0),zero(0,0),target))
        run_input({"d0": zero(0,0).encode(), "Q": zero(0,0).encode(),
                   "target": target, "V_facets": facets_linf(0).encode(),
                   "augmented_facets": facets_linf(0).encode()})
    return rejected


if __name__ == "__main__":
    require(len(sys.argv) == 3 and sys.argv[1] in ("generate","check","adversarial"),
            "usage: replay_examples.py generate|check|adversarial FILE.json")
    path = Path(sys.argv[2])
    if sys.argv[1] == "generate":
        receipt = generate()
        check(receipt)
        path.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        print("Generated and checked four source/extension cases and generic LP certificates.")
    else:
        receipt = read_json(path)
        check(receipt)
        if sys.argv[1] == "adversarial":
            names = adversarial(receipt)
            print("Rejected all %d tampered certificates; restricted-menu and degenerate cases passed."
                  % len(names))
        else:
            print("All exact source, minimality, recovery, and LP certificate checks passed.")
