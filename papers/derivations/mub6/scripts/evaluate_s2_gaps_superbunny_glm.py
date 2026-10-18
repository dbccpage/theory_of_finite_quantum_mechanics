"""Evaluation script for the 5 Gaps in mub6_gap_registry.json (S2: G1-G5).

Evaluates Super Bunny Alpha (stealth/space-bunny-alpha) and GLM 5.3 (z-ai/glm-5.3) via OpenRouter.
Enforces Claim Hygiene, Epistemic Firewall:
stated region only; mints no authority.
"""

import concurrent.futures
import json
import os
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
MUB6_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = MUB6_ROOT / "artifacts"
RESEARCH_DIR = MUB6_ROOT / "research"

MODELS = [
    {
        "id": "stealth/space-bunny-alpha",
        "name": "Super Bunny Alpha",
        "tier": "Stealth Frontier Reasoning",
    },
    {
        "id": "z-ai/glm-5.3",
        "name": "GLM 5.3",
        "tier": "GLM Frontier Reasoning",
    },
]

FIREWALL = "stated region only; mints no authority"

GAP_PROMPTS = {
    "G1": {
        "title": "Gap G1: Full Moduli Classification & Subgap R7 (ENC-1147) Exhaustion",
        "context": (
            "In MUB(6) moduli classification, Subgap R6 (sporadic literature CHM classes) "
            "and Subgap R7 (ENC-1147: full 6x6 Complex Hadamard Matrix variety exhaustion on I_55) "
            "are open residuals. The ideal I_55 consists of 55 polynomials in 50 real variables defining "
            "6x6 unitary matrices with unimodular entries."
        ),
        "prompt": (
            "Provide the exact algebraic geometry / Positivstellensatz formulation to discharge Subgap R7 for the 55-polynomial "
            "ideal I_55 subset R[x_1, ..., y_25]. Specifically:\n"
            "1. How can algebraic degree and dimension bounds on the coordinate ring R[X]/I_55 rigorously exclude detached real "
            "components on Sper(R[X]/I_55) outside the 5 literature families (F(x,y), B_6(theta), K_6^(3), S_6, H_6)?\n"
            "2. What exact Stengle/Putinar Positivstellensatz refutation certificate structure can be computed over Q or Q(zeta_24) "
            "to certify that any real solution satisfying I_55 = 0 must belong to the algebraic closure of one of the 5 canonical charts?\n"
            "3. State the narrowest defensible claim and the exact next computational test needed, respecting the strict firewall: "
            f"'{FIREWALL}'."
        ),
    },
    "G2": {
        "title": "Gap G2: Candidate Representation Bridge Unconditional Discharge",
        "context": (
            "Gap G2 is currently DISCHARGED_CONDITIONAL on G1. It is mechanized in "
            "TargetA7ZeroRelVariety.lean (CurvatureWallCertifiedAtlas), establishing that every candidate quadruple built from "
            "the declared catalog representatives exhibits a certified curvature wall obstruction Psi^2 > 0."
        ),
        "prompt": (
            "Explain how the Candidate Representation Bridge becomes unconditional once G1/R7 is discharged:\n"
            "1. Detail the exact quotient map from the affine variety V(I_55) to the dephased orbit space "
            "M_6 = V(I_55) / (T^5 x T^5 rtimes S_6 x S_6).\n"
            "2. How is positive semi-definiteness (PSD) of the Gramian block matrices and dual SDP witness matrices W = L D L^dag "
            "preserved under continuous gauge transport along each Hadamard orbit?\n"
            "3. What explicit theorem specification in Lean 4 connects the real spectrum gluing of G1 directly to "
            "TargetA7ZeroRelVariety.lean without circular dependencies, respecting the firewall: "
            f"'{FIREWALL}'?"
        ),
    },
    "G3": {
        "title": "Gap G3: Analytic Variation Enclosures Global Certification",
        "context": (
            "Gap G3 is PARTIAL. Scoped Targets B1-B3 cover stated continuous curves and cells but do not "
            "certify parameter variation across all 6x6 CHM moduli. Endpoint margin interpolation does not bound "
            "matrix derivatives or curvature walls along general families."
        ),
        "prompt": (
            "Explain how the analytic parameter variation enclosure is unified globally across Sper(R[X]/I_55):\n"
            "1. Explain how to bound matrix derivatives and curvature walls along continuous deformation trajectories "
            "beyond convex combination of endpoint margins.\n"
            "2. Formulate the uniform Lipschitz continuity bound L = 85/9 and its interaction with the certified bisection mesh step "
            "delta = 1/1000 to ensure strict gap propagation epsilon - L*delta > 0.\n"
            "3. State the narrowest defensible claim regarding global enclosure over the certified charts, respecting: "
            f"'{FIREWALL}'."
        ),
    },
    "G4": {
        "title": "Gap G4: Genuine Simplicial 1-Cochains Topological Invariance",
        "context": (
            "Gap G4 is DISCHARGED_CONDITIONAL on G1. Cycle circulation Phi_1 >= Gamma = 12133/5000 > 0 is certified by "
            "Network Simplex over the declared 5-chart nerve with zero rational duality gap. Genuine cochains from continuous "
            "chart geometry require G1 moduli classification."
        ),
        "prompt": (
            "Explain the topological invariance of genuine alternating simplicial 1-cochains derived from the Cech nerve of the 5-chart cover:\n"
            "1. Formulate the nerve simplicial complex N(U) of the 5 charts (B_6, K_6^(3), cusps, H_6, S_6).\n"
            "2. Prove that the coboundary operator delta_0: C^0 -> C^1 satisfies sum_{e in C} (delta_0 alpha)_e == 0 for every 0-cochain "
            "potential alpha on every closed 1-cycle C in Z_1(N(U)).\n"
            "3. How does this prove that the circulation obstruction Phi_1 >= Gamma > 0 represents a genuine non-trivial cohomology class "
            "in H^1(N(U); R) that cannot be eliminated by any local gauge transformation, respecting: "
            f"'{FIREWALL}'?"
        ),
    },
    "G5": {
        "title": "Gap G5: Projector-Moment Positivity & Generic Operator Gap Q5/Q6",
        "context": (
            "Gap G5 is PARTIAL (Q5/Q6 generic operator gap open). Formalized in MomentPositivityObligation.lean, "
            "which defines the non-commutative polynomial algebra, truncated moment matrices M_d(E_tilde), and dual witness "
            "refutations W = L D L^T. It identifies the Soundness Gap between finite truncation and universal physical state realization."
        ),
        "prompt": (
            "Analyze the resolution of the Soundness Gap for generic operator candidates in MomentPositivityObligation.lean:\n"
            "1. Contrast the two formal closure routes: (a) Archimedean Positivstellensatz certificate in the non-commutative quadratic module, "
            "versus (b) Curto-Fialkow flat extension rank-loop closure (rank(M_d) = rank(M_{d-1})) via non-commutative GNS construction.\n"
            "2. Which route is computationally tractable in exact rational arithmetic for the 24x24 Gramian blocks of dimension 6?\n"
            "3. Formulate the exact Lean 4 theorem specification needed to close ProjectorMomentSoundnessBridge, respecting: "
            f"'{FIREWALL}'."
        ),
    },
}

