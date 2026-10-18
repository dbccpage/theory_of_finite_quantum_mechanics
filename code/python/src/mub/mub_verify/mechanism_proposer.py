"""
Mechanism & Attention Proposer Integration for MUB(6) Variety Search.

Ported from Symbol Game mechanism primitives:
- Layer 2 logit-level carrier projection (CarrierProjection): masks off-carrier tokens to -inf.
- Layer 1 2D attention mask distillation and steering (AttentionMaskDistiller): suppresses distractor
  key positions and optionally boosts carrier key positions via additive score biases.
- Pure-Python carrier grammar and token-level validation: provides graceful fallback when PyTorch or
  Transformers are not installed, verifying valid token alphabets and strict zero-float AST rules.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority
"""

from __future__ import annotations

import ast
import math
import re
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False

try:
    import transformers
    from transformers import LogitsProcessor
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    transformers = None
    TRANSFORMERS_AVAILABLE = False
    LogitsProcessor = object



def pure_carrier_projection(
    scores: Union[List[float], List[List[float]]],
    carrier_ids: Sequence[int],
    vocab_size: int,
) -> Union[List[float], List[List[float]]]:
    """
    Pure Python logit carrier projection.
    Sets all off-carrier logits to float("-inf").

    Validates:
    - carrier_ids is non-empty, contains integers in [0, vocab_size - 1].
    - vocab_size >= 1.
    - Each row contains at least one finite allowed token (fail-closed if all allowed are -inf/inf/nan).
    """
    carrier_list = list(carrier_ids)
    if (
        not carrier_list
        or vocab_size < 1
        or any(not isinstance(t, int) or not (0 <= t < vocab_size) for t in carrier_list)
    ):
        raise ValueError("carrier must contain valid token IDs in the score vocabulary")

    carrier_set = set(carrier_list)

    if not scores:
        return scores

    is_1d = not isinstance(scores[0], list)
    rows: List[List[float]] = [scores] if is_1d else scores

    result_rows: List[List[float]] = []
    for row in rows:
        if len(row) != vocab_size:
            raise ValueError(
                f"score vocabulary size {len(row)} does not match expected {vocab_size}"
            )

        allowed_finite = False
        for tid in carrier_list:
            val = row[tid]
            if math.isnan(val) or (math.isinf(val) and val > 0):
                raise ValueError("every score row needs a finite allowed token")
            if math.isfinite(val):
                allowed_finite = True

        if not allowed_finite:
            raise ValueError("every score row needs a finite allowed token")

        new_row = [val if idx in carrier_set else float("-inf") for idx, val in enumerate(row)]
        result_rows.append(new_row)

    return result_rows[0] if is_1d else result_rows


class CarrierProjection(LogitsProcessor if TRANSFORMERS_AVAILABLE else object):
    """
    Layer 2 Carrier Projection:
    Forces next-token probability mass onto the declared carrier simplex face
    by setting every off-carrier logit to -inf.
    Supports both PyTorch Tensors and pure-Python nested lists.
    """

    def __init__(self, carrier_ids: Sequence[int], vocab_size: int) -> None:
        carrier_list = list(carrier_ids)
        if (
            not carrier_list
            or vocab_size < 1
            or any(not isinstance(t, int) or not (0 <= t < vocab_size) for t in carrier_list)
        ):
            raise ValueError("carrier must contain valid token IDs in the score vocabulary")

        self.carrier_ids = sorted(set(carrier_list))
        self.vocab_size = vocab_size

        if TORCH_AVAILABLE and torch is not None:
            mask = torch.ones(vocab_size, dtype=torch.bool)
            mask[self.carrier_ids] = False
            self.off_carrier: Optional[torch.Tensor] = mask
        else:
            self.off_carrier = None

    def __call__(self, input_ids: Any, scores: Any) -> Any:
        if TORCH_AVAILABLE and torch is not None and isinstance(scores, torch.Tensor):
            if scores.ndim not in (1, 2) or scores.shape[-1] != self.vocab_size:
                raise ValueError("score vocabulary does not match the carrier mask")

            orig_ndim = scores.ndim
            if orig_ndim == 1:
                scores = scores.unsqueeze(0)

            assert self.off_carrier is not None
            off_carrier = self.off_carrier.to(scores.device)
            allowed = scores[:, ~off_carrier]

            if (
                torch.isnan(allowed).any()
                or torch.isposinf(allowed).any()
                or not torch.isfinite(allowed).any(dim=1).all()
            ):
                raise ValueError("every score row needs a finite allowed token")

            scores_out = scores.clone()
            scores_out[:, off_carrier] = float("-inf")
            return scores_out.squeeze(0) if orig_ndim == 1 else scores_out
        else:
            return pure_carrier_projection(scores, self.carrier_ids, self.vocab_size)


