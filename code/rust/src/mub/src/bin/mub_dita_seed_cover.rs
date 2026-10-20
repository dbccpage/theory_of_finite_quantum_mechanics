
use num_rational::BigRational;
use omega_mub::omega_native::campaign::mub6_dita_seed_cover::{
    dita_seed_gauge_fixed_chunk_cover, dita_seed_gauge_fixed_cover_parallel,
    dita_seed_neighborhood_gauge_fixed_chunk_cover,
    dita_seed_neighborhood_gauge_fixed_cover_parallel, genuine_dita_y2q1_triple_seeds_check,
    merge_on_disk_presplit6_chunks_strict, merge_on_disk_presplit6_neighborhood_chunks_strict,
    neighborhood_chunk_filename, neighborhood_delta_1_1000, write_cover_certificate_artifact,
};
use omega_mub::omega_native::exact::mub6_cover_run::CoverCertificate;
use omega_number_theory::rational::ri;

struct DitaCli {
    dx: i64,
    dy: i64,
    presplit: u32,
    depth: u32,
    threads: usize,
    chunk: Option<usize>,
    chunk_end: Option<usize>,
    neighborhood: bool,
    delta_den: i64,
    merge: bool,
}

fn parse_arg_or<T: std::str::FromStr>(args: &[String], idx: usize, default: T) -> T {
    if let Some(s) = args.get(idx) {
        if let Ok(val) = s.parse() {
            return val;
        }
    }
    default
}

fn parse_opt_arg<T: std::str::FromStr>(args: &[String], idx: usize) -> Option<T> {
    if let Some(s) = args.get(idx) {
        return s.parse().ok();
    }
    None
}

fn print_help_and_exit() -> ! {
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

fn apply_kv_flag(cli: &mut DitaCli, args: &[String], i: usize) -> Option<usize> {
    match args[i].as_str() {
        "--dx" => cli.dx = parse_arg_or(args, i + 1, cli.dx),
        "--dy" => cli.dy = parse_arg_or(args, i + 1, cli.dy),
        "--presplit" => cli.presplit = parse_arg_or(args, i + 1, cli.presplit),
        "--depth" => cli.depth = parse_arg_or(args, i + 1, cli.depth),
        "--threads" => cli.threads = parse_arg_or(args, i + 1, cli.threads),
        "--chunk" => cli.chunk = parse_opt_arg(args, i + 1),
        "--chunk-end" => cli.chunk_end = parse_opt_arg(args, i + 1),
        "--delta-den" => cli.delta_den = parse_arg_or(args, i + 1, cli.delta_den),
        _ => return None,
    }
    Some(i + 2)
}

fn apply_bool_flag(cli: &mut DitaCli, flag: &str, i: usize) -> usize {
    match flag {
        "--neighborhood" | "--neigh" => {
            cli.neighborhood = true;
            i + 1
        }
        "--merge" => {
            cli.merge = true;
            i + 1
        }
        "--help" | "-h" => print_help_and_exit(),
        other => {
            eprintln!("unknown arg: {other}");
            std::process::exit(2);
        }
    }
}

fn parse_dita_cli(args: &[String]) -> DitaCli {
    let mut cli = DitaCli {
        dx: 0,
        dy: 8,
        presplit: 6,
        depth: 32,
        threads: 0,
        chunk: None,
        chunk_end: None,
        neighborhood: false,
        delta_den: 1000,
        merge: false,
    };
    let mut i = 1;
    while i < args.len() {
        if let Some(next_i) = apply_kv_flag(&mut cli, args, i) {
            i = next_i;
        } else {
            i = apply_bool_flag(&mut cli, &args[i], i);
        }
    }
    cli
}

fn load_merged_chunks(cli: &DitaCli, delta_tag: &str) -> (CoverCertificate, String, Vec<(usize, String)>) {
    let (dx, dy, delta_den) = (cli.dx, cli.dy, cli.delta_den);
    if cli.neighborhood {
        eprintln!(
            "merging on-disk NEIGH chunks F6({dx},{dy}) delta=1/{delta_den} presplit=6 (enforcing strict bijection & checksum validation)"
        );
        match merge_on_disk_presplit6_neighborhood_chunks_strict(dx, dy, delta_tag) {
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
                format!("dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged_complete.json"),
                csums,
            ),
            Err(e) => {
                eprintln!("strict merge failed: {e}");
                std::process::exit(1);
            }
        }
    }
}

fn run_merge_mode(cli: &DitaCli) {
    let delta_tag = format!("1_{}", cli.delta_den);
    let (cert, fname, checksums) = load_merged_chunks(cli, &delta_tag);
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
            let manifest_fname = format!("{fname}.chunks.sha256");
            let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/omega_mub/artifacts");
            let manifest_path = dir.join(manifest_fname);
            let mut manifest_content = String::new();
            for (idx, sha) in &checksums {
                manifest_content.push_str(&format!("{sha}  chunk{idx}\n"));
            }
            let _ = std::fs::write(&manifest_path, manifest_content);
            if !cert.complete {
                eprintln!("WARNING: merge incomplete (uncertified={})", cert.uncertified);
                std::process::exit(3);
            }
        }
        Err(e) => {
            eprintln!("failed to write merged artifact: {e}");
            std::process::exit(1);
        }
    }
}

fn write_cert_or_exit(cert: &CoverCertificate, fname: &str) {
    match write_cover_certificate_artifact(cert, fname) {
        Ok(path) => println!("{}", path.display()),
        Err(e) => {
            eprintln!("write failed: {e}");
            std::process::exit(1);
        }
    }
}

