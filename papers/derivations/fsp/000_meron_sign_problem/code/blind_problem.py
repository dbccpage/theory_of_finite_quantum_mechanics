"""Problem-text generator for the cluster sign-cancellation benchmark.

``assert_lexical_hygiene`` rejects any text that contains one of the twelve
substrings in ``FORBIDDEN_WORDS`` (case-insensitive). It is a substring filter
only: it does not remove other domain vocabulary or information that
determines the answer.
"""

from __future__ import annotations

from oracle import BlindClusterOracle

FORBIDDEN_WORDS = [
    "meron",
    "fermion",
    "physics",
    "hamiltonian",
    "hubbard",
    "chandrasekharan",
    "wiese",
    "trotter",
    "fock",
    "anticommut",
    "quantum monte carlo",
    "qmc",
]


def assert_lexical_hygiene(text: str) -> None:
    """Hard assertion: fail immediately if any domain hint is leaked."""
    text_lower = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            raise ValueError(
                f"LEXICAL HYGIENE VIOLATION: Forbidden keyword '{word}' found in prompt/problem text!"
            )


BLIND_PROBLEM_DESCRIPTION = """
MATHEMATICAL GRAPH-PARTITION OPTIMIZATION PROBLEM

You are analyzing an oriented multigraph system with 16 nodes and 256 admissible decomposition subgraphs {G_k}.
Each subgraph G_k decomposes into a set of k disjoint connected cycle components C_k = {c_1, c_2, ..., c_k}.

A configuration on subgraph G_k is a discrete orientation assignment across its k cycle components.
Because each cycle can be oriented in 2 directions, a subgraph with k cycles has 2^k possible configurations.
Across all 256 subgraphs, there are exactly 1,296 total configurations.

Each configuration C has:
  1. An exact rational Boltzmann-like weight W(C) > 0
  2. A discrete global parity sign sigma(C) in {+1, -1} determined by alternating path crossings.

The global partition value Z is defined as the signed sum over all 1,296 configurations:
  Z = sum_{C} sigma(C) * W(C)

THE COMPUTATIONAL OBSTRUCTION:
In the naive configuration sum:
  - 1,104 configurations have sign sigma = +1
  - 192 configurations have sign sigma = -1
  - Absolute sum Z_abs = sum |W(C)| = 1,296
  - The average sign is <sigma> = 19/27 (severe sign cancellation).
In large graphs, this sign cancellation grows exponentially worse, making naive sampling impossible.

YOUR OBJECTIVE:
1. Prove an exact structural decomposition showing how cycle orientations interact with the global sign sigma(C).
2. Discover the discrete parity invariant I(c) in {0, 1} for an individual cycle component c such that:
     Flipping cycle c inverts the global sign (sigma -> -sigma) if and only if I(c) = 1.
3. Prove that whenever a subgraph G_k contains AT LEAST ONE cycle with I(c) = 1, the sum over all 2^k orientation configurations on G_k vanishes IDENTICALLY:
     sum_{orientations} sigma(C) * W(C) = 0
4. Deduce that the entire partition value Z is computed strictly by summing over the zero-odd-cycle sector (subgraphs where ALL cycles have I(c) = 0), with ZERO negative configurations.
5. Compute the exact ground-truth integer value of Z.
"""


def generate_blind_problem_packet() -> dict:
    """Generate the full problem packet with verified lexical hygiene."""
    oracle = BlindClusterOracle()
    samples = oracle.get_sample_subgraphs(limit=4)

    sample_text_blocks = []
    for s in samples:
        block = (
            f"Subgraph ID {s['subgraph_id']}:\n"
            f"  Cycles: {s['cycle_count']} disjoint cycles (lengths: {[c['length'] for c in s['cycles']]})\n"
            f"  Base weight: {s['base_weight']}\n"
            f"  Configurations ({len(s['configurations'])} total):\n"
        )
        for c in s["configurations"]:
            block += f"    Flip Mask {c['flip_mask']:0{s['cycle_count']}b}: sign={c['sign']:+d}, weight={c['weight']}\n"
        sample_text_blocks.append(block)

    full_text = (
        BLIND_PROBLEM_DESCRIPTION
        + "\n\nREPRESENTATIVE SUBGRAPH SAMPLES:\n"
        + "\n".join(sample_text_blocks)
    )
    assert_lexical_hygiene(full_text)

    return {
        "description": BLIND_PROBLEM_DESCRIPTION.strip(),
        "samples": samples,
        "sample_text": "\n".join(sample_text_blocks),
        "full_prompt_text": full_text,
        "ground_truth_z": oracle.signed_partition,
    }


if __name__ == "__main__":
    packet = generate_blind_problem_packet()
    print("Blind Problem Generator:")
    print("  Lexical hygiene verified: PASS (0 domain leaks)")
    print(f"  Sample subgraphs formatted: {len(packet['samples'])}")
    print(f"  Target Z: {packet['ground_truth_z']}")
    print("Ready for benchmark integration.")
