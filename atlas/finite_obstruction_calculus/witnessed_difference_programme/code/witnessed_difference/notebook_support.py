"""Deterministic display helpers shared by the educational notebooks.

The committed notebooks are output-free.  In an ordinary interactive kernel,
``slider_html`` returns a dependency-free HTML range control.  The replay gate
sets :data:`STATIC_WIDGET_ENV` so the very same cell emits a deterministic
``<pre>`` fallback instead.  This keeps automated receipts independent of a
browser's JavaScript runtime without pretending that the static receipt is an
interactive test.
"""

from __future__ import annotations

import json
import os
from hashlib import sha256
from html import escape
from typing import Any

from .exact import canonical_data

STATIC_WIDGET_ENV = "WDP_NOTEBOOK_STATIC"


def static_slider(label: str, minimum: int, maximum: int, value: int) -> dict[str, object]:
    if not label or minimum > maximum or not minimum <= value <= maximum:
        raise ValueError("static slider needs a label and an in-range value")
    return {
        "control": "static_slider_fallback",
        "label": label,
        "maximum": maximum,
        "minimum": minimum,
        "value": value,
    }


def slider_html(
    label: str,
    minimum: int,
    maximum: int,
    value: int,
    *,
    static: bool | None = None,
) -> str:
    """Return a real HTML slider or the deterministic replay fallback.

    ``static=None`` delegates the choice to :data:`STATIC_WIDGET_ENV`.  The
    interactive branch has no third-party widget dependency: a small inline
    script updates the adjacent ``output`` element.  Both branches include the
    same canonical fallback payload and stable element identifier.
    """

    fallback = static_slider(label, minimum, maximum, value)
    if static is None:
        static = os.environ.get(STATIC_WIDGET_ENV) == "1"
    payload = json.dumps(fallback, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    escaped_payload = escape(payload)
    if static:
        return (
            '<pre class="wdp-slider-fallback" data-widget-mode="static">'
            f"{escaped_payload}</pre>"
        )
    identifier = "wdp-slider-" + sha256(payload.encode("utf-8")).hexdigest()[:12]
    safe_label = escape(label)
    return (
        f'<div id="{identifier}" class="wdp-slider" data-widget-mode="interactive">'
        f'<label for="{identifier}-input">{safe_label}: '
        f'<output id="{identifier}-output">{value}</output></label> '
        f'<input id="{identifier}-input" type="range" min="{minimum}" '
        f'max="{maximum}" value="{value}" step="1" '
        f'aria-label="{safe_label}">'
        "<script>(()=>{const root=document.getElementById('"
        + identifier
        + "');const input=root.querySelector('input');const output=root.querySelector('output');"
        "input.addEventListener('input',()=>{output.value=input.value;output.textContent=input.value;});"
        "})();</script>"
        f"<noscript><pre>{escaped_payload}</pre></noscript></div>"
    )


def display_json(value: Any) -> str:
    return json.dumps(canonical_data(value), indent=2, sort_keys=True)
# Executable finite evidence; AuthorityEffect: None.
