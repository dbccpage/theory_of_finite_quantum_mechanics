"""
a2_llm_proposer.py — OpenRouter LLM proposer for Target A2 (det=0 witness search).

This is where an LLM proposer provides genuine value: the det=0 surface
is an algebraic variety where creative proposals from a language model
can discover exact rational points that a grid search would miss.

The governor uses the 3-vertex cycle encoding from mub6_symbol_game_session.py:
  det = ad - bc - (a - b) - (d - c)
  Phi_1 = |det| exactly (H^1 cohomological obstruction)

AuthorityEffect: None.
stated region only; mints no authority
"""

import json
import os
import sys
from fractions import Fraction
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from .mub6_proposer import _safe_eval
from .openrouter_proposer import OpenRouterProposer, scripted_fallback_proposer
from .a1_collar_swarm import _clean_response, load_governor_module
from . import l1_governor


def build_det_cycle(gov_mod):
    """3-vertex directed cycle encoding det = prod_diff - lin_corr."""
    return gov_mod.ConstraintGraph(
        vertices=("origin", "mid", "end"),
        edges=(
            gov_mod.Edge("origin", "mid", weight=1),
            gov_mod.Edge("mid", "end", weight=1),
            gov_mod.Edge("end", "origin", weight=1),
        ),
    )


def verify_witness(a, b, c, d, gov_mod):
    """Verify a witness (a,b,c,d) using the full L1SymbolGameGovernor.
    
    Returns (det, phi1, governor) tuple.
    """
    prod_diff = a * d - b * c
    lin_corr = (a - b) + (d - c)
    det = prod_diff - lin_corr
    
    graph = build_det_cycle(gov_mod)
    gov = gov_mod.L1SymbolGameGovernor(graph)
    
    gov.step_assert("origin", "mid", prod_diff, step_id="assert_prod")
    gov.step_assert("mid", "end", -lin_corr, step_id="assert_lin")
    gov.step_assert("end", "origin", Fraction(0), step_id="assert_close")
    
    projected = gov.project(gov.section)
    gov.step_cut(proposed_section=projected, step_id="cut")
    gov.step_verify("ZERO_OBSTRUCTION", step_id="verify")
    
    phi1 = gov.primary_obstruction()
    return det, phi1, gov


