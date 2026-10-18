import json
from fractions import Fraction
from typing import Callable, Any, Dict, List, Optional
from dataclasses import dataclass, field
import ast

from .cyclotomic import Cyc24

@dataclass(frozen=True)
class SessionResult:
    terminal_status: str
    admitted: int = 0
    refused: int = 0
    turn_records: Any = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.turn_records, list):
            object.__setattr__(self, "turn_records", tuple(self.turn_records))

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return (
            self.terminal_status == other.terminal_status
            and self.admitted == other.admitted
            and self.refused == other.refused
            and self.turn_records == other.turn_records
        )

def scripted_proposer(moves: list) -> Callable[[str], str]:
    moves_iter = iter(moves)
    def complete(prompt: str) -> str:
        return next(moves_iter)
    return complete

def _safe_eval(val_str: str) -> Any:
    tree = ast.parse(val_str, mode='eval')

    allowed_nodes = (
        ast.Expression, ast.Dict, ast.List, ast.Tuple, ast.Set,
        ast.Constant, ast.Name, ast.Call, ast.Load, ast.UnaryOp,
        ast.UAdd, ast.USub, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (float, complex)):
                raise ValueError("FLOAT_REJECTED")
        if not isinstance(node, allowed_nodes):
            raise ValueError("PARSE_ERROR")
        if isinstance(node, ast.Name):
            if node.id not in ("Fraction", "Cyc24"):
                raise ValueError("PARSE_ERROR")

    allowed_globals = {
        "Fraction": Fraction,
        "Cyc24": Cyc24
    }

    val = eval(val_str, {"__builtins__": None}, allowed_globals)

    def _has_float(v: Any) -> bool:
        if isinstance(v, (float, complex)):
            return True
        if isinstance(v, dict):
            return any(_has_float(k) or _has_float(val) for k, val in v.items())
        if isinstance(v, (list, tuple, set)):
            return any(_has_float(item) for item in v)
        return False

    if _has_float(val):
        raise ValueError("FLOAT_REJECTED")

    return val

class MUB6ProposerHost:
    def __init__(self, complete: Callable[[str], str]):
        self.complete = complete

    def _turn(self, prompt: str, evaluator: Callable[[Any], bool]) -> bool:
        response_str = self.complete(prompt)
        try:
            val = _safe_eval(response_str)
        except ValueError as e:
            if str(e) == "FLOAT_REJECTED":
                return False, "FLOAT_REJECTED"
            return False, "PARSE_ERROR"
        except Exception:
            return False, "PARSE_ERROR"

        try:
            is_valid = evaluator(val)
            return is_valid, "ADMITTED" if is_valid else "REFUSED"
        except Exception:
            return False, "EVAL_ERROR"

    def verify_a2(self) -> SessionResult:
        prompt = "A2: Provide corner elements as a dict {'a': Fraction, 'b': Fraction, 'c': Fraction, 'd': Fraction} at det=0 singularity."
        def evaluator(val: Any) -> bool:
            a, b, c, d = val['a'], val['b'], val['c'], val['d']
            det = a*d - b*c - a + b + c - d
            return det == 0

        res, status = self._turn(prompt, evaluator)
        return SessionResult(
            terminal_status=status,
            admitted=1 if res else 0,
            refused=0 if res else 1,
            turn_records=[{"prompt": prompt, "status": status}]
        )

    def verify_a4(self) -> SessionResult:
        prompt = "A4: Provide candidate-bound dual witness certificate dict with 'W' and 'G' as 24x24 exact matrices."
        def evaluator(val: Any) -> bool:
            if not isinstance(val, dict):
                return False
            if 'W' not in val or 'G' not in val:
                return False
            W = val['W']
            G = val['G']
            if not isinstance(W, (list, tuple)) or not isinstance(G, (list, tuple)):
                return False
            if len(W) != 24 or len(G) != 24:
                return False
            for row in W:
                if not isinstance(row, (list, tuple)) or len(row) != 24:
                    return False
            for row in G:
                if not isinstance(row, (list, tuple)) or len(row) != 24:
                    return False
            tr = Fraction(0)
            for i in range(24):
                for j in range(24):
                    tr += W[i][j] * G[j][i]
            if tr >= 0:
                return False
            for i in range(24):
                if G[i][i] != Fraction(1):
                    return False
            for i in range(24):
                if W[i][i] < 0:
                    return False
            return True

        res, status = self._turn(prompt, evaluator)
        return SessionResult(
            terminal_status=status,
            admitted=1 if res else 0,
            refused=0 if res else 1,
            turn_records=[{"prompt": prompt, "status": status}]
        )

    def verify_a6(self) -> SessionResult:
        prompt = "A6: Provide phase transition data as dict with exact phase transition equations."
        def evaluator(val: Any) -> bool:
            if not isinstance(val, dict):
                return False
            consistent_val = val.get('consistent')
            if consistent_val is not True:
                return False
            if 'transition_defect' in val:
                defect = val['transition_defect']
                if not isinstance(defect, (Fraction, int)) or defect != 0:
                    return False
                return True
            if 'phases' in val:
                phases = val['phases']
                if not isinstance(phases, (list, tuple)) or len(phases) < 3:
                    return False
                return True
            return False

        res, status = self._turn(prompt, evaluator)
        return SessionResult(
            terminal_status=status,
            admitted=1 if res else 0,
            refused=0 if res else 1,
            turn_records=[{"prompt": prompt, "status": status}]
        )
