"""Literal, inspectable contracts. Validation confers no research authority."""
from __future__ import annotations

import hashlib
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

Digest = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
GitOID = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{40}$")]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def relative_path(value: str) -> str:
    if (not value or value.startswith("/") or "\\" in value or ":" in value
            or any(p in {"", ".", ".."} for p in value.split("/"))):
        raise ValueError("expected a normalized relative POSIX path")
    return value


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class SourceSpan(ContractModel):
    """Half-open Unicode character offsets; line numbers are one-based."""
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)

    @model_validator(mode="after")
    def ordered(self):
        if self.end < self.start or self.end_line < self.start_line:
            raise ValueError("reversed source span")
        return self


class LiteralBlock(ContractModel):
    id: str
    span: SourceSpan
    raw: str
    sha256: Digest

    @model_validator(mode="after")
    def exact(self):
        if self.span.end - self.span.start != len(self.raw) or sha256(self.raw) != self.sha256:
            raise ValueError("literal length/hash mismatch")
        return self


class HeadingBlock(LiteralBlock):
    kind: Literal["heading"] = "heading"
    level: int = Field(ge=1, le=6)
    title: str
    number: str | None = None


class ProseBlock(LiteralBlock):
    kind: Literal["prose"] = "prose"


class MathBlock(LiteralBlock):
    kind: Literal["math"] = "math"


class CodeBlock(LiteralBlock):
    kind: Literal["code"] = "code"
    language: str


class TableRow(ContractModel):
    span: SourceSpan
    raw: str
    cells: tuple[str, ...]


class TableBlock(LiteralBlock):
    kind: Literal["table"] = "table"
    rows: tuple[TableRow, ...]


class MarkupBlock(LiteralBlock):
    kind: Literal["markup"] = "markup"
    syntax: Literal["whitespace", "list", "quote", "html", "rule", "latex"]


Block = Annotated[
    HeadingBlock | ProseBlock | MathBlock | CodeBlock | TableBlock | MarkupBlock,
    Field(discriminator="kind"),
]


class Section(ContractModel):
    id: str
    heading_id: str
    title: str
    number: str | None
    level: int = Field(ge=1, le=6)
    parent_id: str | None
    children: tuple[str, ...]
    block_ids: tuple[str, ...]
    span: SourceSpan


class Equation(ContractModel):
    id: str
    section_id: str | None
    span: SourceSpan
    raw: str
    latex: str
    delimiter: Literal["$", "$$", "\\(", "\\["]
    display: bool
    labels: tuple[str, ...] = ()


class ClaimOccurrence(ContractModel):
    """An occurrence is not a declaration or evidence of its current status."""
    claim_id: str
    section_id: str | None
    span: SourceSpan
    literal: str


class TextReference(ContractModel):
    kind: Literal["anchor", "link", "reference_definition"]
    span: SourceSpan
    raw: str
    target: str


class ParseDiagnostic(ContractModel):
    code: str
    span: SourceSpan
    message: str


class MetadataField(ContractModel):
    name: str
    value_literal: str
    span: SourceSpan


