"""M2 — DDA 8-letter tape + step receipts (Laws 1–2 enforced)."""

from __future__ import annotations
import hashlib
from typing import List, Optional

from omega_engine.crates.type.runtime_axes import DdaLetter, DdaStepReceipt


class DdaTraceEngine:
    """Records typed letters; Law 1 AuthorityEffect None; Law 2 terminal absorption."""

    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.tape: List[DdaLetter] = []
        self.receipts: List[DdaStepReceipt] = []
        self.is_terminalized = False

    def emit_step(
        self,
        letter: DdaLetter,
        input_state: str,
        output_state: str,
        carrier: str,
        diag_before: str,
        diag_after: str,
        witness: str,
        refusal_reason: Optional[str] = None,
    ) -> DdaStepReceipt:
        if self.is_terminalized:
            raise AssertionError(
                "DDA Law 2: Cannot modify trace after Terminalization (T)"
            )

        self.tape.append(letter)
        step_index = len(self.receipts) + 1
        step_id = f"DDA_STEP_{step_index:03d}"

        def h(s: str) -> str:
            return hashlib.sha256(s.encode("utf-8")).hexdigest()

        receipt = DdaStepReceipt(
            step_id=step_id,
            letter=letter,
            input_state_hash=h(input_state),
            output_state_hash=h(output_state),
            carrier_hash=h(carrier),
            diagnostic_before=diag_before,
            diagnostic_after=diag_after,
            required_witness=witness,
            witness_hash=h(witness),
            refusal_reason=refusal_reason,
            authority_effect="None",
        )
        self.receipts.append(receipt)
        if letter == DdaLetter.T:
            self.is_terminalized = True
        return receipt

    def get_tape_string(self) -> str:
        return " · ".join(l.value for l in self.tape)

    def check_law1_all_none(self) -> bool:
        return all(r.authority_effect == "None" for r in self.receipts)