def build_carrier(tokenizer: Any, allowed: Sequence[str]) -> List[int]:
    """
    Finds all token IDs whose decoded surface text matches one of the declared allowed strings.
    Supports HuggingFace tokenizers, tiktoken encodings, and mock tokenizers.
    """
    allowed_set = set(allowed)
    ids: List[int] = []

    if hasattr(tokenizer, "__len__") and hasattr(tokenizer, "decode"):
        vocab_len = len(tokenizer)
        for tid in range(vocab_len):
            try:
                decoded = tokenizer.decode([tid])
                if decoded.strip() in allowed_set or decoded in allowed_set:
                    ids.append(tid)
            except Exception:
                continue
    elif hasattr(tokenizer, "vocab_size") and hasattr(tokenizer, "decode"):
        for tid in range(tokenizer.vocab_size):
            try:
                decoded = tokenizer.decode([tid])
                if decoded.strip() in allowed_set or decoded in allowed_set:
                    ids.append(tid)
            except Exception:
                continue
    elif hasattr(tokenizer, "get_vocab"):
        vocab = tokenizer.get_vocab()
        for tok_str, tid in vocab.items():
            if tok_str.strip() in allowed_set or tok_str in allowed_set:
                ids.append(tid)
    elif isinstance(tokenizer, dict):
        for tok_str, tid in tokenizer.items():
            if tok_str.strip() in allowed_set or tok_str in allowed_set:
                ids.append(tid)

    if not ids:
        raise ValueError("no tokenizer tokens match the declared carrier")
    return sorted(set(ids))



def create_attention_mask_2d(
    seq_len: int,
    distractor_positions: Sequence[int],
    carrier_positions: Optional[Sequence[int]] = None,
    causal: bool = False,
    additive: bool = False,
    delta: float = 0.0,
    return_tensor: bool = False,
) -> Any:
    """
    Constructs a 2D attention mask [seq_len, seq_len] with distractor suppression
    and optional carrier steering.

    Parameters:
    - seq_len: sequence length.
    - distractor_positions: positions of distractors/fluff tokens to suppress.
    - carrier_positions: positions of carrier tokens (used when delta != 0.0).
    - causal: if True, applies causal lower-triangular masking.
    - additive: if True, creates additive mask (0.0 for attend, -inf for mask, +delta for steer).
                if False, creates multiplicative mask (1.0 for attend, 0.0 for mask).
    - delta: additive attention bias added to carrier key columns.
    - return_tensor: if True and PyTorch is available, returns torch.Tensor.
    """
    if seq_len < 1:
        raise ValueError("seq_len must be positive")

    dist_set = set(distractor_positions)
    carrier_set = set(carrier_positions) if carrier_positions is not None else set()

    for p in dist_set:
        if not (0 <= p < seq_len):
            raise ValueError(f"distractor position {p} out of range [0, {seq_len})")
    for p in carrier_set:
        if not (0 <= p < seq_len):
            raise ValueError(f"carrier position {p} out of range [0, {seq_len})")

    if dist_set & carrier_set:
        raise ValueError("carrier and distractor positions must be disjoint")

    mask: List[List[float]] = []
    for i in range(seq_len):
        row: List[float] = []
        for j in range(seq_len):
            is_masked = (j in dist_set) or (causal and j > i)
            if additive:
                if is_masked:
                    val = float("-inf")
                else:
                    val = delta if (j in carrier_set) else 0.0
            else:
                val = 0.0 if is_masked else 1.0
            row.append(val)
        mask.append(row)

    if return_tensor and TORCH_AVAILABLE and torch is not None:
        return torch.tensor(mask, dtype=torch.float32)
    return mask