class PaperDocument(ContractModel):
    path: str
    source_sha256: Digest
    utf8_bytes: int = Field(ge=0)
    characters: int = Field(ge=0)
    blocks: tuple[Block, ...]
    sections: tuple[Section, ...]
    equations: tuple[Equation, ...]
    claim_occurrences: tuple[ClaimOccurrence, ...]
    references: tuple[TextReference, ...]
    metadata_fields: tuple[MetadataField, ...] = ()
    diagnostics: tuple[ParseDiagnostic, ...] = ()

    _path = field_validator("path")(relative_path)

    def literal(self) -> str:
        return "".join(block.raw for block in self.blocks)

    @model_validator(mode="after")
    def lossless(self):
        raw = self.literal()
        if (len(raw) != self.characters or len(raw.encode("utf-8")) != self.utf8_bytes
                or sha256(raw) != self.source_sha256):
            raise ValueError("document length/hash mismatch")
        from .parser import literal_blocks
        if self.blocks != literal_blocks(raw):
            raise ValueError("literal block classification is incomplete or altered")
        ids = [block.id for block in self.blocks]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate block ID")
        cursor = 0
        for block in self.blocks:
            if block.span.start != cursor:
                raise ValueError("blocks must partition the entire source without gaps/overlaps")
            self._check_span(raw, block.span, block.raw)
            cursor = block.span.end
            if isinstance(block, HeadingBlock):
                import re
                match = re.match(r"^(#{1,6})[ \t]+(.+?)[ \t]*(?:\r?\n)?$", block.raw)
                if not match or len(match[1]) != block.level or match[2] != block.title:
                    raise ValueError("heading metadata disagrees with literal heading")
            if isinstance(block, TableBlock):
                from .parser import table_cells
                if "".join(row.raw for row in block.rows) != block.raw:
                    raise ValueError("table rows must preserve all table bytes")
                row_cursor = block.span.start
                for row in block.rows:
                    if row.span.start != row_cursor:
                        raise ValueError("non-contiguous table rows")
                    self._check_span(raw, row.span, row.raw)
                    if row.cells != table_cells(row.raw):
                        raise ValueError("table cells disagree with literal row")
                    row_cursor = row.span.end
        sections = {s.id: s for s in self.sections}
        if len(sections) != len(self.sections):
            raise ValueError("duplicate section ID")
        heading_ids = {b.id for b in self.blocks if isinstance(b, HeadingBlock)}
        if {s.heading_id for s in self.sections} != heading_ids:
            raise ValueError("every heading needs exactly one section")
        if len(self.sections) != len(heading_ids):
            raise ValueError("section/heading census mismatch")
        for section in self.sections:
            self._check_span(raw, section.span)
            heading = self.blocks[ids.index(section.heading_id)]
            if (section.title, section.level, section.number, section.span.start) != (
                    heading.title, heading.level, heading.number, heading.span.start):
                raise ValueError("section metadata disagrees with its heading")
            if section.parent_id is not None:
                parent = sections.get(section.parent_id)
                if (parent is None or parent.level >= section.level
                        or section.id not in parent.children
                        or not parent.span.start <= section.span.start < section.span.end <= parent.span.end):
                    raise ValueError("invalid section ancestry")
            if any(c not in sections or sections[c].parent_id != section.id for c in section.children):
                raise ValueError("invalid section children")
            if any(b not in ids for b in section.block_ids):
                raise ValueError("unknown section block")
        heading_to_section = {s.heading_id: s for s in self.sections}
        literal_headings = [b for b in self.blocks if isinstance(b, HeadingBlock)]
        if [s.heading_id for s in self.sections] != [b.id for b in literal_headings]:
            raise ValueError("section source order mismatch")
        owner = None
        expected_blocks = {s.id: [] for s in self.sections}
        ownership = []
        for block in self.blocks:
            if isinstance(block, HeadingBlock):
                owner = heading_to_section[block.id].id
            ownership.append((block.span.start, owner))
            if owner:
                expected_blocks[owner].append(block.id)
        for index, section in enumerate(self.sections):
            if tuple(expected_blocks[section.id]) != section.block_ids:
                raise ValueError("section block membership/order mismatch")
            end = next((s.span.start for s in self.sections[index + 1:] if s.level <= section.level), len(raw))
            if section.span.end != end:
                raise ValueError("section extent does not match literal heading hierarchy")
        import bisect
        starts = [p for p, _ in ownership]
        for obj in (*self.equations, *self.claim_occurrences):
            self._check_span(raw, obj.span, obj.raw if isinstance(obj, Equation) else obj.literal)
            if obj.section_id is not None and obj.section_id not in sections:
                raise ValueError("unknown index section")
            index = bisect.bisect_right(starts, obj.span.start) - 1
            if obj.section_id != (ownership[index][1] if index >= 0 else None):
                raise ValueError("index entry bound to the wrong section")
        for equation in self.equations:
            closing = {"$": "$", "$$": "$$", "\\(": "\\)", "\\[": "\\]"}[equation.delimiter]
            if (equation.raw != equation.delimiter + equation.latex + closing
                    or equation.display != (equation.delimiter in {"$$", "\\["})):
                raise ValueError("equation metadata disagrees with literal equation")
            import re
            if equation.labels != tuple(re.findall(r"\\(?:label|tag)\{([^}]+)\}", equation.latex)):
                raise ValueError("equation label metadata mismatch")
        for reference in self.references:
            self._check_span(raw, reference.span, reference.raw)
        for diagnostic in self.diagnostics:
            self._check_span(raw, diagnostic.span)
        for metadata in self.metadata_fields:
            self._check_span(raw, metadata.span)
            if raw[metadata.span.start:metadata.span.end].rstrip("\r\n") != f"**{metadata.name}:** {metadata.value_literal}":
                raise ValueError("metadata disagrees with literal source")
        # Verify the complete lexical census, not only the supplied index entries.
        from .parser import CLAIM, Source, code_ranges, math_ranges, metadata_index, reference_index
        masks, code_diagnostics = code_ranges(Source(raw))
        equations, math_diagnostics = math_ranges(Source(raw), masks)
        if [(a, b, d, latex) for a, b, d, latex in equations] != [
                (e.span.start, e.span.end, e.delimiter, e.latex) for e in self.equations]:
            raise ValueError("equation index is incomplete or reordered")
        if tuple((*code_diagnostics, *math_diagnostics)) != self.diagnostics:
            raise ValueError("parse diagnostic census mismatch")
        fenced = [(b.span.start, b.span.end) for b in self.blocks if isinstance(b, CodeBlock)]
        if reference_index(raw, Source(raw), fenced) != self.references:
            raise ValueError("reference index is incomplete or altered")
        if metadata_index(raw, Source(raw)) != self.metadata_fields:
            raise ValueError("metadata index is incomplete or altered")
        stack = []
        children = {section.id: [] for section in self.sections}
        for section in self.sections:
            while stack and stack[-1].level >= section.level:
                stack.pop()
            parent_id = stack[-1].id if stack else None
            if section.parent_id != parent_id:
                raise ValueError("section parent differs from literal heading hierarchy")
            if parent_id is not None:
                children[parent_id].append(section.id)
            stack.append(section)
        if any(section.children != tuple(children[section.id]) for section in self.sections):
            raise ValueError("section children/order differ from literal heading hierarchy")
        expected_claims = [(m[0], m.start(), m.end()) for m in CLAIM.finditer(raw)
                           if not any(a <= m.start() < b for a, b in fenced)]
        if expected_claims != [(c.literal, c.span.start, c.span.end) for c in self.claim_occurrences]:
            raise ValueError("claim occurrence index is incomplete or reordered")
        for claim in self.claim_occurrences:
            if claim.claim_id != claim.literal:
                raise ValueError("claim identifier is not its literal occurrence")
        return self

    @staticmethod
    def _check_span(raw: str, span: SourceSpan, literal: str | None = None):
        if span.end > len(raw) or (literal is not None and raw[span.start:span.end] != literal):
            raise ValueError("source slice mismatch")
        first = raw.count("\n", 0, span.start) + 1
        last = raw.count("\n", 0, max(span.start, span.end - 1)) + 1
        if (first, last) != (span.start_line, span.end_line):
            raise ValueError("line/character span mismatch")


