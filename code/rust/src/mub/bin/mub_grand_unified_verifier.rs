
use tfqm_mub::native::{
    exact::mub6_collar_solver, exact::mub6_deltoid_cusp_asymptotics, exact::mub6_frame_potential, exact::mub6_hyper_gramian,
    exact::mub6_quad_sdp, exact::mub6_tao_confluence,
};
use serde::Serialize;
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::{
    fs,
    path::{Path, PathBuf},
};

pub const CANONICAL_ARTIFACTS: &[(&str, &str)] = &[
    (
        "dita_seed_f6_0_8_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json",
        "c19a88e198f9fb0b13bd710a9d2476f4f602113590a17f4d93e7c7459a7a5500",
    ),
    (
        "dita_seed_f6_8_0_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json",
        "3365d33601e382602d5eab15e8d77b1c42abfe9120a229149f2b9302de5feaea",
    ),
    (
        "dita_seed_f6_16_16_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json",
        "bd7d0b07e5738ca1b7f890aa2308e7ef97fb4f7bdc70a0e96e7627cb4ffc08da",
    ),
    (
        "dita_seed_f6_0_16_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json",
        "88f1ee39d38dbc2bc1b38c52e3e7be43ed254900ffebf68a65b4e68e69406d04",
    ),
    (
        "dita_seed_f6_8_8_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json",
        "72a84db365a57b5a4c6113d946c20e4291deb27e61616896ae8d29b1df18f42c",
    ),
    (
        "dita_seed_f6_16_0_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json",
        "5d5eeaa3e601f0be0867989cdb783dfdbd43241a6955cecd2f8159fdd2db2fad",
    ),
    (
        "kernel_reflection_tao_s6_box_cover.json",
        "8675bec28ded1849d122cc594521ba62288785a7e299f4830d470e1668bd573c",
    ),
    (
        "kernel_reflection_haagerup_h6_box_cover.json",
        "6a1dc358d0875e0ce86e125109113ed3b70f643d9adf7a34e5e45f35b1bb4a65",
    ),
    (
        "mub_continuous_manifold_residue_cover.json",
        "8cfde36248b61bc7dc904cf5f48cebb67f03e964f6a988549fe736fcbdcb6d53",
    ),
    (
        "dita_seed_atlas_c2_report_20260724.json",
        "a3feea0ea3f7e439d48105e938b72d9ecc7904b6821fac7a170e136de47df854",
    ),
    (
        "kernel_reflection_1024_box_complex_dita_0_16.json",
        "5973324bdec76985be0733d4a37fcb0c567fba49bd0b98ef86359e122ad3cbd8",
    ),
    (
        "szollosi_triad_search_receipt.json",
        "fa0d854e97a790eb8ef30f3306368373f257da54659553833eb22637024a39ad",
    ),
    (
        "lane_v2_python_verification_receipt.json",
        "d12ef371a6355089dda6dad3076b70a647108e6e48ee00d67240923ad288851e",
    ),
    (
        "lane_v3_adversarial_soundness_audit_20260917.json",
        "bc4ec8dea2b693c5c2dd94509f306d4415391b189c3ed0ff9ea9d244a2d5105e",
    ),
    (
        "mub_karlsson_volume_cover.json",
        "5d534f8d8c8b93c5bcd9cde8d136d9fff84a510ef05b690c35edc1cc6a60ae6f",
    ),
    (
        "mub_karlsson_collar_cover.json",
        "61d5369bef2ddf5b6abb5d2adc3a2a509f5f7f1bc459c1e6d94e0b10aeef68f8",
    ),
    (
        "mub_deltoid_cusps.json",
        "b5137d5a33b845d2b6b0a572e95ce791ad86a15349edc160a0c593057c645fb7",
    ),
    (
        "mub_tao_confluence_receipt.json",
        "6ba75dd6445cc84ffd6875657a8650a6209ace6a2f22753060e7f60b8f730c58",
    ),
    (
        "mub_quad_sdp_certificate.json",
        "eb762d08da02183a25e876c43091a83a488ef826cae66570a13eedea40777548",
    ),
    (
        "mub_hyper_gramian_sdp.json",
        "8458cd0e03eabd214c27e4accf52d946ac28ddf0be7c29a29ce0ab55ccb8d3bc",
    ),
    (
        "mub_frame_potential.json",
        "4501eda390469ddd57fe2a39e07df4dfa4605513b8ac209b2ce2b5de9198bc61",
    ),
];

#[derive(Debug, Serialize)]
struct ArtifactCheck {
    filename: String,
    sha256: String,
    status: String,
}

#[derive(Debug, Serialize)]
struct Receipt {
    schema_version: &'static str,
    authority_effect: &'static str,
    firewall: &'static str,
    overall_verdict: &'static str,
    integrity_status: &'static str,
    mathematical_certification: bool,
    frontier_receipts_replayed: usize,
    artifacts: Vec<ArtifactCheck>,
    pending_obligations: Vec<&'static str>,
}

