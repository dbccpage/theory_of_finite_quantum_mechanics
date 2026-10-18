"""
OpenRouter Proposer Adapter with Mechanism Steering and L1 Governor Closed-Loop.

Features:
- Parameter steering via `logit_bias` targeting declared token sequences.
- Next-token logprob extraction and confidence scoring for candidate algebraic proposals.
- Closed-loop coupling with fail-closed L1 governor (`l1_governor.py`) ensuring monotonic defect descent.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority
"""

from __future__ import annotations

import ast
import json
import math
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

from .l1_governor import (
    Cochain1,
    ConstraintGraph,
    Edge,
    GovernorVerdict,
    L1SymbolGameGovernor,
)
from .mechanism_proposer import CarrierGrammar


# =============================================================================
# 1. Logit Bias & Steering Utilities
# =============================================================================

def build_logit_bias(
    force_tokens: Sequence[Union[int, str]],
    suppress_tokens: Sequence[Union[int, str]],
    force_bias: int = 100,
    suppress_bias: int = -100,
    tokenizer_name: str = "o200k_base",
) -> Dict[int, int]:
    """
    Constructs a logit_bias dictionary mapping integer token IDs to bias values.
    Supports integer token IDs or surface string tokens (resolved via tiktoken).

    Validates:
    - String tokens resolve to distinct single token IDs.
    - force and suppress token IDs do not overlap.
    """
    force_ids: List[int] = []
    suppress_ids: List[int] = []

    def _resolve_token(token: Union[int, str]) -> int:
        if isinstance(token, int):
            return token
        try:
            import tiktoken
            enc = tiktoken.get_encoding(tokenizer_name)
            ids = enc.encode(token)
            if len(ids) != 1:
                raise ValueError(
                    f"token '{token}' encodes to {len(ids)} tokens; must be a distinct single token"
                )
            return ids[0]
        except ImportError:
            raise ImportError("tiktoken is required to encode string token targets into token IDs")

    for t in force_tokens:
        force_ids.append(_resolve_token(t))
    for t in suppress_tokens:
        suppress_ids.append(_resolve_token(t))

    force_set = set(force_ids)
    suppress_set = set(suppress_ids)

    if force_set & suppress_set:
        raise ValueError("force and suppress must be distinct single tokens")

    bias_dict: Dict[int, int] = {}
    for fid in force_ids:
        bias_dict[fid] = force_bias
    for sid in suppress_ids:
        bias_dict[sid] = suppress_bias

    return bias_dict


def compute_logprob_confidence(logprobs: Sequence[float]) -> float:
    """
    Computes a normalized confidence score in [0.0, 1.0] from a sequence of logprobs.
    Uses the geometric mean of token probabilities: exp(mean(logprob)).
    """
    valid_lps = [lp for lp in logprobs if math.isfinite(lp)]
    if not valid_lps:
        return 0.0
    mean_lp = sum(valid_lps) / len(valid_lps)
    score = math.exp(mean_lp)
    return max(0.0, min(1.0, score))


# =============================================================================
# 2. Proposal Response Dataclass
# =============================================================================

@dataclass
class ProposalResponse:
    """
    Encapsulates candidate algebraic proposal outputs with optional logprob
    and confidence metadata.
    """
    content: str
    tokens: List[str] = field(default_factory=list)
    logprobs: List[float] = field(default_factory=list)
    top_logprobs: List[List[Dict[str, float]]] = field(default_factory=list)
    confidence_score: float = 0.0
    raw_json: Optional[Dict[str, Any]] = None


# =============================================================================
# 3. OpenRouter Proposer Adapter
# =============================================================================