class AttentionMaskDistiller:
    """
    Distills and controls 2D attention masks by differentiating carrier tokens from distractors.
    Supports reading attention mass distributions across layers and heads.
    """

    def __init__(
        self,
        seq_len: int,
        carrier_positions: Sequence[int],
        distractor_positions: Sequence[int],
    ) -> None:
        if seq_len < 1:
            raise ValueError("seq_len must be positive")
        self.seq_len = seq_len
        self.carrier_positions = sorted(set(carrier_positions))
        self.distractor_positions = sorted(set(distractor_positions))

        for p in self.carrier_positions:
            if not (0 <= p < seq_len):
                raise ValueError(f"carrier position {p} out of bounds [0, {seq_len})")
        for p in self.distractor_positions:
            if not (0 <= p < seq_len):
                raise ValueError(f"distractor position {p} out of bounds [0, {seq_len})")

        if set(self.carrier_positions) & set(self.distractor_positions):
            raise ValueError("carrier and distractor positions must be disjoint")

    @classmethod
    def from_tokens(
        cls,
        tokens: Sequence[str],
        carrier_patterns: Sequence[str],
        distractor_patterns: Sequence[str],
    ) -> "AttentionMaskDistiller":
        carrier_set = set(carrier_patterns)
        distractor_set = set(distractor_patterns)

        carrier_pos: List[int] = []
        distractor_pos: List[int] = []

        for i, tok in enumerate(tokens):
            clean = tok.strip()
            is_carrier = (
                tok in carrier_set
                or clean in carrier_set
                or any(c in carrier_set for c in clean)
            )
            is_distractor = tok in distractor_set or clean in distractor_set

            if is_carrier and not is_distractor:
                carrier_pos.append(i)
            elif is_distractor and not is_carrier:
                distractor_pos.append(i)

        return cls(len(tokens), carrier_pos, distractor_pos)

    def distill_2d_mask(
        self,
        causal: bool = False,
        additive: bool = False,
        delta: float = 0.0,
        return_tensor: bool = False,
    ) -> Any:
        return create_attention_mask_2d(
            seq_len=self.seq_len,
            distractor_positions=self.distractor_positions,
            carrier_positions=self.carrier_positions,
            causal=causal,
            additive=additive,
            delta=delta,
            return_tensor=return_tensor,
        )

    def compute_attention_mass(
        self,
        attentions: Any,
        query_pos: int = -1,
        layer: int = -1,
    ) -> Dict[str, float]:
        """
        Computes attention mass allocated to carrier vs. distractor key positions
        at query position query_pos.
        Handles:
        - PyTorch tensor: [batch, heads, seq, seq] or [seq, seq]
        - Python nested lists: 4D, 3D, or 2D.
        """
        if TORCH_AVAILABLE and torch is not None and isinstance(attentions, torch.Tensor):
            t = attentions
            if t.ndim == 4:
                row = t[0].mean(dim=0)[query_pos].float().tolist()
            elif t.ndim == 3:
                row = t.mean(dim=0)[query_pos].float().tolist()
            elif t.ndim == 2:
                row = t[query_pos].float().tolist()
            elif t.ndim == 1:
                row = t.float().tolist()
            else:
                raise ValueError(f"unsupported attention tensor shape {t.shape}")
        elif isinstance(attentions, (list, tuple)):
            if len(attentions) > 0 and isinstance(
                attentions[0], (list, tuple, torch.Tensor if TORCH_AVAILABLE and torch is not None else ())
            ):
                elem = attentions[layer]
                if TORCH_AVAILABLE and torch is not None and isinstance(elem, torch.Tensor):
                    return self.compute_attention_mass(elem, query_pos=query_pos)
                if (
                    isinstance(elem[0], list)
                    and isinstance(elem[0][0], list)
                    and isinstance(elem[0][0][0], (int, float))
                ):
                    heads = elem[0]
                    n_heads = len(heads)
                    k_len = len(heads[0][query_pos])
                    row = [
                        sum(heads[h][query_pos][k] for h in range(n_heads)) / n_heads
                        for k in range(k_len)
                    ]
                elif isinstance(elem[0], list) and isinstance(elem[0][0], (int, float)):
                    row = elem[query_pos]
                else:
                    row = list(elem)
            else:
                row = list(attentions)
        else:
            raise TypeError(f"unsupported attention object type: {type(attentions)}")

        total_mass = sum(row)
        if total_mass <= 0:
            return {"carrier_mass": 0.0, "distractor_mass": 0.0, "other_mass": 0.0}

        carrier_mass = sum(row[p] for p in self.carrier_positions if p < len(row))
        distractor_mass = sum(row[p] for p in self.distractor_positions if p < len(row))
        other_mass = total_mass - carrier_mass - distractor_mass

        return {
            "carrier_mass": round(carrier_mass / total_mass, 6),
            "distractor_mass": round(distractor_mass / total_mass, 6),
            "other_mass": round(max(0.0, other_mass) / total_mass, 6),
        }



