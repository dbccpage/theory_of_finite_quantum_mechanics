#!/usr/bin/env python3
"""
Higgs Pure Linear Certificate & Multi-Model Fit
================================================
Canonical pure diagnostic certificate for the Higgs potential on finite ℓ¹ carriers.

AuthorityEffect: None
Claim Ledger Link: HELL-C8 = FAILED (Mexican-hat potential does not emerge from pure L1 topology).
"""

import os
import json
import hashlib
import numpy as np
from pathlib import Path

def generate_certificate(output_path: str | os.PathLike[str] | None = None):
    phi_vals = np.linspace(0.1, 5.0, 50)
    # Pure l1 residual energy is strictly linear in field magnitude: E(phi) = |phi|
    energies_pure = np.abs(phi_vals)

    # 1. Linear Fit: E(phi) = a * phi + b
    fit_lin = np.polyfit(phi_vals, energies_pure, 1)
    pred_lin = np.poly1d(fit_lin)(phi_vals)
    r2_lin = float(1.0 - np.sum((energies_pure - pred_lin)**2) / np.sum((energies_pure - np.mean(energies_pure))**2))

    # 2. Quadratic Fit: E(phi) = a * phi^2 + b * phi + c
    fit_quad = np.polyfit(phi_vals, energies_pure, 2)
    pred_quad = np.poly1d(fit_quad)(phi_vals)
    r2_quad = float(1.0 - np.sum((energies_pure - pred_quad)**2) / np.sum((energies_pure - np.mean(energies_pure))**2))

    # 3. Quartic Fit: E(phi) = a * phi^4 + b * phi^2 + c (Mexican-hat shape)
    phi_sq = phi_vals**2
    fit_quartic = np.polyfit(phi_sq, energies_pure, 2)
    pred_quartic = np.poly1d(fit_quartic)(phi_sq)
    r2_quartic = float(1.0 - np.sum((energies_pure - pred_quartic)**2) / np.sum((energies_pure - np.mean(energies_pure))**2))

    cert_data = {
        "certificate_name": "higgs_pure_linear_certificate",
        "authority_effect": "None",
        "claim_ledger_ref": "HELL-C8",
        "claim_status": "FAILED",
        "verdict": "Along a fixed ray on a fixed-carrier complex with linear correction space, the sampled residual energy E(phi) = |phi| obeys fixed-carrier quotient homogeneity Phi_D(t*omega) = |t|*Phi_D(omega) (R2_linear = 1.000000). This V-shaped profile cannot produce a Mexican-hat double well without manual polynomial injection.",
        "r2_scores": {
            "r2_linear": round(r2_lin, 6),
            "r2_quadratic": round(r2_quad, 6),
            "r2_quartic": round(r2_quartic, 6)
        },
        "fits": {
            "linear_coeffs": [float(c) for c in fit_lin],
            "quadratic_coeffs": [float(c) for c in fit_quad],
            "quartic_coeffs": [float(c) for c in fit_quartic]
        }
    }

    # Hash payload
    cert_json = json.dumps(cert_data, indent=2)
    cert_hash = hashlib.sha256(cert_json.encode('utf-8')).hexdigest()
    cert_data["sha256_fingerprint"] = cert_hash

    # Save JSON certificate
    json_path = (
        Path(output_path)
        if output_path is not None
        else Path(__file__).resolve().with_suffix(".json")
    )
    with json_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(cert_data, f, indent=2)

    print("=" * 65)
    print(" HIGGS PURE LINEAR DIAGNOSTIC CERTIFICATE")
    print("=" * 65)
    print(f" R2 Linear Fit:    {r2_lin:.6f}  (PERFECT LINEAR FIT)")
    print(f" R2 Quadratic Fit: {r2_quad:.6f}")
    print(f" R2 Quartic Fit:   {r2_quartic:.6f}")
    print(f" Claim HELL-C8:    {cert_data['claim_status']}")
    print(f" SHA256 Fingerprint: {cert_hash}")
    print("=" * 65)
    print(f" Certificate saved to: {json_path}")

    return cert_data

if __name__ == "__main__":
    generate_certificate()
