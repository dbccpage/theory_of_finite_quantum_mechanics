"""Replay one explicit finite population, optionally through fresh Lean and Rust."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import tempfile
from pathlib import Path

from preservation import protocol

ROOT = Path(__file__).resolve().parents[1]


def csv(values) -> str:
    return ",".join(map(str, values))


def records() -> list[str]:
    result = []
    for size in range(5):
        for reports in itertools.product(range(3), repeat=size):
            for answers in itertools.product(range(2), repeat=size):
                result.append(f"v1\tfactor\t{csv(reports)}\t{csv(answers)}")
    for n in range(5):
        for w, d, b in itertools.product(range(2**n), repeat=3):
            result.append(f"v1\tdemand\t{n}\t{w}\t{d}\t{b}")
    for n in range(1, 5):
        for a, b, weight in itertools.product(range(n), range(n), range(-2, 3)):
            result.append(f"v1\tboundary\t{n}\t{a},{b}\t{weight}")
    for weights in itertools.product(range(-2, 3), repeat=3):
        result.append(f"v1\tboundary\t3\t0,1,1,2,2,0\t{csv(weights)}")
    for size in range(7):
        for word in itertools.product("ab", repeat=size):
            result.append("v1\tcode\t"+"".join(word))
    for values in itertools.product((-1, 0, 1), repeat=4):
        result.append("v1\tchsh\t"+csv(values))
    result.extend(["v2\tcode\ta", "v1\tcode\tc", "v1\tfactor\t0\t", "v1\tboundary\t0\t\t",
        "v1\tboundary\t1\t0,1\t1", "v1\tboundary\t2\t0\t1", "v1\tdemand\t9\t0\t0\t0",
        "v1\tdemand\t2\t-1\t0\t0", "v1\tchsh\t1000001,0,0,0", "v1\tcode\t"+"a"*65,
        "v1\tfactor\t00\t0", "v1\tfactor\t+1\t1", "v1\tfactor\t-0\t0",
        "v1\tfactor\t١\t1", "v1\tdemand\t02\t0\t0\t0", "v1\tboundary\t+2\t\t"])
    for modulus, value in itertools.product(range(-8, 9), range(-32, 33)):
        result.append(f"v1\tcyclic\t{modulus},{value}")
    result.extend(["v1\tcyclic\t0,-1000000", "v1\tcyclic\t1000000,-1000000",
        "v1\tcyclic\t-1000000,-999999", "v1\tcyclic\t-1,1000000",
        "v1\tcyclic\t2", "v1\tcyclic\t2,1,0", "v1\tcyclic\t02,1",
        "v1\tcyclic\t٢,1", "v1\tcyclic\t2,1000001", "v1\tcyclic\t2,-1000001",
        "v1\tcyclic\t-0,1", "v1\tcyclic\t2,+1"])
    for n in range(4):
        possible = list(itertools.product(range(n), repeat=2))
        for length in range(3):
            for edges in itertools.product(possible, repeat=length):
                endpoints = csv(value for edge in edges for value in edge)
                for chain in itertools.product((-1, 0, 1), repeat=n):
                    result.append(f"v1\tcomponents\t{n}\t{endpoints}\t{csv(chain)}")
    result.extend(["v1\tcomponents\t3\t0,1,1,2,2,0\t-2,1,1",
        "v1\tcomponents\t4\t3,2,2,0,3,2,1,1\t2,-1,3,-2",
        "v1\tcomponents\t8\t0,7\t1000000,0,0,0,0,0,0,1000000",
        "v1\tcomponents\t2\t0,2\t1,1", "v1\tcomponents\t2\t0\t1,1",
        "v1\tcomponents\t2\t\t1", "v1\tcomponents\t9\t\t",
        "v1\tcomponents\t02\t\t1,1", "v1\tcomponents\t2\t-1,0\t1,1",
        "v1\tcomponents\t1\t\t1000001",
        "v1\tcomponents\t1\t"+csv([0]*34)+"\t0"])
    for filled in (0, 1):
        for chain in itertools.product(range(-5, 6), repeat=3):
            result.append(f"v1\ttriangle\t{filled}\t{csv(chain)}")
        for k in (-1_000_000, 1_000_000):
            result.append(f"v1\ttriangle\t{filled}\t{k},{k},{k}")
    result.extend(["v1\ttriangle\t2\t1,1,1", "v1\ttriangle\t01\t1,1,1",
        "v1\ttriangle\t-1\t1,1,1", "v1\ttriangle\t0\t1,1",
        "v1\ttriangle\t0\t1,1,1,1", "v1\ttriangle\t0\t01,1,1",
        "v1\ttriangle\t0\t1000001,1000001,1000001"])
    for cochain in itertools.product(range(-5, 6), repeat=3):
        result.append("v1\tcochain\t"+csv(cochain))
    result.extend(["v1\tcochain\t1000000,1000000,1000000", "v1\tcochain\t1,2",
        "v1\tcochain\t1,2,1000001", "v1\tcochain\t1,2,03"])
    result.extend(["v1\tbellpair\t0", "v1\tbellpair\t1", "v1\tbellpair\t2",
        "v1\tbellpair\t01", "v1\tbellpair\t-1", "v1\tbellpair\t+1",
        "v1\tbellpair\t١", "v1\tbellpair\t"])
    for size in range(4):
        for word in itertools.product("0123456789", repeat=size):
            result.append("v1\tdecimal\t"+"".join(word))
    for size in range(9):
        for bits in itertools.product("01", repeat=size):
            result.append("v1\tdecimal_decode\t"+"".join(bits))
    for size in range(6):
        for word in itertools.product("abc", repeat=size):
            for operation in ("recover", "erase"):
                result.append(f"v1\t{operation}\t"+"".join(word))
    for size in range(4):
        for mapping in itertools.product(range(3), repeat=size):
            for length in range(4):
                for word in itertools.product(range(size), repeat=length):
                    result.append(f"v1\trename\t{csv(mapping)}\t{csv(word)}")
    possible_edges = list(itertools.product(range(2), (0, 1), range(2)))
    for length in range(3):
        for trace in itertools.product(possible_edges, repeat=length):
            result.append("v1\ttrace\t"+csv(value for edge in trace for value in edge))
    result.extend(["v1\tdecimal\t١", "v1\tdecimal\t"+"0"*17,
        "v1\tdecimal\t9999999999999999", "v1\tdecimal_decode\t0020",
        "v1\tdecimal_decode\t"+"0"*65, "v1\trecover\td", "v1\terase\t"+"a"*65,
        "v1\trename\t1,2\t2", "v1\trename\t1,2\t-1", "v1\ttrace\t0,2,1",
        "v1\ttrace\t0,1", "v1\ttrace\t0,01,1", "v1\ttrace\t"+csv([0]*51)])
    for size in range(7):
        for word in itertools.product("abAB", repeat=size):
            result.append("v1\tfreeword\t"+"".join(word))
    result.extend(["v1\tfreeword\tc", "v1\tfreeword\t"+"a"*65,
        "v1\tfreeword\tá", "v1\tfreeword\t"+"aA"*32,
        "v1\tfreeword\t"+"abAB"*16])
    for first, second in itertools.product(range(16), repeat=2):
        for a, b in itertools.product((1, 2, 1_000_000), repeat=2):
            weights = [0]*16
            weights[first] = a
            weights[second] = b
            result.append("v1\tbellmix\t"+csv(weights))
    for selected in itertools.combinations(range(16), 3):
        weights = [int(i in selected) for i in range(16)]
        result.append("v1\tbellmix\t"+csv(weights))
    result.extend(["v1\tbellmix\t"+csv([1]*16), "v1\tbellmix\t"+csv([0]*16),
        "v1\tbellmix\t"+csv([-1]+[1]*15), "v1\tbellmix\t"+csv([1]*15),
        "v1\tbellmix\t"+csv([1]*17), "v1\tbellmix\t"+csv([1_000_001]+[1]*15),
        "v1\tbellmix\t01,"+csv([1]*15)])
    for degree in range(-4, 5):
        for chain in itertools.product(range(-4, 5), repeat=3):
            result.append(f"v1\ttriangle_degree\t{degree},"+csv(chain))
    result.extend(["v1\ttriangle_degree\t0,-1000000,-1000000,-1000000",
        "v1\ttriangle_degree\t-1000000,999999,999999,999999",
        "v1\ttriangle_degree\t2,1,1", "v1\ttriangle_degree\t2,1,1,1,1",
        "v1\ttriangle_degree\t02,1,1,1", "v1\ttriangle_degree\t٢,1,1,1",
        "v1\ttriangle_degree\t2,1000001,1000001,1000001"])
    return result


def reproduce(native: bool = False) -> dict:
    population = records()
    expected = [protocol(record) for record in population]
    source = "\n".join(population) + "\n"
    receipt = dict(schema="pre_mssn.replay.v1", records=len(population),
        refused=expected.count("REFUSE"), input_sha256=hashlib.sha256(source.encode()).hexdigest(),
        output_sha256=hashlib.sha256(("\n".join(expected)+"\n").encode()).hexdigest(),
        authority_effect="None", native_executions=[])
    if native:
        environment = dict(os.environ)
        environment["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.33.0"
        commands = [
            (["cargo", "run", "--quiet", "--offline", "--manifest-path", "code/rust/Cargo.toml"], ROOT),
            (["lake", "env", "lean", "--run", "Replay.lean"], ROOT / "lean4"),
        ]
        with tempfile.TemporaryDirectory(prefix="pre-mssn-rust-") as build:
            environment["CARGO_TARGET_DIR"] = build
            tests = subprocess.run(["cargo", "test", "--offline", "--manifest-path", "code/rust/Cargo.toml"],
                cwd=ROOT, env=environment, text=True, encoding="utf-8", capture_output=True, timeout=300, check=True)
            receipt["rust_tests_stdout"] = tests.stdout
            for command, directory in commands:
                run = subprocess.run(command, cwd=directory, env=environment, input=source,
                                     text=True, encoding="utf-8", capture_output=True, timeout=300, check=True)
                actual = run.stdout.splitlines()
                if actual != expected:
                    for i, (left, right) in enumerate(itertools.zip_longest(actual, expected)):
                        if left != right:
                            raise ValueError(f"{command[0]} divergence at record {i}: {population[i]!r}; {left!r} != {right!r}")
                receipt["native_executions"].append(dict(command=command, compared=len(actual), status="PASS"))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", action="store_true")
    print(json.dumps(reproduce(parser.parse_args().native), indent=2))
