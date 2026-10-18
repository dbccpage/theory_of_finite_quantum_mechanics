//! Production runner: branch-and-bound cover driver for Haagerup / Szöllősi H6 triple (I6, F6, H6).
//!
//! Point cover (fixed triple, delta=0):
//! ```text
//! cargo run -j 1 -p omega_mub --release --bin mub_haagerup_cover -- \
//!   --presplit 6 --depth 32 --chunk 0 --chunk-end 8
//! ```
//!
//! Neighborhood cover (widened by ±delta, default 1/1000):
//! ```text
//! cargo run -j 1 -p omega_mub --release --bin mub_haagerup_cover -- \
//!   --neighborhood --delta-den 1000 --presplit 6 --depth 32
//! ```
//!
//! Emit Lean 4 kernel reflection artifact:
//! ```text
//! cargo run -j 1 -p omega_mub --release --bin mub_haagerup_cover -- --emit-reflection
//! ```
//!
//! Writes under `artifacts/`. Completeness is never fabricated.
//!
//! AuthorityEffect: None

use omega_mub::omega_native::exact::mub6_cover_run::CoverCertificate;
use omega_mub::omega_native::campaign::mub6_dita_seed_cover::narrow_torus_cell;
use omega_mub::omega_native::exact::mub6_haagerup_cover::{
    cover_haagerup_gauge_fixed_chunk, cover_haagerup_narrow_cell,
    cover_haagerup_neighborhood_region, cover_haagerup_wide_cell, haagerup_cover_status,
    write_haagerup_reflection_artifact,
};
use omega_number_theory::rational::ri;
use std::path::PathBuf;

fn save_certificate(cert: &CoverCertificate, path: &PathBuf) {
    let json = serde_json::to_string_pretty(cert).expect("serialize certificate");
    std::fs::write(path, json).expect("write certificate file");
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut presplit: u32 = 6;
    let mut depth: u32 = 32;
    let mut threads: usize = 0;
    let mut chunk: Option<usize> = None;
    let mut chunk_end: Option<usize> = None;
    let mut neighborhood = false;
    let mut delta_den: i64 = 1000;
    let mut narrow_cell = false;
    let mut wide_cell = false;
    let mut emit_reflection = false;
    let mut status_only = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--presplit" => {
                presplit = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(presplit);
                i += 2;
            }
            "--depth" => {
                depth = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(depth);
                i += 2;
            }
            "--threads" => {
                threads = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(threads);
                i += 2;
            }
            "--chunk" => {
                chunk = args.get(i + 1).and_then(|s| s.parse().ok());
                i += 2;
            }
            "--chunk-end" => {
                chunk_end = args.get(i + 1).and_then(|s| s.parse().ok());
                i += 2;
            }
            "--neighborhood" | "--neigh" => {
                neighborhood = true;
                i += 1;
            }
            "--delta-den" => {
                delta_den = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(delta_den);
                i += 2;
            }
            "--narrow-cell" => {
                narrow_cell = true;
                i += 1;
            }
            "--wide-cell" => {
                wide_cell = true;
                i += 1;
            }
            "--emit-reflection" => {
                emit_reflection = true;
                i += 1;
            }
            "--status" => {
                status_only = true;
                i += 1;
            }
            "--help" | "-h" => {
                eprintln!(
                    "usage: mub_haagerup_cover [--presplit N] [--depth N] [--threads N] \
                     [--chunk I] [--chunk-end J] [--neighborhood] [--delta-den N] \
                     [--narrow-cell] [--wide-cell] [--emit-reflection] [--status]"
                );
                eprintln!(
                    "Triple: {{I6, F6(0,0), H6}} with H6 discrete Szöllősi basepoint (1, i, 1, -1)"
                );
                eprintln!("--emit-reflection: generates artifacts/kernel_reflection_haagerup_h6_box_cover.json");
                eprintln!("--neighborhood: widen B2/B3 by ±1/delta-den (default den=1000)");
                std::process::exit(0);
            }
            other => {
                eprintln!("unknown argument: {other} (try --help)");
                std::process::exit(2);
            }
        }
    }

    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let artifacts_dir = manifest_dir.join("../tests/omega_mub/artifacts");
    if !artifacts_dir.exists() {
        std::fs::create_dir_all(&artifacts_dir).expect("create artifacts dir");
    }

    if status_only {
        let st = haagerup_cover_status();
        println!("{}", serde_json::to_string_pretty(&st).unwrap());
        return;
    }

    if emit_reflection {
        let artifact_path = artifacts_dir.join("kernel_reflection_haagerup_h6_box_cover.json");
        println!(
            "Emitting Lean 4 kernel reflection artifact to {}...",
            artifact_path.display()
        );
        write_haagerup_reflection_artifact(&artifact_path).expect("write reflection artifact");
        println!("Artifact written successfully.");
    }

    if narrow_cell {
        println!("Running narrow cell cover...");
        let cert = cover_haagerup_narrow_cell();
        println!(
            "Narrow cell complete: {}, certified: {}, off_torus: {}, min_gap: {:?}",
            cert.complete, cert.certified, cert.off_torus, cert.min_gap
        );
        let path = artifacts_dir.join("haagerup_h6_narrow_cell_cover.json");
        save_certificate(&cert, &path);
    }

    if wide_cell {
        println!("Running wide cell cover...");
        let cert = cover_haagerup_wide_cell();
        println!(
            "Wide cell complete: {}, certified: {}, off_torus: {}, min_gap: {:?}",
            cert.complete, cert.certified, cert.off_torus, cert.min_gap
        );
        let path = artifacts_dir.join("haagerup_h6_wide_cell_cover.json");
        save_certificate(&cert, &path);
    }

    if let Some(c_start) = chunk {
        let c_end = chunk_end.unwrap_or(c_start + 1);
        println!("Running chunk range {c_start}..{c_end} (presplit {presplit}, depth {depth})...");
        for c in c_start..c_end {
            let cert = cover_haagerup_gauge_fixed_chunk(presplit, c, depth);
            let fname = format!("haagerup_h6_presplit{presplit}_chunk{c}_depth{depth}.json");
            let path = artifacts_dir.join(fname);
            save_certificate(&cert, &path);
            println!(
                "Chunk {c}: certified={}, off_torus={}, uncertified={}, complete={}, min_gap={:?}",
                cert.certified, cert.off_torus, cert.uncertified, cert.complete, cert.min_gap
            );
        }
    } else if neighborhood {
        let delta = ri(1) / ri(delta_den);
        println!("Running neighborhood cover with delta = 1/{delta_den} on narrow cell...");
        let cert = cover_haagerup_neighborhood_region(&delta, narrow_torus_cell(), depth);
        let fname = format!("haagerup_h6_neigh_delta_1_{delta_den}_narrow_cell.json");
        let path = artifacts_dir.join(fname);
        save_certificate(&cert, &path);
        println!(
            "Neighborhood cover: certified={}, off_torus={}, complete={}, min_gap={:?}",
            cert.certified, cert.off_torus, cert.complete, cert.min_gap
        );
    }
}
