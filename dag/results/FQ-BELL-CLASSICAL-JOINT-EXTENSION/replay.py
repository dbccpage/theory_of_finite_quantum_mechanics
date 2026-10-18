"""Replay this one Bell prompt's arithmetic and exact mathematical certificate.

Run with --write to regenerate response.json and certificate.json. No model API
is called; this is a deterministic replay of the Codex-assisted derivation.
"""

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NODE = "FQ-BELL-CLASSICAL-JOINT-EXTENSION"
# Replay only the historical snapshot; the live prompt now has a staged contract.
PROMPT = HERE / "prompt.yaml"
SPEC = importlib.util.spec_from_file_location("bell_joint_extension", ROOT / "code/python/src/qm/bell_joint_extension.py")
bell = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bell
SPEC.loader.exec_module(bell)


def pair(value):
    value = Q(value)
    return [value.numerator, value.denominator]


def results():
    potentials = [1140, 1140-3420, 1140-3420+3990]
    response = {
        "derived_under_policy": "SPK-001",
        "authority_effect": "None",
        "firewall_status": "stated region only; mints no authority.",
        "node_id": NODE,
        "stage": "FINITE_QM_CORE",
        "dag_status": "PROVED_LEAN",
        "operad_family_id": "OP-FINITE_QM_CORE-" + NODE,
        "p_star_tree_potentials": potentials,
        "p_star_chord_potential": potentials[-1],
        "p_star_holonomy_gamma2": abs(-570-potentials[-1]),
        "cochain_d1_d0_exact_zero": True,
        "finite_shadow_witness_int": 4*114+3*7+3,
        "countermodel_witness_int": 263-128-7,
        "unpaid_import_count": 2,
        "unconditional_promotion_refused": True,
        "lean4_theorem_anchor": "lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound",
        "rust_witness_anchor": "omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness",
        "should_continue": False,
    }
    d0 = [[-1,1,0,0],[0,-1,1,0],[0,0,-1,1],[-1,0,0,1]]
    d1 = [1,1,1,-1]
    c = [1140,-3420,3990,-570]
    a = [0]+potentials
    kernel = [sum(d1[e]*d0[e][v] for e in range(4)) for v in range(4)]
    residual = [c[e]-sum(d0[e][v]*a[v] for v in range(4)) for e in range(4)]
    gamma = abs(sum(x*y for x,y in zip(d1,c)))
    dual_pairing = sum(x*y for x,y in zip(d1,c))
    assert kernel == [0]*4 and gamma == sum(map(abs,residual)) == dual_pairing == 2280
    wrong_d1 = [1,1,1,1]
    wrong_kernel = [sum(wrong_d1[e]*d0[e][v] for e in range(4)) for v in range(4)]
    assert wrong_kernel != [0]*4
    vertices = []
    for mask in range(16):
        law = [0]*16
        law[mask] = 1
        cert = bell.certify_joint_law(law)
        vertices.append({"mask":mask,"assignment":[1 if mask & (1<<j) else -1 for j in range(4)],"correlators":[pair(q) for q in cert.correlators],"chsh":pair(cert.chsh)})
    assert Counter(v["chsh"][0] for v in vertices) == {2:8,-2:8}
    laws = {
        "upper_saturation": [Q(1)]+[Q(0)]*15,
        "lower_saturation": [Q(0),Q(1)]+[Q(0)]*14,
        "uniform": [Q(1,16)]*16,
        "nontrivial_mixture": [Q(3,5),Q(2,5)]+[Q(0)]*14,
    }
    controls = {}
    for name, law in laws.items():
        cert = bell.certify_joint_law(law)
        assert cert.lower_slack == 4*cert.positive_score_mass >= 0
        assert cert.upper_slack == 4*cert.negative_score_mass >= 0
        controls[name] = {
            "weights": [pair(p) for p in law],
            "correlators": [pair(q) for q in cert.correlators],
            "chsh": pair(cert.chsh),
            "positive_score_mass": pair(cert.positive_score_mass),
            "negative_score_mass": pair(cert.negative_score_mass),
            "lower_slack": pair(cert.lower_slack),
            "upper_slack": pair(cert.upper_slack),
        }
    refusals = {}
    for name, law in {
        "signed_normalized_score_4": [Q(3,2),Q(-1,2)]+[Q(0)]*14,
        "unnormalized_score_4": [Q(2)]+[Q(0)]*15,
    }.items():
        try:
            bell.certify_joint_law(law)
        except ValueError as error:
            refusals[name] = str(error)
        else:
            raise AssertionError(f"Invalid law accepted: {name}")
    certificate = {
        "node_id":NODE,"authority_effect":"None",
        "prompt_sha256":hashlib.sha256(PROMPT.read_bytes()).hexdigest(),
        "scalar_field":"Q; finite common-denominator representation in Lean",
        "bit_order":["A0","A1","B0","B1"],
        "deterministic_vertices":vertices,"valid_controls":controls,"refused_controls":refusals,
        "diagnostic_only":{"d0":d0,"d1":d1,"d1_d0":kernel,"cochain":c,"potential":a,"residual":residual,"dual":d1,"dual_pairing":dual_pairing,"l1_optimum":sum(map(abs,residual)),"gamma2":gamma,"wrong_sign_d1_d0":wrong_kernel},
        "bookkeeping_only":{"stage_route_value":480,"prescribed_subtraction_value":128,"quotient_interpretation":"not established by the supplied scalar arithmetic"},
    }
    assert len(response) == 18
    return {"response.json":response,"certificate.json":certificate}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    options = parser.parse_args()
    assert hashlib.sha256(PROMPT.read_bytes()).hexdigest() == json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))["prompt_sha256"], "Historical input snapshot changed"
    for filename, data in results().items():
        path = HERE / filename
        if options.write:
            path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        else:
            assert json.loads(path.read_text(encoding="utf-8")) == data, filename
    print("PASS: one prompt, 18 response fields, 16 vertices, exact valid/refusal controls, and C4 primal/dual certificate.")
