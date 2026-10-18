//! Emit scoped, deterministic diagnostics. See research/mub6_frontier_synthesis.md.
//! AuthorityEffect: None.
use omega_mub::omega_native::mub6_frame_potential;
use std::{fs, path::PathBuf};

fn run() -> Result<(), String> {
    let mut emit = false;
    let mut output = None;
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--emit" => emit = true,
            "--output" => output = Some(PathBuf::from(args.next().ok_or("--output needs a path")?)),
            "--help" | "-h" => {
                println!("usage: mub_frame_potential_verifier [--emit | --output PATH]");
                return Ok(());
            }
            _ => return Err(format!("unknown argument: {arg}")),
        }
    }
    if emit && output.is_some() {
        return Err("choose --emit or --output".into());
    }
    let report = mub6_frame_potential::solve_frame_potential_certificate();
    let bytes = serde_json::to_vec_pretty(&report).map_err(|e| e.to_string())?;
    if let Some(path) = output {
        fs::write(path, &bytes).map_err(|e| e.to_string())?;
    } else if emit {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..");
        for dir in [
            root.join("artifacts"),
            PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts"),
        ] {
            fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
            fs::write(dir.join("mub_frame_potential.json"), &bytes).map_err(|e| e.to_string())?;
        }
    }
    println!("{}", String::from_utf8(bytes).map_err(|e| e.to_string())?);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
