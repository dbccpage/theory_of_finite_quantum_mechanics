//! Production runner: gauge-fixed 5-torus cover for genuine Dita seed triples.
//!
//! Point cover (fixed triple, delta=0):
//! ```text
//! cargo run -j 1 -p omega_mub --release --bin mub_dita_seed_cover -- \
//!   --dx 0 --dy 8 --presplit 6 --depth 32 --chunk 0 --chunk-end 8
//! ```
//!
//! Neighborhood cover (B2/B3 widened by ±delta, default 1/1000):
//! ```text
//! cargo run -j 1 -p omega_mub --release --bin mub_dita_seed_cover -- \
//!   --dx 0 --dy 8 --neighborhood --delta-den 1000 --presplit 6 --depth 32 \
//!   --chunk 0 --chunk-end 8
//! ```
//!
//! Writes under `artifacts/`. Completeness is never fabricated.

use num_rational::BigRational;
use omega_mub::omega_native::campaign::mub6_dita_seed_cover::{
    dita_seed_gauge_fixed_chunk_cover, dita_seed_gauge_fixed_cover_parallel,
    dita_seed_neighborhood_gauge_fixed_chunk_cover,
    dita_seed_neighborhood_gauge_fixed_cover_parallel, genuine_dita_y2q1_triple_seeds_check,
    merge_on_disk_presplit6_chunks_strict, merge_on_disk_presplit6_neighborhood_chunks_strict,
    neighborhood_chunk_filename, neighborhood_delta_1_1000, write_cover_certificate_artifact,
};
use omega_number_theory::rational::ri;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut dx: i64 = 0;
    let mut dy: i64 = 8;
    let mut presplit: u32 = 6;
    let mut depth: u32 = 32;
    let mut threads: usize = 0;
    let mut chunk: Option<usize> = None;
    let mut chunk_end: Option<usize> = None;
    let mut neighborhood = false;
    let mut delta_den: i64 = 1000;
    let mut merge = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--dx" => {
                dx = args.get(i + 1).and_then(|s| s.parse().ok()).unwrap_or(dx);
                i += 2;
            }
            "--dy" => {
                dy = args.get(i + 1).and_then(|s| s.parse().ok()).unwrap_or(dy);
                i += 2;
            }
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
            "--merge" => {
                merge = true;
                i += 1;
            }
            "--delta-den" => {
                delta_den = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(delta_den);
                i += 2;
            }
            "--help" | "-h" => {
                eprintln!(
                    "usage: mub_dita_seed_cover [--dx N] [--dy N] [--presplit N] [--depth N] \
                     [--threads N] [--chunk I] [--chunk-end J] [--neighborhood] [--delta-den N] \
                     [--merge]"
                );
                eprintln!("genuine Y2Q1 seeds: (0,8), (8,0), (16,16)");
                eprintln!("genuine Y2Q2 dual:  (0,16), (8,8), (16,0)");
                eprintln!("chunk mode: cover chunks I..J-1 of 2^presplit (exclusive end)");
                eprintln!("--neighborhood: widen B2/B3 by ±1/delta-den (default den=1000)");
                eprintln!("--merge: load 64 on-disk chunks and write *_merged_complete.json");
                std::process::exit(0);
            }
            other => {
                eprintln!("unknown arg: {other}");
                std::process::exit(2);
            }
        }
    }

    if let Err(msg) = genuine_dita_y2q1_triple_seeds_check(dx, dy) {
        eprintln!("refusing non-genuine seed: {msg}");
        std::process::exit(2);
    }

    if merge {
        let delta_tag = format!("1_{delta_den}");
        let (cert, fname, checksums) = if neighborhood {
            eprintln!(
                "merging on-disk NEIGH chunks F6({dx},{dy}) delta=1/{delta_den} presplit=6 (enforcing strict bijection & checksum validation)"
            );
            match merge_on_disk_presplit6_neighborhood_chunks_strict(dx, dy, &delta_tag) {
                Ok((c, csums)) => (
                    c,
                    format!(
                        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_gauge_fixed_5_torus_presplit6_merged_complete.json"
                    ),
                    csums,
                ),
                Err(e) => {
                    eprintln!("strict merge failed: {e}");
                    std::process::exit(1);
                }
            }
        } else {
            eprintln!(
                "merging on-disk POINT chunks F6({dx},{dy}) presplit=6 (enforcing strict bijection & checksum validation)"
            );
            match merge_on_disk_presplit6_chunks_strict(dx, dy) {
                Ok((c, csums)) => (
                    c,
                    format!(
                        "dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged_complete.json"
                    ),
                    csums,
                ),
                Err(e) => {
                    eprintln!("strict merge failed: {e}");
                    std::process::exit(1);
                }
            }
        };
        eprintln!(
            "merged: complete={} certified={} off_torus={} uncertified={} max_depth={} min_gap={:?} (verified {} chunk checksums)",
            cert.complete,
            cert.certified,
            cert.off_torus,
            cert.uncertified,
            cert.max_depth_used,
            cert.min_gap,
            checksums.len()
        );
        match write_cover_certificate_artifact(&cert, &fname) {
            Ok(path) => {
                println!("{}", path.display());
                // Write chunk checksum manifest alongside the merged complete certificate
                let manifest_fname = format!("{fname}.chunks.sha256");
                let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
                let manifest_path = dir.join(manifest_fname);
                let manifest_content: String = checksums
                    .iter()
                    .map(|(idx, sha)| format!("{sha}  chunk{idx}\n"))
                    .collect();
                let _ = std::fs::write(&manifest_path, manifest_content);
                if !cert.complete {
                    eprintln!(
                        "WARNING: merge incomplete (uncertified={})",
                        cert.uncertified
                    );
                    std::process::exit(3);
                }
            }
            Err(e) => {
                eprintln!("failed to write merged artifact: {e}");
                std::process::exit(1);
            }
        }
        return;
    }

    let delta: BigRational = if neighborhood {
        if delta_den <= 0 {
            eprintln!("--delta-den must be positive");
            std::process::exit(2);
        }
        ri(1) / ri(delta_den)
    } else {
        neighborhood_delta_1_1000() // unused in point mode
    };
    let delta_tag = format!("1_{delta_den}");

    if let Some(start) = chunk {
        let end = chunk_end.unwrap_or(start + 1);
        let n_chunks = 1usize << presplit;
        if start >= n_chunks || end > n_chunks || start >= end {
            eprintln!("invalid chunk range [{start},{end}) for n={n_chunks}");
            std::process::exit(2);
        }
        let mut any_incomplete = false;
        let mut complete_count = 0usize;
        for idx in start..end {
            if neighborhood {
                eprintln!(
                    "chunk {idx}/{n_chunks} F6({dx},{dy}) NEIGH delta=1/{delta_den} \
                     presplit={presplit} depth={depth}"
                );
                let cert = dita_seed_neighborhood_gauge_fixed_chunk_cover(
                    dx, dy, &delta, presplit, idx, depth,
                );
                eprintln!(
                    "  complete={} certified={} off_torus={} uncertified={} max_depth={}",
                    cert.complete,
                    cert.certified,
                    cert.off_torus,
                    cert.uncertified,
                    cert.max_depth_used
                );
                let fname = neighborhood_chunk_filename(dx, dy, &delta_tag, presplit, idx, depth);
                match write_cover_certificate_artifact(&cert, &fname) {
                    Ok(path) => println!("{}", path.display()),
                    Err(e) => {
                        eprintln!("write failed: {e}");
                        std::process::exit(1);
                    }
                }
                if cert.complete {
                    complete_count += 1;
                } else {
                    any_incomplete = true;
                }
            } else {
                eprintln!(
                    "chunk {idx}/{n_chunks} F6({dx},{dy}) POINT presplit={presplit} depth={depth}"
                );
                let cert = dita_seed_gauge_fixed_chunk_cover(dx, dy, presplit, idx, depth);
                eprintln!(
                    "  complete={} certified={} off_torus={} uncertified={} max_depth={}",
                    cert.complete,
                    cert.certified,
                    cert.off_torus,
                    cert.uncertified,
                    cert.max_depth_used
                );
                let fname = format!(
                    "dita_seed_F6_{dx}_{dy}_gauge5_presplit{presplit}_chunk{idx}_depth{depth}.json"
                );
                match write_cover_certificate_artifact(&cert, &fname) {
                    Ok(path) => println!("{}", path.display()),
                    Err(e) => {
                        eprintln!("write failed: {e}");
                        std::process::exit(1);
                    }
                }
                if cert.complete {
                    complete_count += 1;
                } else {
                    any_incomplete = true;
                }
            }
        }
        eprintln!(
            "farm done: {}/{} chunks complete in range (neighborhood={neighborhood})",
            complete_count,
            end - start
        );
        if any_incomplete {
            std::process::exit(3);
        }
        return;
    }

    if neighborhood {
        eprintln!(
            "running full gauge-fixed 5-torus NEIGHBORHOOD cover for F6({dx},{dy})+Y2Q1 \
             delta=1/{delta_den} presplit={presplit} depth={depth} threads={threads}"
        );
        let cert = dita_seed_neighborhood_gauge_fixed_cover_parallel(
            dx, dy, &delta, presplit, depth, threads,
        );
        eprintln!(
            "done: complete={} certified={} off_torus={} uncertified={} max_depth={} min_gap={:?}",
            cert.complete,
            cert.certified,
            cert.off_torus,
            cert.uncertified,
            cert.max_depth_used,
            cert.min_gap
        );
        let fname = format!(
            "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_presplit{presplit}_depth{depth}.json"
        );
        match write_cover_certificate_artifact(&cert, &fname) {
            Ok(path) => {
                println!("{}", path.display());
                if !cert.complete {
                    eprintln!(
                        "WARNING: cover incomplete (uncertified={})",
                        cert.uncertified
                    );
                    std::process::exit(3);
                }
            }
            Err(e) => {
                eprintln!("failed to write artifact: {e}");
                std::process::exit(1);
            }
        }
        return;
    }

    eprintln!(
        "running full gauge-fixed 5-torus POINT cover for F6({dx},{dy})+Y2Q1 \
         presplit={presplit} depth={depth} threads={threads}"
    );
    let cert = dita_seed_gauge_fixed_cover_parallel(dx, dy, presplit, depth, threads);
    eprintln!(
        "done: complete={} certified={} off_torus={} uncertified={} max_depth={} min_gap={:?}",
        cert.complete,
        cert.certified,
        cert.off_torus,
        cert.uncertified,
        cert.max_depth_used,
        cert.min_gap
    );

    let fname = format!("dita_seed_F6_{dx}_{dy}_gauge5_presplit{presplit}_depth{depth}.json");
    match write_cover_certificate_artifact(&cert, &fname) {
        Ok(path) => {
            println!("{}", path.display());
            if !cert.complete {
                eprintln!(
                    "WARNING: cover incomplete (uncertified={})",
                    cert.uncertified
                );
                std::process::exit(3);
            }
        }
        Err(e) => {
            eprintln!("failed to write artifact: {e}");
            std::process::exit(1);
        }
    }
}
