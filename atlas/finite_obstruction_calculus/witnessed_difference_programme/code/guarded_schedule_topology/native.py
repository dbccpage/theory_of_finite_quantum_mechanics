"""Source-bound native transition replay, separate from the topological model."""

from __future__ import annotations

import hashlib
from itertools import permutations

from .experiment import encoded
from .model import TopologyRefusal, count_trace


def replay_native(owner) -> dict:
    # These existing adapters call the actual configured omega_wdp binary.
    # They contain no fallback transition implementation.
    from scripts.check_guarded_coherence import try_replay

    owner.verify_custody()
    transcript = hashlib.sha256()
    cases = []
    for n in range(1, 5):
        causal = [word for word in permutations(range(2 * n))
                  if all(word.index(2 * i) < word.index(2 * i + 1) for i in range(n))]
        for capacity in range(n + 1):
            initial = {"terms": ["t0"], "r": [str(capacity)], "s": ["0"], "filled": []}
            accepted = refused = 0
            for word in causal:
                changes = [{"kind": "add_assertion" if e % 2 else "remove",
                            "relation": "r", "x": 0, "y": 0} for e in word]
                run, reason = try_replay(owner, initial, changes)
                trace = count_trace(word, capacity)
                if (run is not None) != (trace is not None):
                    raise TopologyRefusal("actual native guard disagrees with direct count replay")
                if run is None:
                    refused += 1
                else:
                    accepted += 1
                    expected_counts = [str(value) for value in trace]
                    for state, value in zip(run["states"], expected_counts):
                        if (state["terms"] != ["t0"] or state["r"] != [value]
                                or state["s"] != ["0"] or state["filled"] != []):
                            raise TopologyRefusal("native intermediate state does not match the declared count kernel")
                    if run["addition_price"] != ["0", str(n)]:
                        raise TopologyRefusal("native addition count differs from the tagged add events")
                transcript.update(encoded({"pairs": n, "capacity": capacity, "word": word,
                                           "run": run, "reason": reason}) + b"\n")
            cases.append({"pairs": n, "capacity": capacity, "causal_words": len(causal),
                          "accepted": accepted, "refused": refused})
    owner.verify_custody()
    return {"fresh_native_replay": True, "native_binding": owner.binding,
            "cases": cases, "calls": sum(row["causal_words"] for row in cases),
            "transcript_sha256": transcript.hexdigest(),
            "scope": "all causal tagged schedules, n=1..4, every capacity 0..n; one fixed R loop",
            "pair_precedence_source": "explicit event protocol; not a native count guard"}
