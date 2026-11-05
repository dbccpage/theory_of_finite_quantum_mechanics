"""Execute Prompt 1 (G4) via SakanaOpenRouterAdapter and record response and receipts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load launching process environment explicitly
load_dotenv()

REPO_ROOT = str(Path(__file__).resolve().parents[1])
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_engine_woland.infrastructure.providers.adapters import get_backend  # noqa: E402


def main() -> int:
    prompt_path = Path("omega_engine_library/prompts/g4_prompt.md")
    if not prompt_path.is_file():
        prompt_path = Path("g4_prompt.md")

    prompt_text = prompt_path.read_text(encoding="utf-8")

    print(f"Reading prompt from {prompt_path} ({len(prompt_text)} characters)...")
    print("Initializing backend: get_backend('sakana')...")

    backend = get_backend("sakana", timeout=1200.0, max_tokens=None)
    print(f"Backend name: {backend.name}")
    print(f"Model: {getattr(backend, 'model', 'unknown')}")
    print(f"Max tokens: {getattr(backend, 'max_tokens', 'unlimited (native provider max)')}")
    print("Dispatching request to OpenRouter...")

    # We call complete_with_receipt to capture full token and cost information
    try:
        receipt = backend.complete_with_receipt(prompt_text)
    except Exception as exc:
        print(f"Error during completion: {exc}", file=sys.stderr)
        return 1

    print("Completion received!")
    print(f"Generation ID: {receipt.generation_id}")
    print(f"Prompt Tokens: {receipt.prompt_tokens}")
    print(f"Completion Tokens: {receipt.completion_tokens}")
    print(f"Total Tokens: {receipt.total_tokens}")
    print(f"Cost USD: {receipt.cost_usd}")
    print(f"Latency: {receipt.latency_ms:.2f} ms")

    # Write response to runs/ and workspace root
    out_dir = Path("runs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "g4_sakana_fugu_ultra_v2_response.md"
    out_file.write_text(receipt.content, encoding="utf-8")
    print(f"Response written to: {out_file}")

    root_out = Path("g4_sakana_fugu_ultra_v2_response.md")
    root_out.write_text(receipt.content, encoding="utf-8")
    print(f"Response written to: {root_out}")

    receipt_file = out_dir / "g4_sakana_fugu_ultra_v2_receipt.json"
    receipt_data = {
        "model": receipt.model,
        "generation_id": receipt.generation_id,
        "prompt_tokens": receipt.prompt_tokens,
        "completion_tokens": receipt.completion_tokens,
        "total_tokens": receipt.total_tokens,
        "cost_usd": receipt.cost_usd,
        "latency_ms": round(receipt.latency_ms, 2),
        "raw_usage": receipt.raw_usage,
    }
    receipt_file.write_text(json.dumps(receipt_data, indent=2), encoding="utf-8")
    print(f"Receipt written to: {receipt_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
