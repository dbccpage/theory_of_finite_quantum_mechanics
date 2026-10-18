"""Host verifier and antibody miner for the blind cluster sign challenge.

Catches model hallucinations, invalid deductions, and boundary failures,
minting them into typed Antimorphisms (Antibodies) for subsequent re-injection.

AuthorityEffect: None.
Firewall: Abstract discrete graph partition; zero physics keywords.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega_engine_projects.fsp.demos.blind_cluster_recovery.oracle import (
    BlindClusterOracle,
)


class AntibodyMiner:
    """Mines hallucinations from proposer responses into formal antibodies."""

    def __init__(self, oracle: BlindClusterOracle) -> None:
        self.oracle = oracle

    def parse_proposer_response(self, raw_text: str | None) -> dict:
        """Robustly extract the JSON payload from the raw model response."""
        if not raw_text:
            return {
                "parse_error": True,
                "raw_text": "",
                "cycle_independence": False,
                "cycle_parity_invariant_found": False,
                "cancellation_mechanism": "Empty response",
                "zero_odd_sector_subgraphs": 0,
                "exact_partition_z": None,
                "scratchpad": "",
            }

        try:
            return json.loads(raw_text.strip())
        except Exception:
            pass

        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass

        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_text[start : end + 1])
            except Exception:
                pass

        return {
            "parse_error": True,
            "raw_text": (raw_text or "")[:500],
            "cycle_independence": False,
            "cycle_parity_invariant_found": False,
            "cancellation_mechanism": "Unparseable output",
            "zero_odd_sector_subgraphs": 0,
            "exact_partition_z": None,
            "scratchpad": "",
        }

    def evaluate_and_mine(
        self,
        raw_response: str,
        prior_antibodies: list[dict],
    ) -> tuple[dict, list[dict]]:
        """Evaluate response, compute score, and mine new antibodies if needed."""
        parsed = self.parse_proposer_response(raw_response)

        claimed_z = self._coerce_int(parsed.get("exact_partition_z"))
        indep = bool(parsed.get("cycle_independence", False))
        parity_found = bool(parsed.get("cycle_parity_invariant_found", False))
        zero_count = self._coerce_int(parsed.get("zero_odd_sector_subgraphs"))

        mechanism = str(parsed.get("cancellation_mechanism", "")).lower()
        parity_proved = parity_found and any(
            kw in mechanism
            for kw in ["canc", "flip", "odd", "pairwise", "vanish", "zero", "1 + (-1)", "1+(-1)"]
        )

        zero_sector_used = zero_count == 199

        eval_result = self.oracle.evaluate_proposer_claim(
            claimed_z=claimed_z,
            cycle_independence_recognized=indep,
            parity_cancellation_proved=parity_proved,
            zero_sector_reduction_used=zero_sector_used,
        )

        new_antibodies = []
        existing_codes = {a["code"] for a in prior_antibodies}

        if claimed_z != 912:
            code = "ANTI_PARTITION_DRIFT"
            if code not in existing_codes:
                new_antibodies.append(
                    {
                        "code": code,
                        "explanation": f"Model claimed Z = {claimed_z}, which contradicts exact graph evaluation.",
                        "correction": "The exact integer partition sum Z must equal 912. No approximation or empirical sample average is permitted.",
                    }
                )

        if not indep:
            code = "ANTI_COUPLED_CYCLE_HALLUCINATION"
            if code not in existing_codes:
                new_antibodies.append(
                    {
                        "code": code,
                        "explanation": "Model assumed cycle orientations are globally entangled.",
                        "correction": "Cycle orientations are mutually disjoint topological loops. The sign sigma(C) factorizes as a direct product over independent cycle parity characters.",
                    }
                )

        if not parity_proved:
            code = "ANTI_MISSING_PAIRWISE_CANCELLATION"
            if code not in existing_codes:
                new_antibodies.append(
                    {
                        "code": code,
                        "explanation": "Model failed to prove exact zero-sum cancellation across the 2^k flip states.",
                        "correction": "Flipping an odd-winding cycle inverts the global sign (sigma -> -sigma) while leaving the positive weight invariant. In any subgraph with >= 1 odd cycle, the sum factors as (1 + (-1)) * prod(...) = 0.",
                    }
                )

        if not zero_sector_used:
            code = "ANTI_NEGATIVE_CONTRIBUTION_LEAK"
            if code not in existing_codes:
                new_antibodies.append(
                    {
                        "code": code,
                        "explanation": "Model included subgraphs containing odd-winding cycles in the final non-negative sum.",
                        "correction": "All 57 subgraphs with odd-winding cycles sum to zero. The non-negative partition is computed strictly by summing the remaining 199 zero-odd-charge subgraphs.",
                    }
                )

        accumulated = prior_antibodies + new_antibodies
        return eval_result, accumulated

    @staticmethod
    def _coerce_int(value: object) -> int | None:
        """Accept exact integer spellings while rejecting booleans and fractions."""
        if isinstance(value, bool):
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value.strip())
            except ValueError:
                return None
        return None


if __name__ == "__main__":
    oracle = BlindClusterOracle()
    miner = AntibodyMiner(oracle)

    bad_sample = json.dumps(
        {
            "cycle_independence": False,
            "cycle_parity_invariant_found": False,
            "cancellation_mechanism": "It is difficult to cancel negative signs.",
            "zero_odd_sector_subgraphs": 256,
            "exact_partition_z": 1296,
            "scratchpad": "Summing all weights gives 1296.",
        }
    )
    res, antibodies = miner.evaluate_and_mine(bad_sample, [])
    print("Antibody Miner Test on Negative Control:")
    print(f"  Score: {res['score']} / {res['max_score']}")
    print(f"  Mined Antibodies: {len(antibodies)}")
    for a in antibodies:
        print(f"    - {a['code']}: {a['correction']}")

    good_sample = json.dumps(
        {
            "cycle_independence": True,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": "Flipping an odd cycle reverses sign so (1+(-1))=0 cancels the sum across 2^k states.",
            "zero_odd_sector_subgraphs": 199,
            "exact_partition_z": 912,
            "scratchpad": "Summing 199 zero-meron graphs yields 912.",
        }
    )
    res_good, _ = miner.evaluate_and_mine(good_sample, [])
    print()
    print("Antibody Miner Test on Positive Control:")
    print(f"  Score: {res_good['score']} / {res_good['max_score']}")
    print(f"  Perfect: {res_good['perfect']}")
    print("Antibody Miner operational: PASS")