SYSTEM_INSTRUCTION = """You are a world-class theoretical physicist, algebraic geometer, and Lean 4 formal verification specialist.
You are evaluating the 5 Gaps (S2: G1-G5) in the MUB(6) program under strict epistemic governance.

CONSTITUTIONAL RULES:
1. Strict Firewall: You MUST NEVER claim or imply MUB(6)=3 or MUB(6)<=3. All findings apply strictly to the declared region/moduli and mint no authority.
2. Claim Hygiene: Do NOT use hype verbs ('proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence', 'impossible', 'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized').
3. For each gap analysis, ALWAYS include:
   - What it supports
   - What it does not support
   - The narrowest defensible claim
   - The next test needed
4. Provide precise algebraic, geometric, and formal Lean 4 insights.
"""


def call_openrouter(model_id: str, prompt: str, api_key: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dbccpage/the_symbol_game",
        "X-Title": "MUB6-S2-Gap-Sweep",
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 8192,
    }
    t0 = time.time()
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - t0
            choice = data["choices"][0]
            finish_reason = choice.get("finish_reason")
            msg = choice.get("message", {})
            content = (msg.get("content") or "").strip()
            reasoning = (msg.get("reasoning") or "").strip()

            is_truncated = (finish_reason == "length") or (not content)
            success = (finish_reason != "length") and bool(content)

            usage = data.get("usage", {})
            return {
                "success": success,
                "finish_reason": finish_reason,
                "is_truncated": is_truncated,
                "content": content,
                "reasoning": reasoning,
                "elapsed_sec": round(elapsed, 2),
                "tokens": usage.get("total_tokens", 0),
                "cost": usage.get("cost", 0.0),
                "raw": data,
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        body_text = ""
        try:
            body_text = e.read().decode("utf-8")
        except Exception:
            pass
        return {
            "success": False,
            "finish_reason": "http_error",
            "is_truncated": False,
            "error": f"HTTPError {e.code}: {e.reason}",
            "http_status": e.code,
            "http_body": body_text,
            "elapsed_sec": round(elapsed, 2),
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "success": False,
            "finish_reason": "exception",
            "is_truncated": False,
            "error": str(e),
            "elapsed_sec": round(elapsed, 2),
        }


def evaluate_item(item: tuple) -> dict:
    gap_id, gap_info, model, api_key = item
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Launching {gap_id} on {model['name']}...")
    full_prompt = f"### CONTEXT:\n{gap_info['context']}\n\n### TASK:\n{gap_info['prompt']}"
    res = call_openrouter(model["id"], full_prompt, api_key)
    if res.get("success"):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] COMPLETED {gap_id} on {model['name']} ({res['elapsed_sec']}s, {res['tokens']} tokens)")
    elif res.get("is_truncated"):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] TRUNCATED {gap_id} on {model['name']} (finish_reason: {res.get('finish_reason')}, {res['elapsed_sec']}s)")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] FAILED {gap_id} on {model['name']}: {res.get('error')}")
    return {
        "gap_id": gap_id,
        "gap_title": gap_info["title"],
        "model_id": model["id"],
        "model_name": model["name"],
        "result": res,
    }


