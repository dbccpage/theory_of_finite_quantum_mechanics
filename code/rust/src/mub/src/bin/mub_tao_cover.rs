
use omega_mub::omega_native::exact::mub6_tao_cover::{
    cover_tao_narrow_cell, cover_tao_wide_cell, tao_gauge_fixed_chunk_cover,
    tao_gauge_fixed_cover_parallel, tao_seed_smoke_check, write_kernel_reflection_tao_s6_artifact,
};

struct TaoCli {
    presplit: u32,
    depth: u32,
    threads: usize,
    chunk: Option<usize>,
    chunk_end: Option<usize>,
    run_narrow: bool,
    run_wide: bool,
    emit_complex: bool,
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

fn apply_tao_kv_flag(cli: &mut TaoCli, args: &[String], i: usize) -> Option<usize> {
    match args[i].as_str() {
        "--presplit" => cli.presplit = parse_arg_or(args, i + 1, cli.presplit),
        "--depth" => cli.depth = parse_arg_or(args, i + 1, cli.depth),
        "--threads" => cli.threads = parse_arg_or(args, i + 1, cli.threads),
        "--chunk" => cli.chunk = parse_opt_arg(args, i + 1),
        "--chunk-end" => cli.chunk_end = parse_opt_arg(args, i + 1),
        _ => return None,
    }
    Some(i + 2)
}

fn apply_tao_bool_flag(cli: &mut TaoCli, flag: &str, i: usize) -> usize {
    match flag {
        "--narrow" => cli.run_narrow = true,
        "--wide" => cli.run_wide = true,
        "--complex" | "--emit" => cli.emit_complex = true,
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
    i + 1
}

fn parse_tao_cli(args: &[String]) -> TaoCli {
    let mut cli = TaoCli {
        presplit: 6,
        depth: 24,
        threads: 0,
        chunk: None,
        chunk_end: None,
        run_narrow: false,
        run_wide: false,
        emit_complex: false,
    };
    let mut i = 1;
    while i < args.len() {
        if let Some(next_i) = apply_tao_kv_flag(&mut cli, args, i) {
            i = next_i;
        } else {
            i = apply_tao_bool_flag(&mut cli, &args[i], i);
        }
    }
    cli
}

fn run_tao_chunks(cli: &TaoCli, start_chunk: usize) {
    let end_chunk = cli.chunk_end.unwrap_or(start_chunk + 1);
    let depth = cli.depth;
    println!("Running gauge-fixed 5-torus chunk cover for chunks {start_chunk}..{end_chunk} at depth {depth}...");
    for c in start_chunk..end_chunk {
        let cert = tao_gauge_fixed_chunk_cover(cli.presplit, c, depth);
        println!(
            "Chunk {c}: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
    }
}

fn run_tao_cells(cli: &TaoCli, run_all: bool) {
    if cli.run_narrow || run_all {
        println!("Running narrow cell cover (stated region [26/100, 30/100]^12)...");
        let cert = cover_tao_narrow_cell(cli.depth);
        println!(
            "Narrow cell cover: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
        assert!(cert.complete && cert.uncertified == 0);
    }
    if cli.run_wide || run_all {
        println!("Running wide cell cover (stated region [10/100, 46/100]^12)...");
        let cert = cover_tao_wide_cell(30);
        println!(
            "Wide cell cover: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
        assert!(cert.complete && cert.uncertified == 0);
    }
}

fn run_tao_emit(cli: &TaoCli, run_all: bool) {
    if cli.emit_complex || run_all {
        let presplit = cli.presplit;
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
}

fn run_tao_cells_and_emit(cli: &TaoCli) {
    let run_all = !cli.run_narrow && !cli.run_wide && !cli.emit_complex;
    run_tao_cells(cli, run_all);
    run_tao_emit(cli, run_all);
}

fn main() {
    println!("=== MUB(6) Terence Tao S6 Seed Cover Runner ===");
    println!("AuthorityEffect: None");
    println!("Firewall: stated region only; mints no authority");

    let args: Vec<String> = std::env::args().collect();
    let cli = parse_tao_cli(&args);

    let (smoke_pass, smoke_gap) = tao_seed_smoke_check();
    println!("Smoke check (bad basis box col0 near e0 excluded): {smoke_pass}");
    if let Some(gap) = smoke_gap {
        println!("Smoke vector gap lower bound: {gap}");
    }
    assert!(smoke_pass, "Tao seed smoke check failed");

    if let Some(start_chunk) = cli.chunk {
        run_tao_chunks(&cli, start_chunk);
        return;
    }

    if cli.threads > 0 {
        let (threads, presplit, depth) = (cli.threads, cli.presplit, cli.depth);
        println!("Running parallel cover with {threads} threads, presplit {presplit}, depth {depth}...");
        let cert = tao_gauge_fixed_cover_parallel(presplit, depth, threads);
        println!(
            "Parallel cover: complete={} certified={} off_torus={} uncertified={} min_gap={:?}",
            cert.complete, cert.certified, cert.off_torus, cert.uncertified, cert.min_gap
        );
        return;
    }

    run_tao_cells_and_emit(&cli);

    println!("=== Tao S6 Cover Runner Completed Successfully ===");
}
