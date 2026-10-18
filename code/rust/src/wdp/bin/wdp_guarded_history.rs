//! Emit a `wdp-guarded-coherence-v1` certificate for one causal problem file.
//!
//! Usage: `wdp_guarded_history <problem.json> [--pairs K]` (default `K = 3`).
//! The certificate is printed as compact, key-sorted ASCII JSON. A refusal is
//! printed as a typed refusal record with exit status 2. AuthorityEffect: None.
use omega_wdp::genesis_guarded_history::{guarded_certificate, Json, CERTIFICATE_SCHEMA};
use std::process::ExitCode;

fn refuse(reason: String) -> ExitCode {
    println!(
        "{}",
        Json::object([
            ("schema", Json::text(CERTIFICATE_SCHEMA)),
            ("status", Json::text("REFUSE")),
            ("authority_effect", Json::text("None")),
            ("reason", Json::text(reason)),
        ])
        .to_canonical()
    );
    ExitCode::from(2)
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut path = None;
    let mut pairs = 3usize;
    let mut k = 0;
    while k < args.len() {
        if args[k] == "--pairs" {
            let Some(value) = args.get(k + 1).and_then(|v| v.parse::<usize>().ok()) else {
                return refuse("--pairs needs a natural number".into());
            };
            pairs = value;
            k += 2;
        } else if path.is_none() {
            path = Some(args[k].clone());
            k += 1;
        } else {
            return refuse(format!("unexpected argument: {}", args[k]));
        }
    }
    let Some(path) = path else {
        return refuse("usage: wdp_guarded_history <problem.json> [--pairs K]".into());
    };
    let bytes = match std::fs::read(&path) {
        Ok(bytes) => bytes,
        Err(e) => return refuse(format!("problem file unavailable: {e}")),
    };
    match guarded_certificate(&bytes, pairs) {
        Ok(certificate) => {
            println!("{}", certificate.to_canonical());
            ExitCode::SUCCESS
        }
        Err(e) => refuse(e.to_string()),
    }
}