class OpenRouterProposer:
    """
    OpenRouter API adapter supporting:
    - logit_bias parameter steering.
    - logprob extraction and confidence scoring.
    - Fail-closed error handling (returns empty proposal on network error).
    """

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek/deepseek-chat",
        temperature: float = 0.1,
        max_tokens: int = 512,
        logit_bias: Optional[Dict[Union[int, str], int]] = None,
        logprobs: bool = False,
        top_logprobs: Optional[int] = None,
        base_url: str = "https://openrouter.ai/api/v1",
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logit_bias = logit_bias
        self.logprobs = logprobs
        self.top_logprobs = top_logprobs
        self.base_url = base_url.rstrip("/")
        self.system_prompt = (
            "You are a mathematical proposer. Return ONLY a single-line Python dict "
            "expression. Use Fraction(num, den) for all values. "
            "NO markdown, NO code fences, NO explanations, NO text before or after. "
            "Example: {'a': Fraction(1, 2), 'b': Fraction(3, 4)}"
        )

    def _prepare_payload(
        self,
        prompt: str,
        logit_bias: Optional[Dict[Union[int, str], int]] = None,
        request_logprobs: bool = False,
        top_logprobs: Optional[int] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        # Format logit bias
        merged_bias: Dict[str, int] = {}
        if self.logit_bias:
            for k, v in self.logit_bias.items():
                merged_bias[str(k)] = v
        if logit_bias:
            for k, v in logit_bias.items():
                merged_bias[str(k)] = v
        if merged_bias:
            data["logit_bias"] = merged_bias

        # Format logprobs
        if request_logprobs or self.logprobs:
            data["logprobs"] = True
            top_k = top_logprobs or self.top_logprobs or 5
            data["top_logprobs"] = top_k

        return data

    def complete(
        self,
        prompt: str,
        logit_bias: Optional[Dict[Union[int, str], int]] = None,
    ) -> str:
        """
        Sends completion request and returns generated text.
        Returns empty string on network error (fail-closed).
        """
        time.sleep(0.1)
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dbccpage/MUB6",
            "X-Title": "MUB6-SymbolGame",
        }
        data = self._prepare_payload(prompt, logit_bias=logit_bias, request_logprobs=False)

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read().decode("utf-8")
                response_json = json.loads(response_body)
                return response_json["choices"][0]["message"]["content"].strip()
        except Exception:
            return ""

    def complete_with_logprobs(
        self,
        prompt: str,
        logit_bias: Optional[Dict[Union[int, str], int]] = None,
        top_logprobs: Optional[int] = None,
    ) -> ProposalResponse:
        """
        Sends completion request with logprob extraction and confidence scoring.
        Returns ProposalResponse with empty content and zero confidence on error.
        """
        time.sleep(0.1)
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dbccpage/MUB6",
            "X-Title": "MUB6-SymbolGame",
        }
        data = self._prepare_payload(
            prompt,
            logit_bias=logit_bias,
            request_logprobs=True,
            top_logprobs=top_logprobs,
        )

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read().decode("utf-8")
                response_json = json.loads(response_body)
                choice = response_json["choices"][0]
                content = choice["message"]["content"].strip()

                tokens: List[str] = []
                logprobs: List[float] = []
                top_lps: List[List[Dict[str, float]]] = []

                lp_info = choice.get("logprobs")
                if lp_info and "content" in lp_info and lp_info["content"]:
                    for item in lp_info["content"]:
                        tok_str = item.get("token", "")
                        tok_lp = float(item.get("logprob", 0.0))
                        tokens.append(tok_str)
                        logprobs.append(tok_lp)

                        step_top: List[Dict[str, float]] = []
                        if "top_logprobs" in item:
                            for top_entry in item["top_logprobs"]:
                                step_top.append({
                                    top_entry.get("token", ""): float(top_entry.get("logprob", 0.0))
                                })
                        top_lps.append(step_top)

                confidence = compute_logprob_confidence(logprobs) if logprobs else 0.5
                return ProposalResponse(
                    content=content,
                    tokens=tokens,
                    logprobs=logprobs,
                    top_logprobs=top_lps,
                    confidence_score=confidence,
                    raw_json=response_json,
                )
        except Exception:
            return ProposalResponse(content="", confidence_score=0.0)

    def steer_logit_bias(
        self,
        prompt: str,
        force: Union[int, str],
        suppress: Union[int, str],
        force_bias: int = 100,
        suppress_bias: int = -100,
    ) -> str:
        """Convenience method steering generation with a single force/suppress token pair."""
        bias = build_logit_bias(
            force_tokens=[force],
            suppress_tokens=[suppress],
            force_bias=force_bias,
            suppress_bias=suppress_bias,
        )
        return self.complete(prompt, logit_bias=bias)


# =============================================================================
# 4. Fallback Scripted Proposers
# =============================================================================

def scripted_fallback_proposer(
    moves: Sequence[Union[str, ProposalResponse]]
) -> Callable[[str], str]:
    """Returns a deterministic callable proposing each move in sequence."""
    moves_iter = iter(moves)

    def complete(prompt: str) -> str:
        try:
            val = next(moves_iter)
            return val.content if isinstance(val, ProposalResponse) else str(val)
        except StopIteration:
            return ""

    return complete