fn run_single_chunk(cli: &DitaCli, idx: usize, n_chunks: usize, delta: &BigRational, delta_tag: &str) -> bool {
    let (dx, dy, presplit, depth, delta_den) = (cli.dx, cli.dy, cli.presplit, cli.depth, cli.delta_den);
    let (cert, fname) = if cli.neighborhood {
        eprintln!(
            "chunk {idx}/{n_chunks} F6({dx},{dy}) NEIGH delta=1/{delta_den} presplit={presplit} depth={depth}"
        );
        let c = dita_seed_neighborhood_gauge_fixed_chunk_cover(dx, dy, delta, presplit, idx, depth);
        let f = neighborhood_chunk_filename(dx, dy, delta_tag, presplit, idx, depth);
        (c, f)
    } else {
        eprintln!("chunk {idx}/{n_chunks} F6({dx},{dy}) POINT presplit={presplit} depth={depth}");
        let c = dita_seed_gauge_fixed_chunk_cover(dx, dy, presplit, idx, depth);
        let f = format!("dita_seed_F6_{dx}_{dy}_gauge5_presplit{presplit}_chunk{idx}_depth{depth}.json");
        (c, f)
    };
    eprintln!(
        "  complete={} certified={} off_torus={} uncertified={} max_depth={}",
        cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.max_depth_used
    );
    write_cert_or_exit(&cert, &fname);
    cert.complete
}

fn run_chunk_range(cli: &DitaCli, start: usize, delta: &BigRational, delta_tag: &str) {
    let end = cli.chunk_end.unwrap_or(start + 1);
    let n_chunks = 1usize << cli.presplit;
    if start >= n_chunks || end > n_chunks || start >= end {
        eprintln!("invalid chunk range [{start},{end}) for n={n_chunks}");
        std::process::exit(2);
    }
    let mut any_incomplete = false;
    let mut complete_count = 0usize;
    for idx in start..end {
        if run_single_chunk(cli, idx, n_chunks, delta, delta_tag) {
            complete_count += 1;
        } else {
            any_incomplete = true;
        }
    }
    eprintln!(
        "farm done: {}/{} chunks complete in range (neighborhood={})",
        complete_count,
        end - start,
        cli.neighborhood
    );
    if any_incomplete {
        std::process::exit(3);
    }
}

fn write_full_cert_and_check(cert: &CoverCertificate, fname: &str) {
    match write_cover_certificate_artifact(cert, fname) {
        Ok(path) => {
            println!("{}", path.display());
            if !cert.complete {
                eprintln!("WARNING: cover incomplete (uncertified={})", cert.uncertified);
                std::process::exit(3);
            }
        }
        Err(e) => {
            eprintln!("failed to write artifact: {e}");
            std::process::exit(1);
        }
    }
}

fn run_full_cover(cli: &DitaCli, delta: &BigRational, delta_tag: &str) {
    let (dx, dy, presplit, depth, threads, delta_den) = (
        cli.dx,
        cli.dy,
        cli.presplit,
        cli.depth,
        cli.threads,
        cli.delta_den,
    );
    if cli.neighborhood {
        eprintln!(
            "running full gauge-fixed 5-torus NEIGHBORHOOD cover for F6({dx},{dy})+Y2Q1 \
             delta=1/{delta_den} presplit={presplit} depth={depth} threads={threads}"
        );
        let cert = dita_seed_neighborhood_gauge_fixed_cover_parallel(
            dx, dy, delta, presplit, depth, threads,
        );
        eprintln!(
            "done: complete={} certified={} off_torus={} uncertified={} max_depth={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.max_depth_used, cert.min_gap
        );
        let fname = format!(
            "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_presplit{presplit}_depth{depth}.json"
        );
        write_full_cert_and_check(&cert, &fname);
        return;
    }

    eprintln!(
        "running full gauge-fixed 5-torus POINT cover for F6({dx},{dy})+Y2Q1 \
         presplit={presplit} depth={depth} threads={threads}"
    );
    let cert = dita_seed_gauge_fixed_cover_parallel(dx, dy, presplit, depth, threads);
    eprintln!(
        "done: complete={} certified={} off_torus={} uncertified={} max_depth={} min_gap={:?}",
        cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.max_depth_used, cert.min_gap
    );
    let fname = format!("dita_seed_F6_{dx}_{dy}_gauge5_presplit{presplit}_depth{depth}.json");
    write_full_cert_and_check(&cert, &fname);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cli = parse_dita_cli(&args);

    if let Err(msg) = genuine_dita_y2q1_triple_seeds_check(cli.dx, cli.dy) {
        eprintln!("refusing non-genuine seed: {msg}");
        std::process::exit(2);
    }

    if cli.merge {
        run_merge_mode(&cli);
        return;
    }

    let delta: BigRational = if cli.neighborhood {
        if cli.delta_den <= 0 {
            eprintln!("--delta-den must be positive");
            std::process::exit(2);
        }
        ri(1) / ri(cli.delta_den)
    } else {
        neighborhood_delta_1_1000()
    };
    let delta_tag = format!("1_{}", cli.delta_den);

    if let Some(start) = cli.chunk {
        run_chunk_range(&cli, start, &delta, &delta_tag);
        return;
    }

    run_full_cover(&cli, &delta, &delta_tag);
}