DEFAULT_MUB6_CARRIER_CHARS: Set[str] = set(
    "0123456789+-*/=(){}[],:.'\" \n\t"
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
)


class CarrierGrammar:
    """
    Pure Python Carrier Grammar and AST Validator.
    Ensures proposals strictly conform to declared character codepoints,
    token sets, and AST zero-float contracts without requiring external libraries.
    """

    def __init__(
        self,
        allowed_chars: Optional[Set[str]] = None,
        allowed_tokens: Optional[Set[str]] = None,
    ) -> None:
        self.allowed_chars = (
            allowed_chars if allowed_chars is not None else set(DEFAULT_MUB6_CARRIER_CHARS)
        )
        self.allowed_tokens = allowed_tokens

    def validate_string(self, text: str) -> Tuple[bool, Optional[str]]:
        """Validates that all characters in text are members of the allowed carrier alphabet."""
        for idx, ch in enumerate(text):
            if ch not in self.allowed_chars:
                return (
                    False,
                    f"Off-carrier character '{ch}' (codepoint U+{ord(ch):04X}) at index {idx}.",
                )
        return True, None

    def validate_token_sequence(self, tokens: Sequence[str]) -> Tuple[bool, Optional[str]]:
        """Validates that each token in sequence belongs to declared allowed_tokens."""
        if self.allowed_tokens is None:
            return True, None
        for idx, tok in enumerate(tokens):
            if tok not in self.allowed_tokens:
                return False, f"Off-carrier token '{tok}' at index {idx}."
        return True, None

    def validate_proposal_ast(self, expression_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validates algebraic proposal using AST:
        - Refuses any float or complex constant (FLOAT_REJECTED).
        - Forbids unsafe nodes (loops, imports, lambdas, attribute mutations).
        - Allows only exact Fractions, Cyc24, integers, and standard container literals.
        """
        try:
            tree = ast.parse(expression_str, mode="eval")
        except Exception as e:
            return False, f"AST parse syntax error: {e}"

        allowed_nodes = (
            ast.Expression,
            ast.Dict,
            ast.List,
            ast.Tuple,
            ast.Set,
            ast.Constant,
            ast.Name,
            ast.Call,
            ast.Load,
            ast.UnaryOp,
            ast.UAdd,
            ast.USub,
            ast.BinOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
        )

        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return False, f"Forbidden AST node: {type(node).__name__}"

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (float, complex)):
                    return False, "FLOAT_REJECTED: floating-point literal detected"
            if isinstance(node, ast.Call):
                if not (isinstance(node.func, ast.Name) and node.func.id in ("Fraction", "Cyc24")):
                    func_repr = ast.unparse(node.func) if hasattr(ast, "unparse") else getattr(node.func, "id", str(node.func))
                    return False, f"CALL_REJECTED: unauthorized function call {func_repr}"
            if isinstance(node, ast.Name):
                if node.id not in ("Fraction", "Cyc24", "None", "True", "False"):
                    pass

        return True, None

    def safe_parse_proposal(self, expression_str: str) -> Any:
        """
        Safely evaluates expression into Fraction/int/str/dict/list structure.
        Refuses float/complex fail-closed.
        """
        is_valid, reason = self.validate_proposal_ast(expression_str)
        if not is_valid:
            raise ValueError(reason)

        allowed_globals: Dict[str, Any] = {
            "Fraction": Fraction,
        }
        try:
            from .cyclotomic import Cyc24
            allowed_globals["Cyc24"] = Cyc24
        except ImportError:
            pass

        try:
            val = eval(expression_str, {"__builtins__": None}, allowed_globals)
        except (TypeError, NameError, Exception) as e:
            raise ValueError(f"Safe parse evaluation error: {e}") from e

        def _check_no_float(v: Any) -> None:
            if isinstance(v, (float, complex)):
                raise ValueError("FLOAT_REJECTED: float value detected in parsed object")
            if isinstance(v, dict):
                for k, sub_v in v.items():
                    _check_no_float(k)
                    _check_no_float(sub_v)
            elif isinstance(v, (list, tuple, set)):
                for item in v:
                    _check_no_float(item)

        _check_no_float(val)
        return val
