"""Reviewable fingerprints and explicit drift reports. No implicit approval."""
from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import field_validator, model_validator

from .models import (
    ContractModel,
    Digest,
    FileArtifact,
    GitOID,
    ResearchPaper,
    relative_path,
    sha256,
)


class Fingerprint(ContractModel):
    category: Literal["document", "section", "equation", "claim", "reference", "diagnostic", "metadata"]
    key: str
    sha256: Digest


class PaperBaseline(ContractModel):
    schema_version: Literal["1.0"] = "1.0"
    authority_effect: Literal["None"] = "None"
    repository: str
    paper_root: str
    source_commit: GitOID
    excluded_self_path: Literal["manifests/paper_contract.baseline.json"] = "manifests/paper_contract.baseline.json"
    directories: tuple[str, ...]
    files: tuple[FileArtifact, ...]
    fingerprints: tuple[Fingerprint, ...]
    _root = field_validator("paper_root")(relative_path)

    @model_validator(mode="after")
    def unique(self):
        paths = [f.path for f in self.files]
        if len(paths) != len(set(paths)) or self.excluded_self_path in paths:
            raise ValueError("duplicate or self-referential baseline file")
        keys = [(f.category, f.key) for f in self.fingerprints]
        if len(keys) != len(set(keys)) or len(self.directories) != len(set(self.directories)):
            raise ValueError("duplicate baseline fingerprint/directory")
        for path in self.directories:
            relative_path(path)
        return self


class Change(ContractModel):
    category: str
    key: str
    operation: Literal["added", "removed", "changed", "reordered"]
    before: str | None
    after: str | None


class AuditReport(ContractModel):
    authority_effect: Literal["None"] = "None"
    matches_baseline: bool
    changes: tuple[Change, ...]
    issues: tuple[str, ...]


def fingerprint(paper: ResearchPaper) -> PaperBaseline:
    result = []
    for doc in (paper.manuscript, paper.claim_ledger.document):
        result.append(Fingerprint(category="document", key=doc.path, sha256=doc.source_sha256))
        raw = doc.literal()
        for section in doc.sections:
            result.append(Fingerprint(category="section", key=f"{doc.path}#{section.id}",
                                      sha256=sha256(raw[section.span.start:section.span.end])))
        for eq in doc.equations:
            result.append(Fingerprint(category="equation", key=f"{doc.path}#{eq.id}", sha256=sha256(eq.raw)))
        # Preserve occurrence order and targets including duplicate anchors and links.
        for index, ref in enumerate(doc.references):
            result.append(Fingerprint(category="reference", key=f"{doc.path}:reference-{index:04d}", sha256=sha256(ref.raw)))
        for index, metadata in enumerate(doc.metadata_fields):
            result.append(Fingerprint(category="metadata", key=f"{doc.path}:metadata-{index:04d}",
                                      sha256=sha256(metadata.model_dump_json())))
        for index, diagnostic in enumerate(doc.diagnostics):
            result.append(Fingerprint(category="diagnostic", key=f"{doc.path}:diagnostic-{index:04d}",
                                      sha256=sha256(diagnostic.model_dump_json())))
    for record in paper.claim_ledger.records:
        # Exclude source offsets so moving a row doesn't pretend its statement changed.
        result.append(Fingerprint(category="claim", key=record.claim_id,
                                  sha256=sha256(record.model_dump_json(exclude={"ledger_span"})) ))
    folders = paper.folders()
    return PaperBaseline(repository=paper.provenance.repository, paper_root=paper.provenance.paper_root,
                         source_commit=paper.provenance.commit, directories=tuple(sorted(
                             p for f in folders for p in (f.path, *f.directories))),
                         files=paper.artifacts(), fingerprints=tuple(result))


def integrity_issues(paper: ResearchPaper) -> tuple[str, ...]:
    issues = []
    for doc in (paper.manuscript, paper.claim_ledger.document):
        issues.extend(f"{doc.path}:{d.span.start_line}: {d.code}: {d.message}" for d in doc.diagnostics)
    known = {c.claim_id for c in paper.manuscript.claim_occurrences}
    references = {r.target for r in paper.manuscript.references if r.kind == "anchor"}
    for record in paper.claim_ledger.records:
        if record.claim_id not in known:
            issues.append(f"ledger claim absent from manuscript: {record.claim_id}")
        if record.canonical_location_literal:
            import re
            for anchor in re.findall(r"\]\([^)]*#([^)]*)\)", record.canonical_location_literal):
                if anchor not in references:
                    issues.append(f"ledger claim anchor absent from manuscript: {record.claim_id} -> {anchor}")
    # Evidence status is copied from the ledger; the ID suffix supplies no status.
    return tuple(issues)


def compare(baseline: PaperBaseline, paper: ResearchPaper) -> AuditReport:
    candidate = fingerprint(paper)
    changes = []
    for category, before, after in (
        ("file", {f.path: f.model_dump_json() for f in baseline.files}, {f.path: f.model_dump_json() for f in candidate.files}),
        ("directory", {p: p for p in baseline.directories}, {p: p for p in candidate.directories}),
        ("content", {(f.category, f.key): f.sha256 for f in baseline.fingerprints},
         {(f.category, f.key): f.sha256 for f in candidate.fingerprints}),
    ):
        for key in sorted(before.keys() | after.keys()):
            a, b = before.get(key), after.get(key)
            if a != b:
                changes.append(Change(category=key[0] if isinstance(key, tuple) else category,
                                      key=key[1] if isinstance(key, tuple) else key,
                                      operation="added" if a is None else "removed" if b is None else "changed",
                                      before=a, after=b))
    old_order = [(f.category, f.key) for f in baseline.fingerprints]
    new_order = [(f.category, f.key) for f in candidate.fingerprints]
    if old_order != new_order and Counter(old_order) == Counter(new_order):
        changes.append(Change(category="index", key="source_order", operation="reordered", before=None, after=None))
    issues = list(integrity_issues(paper))
    if (baseline.repository, baseline.paper_root) != (candidate.repository, candidate.paper_root):
        issues.append("baseline belongs to a different repository/paper")
    return AuditReport(matches_baseline=not changes and not issues, changes=tuple(changes), issues=tuple(issues))
