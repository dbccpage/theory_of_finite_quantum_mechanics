"""Backward-compatible façade re-exporting IntakeTrace and IntakeTraceRecord."""

from __future__ import annotations

from ..type.trace.intake_trace_record import IntakeTraceRecord
from ..trace.intake_trace import IntakeTrace

__all__ = ("IntakeTrace", "IntakeTraceRecord")
