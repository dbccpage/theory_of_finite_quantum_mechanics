#!/usr/bin/env python3
"""
Collect all Symbol Game swarm transcripts into a single research folder.

Walks the Antigravity brain directory tree starting from the root coordinator
conversation and recursively gathers every subagent transcript. Copies them
into research/symbol_game_swarm_2026_09_23/transcripts_raw/ with human-
readable filenames derived from the agent role.

Usage:
    python research/symbol_game_swarm_2026_09_23/collect_transcripts.py
"""

import json
import re
import shutil
from pathlib import Path

# === Configuration ===
BRAIN_ROOT = Path(r"C:\Users\a343o\.gemini\antigravity\brain")
COORDINATOR_ID = "2545a94c-04f3-4e18-8c55-d611cc85c6a4"
OUTPUT_DIR = Path(r"C:\Users\a343o\source\repos\MUB6\research\symbol_game_swarm_2026_09_23")
TRANSCRIPTS_DIR = OUTPUT_DIR / "transcripts_raw"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def sanitize(name: str) -> str:
    """Convert a role string to a safe filename fragment."""
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()[:80]


def find_subagent_ids(transcript_path: Path) -> list[tuple[str, str]]:
    """Extract (conversationId, role) pairs from a transcript."""
    results = []
    if not transcript_path.exists():
        return results
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Look in tool_calls for invoke_subagent results
            content = entry.get("content", "")
            if "conversationId" in content:
                # Extract conversation IDs from content
                for match in re.finditer(
                    r'"conversationId"\s*:\s*"([0-9a-f-]{36})"', content
                ):
                    cid = match.group(1)
                    # Try to find role nearby
                    role_match = re.search(
                        r'"role"\s*:\s*"([^"]+)"', content
                    )
                    role = role_match.group(1) if role_match else "unknown"
                    results.append((cid, role))
            # Also check tool_calls array
            for tc in entry.get("tool_calls", []):
                args = tc.get("arguments", {})
                if isinstance(args, dict):
                    for sub in args.get("Subagents", []):
                        if isinstance(sub, dict) and "Role" in sub:
                            # The conversation ID comes from the result
                            pass
                result = tc.get("result", "")
                if isinstance(result, str) and "conversationId" in result:
                    for match in re.finditer(
                        r'"conversationId"\s*:\s*"([0-9a-f-]{36})"', result
                    ):
                        cid = match.group(1)
                        role_match = re.search(
                            r'"role"\s*:\s*"([^"]+)"', result
                        )
                        role = (
                            role_match.group(1) if role_match else "unknown"
                        )
                        results.append((cid, role))
    return results


def collect_recursive(
    conv_id: str,
    role: str,
    depth: int = 0,
    visited: set | None = None,
) -> list[dict]:
    """Recursively collect transcripts from a conversation and its subagents."""
    if visited is None:
        visited = set()
    if conv_id in visited:
        return []
    visited.add(conv_id)

    manifest = []
    conv_dir = BRAIN_ROOT / conv_id
    logs_dir = conv_dir / ".system_generated" / "logs"

    for variant in ["transcript_full.jsonl", "transcript.jsonl"]:
        src = logs_dir / variant
        if src.exists():
            safe_role = sanitize(role)
            dest_name = f"depth{depth:02d}_{safe_role}_{conv_id[:8]}_{variant}"
            dest = TRANSCRIPTS_DIR / dest_name
            shutil.copy2(src, dest)
            manifest.append(
                {
                    "conversation_id": conv_id,
                    "role": role,
                    "depth": depth,
                    "file": dest_name,
                    "size_bytes": dest.stat().st_size,
                }
            )
            print(f"  {'  ' * depth}[depth {depth}] {role} ({conv_id[:8]}) -> {dest_name}")

    # Also copy any artifacts (non-system-generated files)
    for artifact in conv_dir.glob("*.md"):
        safe_role = sanitize(role)
        dest_name = f"depth{depth:02d}_{safe_role}_{conv_id[:8]}_{artifact.name}"
        dest = TRANSCRIPTS_DIR / dest_name
        shutil.copy2(artifact, dest)

    # Find and recurse into subagents
    transcript_path = logs_dir / "transcript.jsonl"
    full_path = logs_dir / "transcript_full.jsonl"
    for path in [full_path, transcript_path]:
        for sub_id, sub_role in find_subagent_ids(path):
            manifest.extend(
                collect_recursive(sub_id, sub_role, depth + 1, visited)
            )

    return manifest


def main():
    print(f"Collecting Symbol Game swarm transcripts")
    print(f"Coordinator: {COORDINATOR_ID}")
    print(f"Output: {TRANSCRIPTS_DIR}")
    print()

    manifest = collect_recursive(COORDINATOR_ID, "Swarm_Coordinator")

    # Write manifest
    manifest_path = OUTPUT_DIR / "transcript_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "coordinator_id": COORDINATOR_ID,
                "total_transcripts": len(manifest),
                "transcripts": manifest,
            },
            f,
            indent=2,
        )

    print(f"\n{'='*60}")
    print(f"Collected {len(manifest)} transcript files")
    print(f"Manifest: {manifest_path}")
    print(f"Raw files: {TRANSCRIPTS_DIR}")


if __name__ == "__main__":
    main()
