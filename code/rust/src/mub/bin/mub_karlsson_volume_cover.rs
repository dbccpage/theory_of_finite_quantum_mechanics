//! Production runner: exact rational 3D octree interval solver for the Karlsson volume K_6^{(3)}(x, y, z).
//!
//! AuthorityEffect: None
//! Restricted words: forced, minimal, free, canonical, equivalent, universal, complete
//! require proof or explicit conditional scope. The `complete` flag denotes finite
//! branch-and-bound partition termination over the declared stated region, nothing more.
//!
//! ## Usage
//! ```text
//! cargo run --release -p omega_mub --bin mub_karlsson_volume_cover -- \
//!   --grid 2 --delta-den 1000 --max-depth 24 --emit
//! ```
//!
//! Writes exact cover receipt under:
//! - `omega_engine/crates_rs/tests/omega_mub/artifacts/mub_karlsson_volume_cover.json`
//! - `artifacts/mub_karlsson_volume_cover.json`

use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;

use num_rational::BigRational;
use sha2::{Digest, Sha256};

use omega_mub::omega_native::exact::mub6_karlsson_volume_cover::solve_karlsson_volume_cover;

fn find_repo_root(start: &Path) -> PathBuf {
    let mut cur = start.to_path_buf();
    while let Some(parent) = cur.parent() {
        cur = parent.to_path_buf();
        if cur.join(".git").exists() {
            return cur;
        }
    }
    start.to_path_buf()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut grid: usize = 2;
    let mut delta_den: i64 = 1000;
    let mut max_depth: u32 = 24;
    let mut emit = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--grid" => {
                grid = args.get(i + 1).and_then(|s| s.parse().ok()).unwrap_or(grid);
                i += 2;
            }
            "--delta-den" => {
                delta_den = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(delta_den);
                i += 2;
            }
            "--max-depth" => {
                max_depth = args
                    .get(i + 1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(max_depth);
                i += 2;
            }
            "--emit" => {
                emit = true;
                i += 1;
            }
            "--help" | "-h" => {
                eprintln!(
                    "usage: mub_karlsson_volume_cover [--grid N] [--delta-den N] [--max-depth N] [--emit]"
                );
                return;
            }
            other => {
                eprintln!("unknown argument: {}", other);
                std::process::exit(1);
            }
        }
    }

    let delta = BigRational::new(1.into(), delta_den.into());

    println!("=== Karlsson 3D Volume Cover Interval Solver ===");
    println!("AuthorityEffect: None");
    println!("Firewall Line: stated region only; mints no authority");
    println!("Grid divisions per axis: {}", grid);
    println!("Seed exclusion delta: {}", delta);
    println!("Max bisection depth: {}", max_depth);
    println!("Emit JSON receipt: {}", emit);
    println!("================================================");

    let start = Instant::now();
    let mut report = solve_karlsson_volume_cover(grid, &delta, max_depth);
    let elapsed = start.elapsed();

    println!();
    println!("=== Solver Results ===");
    println!("Elapsed time: {:?}", elapsed);
    println!("Total boxes explored: {}", report.total_boxes_explored);
    println!("Off-torus boxes pruned: {}", report.off_torus_boxes_pruned);
    println!("Seed neighborhood boxes: {}", report.seed_neighborhood_boxes);
    println!("Outside boxes certified: {}", report.outside_boxes_certified);
    println!("Uncertified boxes: {}", report.uncertified_boxes);
    println!("Min triad defect gap: {}", report.min_triad_defect_gap);
    println!("Min extension psi gap: {}", report.min_extension_psi_gap);
    println!(
        "Overall min psi: {} / {}",
        report.overall_min_psi_num, report.overall_min_psi_den
    );
    println!("Max depth used: {}", report.max_depth_used);
    println!("Cover complete: {}", report.complete);
    println!("======================");

    if emit {
        // Pre-serialize without digest to compute SHA-256 over canonical content
        let pre_json = serde_json::to_string_pretty(&report)
            .expect("failed to serialize preliminary Karlsson volume report to JSON");
        let mut hasher = Sha256::new();
        hasher.update(pre_json.as_bytes());
        let digest = format!("{:x}", hasher.finalize());

        report.sha256_digest = Some(digest.clone());

        let json_str = serde_json::to_string_pretty(&report)
            .expect("failed to serialize final Karlsson volume report to JSON");

        // Target path 1: inside omega_mub/artifacts/
        let crate_artifact_dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
        fs::create_dir_all(&crate_artifact_dir)
            .expect("failed to create crate artifacts directory");
        let crate_artifact_path = crate_artifact_dir.join("mub_karlsson_volume_cover.json");
        fs::write(&crate_artifact_path, &json_str)
            .expect("failed to write crate cover receipt JSON");

        // Target path 2: repository root artifacts/
        let repo_root = find_repo_root(Path::new(env!("CARGO_MANIFEST_DIR")));
        let repo_artifact_dir = repo_root.join("artifacts");
        fs::create_dir_all(&repo_artifact_dir)
            .expect("failed to create repo artifacts directory");
        let repo_artifact_path = repo_artifact_dir.join("mub_karlsson_volume_cover.json");
        fs::write(&repo_artifact_path, &json_str)
            .expect("failed to write repo cover receipt JSON");

        println!();
        println!("Cover receipt emitted:");
        println!("  Crate path: {}", crate_artifact_path.display());
        println!("  Repo path:  {}", repo_artifact_path.display());
        println!("  SHA-256:    {}", digest);
    }

    if !report.complete || report.uncertified_boxes > 0 {
        eprintln!(
            "FAIL: Cover incomplete (uncertified_boxes = {})",
            report.uncertified_boxes
        );
        std::process::exit(2);
    }
}
