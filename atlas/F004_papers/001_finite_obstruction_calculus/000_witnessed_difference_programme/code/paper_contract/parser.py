"""Conservative Markdown/TeX indexing; unknown syntax is retained literally.

This is a source index, not a renderer or a mathematical semantic parser.
Repeated headings and unnumbered equations have occurrence-based local IDs.
"""
from __future__ import annotations

import bisect
import re
from collections import Counter

from .models import (
    ClaimLedger,
    ClaimOccurrence,
    ClaimRecord,
    CodeBlock,
    Equation,
    HeadingBlock,
    MarkupBlock,
    MathBlock,
    MetadataField,
    PaperDocument,
    ParseDiagnostic,
    ProseBlock,
    Section,
    SourceSpan,
    TableBlock,
    TableRow,
    TextReference,
    sha256,
)

CLAIM = re.compile(
    r"(?<![A-Za-z0-9_])(?:WDP-CH\d{2}-[A-Z]\d{2}[A-Z]?|CH\d{2}-[A-Z]\d{2}[A-Z]?"
    r"|GEN-WDP-(?:\d{2}|[A-Z]\d{2})|WDP-R\d+-[A-Z]\d{2}"
    r"|WDP-DIM-(?:\d+|R)|QPE-\d+|DP-\d+|REF-[A-Z0-9]+-\d+)"
    r"(?![A-Za-z0-9_])"
)
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*(?:\r?\n)?$")
FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})([^\r\n]*)")
NUMBER = re.compile(r"^(Appendix [A-Z]|(?:Chapter )?\d+[A-Z]?(?:\.\d+)*|[A-Z](?:\.\d+)+)(?=[\s.—:)]|\.(?:\s|$)|$)")


class Source:
    def __init__(self, raw: str):
        self.raw = raw
        self.lines = raw.splitlines(keepends=True)
        self.starts = [0]
        for match in re.finditer("\n", raw):
            self.starts.append(match.end())

    def span(self, start: int, end: int) -> SourceSpan:
        return SourceSpan(start=start, end=end, start_line=bisect.bisect_right(self.starts, start),
                          end_line=bisect.bisect_right(self.starts, max(start, end - 1)))


def escaped(raw: str, index: int) -> bool:
    count = 0
    index -= 1
    while index >= 0 and raw[index] == "\\":
        count += 1
        index -= 1
    return count % 2 == 1


def code_ranges(source: Source):
    ranges = []
    diagnostics = []
    offset = 0
    opened = None
    for line in source.lines:
        fence = FENCE.match(line)
        if opened:
            start, marker = opened
            if re.match(r"^[ \t]{0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}[ \t]*\r?\n?$", line):
                ranges.append((start, offset + len(line)))
                opened = None
        elif fence:
            opened = (offset, fence[1])
        else:
            # Inline code is masked for mathematics; claim lookup IDs remain indexed.
            for match in re.finditer(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)", line):
                ranges.append((offset + match.start(), offset + match.end()))
        offset += len(line)
    if opened:
        ranges.append((opened[0], len(source.raw)))
        diagnostics.append(ParseDiagnostic(code="unclosed_code_fence", span=source.span(opened[0], len(source.raw)),
                                           message="Unclosed fenced code; bytes retained, classification incomplete."))
    return sorted(ranges), diagnostics


def math_ranges(source: Source, masks):
    raw = source.raw
    result = []
    diagnostics = []
    tokens = re.compile(r"\$\$|\\\[|\\\(|\$(?!\$)")
    mask_index = 0
    cursor = 0
    while match := tokens.search(raw, cursor):
        start = match.start()
        while mask_index < len(masks) and masks[mask_index][1] <= start:
            mask_index += 1
        if mask_index < len(masks) and masks[mask_index][0] <= start < masks[mask_index][1]:
            cursor = masks[mask_index][1]
            continue
        opening = match[0]
        cursor = match.end()
        if escaped(raw, start) or (opening == "$" and (cursor == len(raw) or raw[cursor].isspace())):
            continue
        closing = {"$": "$", "$$": "$$", "\\[": "\\]", "\\(": "\\)"}[opening]
        stop = cursor
        while True:
            stop = raw.find(closing, stop)
            if stop < 0:
                break
            if not escaped(raw, stop) and (opening != "$" or not raw[stop - 1].isspace()):
                break
            stop += len(closing)
        if stop < 0:
            diagnostics.append(ParseDiagnostic(code="unclosed_math", span=source.span(start, match.end()),
                                               message="Unclosed math delimiter; bytes retained."))
            continue
        end = stop + len(closing)
        result.append((start, end, opening, raw[match.end():stop]))
        cursor = end
    return result, diagnostics


