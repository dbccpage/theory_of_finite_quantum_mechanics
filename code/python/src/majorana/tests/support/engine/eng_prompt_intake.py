from __future__ import annotations
import json
import hashlib
import csv
import io
from typing import Optional
from omega_engine.crates.engine.base.engine_base import Engine

CONTRACT_ID = "urn:omega:engine:prompt_intake_engine:file:v1.0.0"


class PromptGeometry:
    def __init__(
        self,
        prompt_class: str = "",
        morphism_type: str = "",
        entropy: float = 0.0,
        coherence: float = 0.0,
        decidability: float = 0.0,
        hostility: float = 0.0,
        fingerprint: str = "",
    ):
        self.prompt_class = prompt_class
        self.morphism_type = morphism_type
        self.entropy = entropy
        self.coherence = coherence
        self.decidability = decidability
        self.hostility = hostility
        self.fingerprint = fingerprint

    def status(self) -> str:
        return "stubbed"


def perceive(text: str) -> PromptGeometry:
    return PromptGeometry()


class PromptRecord:
    def __init__(
        self,
        id: str,
        raw_prompt: str,
        expected_answer: Optional[str] = None,
        geometry: Optional[PromptGeometry] = None,
    ):
        self.id = id
        self.raw_prompt = raw_prompt
        self.expected_answer = expected_answer
        self.geometry = geometry or PromptGeometry()


class CotRecord:
    def __init__(
        self,
        id: str,
        obstructed_prompt: str,
        cot_steps: list,
        final_answer: str,
        geometry: Optional[PromptGeometry] = None,
    ):
        self.id = id
        self.obstructed_prompt = obstructed_prompt
        self.cot_steps = cot_steps
        self.final_answer = final_answer
        self.geometry = geometry or PromptGeometry()


def normalize_text(value: str) -> str:
    return value.strip().lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def fallback_id_for(prompt: str) -> str:
    h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    return f"prompt_{h}"


def parse_csv_fields(line: str) -> list:
    f = io.StringIO(line)
    reader = csv.reader(f)
    try:
        fields = next(reader)
        return fields
    except StopIteration:
        return []
    except csv.Error as e:
        raise ValueError(f"Invalid CSV format: {e}")


class PromptIntakeEngine(Engine):
    @staticmethod
    def parse_jsonl_record(line: str) -> PromptRecord:
        try:
            v = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        prompt_val = v.get("prompt") or v.get("question") or ""
        prompt = normalize_text(str(prompt_val))
        if not prompt:
            raise ValueError("Invalid JSONL record: empty prompt")

        id_val = v.get("id") or v.get("QuestionId") or ""
        id_str = normalize_text(str(id_val))
        if not id_str:
            id_str = fallback_id_for(prompt)

        solution_val = v.get("solution") or v.get("answer") or ""
        expected_answer: Optional[str] = normalize_text(str(solution_val))
        if not expected_answer:
            expected_answer = None

        geometry = perceive(prompt)

        return PromptRecord(
            id=id_str,
            raw_prompt=prompt,
            expected_answer=expected_answer,
            geometry=geometry,
        )

    @staticmethod
    def parse_csv_record(line: str) -> PromptRecord:
        fields = parse_csv_fields(line)
        if len(fields) < 2:
            raise ValueError("Invalid CSV format: expected at least id,prompt")

        prompt = normalize_text(fields[1])
        if not prompt:
            raise ValueError("Invalid CSV record: empty prompt")

        id_str = normalize_text(fields[0])
        if not id_str:
            id_str = fallback_id_for(prompt)

        expected_answer: Optional[str] = None
        if len(fields) > 2:
            expected_answer = normalize_text(fields[2])
            if not expected_answer:
                expected_answer = None

        geometry = perceive(prompt)

        return PromptRecord(
            id=id_str,
            raw_prompt=prompt,
            expected_answer=expected_answer,
            geometry=geometry,
        )

    @staticmethod
    def parse_cot_record(line: str) -> CotRecord:
        try:
            v = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        obstructed_prompt_val = v.get("obstructed_prompt") or v.get("prompt") or ""
        obstructed_prompt = normalize_text(str(obstructed_prompt_val))
        if not obstructed_prompt:
            raise ValueError("Invalid CoT JSONL record: empty obstructed_prompt")

        id_str = f"cot_{fallback_id_for(obstructed_prompt)}"

        cot_steps = []
        steps_val = v.get("cot_steps")
        if isinstance(steps_val, list):
            for step in steps_val:
                cleaned = normalize_text(str(step))
                if cleaned:
                    cot_steps.append(cleaned)

        final_answer_val = v.get("final_answer") or v.get("solution") or ""
        final_answer = normalize_text(str(final_answer_val))

        geometry = perceive(obstructed_prompt)

        return CotRecord(
            id=id_str,
            obstructed_prompt=obstructed_prompt,
            cot_steps=cot_steps,
            final_answer=final_answer,
            geometry=geometry,
        )