ClaimStatus = Literal[
    "DEFINITION", "FINITE_PROPOSITION", "TYPING_PROPOSITION", "CONDITIONAL_RESULT",
    "CITED_RESULT", "MECHANIZED_ELSEWHERE", "OPEN_CLAIM", "OPEN_INTERFACE", "CONJECTURE",
    "REFUTED_DRAFT", "INTERPRETIVE_PROPOSAL", "NONCLAIM", "SYNTHESIS_CONCLUSION",
]


class ClaimRecord(ContractModel):
    claim_id: str
    register_kind: Literal["canonical", "preserver_generator_supplement"]
    status: ClaimStatus
    status_literal: str
    statement_literal: str
    canonical_location_literal: str | None
    evidence_literal: str
    ledger_span: SourceSpan


class ClaimLedger(ContractModel):
    document: PaperDocument
    records: tuple[ClaimRecord, ...]

    @model_validator(mode="after")
    def records_bound(self):
        ids = [r.claim_id for r in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate authoritative claim row")
        raw = self.document.literal()
        for record in self.records:
            PaperDocument._check_span(raw, record.ledger_span)
            if record.claim_id not in raw[record.ledger_span.start:record.ledger_span.end]:
                raise ValueError("claim record not bound to ledger row")
            from .parser import table_cells
            cells = table_cells(raw[record.ledger_span.start:record.ledger_span.end])
            if record.register_kind == "canonical":
                expected = (record.claim_id, record.status_literal, record.canonical_location_literal,
                            record.evidence_literal, record.statement_literal)
            else:
                expected = (record.claim_id, record.status_literal + ": " + record.statement_literal,
                            record.evidence_literal)
            if cells != expected or record.status != record.status_literal:
                raise ValueError("claim status/statement/evidence metadata disagrees with literal ledger row")
        import re
        begin, end = "<!-- CANONICAL-CLAIM-TABLE:BEGIN -->", "<!-- CANONICAL-CLAIM-TABLE:END -->"
        if raw.count(begin) != 1 or raw.count(end) != 1 or raw.index(begin) >= raw.index(end):
            raise ValueError("invalid canonical claim-register delimiters")
        expected_ids = []
        for block in self.document.blocks:
            if isinstance(block, TableBlock):
                for row in block.rows:
                    if (row.cells and len(row.cells) == 5 and raw.index(begin) < row.span.start < raw.index(end)
                            and re.fullmatch(r"WDP-CH\d{2}-[A-Z]\d{2}", row.cells[0])):
                        expected_ids.append(row.cells[0])
                    elif row.cells and len(row.cells) == 3 and re.fullmatch(r"WDP-R(?:12|13)-[A-Z]\d{2}", row.cells[0]):
                        expected_ids.append(row.cells[0])
        if [r.claim_id for r in self.records] != expected_ids:
            raise ValueError("authoritative claim-row census/order mismatch")
        return self


class ClaimCodeBinding(ContractModel):
    claim_id: str
    status: ClaimStatus
    module: str
    tests: tuple[str, ...]
    evidence_type: str
    _module = field_validator("module")(relative_path)


class ClaimCodeMap(ContractModel):
    """Exact JSON source and typed executable bindings; no inferred proof credit."""
    path: Literal["manifests/claim_code_map.json"] = "manifests/claim_code_map.json"
    raw: str
    authority_effect: Literal["None"] = "None"
    scope: str
    claims: tuple[ClaimCodeBinding, ...]

    @model_validator(mode="after")
    def literal_binding(self):
        import json
        payload = json.loads(self.raw)
        if payload != self.model_dump(mode="json", exclude={"path", "raw"}):
            raise ValueError("claim-code bindings disagree with literal JSON")
        ids = [c.claim_id for c in self.claims]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate claim-code binding")
        for claim in self.claims:
            for path in claim.tests:
                relative_path(path)
        return self


class FileArtifact(ContractModel):
    path: str
    git_blob_sha: GitOID
    bytes: int = Field(ge=0)
    mode: Literal["100644", "100755"] = "100644"
    _path = field_validator("path")(relative_path)


class Folder(ContractModel):
    """Exact recursive inventory; directories include paths relative to paper root."""
    path: str
    directories: tuple[str, ...]
    files: tuple[FileArtifact, ...]
    _path = field_validator("path")(relative_path)

    @model_validator(mode="after")
    def contained(self):
        all_paths = [self.path, *self.directories, *(f.path for f in self.files)]
        if len(all_paths) != len(set(all_paths)):
            raise ValueError("duplicate inventory path")
        directories = {self.path, *self.directories}
        for path in all_paths[1:]:
            relative_path(path)
            if not path.startswith(self.path + "/") or path.rpartition("/")[0] not in directories:
                raise ValueError("folder inventory escapes its root or omits a parent")
        return self


class TestsFolder(Folder):
    path: Literal["code/tests"] = "code/tests"


class CodeFolder(Folder):
    path: Literal["code"] = "code"
    tests: TestsFolder

    @model_validator(mode="after")
    def tests_bound(self):
        if "code/tests" not in self.directories:
            raise ValueError("code/tests is required")
        if (tuple(f for f in self.files if f.path.startswith("code/tests/")) != self.tests.files
                or tuple(d for d in self.directories if d.startswith("code/tests/")) != self.tests.directories):
            raise ValueError("code.tests inventory differs from code inventory")
        return self


class DocsFolder(Folder):
    path: Literal["docs"] = "docs"


class EvidenceFolder(Folder):
    path: Literal["evidence"] = "evidence"


class JupyterNotebooksFolder(Folder):
    path: Literal["jupyter_notebooks"] = "jupyter_notebooks"


class Lean4Folder(Folder):
    path: Literal["lean4"] = "lean4"


class ScriptsFolder(Folder):
    path: Literal["scripts"] = "scripts"


class ImagesFolder(Folder):
    path: Literal["images"] = "images"


class ManifestsFolder(Folder):
    path: Literal["manifests"] = "manifests"


class Provenance(ContractModel):
    repository: str
    commit: GitOID
    paper_root: str
    inventory_source: Literal["github_git_tree", "git_worktree"]
    _root = field_validator("paper_root")(relative_path)


class ResearchPaper(ContractModel):
    schema_version: Literal["1.0"] = "1.0"
    authority_effect: Literal["None"] = "None"
    provenance: Provenance
    manuscript: PaperDocument
    claim_ledger: ClaimLedger
    claim_code_map: ClaimCodeMap | None = None
    code: CodeFolder
    docs: DocsFolder
    lean4: Lean4Folder
    scripts: ScriptsFolder
    evidence: EvidenceFolder | None = None
    jupyter_notebooks: JupyterNotebooksFolder | None = None
    images: ImagesFolder | None = None
    manifests: ManifestsFolder | None = None
    additional_folders: tuple[Folder, ...] = ()
    root_files: tuple[FileArtifact, ...]

    def artifacts(self) -> tuple[FileArtifact, ...]:
        folders = self.folders()
        return tuple(sorted((*self.root_files, *(f for d in folders for f in d.files)), key=lambda f: f.path))

    def folders(self) -> tuple[Folder, ...]:
        named = (self.code, self.docs, self.lean4, self.scripts, self.evidence,
                 self.jupyter_notebooks, self.images, self.manifests)
        return (*tuple(f for f in named if f is not None), *self.additional_folders)

    @model_validator(mode="after")
    def bound(self):
        paths = [f.path for f in self.artifacts()]
        if len(paths) != len(set(paths)) or any("/" in f.path for f in self.root_files):
            raise ValueError("overlapping/root file inventory")
        folder_paths = [f.path for f in self.folders()]
        if len(folder_paths) != len(set(folder_paths)) or any("/" in p for p in folder_paths):
            raise ValueError("duplicate or nested top-level folder")
        for document in (self.manuscript, self.claim_ledger.document):
            artifact = next((f for f in self.artifacts() if f.path == document.path), None)
            data = document.literal().encode("utf-8")
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if artifact is None or artifact.bytes != len(data) or artifact.git_blob_sha != digest:
                raise ValueError("document does not match its inventoried Git blob")
        if self.claim_code_map:
            mapping = self.claim_code_map
            data = mapping.raw.encode("utf-8")
            artifact = next((f for f in self.artifacts() if f.path == mapping.path), None)
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if artifact is None or artifact.git_blob_sha != digest or artifact.bytes != len(data):
                raise ValueError("claim-code map does not match inventoried Git blob")
            statuses = {r.claim_id: r.status for r in self.claim_ledger.records if r.register_kind == "canonical"}
            for binding in mapping.claims:
                if statuses.get(binding.claim_id) != binding.status:
                    raise ValueError("claim-code status disagrees with canonical ledger")
                if any(p not in paths for p in (binding.module, *binding.tests)):
                    raise ValueError("claim-code binding points to missing module/tests")
        return self