class A2WitnessSearch:
    """Search for exact rational witnesses on the det=0 surface using an LLM."""
    
    def __init__(self, proposer, max_turns=50):
        self.proposer = proposer
        self.max_turns = max_turns
        self.admitted = []
        self.refused = []
        self.phi1_trajectory = []
        self.gov_mod = load_governor_module()
    
    def run(self):
        """Run the witness search loop."""
        last_failure = ""
        
        for turn in range(self.max_turns):
            # Build the prompt with Gamma_2 feedback
            admitted_summary = ""
            if self.admitted:
                examples = []
                for w in self.admitted[-3:]:
                    examples.append(
                        f"  a={w['a']}, b={w['b']}, c={w['c']}, d={w['d']} "
                        f"(det={w['det']})"
                    )
                admitted_summary = "Already admitted:\n" + "\n".join(examples) + "\n"
            
            prompt = (
                "Return ONLY a Python dict on one line, no markdown:\n"
                "{'a': Fraction(p,q), 'b': Fraction(r,s), "
                "'c': Fraction(u,v), 'd': Fraction(w,x)}\n\n"
                "CONSTRAINT: det = a*d - b*c - (a-b) - (d-c) must equal ZERO.\n"
                "The det=0 surface is: a*d - b*c = a - b + d - c.\n"
                "Find DIVERSE exact rational points on this surface.\n"
                "Avoid a=b=c=d=0 and other trivial solutions.\n"
                "Try parametric families: e.g. fix c=1, d=1, then a*1-b*1 = a-b+1-1 "
                "gives a-b = a-b (always true). Or fix a, solve for d.\n"
                f"{admitted_summary}"
                f"Admitted witnesses: {len(self.admitted)}. "
                f"Refused: {len(self.refused)}.\n"
            )
            if last_failure:
                prompt += f"Last failure: {last_failure}\n"
            
            response = self.proposer(prompt)
            if not response or not response.strip():
                continue
            
            response = _clean_response(response)
            if not response:
                continue
            
            try:
                witness = _safe_eval(response)
                if not isinstance(witness, dict):
                    last_failure = "Response must be a dict with keys a, b, c, d"
                    continue
                
                a = witness.get("a")
                b = witness.get("b")
                c = witness.get("c")
                d = witness.get("d")
                
                if any(x is None for x in [a, b, c, d]):
                    last_failure = "Dict must have keys 'a', 'b', 'c', 'd'"
                    continue
                
                if not all(isinstance(x, Fraction) for x in [a, b, c, d]):
                    last_failure = "All values must be Fraction(num, den)"
                    continue
                
                # Check for duplicates
                witness_tuple = (a, b, c, d)
                if witness_tuple in {(w["a"], w["b"], w["c"], w["d"]) for w in self.admitted}:
                    last_failure = f"Duplicate witness (a={a}, b={b}, c={c}, d={d})"
                    continue
                
                # Run through the full governor
                det, phi1, gov = verify_witness(a, b, c, d, self.gov_mod)
                self.phi1_trajectory.append(phi1)
                
                record = {
                    "turn": turn,
                    "a": a, "b": b, "c": c, "d": d,
                    "det": det,
                    "phi1": phi1,
                    "prod_diff": a * d - b * c,
                    "lin_corr": (a - b) + (d - c),
                }
                
                if phi1 == 0:
                    record["verdict"] = "ADMITTED"
                    self.admitted.append(record)
                    last_failure = ""
                    print(f"  Turn {turn}: ADMITTED a={a}, b={b}, c={c}, d={d} (det={det})")
                else:
                    record["verdict"] = "REFUSED"
                    self.refused.append(record)
                    last_failure = (
                        f"REFUSED: det={det} (must be 0). "
                        f"Phi_1={phi1}. "
                        f"prod_diff={record['prod_diff']}, "
                        f"lin_corr={record['lin_corr']}. "
                        f"Need prod_diff = lin_corr exactly."
                    )
                    print(f"  Turn {turn}: REFUSED a={a}, b={b}, c={c}, d={d} "
                          f"(det={det}, Phi_1={phi1})")
                    
            except ValueError as e:
                last_failure = f"Rejected: {str(e)}"
            except Exception as e:
                last_failure = f"Parse error: {type(e).__name__}: {str(e)}"
        
        return {
            "target": "A2 (det=0 singularity surface)",
            "protocol": "PO-032 L1SymbolGameGovernor (cycle encoding)",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "authority_effect": "None",
            "total_turns": self.max_turns,
            "admitted_count": len(self.admitted),
            "refused_count": len(self.refused),
            "admitted": self.admitted,
            "refused": self.refused[:10],
            "phi1_trajectory": self.phi1_trajectory,
        }
    
    def save_receipt(self, path):
        """Save session receipt as JSON."""
        result = self.run.__wrapped__ if hasattr(self.run, '__wrapped__') else None
        # Use last run result
        receipt = {
            "admitted": [
                {"a": str(w["a"]), "b": str(w["b"]),
                 "c": str(w["c"]), "d": str(w["d"]),
                 "det": str(w["det"]), "phi1": str(w["phi1"])}
                for w in self.admitted
            ],
            "refused_count": len(self.refused),
            "phi1_trajectory": [str(p) for p in self.phi1_trajectory],
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(receipt, f, indent=2)


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if api_key:
        proposer = OpenRouterProposer(
            api_key=api_key,
            model="deepseek/deepseek-chat",
            temperature=0.3,  # slightly higher for diversity
            max_tokens=256,
        ).complete
        print("Using OpenRouter (DeepSeek V3)")
    else:
        # Scripted fallback with mix of good and bad witnesses
        moves = [
            "{'a': Fraction(1, 2), 'b': Fraction(1, 3), 'c': Fraction(1, 3), 'd': Fraction(1, 9)}",
            "{'a': Fraction(2, 1), 'b': Fraction(3, 1), 'c': Fraction(1, 1), 'd': Fraction(2, 1)}",
            "{'a': Fraction(5, 7), 'b': Fraction(5, 7), 'c': Fraction(1, 1), 'd': Fraction(1, 1)}",
            "{'a': Fraction(3, 1), 'b': Fraction(2, 1), 'c': Fraction(1, 1), 'd': Fraction(1, 1)}",
            "{'a': Fraction(0, 1), 'b': Fraction(0, 1), 'c': Fraction(1, 1), 'd': Fraction(1, 1)}",
            "{'a': Fraction(7, 3), 'b': Fraction(4, 3), 'c': Fraction(1, 1), 'd': Fraction(1, 1)}",
        ]
        proposer = scripted_fallback_proposer(moves)
        print("Using scripted fallback (no API key)")
    
    search = A2WitnessSearch(proposer, max_turns=50)
    result = search.run()
    
    search.save_receipt("research/a2_witness_search_receipt.json")
    
    print(f"\n=== A2 Witness Search Results ===")
    print(f"Admitted: {result['admitted_count']}")
    print(f"Refused: {result['refused_count']}")
    if result['phi1_trajectory']:
        print("Phi_1 trajectory: " + " -> ".join(str(p) for p in result['phi1_trajectory'][:20]))


if __name__ == "__main__":
    main()
