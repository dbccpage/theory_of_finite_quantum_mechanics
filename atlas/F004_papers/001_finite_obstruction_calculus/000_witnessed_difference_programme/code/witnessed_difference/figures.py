"""Dependency-free deterministic SVG and PNG assets."""

from __future__ import annotations

import struct
import zlib
from html import escape


def flow_svg(title: str, labels: tuple[str, ...], *, width: int = 960, height: int = 220) -> str:
    if not labels:
        raise ValueError("a flow diagram needs at least one label")
    box_width = max(100, (width - 80) // len(labels) - 30)
    boxes: list[str] = []
    arrows: list[str] = []
    for index, label in enumerate(labels):
        x = 40 + index * ((width - 80) // len(labels))
        boxes.append(
            f'<rect x="{x}" y="85" width="{box_width}" height="62" rx="10" '
            f'fill="#e8f1fa" stroke="#1f4e79" stroke-width="2"/>'
            f'<text x="{x + box_width // 2}" y="120" text-anchor="middle" '
            f'font-family="sans-serif" font-size="15">{escape(label)}</text>'
        )
        if index:
            prior_x = 40 + (index - 1) * ((width - 80) // len(labels)) + box_width
            arrows.append(
                f'<path d="M {prior_x + 5} 116 L {x - 8} 116" stroke="#b04a35" '
                'stroke-width="3" marker-end="url(#arrow)"/>'
            )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{escape(title)}</title>'
        f'<desc id="desc">A left-to-right finite flow: {escape(", ".join(labels))}.</desc>'
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" '
        'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#b04a35"/></marker></defs>'
        f'<text x="{width // 2}" y="38" text-anchor="middle" font-family="sans-serif" '
        f'font-size="22" font-weight="bold">{escape(title)}</text>'
        + "".join(arrows)
        + "".join(boxes)
        + '</svg>\n'
    )


def tiny_png(width: int = 64, height: int = 64) -> bytes:
    """Create a deterministic colorblind-safe closed-loop holonomy glyph."""

    if width <= 0 or height <= 0:
        raise ValueError("PNG dimensions must be positive")
    background = (248, 249, 250)
    edge_color = (31, 78, 121)
    node_color = (230, 159, 0)
    pixels = [[background for _ in range(width)] for _ in range(height)]

    def paint(x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < width and 0 <= y < height:
            pixels[y][x] = color

    def line(start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int]) -> None:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        steps = max(abs(dx), abs(dy))
        thickness = max(1, min(width, height) // 48)
        for step in range(steps + 1):
            fraction = 0 if steps == 0 else step / steps
            x = round(start[0] + dx * fraction)
            y = round(start[1] + dy * fraction)
            for offset_x in range(-thickness, thickness + 1):
                for offset_y in range(-thickness, thickness + 1):
                    paint(x + offset_x, y + offset_y, color)

    left, right = width // 5, width - 1 - width // 5
    top, bottom = height // 5, height - 1 - height // 5
    vertices = ((left, top), (right, top), (right, bottom), (left, bottom))
    for start, end in zip(vertices, vertices[1:] + vertices[:1]):
        line(start, end, edge_color)
    radius = max(1, min(width, height) // 12)
    for center_x, center_y in vertices:
        for offset_x in range(-radius, radius + 1):
            for offset_y in range(-radius, radius + 1):
                if offset_x * offset_x + offset_y * offset_y <= radius * radius:
                    paint(center_x + offset_x, center_y + offset_y, node_color)
    arrow = max(2, min(width, height) // 12)
    midpoint = (left + right) // 2
    line((midpoint - arrow, top - arrow), (midpoint, top), node_color)
    line((midpoint - arrow, top + arrow), (midpoint, top), node_color)

    rows = bytearray()
    for row in pixels:
        rows.append(0)
        for color in row:
            rows.extend(color)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    signature = b"\x89PNG\r\n\x1a\n"
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return signature + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")


def figure_assets() -> dict[str, bytes]:
    diagrams = {
        "witness_ladder.svg": (
            "Witness, observation, and measurement ladder",
            (
                "interaction",
                "retained mark",
                "re-access",
                "attempt + result",
                "accepted E-obs",
                "measurement",
            ),
        ),
        "observer_types.svg": (
            "Distinct observer representations",
            ("quotient observer", "explicit bridge", "observer object", "typed refusal"),
        ),
        "duration_classes.svg": (
            "Finite duration classifier",
            ("cochain", "closure", "exactness", "four-way status"),
        ),
    }
    result = {name: flow_svg(title, labels).encode("utf-8") for name, (title, labels) in diagrams.items()}
    result["u1_holonomy.png"] = tiny_png()
    return result
# Executable finite evidence; AuthorityEffect: None.