def table_cells(raw: str) -> tuple[str, ...]:
    """Split structural pipes, preserving pipes inside code and delimited math."""
    source = Source(raw)
    masks, _ = code_ranges(source)
    math, _ = math_ranges(source, masks)
    protected = sorted([*masks, *((a, b) for a, b, _, _ in math)])
    cuts = [i for i, char in enumerate(raw) if char == "|" and not escaped(raw, i)
            and not any(a <= i < b for a, b in protected)]
    boundaries = [-1, *cuts, len(raw)]
    cells = [raw[a + 1:b].strip() for a, b in zip(boundaries, boundaries[1:])]
    if cuts and not cells[0]:
        cells.pop(0)
    if cuts and cells and not cells[-1]:
        cells.pop()
    return tuple(cells)



def reference_index(raw: str, source: Source, fenced):
    references = []
    patterns = [("anchor", r'<a\s+id=["\']([^"\']+)["\'][^>]*>'),
                ("link", r'\[[^\]\n]*\]\(([^\n]*?)\)'),
                ("reference_definition", r'^\s{0,3}\[[^\]\n]+\]:\s*(\S+)')]
    for kind, pattern in patterns:
        for match in re.finditer(pattern, raw, re.M):
            if not any(a <= match.start() < b for a, b in fenced):
                references.append(TextReference(kind=kind, raw=match[0], target=match[1],
                                                span=source.span(match.start(), match.end())))
    return tuple(sorted(references, key=lambda r: r.span.start))


def metadata_index(raw: str, source: Source):
    return tuple(MetadataField(name=m[1], value_literal=m[2], span=source.span(m.start(), m.end()))
                 for m in re.finditer(r"^\*\*([^*\n]+):\*\* ([^\r\n]*)(?:\r?\n|$)", raw, re.M))


