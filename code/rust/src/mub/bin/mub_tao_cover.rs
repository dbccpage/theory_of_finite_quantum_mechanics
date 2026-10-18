
use omega_mub::omega_native::exact::mub6_tao_cover::{
    cover_tao_narrow_cell, cover_tao_wide_cell, tao_gauge_fixed_chunk_cover,
    tao_gauge_fixed_cover_parallel, tao_seed_smoke_check, write_kernel_reflection_tao_s6_artifact,
};

fn main() {
    println!("=== MUB(6) Terence Tao S6 Seed Cover Runner ===");
    println!("AuthorityEffect: None");
    println!("Firewall: stated region only; mints no authority");

    let args: Vec<String> = std::env::args().collect();
    let mut presplit: u32 = 6;
    let mut depth: u32 = 24;
    let mut threads: usize = 0;
    let mut chunk: Option<usize> = None;
    let mut chunk_end: Option<usize> = None;
    let mut run_narrow = false;
    let mut run_wide = false;
    let mut emit_complex = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--presplit" => {
                presplit = args.get(i + 1).and_then(|s| s.parse().ok()).unwrap_or(presplit);
                i += 2;
            }
            "--depth" => {
                depth = args.get(i + 1).and_then(|s| s.parse().ok()).unwrap_or(depth);
                i += 2;
            }
            "--threads" => {
                threads = args.get(i + 1).and_then(|s| s.parse().ok()).unwrap_or(threads);
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
            "--narrow" => {
                run_narrow = true;
                i += 1;
            }
            "--wide" => {
                run_wide = true;
                i += 1;
            }
            "--complex" | "--emit" => {
                emit_complex = true;
                i += 1;
            }
            "--help" | "-h" => {
                eprintln!(
                    "usage: mub_tao_cover [--presplit N] [--depth N] [--threads N] \
                     [--chunk I] [--chunk-end J] [--narrow] [--wide] [--complex]"
                );
                std::process::exit(0);
            }
            other => {
                eprintln!("unknown arg: {other}");
                std::process::exit(2);
            }
        }
    }

    let (smoke_pass, smoke_gap) = tao_seed_smoke_check();
    println!("Smoke check (bad basis box col0 near e0 excluded): {smoke_pass}");
    if let Some(gap) = smoke_gap {
        println!("Smoke vector gap lower bound: {gap}");
    }
    assert!(smoke_pass, "Tao seed smoke check failed");

    if let Some(start_chunk) = chunk {
        let end_chunk = chunk_end.unwrap_or(start_chunk + 1);
        println!("Running gauge-fixed 5-torus chunk cover for chunks {start_chunk}..{end_chunk} at depth {depth}...");
        for c in start_chunk..end_chunk {
            let cert = tao_gauge_fixed_chunk_cover(presplit, c, depth);
            println!(
                "Chunk {c}: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
                cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
            );
        }
        return;
    }

    if threads > 0 {
        println!("Running parallel cover with {threads} threads, presplit {presplit}, depth {depth}...");
        let cert = tao_gauge_fixed_cover_parallel(presplit, depth, threads);
        println!(
            "Parallel cover: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
        return;
    }

    let run_all = !run_narrow && !run_wide && !emit_complex;

    if run_narrow || run_all {
        println!("Running narrow cell cover (stated region [26/100, 30/100]^12)...");
        let cert = cover_tao_narrow_cell(depth);
        println!(
            "Narrow cell cover: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
        assert!(cert.complete && cert.uncertified == 0);
    }

    if run_wide || run_all {
        println!("Running wide cell cover (stated region [10/100, 46/100]^12)...");
        let cert = cover_tao_wide_cell(30);
        println!(
            "Wide cell cover: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
        assert!(cert.complete && cert.uncertified == 0);
    }

    if emit_complex || run_all {
        println!("Emitting kernel reflection scaled complex artifact (presplit={presplit})...");
        match write_kernel_reflection_tao_s6_artifact(presplit) {
            Ok(path) => {
                println!("SUCCESS: Emitted certified artifact at: {}", path.display());
            }
            Err(e) => {
                eprintln!("ERROR emitting artifact: {e}");
                std::process::exit(1);
            }
        }
    }

    println!("=== Tao S6 Cover Runner Completed Successfully ===");
}
