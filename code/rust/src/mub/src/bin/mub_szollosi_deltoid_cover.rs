
use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;

use num_rational::BigRational;
use sha2::{Digest, Sha256};

use omega_mub::omega_native::exact::mub6_szollosi_deltoid_cover::solve_szollosi_deltoid_cover;

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
    let mut grid: usize = 8;
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
                    "usage: mub_szollosi_deltoid_cover [--grid N] [--delta-den N] [--max-depth N] [--emit]"
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

    println!("=== Szöllősi Deltoid Arc Interval Solver ===");
    println!("AuthorityEffect: None");
    println!("Firewall Line: stated region only; mints no authority");
    println!("Grid divisions per axis: {}", grid);
    println!("Cusp exclusion delta: {}", delta);
    println!("Max bisection depth: {}", max_depth);
    println!("Emit JSON receipt: {}", emit);
    println!("============================================");

    let start = Instant::now();
    let mut report = solve_szollosi_deltoid_cover(grid, &delta, max_depth);
    let elapsed = start.elapsed();

    println!();
    println!("=== Solver Results ===");
    println!("Elapsed time: {:?}", elapsed);
    println!("Total boxes explored: {}", report.total_boxes_explored);
    println!("Off-circle boxes pruned: {}", report.off_circle_boxes_pruned);
    println!("Cusp neighborhood boxes: {}", report.cusp_neighborhood_boxes);
    println!("Outside boxes certified: {}", report.outside_boxes_certified);
    println!("Uncertified boxes: {}", report.uncertified_boxes);
    println!("Min triad defect gap: {}", report.min_triad_defect_gap);
    println!("Min extension psi gap: {}", report.min_extension_psi_gap);
    println!("Overall min psi: {} / {}", report.overall_min_psi_num, report.overall_min_psi_den);
    println!("Max depth used: {}", report.max_depth_used);
    println!("Cover complete: {}", report.complete);
    println!("======================");

    if emit {
        let pre_json = serde_json::to_string_pretty(&report)
            .expect("failed to serialize preliminary deltoid report to JSON");
        let mut hasher = Sha256::new();
        hasher.update(pre_json.as_bytes());
        let digest = format!("{:x}", hasher.finalize());

        report.sha256_digest = Some(digest.clone());

        let json_str = serde_json::to_string_pretty(&report)
            .expect("failed to serialize final deltoid report to JSON");

        let crate_artifact_dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
        fs::create_dir_all(&crate_artifact_dir)
            .expect("failed to create crate artifacts directory");
        let crate_artifact_path = crate_artifact_dir.join("mub_szollosi_deltoid_cover.json");
        fs::write(&crate_artifact_path, &json_str)
            .expect("failed to write crate cover receipt JSON");

        let repo_root = find_repo_root(Path::new(env!("CARGO_MANIFEST_DIR")));
        let repo_artifact_dir = repo_root.join("artifacts");
        fs::create_dir_all(&repo_artifact_dir)
            .expect("failed to create repo artifacts directory");
        let repo_artifact_path = repo_artifact_dir.join("mub_szollosi_deltoid_cover.json");
        fs::write(&repo_artifact_path, &json_str)
            .expect("failed to write repo cover receipt JSON");

        println!();
        println!("Cover receipt emitted:");
        println!("  Crate path: {}", crate_artifact_path.display());
        println!("  Repo path:  {}", repo_artifact_path.display());
        println!("  SHA-256:    {}", digest);
    }

    if !report.complete || report.uncertified_boxes > 0 {
        eprintln!("WARNING: Solver finished with uncertified boxes (depth limit reached).");
        std::process::exit(2);
    }
}