fn replay(name: &str) -> Result<Option<Value>, String> {
    let result = match name {
        "mub_karlsson_collar_cover.json" => {
            serde_json::to_value(mub6_collar_solver::solve_karlsson_collar_cover(2))
        }
        "mub_deltoid_cusps.json" => {
            serde_json::to_value(mub6_deltoid_cusp_asymptotics::solve_deltoid_cusp_asymptotics())
        }
        "mub_tao_confluence_receipt.json" => {
            serde_json::to_value(mub6_tao_confluence::solve_tao_confluence())
        }
        "mub_quad_sdp_certificate.json" => {
            serde_json::to_value(mub6_quad_sdp::solve_quad_sdp_certificate())
        }
        "mub_hyper_gramian_sdp.json" => {
            serde_json::to_value(mub6_hyper_gramian::solve_hyper_gramian_certificate())
        }
        "mub_frame_potential.json" => {
            serde_json::to_value(mub6_frame_potential::solve_frame_potential_certificate())
        }
        _ => return Ok(None),
    };
    result.map(Some).map_err(|e| e.to_string())
}

fn verify_artifacts(dir: &Path) -> Result<Receipt, String> {
    let mut artifacts = Vec::new();
    let mut replayed = 0;
    for (filename, expected_digest) in CANONICAL_ARTIFACTS {
        let bytes = fs::read(dir.join(filename)).map_err(|e| format!("{filename}: {e}"))?;
        let digest = format!("{:x}", Sha256::digest(&bytes));
        if &digest != expected_digest {
            return Err(format!(
                "SHA-256 mismatch for {filename}: expected {expected_digest}, got {digest}"
            ));
        }
        let supplied: Value =
            serde_json::from_slice(&bytes).map_err(|e| format!("{filename}: {e}"))?;
        let status = if let Some(expected) = replay(filename)? {
            if supplied != expected {
                return Err(format!("exact replay mismatch for {filename}"));
            }
            replayed += 1;
            "SCOPED_DIAGNOSTIC_REPLAYED"
        } else {
            "LEGACY_DIGEST_ONLY_NOT_MATHEMATICALLY_REPLAYED"
        };
        artifacts.push(ArtifactCheck {
            filename: (*filename).into(),
            sha256: digest,
            status: status.into(),
        });
    }
    Ok(Receipt {
        schema_version:"omega.mub.grand-unified-verification.v2",
        authority_effect:"None",
        firewall:"stated region only; mints no authority",
        overall_verdict:"INCOMPLETE_MATHEMATICAL_CERTIFICATION",
        integrity_status:"PASS",
        mathematical_certification:false,
        frontier_receipts_replayed:replayed,
        artifacts,
        pending_obligations:vec![
            "full replay and candidate-domain binding of the legacy cover receipts",
            "concrete family, derivative, and curvature bounds for the collar and cusp charts",
            "a justified Tao confluence chart and a checked candidate-space cover",
            "a representation/coverage theorem extending a fixed block-matrix diagnostic to other candidates",
            "explicit moduli coverage and gluing hypotheses linked to concrete Lean definitions",
        ],
    })
}

struct VerifierArgs {
    dir: PathBuf,
    output: Option<PathBuf>,
    emit: bool,
    integrity_only: bool,
}

fn apply_verifier_flag(
    arg: &str,
    args: &mut std::iter::Skip<std::env::Args>,
    parsed: &mut VerifierArgs,
) -> Result<bool, String> {
    match arg {
        "--artifacts-dir" => {
            parsed.dir = PathBuf::from(args.next().ok_or("--artifacts-dir requires a path")?);
        }
        "--output" => {
            parsed.output = Some(PathBuf::from(
                args.next().ok_or("--output requires a path")?,
            ));
        }
        "--emit" => parsed.emit = true,
        "--integrity-only" => parsed.integrity_only = true,
        "--verbose" => {}
        "--help" | "-h" => {
            println!("usage: mub_grand_unified_verifier [--artifacts-dir PATH] [--integrity-only] [--emit | --output PATH]");
            return Ok(false);
        }
        _ => return Err(format!("unknown argument: {arg}")),
    }
    Ok(true)
}

fn parse_verifier_args(default_dir: PathBuf) -> Result<Option<VerifierArgs>, String> {
    let mut parsed = VerifierArgs {
        dir: default_dir,
        output: None,
        emit: false,
        integrity_only: false,
    };
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        if !apply_verifier_flag(&arg, &mut args, &mut parsed)? {
            return Ok(None);
        }
    }
    if parsed.emit && parsed.output.is_some() {
        return Err("choose --emit or --output".into());
    }
    Ok(Some(parsed))
}

fn write_verifier_output(
    bytes: &[u8],
    output: Option<PathBuf>,
    emit: bool,
    artifacts: PathBuf,
) -> Result<(), String> {
    if let Some(path) = output {
        fs::write(path, bytes).map_err(|e| e.to_string())?;
    } else if emit {
        for target in [artifacts] {
            fs::write(
                target.join("grand_unified_mub6_verification_receipt.json"),
                bytes,
            )
            .map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}

fn run() -> Result<i32, String> {
    let artifacts = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    let Some(parsed) = parse_verifier_args(artifacts.clone())? else {
        return Ok(0);
    };
    let receipt = verify_artifacts(&parsed.dir)?;
    let bytes = serde_json::to_vec_pretty(&receipt).map_err(|e| e.to_string())?;
    write_verifier_output(&bytes, parsed.output, parsed.emit, artifacts)?;
    println!("{}", String::from_utf8(bytes).map_err(|e| e.to_string())?);
    Ok(if parsed.integrity_only { 0 } else { 2 })
}

fn main() {
    match run() {
        Ok(code) => std::process::exit(code),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    }
}
