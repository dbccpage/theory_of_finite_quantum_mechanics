"""Helpers shared by the A2 collar proposers.

The ``A1CollarSwarm`` class that lived here was removed on 2026-10-06. Its ``run``
refused with ``FUNCTIONAL_BOUNDARY_UNAVAILABLE`` (uncovered area cannot be reported as
Phi1), so it ran nothing; ``scripts/run_live_swarm.py`` only called that refusing
method and was removed with it. Git history keeps both.

AuthorityEffect: None.
"""

import re
from fractions import Fraction


def _clean_response(text: str) -> str:
    """Strip markdown fences, preamble, and extract the dict expression.
    
    LLMs often wrap responses in ```python ... ``` blocks or add
    explanatory text. This extracts just the {..} dict expression.
    """
    # Remove ```python ... ``` fences
    text = re.sub(r'```(?:python)?\s*', '', text)
    
    # Find the first { and last } to extract the dict
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace == -1 or last_brace == -1 or first_brace >= last_brace:
        return ""
    
    extracted = text[first_brace:last_brace + 1]
    
    # Collapse to single line (some models use multiline dicts)
    extracted = ' '.join(extracted.split())
    
    return extracted

def load_governor_module():
    from . import l1_governor
    return l1_governor

def build_box_cycle_graph(gov_module):
    return gov_module.ConstraintGraph(
        vertices=("start", "mid", "end"),
        edges=(
            gov_module.Edge("start", "mid", weight=1),
            gov_module.Edge("mid", "end", weight=1),
            gov_module.Edge("end", "start", weight=1),
        ),
    )

def cos_rational_approx(x: Fraction) -> Fraction:
    return Fraction(1) - (x**2) / Fraction(2) + (x**4) / Fraction(24)