def literal_blocks(raw: str):
    source = Source(raw)
    masks, diagnostics = code_ranges(source)
    math, math_diagnostics = math_ranges(source, masks)
    diagnostics.extend(math_diagnostics)
    lines = source.lines
    offsets = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)
    blocks = []
    i = 0
    while i < len(lines):
        first = i
        line = lines[i]
        start = offsets[i]
        heading = HEADING.match(line)
        fence = FENCE.match(line)
        extra = {}
        cls = ProseBlock
        if heading:
            cls = HeadingBlock
            number = NUMBER.match(heading[2])
            extra = {"level": len(heading[1]), "title": heading[2], "number": number[1] if number else None}
            i += 1
        elif fence:
            cls = CodeBlock
            extra = {"language": fence[2].strip()}
            i += 1
            while i < len(lines):
                closing = re.match(r"^[ \t]{0,3}" + re.escape(fence[1][0]) + "{" + str(len(fence[1])) + r",}[ \t]*\r?\n?$", lines[i])
                i += 1
                if closing:
                    break
        elif not line.strip():
            cls = MarkupBlock
            extra = {"syntax": "whitespace"}
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
        elif line.lstrip().startswith("|"):
            cls = TableBlock
            i += 1
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                i += 1
            extra = {"rows": tuple(TableRow(span=source.span(offsets[j], offsets[j] + len(lines[j])),
                                            raw=lines[j], cells=table_cells(lines[j])) for j in range(first, i))}
        elif any(a == start + len(line) - len(line.lstrip()) and delim in {"$$", "\\["}
                 for a, _, delim, _ in math):
            cls = MathBlock
            end_math = next(b for a, b, delim, _ in math
                            if a == start + len(line) - len(line.lstrip()) and delim in {"$$", "\\["})
            i += 1
            while i < len(lines) and offsets[i] < end_math:
                i += 1
        else:
            syntax = None
            if re.match(r"^\s*(?:[-+*]|\d+[.)])\s+", line):
                syntax = "list"
            elif line.startswith(">"):
                syntax = "quote"
            elif line.startswith("<"):
                syntax = "html"
            elif re.match(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$", line):
                syntax = "rule"
            elif line.startswith(r"\begin{"):
                syntax = "latex"
            if syntax:
                cls, extra = MarkupBlock, {"syntax": syntax}
            i += 1
            while i < len(lines) and lines[i].strip() and not (
                    HEADING.match(lines[i]) or FENCE.match(lines[i]) or lines[i].lstrip().startswith(("|", "$$", r"\[", "<a "))):
                i += 1
        end = offsets[i] if i < len(lines) else len(raw)
        literal = raw[start:end]
        blocks.append(cls(id=f"block-{len(blocks) + 1:05d}", span=source.span(start, end),
                          raw=literal, sha256=sha256(literal), **extra))

    return tuple(blocks)


def parse_document(raw: str, path: str) -> PaperDocument:
    source = Source(raw)
    masks, diagnostics = code_ranges(source)
    math, math_diagnostics = math_ranges(source, masks)
    diagnostics.extend(math_diagnostics)
    blocks = literal_blocks(raw)
    sections = []
    stack = []
    names = Counter()
    owners = []
    for block in blocks:
        if isinstance(block, HeadingBlock):
            while stack and sections[stack[-1]]["level"] >= block.level:
                sections[stack.pop()]["end"] = block.span.start
            slug = re.sub(r"[^\w]+", "-", block.title.lower()).strip("-")
            parent = sections[stack[-1]]["id"] if stack else None
            key = f"{parent}/{slug}" if parent else slug
            names[key] += 1
            sid = key + (f"~{names[key]}" if names[key] > 1 else "")
            item = {"id": sid, "heading_id": block.id, "title": block.title, "number": block.number,
                    "level": block.level, "parent_id": parent, "children": [], "block_ids": [],
                    "start": block.span.start, "end": len(raw)}
            if stack:
                sections[stack[-1]]["children"].append(sid)
            sections.append(item)
            stack.append(len(sections) - 1)
        owner = sections[stack[-1]] if stack else None
        if owner:
            owner["block_ids"].append(block.id)
        owners.append((block.span.start, owner["id"] if owner else None))
    owner_starts = [a for a, _ in owners]

    def owner_at(position):
        index = bisect.bisect_right(owner_starts, position) - 1
        return owners[index][1] if index >= 0 else None

    section_models = []
    for item in sections:
        start, end = item.pop("start"), item.pop("end")
        item["children"], item["block_ids"] = tuple(item["children"]), tuple(item["block_ids"])
        section_models.append(Section(**item, span=source.span(start, end)))
    equation_counts = Counter()
    equations = []
    for start, end, delimiter, latex in math:
        owner = owner_at(start)
        equation_counts[owner] += 1
        labels = tuple(re.findall(r"\\(?:label|tag)\{([^}]+)\}", latex))
        equations.append(Equation(id=f"{owner or 'preamble'}:eq-{equation_counts[owner]:04d}",
                                  section_id=owner, span=source.span(start, end), raw=raw[start:end],
                                  latex=latex, delimiter=delimiter, display=delimiter in {"$$", "\\["}, labels=labels))
    # Identifiers in inline code ARE lookup keys in this paper. Only fenced code is excluded.
    fenced = [(b.span.start, b.span.end) for b in blocks if isinstance(b, CodeBlock)]
    claims = tuple(ClaimOccurrence(claim_id=m[0], literal=m[0], section_id=owner_at(m.start()),
                                   span=source.span(m.start(), m.end())) for m in CLAIM.finditer(raw)
                   if not any(a <= m.start() < b for a, b in fenced))
    return PaperDocument(path=path, source_sha256=sha256(raw), utf8_bytes=len(raw.encode("utf-8")),
                         characters=len(raw), blocks=tuple(blocks), sections=tuple(section_models),
                         equations=tuple(equations), claim_occurrences=claims,
                         references=reference_index(raw, source, fenced), diagnostics=tuple(diagnostics),
                         metadata_fields=metadata_index(raw, source))


def parse_ledger(raw: str, path: str) -> ClaimLedger:
    document = parse_document(raw, path)
    begin, end = "<!-- CANONICAL-CLAIM-TABLE:BEGIN -->", "<!-- CANONICAL-CLAIM-TABLE:END -->"
    if raw.count(begin) != 1 or raw.count(end) != 1:
        raise ValueError("ledger must have one canonical register delimiter pair")
    a, b = raw.index(begin) + len(begin), raw.index(end)
    if a >= b:
        raise ValueError("reversed canonical register delimiters")
    records = []
    for block in document.blocks:
        if not isinstance(block, TableBlock):
            continue
        for row in block.rows:
            cells = row.cells
            if len(cells) == 5 and a <= row.span.start < b and re.fullmatch(r"WDP-CH\d{2}-[A-Z]\d{2}", cells[0]):
                records.append(ClaimRecord(claim_id=cells[0], register_kind="canonical", status=cells[1],
                                           status_literal=cells[1], canonical_location_literal=cells[2],
                                           evidence_literal=cells[3], statement_literal=cells[4], ledger_span=row.span))
            elif len(cells) == 3 and re.fullmatch(r"WDP-R(?:12|13)-[A-Z]\d{2}", cells[0]):
                status, separator, statement = cells[1].partition(": ")
                if not separator:
                    raise ValueError("supplement status/statement delimiter missing")
                records.append(ClaimRecord(claim_id=cells[0], register_kind="preserver_generator_supplement", status=status,
                                           status_literal=status, canonical_location_literal=None,
                                           evidence_literal=cells[2], statement_literal=statement, ledger_span=row.span))
    if not any(r.register_kind == "canonical" for r in records):
        raise ValueError("empty canonical claim register")
    return ClaimLedger(document=document, records=tuple(records))
