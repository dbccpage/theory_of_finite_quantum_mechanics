
use tfqm_mub::native::exact::mub6_cover_run::CoverCertificate;
use tfqm_mub::native::campaign::mub6_dita_seed_cover::narrow_torus_cell;
use tfqm_mub::native::exact::mub6_haagerup_cover::{
    cover_haagerup_gauge_fixed_chunk, cover_haagerup_narrow_cell,
    cover_haagerup_neighborhood_region, cover_haagerup_wide_cell, haagerup_cover_status,
    write_haagerup_reflection_artifact,
};
use engine_number_theory::rational::ri;
use std::path::PathBuf;

fn save_certificate(cert: &CoverCertificate, path: &PathBuf) {
    let json = serde_json::to_string_pretty(cert).expect("serialize certificate");
    std::fs::write(path, json).expect("write certificate file");
}

struct HaagerupCli {
    presplit: u32,
    depth: u32,
    threads: usize,
    chunk: Option<usize>,
    chunk_end: Option<usize>,
    neighborhood: bool,
    delta_den: i64,
    narrow_cell: bool,
    wide_cell: bool,
    emit_reflection: bool,
    status_only: bool,
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

fn apply_kv_flag(cli: &mut HaagerupCli, args: &[String], i: usize) -> Option<usize> {
    match args[i].as_str() {
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

fn apply_bool_flag(cli: &mut HaagerupCli, flag: &str, i: usize) -> usize {
    match flag {
        "--neighborhood" | "--neigh" => cli.neighborhood = true,
        "--narrow-cell" => cli.narrow_cell = true,
        "--wide-cell" => cli.wide_cell = true,
        "--emit-reflection" => cli.emit_reflection = true,
        "--status" => cli.status_only = true,
        "--help" | "-h" => print_help_and_exit(),
        other => {
            eprintln!("unknown argument: {other} (try --help)");
            std::process::exit(2);
        }
    }
    i + 1
}

fn parse_haagerup_cli(args: &[String]) -> HaagerupCli {
    let mut cli = HaagerupCli {
        presplit: 6,
        depth: 32,
        threads: 0,
        chunk: None,
        chunk_end: None,
        neighborhood: false,
        delta_den: 1000,
        narrow_cell: false,
        wide_cell: false,
        emit_reflection: false,
        status_only: false,
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

fn run_cell_covers(cli: &HaagerupCli, artifacts_dir: &PathBuf) {
    if cli.emit_reflection {
        let artifact_path = artifacts_dir.join("kernel_reflection_haagerup_h6_box_cover.json");
        println!(
            "Emitting Lean 4 kernel reflection artifact to {}...",
            artifact_path.display()
        );
        write_haagerup_reflection_artifact(&artifact_path).expect("write reflection artifact");
        println!("Artifact written successfully.");
    }
    if cli.narrow_cell {
        println!("Running narrow cell cover...");
        let cert = cover_haagerup_narrow_cell();
        println!(
            "Narrow cell complete: {}, certified: {}, off_torus: {}, min_gap: {:?}",
            cert.complete, cert.certified, cert.off_torus, cert.min_gap
        );
        let path = artifacts_dir.join("haagerup_h6_narrow_cell_cover.json");
        save_certificate(&cert, &path);
    }
    if cli.wide_cell {
        println!("Running wide cell cover...");
        let cert = cover_haagerup_wide_cell();
        println!(
            "Wide cell complete: {}, certified: {}, off_torus: {}, min_gap: {:?}",
            cert.complete, cert.certified, cert.off_torus, cert.min_gap
        );
        let path = artifacts_dir.join("haagerup_h6_wide_cell_cover.json");
        save_certificate(&cert, &path);
    }
}

fn run_chunk_or_neighborhood(cli: &HaagerupCli, artifacts_dir: &PathBuf) {
    let (presplit, depth, delta_den) = (cli.presplit, cli.depth, cli.delta_den);
    if let Some(c_start) = cli.chunk {
        let c_end = cli.chunk_end.unwrap_or(c_start + 1);
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
    } else if cli.neighborhood {
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

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cli = parse_haagerup_cli(&args);

    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let artifacts_dir = manifest_dir.join("../../tests/mub/artifacts");
    if !artifacts_dir.exists() {
        std::fs::create_dir_all(&artifacts_dir).expect("create artifacts dir");
    }

    if cli.status_only {
        let st = haagerup_cover_status();
        println!("{}", serde_json::to_string_pretty(&st).unwrap());
        return;
    }

    run_cell_covers(&cli, &artifacts_dir);
    run_chunk_or_neighborhood(&cli, &artifacts_dir);
}
