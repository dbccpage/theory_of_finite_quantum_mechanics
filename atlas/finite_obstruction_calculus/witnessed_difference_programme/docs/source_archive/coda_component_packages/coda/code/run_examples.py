"""Replay the finite examples in coda.md, optionally recording exact JSON."""

import json
from argparse import ArgumentParser
from fractions import Fraction
from pathlib import Path

from coda_core import example_results


def exact_json(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(type(value).__name__)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(example_results(), default=exact_json, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