def scripted_logprob_proposer(
    responses: Sequence[ProposalResponse]
) -> Callable[[str], ProposalResponse]:
    """Returns a deterministic callable proposing structured ProposalResponse items."""
    resp_iter = iter(responses)

    def complete(prompt: str) -> ProposalResponse:
        try:
            return next(resp_iter)
        except StopIteration:
            return ProposalResponse(content="", confidence_score=0.0)

    return complete


# =============================================================================
# 5. Closed-Loop L1 Governor Integration
# =============================================================================

def parse_candidate_proposal(content: str) -> Any:
    """
    Parses candidate mathematical proposal strings into Python dictionary or list structure.
    Strictly forbids floats and non-deterministic/un-safe syntax.
    """
    clean = content.strip()
    if clean.startswith("```"):
        lines = clean.split("\n")
        clean = "\n".join(line for line in lines if not line.strip().startswith("```")).strip()

    # Try list of integers or fractions: e.g. "-2 1 1"
    space_tokens = clean.split()
    if space_tokens and all(re.fullmatch(r"-?\d+(/\d+)?", tok) for tok in space_tokens):
        return [Fraction(tok) for tok in space_tokens]

    grammar = CarrierGrammar()
    return grammar.safe_parse_proposal(clean)


class GovernedProposer:
    """
    Closed-loop proposer governor that wires language model proposals directly
    to the exact discrete L1 projection governor (L1SymbolGameGovernor).
    
    Enforces:
    1. Pure-Python carrier grammar and token-level validation.
    2. Strict zero-float AST discipline (FLOAT_REJECTED).
    3. Fail-closed monotonic defect descent (rejects defect increases and unparseable proposals).
    """

    def __init__(
        self,
        proposer: Union[
            OpenRouterProposer,
            Callable[[str], str],
            Callable[[str], ProposalResponse],
        ],
        governor: L1SymbolGameGovernor,
        carrier_grammar: Optional[CarrierGrammar] = None,
    ) -> None:
        self.proposer = proposer
        self.governor = governor
        self.carrier_grammar = carrier_grammar or CarrierGrammar()

    def propose_and_verify(
        self,
        prompt: str,
        parse_fn: Optional[Callable[[str], Any]] = None,
        step_id: Optional[str] = None,
    ) -> Tuple[GovernorVerdict, ProposalResponse]:
        """
        Executes one proposer query turn and validates the proposal against the L1 governor.
        Returns a tuple of (GovernorVerdict, ProposalResponse).
        """
        sid = step_id or f"step_{len(self.governor.history) + 1:03d}"
        defect_before = self.governor.section_defect()

        # 1. Obtain proposer response
        if isinstance(self.proposer, OpenRouterProposer):
            if self.proposer.logprobs:
                response = self.proposer.complete_with_logprobs(prompt)
            else:
                raw_text = self.proposer.complete(prompt)
                response = ProposalResponse(content=raw_text)
        else:
            proposer_out = self.proposer(prompt)
            if isinstance(proposer_out, ProposalResponse):
                response = proposer_out
            else:
                response = ProposalResponse(content=str(proposer_out))

        if not response.content:
            return (
                GovernorVerdict(
                    admitted=False,
                    status="RefusedEmpty",
                    defect_before=defect_before,
                    defect_after=defect_before,
                    details="Proposer returned empty response.",
                    step_id=sid,
                ),
                response,
            )

        # 2. Validate carrier grammar
        is_carrier, char_reason = self.carrier_grammar.validate_string(response.content)
        if not is_carrier:
            return (
                GovernorVerdict(
                    admitted=False,
                    status="RefusedOffCarrier",
                    defect_before=defect_before,
                    defect_after=defect_before,
                    details=f"Off-carrier character detected: {char_reason}",
                    step_id=sid,
                ),
                response,
            )

        # 3. Parse proposal safely
        try:
            if parse_fn is not None:
                parsed = parse_fn(response.content)
            else:
                parsed = parse_candidate_proposal(response.content)
        except ValueError as e:
            err_msg = str(e)
            status = "RefusedInvalidAST" if "FLOAT_REJECTED" in err_msg else "UnparseableProposal"
            return (
                GovernorVerdict(
                    admitted=False,
                    status=status,
                    defect_before=defect_before,
                    defect_after=defect_before,
                    details=f"Parsing failed: {err_msg}",
                    step_id=sid,
                ),
                response,
            )
        except Exception as e:
            return (
                GovernorVerdict(
                    admitted=False,
                    status="UnparseableProposal",
                    defect_before=defect_before,
                    defect_after=defect_before,
                    details=f"Unexpected parsing exception: {e}",
                    step_id=sid,
                ),
                response,
            )

        # 4. Dispatch to governor step_cut
        if isinstance(parsed, dict):
            # Check if dict represents edge claims or vertex potentials
            is_edge_claims = any(
                (isinstance(k, tuple) and len(k) == 2)
                or (isinstance(k, str) and ("->" in k or "," in k))
                for k in parsed.keys()
            )

            if is_edge_claims:
                normalized_claims: Dict[Tuple[str, str], Fraction] = {}
                for k, v in parsed.items():
                    if isinstance(k, str) and "->" in k:
                        u, v_node = k.split("->", 1)
                        normalized_claims[(u.strip(), v_node.strip())] = Fraction(v)
                    elif isinstance(k, (tuple, list)) and len(k) == 2:
                        normalized_claims[(str(k[0]), str(k[1]))] = Fraction(v)
                    else:
                        normalized_claims[k] = Fraction(v)
                verdict = self.governor.step_cut(proposed_claims=normalized_claims, step_id=sid)
            else:
                # Vertex potential section
                normalized_section: Dict[str, Fraction] = {
                    str(k): Fraction(v) for k, v in parsed.items()
                }
                verdict = self.governor.step_cut(proposed_section=normalized_section, step_id=sid)

        elif isinstance(parsed, (list, tuple)):
            edges = self.governor.graph.edges
            if len(parsed) != len(edges):
                return (
                    GovernorVerdict(
                        admitted=False,
                        status="MoveViolation",
                        defect_before=defect_before,
                        defect_after=defect_before,
                        details=f"List proposal dimension {len(parsed)} does not match edge count {len(edges)}.",
                        step_id=sid,
                    ),
                    response,
                )
            proposed_claims = {
                e.key: Fraction(parsed[idx]) for idx, e in enumerate(edges)
            }
            verdict = self.governor.step_cut(proposed_claims=proposed_claims, step_id=sid)
        else:
            return (
                GovernorVerdict(
                    admitted=False,
                    status="UnparseableProposal",
                    defect_before=defect_before,
                    defect_after=defect_before,
                    details=f"Unrecognized proposal object type: {type(parsed).__name__}",
                    step_id=sid,
                ),
                response,
            )

        return verdict, response

    def run_repair_loop(
        self,
        base_prompt: str,
        parse_fn: Optional[Callable[[str], Any]] = None,
        max_turns: int = 5,
        target_defect: Fraction = Fraction(0),
    ) -> Dict[str, Any]:
        """
        Drives a multi-turn repair loop until defect reaches target_defect or max_turns exceeded.
        Enforces fail-closed monotonic descent.
        """
        initial_defect = self.governor.section_defect()
        initial_phi1 = self.governor.primary_obstruction()
        turns: List[Dict[str, Any]] = []
        history_prompt = ""
        terminal = "SURVIVOR_OBSTRUCTION"

        for turn_idx in range(1, max_turns + 1):
            prompt = base_prompt + history_prompt
            verdict, resp = self.propose_and_verify(
                prompt=prompt,
                parse_fn=parse_fn,
                step_id=f"turn_{turn_idx:02d}",
            )
            current_defect = self.governor.section_defect()
            current_phi1 = self.governor.primary_obstruction()

            turns.append({
                "turn": turn_idx,
                "content": resp.content,
                "confidence_score": resp.confidence_score,
                "admitted": verdict.admitted,
                "status": verdict.status,
                "defect_before": str(verdict.defect_before),
                "defect_after": str(verdict.defect_after),
                "primary_obstruction": str(current_phi1),
                "details": verdict.details,
            })

            if verdict.admitted and (current_defect <= target_defect or current_phi1 <= target_defect):
                terminal = "ACCEPTED_ZERO_DEFECT"
                break

            history_prompt += (
                f"\n(Turn {turn_idx}: proposal gave status {verdict.status} "
                f"with defect {current_defect}; please propose a strict descent repair.)"
            )

        final_defect = self.governor.section_defect()
        final_phi1 = self.governor.primary_obstruction()

        # Fail-closed invariant check: final defect cannot exceed initial defect
        assert final_defect <= initial_defect or final_phi1 <= initial_phi1, (
            "Fail-closed invariant violation: defect increased in repair loop"
        )

        return {
            "terminal": terminal,
            "turns": turns,
            "initial_defect": str(initial_defect),
            "final_defect": str(final_defect),
            "initial_phi1": str(initial_phi1),
            "final_phi1": str(final_phi1),
            "turns_count": len(turns),
        }
