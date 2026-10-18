"""Prompt builder for the 5 experimental arms of the blind cluster recovery benchmark.

Arms:
  Arm 1: Constrained JSON Decoding
  Arm 2: Attention Distractor-Key Masking
  Arm 3: DDC Hieroglyphic Factorization
  Arm 4: Multi-Round Typed Input/Output (Self-Selected Lifts + Antibodies)
  Arm 5: Full Hybrid (Hieroglyphics + Distractor Masking + Scratchpad + Antibodies)

AuthorityEffect: None.
Firewall: Strict lexical hygiene; zero physics keywords.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega_engine_projects.fsp.demos.blind_cluster_recovery.blind_problem import (  # noqa: E402
    assert_lexical_hygiene,
    generate_blind_problem_packet,
)

JSON_SCHEMA_ARM1 = {
    "type": "object",
    "properties": {
        "cycle_independence": {
            "type": "boolean",
            "description": "True if the configuration sign and weight factorize independently over cycle components",
        },
        "cycle_parity_invariant_found": {
            "type": "boolean",
            "description": "True if each cycle has a discrete parity I(c) in {0,1} such that flipping c flips global sign iff I(c)=1",
        },
        "cancellation_mechanism": {
            "type": "string",
            "description": "Mathematical explanation of the exact pairwise cancellation across 2^k configurations",
        },
        "zero_odd_sector_subgraphs": {
            "type": "integer",
            "description": "Number of subgraphs where all cycles have I(c)=0",
        },
        "exact_partition_z": {
            "type": "integer",
            "description": "Exact integer value of the signed partition function Z",
        },
        "scratchpad": {
            "type": "string",
            "description": "Step-by-step intermediate algebraic derivation",
        },
    },
    "required": [
        "cycle_independence",
        "cycle_parity_invariant_found",
        "cancellation_mechanism",
        "zero_odd_sector_subgraphs",
        "exact_partition_z",
        "scratchpad",
    ],
    "additionalProperties": False,
}


def build_prompt_arm1_constrained_decoding(packet: dict) -> str:
    """Arm 1: Standard blind prompt with mandatory JSON schema output constraint."""
    prompt = (
        packet["full_prompt_text"]
        + "\n\n"
        + "OUTPUT INSTRUCTION:\n"
        + "Return ONLY a valid RFC 8259 JSON object with the following exact keys:\n"
        + "  - cycle_independence: boolean (true/false)\n"
        + "  - cycle_parity_invariant_found: boolean (true/false)\n"
        + "  - cancellation_mechanism: string (exact cancellation proof)\n"
        + "  - zero_odd_sector_subgraphs: integer (count of surviving subgraphs)\n"
        + "  - exact_partition_z: integer (exact value of Z)\n"
        + "  - scratchpad: string (intermediate algebraic steps)\n"
        + "Do not include conversational prose or markdown formatting outside the JSON object."
    )
    assert_lexical_hygiene(prompt)
    return prompt


def build_prompt_arm2_attention_masking(packet: dict) -> str:
    """Arm 2: Attention Distractor-Key Masking.

    Strips microscopic node IDs and edge lists. Presents only the macroscopic
    topological invariant spectrum (cycle counts, cycle lengths, and flip parities),
    preventing attention dispersion across irrelevant vertex permutations.
    """
    masked_samples = []
    for s in packet["samples"]:
        # Distractor masking: replace explicit vertex connectivity with abstract cycle invariants
        masked_samples.append(
            f"Macro-Topology Spectrum (Subgraph {s['subgraph_id']}):\n"
            f"  Component Cycle Invariants: {s['cycle_count']} independent loops [lengths: {[c['length'] for c in s['cycles']]}]\n"
            f"  Orbit Configuration Dimension: 2^{s['cycle_count']} = {len(s['configurations'])} states\n"
            f"  Sign Parity Spectrum under Basis Flip:\n"
            f"    Odd-Winding Components: {s['odd_parity_cycles']}\n"
            f"    Positive Weight Density: {s['base_weight']}\n"
        )

    prompt = (
        "MACROSCOPIC TOPOLOGICAL SIGN-INVERSION PROBLEM\n\n"
        "You are given an ensemble of 256 independent graph decompositions. All microscopic vertex\n"
        "distractors have been integrated out, leaving the macroscopic cycle topology spectrum.\n\n"
        "The system has 1,296 total configurations, 192 of which have negative parity (-1).\n"
        "Absolute sum is 1,296; raw average parity sign is 19/27.\n\n"
        "FILTERED TOPOLOGICAL SPECTRA:\n"
        + "\n".join(masked_samples)
        + "\n\n"
        + "ATTENTION FOCUS DIRECTIVE:\n"
        + "Focus attention strictly on the parity homomorphism: (Z_2)^k -> {+1, -1}.\n"
        + "1. Prove that whenever a decomposition contains >= 1 odd-winding loop, the sum over all 2^k flip states vanishes identically: sum sigma(C) = 0.\n"
        + "2. Identify the number of subgraphs having zero odd-winding loops.\n"
        + "3. Compute the exact non-negative reduced partition value Z.\n\n"
        + "Return ONLY a valid JSON object matching the required schema."
    )
    assert_lexical_hygiene(prompt)
    return prompt


def build_prompt_arm3_hieroglyphics(packet: dict) -> str:
    """Arm 3: DDC Hieroglyphic Prompt Factorization.

    Encodes problem instances using the Discrete Deformation Calculus (DDC)
    8-letter operational trace alphabet:
      {E, R, C, I, Λ, D, M, T}
      E: Spanning-tree edge
      R: Chord defect relation
      C: Closed cycle component
      I: Parity invariant
      Λ: Structural lift / flip
      D: Defect mass (negative sign)
      M: Terminal obstruction / refusal
      T: Terminal exact trace
    """
    ddc_blocks = []
    for s in packet["samples"]:
        # Express each subgraph as a compact DDC trace
        cycle_runes = "".join(f"[C_{i}:{c['length']}]" for i, c in enumerate(s["cycles"]))
        ddc_blocks.append(
            f"DDC_GRAPH_{s['subgraph_id']}:\n"
            f"  Σ = {cycle_runes}\n"
            f"  dim(H_1) = {s['cycle_count']}\n"
            f"  Λ_flips = 2^{s['cycle_count']} ∈ (Z_2)^{s['cycle_count']}\n"
            f"  I_odd = {s['odd_parity_cycles']}\n"
            f"  W_base = {s['base_weight']}\n"
        )

    prompt = (
        "DDC HIEROGLYPHIC FACTORIZED GRAPH-PARTITION TASK\n\n"
        "Trace Alphabet: A_DDC = {E, R, C, I, Λ, D, M, T}\n"
        "Grammar: Graph G decomposes into cycle basis Σ = ⊕ C_i.\n"
        "Orientation shifts act as discrete gauge lifts Λ ∈ (Z_2)^k.\n"
        "Defect functional D(C) maps orientation C to parity sign sigma(C) ∈ {+1, -1}.\n\n"
        "Global partition trace: T = ∑_{C} sigma(C) * W(C) across 1,296 states.\n"
        "Raw defect mass: 192 negative states. Average parity: 19/27.\n\n"
        "DDC FACTORIZED SAMPLES:\n"
        + "\n".join(ddc_blocks)
        + "\n\n"
        + "DDC DESCENT OBJECTIVE:\n"
        + "Find the exact cochain kernel ker(D) where defect mass vanishes identically.\n"
        + "Prove that any subgraph with I_odd >= 1 satisfies ∑_{Λ} sigma(Λ) = 0.\n"
        + "Emit the exact terminal trace T = Z.\n\n"
        + "Return JSON matching the schema."
    )
    assert_lexical_hygiene(prompt)
    return prompt


def build_prompt_arm4_immune_round(
    packet: dict,
    round_number: int,
    accumulated_antibodies: list[dict],
    selected_lift: str | None = None,
) -> str:
    """Arm 4: Multi-Round Typed Input/Output with Self-Selected Lifts & Antibody Feedback."""
    prompt_lines = [
        f"SYMBOL GAME MULTI-ROUND IMMUNE LOOP — ROUND {round_number}/7",
        "",
        packet["description"],
        "",
        "REPRESENTATIVE SUBGRAPH SAMPLES:",
        packet["sample_text"],
        "",
    ]

    if accumulated_antibodies:
        prompt_lines.append(
            "ACCUMULATED HOST ANTIBODIES (Prior Round Obstructions Catching Hallucinations):"
        )
        for i, ab in enumerate(accumulated_antibodies, 1):
            prompt_lines.append(f"  [ANTIBODY_{i}] {ab['code']}: {ab['explanation']}")
            prompt_lines.append(f"    Target invariant to enforce: {ab['correction']}")
        prompt_lines.append("")

    if selected_lift:
        prompt_lines.append(f"ACTIVE MATHEMATICAL LIFT APPLIED: {selected_lift}")
        prompt_lines.append("")

    prompt_lines.append(
        "PROPOSER DIRECTIVE:\n"
        "1. In your scratchpad, derive whether cycle orientations flip signs independently.\n"
        "2. Formulate the exact pairwise cancellation proof.\n"
        "3. Specify which next mathematical lift you request (e.g. 'cycle contraction', 'homology reduction', 'quotient projection').\n"
        "4. Output the exact integer partition value Z.\n\n"
        "Return your answer as a JSON object matching the schema."
    )

    full_text = "\n".join(prompt_lines)
    assert_lexical_hygiene(full_text)
    return full_text


def build_prompt_arm5_hybrid(
    packet: dict,
    accumulated_antibodies: list[dict] | None = None,
) -> str:
    """Arm 5: Full Hybrid (DDC hieroglyphics + attention masking + mandatory 4-step scratchpad + antibodies)."""
    masked_ddc_samples = []
    for s in packet["samples"]:
        cycle_spec = " ⊗ ".join(f"C_{i}(len={c['length']})" for i, c in enumerate(s["cycles"]))
        masked_ddc_samples.append(
            f"  [G_{s['subgraph_id']}]: Σ = {cycle_spec} | Flips: 2^{s['cycle_count']} | Odd-Winding: {s['odd_parity_cycles']} | Weight: {s['base_weight']}"
        )

    prompt_lines = [
        "HYBRID DDC TOPOLOGICAL PARTITION RECOVERY (ARM 5)",
        "",
        "Ensemble: 256 subgraphs, 1,296 total orientation states, 192 negative states, <sigma> = 19/27.",
        "Microscopic distractors masked; factorized into DDC cycle spectra:",
        "\n".join(masked_ddc_samples),
        "",
    ]

    if accumulated_antibodies:
        prompt_lines.append("HOST ANTIMORPHISM GUARDS (Antibodies):")
        for i, ab in enumerate(accumulated_antibodies, 1):
            prompt_lines.append(f"  - Guard {i} ({ab['code']}): {ab['correction']}")
        prompt_lines.append("")

    prompt_lines.append(
        "MANDATORY 4-STEP TOPOLOGICAL SCRATCHPAD:\n"
        "Step 1: Write the sum over 2^k flip states for a subgraph with k cycles.\n"
        "Step 2: Factorize the sign sigma(C) into the product of independent cycle signs: sigma(C) = prod_i s_i^{I(c_i)}.\n"
        "Step 3: Show that when any I(c_i) = 1, the sum factors as (1 + (-1)) * prod_{j != i} (...) = 0.\n"
        "Step 4: Count the subgraphs where all I(c_i) = 0 and compute Z.\n\n"
        "Return ONLY a JSON object with: cycle_independence, cycle_parity_invariant_found, cancellation_mechanism, zero_odd_sector_subgraphs, exact_partition_z, scratchpad."
    )

    full_text = "\n".join(prompt_lines)
    assert_lexical_hygiene(full_text)
    return full_text


if __name__ == "__main__":
    packet = generate_blind_problem_packet()
    p1 = build_prompt_arm1_constrained_decoding(packet)
    p2 = build_prompt_arm2_attention_masking(packet)
    p3 = build_prompt_arm3_hieroglyphics(packet)
    p4 = build_prompt_arm4_immune_round(packet, 1, [])
    p5 = build_prompt_arm5_hybrid(packet)

    print("Prompt Builder Test:")
    print(f"  Arm 1 length: {len(p1)} chars")
    print(f"  Arm 2 length: {len(p2)} chars")
    print(f"  Arm 3 length: {len(p3)} chars")
    print(f"  Arm 4 length: {len(p4)} chars")
    print(f"  Arm 5 length: {len(p5)} chars")
    print("All 5 prompt arms built with verified lexical hygiene: PASS")
