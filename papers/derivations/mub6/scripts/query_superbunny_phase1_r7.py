"""
Query Super Bunny Alpha on OpenRouter for Phase 1 Step 1.3:
Subgap R7 (ENC-1147) Singular Segre Branch Desingularization and Stengle Positivstellensatz SOS Refutation.

Firewall: stated region only; mints no authority
Model: stealth/space-bunny-alpha
"""

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return start.parents[5]


REPO_ROOT = _find_repo_root(Path(__file__).resolve())
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega_engine_operations.domain.rop.result import Err
from omega_engine_woland.infrastructure.providers.credential_source import (
    resolve_credential,
)

MUB6_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = MUB6_ROOT / "artifacts"
RESEARCH_DIR = MUB6_ROOT / "research"

ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

_found = resolve_credential(["OPENROUTER_API_KEY"], start=REPO_ROOT)
API_KEY = None if isinstance(_found, Err) else _found.value.value
if not API_KEY:
    print("ERROR: OPENROUTER_API_KEY not found by credential_source.")
    sys.exit(1)

FIREWALL = "stated region only; mints no authority"

PROMPT = f"""You are the senior real algebraic geometer and Lean 4 formal verification specialist for the MUB(6) research program.

Epistemic Firewall: '{FIREWALL}'
Zero Hype Verbs: Do NOT use 'proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence', 'impossible', 'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized'.
Always write with claim discipline: include What it supports, What it does not support, Narrowest defensible claim, Next test needed.

TASK: Phase 1 Step 1.3 - Subgap R7 (ENC-1147) Singular Segre Branch Desingularization & Positivstellensatz SOS Refutation.

BACKGROUND:
- Defining Ideal I_55: 55 polynomial equations in 50 real coordinates (x_{{ij}}, y_{{ij}} for 1 <= i,j <= 5) in K[x, y] with K = Q(sqrt(2), sqrt(3)) = Q(zeta_24 + zeta_24^{{-1}}).
  * 25 circle equations: x_{{ij}}^2 + y_{{ij}}^2 - 1 = 0
  * 15 real orthogonality equations: Re <r_j, r_k> = 0
  * 15 imag orthogonality equations: Im <r_j, r_k> = 0
- Master Case Routing: P_corner(H) = det(H_{{1..3, 1..3}}).
- Step 1.2 treats the Regular Branch P_corner(H) != 0 -> factors into Fourier F(x, y) and Karlsson K_6^(3).
- Step 1.3 treats the Singular Branch P_corner(H) == 0:
  * Along this singular locus, the Segre quadric relation (a-1)(d-1) = (b-1)(c-1) holds.
  * The certified canonical components on this locus are:
    1. The 1-parameter non-affine Szollosi family B_6(theta) (56 certified cells covering S^1, including the 3 desingularized deltoid cusps via 24 blown-up leaf cells with delta < 1/1000).
    2. The isolated Chernyavsky-Tao matrix S_6.
    3. The isolated Haagerup matrix H_6.
  * Subgap R7 requires refuting the existence of any detached real components on V_R(I_55) cap {{P_corner == 0}} outside the collar neighborhood of B_6(theta) cup {{S_6}} cup {{H_6}}.

QUESTIONS TO SOLVE:
1. Exact Separating Polynomial Formulation:
   Construct an explicit polynomial f_sep(x, y) in K[x, y] vanishing on the algebraic closure of B_6(theta) cup {{S_6}} cup {{H_6}} and satisfying f_sep(x, y) >= eps > 0 for all points at distance >= delta from this union. What degree and monomials are required?

2. Stengle / Putinar Positivstellensatz Infeasibility Certificate:
   Provide the exact rational SOS certificate structure over Q (or K):
     -1 = s_0 + sum_{{i=1}}^{{55}} h_i * f_i + sum_j s_j * g_j
   where g_j are semialgebraic boundary guards (e.g. f_sep - eps >= 0, P_corner == 0, etc.) and s_0, s_j are sums of squares.
   How does this exclude detached 0-dimensional or 1-dimensional real components that might otherwise evade degree/dimension bounds?

3. Lean 4 Formalization Blueprint for MasterClassification.lean:
   Provide the exact theorem declaration, hypothesis signatures, and proof outline in Lean 4 to prove:
   theorem singular_segre_branch_exhaustion :
     forall (H : Matrix (Fin 6) (Fin 6) Complex),
       IsCH6 H -> P_corner H = 0 ->
       (H in Orbit B6 \\/ H in Orbit S6 \\/ H in Orbit H6)
   using standard axioms [propext, Quot.sound].

4. Synthesize the 4-part Claim Hygiene summary:
   (a) What it supports
   (b) What it does not support
   (c) Narrowest defensible claim
   (d) Next test needed
"""

def query_super_bunny():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dbccpage/the_symbol_game",
        "X-Title": "MUB6 Phase 1 R7 Evaluation",
    }
    payload = {
        "model": "stealth/space-bunny-alpha",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert real algebraic geometer and Lean 4 formal prover. "
                    "Write with strict claim discipline and rigorous mathematical depth. "
                    f"Epistemic Firewall: {FIREWALL}"
                ),
            },
            {"role": "user", "content": PROMPT},
        ],
        "temperature": 0.2,
        "max_tokens": 8192,
    }

    print("Querying Super Bunny Alpha on OpenRouter for Phase 1 Step 1.3 (Subgap R7)...")
    start_time = time.time()
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            latency = time.time() - start_time
            data = json.loads(response.read().decode("utf-8"))
            print(f"Response received in {latency:.2f}s.")
            return data, latency
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
        raise
    except Exception as e:
        print(f"Error querying OpenRouter: {e}")
        raise

def main():
    data, latency = query_super_bunny()
    choices = data.get("choices", [])
    if not choices:
        print("No choices returned in API response.")
        return

    choice = choices[0]
    message = choice.get("message", {})
    content = message.get("content") or ""
    reasoning = message.get("reasoning") or ""
    usage = data.get("usage", {})

    print(f"Prompt tokens: {usage.get('prompt_tokens')}, Completion tokens: {usage.get('completion_tokens')}")
    print(f"Reasoning length: {len(reasoning)} chars, Content length: {len(content)} chars")

    receipt = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "firewall": FIREWALL,
        "phase": "Phase 1: Subgap R7 (ENC-1147) Singular Segre Exhaustion",
        "model": "stealth/space-bunny-alpha",
        "latency_sec": latency,
        "usage": usage,
        "raw_response": data,
    }
    receipt_path = ARTIFACTS_DIR / "mub_phase1_r7_superbunny_receipt.json"
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
    print(f"Receipt written to: {receipt_path}")

    md_content = f"""# MUB(6) Phase 1 Step 1.3: Singular Segre Branch (Subgap R7) Super Bunny Alpha Synthesis

**Date:** {datetime.now(timezone.utc).isoformat()}
**Model:** Super Bunny Alpha (`stealth/space-bunny-alpha`)
**Firewall Line:** `{FIREWALL}`
**Latency:** {latency:.2f}s | **Tokens:** {usage.get('total_tokens', 'N/A')}

---

## Reasoning Trace

<details><summary>Click to view internal reasoning ({len(reasoning)} chars)</summary>

```
{reasoning}
```

</details>

---

## Mathematical Formulation & Lean 4 Blueprint

{content if content else reasoning}
"""
    synthesis_path = RESEARCH_DIR / "mub_phase1_r7_superbunny_synthesis.md"
    with open(synthesis_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Synthesis report written to: {synthesis_path}")

if __name__ == "__main__":
    main()