def main():
    print("=================================================================")
    print("MUB(6) S2 Gap Evaluation: Super Bunny Alpha & GLM 5.3")
    print(f"Firewall: {FIREWALL}")
    print("=================================================================")

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("REFUSAL: OPENROUTER_API_KEY environment variable not set in process environment.")
        sys.exit(1)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

    tasks = []
    for gap_id, gap_info in GAP_PROMPTS.items():
        for model in MODELS:
            tasks.append((gap_id, gap_info, model, api_key))

    print(f"Submitting {len(tasks)} tasks concurrently...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(evaluate_item, task) for task in tasks]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: (x["gap_id"], x["model_name"]))

    ts_slug = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = ARTIFACTS_DIR / f"s2_gaps_superbunny_glm_evaluation_{ts_slug}.json"
    if report_path.exists():
        print(f"REFUSAL: Target report path already exists: {report_path}")
        sys.exit(1)

    report_data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "firewall": FIREWALL,
        "total_evaluations": len(results),
        "successful_evaluations": sum(1 for r in results if r["result"].get("success")),
        "truncated_evaluations": sum(1 for r in results if r["result"].get("is_truncated")),
        "failed_evaluations": sum(
            1 for r in results if not r["result"].get("success") and not r["result"].get("is_truncated")
        ),
        "results": results,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    print(f"\n[OK] Raw JSON report saved to: {report_path}")

    md_lines = [
        "# MUB(6) Subgraph S2 Gap Evaluation Synthesis",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
        f"**Epistemic Firewall:** `{FIREWALL}`  ",
        "**Evaluated Models:** Super Bunny Alpha (`stealth/space-bunny-alpha`), GLM 5.3 (`z-ai/glm-5.3`)  ",
        "",
        "> [!WARNING]",
        "> **EPISTEMIC NOTICE & FIREWALL ENFORCEMENT:**",
        "> Model outputs are untrusted proposals with `AuthorityEffect: None`. They do not discharge or alter registry gap statuses.",
        "> When calls terminate at token limits with empty content, reasoning traces represent uncompleted scratchpads.",
        "",
        "---",
        "",
        "## Canonical Gap Status Reference",
        "",
        "Authoritative gap statuses, dependency bounds, and open residuals are maintained in [mub6_gap_registry.json](mub6_gap_registry.json):",
        "",
        "- **G1 (Full Moduli Classification)**: `OPEN` (Priority 1). Subgaps R6 (claimed unverified) and R7 (ENC-1147) open.",
        "- **G2 (Candidate Representation Bridge)**: `DISCHARGED_CONDITIONAL` on G1.",
        "- **G3 (Analytic Parameter Variation Enclosures)**: `PARTIAL`. Linear interpolation bounds endpoint margins only; does not bound parameter variation across CHM moduli.",
        "- **G4 (Genuine Simplicial 1-Cochains)**: `DISCHARGED_CONDITIONAL` on G1. Nerve circulation Phi_1 >= 12133/5000 is over declared nerve, not derived from continuous chart geometry.",
        "- **G5 (Projector-Moment Positivity)**: `PARTIAL` (Q5/Q6 generic operator gap open).",
        "",
        "---",
        "",
    ]

    for gap_id in ["G1", "G2", "G3", "G4", "G5"]:
        gap_results = [r for r in results if r["gap_id"] == gap_id]
        gap_title = gap_results[0]["gap_title"]
        md_lines.append(f"## {gap_title}\n")
        for gr in gap_results:
            model_name = gr["model_name"]
            res = gr["result"]
            md_lines.append(f"### Model: {model_name}\n")
            if res.get("success"):
                content = res.get("content") or ""
                reasoning = res.get("reasoning") or ""
                md_lines.append(f"- **Status:** Complete | **Latency:** {res.get('elapsed_sec')}s | **Tokens:** {res.get('tokens')}\n")
                if reasoning:
                    md_lines.append(f"<details><summary>Reasoning Trace ({len(reasoning)} chars)</summary>\n\n```\n{reasoning[:3000]}...\n```\n</details>\n")
                md_lines.append(f"#### Response:\n\n{content}\n")
            elif res.get("is_truncated"):
                reasoning = res.get("reasoning") or ""
                md_lines.append(f"- **Status:** TRUNCATED (finish_reason: {res.get('finish_reason')}) | **Latency:** {res.get('elapsed_sec')}s | **Tokens:** {res.get('tokens')}\n")
                md_lines.append("*Notice: Call hit token limit with message.content == null. Content is empty.*\n")
                if reasoning:
                    md_lines.append(f"<details><summary>Truncated Reasoning Trace ({len(reasoning)} chars)</summary>\n\n```\n{reasoning[:3000]}...\n```\n</details>\n")
            else:
                md_lines.append(f"**Error:** {res.get('error')}\n")
            md_lines.append("\n---\n")

    md_path = RESEARCH_DIR / f"s2_gaps_superbunny_glm_synthesis_{ts_slug}.md"
    if md_path.exists():
        print(f"REFUSAL: Target synthesis path already exists: {md_path}")
        sys.exit(1)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[OK] Markdown synthesis report saved to: {md_path}")

    any_failed_or_truncated = any(
        (not r["result"].get("success")) or r["result"].get("is_truncated")
        for r in results
    )
    if any_failed_or_truncated:
        print("[WARNING] One or more evaluations failed or were truncated. Exiting non-zero.")
        sys.exit(2)


if __name__ == "__main__":
    main()
